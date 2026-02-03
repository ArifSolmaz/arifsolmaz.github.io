#!/usr/bin/env python3
"""Debug script to inspect arXiv HTML structure."""

import requests
import re

url = "https://arxiv.org/list/astro-ph.EP/new"
print(f"Fetching: {url}\n")

response = requests.get(url, timeout=30)
html = response.text

# Save full HTML for inspection
with open("arxiv_debug.html", "w", encoding="utf-8") as f:
    f.write(html)
print("✅ Saved full HTML to arxiv_debug.html\n")

# Find all h3 tags
print("=" * 60)
print("ALL <h3> TAGS FOUND:")
print("=" * 60)

h3_pattern = r'<h3[^>]*>(.*?)</h3>'
h3_matches = re.findall(h3_pattern, html, re.DOTALL | re.IGNORECASE)

for i, h3 in enumerate(h3_matches):
    clean = ' '.join(h3.split())[:100]
    print(f"[{i+1}] {clean}")

print("\n" + "=" * 60)
print("SEARCHING FOR DATE PATTERNS:")
print("=" * 60)

# Try different date patterns
patterns = [
    r'([A-Za-z]{3},\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})',
    r'(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})',
    r'(Tue|Mon|Wed|Thu|Fri|Sat|Sun)[,\s]+(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})',
]

for pattern in patterns:
    matches = re.findall(pattern, html)
    if matches:
        print(f"\nPattern: {pattern}")
        print(f"Matches: {matches[:5]}")

print("\n" + "=" * 60)
print("LOOKING FOR 'showing X of Y entries':")
print("=" * 60)

entries_pattern = r'showing\s+(\d+)\s+of\s+(\d+)\s+entries'
entries_matches = re.findall(entries_pattern, html, re.IGNORECASE)
print(f"Found: {entries_matches}")

print("\n" + "=" * 60)
print("FIRST 500 CHARS OF HTML:")
print("=" * 60)
print(html[:500])
