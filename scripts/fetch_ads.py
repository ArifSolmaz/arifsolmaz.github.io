#!/usr/bin/env python3
"""
Refresh lab/ads-publications.json from NASA ADS.

Identity comes from ORCID, not from the name: an author search for
"Solmaz, Arif" also returns papers by other researchers with that surname.

Environment:
  ADS_API_TOKEN   required — free token from https://ui.adsabs.harvard.edu/user/settings/token
  ADS_QUERY       optional — overrides the default ORCID query
  ADS_ORCID       optional — ORCID to query (default: value in lab/publication-filters.json)

Exit codes: 0 wrote/updated (or unchanged), 1 no token, 2 request failed.
The lab page keeps working from the previous file if this fails.
"""

import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "lab" / "ads-publications.json"
FILTERS = ROOT / "lab" / "publication-filters.json"

FIELDS = ",".join([
    "bibcode", "title", "year", "pub", "volume", "page", "doi",
    "bibstem", "database", "property", "author_count", "first_author",
])
API = "https://api.adsabs.harvard.edu/v1/search/query"


def default_orcid() -> str:
    if FILTERS.exists():
        try:
            return json.loads(FILTERS.read_text(encoding="utf-8")).get("orcid", "")
        except json.JSONDecodeError:
            pass
    return ""


def main() -> int:
    token = os.environ.get("ADS_API_TOKEN", "").strip()
    if not token:
        print("no ADS_API_TOKEN set — keeping the existing publication file")
        return 1

    orcid = os.environ.get("ADS_ORCID", "").strip() or default_orcid()
    query = os.environ.get("ADS_QUERY", "").strip()
    if not query:
        if not orcid:
            print("no ORCID and no ADS_QUERY — nothing to search for")
            return 2
        query = f'orcid:"{orcid}"'

    params = urllib.parse.urlencode({
        "q": query,
        "fl": FIELDS,
        "fq": "database:(astronomy OR physics)",
        "rows": "200",
        "sort": "date desc",
    })
    request = urllib.request.Request(
        f"{API}?{params}",
        headers={"Authorization": f"Bearer {token}"},
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        print(f"ADS request failed ({exc}) — keeping the existing publication file")
        return 2

    found = payload.get("response", {}).get("numFound", 0)
    if not found:
        print(f"query returned no records: {query} — refusing to overwrite with an empty list")
        return 2

    payload.setdefault("_meta", {})["query"] = query
    new_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    if OUT.exists() and OUT.read_text(encoding="utf-8") == new_text:
        print(f"{found} records — unchanged")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new_text, encoding="utf-8")
    print(f"{found} records written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
