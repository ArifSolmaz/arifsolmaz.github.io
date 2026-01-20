#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate AI summaries.

FIXED: Now uses actual arXiv announcement dates instead of script run time.
- Detects when no new papers (holidays, weekends)
- Uses most recent paper's published date as the announcement date
- Preserves existing data when arXiv has no new announcements
"""

import json
import os
import re
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None

# Configuration
ARXIV_CATEGORY = "astro-ph.EP"
MAX_PAPERS = 25
FETCH_MULTIPLIER = 3  # Fetch 3x more to ensure enough after filtering

SCRIPT_DIR = Path(__file__).parent
OUTPUT_FILE = SCRIPT_DIR / "data" / "papers.json"
ARCHIVE_DIR = SCRIPT_DIR / "data" / "archive"
ARCHIVE_INDEX = ARCHIVE_DIR / "index.json"

# Tweetability scoring - higher = more tweetable
TWEETABILITY_KEYWORDS = {
    # High interest discoveries
    "habitable": 15, "earth-like": 15, "earth-sized": 12, "potentially habitable": 20,
    "water": 8, "ocean": 10, "life": 12, "biosignature": 15, "oxygen": 10,
    "jwst": 12, "james webb": 12, "webb telescope": 12,
    "first": 10, "discovery": 8, "detected": 6, "confirmed": 8,
    "nearest": 10, "closest": 10, "proxima": 8,
    "trappist": 10, "kepler": 5, "tess": 5,
    
    # Interesting planet types
    "hot jupiter": 6, "super-earth": 8, "mini-neptune": 6,
    "rogue planet": 12, "free-floating": 10,
    
    # Atmosphere studies
    "atmosphere": 5, "spectrum": 4, "spectroscopy": 4,
    "clouds": 5, "weather": 6, "climate": 5,
    
    # Orbital dynamics
    "migration": 4, "resonance": 4, "tidal": 4,
    
    # Lower interest (but still astro-ph.EP)
    "asteroid": -2, "comet": -2, "kuiper": -3, "debris disk": -2,
    "solar system": -5, "mars": -5, "venus": -3, "jupiter": -2,
}


def clean_latex_name(name: str) -> str:
    """Convert LaTeX escapes to Unicode characters in author names."""
    latex_map = {
        r"\'a": "á", r"\'e": "é", r"\'i": "í", r"\'o": "ó", r"\'u": "ú",
        r'\"a': "ä", r'\"e': "ë", r'\"i': "ï", r'\"o': "ö", r'\"u': "ü",
        r"\v{c}": "č", r"\v{s}": "š", r"\v{z}": "ž", r"\v{r}": "ř",
        r"\'c": "ć", r"\l": "ł", r"\~n": "ñ", r"\c{c}": "ç",
        r"\'A": "Á", r"\'E": "É", r"\'I": "Í", r"\'O": "Ó", r"\'U": "Ú",
        r'\"A': "Ä", r'\"E': "Ë", r'\"I': "Ï", r'\"O': "Ö", r'\"U': "Ü",
    }
    for latex, char in latex_map.items():
        name = name.replace(latex, char)
    name = re.sub(r"\\['\"`^~v]{(\w)}", r"\1", name)
    name = re.sub(r"\\['\"`^~v](\w)", r"\1", name)
    name = re.sub(r"[{}]", "", name)
    return name.strip()


def is_exoplanet_paper(title: str, abstract: str) -> bool:
    """
    Determine if a paper is specifically about exoplanets.
    Uses strict matching to separate exoplanet papers from general planetary science.
    """
    text = f"{title} {abstract}".lower()
    
    strict_exoplanet_keywords = [
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
    
    for keyword in strict_exoplanet_keywords:
        if keyword in text:
            return True
    
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate how 'tweetable' a paper is based on keywords."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    score = 0
    
    for keyword, points in TWEETABILITY_KEYWORDS.items():
        if keyword.lower() in text:
            score += points
    
    return score


def get_announcement_date_from_papers(papers: list[dict]) -> str:
    """
    Determine the arXiv announcement date from paper metadata.
    
    arXiv announces papers at 20:00 ET (01:00 UTC next day).
    The 'published' field gives us when papers were made public.
    """
    if not papers:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Get the most recent paper's published date
    # This represents the arXiv announcement batch
    latest_published = None
    for paper in papers:
        pub_str = paper.get("published", "")
        if pub_str:
            try:
                pub_date = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                if latest_published is None or pub_date > latest_published:
                    latest_published = pub_date
            except ValueError:
                continue
    
    if latest_published:
        # Return just the date part (YYYY-MM-DD)
        return latest_published.strftime("%Y-%m-%d")
    
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def fetch_arxiv_papers(category: str, max_results: int = 15) -> list[dict]:
    """Fetch recent papers from arXiv API and filter for exoplanet content."""
    
    fetch_count = max_results * FETCH_MULTIPLIER
    
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": fetch_count,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    
    all_papers = []
    for entry in root.findall("atom:entry", ns):
        arxiv_id = entry.find("atom:id", ns).text
        paper_id = arxiv_id.split("/abs/")[-1]
        
        title = entry.find("atom:title", ns).text
        title = " ".join(title.split())
        
        abstract = entry.find("atom:summary", ns).text
        abstract = " ".join(abstract.split())
        
        authors = [
            clean_latex_name(author.find("atom:name", ns).text)
            for author in entry.findall("atom:author", ns)
        ]
        
        categories = [
            cat.get("term") 
            for cat in entry.findall("atom:category", ns)
        ]
        
        published = entry.find("atom:published", ns).text
        updated = entry.find("atom:updated", ns).text
        
        pdf_link = f"https://arxiv.org/pdf/{paper_id}.pdf"
        abs_link = f"https://arxiv.org/abs/{paper_id}"
        
        all_papers.append({
            "id": paper_id,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "categories": categories,
            "published": published,
            "updated": updated,
            "pdf_link": pdf_link,
            "abs_link": abs_link
        })
    
    for paper in all_papers:
        paper["is_exoplanet_focused"] = is_exoplanet_paper(paper["title"], paper["abstract"])
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    exoplanet_papers = [p for p in all_papers if p["is_exoplanet_focused"]]
    general_papers = [p for p in all_papers if not p["is_exoplanet_focused"]]
    
    print(f"Fetched {len(all_papers)} total papers:")
    print(f"  🪐 Exoplanet-focused: {len(exoplanet_papers)}")
    print(f"  🔭 General astro-ph.EP: {len(general_papers)}")
    
    exoplanet_papers.sort(key=lambda p: -p["tweetability_score"])
    general_papers.sort(key=lambda p: -p["tweetability_score"])
    
    all_sorted = exoplanet_papers + general_papers
    return all_sorted[:max_results]


def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch the first figure from an arXiv paper's HTML page."""
    try:
        html_url = f"https://arxiv.org/html/{paper_id}"
        response = requests.get(html_url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        html = response.text
        img_patterns = [
            r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*ltx_graphics[^"]*"',
            r'<img[^>]+class="[^"]*ltx_graphics[^"]*"[^>]*src="([^"]+)"',
            r'<figure[^>]*>.*?<img[^>]+src="([^"]+)"',
        ]
        
        for pattern in img_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                img_src = match.group(1)
                if img_src.startswith('/'):
                    img_src = f"https://arxiv.org{img_src}"
                elif not img_src.startswith('http'):
                    img_src = f"https://arxiv.org/html/{paper_id}/{img_src}"
                
                if any(skip in img_src.lower() for skip in ['logo', 'icon', 'badge', 'button']):
                    continue
                    
                return img_src
        
        return None
        
    except Exception as e:
        print(f"  Could not fetch figure for {paper_id}: {e}")
        return None


def get_topic_fallback_image(title: str, abstract: str) -> str:
    """Return a topic-appropriate fallback image URL."""
    text = f"{title} {abstract}".lower()
    
    topic_images = {
        "jwst": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800",
        "james webb": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800",
        "atmosphere": "https://images.unsplash.com/photo-1614642264762-d0a3b8bf3700?w=800",
        "habitable": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=800",
        "earth-like": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=800",
        "hot jupiter": "https://images.unsplash.com/photo-1630839437035-dac17da580d0?w=800",
        "transit": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800",
        "spectrum": "https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=800",
        "star": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800",
    }
    
    for keyword, url in topic_images.items():
        if keyword in text:
            return url
    
    return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800"


def generate_summary(client, paper: dict) -> str:
    """Generate an accessible summary for a paper using Claude."""
    
    prompt = f"""You are a science communicator writing for a general audience. Summarize this exoplanet research paper in an accessible, engaging way.

PAPER TITLE: {paper['title']}

ABSTRACT: {paper['abstract']}

Write an extended summary (250-350 words) with these exact section headers:

**Why It Matters**
Open with the big picture significance—why should a general reader care about this research? Connect it to broader questions about planets, the search for life, or understanding our place in the universe.

**What They Did**
Explain the research methods in simple terms. Avoid jargon entirely, or if you must use a technical term, explain it immediately. Use analogies to everyday concepts when helpful.

**Key Findings**
Describe the main discoveries. What did they actually find? Use concrete numbers or comparisons when possible to make the findings tangible.

**Looking Forward**
End with implications—what does this mean for exoplanet science? What questions does it open up? How might this lead to future discoveries?

Guidelines:
- Write for someone curious about space but with no astronomy background
- Use analogies (e.g., "about the size of Neptune" or "orbiting closer than Mercury does to our Sun")
- Avoid acronyms unless you spell them out
- Be engaging and convey the excitement of discovery
- Keep paragraphs short and readable"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating summary for {paper['id']}: {e}")
        return ""


def generate_tweet_hook(client, paper: dict) -> dict:
    """Generate tweet-optimized hook, evidence, and question for a paper."""
    
    prompt = f"""You are writing a Twitter thread hook for an exoplanet research paper.

PAPER TITLE: {paper['title']}

ABSTRACT: {paper['abstract']}

Generate a compelling tweet thread opener. Return JSON with these fields:

1. "hook" - A single attention-grabbing sentence (max 100 chars) that makes someone want to read more. Start with something surprising or intriguing from the paper.

2. "claim" - A clear, specific claim about what the paper found (max 150 chars). Be concrete.

3. "evidence" - One key piece of evidence or number that supports the claim (max 150 chars).

4. "question" - An engaging question that invites discussion (max 100 chars).

Guidelines:
- Be accurate to the paper's actual findings
- Avoid clickbait but do make it compelling
- Use plain language, no jargon
- Numbers and specifics are good

Return ONLY valid JSON, no other text."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text.strip()
        if content.startswith("```"):
            content = re.sub(r"^```json?\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        
        return json.loads(content)
    except Exception as e:
        print(f"Error generating tweet hook for {paper['id']}: {e}")
        return {"hook": "", "claim": "", "evidence": "", "question": ""}


def format_summary_html(summary: str) -> str:
    """Convert markdown summary to HTML."""
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
            p = p.replace('\n', ' ')
            formatted.append(f'<p>{p}</p>')
    
    return '\n'.join(formatted)


def paper_needs_summary(paper: dict) -> bool:
    """Check if a paper is missing its summary or tweet hook."""
    summary_html = paper.get("summary_html", "")
    has_summary = summary_html and summary_html != "<p><em>Summary unavailable.</em></p>"
    
    tweet_hook = paper.get("tweet_hook", {})
    has_hook = tweet_hook and tweet_hook.get("hook")
    
    return not has_summary or not has_hook


def save_to_archive(papers: list[dict], announcement_date: str):
    """Save papers to the date-based archive."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    archive_file = ARCHIVE_DIR / f"{announcement_date}.json"
    archive_data = {
        "date": announcement_date,
        "paper_count": len(papers),
        "papers": papers
    }
    
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(archive_data, f, indent=2, ensure_ascii=False)
    
    # Update archive index
    if ARCHIVE_INDEX.exists():
        with open(ARCHIVE_INDEX, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {"dates": []}
    
    if announcement_date not in index["dates"]:
        index["dates"].append(announcement_date)
        index["dates"].sort(reverse=True)
        
        with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
    
    print(f"Archived to {archive_file}")


def main():
    """Main function to fetch papers and generate summaries."""
    
    print(f"Fetching papers from arXiv {ARXIV_CATEGORY}...")
    papers = fetch_arxiv_papers(ARXIV_CATEGORY, MAX_PAPERS)
    print(f"Found {len(papers)} papers")
    
    if len(papers) == 0:
        print("No papers found. Exiting.")
        return
    
    # Determine the actual announcement date from paper metadata
    announcement_date = get_announcement_date_from_papers(papers)
    print(f"📅 Announcement date (from papers): {announcement_date}")
    
    # Load existing data
    existing_papers = {}
    existing_ids = set()
    existing_date = None
    
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_ids = {p["id"] for p in existing_data.get("papers", [])}
                existing_papers = {p["id"]: p for p in existing_data.get("papers", [])}
                existing_date = existing_data.get("announcement_date") or existing_data.get("updated_at", "")[:10]
        except (json.JSONDecodeError, KeyError):
            pass
    
    new_paper_ids = {p["id"] for p in papers}
    
    # Check if these are actually new papers or the same batch
    if new_paper_ids == existing_ids:
        # Check if any papers are missing summaries
        papers_missing_summaries = [
            p_id for p_id in new_paper_ids 
            if p_id in existing_papers and paper_needs_summary(existing_papers[p_id])
        ]
        
        if not papers_missing_summaries:
            print("⏸️  No new papers since last update. Same batch as before.")
            print(f"   Previous date: {existing_date}")
            print(f"   Current papers date: {announcement_date}")
            print("   Keeping existing data unchanged (no arXiv announcement today).")
            return
        else:
            print(f"Found {len(papers_missing_summaries)} papers missing summaries. Regenerating...")
    else:
        # New papers detected
        new_count = len(new_paper_ids - existing_ids)
        print(f"📰 Found {new_count} new papers!")
    
    # Initialize Anthropic client
    client = None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and anthropic:
        client = anthropic.Anthropic(api_key=api_key)
        print("✓ Anthropic client initialized")
    else:
        print("⚠ No ANTHROPIC_API_KEY - summaries will be empty")
    
    # Generate summaries
    for i, paper in enumerate(papers):
        # Check if we already have this paper with content
        if paper["id"] in existing_papers:
            existing = existing_papers[paper["id"]]
            has_valid_summary = existing.get("summary_html") and existing["summary_html"] != "<p><em>Summary unavailable.</em></p>"
            has_valid_hook = existing.get("tweet_hook", {}).get("hook")
            
            if has_valid_summary and has_valid_hook:
                paper["summary"] = existing.get("summary", "")
                paper["summary_html"] = existing["summary_html"]
                paper["tweet_hook"] = existing["tweet_hook"]
                paper["figure_url"] = existing.get("figure_url")
                continue
        
        print(f"Generating content {i+1}/{len(papers)}: {paper['id']}")
        
        if client:
            summary = generate_summary(client, paper)
            paper["summary"] = summary
            paper["summary_html"] = format_summary_html(summary)
            
            time.sleep(0.5)
            tweet_hook = generate_tweet_hook(client, paper)
            paper["tweet_hook"] = tweet_hook
            
            if i < len(papers) - 1:
                time.sleep(1)
        else:
            paper["summary"] = ""
            paper["summary_html"] = "<p><em>Summary unavailable.</em></p>"
            paper["tweet_hook"] = {"hook": "", "claim": "", "evidence": "", "question": ""}
    
    # Fetch figures
    print("\nFetching figures for papers...")
    for i, paper in enumerate(papers):
        if paper.get("figure_url"):
            continue
        
        if paper["id"] in existing_papers and existing_papers[paper["id"]].get("figure_url"):
            paper["figure_url"] = existing_papers[paper["id"]]["figure_url"]
            continue
        
        print(f"  [{i+1}/{len(papers)}] Fetching figure for {paper['id']}...")
        
        figure_url = fetch_arxiv_figure(paper["id"])
        
        if figure_url:
            print(f"    ✓ Found arXiv figure")
            paper["figure_url"] = figure_url
        else:
            paper["figure_url"] = get_topic_fallback_image(paper["title"], paper["abstract"])
            print(f"    → Using topic-based fallback")
        
        time.sleep(0.3)
    
    # Prepare output - use announcement_date instead of current time
    output = {
        "updated_at": f"{announcement_date}T20:00:00Z",  # Standard arXiv announcement time
        "announcement_date": announcement_date,
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(papers)} papers to {OUTPUT_FILE}")
    print(f"   Announcement date: {announcement_date}")
    
    # Save to archive
    save_to_archive(papers, announcement_date)


if __name__ == "__main__":
    main()
