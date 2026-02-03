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
    
    # Symbol replacements
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
        (r'\eta', 'η'),
        (r'\lambda', 'λ'),
        (r'\mu', 'μ'),
        (r'\nu', 'ν'),
        (r'\pi', 'π'),
        (r'\rho', 'ρ'),
        (r'\sigma', 'σ'),
        (r'\tau', 'τ'),
        (r'\omega', 'ω'),
        (r'\Omega', 'Ω'),
        (r'\odot', '☉'),
        (r'\oplus', '⊕'),
        (r'\deg', '°'),
        (r'\AA', 'Å'),
        (r'\prime', '′'),
        (r'\dot', ''),
    ]
    for latex, char in replacements:
        text = text.replace(latex, char)
    
    # LaTeX tilde is non-breaking space - convert to regular space
    text = text.replace('~', ' ')
    
    # Handle superscripts: ^{-1} or ^-1 or ^{5} or ^5
    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ',
    }
    
    def convert_superscript(match):
        content = match.group(1)
        result = ''
        for char in content:
            result += superscript_map.get(char, char)
        return result
    
    # Match ^{...} or ^X (single char) or ^-1 (negative exponent)
    text = re.sub(r'\^{([^}]+)}', convert_superscript, text)
    text = re.sub(r'\^(-?[0-9]+)', convert_superscript, text)  # Handle ^-1, ^2, ^-2, etc.
    
    # Handle subscripts: _{*} or _* or _{text}
    subscript_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ',
        '*': '∗', 'p': 'ₚ', 'n': 'ₙ',
    }
    
    def convert_subscript(match):
        content = match.group(1)
        result = ''
        for char in content:
            result += subscript_map.get(char, char)
        return result
    
    # Match _{...} or _X (single char)
    text = re.sub(r'_{([^}]+)}', convert_subscript, text)
    text = re.sub(r'_([0-9*a-z])', convert_subscript, text)
    
    # Handle standalone ^ as prime symbol (common in astronomy: Q_*^ means Q_*')
    text = re.sub(r'\^(?![0-9{\-+])', '′', text)
    
    # Remove $ delimiters
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    # Remove remaining LaTeX commands like \mathrm{...}, \text{...}
    text = re.sub(r'\\(?:mathrm|text|rm|bf|it|textit|textbf)\{([^}]*)\}', r'\1', text)
    
    # Remove any remaining backslash commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Remove remaining braces
    text = re.sub(r'[{}]', '', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def is_exoplanet_focused(paper: dict) -> bool:
    """
    Determine if a paper is about exoplanets.
    Uses comprehensive keyword matching based on exoplanet research taxonomy.
    """
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    text = f"{title} {abstract}"
    
    # ===========================================
    # STRONG INDICATORS - any one = INCLUDE
    # ===========================================
    
    # 1) Core exoplanet terms
    core_terms = [
        "exoplanet", "exoplanets", "exoplanetary",
        "extrasolar planet", "extra-solar planet",
        "planetary system", "exoplanet system",
        "planet candidate", "planet candidates",
        "transiting planet", "transiting exoplanet",
        "confirmed planet", "validated planet",
    ]
    
    # Known exoplanet naming conventions
    exoplanet_names = [
        "toi-", "toi ", "koi-", "koi ",
        "wasp-", "hat-p-", "hats-", "hatp-",
        "kepler-", "k2-", "trappist-",
        "gj ", "gl ", "hd ", "hip ",
        "proxima b", "proxima c",
        "55 cnc", "55 cancri",
    ]
    
    # Check core terms
    for term in core_terms:
        if term in text:
            return True
    
    # Check exoplanet names
    for name in exoplanet_names:
        if name in text:
            return True
    
    # 2) Planet types (strong indicators)
    planet_types = [
        "hot jupiter", "warm jupiter", "cold jupiter",
        "super-earth", "super earth", "sub-neptune", "mini-neptune",
        "terrestrial planet", "rocky planet", "earth-like planet",
        "gas giant exo", "ice giant exo",  # "exo" to avoid solar system
        "ultra-short period planet", "usp planet",
        "compact multiplanet",
    ]
    
    for ptype in planet_types:
        if ptype in text:
            return True
    
    # 3) Habitability / biosignatures (strong indicators)
    habitability_terms = [
        "habitable zone", "habitable planet", "habitable world",
        "habitability", "biosignature", "technosignature",
        "eta-earth", "η⊕",
    ]
    
    for term in habitability_terms:
        if term in text:
            return True
    
    # ===========================================
    # EXCLUDE - Solar system topics
    # ===========================================
    
    solar_system_exclude = [
        # Planets by name (in solar system context)
        "mars", "martian", "venus", "venusian", "mercury", "mercurian",
        "lunar", "moon", "titan", "europa", "enceladus", "ganymede", "io",
        "phobos", "deimos", "triton", "charon",
        # Small bodies
        "asteroid", "comet", "meteoroid", "meteorite",
        "kuiper belt", "tno", "trans-neptunian",
        "centaur", "trojan",
        # Solar system specific
        "interplanetary dust", "zodiacal",
        "juno mission", "cassini", "voyager",
        "perseverance", "curiosity", "insight",
    ]
    
    # Check for solar system - but allow if also has strong exoplanet term
    has_solar_system = any(term in text for term in solar_system_exclude)
    
    if has_solar_system:
        # Exception: "Jupiter" or "Saturn" with "hot" or "warm" prefix
        if ("hot jupiter" in text or "warm jupiter" in text or 
            "hot saturn" in text or "warm saturn" in text):
            return True
        # Exception: has explicit exoplanet context
        if any(term in text for term in ["exoplanet", "extrasolar", "toi-", "wasp-", "kepler-"]):
            return True
        # Otherwise exclude
        return False
    
    # ===========================================
    # MODERATE INDICATORS - need 2+, or 1 + mission
    # ===========================================
    
    # Detection methods
    detection_methods = [
        # Transits
        "transit", "transits", "transiting",
        "transit photometry", "light curve", "lightcurve",
        "transit timing variation", "ttv",
        "secondary eclipse", "phase curve",
        # Radial velocity
        "radial velocity", "doppler spectroscopy",
        "spectroscopic orbit", "rv detection",
        # Direct imaging
        "direct imaging", "high-contrast imaging", "hci",
        "coronagraph", "coronagraphy",
        "angular differential imaging", "adi",
        # Microlensing / astrometry
        "microlensing", "gravitational microlensing",
        "astrometric detection",
        # Other
        "rossiter-mclaughlin", "rm effect",
        "transmission spectrum", "emission spectrum",
        "occultation spectroscopy",
    ]
    
    # Atmospheres / spectra
    atmosphere_terms = [
        "exoplanet atmosphere", "planetary atmosphere",
        "atmospheric retrieval", "retrieval",
        "transmission spectroscopy", "emission spectroscopy",
        "high-resolution spectroscopy",
        "molecular abundance", "photochemistry",
        "clouds", "hazes", "aerosol",
        "thermal emission", "brightness temperature",
        "circulation", "gcm", "general circulation model",
        "radiative transfer",
    ]
    
    # Formation / evolution / dynamics
    formation_terms = [
        "planet formation", "planet migration",
        "protoplanetary disk", "circumstellar disk",
        "core accretion", "pebble accretion",
        "disk migration", "type i migration", "type ii migration",
        "orbital dynamics", "tidal evolution",
        "atmospheric escape", "evaporation", "photoevaporation",
        "radius valley", "photoevaporation valley",
        "mass-radius relation",
    ]
    
    # Demographics / architecture
    demographics_terms = [
        "occurrence rate", "planet occurrence",
        "system architecture", "orbital architecture",
        "mean-motion resonance", "resonant chain",
        "metallicity correlation",
    ]
    
    # Host stars context
    host_star_terms = [
        "m dwarf planet", "k dwarf planet",
        "planet host", "planet-hosting",
        "star-planet interaction",
    ]
    
    # Combine all moderate indicators
    moderate_indicators = (detection_methods + atmosphere_terms + 
                          formation_terms + demographics_terms + host_star_terms)
    
    # Count moderate indicator matches
    moderate_count = sum(1 for term in moderate_indicators if term in text)
    
    # Space missions (boost signal)
    space_missions = [
        "tess", "kepler", "k2 mission", "corot", "cheops", "plato",
        "jwst", "james webb", "hst", "hubble", "spitzer",
        "roman", "nancy grace roman", "ariel", "gaia",
    ]
    
    # Ground surveys
    ground_surveys = [
        "wasp survey", "hatnet", "hatsouth", "ngts", "kelt",
        "trappist survey", "speculoos", "mearth",
        "ogle", "moa",
    ]
    
    # Instruments (RV spectrographs, imagers)
    instruments = [
        "harps", "espresso", "carmenes", "neid", "nirps", "spirou",
        "expres", "sophie", "maroon-x",
        "sphere", "gpi", "scexao", "nirc2",
    ]
    
    has_mission = any(m in text for m in space_missions + ground_surveys + instruments)
    
    # Decision logic for moderate indicators
    if moderate_count >= 2:
        return True
    if moderate_count >= 1 and has_mission:
        return True
    if has_mission:
        # Check if mission is in exoplanet context
        exo_context = ["planet", "transit", "atmosphere", "spectrum", "detection", "orbit"]
        if any(ctx in text for ctx in exo_context):
            return True
    
    # Default: not exoplanet focused
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
    
    arXiv HTML structure:
    - <h3>Showing new listings for Tuesday, 3 February 2026</h3>
    - <h3>New submissions (showing 14 of 14 entries)</h3>
    - <h3>Cross submissions (showing 4 of 4 entries)</h3>
    - <h3>Replacement submissions (showing 8 of 8 entries)</h3>
    """
    print(f"📡 Fetching: {RECENT_URL}")
    
    response = requests.get(RECENT_URL, timeout=30)
    response.raise_for_status()
    html = response.text
    
    # Find all h3 tags
    h3_pattern = r'<h3[^>]*>(.*?)</h3>'
    h3_matches = re.findall(h3_pattern, html, re.DOTALL | re.IGNORECASE)
    
    announcement_date = None
    new_submissions_count = None
    
    for h3_content in h3_matches:
        h3_clean = ' '.join(h3_content.split())
        
        # Date pattern: "Showing new listings for Tuesday, 3 February 2026"
        date_match = re.search(
            r'new listings for\s+([A-Za-z]+),?\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})',
            h3_clean, re.IGNORECASE
        )
        if date_match:
            day = int(date_match.group(2))
            month_name = date_match.group(3)
            year = int(date_match.group(4))
            
            # Parse month name
            months = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                      'may': 5, 'june': 6, 'july': 7, 'august': 8,
                      'september': 9, 'october': 10, 'november': 11, 'december': 12}
            month = months.get(month_name.lower(), 1)
            
            announcement_date = f"{year}-{month:02d}-{day:02d}"
            print(f"📅 Found announcement date: {announcement_date}")
        
        # New submissions count: "New submissions (showing 14 of 14 entries)"
        new_match = re.search(r'New submissions.*?showing\s+(\d+)\s+of\s+(\d+)', h3_clean, re.IGNORECASE)
        if new_match:
            new_submissions_count = int(new_match.group(2))
            print(f"📊 New submissions: {new_submissions_count}")
    
    if not announcement_date:
        announcement_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"⚠️ No date found, using today: {announcement_date}")
    
    # Extract paper IDs - only from NEW submissions section
    # The new submissions section comes after "New submissions" h3 and before "Cross submissions" h3
    
    # Split by h3 tags to isolate sections
    sections = re.split(r'<h3[^>]*>.*?</h3>', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Find the "New submissions" section by looking at what comes after that h3
    new_section = None
    h3_positions = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL | re.IGNORECASE))
    
    for i, match in enumerate(h3_positions):
        h3_text = ' '.join(match.group(1).split())
        if 'new submissions' in h3_text.lower() and 'showing' in h3_text.lower():
            # Get content between this h3 and the next h3
            start = match.end()
            end = h3_positions[i + 1].start() if i + 1 < len(h3_positions) else len(html)
            new_section = html[start:end]
            break
    
    if new_section:
        # Extract paper IDs from new submissions section only
        id_pattern = r'/abs/(\d{4}\.\d{4,5}(?:v\d+)?)'
        paper_ids = re.findall(id_pattern, new_section)
    else:
        # Fallback: get all paper IDs
        print("⚠️ Could not isolate New submissions section, using all papers")
        id_pattern = r'/abs/(\d{4}\.\d{4,5}(?:v\d+)?)'
        paper_ids = re.findall(id_pattern, html)
    
    # Deduplicate while preserving order
    seen = set()
    unique_ids = []
    for pid in paper_ids:
        base_id = re.sub(r'v\d+$', '', pid)
        if base_id not in seen:
            seen.add(base_id)
            unique_ids.append(pid)
    
    # Verify count matches
    if new_submissions_count and len(unique_ids) != new_submissions_count:
        print(f"⚠️ Found {len(unique_ids)} IDs but expected {new_submissions_count}")
    
    print(f"📰 Found {len(unique_ids)} new paper IDs for {announcement_date}")
    
    return announcement_date, unique_ids
    
    print(f"📰 Found {len(unique_ids)} unique paper IDs for {announcement_date}")
    
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
        print(f"    Error generating summary: {e}")
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
    other_count = len(papers) - exo_count
    print(f"   🪐 Exoplanet-focused: {exo_count}")
    print(f"   📊 Other astro-ph.EP: {other_count}")
    
    # FILTER: Only keep exoplanet-focused papers
    if other_count > 0:
        print(f"\n🚫 Excluding {other_count} non-exoplanet papers:")
        for p in papers:
            if not p["is_exoplanet_focused"]:
                print(f"   - {p['id']}: {p['title'][:50]}...")
        papers = [p for p in papers if p["is_exoplanet_focused"]]
    
    if len(papers) == 0:
        print("❌ No exoplanet papers found in this batch.")
        return
    
    # Sort by tweetability
    papers.sort(key=lambda p: p["tweetability_score"], reverse=True)
    
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
