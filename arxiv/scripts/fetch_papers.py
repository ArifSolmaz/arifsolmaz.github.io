#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate accessible AI summaries.
Saves daily archives + updates main papers.json for the current day.

Archive structure:
  data/papers.json          - Current day (for backwards compatibility)
  data/archive/index.json   - List of all available dates
  data/archive/2026-01-19.json - Papers for specific date
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import anthropic
import requests

# Configuration
ARXIV_CATEGORY = "astro-ph.EP"
MAX_PAPERS = 25
FETCH_MULTIPLIER = 6
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "papers.json"
ARCHIVE_DIR = DATA_DIR / "archive"
ARCHIVE_INDEX = ARCHIVE_DIR / "index.json"

# Tweetability scoring
TWEETABILITY_KEYWORDS = {
    "jwst": 20, "james webb": 20, "webb telescope": 20,
    "tess": 10, "kepler": 8, "hubble": 8,
    "habitable": 25, "habitability": 25, "habitable zone": 25,
    "biosignature": 30, "biosignatures": 30, "signs of life": 30,
    "earth-like": 20, "earth-sized": 15, "rocky planet": 15,
    "atmosphere": 10, "atmospheric": 10,
    "water": 12, "ocean": 12,
    "first detection": 20, "first discovery": 20,
    "unprecedented": 15, "breakthrough": 15,
    "trappist-1": 18, "proxima": 15, "proxima centauri": 15,
    "transmission spectrum": 8, "emission spectrum": 8,
    "direct imaging": 10,
}


def is_exoplanet_focused(title: str, abstract: str) -> bool:
    """Check if paper is specifically about exoplanets."""
    text = f"{title} {abstract}".lower()
    
    strict_keywords = [
        "exoplanet", "exoplanets", "exoplanetary",
        "extrasolar planet", "extrasolar planets",
        "hot jupiter", "warm jupiter", "cold jupiter",
        "super-earth", "super earth", "mini-neptune", "sub-neptune",
        "habitable zone", "habitable exoplanet", "habitability",
        "biosignature", "biosignatures",
        "tess planet", "tess candidate", "toi-",
        "kepler planet", "kepler candidate", "kepler-",
        "k2 planet", "k2-",
        "wasp-", "hat-p-", "hatp-",
        "trappist-1", "trappist",
        "proxima centauri b", "proxima b",
        "gj 1214", "gj 436", "hd 189733", "hd 209458",
        "55 cancri", "tau ceti",
        "exoplanet atmosphere", "exoplanetary atmosphere",
        "transmission spectrum", "transmission spectroscopy",
        "planet occurrence", "planet frequency",
        "planet host star", "planet-hosting star",
    ]
    
    return any(keyword in text for keyword in strict_keywords)


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate engagement score."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    return sum(points for keyword, points in TWEETABILITY_KEYWORDS.items() if keyword.lower() in text)


def fetch_via_rss() -> list[dict]:
    """Fetch from RSS feed using requests."""
    print("Trying RSS feed...")
    url = f"https://rss.arxiv.org/rss/{ARXIV_CATEGORY}"
    
    try:
        response = requests.get(url, timeout=30, headers={'User-Agent': 'ExoplanetBot/1.0'})
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        channel = root.find('channel')
        
        if channel is None:
            print("  No channel in RSS")
            return []
        
        papers = []
        for item in channel.findall('item'):
            link = item.find('link')
            if link is None or link.text is None:
                continue
            
            paper_id = link.text.split('/abs/')[-1]
            
            title_elem = item.find('title')
            title = " ".join(title_elem.text.split()) if title_elem is not None and title_elem.text else ""
            
            desc_elem = item.find('description')
            abstract = ""
            if desc_elem is not None and desc_elem.text:
                abstract = re.sub(r'<[^>]+>', '', desc_elem.text)
                abstract = " ".join(abstract.split())
            
            authors = []
            for creator in item.findall('.//{http://purl.org/dc/elements/1.1/}creator'):
                if creator.text:
                    authors.append(creator.text)
            
            pub_date = item.find('pubDate')
            published = pub_date.text if pub_date is not None else ""
            
            papers.append({
                "id": paper_id,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "categories": [ARXIV_CATEGORY],
                "published": published,
                "updated": published,
                "pdf_link": f"https://arxiv.org/pdf/{paper_id}.pdf",
                "abs_link": f"https://arxiv.org/abs/{paper_id}",
            })
        
        print(f"  RSS returned {len(papers)} papers")
        return papers
        
    except Exception as e:
        print(f"  RSS failed: {e}")
        return []


def fetch_via_api(max_results: int) -> list[dict]:
    """Fetch from arXiv API."""
    print("Fetching from API...")
    
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{ARXIV_CATEGORY}",
        "start": 0,
        "max_results": max_results * FETCH_MULTIPLIER,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        
        papers = []
        for entry in root.findall("atom:entry", ns):
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            
            title = entry.find("atom:title", ns).text
            title = " ".join(title.split())
            
            abstract = entry.find("atom:summary", ns).text
            abstract = " ".join(abstract.split())
            
            authors = [
                author.find("atom:name", ns).text 
                for author in entry.findall("atom:author", ns)
            ]
            
            categories = [cat.get("term") for cat in entry.findall("atom:category", ns)]
            
            published = entry.find("atom:published", ns).text
            updated = entry.find("atom:updated", ns).text
            
            papers.append({
                "id": arxiv_id,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "categories": categories,
                "published": published,
                "updated": updated,
                "pdf_link": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "abs_link": f"https://arxiv.org/abs/{arxiv_id}",
            })
        
        print(f"  API returned {len(papers)} papers")
        return papers
        
    except Exception as e:
        print(f"  API failed: {e}")
        return []


def fetch_arxiv_papers(max_results: int = 25) -> list[dict]:
    """Fetch papers from RSS and API, merge results."""
    
    papers = fetch_via_rss()
    api_papers = fetch_via_api(max_results * 2)
    
    existing_ids = {p["id"] for p in papers}
    for p in api_papers:
        if p["id"] not in existing_ids:
            papers.append(p)
            existing_ids.add(p["id"])
    
    if not papers:
        print("WARNING: No papers from RSS or API!")
        return []
    
    for paper in papers:
        paper["is_exoplanet_focused"] = is_exoplanet_focused(paper["title"], paper["abstract"])
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    # Sort by recency (higher arXiv ID = more recent), then exoplanet focus
    def get_arxiv_sortkey(paper):
        try:
            id_part = paper["id"].split("v")[0]
            yymm, num = id_part.split(".")
            return int(yymm) * 100000 + int(num)
        except:
            return 0
    
    papers.sort(key=lambda p: (-get_arxiv_sortkey(p), not p["is_exoplanet_focused"], -p["tweetability_score"]))
    
    return papers[:max_results]


def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch figure from arXiv HTML."""
    try:
        url = f"https://arxiv.org/html/{paper_id}"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            return None
        
        html = response.text
        
        patterns = [
            r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']',
            r'<img[^>]+class=["\'][^"\']*ltx_graphics[^"\']*["\'][^>]+src=["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            if matches:
                img_path = matches[0] if isinstance(matches[0], str) else matches[0][0]
                if img_path.startswith('/'):
                    return f"https://arxiv.org{img_path}"
                elif img_path.startswith('http'):
                    return img_path
                else:
                    return f"https://arxiv.org/html/{paper_id}/{img_path}"
        
        return None
    except Exception:
        return None


def get_topic_fallback_image(title: str, abstract: str) -> str:
    """Get topic-based fallback image."""
    text = f"{title} {abstract}".lower()
    
    if any(k in text for k in ["jwst", "james webb"]):
        return "https://upload.wikimedia.org/wikipedia/commons/f/f0/James_Webb_Space_Telescope_Mirror37.jpg"
    elif any(k in text for k in ["trappist", "habitable"]):
        return "https://upload.wikimedia.org/wikipedia/commons/3/38/TRAPPIST-1e_artist_impression.png"
    elif any(k in text for k in ["hot jupiter", "gas giant"]):
        return "https://upload.wikimedia.org/wikipedia/commons/4/4d/HD_189733b_Exoplanet_atmosphere_%28artist%27s_impression%29.jpg"
    elif any(k in text for k in ["atmosphere", "spectrum"]):
        return "https://upload.wikimedia.org/wikipedia/commons/5/5a/Artist%27s_impression_of_exoplanet_orbiting_two_stars.jpg"
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/8/8f/Exoplanet_Comparison_Kepler-22_b.jpg"


def generate_summary(client: anthropic.Anthropic, paper: dict) -> str:
    """Generate summary using Claude."""
    prompt = f"""Summarize this astronomy paper for a general audience (~300 words):

**Why It Matters** - Big picture significance (2-3 sentences)
**What They Did** - Methods explained simply (2-3 sentences)  
**Key Findings** - Main discoveries (3-4 sentences)
**Looking Forward** - Implications (2-3 sentences)

Title: {paper['title']}
Abstract: {paper['abstract']}

Use the exact headers with ** markers. Be engaging but accurate."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"    Summary failed: {e}")
        return ""


def generate_tweet_hook(client: anthropic.Anthropic, paper: dict) -> dict:
    """Generate tweet hook."""
    prompt = f"""Create a tweet hook for this paper. Return ONLY JSON:
{{"hook": "Attention-grabbing opening (10-15 words)", "claim": "What's new (15-20 words)", "evidence": "Specific finding (15-20 words)", "question": "Discussion invite (10-15 words)"}}

Title: {paper['title']}
Abstract: {paper['abstract']}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text)
    except Exception as e:
        print(f"    Hook failed: {e}")
        return {"hook": "", "claim": "", "evidence": "", "question": ""}


def format_summary_html(summary: str) -> str:
    """Convert markdown to HTML."""
    if not summary:
        return "<p><em>Summary unavailable.</em></p>"
    
    html = re.sub(
        r'\*\*(Why It Matters|What They Did|Key Findings|Looking Forward)\*\*',
        r'<h4>\1</h4>',
        summary
    )
    
    paragraphs = html.split('\n\n')
    formatted = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h4>'):
            formatted.append(p)
        else:
            formatted.append(f'<p>{p.replace(chr(10), " ")}</p>')
    
    return '\n'.join(formatted)


def load_archive_index() -> dict:
    """Load or create archive index."""
    if ARCHIVE_INDEX.exists():
        with open(ARCHIVE_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dates": [], "last_updated": None}


def save_archive_index(index: dict):
    """Save archive index."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def load_all_existing_papers() -> dict:
    """Load all papers from archive for content reuse."""
    all_papers = {}
    
    # Load from main papers.json
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for p in data.get("papers", []):
                    all_papers[p["id"]] = p
        except:
            pass
    
    # Load from archive files
    if ARCHIVE_DIR.exists():
        for archive_file in ARCHIVE_DIR.glob("*.json"):
            if archive_file.name == "index.json":
                continue
            try:
                with open(archive_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for p in data.get("papers", []):
                        if p["id"] not in all_papers:
                            all_papers[p["id"]] = p
            except:
                pass
    
    return all_papers


def main():
    """Main function."""
    print("=" * 60)
    print(f"arXiv {ARXIV_CATEGORY} Paper Fetcher (with Archive)")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Fetch papers
    papers = fetch_arxiv_papers(MAX_PAPERS)
    print(f"\nTotal papers: {len(papers)}")
    
    if not papers:
        print("No papers found. Exiting.")
        return
    
    # Show first few
    print("\nTop papers:")
    for i, p in enumerate(papers[:5]):
        exo = "🪐" if p["is_exoplanet_focused"] else "  "
        print(f"  {exo} {p['id']}: {p['title'][:55]}...")
    
    # Load ALL existing papers for content reuse
    existing_papers = load_all_existing_papers()
    print(f"\nLoaded {len(existing_papers)} existing papers for content reuse")
    
    # Initialize Claude
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key) if api_key else None
    
    if not client:
        print("\n⚠️ ANTHROPIC_API_KEY not set - summaries will be empty")
    
    # Generate content
    print("\nProcessing papers...")
    for i, paper in enumerate(papers):
        # Reuse existing content
        if paper["id"] in existing_papers:
            existing = existing_papers[paper["id"]]
            has_summary = existing.get("summary_html", "").strip() not in ["", "<p><em>Summary unavailable.</em></p>"]
            has_hook = bool(existing.get("tweet_hook", {}).get("hook"))
            
            if has_summary and has_hook:
                print(f"  [{i+1}/{len(papers)}] Reusing: {paper['id']}")
                paper["summary"] = existing.get("summary", "")
                paper["summary_html"] = existing["summary_html"]
                paper["tweet_hook"] = existing["tweet_hook"]
                paper["figure_url"] = existing.get("figure_url", "")
                continue
        
        print(f"  [{i+1}/{len(papers)}] Generating: {paper['id']}")
        
        if client:
            paper["summary"] = generate_summary(client, paper)
            paper["summary_html"] = format_summary_html(paper["summary"])
            time.sleep(0.5)
            paper["tweet_hook"] = generate_tweet_hook(client, paper)
            time.sleep(1)
        else:
            paper["summary"] = ""
            paper["summary_html"] = "<p><em>Summary unavailable.</em></p>"
            paper["tweet_hook"] = {"hook": "", "claim": "", "evidence": "", "question": ""}
    
    # Fetch figures
    print("\nFetching figures...")
    for i, paper in enumerate(papers):
        if paper.get("figure_url"):
            continue
        
        figure_url = fetch_arxiv_figure(paper["id"])
        paper["figure_url"] = figure_url or get_topic_fallback_image(paper["title"], paper["abstract"])
        time.sleep(0.2)
    
    # Prepare output data
    output = {
        "date": today,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    # Save to main papers.json (for backwards compatibility)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved to {OUTPUT_FILE}")
    
    # Save to archive
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_file = ARCHIVE_DIR / f"{today}.json"
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Archived to {archive_file}")
    
    # Update archive index
    index = load_archive_index()
    if today not in index["dates"]:
        index["dates"].insert(0, today)  # Newest first
    index["dates"] = index["dates"][:90]  # Keep last 90 days
    index["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_archive_index(index)
    print(f"✅ Updated archive index ({len(index['dates'])} dates)")
    
    # Summary stats
    exo_count = sum(1 for p in papers if p["is_exoplanet_focused"])
    print(f"\n📊 Summary:")
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"   📄 General astro-ph.EP: {len(papers) - exo_count}")


if __name__ == "__main__":
    main()
