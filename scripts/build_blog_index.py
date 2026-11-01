#!/usr/bin/env python3
"""Build the public blog index from blog/*/index.html (Python standard library only)."""
from pathlib import Path
from html.parser import HTMLParser
import json, re

ROOT = Path(__file__).resolve().parents[1]
class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = {}; self.title = ""; self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key: self.meta[key] = a.get("content", "")
        if tag == "title": self.in_title = True
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

posts = []
for file in sorted((ROOT / "blog").glob("*/index.html")):
    html = file.read_text(encoding="utf-8")
    parser = Metadata(); parser.feed(html)
    title = parser.meta.get("og:title") or parser.title.split("|")[0].strip()
    if not title: continue
    date_match = re.search(r'(20\d{2}-\d{2}-\d{2})', html)
    # Prefer machine-readable article publication date; fallback to human-readable Turkish date.
    date = parser.meta.get("article:published_time", "")[:10]
    if not date:
        m = re.search(r'(\d{1,2})\s+(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+(20\d{2})', html)
        if m:
            months = "Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()
            date = f"{m.group(3)}-{months.index(m.group(2))+1:02d}-{int(m.group(1)):02d}"
    if not date: date = date_match.group(1) if date_match else "1970-01-01"
    posts.append({"title": title, "description": parser.meta.get("description", ""),
                  "date": date, "url": "/blog/" + file.parent.name + "/"})
posts.sort(key=lambda p: (p["date"], p["url"]), reverse=True)
(ROOT / "blog" / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Indexed {len(posts)} blog post(s).")
