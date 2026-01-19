#!/usr/bin/env python3
"""
Generate RSS feed from papers.json
Run after fetch_papers.py to create feed.xml
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import html
import re

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
FEED_FILE = SCRIPT_DIR.parent / "feed.xml"

SITE_URL = "https://arifsolmaz.github.io/arxiv"
FEED_TITLE = "Exoplanet Papers | Daily arXiv Summaries"
FEED_DESCRIPTION = "Daily summaries of exoplanet research papers from arXiv astro-ph.EP, written for general audiences."


def escape_xml(text: str) -> str:
    """Escape special XML characters."""
    if not text:
        return ""
    return html.escape(str(text), quote=True)


def strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text)


def get_safe_id(paper_id: str) -> str:
    """Convert paper ID to URL-safe format."""
    return re.sub(r'[^a-zA-Z0-9]', '-', paper_id)


def generate_rss():
    """Generate RSS feed from papers.json."""
    
    if not PAPERS_FILE.exists():
        print("No papers.json found")
        return
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    papers = data.get("papers", [])
    updated_at = data.get("updated_at", datetime.now(timezone.utc).isoformat())
    
    # Parse date for RSS
    try:
        pub_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
    except:
        pub_date = datetime.now(timezone.utc)
    
    rss_date = pub_date.strftime("%a, %d %b %Y %H:%M:%S %z")
    
    # Build RSS XML
    items = []
    
    for paper in papers[:50]:  # Limit to 50 most recent
        safe_id = get_safe_id(paper["id"])
        paper_url = f"{SITE_URL}#paper-{safe_id}"
        
        # Get summary text (strip HTML)
        summary = strip_html(paper.get("summary_html", ""))
        if not summary:
            summary = paper.get("abstract", "")[:500] + "..."
        
        # Format authors
        authors = paper.get("authors", [])
        if len(authors) > 3:
            author_str = f"{authors[0]} et al."
        else:
            author_str = ", ".join(authors)
        
        # Categories
        categories = paper.get("categories", ["astro-ph.EP"])
        category_tags = "\n".join([f"        <category>{escape_xml(cat)}</category>" for cat in categories])
        
        item = f"""    <item>
      <title>{escape_xml(paper["title"])}</title>
      <link>{paper_url}</link>
      <guid isPermaLink="true">{paper_url}</guid>
      <pubDate>{rss_date}</pubDate>
      <dc:creator>{escape_xml(author_str)}</dc:creator>
      <description><![CDATA[{summary}]]></description>
{category_tags}
    </item>"""
        
        items.append(item)
    
    # Full RSS feed
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape_xml(FEED_TITLE)}</title>
    <link>{SITE_URL}</link>
    <description>{escape_xml(FEED_DESCRIPTION)}</description>
    <language>en-us</language>
    <lastBuildDate>{rss_date}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE_URL}/icon.png</url>
      <title>{escape_xml(FEED_TITLE)}</title>
      <link>{SITE_URL}</link>
    </image>
{chr(10).join(items)}
  </channel>
</rss>
"""
    
    # Write feed
    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    
    print(f"Generated RSS feed with {len(items)} items: {FEED_FILE}")


if __name__ == "__main__":
    generate_rss()
