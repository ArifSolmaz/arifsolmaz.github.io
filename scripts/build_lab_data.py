#!/usr/bin/env python3
"""
Build lab/lab-data.json — the data the lab page renders itself from.

Sources (both already in this repository):
  cv.tex             appointments, funded projects, teaching, memberships
  publications.json  a NASA ADS query response for author "Solmaz, Arif"

Run:  python3 scripts/build_lab_data.py
The lab page falls back to its built-in static content if this file is missing,
so a failed run degrades to "slightly stale", never to a blank page.
"""

import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
CV = ROOT / "cv.tex"
PUBS = ROOT / "publications.json"          # manual ADS export (fallback)
ADS_PUBS = ROOT / "lab" / "ads-publications.json"   # written by scripts/fetch_ads.py
FILTERS = ROOT / "lab" / "publication-filters.json"
OUT = ROOT / "lab" / "lab-data.json"

# ----------------------------------------------------------------- LaTeX bits

def de_tex(text: str) -> str:
    """Turn a LaTeX fragment into plain text."""
    text = re.sub(r"\\href\{([^}]*)\}\{((?:[^{}]|\{[^}]*\})*)\}", r"\2", text)
    text = re.sub(r"\\(textbf|textit|emph|text|underline)\{((?:[^{}]|\{[^}]*\})*)\}", r"\2", text)
    text = text.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
    text = text.replace("\\\\", " ").replace("~", " ")
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def section(cv: str, name: str) -> str:
    """Return the body of \\section{NAME} up to the next \\section, comments stripped."""
    m = re.search(
        r"\\section\{" + re.escape(name) + r"\}(.*?)(?=\\section\{|\\end\{document\})",
        cv, re.S | re.I,
    )
    if not m:
        return ""
    # drop full-line LaTeX comments (e.g. the "% ===== EDUCATION =====" separators)
    return re.sub(r"(?m)^\s*%.*$", "", m.group(1))


def parse_appointments(cv: str):
    body = section(cv, "Academic Appointments")
    out = []
    pattern = re.compile(
        r"\\cventry\{([^}]*)\}\{((?:[^{}]|\{[^}]*\})*)\}\{([^}]*)\}\{([^}]*)\}\s*([^\\]*)", re.S
    )
    for role, org, period, place, blurb in pattern.findall(body):
        out.append({
            "role": de_tex(role),
            "organisation": de_tex(org),
            "period": de_tex(period),
            "location": de_tex(place),
            "note": de_tex(blurb),
        })
    return out


def parse_education(cv: str):
    body = section(cv, "Education")
    out = []
    for degree, org, year, place in re.findall(
        r"\\cventry\{([^}]*)\}\{((?:[^{}]|\{[^}]*\})*)\}\{([^}]*)\}\{([^}]*)\}", body
    ):
        out.append({
            "degree": de_tex(degree),
            "organisation": de_tex(org),
            "year": de_tex(year),
            "location": de_tex(place),
        })
    return out


def parse_projects(cv: str):
    """Funded projects, split into PI/coordinator and team-member roles."""
    body = section(cv, "Funded Projects")
    out = []
    role = "Team member"
    for chunk in re.split(r"(\\textbf\{As [^}]*\}:?)", body):
        header = re.match(r"\\textbf\{As ([^}]*?):?\}:?$", chunk.strip())
        if header:
            label = de_tex(header.group(1)).rstrip(":")
            role = "PI / Coordinator" if "Principal" in label else label
            continue
        for item in re.findall(r"\\item\s+(.*?)(?=\\item|\Z)", chunk, re.S):
            title_m = re.search(r"\\textbf\{((?:[^{}]|\{[^}]*\})*)\}", item)
            if not title_m:
                continue
            rest = item[title_m.end():]
            funder = de_tex(rest.split("\\textit{")[0]).lstrip("-–— ").strip(" .")
            period_m = re.search(r"\\textit\{([^}]*)\}", rest)
            after_period = rest.split("\\\\", 1)
            note = de_tex(after_period[1]) if len(after_period) > 1 else ""
            out.append({
                "title": de_tex(title_m.group(1)),
                "role": role,
                "funder": funder,
                "period": de_tex(period_m.group(1)).strip(" .") if period_m else "",
                "note": note,
            })
    return out


def parse_simple(cv: str, name: str) -> str:
    return de_tex(section(cv, name))


def parse_header(cv: str):
    m = re.search(r"\\makeheader\s*\{([^}]*)\}\s*\{([^}]*)\}\s*\{([^}]*)\}", cv, re.S)
    if not m:
        return {}
    return {"name": de_tex(m.group(1)), "title": de_tex(m.group(2)), "email": de_tex(m.group(3))}


# ------------------------------------------------------------------ ADS bits

ARXIV_ONLY = re.compile(r"^\d{4}arXiv", re.I)

# bibstems that are meetings/abstract services rather than journals
CONFERENCE_STEMS = {"epsc", "dps", "iaus", "aas", "cosp", "lpi", "lpic", "esasp", "adass", "acm"}

# community/decadal white papers, and data catalogues — neither is a journal article
WHITEPAPER_STEMS = {"baas", "astro2020", "astro2010"}
DATASET_STEMS = {"ycat"}

# tidy display names for the journals in this record
JOURNAL_NAMES = {
    "A&A": "Astronomy & Astrophysics", "AnA": "Astronomy & Astrophysics",
    "MNRAS": "MNRAS", "ApJS": "ApJS", "ApJ": "ApJ", "AJ": "AJ",
    "NewA": "New Astronomy", "AstL": "Astronomy Letters",
    "TJAA": "Turkish J. Astronomy & Astrophysics", "arXiv": "arXiv preprint",
}


def classify(bibcode: str, stems, props) -> str:
    """journal | conference | preprint — best available evidence, in that order."""
    upper = [p.upper() for p in props]
    if "REFEREED" in upper:
        return "journal"
    low = [s.lower() for s in stems]
    if any(any(c in s for c in DATASET_STEMS) for s in low):
        return "dataset"
    if any(any(c in s for c in WHITEPAPER_STEMS) for s in low):
        return "whitepaper"
    if any(any(c in s for c in CONFERENCE_STEMS) for s in low):
        return "conference"
    if ARXIV_ONLY.match(bibcode or ""):
        return "preprint"
    if "NOT REFEREED" in upper:
        return "conference"
    return "journal"


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def load_filters() -> dict:
    if not FILTERS.exists():
        return {}
    try:
        return json.loads(FILTERS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"  ! ignoring unreadable publication-filters.json: {exc}")
        return {}


def parse_publications(raw: dict, filters: dict = None):
    """Deduplicate an ADS response, preferring the journal version of each paper."""
    filters = filters or {}
    dropped = set(filters.get("exclude_bibcodes", []))
    resp = raw.get("response", {})
    docs = resp.get("docs", [])
    by_title = {}
    skipped = 0

    for d in docs:
        title = (d.get("title") or [""])[0]
        key = norm_title(title)
        if not key:
            continue
        if d.get("bibcode") in dropped:
            skipped += 1
            continue
        bibcode = d.get("bibcode", "")
        props = [p.upper() for p in d.get("property", [])]
        stems = d.get("bibstem") or []
        kind = classify(bibcode, stems, props)
        stem = stems[0] if stems else ""
        entry = {
            "title": title,
            "year": int(d.get("year") or 0) or None,
            "bibcode": bibcode,
            "doi": (d.get("doi") or [None])[0],
            "journal": d.get("pub") or JOURNAL_NAMES.get(stem, stem),
            "kind": kind,
            "volume": d.get("volume"),
            "page": (d.get("page") or [None])[0],
            "preprint": bool(ARXIV_ONLY.match(bibcode)),
            "refereed": ("REFEREED" in props) if props else None,
            "authors": d.get("author_count"),
        }
        keep = by_title.get(key)
        rank = {"journal": 0, "whitepaper": 1, "conference": 2, "preprint": 3, "dataset": 4}
        if keep is None or rank[entry["kind"]] < rank[keep["kind"]]:
            by_title[key] = entry

    pubs = sorted(
        by_title.values(),
        key=lambda p: (p["year"] or 0, p["bibcode"]),
        reverse=True,
    )
    for p in pubs:
        p["url"] = (
            f"https://doi.org/{p['doi']}" if p["doi"]
            else f"https://ui.adsabs.harvard.edu/abs/{p['bibcode']}/abstract"
        )
    return pubs, int(resp.get("numFound") or len(docs)), skipped


def main():
    cv = CV.read_text(encoding="utf-8") if CV.exists() else ""
    filters = load_filters()

    # An ORCID query returns only what the author has claimed on ORCID, which is
    # usually incomplete; a name query is complete but pulls in other people with
    # the same surname. So we MERGE: ORCID records are the trusted core, the
    # name-search records (minus the collisions listed in the filters) fill the
    # gaps, and exclude_bibcodes removes anything that is not this author.
    RANK = {"journal": 0, "whitepaper": 1, "conference": 2, "preprint": 3, "dataset": 4}

    def parse_source(path):
        if not path.exists():
            return [], 0, 0
        try:
            return parse_publications(json.loads(path.read_text(encoding="utf-8")), filters)
        except (json.JSONDecodeError, KeyError, TypeError) as exc:   # keep the page alive
            print(f"  ! could not parse {path.name}: {exc}")
            return [], 0, 0

    orcid_pubs, orcid_found, _ = parse_source(ADS_PUBS)
    name_pubs, name_found, skipped = parse_source(PUBS)

    merged = {}
    for p in orcid_pubs + name_pubs:            # ORCID first, so it wins ties
        key = norm_title(p["title"])
        keep = merged.get(key)
        if keep is None:
            merged[key] = p
            continue
        # prefer the better publication kind; on a tie prefer the one with a DOI
        if (RANK[p["kind"]], 0 if p["doi"] else 1) < (RANK[keep["kind"]], 0 if keep["doi"] else 1):
            merged[key] = p
    pubs = sorted(merged.values(), key=lambda p: (p["year"] or 0, p["bibcode"]), reverse=True)
    num_found = max(orcid_found, name_found)
    print(f"  publications merged: {len(orcid_pubs)} ORCID + {len(name_pubs)} name-search "
          f"-> {len(pubs)} distinct")

    journals = [p for p in pubs if p["kind"] == "journal"]
    whitepapers = [p for p in pubs if p["kind"] == "whitepaper"]
    conferences = [p for p in pubs if p["kind"] == "conference"]
    preprints = [p for p in pubs if p["kind"] == "preprint"]
    datasets = [p for p in pubs if p["kind"] == "dataset"]

    data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "pi": parse_header(cv),
        "profile": parse_simple(cv, "Profile"),
        "education": parse_education(cv),
        "appointments": parse_appointments(cv),
        "projects": parse_projects(cv),
        "teaching": parse_simple(cv, "Teaching"),
        "memberships": parse_simple(cv, "Professional Memberships"),
        "publications": pubs,
        "journal_articles": journals,
        "white_papers": whitepapers,
        "conference_contributions": conferences,
        "preprints": preprints,
        "datasets": datasets,
        "metrics": {
            "ads_records": num_found,
            "distinct_works": len(pubs),
            "journal_articles": len(journals),
            "white_papers": len(whitepapers),
            "conference_contributions": len(conferences),
            "excluded_by_filter": skipped,
            "latest_year": pubs[0]["year"] if pubs else None,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  wrote {OUT.relative_to(ROOT)}")
    print(f"  {len(pubs)} distinct works ({len(journals)} journal, {len(whitepapers)} white paper, "
          f"{len(conferences)} conference, {len(preprints)} preprint, {len(datasets)} dataset) "
          f"from {num_found} ADS records; {skipped} excluded by filter")
    print(f"  {len(data['projects'])} projects, {len(data['appointments'])} appointments")


if __name__ == "__main__":
    main()
