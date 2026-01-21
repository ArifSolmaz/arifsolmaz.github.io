#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate AI summaries.

Scrapes the arXiv recent listings page to get actual announcement dates,
then fetches full paper details from the API.
"""

import json
import os
import re
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
    if not text:
        return text
    
    # Remove $ delimiters
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    # Handle uncertainty notation: _{-0.47}^{+0.53} -> (+0.53/-0.47)
    def format_uncertainty(m):
        sub = m.group(1) if m.group(1) else ''
        sup = m.group(2) if m.group(2) else ''
        if sub and sup:
            return f" ({sup}/{sub})"
        elif sup:
            return f"^{sup}"
        elif sub:
            return f"_{sub}"
        return ''
    
    text = re.sub(r'_\{([^}]*)\}\^\{([^}]*)\}', format_uncertainty, text)
    text = re.sub(r'\^\{([^}]*)\}_\{([^}]*)\}', lambda m: f" ({m.group(1)}/{m.group(2)})", text)
    
    # Simple superscripts/subscripts with braces
    text = re.sub(r'\^\{([^}]+)\}', r'^(\1)', text)
    text = re.sub(r'_\{([^}]+)\}', r'_(\1)', text)
    
    # \text{Jup} -> Jup
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\rm\{([^}]+)\}', r'\1', text)
    
    # Common math symbols
    replacements = {
        r'\pm': '±',
        r'\mp': '∓',
        r'\times': '×',
        r'\cdot': '·',
        r'\div': '÷',
        r'\sim': '~',
        r'\approx': '≈',
        r'\simeq': '≃',
        r'\neq': '≠',
        r'\leq': '≤',
        r'\geq': '≥',
        r'\ll': '≪',
        r'\gg': '≫',
        r'\infty': '∞',
        r'\propto': '∝',
        r'\degree': '°',
        r'\deg': '°',
        r'\circ': '°',
        # Greek letters
        r'\alpha': 'α', r'\Alpha': 'Α',
        r'\beta': 'β', r'\Beta': 'Β',
        r'\gamma': 'γ', r'\Gamma': 'Γ',
        r'\delta': 'δ', r'\Delta': 'Δ',
        r'\epsilon': 'ε', r'\varepsilon': 'ε',
        r'\zeta': 'ζ',
        r'\eta': 'η',
        r'\theta': 'θ', r'\Theta': 'Θ',
        r'\iota': 'ι',
        r'\kappa': 'κ',
        r'\lambda': 'λ', r'\Lambda': 'Λ',
        r'\mu': 'μ',
        r'\nu': 'ν',
        r'\xi': 'ξ', r'\Xi': 'Ξ',
        r'\pi': 'π', r'\Pi': 'Π',
        r'\rho': 'ρ',
        r'\sigma': 'σ', r'\Sigma': 'Σ',
        r'\tau': 'τ',
        r'\upsilon': 'υ',
        r'\phi': 'φ', r'\Phi': 'Φ', r'\varphi': 'φ',
        r'\chi': 'χ',
        r'\psi': 'ψ', r'\Psi': 'Ψ',
        r'\omega': 'ω', r'\Omega': 'Ω',
        # Astronomy symbols
        r'\odot': '☉',
        r'\oplus': '⊕',
        r'\otimes': '⊗',
        r'\star': '★',
        # Arrows
        r'\rightarrow': '→',
        r'\leftarrow': '←',
        r'\leftrightarrow': '↔',
        r'\Rightarrow': '⇒',
        # Other
        r'\&': '&',
        r'\ ': ' ',
    }
    
    for latex, symbol in replacements.items():
        text = text.replace(latex, symbol)
    
    # Clean remaining LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
    
    # Remove remaining braces
    text = re.sub(r'[{}]', '', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def is_exoplanet_paper(title: str, abstract: str) -> bool:
    """
    Determine if a paper is about exoplanets.
    Be INCLUSIVE - astro-ph.EP is already planet-focused.
    Only exclude obvious non-exoplanet topics.
    """
    text = f"{title} {abstract}".lower()
    
    # EXCLUDE: obvious non-exoplanet topics in astro-ph.EP
    exclude_keywords = [
        # Solar system specific
        "solar wind", "solar flare", "solar corona", "solar cycle",
        "martian surface", "mars rover", "mars atmosphere",
        "lunar surface", "moon crater", "apollo",
        "venus surface", "venusian",
        "mercury surface",
        "titan lake", "titan atmosphere",
        "io volcano", "europa ocean",
        "saturn ring", "jupiter storm", "jupiter magnetosphere",
        # Small bodies (not planets)
        "asteroid belt", "asteroid family", "near-earth asteroid",
        "meteorite", "meteorites", "meteor shower",
        "kuiper belt object", "trans-neptunian object", "tno",
        "oort cloud",
        # Interstellar objects (not exoplanets)
        "interstellar object", "1i/", "2i/", "3i/",
        "oumuamua", "borisov",
        # Stellar only (no planet connection)
        "stellar occultation", "occultation by",
        "stellar wind", "stellar flare",
        "stellar abundance", "stellar pipeline", "stellar parameter",
        # Debris/dust only
        "debris disk", "dust disk", "zodiacal",
    ]
    
    for kw in exclude_keywords:
        if kw in text:
            # Double-check: if it also mentions exoplanet keywords, include it
            if any(inc in text for inc in ["exoplanet", "extrasolar", "planet formation", "protoplanet"]):
                return True
            return False
    
    # INCLUDE: broad planet-related keywords
    include_keywords = [
        # Direct exoplanet terms
        "exoplanet", "exoplanets", "exoplanetary", "extrasolar",
        # Planet types
        "planet", "planets", "planetary system",
        "jupiter", "neptune", "earth-like", "earth-sized",
        "super-earth", "mini-neptune", "sub-neptune",
        "hot jupiter", "warm jupiter", "cold jupiter",
        "gas giant", "ice giant", "rocky planet", "terrestrial planet",
        "giant planet", "bound planet",
        # Detection methods
        "transit", "transiting", "radial velocity", "rv measurement",
        "microlensing", "direct imaging", "astrometry",
        "planet detection", "planet discovery",
        # Surveys and missions
        "tess", "kepler", "k2", "jwst", "plato", "ariel",
        "toi-", "koi-", "wasp-", "hat-p", "hd ", "gj ", "hip ",
        "trappist", "proxima",
        # Planet properties
        "habitable", "habitability", "biosignature",
        "planet atmosphere", "planetary atmosphere",
        "transmission spectrum", "emission spectrum",
        "planet mass", "planet radius",
        "orbital period", "semi-major axis",
        # Formation and dynamics
        "planet formation", "protoplanet", "planetesimal",
        "planet migration", "orbital migration",
        "mean motion resonance", "orbital resonance",
        "planet-disk", "circumstellar disk",
        "photoevaporation",
        # Host stars
        "planet host", "planet-hosting", "host star",
    ]
    
    for kw in include_keywords:
        if kw in text:
            return True
    
    # Default: if in astro-ph.EP and not excluded, likely relevant
    # But be conservative - require at least some planet connection
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate how 'tweetable' a paper is."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    score = 0
    for keyword, points in TWEETABILITY_KEYWORDS.items():
        if keyword.lower() in text:
            score += points
    return score


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
    
    # Extract paper IDs from the first date's section (the one with "showing X of Y entries")
    # Split by h3 date headers that contain the paper count
    sections = re.split(r'<h3[^>]*>[A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*\(showing', html)
    
    if len(sections) >= 2:
        first_section = sections[1]
    else:
        # Fallback: split by any h3 date header
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
            
            abstract_elem = entry.find('atom:summary', ns)
            abstract = abstract_elem.text if abstract_elem is not None else ""
            abstract = " ".join(abstract.split())
            abstract = clean_latex_abstract(abstract)
            
            # Also clean title
            title = clean_latex_abstract(title)
            
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
        return response.content[0].text
    except Exception as e:
        print(f"Error generating summary for {paper['id']}: {e}")
        return ""


def generate_tweet_hook(client, paper: dict) -> dict:
    """Generate tweet-optimized hook for a paper."""
    prompt = f"""You are writing a Twitter thread hook for an exoplanet research paper.

PAPER TITLE: {paper['title']}
ABSTRACT: {paper['abstract']}

Generate a compelling tweet thread opener. Return JSON with:
1. "hook" - Attention-grabbing sentence (max 100 chars)
2. "claim" - Clear, specific claim about findings (max 150 chars)
3. "evidence" - One key piece of evidence (max 150 chars)
4. "question" - Engaging question for discussion (max 100 chars)

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
    
    # Ensure dates is a list
    if "dates" not in index or not isinstance(index["dates"], list):
        index["dates"] = []
    
    if announcement_date not in index["dates"]:
        index["dates"].append(announcement_date)
        index["dates"].sort(reverse=True)
    
    # Clean output
    clean_index = {"dates": index["dates"]}
    
    with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
        json.dump(clean_index, f, indent=2)
    
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
    
    # Add metadata
    for paper in papers:
        paper["is_exoplanet_focused"] = is_exoplanet_paper(paper["title"], paper["abstract"])
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    # Filter to exoplanet papers only
    exoplanet_papers = [p for p in papers if p["is_exoplanet_focused"]]
    excluded_papers = [p for p in papers if not p["is_exoplanet_focused"]]
    
    # Sort by tweetability
    exoplanet_papers.sort(key=lambda p: -p["tweetability_score"])
    
    # Only keep exoplanet papers
    papers = exoplanet_papers
    
    print(f"\n📊 Paper breakdown:")
    print(f"   🪐 Exoplanet papers: {len(exoplanet_papers)}")
    print(f"   ❌ Excluded: {len(excluded_papers)}")
    if excluded_papers:
        for p in excluded_papers:
            print(f"      - {p['title'][:60]}...")
    
    if len(papers) == 0:
        print("⚠️ No exoplanet papers found in this batch.")
        return
    
    # Load existing data
    existing_papers = {}
    existing_date = None
    
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_papers = {p["id"]: p for p in existing_data.get("papers", [])}
                existing_date = existing_data.get("announcement_date")
        except (json.JSONDecodeError, KeyError):
            pass
    
    # Check if same batch
    if existing_date == announcement_date:
        new_ids = set(p["id"] for p in papers)
        old_ids = set(existing_papers.keys())
        if new_ids == old_ids:
            print(f"\n⏸️  Same papers as before ({announcement_date}). Checking for missing summaries...")
            
            needs_work = False
            for paper in papers:
                if paper["id"] in existing_papers:
                    existing = existing_papers[paper["id"]]
                    if not existing.get("summary_html") or existing["summary_html"] == "<p><em>Summary unavailable.</em></p>":
                        needs_work = True
                        break
                else:
                    needs_work = True
                    break
            
            if not needs_work:
                print("✅ All papers already have summaries. No changes needed.")
                return
    
    print(f"\n📝 Processing {len(papers)} papers for {announcement_date}...")
    
    # Initialize Anthropic client
    client = None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and anthropic:
        client = anthropic.Anthropic(api_key=api_key)
        print("✓ Anthropic client initialized")
    else:
        print("⚠ No ANTHROPIC_API_KEY - summaries will be empty")
    
    # Generate content
    for i, paper in enumerate(papers):
        if paper["id"] in existing_papers:
            existing = existing_papers[paper["id"]]
            has_summary = existing.get("summary_html") and existing["summary_html"] != "<p><em>Summary unavailable.</em></p>"
            has_hook = existing.get("tweet_hook", {}).get("hook")
            
            if has_summary and has_hook:
                paper["summary"] = existing.get("summary", "")
                paper["summary_html"] = existing["summary_html"]
                paper["tweet_hook"] = existing["tweet_hook"]
                paper["figure_url"] = existing.get("figure_url")
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
