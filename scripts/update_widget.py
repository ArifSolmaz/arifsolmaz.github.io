#!/usr/bin/env python3
"""
update_widget.py
----------------
Picks today's exoplanet project deterministically from data/projects.json and
writes daily-idea/widget.html, daily-idea/fragment.html, and daily-idea/state.json.

Determinism: same UTC date always picks the same project (SHA-256 of date string,
mod catalog size). Run again with a custom date for testing:

    python scripts/update_widget.py 2026-08-15
"""
from __future__ import annotations
import hashlib, html, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "projects.json"
WIDGET_DIR = ROOT / "daily-idea"
PAGE_OUT = WIDGET_DIR / "widget.html"
FRAGMENT_OUT = WIDGET_DIR / "fragment.html"
STATE_OUT = WIDGET_DIR / "state.json"


def md_to_html(md):
    lines = md.split("\n")
    out = []
    in_ol = False
    in_ul = False
    in_para = []

    def flush_para():
        if in_para:
            text = " ".join(in_para).strip()
            if text:
                out.append(f"<p>{inline(text)}</p>")
            in_para.clear()

    def close_ol():
        nonlocal in_ol
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    for raw in lines:
        line = raw.rstrip()
        if re.match(r"^---+\s*$", line):
            flush_para(); close_ol(); close_ul()
            out.append("<hr/>")
            continue
        h = re.match(r"^(#{3,4})\s+(.*)$", line)
        if h:
            flush_para(); close_ol(); close_ul()
            level = len(h.group(1))
            out.append(f"<h{level}>{inline(h.group(2))}</h{level}>")
            continue
        nl = re.match(r"^(\d+)\.\s+(.*)$", line)
        if nl:
            flush_para(); close_ul()
            if not in_ol:
                out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(nl.group(2))}</li>")
            continue
        bl = re.match(r"^[-*]\s+(.*)$", line)
        if bl:
            flush_para(); close_ol()
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(bl.group(1))}</li>")
            continue
        if not line.strip():
            flush_para(); close_ol(); close_ul()
            continue
        in_para.append(line.strip())

    flush_para(); close_ol(); close_ul()
    return "\n".join(out)


def pick_for_date(catalog, date_iso):
    digest = hashlib.sha256(date_iso.encode("utf-8")).hexdigest()
    idx = int(digest, 16) % len(catalog)
    return catalog[idx]


def get_section(body_md, name):
    pattern = re.compile(
        rf"###\s+{re.escape(name)}\s*\n(.+?)(?=\n###\s|\Z)",
        re.DOTALL,
    )
    m = pattern.search(body_md)
    return m.group(1).strip() if m else None


def render_fragment(project, date_iso, catalog_size):
    title = html.escape(project["title"])
    body_md = project["body_md"]
    premise = (
        get_section(body_md, "Scientific Premise")
        or get_section(body_md, "Premise")
        or get_section(body_md, "Motivation")
        or ""
    )
    premise_html = md_to_html(premise) if premise else ""
    full_html = md_to_html(body_md)
    source_date = project.get("source_date") or ""
    source_meta = f"Source brief: {source_date}" if source_date else ""

    return (
        '<section class="exo-daily" aria-label="Exoplanet idea of the day">\n'
        '  <header class="exo-daily__head">\n'
        '    <span class="exo-daily__eyebrow">Exoplanet idea of the day</span>\n'
        f'    <time class="exo-daily__date" datetime="{date_iso}">{date_iso}</time>\n'
        '  </header>\n'
        f'  <h2 class="exo-daily__title">{title}</h2>\n'
        '  <div class="exo-daily__premise">\n'
        f'    {premise_html}\n'
        '  </div>\n'
        '  <details class="exo-daily__more">\n'
        '    <summary>Read the full proposal</summary>\n'
        '    <div class="exo-daily__full">\n'
        f'      {full_html}\n'
        '    </div>\n'
        '  </details>\n'
        '  <footer class="exo-daily__foot">\n'
        f'    <span class="exo-daily__meta">{source_meta}</span>\n'
        f'    <span class="exo-daily__meta">Rotates daily &middot; {catalog_size} ideas in the pool</span>\n'
        '  </footer>\n'
        '</section>\n'
    )


def render_page(fragment, project, date_iso):
    title = html.escape(project["title"])
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f'<title>Idea of the day &mdash; {title}</title>\n'
        '<link rel="stylesheet" href="widget.css"/>\n'
        '</head>\n<body>\n'
        f'{fragment}'
        '</body>\n</html>\n'
    )


def main():
    if not DATA_FILE.exists():
        raise SystemExit(f"Catalog missing: {DATA_FILE}. Run parse_ideas.py first.")
    catalog = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if not catalog:
        raise SystemExit("Catalog is empty.")
    date_iso = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).date().isoformat()
    project = pick_for_date(catalog, date_iso)
    WIDGET_DIR.mkdir(exist_ok=True)
    fragment = render_fragment(project, date_iso, len(catalog))
    page = render_page(fragment, project, date_iso)
    FRAGMENT_OUT.write_text(fragment, encoding="utf-8")
    PAGE_OUT.write_text(page, encoding="utf-8")
    STATE_OUT.write_text(
        json.dumps({
            "date": date_iso,
            "picked_id": project["id"],
            "picked_title": project["title"],
            "catalog_size": len(catalog),
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{date_iso}  ->  {project['title']}")


if __name__ == "__main__":
    main()
