#!/usr/bin/env python3
"""
Backfill missing AI content (EN summary, hook, Turkish) across papers.json and
the whole archive. Safe to re-run: complete papers are skipped.

Env:
  ANTHROPIC_API_KEY   required
  BACKFILL_DAYS       only process the newest N archive days (0 = all, default 0)
  BACKFILL_WORKERS    parallel API calls (default 4)
  BACKFILL_FORCE      "1" to regenerate even complete papers
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ai_content  # noqa: E402

DATA_DIR = Path(__file__).parent.parent / "data"
ARCHIVE_DIR = DATA_DIR / "archive"
PAPERS_FILE = DATA_DIR / "papers.json"

DAYS = int(os.environ.get("BACKFILL_DAYS", "0") or 0)
WORKERS = int(os.environ.get("BACKFILL_WORKERS", "4") or 4)
FORCE = os.environ.get("BACKFILL_FORCE") == "1"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    client = ai_content.make_client()
    if not client:
        sys.exit("ANTHROPIC_API_KEY missing or anthropic package not installed")
    print(f"Model: {ai_content.MODEL}  workers: {WORKERS}  days: {DAYS or 'all'}  force: {FORCE}")

    files = sorted(
        (f for f in ARCHIVE_DIR.glob("????-??-??.json")), reverse=True
    )
    if DAYS:
        files = files[:DAYS]
    targets = files + ([PAPERS_FILE] if PAPERS_FILE.exists() else [])

    cache = {}  # paper id -> generated fields (papers repeat in papers.json + archive)
    total = failed = 0

    for f in targets:
        data = load(f)
        papers = data.get("papers", [])
        todo = [p for p in papers if FORCE or not ai_content.is_complete(p)]
        if not todo:
            continue
        print(f"\n{f.name}: {len(todo)}/{len(papers)} papers need content")

        def work(p):
            if p["id"] in cache:
                return p, cache[p["id"]]
            return p, ai_content.generate_all(client, p)

        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for p, res in ex.map(work, todo):
                if res:
                    cache[p["id"]] = res
                    p.update(res)
                    total += 1
                    print(f"  ok  {p['id']}")
                else:
                    failed += 1
        save(f, data)  # save per day so a crash keeps progress

    print(f"\nDone. generated={total} failed={failed}")
    if failed:
        print("Re-run to retry the failed papers.")


if __name__ == "__main__":
    main()
