#!/usr/bin/env python3
"""
Backfill papers from a specific past date.

Usage:
    python backfill_date.py 2026-02-02

This script:
1. Fetches the arXiv "pastweek" page which shows multiple days
2. Extracts papers specifically from the requested date
3. Generates summaries and saves to archive
"""

import json
import os
import re
import sys
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None

# Configuration
ARXIV_CATEGORY = "astro-ph.EP"
PASTWEEK_URL = f"https://arxiv.org/list/{ARXIV_CATEGORY}/pastweek?skip=0&show=500"

# Get the correct arxiv directory (go up from scripts to arxiv)
SCRIPT_DIR = Path(__file__).parent
if SCRIPT_DIR.name == "scripts":
    ARXIV_DIR = SCRIPT_DIR.parent  # arxiv/scripts -> arxiv
else:
    ARXIV_DIR = SCRIPT_DIR  # fallback

OUTPUT_FILE = ARXIV_DIR / "data" / "papers.json"
ARCHIVE_DIR = ARXIV_DIR / "data" / "archive"
ARCHIVE_INDEX = ARCHIVE_DIR / "index.json"

# Import helper functions from fetch_papers if available, otherwise define them
def clean_latex_name(name: str) -> str:
    """Convert LaTeX escapes to Unicode characters."""
    latex_map = {
        r"\'a": "á", r"\'e": "é", r"\'i": "í", r"\'o": "ó", r"\'u": "ú",
        r'\"a': "ä", r'\"e': "ë", r'\"i': "ï", r'\"o': "ö", r'\"u': "ü",
        r"\v{c}": "č", r"\v{s}": "š", r"\v{z}": "ž", r"\v{r}": "ř",
        r"\'c": "ć", r"\l": "ł", r"\~n": "ñ", r"\c{c}": "ç",
    }
    for latex, char in latex_map.items():
        name = name.replace(latex, char)
    name = re.sub(r"\\['\"`^~v]{(\w)}", r"\1", name)
    name = re.sub(r"\\['\"`^~v](\w)", r"\1", name)
    name = re.sub(r"[{}]", "", name)
    return name.strip()


def clean_latex_abstract(text: str) -> str:
    """Convert LaTeX math notation in abstracts to readable text."""
    replacements = [
        (r'\sim', '~'), (r'\times', '×'), (r'\pm', '±'),
        (r'\leq', '≤'), (r'\geq', '≥'), (r'\approx', '≈'),
        (r'\alpha', 'α'), (r'\beta', 'β'), (r'\gamma', 'γ'),
        (r'\delta', 'δ'), (r'\lambda', 'λ'), (r'\mu', 'μ'),
        (r'\sigma', 'σ'), (r'\omega', 'ω'),
        (r'\odot', '☉'), (r'\oplus', '⊕'),
    ]
    for latex, char in replacements:
        text = text.replace(latex, char)
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_exoplanet_focused(paper: dict) -> bool:
    """STRICT filter: Return True only if paper is genuinely about exoplanets."""
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    text = f"{title} {abstract}"
    
    strong_terms = [
        "exoplanet", "exoplanetary", "extrasolar planet",
        "hot jupiter", "warm jupiter", "super-earth", "mini-neptune",
        "habitable zone planet", "transiting planet", "transiting exoplanet",
        "toi-", "wasp-", "hat-p-", "kepler-", "k2-", "trappist-",
    ]
    
    if any(term in text for term in strong_terms):
        return True
    
    solar_system = [
        "mars", "martian", "venus", "mercury", "jupiter", "jovian",
        "saturn", "uranus", "neptune", "pluto", "asteroid", "comet",
        "moon", "lunar", "titan", "europa", "enceladus",
    ]
    
    if any(term in text for term in solar_system):
        if any(s in text for s in ["exoplanet", "extrasolar", "toi-", "wasp-"]):
            return True
        return False
    
    moderate = ["transiting", "radial velocity", "transmission spectrum", 
                "planet mass", "planet radius", "planet formation"]
    missions = ["tess", "kepler", "jwst", "cheops"]
    
    mod_count = sum(1 for kw in moderate if kw in text)
    has_mission = any(m in text for m in missions)
    
    if mod_count >= 2 or (mod_count >= 1 and has_mission):
        return True
    
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate how 'tweetable' a paper is."""
    keywords = {
        "habitable": 15, "earth-like": 15, "jwst": 12, "james webb": 12,
        "discovery": 8, "first": 10, "atmosphere": 5, "water": 8,
    }
    text = f"{paper['title']} {paper['abstract']}".lower()
    return sum(pts for kw, pts in keywords.items() if kw in text)


def get_topic_fallback_image(title: str, abstract: str) -> str:
    """Return a topic-appropriate fallback image URL."""
    text = f"{title} {abstract}".lower()
    if any(w in text for w in ['habitable', 'life', 'biosignature']):
        return "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=800&q=80"
    elif any(w in text for w in ['jwst', 'james webb']):
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80"
    else:
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80"


def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch the first figure from an arXiv paper's HTML page."""
    try:
        html_url = f"https://arxiv.org/html/{paper_id}"
        response = requests.get(html_url, timeout=10)
        if response.status_code != 200:
            return None
        
        html = response.text
        patterns = [
            r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*ltx_graphics[^"]*"',
            r'<img[^>]+class="[^"]*ltx_graphics[^"]*"[^>]*src="([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                img_src = match.group(1)
                if img_src.startswith('/'):
                    img_src = f"https://arxiv.org{img_src}"
                elif not img_src.startswith('http'):
                    img_src = f"https://arxiv.org/html/{paper_id}/{img_src}"
                if 'logo' not in img_src.lower():
                    return img_src
        return None
    except:
        return None


def scrape_papers_for_date(target_date: str) -> list[str]:
    """
    Scrape arXiv pastweek page and extract paper IDs for a specific date.
    
    Args:
        target_date: Date in YYYY-MM-DD format (e.g., "2026-02-02")
    
    Returns:
        List of paper IDs announced on that date
    """
    print(f"📡 Fetching: {PASTWEEK_URL}")
    
    response = requests.get(PASTWEEK_URL, timeout=60)
    response.raise_for_status()
    html = response.text
    
    # Parse target date
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    target_str = target_dt.strftime("%a, %d %b %Y")  # e.g., "Mon, 02 Feb 2026"
    # Also try alternate format with single digit day
    target_str_alt = target_dt.strftime("%a, %-d %b %Y") if os.name != 'nt' else target_dt.strftime("%a, %#d %b %Y")
    
    print(f"🔍 Looking for date: {target_str}")
    
    # Find all date headers in the HTML
    date_pattern = r'<h3[^>]*>([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s*(?:\(showing[^)]+\))?</h3>'
    date_matches = list(re.finditer(date_pattern, html))
    
    if not date_matches:
        print("❌ No date headers found in HTML")
        return []
    
    print(f"📅 Found {len(date_matches)} date sections:")
    for m in date_matches:
        print(f"   - {m.group(1)}")
    
    # Find our target date section
    target_start = None
    target_end = None
    
    for i, match in enumerate(date_matches):
        date_str = match.group(1)
        # Normalize date string for comparison
        try:
            parsed = datetime.strptime(date_str, "%a, %d %b %Y")
            if parsed.strftime("%Y-%m-%d") == target_date:
                target_start = match.end()
                # End is either next date header or end of file
                if i + 1 < len(date_matches):
                    target_end = date_matches[i + 1].start()
                else:
                    target_end = len(html)
                print(f"✅ Found target date section!")
                break
        except ValueError:
            continue
    
    if target_start is None:
        print(f"❌ Date {target_date} not found in pastweek page")
        print("   This date may be too old (arXiv only shows ~1 week)")
        return []
    
    # Extract paper IDs from this section
    section_html = html[target_start:target_end]
    
    id_pattern = r'/abs/(\d{4}\.\d{4,5}(?:v\d+)?)'
    paper_ids = re.findall(id_pattern, section_html)
    
    # Deduplicate while preserving order
    seen = set()
    unique_ids = []
    for pid in paper_ids:
        base_id = re.sub(r'v\d+$', '', pid)
        if base_id not in seen:
            seen.add(base_id)
            unique_ids.append(pid)
    
    print(f"📰 Found {len(unique_ids)} papers for {target_date}")
    
    return unique_ids


def fetch_paper_details(paper_ids: list[str]) -> list[dict]:
    """Fetch full paper details from arXiv API."""
    if not paper_ids:
        return []
    
    papers = []
    
    for i in range(0, len(paper_ids), 50):
        batch = paper_ids[i:i+50]
        id_list = ','.join(batch)
        
        api_url = f"http://export.arxiv.org/api/query?id_list={id_list}&max_results={len(batch)}"
        print(f"  Fetching batch {i//50 + 1}: {len(batch)} papers...")
        
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        for entry in root.findall('atom:entry', ns):
            id_elem = entry.find('atom:id', ns)
            if id_elem is None:
                continue
            
            full_id = id_elem.text
            paper_id = full_id.split('/abs/')[-1] if '/abs/' in full_id else full_id.split('/')[-1]
            
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text if title_elem is not None else ""
            title = clean_latex_abstract(" ".join(title.split()))
            
            abstract_elem = entry.find('atom:summary', ns)
            abstract = abstract_elem.text if abstract_elem is not None else ""
            abstract = clean_latex_abstract(" ".join(abstract.split()))
            
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text:
                    authors.append(clean_latex_name(name_elem.text))
            
            categories = []
            for cat in entry.findall('arxiv:primary_category', ns):
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text[:10] if published_elem is not None else ""
            
            updated_elem = entry.find('atom:updated', ns)
            updated = updated_elem.text[:10] if updated_elem is not None else ""
            
            papers.append({
                "id": paper_id,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "categories": categories if categories else [ARXIV_CATEGORY],
                "published": published,
                "updated": updated,
                "pdf_link": f"https://arxiv.org/pdf/{paper_id}.pdf",
                "abs_link": f"https://arxiv.org/abs/{paper_id}"
            })
        
        if i + 50 < len(paper_ids):
            time.sleep(0.5)
    
    return papers


def generate_summary(client, paper: dict) -> str:
    """Generate an accessible summary using Claude."""
    prompt = f"""You are a science communicator writing for a general audience. Summarize this exoplanet research paper in an accessible, engaging way.

PAPER TITLE: {paper['title']}

ABSTRACT: {paper['abstract']}

Write an extended summary (250-350 words) with these exact section headers:

**Why It Matters**
Open with the big picture significance—why should a general reader care about this research?

**What They Did**
Explain the research methods in simple terms. Avoid jargon entirely.

**Key Findings**
Describe the main discoveries. Use concrete numbers or comparisons when possible.

**Looking Forward**
End with implications—what does this mean for exoplanet science?

Guidelines:
- Write for someone curious about space but with no astronomy background
- Use analogies to everyday concepts
- Avoid acronyms unless you spell them out
- Be engaging and convey the excitement of discovery"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"    Error: {e}")
        return ""


def format_summary_html(summary: str) -> str:
    """Convert markdown summary to HTML."""
    if not summary:
        return "<p><em>Summary unavailable.</em></p>"
    
    # Convert **Section Header** to <h4>
    html = re.sub(
        r'\*\*(Why It Matters|What They Did|Key Findings|Looking Forward)\*\*',
        r'<h4>\1</h4>',
        summary
    )
    
    # Split into paragraphs and format
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


def generate_tweet_hook(client, paper: dict) -> dict:
    """Generate tweet hook content."""
    prompt = f"""Create a tweet hook for this paper. Return JSON:
{{"hook": "attention-grabbing line (max 100 chars)", "claim": "main finding (max 200 chars)", "evidence": "key detail (max 150 chars)", "question": "engaging question (max 100 chars)"}}

Title: {paper['title']}
Abstract: {paper['abstract'][:500]}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    return {"hook": "", "claim": "", "evidence": "", "question": ""}


def save_to_archive(papers: list[dict], announcement_date: str):
    """Save papers to the archive."""
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
    
    if "dates" not in index:
        index["dates"] = []
    
    if announcement_date not in index["dates"]:
        index["dates"].append(announcement_date)
        index["dates"].sort(reverse=True)
    
    index["updated_at"] = datetime.now(timezone.utc).isoformat()
    index["count"] = len(index["dates"])
    
    with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    print(f"📁 Saved to archive: {archive_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python backfill_date.py YYYY-MM-DD")
        print("Example: python backfill_date.py 2026-02-02")
        sys.exit(1)
    
    target_date = sys.argv[1]
    
    # Validate date format
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"❌ Invalid date format: {target_date}")
        print("   Use YYYY-MM-DD format (e.g., 2026-02-02)")
        sys.exit(1)
    
    print(f"\n🔄 Backfilling papers for {target_date}\n")
    
    # Step 1: Get paper IDs for the target date
    paper_ids = scrape_papers_for_date(target_date)
    
    if not paper_ids:
        print("\n❌ No papers found for this date.")
        print("   If the date is more than ~5 days old, it may no longer be on arXiv's pastweek page.")
        sys.exit(1)
    
    # Step 2: Fetch paper details
    print(f"\n📥 Fetching details for {len(paper_ids)} papers...")
    papers = fetch_paper_details(paper_ids)
    
    if not papers:
        print("❌ Could not fetch paper details.")
        sys.exit(1)
    
    # Filter out revised papers
    papers = [p for p in papers if not re.search(r'v[2-9]$', p["id"])]
    print(f"✓ Got {len(papers)} papers (after filtering revisions)")
    
    # Step 3: Classify papers
    print("\n🔬 Classifying papers...")
    for paper in papers:
        paper["is_exoplanet_focused"] = is_exoplanet_focused(paper)
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    exo_count = sum(1 for p in papers if p["is_exoplanet_focused"])
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"   📊 Other: {len(papers) - exo_count}")
    
    # Sort
    papers.sort(key=lambda p: (p["is_exoplanet_focused"], p["tweetability_score"]), reverse=True)
    
    # Step 4: Generate summaries
    client = None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and anthropic:
        client = anthropic.Anthropic(api_key=api_key)
        print("\n✅ Claude API ready")
    else:
        print("\n⚠️ No API key - summaries will be skipped")
        print("   Set ANTHROPIC_API_KEY environment variable to generate summaries")
    
    print("\n📝 Processing papers...")
    for i, paper in enumerate(papers):
        print(f"  [{i+1}/{len(papers)}] {paper['id']}...")
        
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
        
        # Fetch figure
        figure_url = fetch_arxiv_figure(paper["id"])
        paper["figure_url"] = figure_url or get_topic_fallback_image(paper["title"], paper["abstract"])
        time.sleep(0.3)
    
    # Step 5: Save to archive
    save_to_archive(papers, target_date)
    
    print(f"\n✅ Backfill complete!")
    print(f"   📅 Date: {target_date}")
    print(f"   📄 Papers: {len(papers)}")
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"\n📁 Archive file: {ARCHIVE_DIR / f'{target_date}.json'}")


if __name__ == "__main__":
    main()
