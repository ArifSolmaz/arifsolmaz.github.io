#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate accessible AI summaries.
Uses RSS feed to get actual arXiv announcement dates.

Archive structure:
  data/papers.json          - Current day (for backwards compatibility)
  data/archive/index.json   - List of all available dates
  data/archive/2026-01-19.json - Papers for specific date

Key feature: announcement_date from RSS pubDate matches arXiv's display exactly.
"""

import json
import os
import re
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime

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

# arXiv RSS feed URL
ARXIV_RSS_URL = f"https://rss.arxiv.org/rss/{ARXIV_CATEGORY}"

# 2026 US Federal Holidays (arXiv follows these)
ARXIV_HOLIDAYS_2026 = {
    "2026-01-01",  # New Year's Day
    "2026-01-19",  # MLK Day
    "2026-02-16",  # Presidents' Day
    "2026-05-25",  # Memorial Day
    "2026-06-19",  # Juneteenth
    "2026-07-03",  # Independence Day (observed)
    "2026-09-07",  # Labor Day
    "2026-11-26",  # Thanksgiving
    "2026-11-27",  # Day after Thanksgiving
    "2026-12-25",  # Christmas
    "2026-12-31",  # New Year's Eve (usually closed)
}

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


def clean_abstract(abstract: str) -> str:
    """
    Remove arXiv metadata prefix from abstract.
    RSS feed often includes: 'arXiv:XXXX.XXXXXvN Announce Type: new/replace Abstract: ...'
    """
    if not abstract:
        return ""
    
    # Pattern to match arXiv metadata prefix
    # Examples:
    #   "arXiv:2510.09841v2 Announce Type: replace Abstract: Planned and future..."
    #   "arXiv:2601.12345 Announce Type: new Abstract: We present..."
    pattern = r'^arXiv:\d+\.\d+(?:v\d+)?\s+Announce Type:\s*(?:new|replace|cross)\s+Abstract:\s*'
    
    cleaned = re.sub(pattern, '', abstract, flags=re.IGNORECASE)
    
    # Also handle case where just "Abstract:" appears at start
    cleaned = re.sub(r'^Abstract:\s*', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()


def clean_latex(text: str) -> str:
    """
    Clean LaTeX escape sequences from author names.
    Examples: Z. Balk\'oov\'a → Z. Balková, M\"uller → Müller
    """
    if not text:
        return ""
    
    # Common LaTeX accent sequences
    replacements = [
        # Acute accents (\'X)
        (r"\'a", "á"), (r"\'e", "é"), (r"\'i", "í"), (r"\'o", "ó"), (r"\'u", "ú"), (r"\'y", "ý"),
        (r"\'A", "Á"), (r"\'E", "É"), (r"\'I", "Í"), (r"\'O", "Ó"), (r"\'U", "Ú"), (r"\'Y", "Ý"),
        (r"\'n", "ń"), (r"\'c", "ć"), (r"\'s", "ś"), (r"\'z", "ź"),
        (r"\'N", "Ń"), (r"\'C", "Ć"), (r"\'S", "Ś"), (r"\'Z", "Ź"),
        # Umlaut/diaeresis (\"X)
        (r"\"a", "ä"), (r"\"e", "ë"), (r"\"i", "ï"), (r"\"o", "ö"), (r"\"u", "ü"), (r"\"y", "ÿ"),
        (r"\"A", "Ä"), (r"\"E", "Ë"), (r"\"I", "Ï"), (r"\"O", "Ö"), (r"\"U", "Ü"), (r"\"Y", "Ÿ"),
        # Grave accents (\`X)
        (r"\`a", "à"), (r"\`e", "è"), (r"\`i", "ì"), (r"\`o", "ò"), (r"\`u", "ù"),
        (r"\`A", "À"), (r"\`E", "È"), (r"\`I", "Ì"), (r"\`O", "Ò"), (r"\`U", "Ù"),
        # Tilde (\~X)
        (r"\~n", "ñ"), (r"\~N", "Ñ"), (r"\~a", "ã"), (r"\~o", "õ"),
        (r"\~A", "Ã"), (r"\~O", "Õ"),
        # Circumflex (\^X)
        (r"\^a", "â"), (r"\^e", "ê"), (r"\^i", "î"), (r"\^o", "ô"), (r"\^u", "û"),
        (r"\^A", "Â"), (r"\^E", "Ê"), (r"\^I", "Î"), (r"\^O", "Ô"), (r"\^U", "Û"),
        # Cedilla (\c{X})
        (r"\c{c}", "ç"), (r"\c{C}", "Ç"),
        # Caron/háček (\v{X})
        (r"\v{c}", "č"), (r"\v{s}", "š"), (r"\v{z}", "ž"), (r"\v{r}", "ř"),
        (r"\v{C}", "Č"), (r"\v{S}", "Š"), (r"\v{Z}", "Ž"), (r"\v{R}", "Ř"),
        # Polish L
        (r"\l", "ł"), (r"\L", "Ł"),
        # Scandinavian
        (r"\o", "ø"), (r"\O", "Ø"), (r"\aa", "å"), (r"\AA", "Å"),
        (r"\ae", "æ"), (r"\AE", "Æ"), (r"\oe", "œ"), (r"\OE", "Œ"),
        # German sharp s
        (r"\ss", "ß"),
    ]
    
    result = text
    for latex, unicode_char in replacements:
        result = result.replace(latex, unicode_char)
    
    # Remove any remaining braces
    result = result.replace("{", "").replace("}", "")
    
    return result


def is_exoplanet_focused(title: str, abstract: str) -> bool:
    """Check if paper is specifically about exoplanets."""
    text = f"{title} {abstract}".lower()
    
    strict_keywords = [
        # Core exoplanet terms
        "exoplanet", "exoplanets", "exoplanetary",
        "extrasolar planet", "extrasolar planets",
        
        # Planet types
        "hot jupiter", "warm jupiter", "cold jupiter",
        "super-earth", "super earth", "mini-neptune", "sub-neptune",
        "earth-like planet", "earth-sized planet",
        "rocky planet", "terrestrial planet",
        "gas giant planet", "ice giant planet",
        
        # Habitability
        "habitable zone", "habitable exoplanet", "habitability",
        "biosignature", "biosignatures",
        
        # Detection methods
        "microlensing planet", "microlensing bound planet",
        "transiting planet", "transiting exoplanet",
        "radial velocity planet",
        "directly imaged planet",
        
        # Surveys & missions with planet context
        "tess planet", "tess candidate", "toi-",
        "kepler planet", "kepler candidate", "kepler-",
        "k2 planet", "k2-",
        
        # Known systems
        "wasp-", "hat-p-", "hatp-",
        "trappist-1", "trappist",
        "proxima centauri b", "proxima b",
        "gj 1214", "gj 436", "hd 189733", "hd 209458",
        "55 cancri", "tau ceti",
        
        # Atmospheres
        "exoplanet atmosphere", "exoplanetary atmosphere",
        "planetary atmosphere",
        "transmission spectrum", "transmission spectroscopy",
        "emission spectrum of",
        
        # Specific contexts
        "planet occurrence", "planet frequency",
        "planet host star", "planet-hosting star",
        "spin-orbit", "orbital obliquity",
        "planet detection", "planet discovery",
        "bound planet",  # for microlensing
    ]
    
    # Check for strict keywords
    if any(keyword in text for keyword in strict_keywords):
        return True
    
    # Additional check: "planet" + specific context words
    if "planet" in text:
        planet_contexts = [
            "detected", "discovered", "confirmed", "candidate",
            "orbiting", "orbit", "transit", "radial velocity",
            "mass", "radius", "density", "atmosphere",
            "formation", "migration", "evolution",
        ]
        if any(ctx in text for ctx in planet_contexts):
            # But exclude solar system contexts
            solar_system = ["mars", "venus", "mercury", "saturn", "neptune", "uranus", "pluto", "asteroid", "comet", "interstellar"]
            if not any(ss in text for ss in solar_system):
                return True
    
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate engagement score."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    return sum(points for keyword, points in TWEETABILITY_KEYWORDS.items() if keyword.lower() in text)


def parse_rss_date(date_str: str) -> str:
    """Parse RSS pubDate to YYYY-MM-DD format."""
    try:
        # RSS date format: "Mon, 19 Jan 2026 00:30:00 -0500"
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"  Warning: Could not parse date '{date_str}': {e}")
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def fetch_via_rss() -> tuple[list[dict], str]:
    """
    Fetch from RSS feed using requests.
    Returns (papers, announcement_date) tuple.
    """
    print("Fetching from RSS feed...")
    print(f"  URL: {ARXIV_RSS_URL}")
    
    try:
        response = requests.get(ARXIV_RSS_URL, timeout=30, headers={'User-Agent': 'ExoplanetBot/1.0'})
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        channel = root.find('channel')
        
        if channel is None:
            print("  No channel in RSS")
            return [], ""
        
        # Get announcement date from channel pubDate (RSS feed's date)
        announcement_date = ""
        pub_date_elem = channel.find('pubDate')
        if pub_date_elem is not None and pub_date_elem.text:
            announcement_date = parse_rss_date(pub_date_elem.text)
            print(f"  RSS pubDate: {pub_date_elem.text}")
            print(f"  Announcement date: {announcement_date}")
        
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
                abstract = clean_abstract(abstract)  # Remove arXiv metadata prefix
            
            authors = []
            for creator in item.findall('.//{http://purl.org/dc/elements/1.1/}creator'):
                if creator.text:
                    authors.append(clean_latex(creator.text))  # Clean LaTeX in author names
            
            # Item's pubDate (same as channel for new announcements)
            item_pub_date = item.find('pubDate')
            published = item_pub_date.text if item_pub_date is not None else ""
            
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
        return papers, announcement_date
        
    except Exception as e:
        print(f"  RSS failed: {e}")
        return [], ""


def fetch_via_api(max_results: int) -> list[dict]:
    """Fetch from arXiv API (fallback)."""
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
            abstract = clean_abstract(abstract)  # Remove arXiv metadata prefix if present
            
            authors = [
                clean_latex(author.find("atom:name", ns).text)
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


def get_last_announcement_date() -> str:
    """Calculate the last valid arXiv announcement date based on schedule."""
    now = datetime.now(timezone.utc)
    
    # arXiv announces at 20:00 ET (01:00 UTC next day)
    # So if it's before 01:00 UTC, the last announcement was yesterday's date
    
    # For calculation purposes, work backwards from current UTC time
    check_date = now.date()
    
    for _ in range(14):  # Check up to 2 weeks back
        date_str = check_date.strftime("%Y-%m-%d")
        weekday = check_date.weekday()
        
        # arXiv doesn't announce on Saturday (5) or Sunday (6)
        # Also no announcements on Friday night (announced papers) or Saturday night
        if weekday in [5, 6]:  # Saturday, Sunday
            check_date -= timedelta(days=1)
            continue
        
        # Check holidays
        if date_str in ARXIV_HOLIDAYS_2026:
            check_date -= timedelta(days=1)
            continue
        
        return date_str
    
    # Fallback to today
    return now.strftime("%Y-%m-%d")


def fetch_arxiv_papers(max_results: int = 25) -> tuple[list[dict], str]:
    """
    Fetch papers from RSS feed (today's announcements).
    Returns (papers, announcement_date) tuple.
    
    IMPORTANT: Only returns papers that pass exoplanet filtering!
    """
    
    # RSS feed contains ONLY papers announced today
    papers, announcement_date = fetch_via_rss()
    
    # If RSS failed or returned no date, calculate it
    if not announcement_date:
        announcement_date = get_last_announcement_date()
        print(f"  Using calculated announcement date: {announcement_date}")
    
    # Only use API as fallback if RSS completely fails
    if not papers:
        print("RSS failed, falling back to API...")
        papers = fetch_via_api(max_results)
        papers = papers[:max_results]
    
    if not papers:
        print("WARNING: No papers from RSS or API!")
        return [], announcement_date
    
    # First pass: tag all papers
    for paper in papers:
        paper["is_exoplanet_focused"] = is_exoplanet_focused(paper["title"], paper["abstract"])
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    # STRICT FILTERING: Only keep papers that are about exoplanets
    # This prevents random machine learning or climate papers from being included
    total_before = len(papers)
    papers = [p for p in papers if p["is_exoplanet_focused"]]
    
    print(f"\n🔬 EXOPLANET FILTER: {total_before} papers → {len(papers)} exoplanet papers")
    if total_before > len(papers):
        excluded = total_before - len(papers)
        print(f"   Excluded {excluded} non-exoplanet papers")
    
    # Sort by tweetability score (most engaging first)
    def get_arxiv_sortkey(paper):
        try:
            id_part = paper["id"].split("v")[0]
            yymm, num = id_part.split(".")
            return int(yymm) * 100000 + int(num)
        except:
            return 0
    
    papers.sort(key=lambda p: (-p["tweetability_score"], -get_arxiv_sortkey(p)))
    
    return papers, announcement_date


def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch figure from arXiv HTML with improved patterns."""
    
    urls_to_try = [
        f"https://arxiv.org/html/{paper_id}",
        f"https://ar5iv.labs.arxiv.org/html/{paper_id}",
    ]
    
    for url in urls_to_try:
        try:
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                continue
            
            html = response.text
            
            # Multiple patterns to try (ordered by specificity)
            patterns = [
                # arXiv HTML beta - figures with ltx_figure class
                r'<figure[^>]*class="[^"]*ltx_figure[^"]*"[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']',
                # Standard figure with img inside
                r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg))["\']',
                # Images with ltx_graphics class
                r'<img[^>]+class=["\'][^"\']*ltx_graphics[^"\']*["\'][^>]+src=["\']([^"\']+)["\']',
                # Any img with figure-like filename
                r'<img[^>]+src=["\']([^"\']*(?:x\d+|figure|fig)[^"\']*\.(?:png|jpg|jpeg|gif|svg))["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                if matches:
                    img_path = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    
                    # Skip icons/logos
                    skip_patterns = ['icon', 'logo', 'arrow', 'button', 'nav', 'menu', '1x1', 'pixel']
                    if any(skip in img_path.lower() for skip in skip_patterns):
                        continue
                    
                    # Convert to absolute URL
                    if img_path.startswith('//'):
                        return f"https:{img_path}"
                    elif img_path.startswith('/'):
                        base = url.split('/html/')[0]
                        return f"{base}{img_path}"
                    elif img_path.startswith('http'):
                        return img_path
                    else:
                        # Relative path - include paper ID folder
                        return f"{url}/{img_path}"
            
        except Exception:
            continue
    
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
    print(f"arXiv {ARXIV_CATEGORY} Paper Fetcher (with Announcement Date)")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    
    # CLEANUP: First, check if existing papers.json has non-exoplanet papers and clean them
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            existing_list = existing_data.get("papers", [])
            
            # Re-check all papers for exoplanet focus
            for p in existing_list:
                p["is_exoplanet_focused"] = is_exoplanet_focused(p["title"], p["abstract"])
            
            non_exo = [p for p in existing_list if not p.get("is_exoplanet_focused", False)]
            if non_exo:
                print(f"\n🧹 CLEANUP: Found {len(non_exo)} non-exoplanet papers in existing data:")
                for p in non_exo:
                    print(f"   ❌ {p['id']}: {p['title'][:50]}...")
                
                # Filter them out and save immediately
                clean_papers = [p for p in existing_list if p.get("is_exoplanet_focused", False)]
                existing_data["papers"] = clean_papers
                existing_data["paper_count"] = len(clean_papers)
                
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                print(f"   ✅ Cleaned papers.json: {len(existing_list)} → {len(clean_papers)} papers")
        except Exception as e:
            print(f"  Warning: Could not clean existing data: {e}")
    
    # Fetch papers with announcement date
    papers, announcement_date = fetch_arxiv_papers(MAX_PAPERS)
    print(f"\nAnnouncement date: {announcement_date}")
    print(f"Total papers: {len(papers)}")
    
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
    
    # Prepare output data with announcement_date
    output = {
        "announcement_date": announcement_date,  # NEW: arXiv announcement date
        "updated_at": datetime.now(timezone.utc).isoformat(),  # When we fetched
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    # Save to main papers.json (for backwards compatibility)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved to {OUTPUT_FILE}")
    
    # Save to archive using announcement_date (not today's date!)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_file = ARCHIVE_DIR / f"{announcement_date}.json"
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Archived to {archive_file}")
    
    # Update archive index
    index = load_archive_index()
    if announcement_date not in index["dates"]:
        index["dates"].insert(0, announcement_date)  # Newest first
    # Sort dates in reverse chronological order
    index["dates"] = sorted(list(set(index["dates"])), reverse=True)[:90]
    index["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_archive_index(index)
    print(f"✅ Updated archive index ({len(index['dates'])} dates)")
    
    # Summary stats
    exo_count = sum(1 for p in papers if p["is_exoplanet_focused"])
    print(f"\n📊 Summary:")
    print(f"   📅 Announcement: {announcement_date}")
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"   📄 General astro-ph.EP: {len(papers) - exo_count}")


if __name__ == "__main__":
    main()
