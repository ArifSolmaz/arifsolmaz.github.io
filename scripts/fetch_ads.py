#!/usr/bin/env python3
"""
Refresh both ORCID and filtered-author lab publication files from NASA ADS.

Identity comes from ORCID, not from the name: an author search for
"Solmaz, Arif" also returns papers by other researchers with that surname.

Environment:
  ADS_API_TOKEN   required — free token from https://ui.adsabs.harvard.edu/user/settings/token
  ADS_QUERY       optional — overrides the default ORCID query
  ADS_ORCID       optional — ORCID to query (default: value in lab/publication-filters.json)

Exit codes: 0 wrote/updated (or unchanged), 1 no token, 2 request failed.
Both cached files are retained if either ADS request fails.
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
NAME_OUT = ROOT / "lab" / "ads-name-publications.json"
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

    name_query = os.environ.get("ADS_NAME_QUERY", "").strip()
    if not name_query:
        name_query = json.loads(FILTERS.read_text(encoding="utf-8")).get("ads_name_query", "").strip()
    if not name_query:
        print("no filtered ADS name query configured")
        return 2

    def fetch(q):
        params = urllib.parse.urlencode({
            "q": q,
            "fl": FIELDS,
            "fq": "database:(astronomy OR physics)",
            "rows": "200",
            "sort": "date desc, bibcode desc",
        })
        request = urllib.request.Request(
            f"{API}?{params}",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        docs = payload.get("response", {}).get("docs", [])
        if not docs:
            raise ValueError(f"ADS query returned no records: {q}")
        payload.setdefault("_meta", {})["query"] = q
        return payload

    try:
        orcid_payload = fetch(query)
        name_payload = fetch(name_query)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        print(f"ADS request failed ({exc}) — keeping both existing publication files")
        return 2

    for path, payload in ((OUT, orcid_payload), (NAME_OUT, name_payload)):
        new_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        if path.exists() and path.read_text(encoding="utf-8") == new_text:
            print(f"{path.name}: {len(payload['response']['docs'])} records, unchanged")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8")
        print(f"{path.name}: {len(payload['response']['docs'])} records written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
