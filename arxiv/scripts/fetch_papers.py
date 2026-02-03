#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate AI summaries.

Scrapes the arXiv recent listings page to get actual announcement dates,
then fetches full paper details from the API.

FIXED: Month transition handling - papers submitted in late month X can be
announced in early month Y. The ID prefix filter now allows both months.
"""

import json
import os
import re
import time
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None

# Configuration
ARXIV_CATEGORY = "astro-ph.EP"
RECENT_URL = f"https://arxiv.org/list/{ARXIV_CATEGORY}/new"

SCRIPT_DIR = Path(__file__).parent.parent  # Go up to arxiv/
OUTPUT_FILE = SCRIPT_DIR / "data" / "papers.json"
ARCHIVE_DIR = SCRIPT_DIR / "data" / "archive"
ARCHIVE_INDEX = ARCHIVE_DIR / "index.json"

# Tweetability scoring
TWEETABILITY_KEYWORDS = {
    "habitable": 15, "earth-like": 15, "earth-sized": 12, "potentially habitable": 20,
    "water": 8, "ocean": 10, "life": 12, "biosignature": 15, "oxygen": 10,
    "jwst": 12, "james webb": 12, "webb telescope": 12,
    "first": 10, "discovery": 8, "detected": 6, "confirmed": 8,
    "nearest": 10, "closest": 10, "proxima": 8,
    "trappist": 10, "kepler": 5, "tess": 5,
    "hot jupiter": 6, "super-earth": 8, "mini-neptune": 6,
    "rogue planet": 12, "free-floating": 10,
    "atmosphere": 5, "spectrum": 4, "spectroscopy": 4,
    "clouds": 5, "weather": 6, "climate": 5,
    "migration": 4, "resonance": 4, "tidal": 4,
}


def clean_latex_name(name: str) -> str:
    """Convert LaTeX escapes to Unicode characters."""
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


def clean_latex_abstract(text: str) -> str:
    """Convert LaTeX math notation in abstracts to readable text."""
    replacements = [
        (r'\sim', '~'),
        (r'\times', '×'),
        (r'\pm', '±'),
        (r'\leq', '≤'),
        (r'\geq', '≥'),
        (r'\approx', '≈'),
        (r'\infty', '∞'),
        (r'\alpha', 'α'),
        (r'\beta', 'β'),
        (r'\gamma', 'γ'),
        (r'\delta', 'δ'),
        (r'\lambda', 'λ'),
        (r'\mu', 'μ'),
        (r'\nu', 'ν'),
        (r'\pi', 'π'),
        (r'\sigma', 'σ'),
        (r'\tau', 'τ'),
        (r'\omega', 'ω'),
        (r'\odot', '☉'),
        (r'\oplus', '⊕'),
        (r'\deg', '°'),
        (r'\AA', 'Å'),
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
    """
    STRICT filter: Return True only if paper is genuinely about exoplanets.
    
    Excludes:
    - Solar system studies (Mars, Venus, asteroids, comets, etc.)
    - Pure disk/ISM chemistry without planet connection
    - Star-only studies
    """
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    text = f"{title} {abstract}"
    
    # STRONG INDICATORS - paper is definitely about exoplanets
    strong_exoplanet_terms = [
        "exoplanet", "exoplanetary", "extrasolar planet",
        "hot jupiter", "warm jupiter", "cold jupiter",
        "super-earth", "super earth", "mini-neptune", "sub-neptune",
        "earth-like planet", "earth-sized planet", "earth-mass planet",
        "habitable zone planet", "habitable exoplanet",
        "transiting planet", "transiting exoplanet",
        "directly imaged planet", "directly-imaged planet",
        "circumbinary planet",
        "toi-", "wasp-", "hat-p-", "hatp-", "hd ", "gj ", "gl ",
        "kepler-", "k2-", "trappist-", "proxima b", "proxima c",
        "koi-", "epic ", "tic ",
        "55 cnc", "55 cancri",
    ]
    
    if any(term in text for term in strong_exoplanet_terms):
        return True
    
    # EXCLUSION: Solar system objects (even if they mention "planet")
    solar_system_terms = [
        "mars", "martian", "venus", "venusian", "mercury", "mercurian",
        "jupiter", "jovian", "saturn", "saturnian", "uranus", "neptune",
        "pluto", "ceres", "vesta", "asteroid", "comet", "kuiper belt",
        "oort cloud", "trans-neptunian", "tno", "centaur",
        "moon", "lunar", "titan", "europa", "enceladus", "ganymede", "io",
        "phobos", "deimos", "triton", "charon",
        "meteor", "meteorite", "bolide", "fireball",
        "9p/tempel", "67p/", "c/2", "p/",
        "interplanetary dust", "zodiacal",
    ]
    
    if any(term in text for term in solar_system_terms):
        # Exception: if it also has strong exoplanet context, keep it
        if any(strong in text for strong in ["exoplanet", "extrasolar", "toi-", "wasp-", "hat-p", "koi-"]):
            return True
        return False
    
    # MODERATE INDICATORS - need multiple or combined with context
    moderate_indicators = [
        "transiting", "transit timing", "ttv",
        "radial velocity", "doppler",
        "transmission spectrum", "emission spectrum",
        "planet mass", "planet radius", "planetary mass", "planetary radius",
        "orbital architecture", "planet migration", "orbital migration",
        "mean motion resonance", "orbital resonance",
        "planet formation", "protoplanet", "planetesimal",
        "circumstellar", "protoplanetary disk",
        "planet-disk interaction", "disk-planet",
        "host star", "planet host", "planet-hosting",
        "m dwarf planet", "m-dwarf planet",
        "photoevaporation", "atmospheric escape",
    ]
    
    moderate_count = sum(1 for kw in moderate_indicators if kw in text)
    
    # Need at least 2 moderate indicators, or 1 moderate + mission name
    missions = ["tess", "kepler", "k2 mission", "jwst", "plato mission", "ariel mission", "cheops"]
    has_mission = any(m in text for m in missions)
    
    if moderate_count >= 2:
        return True
    if moderate_count >= 1 and has_mission:
        return True
    
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate how 'tweetable' a paper is."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    score = 0
    for keyword, points in TWEETABILITY_KEYWORDS.items():
        if keyword.lower() in text:
            score += points
    return score


def get_valid_id_prefixes(announcement_date: str) -> list[str]:
    """
    Get valid arXiv ID prefixes for a given announcement date.
    
    CRITICAL FIX: Papers submitted in late month X can be announced in early month Y.
    For example, papers submitted Jan 30-31 might be announced Feb 2-3.
    
    arXiv ID format: YYMM.NNNNN
    - Papers submitted Jan 30, 2026 → 2601.xxxxx
    - But announced Feb 2, 2026 (after weekend)
    
    This function returns both current and previous month prefixes for
    the first 5 days of any month.
    """
    try:
        date_obj = datetime.strptime(announcement_date, "%Y-%m-%d")
    except ValueError:
        # Fallback: just use current date
        date_obj = datetime.now(timezone.utc)
    
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    
    # Current month prefix
    current_prefix = f"{year % 100:02d}{month:02d}"
    prefixes = [current_prefix]
    
    # If we're in the first 5 days of the month, also allow previous month
    # This handles weekend/holiday gaps at month boundaries
    if day <= 5:
        prev_month = month - 1
        prev_year = year
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
        prev_prefix = f"{prev_year % 100:02d}{prev_month:02d}"
        prefixes.append(prev_prefix)
    
    return prefixes


def scrape_recent_listings() -> tuple[str, list[str]]:
    """
    Scrape arXiv recent listings page to get actual announcement date and paper IDs.
    Returns (announcement_date, list_of_paper_ids).
    """
    print(f"📡 Fetching: {RECENT_URL}")
    
    response = requests.get(RECENT_URL, timeout=30)
    response.raise_for_status()
    html = response.text
    
    # Find the date header that has "(showing X of Y entries)" - this is the actual content section
    date_pattern = r'<h3[^>]*>([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s*\(showing'
    date_match = re.search(date_pattern, html)
    
    if not date_match:
        # Fallback: find any h3 with a date
        date_pattern = r'<h3[^>]*>([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})'
        date_match = re.search(date_pattern, html)
    
    if not date_match:
        # Last fallback: navigation links
        date_pattern2 = r'<li><a[^>]*>([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})</a>'
        date_match = re.search(date_pattern2, html)
    
    if date_match:
        date_str = date_match.group(1)
        try:
            parsed = datetime.strptime(date_str, "%a, %d %b %Y")
            announcement_date = parsed.strftime("%Y-%m-%d")
            print(f"📅 Found announcement date: {announcement_date} ({date_str})")
        except ValueError:
            announcement_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            print(f"⚠️ Could not parse date '{date_str}', using today")
    else:
        announcement_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"⚠️ No date found in HTML, using today: {announcement_date}")
    
    # Find paper count
    count_pattern = r'\(showing\s+(\d+)\s+of\s+(\d+)\s+entries?\)'
    count_match = re.search(count_pattern, html)
    
    if count_match:
        total = int(count_match.group(2))
        print(f"📊 Papers for this date: {total}")
    
    # Extract paper IDs from the first date's section
    sections = re.split(r'<h3[^>]*>[A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*\(showing', html)
    
    if len(sections) >= 2:
        first_section = sections[1]
    else:
        sections = re.split(r'<h3[^>]*>[A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4}', html)
        if len(sections) >= 2:
            first_section = sections[1]
        else:
            first_section = html
    
    id_pattern = r'/abs/(\d{4}\.\d{4,5}(?:v\d+)?)'
    paper_ids = re.findall(id_pattern, first_section)
    
    seen = set()
    unique_ids = []
    for pid in paper_ids:
        base_id = re.sub(r'v\d+$', '', pid)
        if base_id not in seen:
            seen.add(base_id)
            unique_ids.append(pid)
    
    print(f"📰 Found {len(unique_ids)} unique paper IDs")
    
    return announcement_date, unique_ids


def fetch_paper_details(paper_ids: list[str]) -> list[dict]:
    """Fetch full paper details from arXiv API for given paper IDs."""
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
            title = " ".join(title.split())
            title = clean_latex_abstract(title)
            
            abstract_elem = entry.find('atom:summary', ns)
            abstract = abstract_elem.text if abstract_elem is not None else ""
            abstract = " ".join(abstract.split())
            abstract = clean_latex_abstract(abstract)
            
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
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term')
                if term and term not in categories:
                    categories.append(term)
            
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text[:10] if published_elem is not None else ""
            
            updated_elem = entry.find('atom:updated', ns)
            updated = updated_elem.text[:10] if updated_elem is not None else ""
            
            pdf_link = f"https://arxiv.org/pdf/{paper_id}.pdf"
            abs_link = f"https://arxiv.org/abs/{paper_id}"
            
            papers.append({
                "id": paper_id,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "categories": categories if categories else [ARXIV_CATEGORY],
                "published": published,
                "updated": updated,
                "pdf_link": pdf_link,
                "abs_link": abs_link
            })
        
        if i + 50 < len(paper_ids):
            time.sleep(0.5)
    
    return papers


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
    
    if any(word in text for word in ['habitable', 'life', 'biosignature', 'oxygen', 'water', 'ocean']):
        return "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=800&q=80"
    elif any(word in text for word in ['jwst', 'james webb', 'webb telescope', 'infrared']):
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80"
    elif any(word in text for word in ['hot jupiter', 'gas giant', 'giant planet']):
        return "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800&q=80"
    elif any(word in text for word in ['rocky', 'terrestrial', 'earth-like', 'super-earth']):
        return "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800&q=80"
    elif any(word in text for word in ['transit', 'light curve', 'photometry']):
        return "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&q=80"
    elif any(word in text for word in ['atmosphere', 'spectrum', 'spectroscopy']):
        return "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800&q=80"
    elif any(word in text for word in ['disk', 'protoplanetary', 'debris']):
        return "https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=800&q=80"
    else:
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80"


def generate_summary(client, paper: dict) -> str:
    """Generate a summary using Claude API."""
    prompt = f"""You are an expert science communicator writing for astronomy enthusiasts.

Summarize this astronomy paper in 3-4 sentences for a general audience interested in space.

Title: {paper['title']}
Authors: {', '.join(paper['authors'][:5])}
Abstract: {paper['abstract']}

Requirements:
- Start directly with the key finding or discovery
- Explain why this matters for our understanding of planets/space
- Avoid jargon - explain technical terms briefly if needed
- Be engaging but accurate
- Keep to 3-4 sentences total"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"    Error generating summary: {e}")
        return ""


def format_summary_html(summary: str) -> str:
    """Convert summary to HTML with bold terms."""
    if not summary:
        return "<p><em>Summary unavailable.</em></p>"
    
    html = summary
    bold_terms = [
        "exoplanet", "exoplanets", "JWST", "James Webb",
        "habitable", "atmosphere", "transit", "spectrum",
        "TESS", "Kepler", "hot Jupiter", "super-Earth",
    ]
    for term in bold_terms:
        html = re.sub(rf'\b({re.escape(term)})\b', r'<strong>\1</strong>', html, flags=re.IGNORECASE)
    
    paragraphs = html.split('\n\n')
    html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
    
    return html


def generate_tweet_hook(client, paper: dict) -> dict:
    """Generate tweet hook content using Claude API."""
    prompt = f"""You are a science communicator creating a compelling social media hook.

Paper title: {paper['title']}
Abstract: {paper['abstract'][:500]}

Create a tweet hook that will make people want to learn more. Return JSON:
{{
  "hook": "An attention-grabbing first line (max 100 chars)",
  "claim": "The main finding in plain language (max 200 chars)", 
  "evidence": "Key supporting detail (max 150 chars)",
  "question": "An engaging question for readers (max 100 chars)"
}}

Requirements:
- Make it exciting but accurate
- Use everyday language
- Include specific numbers/findings when possible
- The hook should create curiosity"""

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
        return {"hook": "", "claim": "", "evidence": "", "question": ""}
    except Exception as e:
        print(f"    Error generating tweet hook: {e}")
        return {"hook": "", "claim": "", "evidence": "", "question": ""}


def load_existing_papers() -> dict:
    """Load existing papers.json to preserve summaries."""
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {p["id"]: p for p in data.get("papers", [])}
        except Exception:
            pass
    return {}


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
    
    if "dates" not in index or not isinstance(index["dates"], list):
        index["dates"] = []
    
    if announcement_date not in index["dates"]:
        index["dates"].append(announcement_date)
        index["dates"].sort(reverse=True)
    
    # Update metadata
    index["updated_at"] = datetime.now(timezone.utc).isoformat()
    index["count"] = len(index["dates"])
    
    with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    print(f"📁 Archived to {archive_file}")


def main():
    """Main function to fetch papers and generate summaries."""
    
    print(f"🔍 Fetching papers from arXiv ({ARXIV_CATEGORY})...")
    
    # Step 1: Scrape recent listings
    announcement_date, paper_ids = scrape_recent_listings()
    
    if len(paper_ids) == 0:
        print("❌ No papers found on recent listings page.")
        return
    
    # Step 2: Fetch full paper details
    print(f"\n📥 Fetching details for {len(paper_ids)} papers...")
    papers = fetch_paper_details(paper_ids)
    
    if len(papers) == 0:
        print("❌ Could not fetch paper details from API.")
        return
    
    print(f"✓ Got details for {len(papers)} papers")
    
    # FIXED: Allow papers from current OR previous month (for month transitions)
    valid_prefixes = get_valid_id_prefixes(announcement_date)
    print(f"📆 Valid ID prefixes: {valid_prefixes}")
    
    new_papers = []
    old_papers = []
    for paper in papers:
        paper_prefix = paper["id"][:4]  # e.g., "2601" from "2601.12345v1"
        if paper_prefix in valid_prefixes:
            new_papers.append(paper)
        else:
            old_papers.append(paper)
    
    if old_papers:
        print(f"\n🔄 Filtered out {len(old_papers)} old/replacement papers:")
        for p in old_papers[:5]:
            print(f"   - {p['id']}: {p['title'][:50]}...")
        if len(old_papers) > 5:
            print(f"   ... and {len(old_papers) - 5} more")
    
    papers = new_papers
    print(f"📰 Keeping {len(papers)} new papers from {announcement_date}")
    
    # Filter out REVISED papers (v2, v3, etc.)
    revised_papers = [p for p in papers if re.search(r'v[2-9]$', p["id"])]
    if revised_papers:
        print(f"\n🔄 Filtered out {len(revised_papers)} revised papers:")
        for p in revised_papers[:3]:
            print(f"   - {p['id']}: {p['title'][:50]}...")
        papers = [p for p in papers if not re.search(r'v[2-9]$', p["id"])]
    
    if len(papers) == 0:
        print("❌ No new papers after filtering.")
        return
    
    # Classify papers
    print("\n🔬 Classifying papers...")
    for paper in papers:
        paper["is_exoplanet_focused"] = is_exoplanet_focused(paper)
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    exo_count = sum(1 for p in papers if p["is_exoplanet_focused"])
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"   📊 Other astro-ph.EP: {len(papers) - exo_count}")
    
    # Sort by tweetability
    papers.sort(key=lambda p: (p["is_exoplanet_focused"], p["tweetability_score"]), reverse=True)
    
    # Load existing papers to reuse summaries
    existing_papers = load_existing_papers()
    
    # Initialize Claude client
    client = None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and anthropic:
        client = anthropic.Anthropic(api_key=api_key)
        print("\n✅ Claude API ready")
    else:
        print("\n⚠️ No API key - summaries will be skipped")
    
    # Generate summaries
    print("\n📝 Processing papers...")
    for i, paper in enumerate(papers):
        # Reuse existing content if available
        if paper["id"] in existing_papers:
            existing = existing_papers[paper["id"]]
            has_summary = existing.get("summary_html", "").strip() not in ["", "<p><em>Summary unavailable.</em></p>"]
            has_hook = bool(existing.get("tweet_hook", {}).get("hook"))
            
            if has_summary:
                paper["summary"] = existing.get("summary", "")
                paper["summary_html"] = existing["summary_html"]
            if has_hook:
                paper["tweet_hook"] = existing["tweet_hook"]
            if existing.get("figure_url"):
                paper["figure_url"] = existing["figure_url"]
            
            if has_summary and has_hook:
                print(f"  [{i+1}/{len(papers)}] {paper['id']} - reusing existing content")
                continue
        
        print(f"  [{i+1}/{len(papers)}] {paper['id']} - generating new content...")
        
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
    print("\n🖼️  Fetching figures...")
    for i, paper in enumerate(papers):
        if paper.get("figure_url"):
            continue
        
        if paper["id"] in existing_papers and existing_papers[paper["id"]].get("figure_url"):
            paper["figure_url"] = existing_papers[paper["id"]]["figure_url"]
            continue
        
        figure_url = fetch_arxiv_figure(paper["id"])
        if figure_url:
            paper["figure_url"] = figure_url
        else:
            paper["figure_url"] = get_topic_fallback_image(paper["title"], paper["abstract"])
        
        time.sleep(0.3)
    
    # Save output
    output = {
        "announcement_date": announcement_date,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(papers)} papers to {OUTPUT_FILE}")
    print(f"   📅 Announcement date: {announcement_date}")
    
    # Save to archive
    save_to_archive(papers, announcement_date)


if __name__ == "__main__":
    main()
