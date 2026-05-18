#!/usr/bin/env python3
"""
parse_ideas.py
--------------
Walks the `ideas/` directory of markdown files and produces `data/projects.json`,
a flat catalog of every individual project block.

Supported heading styles:
    ## Project 1: Title
    ## 1. Title

Run from the repo root:
    python scripts/parse_ideas.py
"""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDEAS_DIR = ROOT / "ideas"
DATA_DIR = ROOT / "data"
OUT_FILE = DATA_DIR / "projects.json"

PROJECT_HEADER_RE = re.compile(
    r"^##\s+(?:Project\s+)?(\d+)\s*[:.]\s+(.+?)\s*$",
    re.MULTILINE,
)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def split_projects(text):
    matches = list(PROJECT_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        yield int(m.group(1)), m.group(2).strip(), body


def stable_id(source_file, project_num, title):
    return hashlib.sha256(
        f"{source_file}|{project_num}|{title}".encode("utf-8")
    ).hexdigest()[:10]


def main():
    if not IDEAS_DIR.exists():
        raise SystemExit(f"Ideas directory not found: {IDEAS_DIR}")
    DATA_DIR.mkdir(exist_ok=True)
    catalog = []
    md_files = sorted(IDEAS_DIR.glob("*.md"))
    if not md_files:
        raise SystemExit(f"No .md files in {IDEAS_DIR}")
    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        m = DATE_RE.search(md_path.name)
        source_date = m.group(1) if m else None
        for project_num, title, body_md in split_projects(text):
            catalog.append({
                "id": stable_id(md_path.name, project_num, title),
                "source_file": md_path.name,
                "source_date": source_date,
                "project_num": project_num,
                "title": title,
                "body_md": body_md,
            })
    catalog.sort(
        key=lambda p: (p["source_date"] or "0000-00-00", -p["project_num"]),
        reverse=True,
    )
    OUT_FILE.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Parsed {len(catalog)} projects from {len(md_files)} files.")
    print(f"Wrote {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
