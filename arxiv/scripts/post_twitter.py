#!/usr/bin/env python3
"""
Post exoplanet papers to Twitter/X as 2-tweet threads.
Improved version with better figure fetching.

Changes:
- Uses pre-fetched figure_url from papers.json first
- Falls back to fresh fetch only if needed
- Skips Unsplash placeholders (uses paper card instead)
- Better logging for debugging
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont


def clean_latex_name(name: str) -> str:
    """Clean LaTeX escape sequences from author names."""
    # Common LaTeX accent replacements
    replacements = {
        # Acute accents \'
        "\\'a": "á", "\\'e": "é", "\\'i": "í", "\\'o": "ó", "\\'u": "ú",
        "\\'A": "Á", "\\'E": "É", "\\'I": "Í", "\\'O": "Ó", "\\'U": "Ú",
        "\\'n": "ń", "\\'c": "ć", "\\'s": "ś", "\\'z": "ź",
        # Grave accents \`
        "\\`a": "à", "\\`e": "è", "\\`i": "ì", "\\`o": "ò", "\\`u": "ù",
        # Umlaut \"
        '\\"a': "ä", '\\"e': "ë", '\\"i': "ï", '\\"o': "ö", '\\"u': "ü",
        '\\"A': "Ä", '\\"E': "Ë", '\\"I': "Ï", '\\"O': "Ö", '\\"U': "Ü",
        # Caron \v{}
        "\\v{c}": "č", "\\v{C}": "Č", "\\v{s}": "š", "\\v{S}": "Š",
        "\\v{z}": "ž", "\\v{Z}": "Ž", "\\v{r}": "ř", "\\v{R}": "Ř",
        "\\v{e}": "ě", "\\v{E}": "Ě", "\\v{n}": "ň", "\\v{N}": "Ň",
        # Cedilla \c{}
        "\\c{c}": "ç", "\\c{C}": "Ç",
        # Tilde \~
        "\\~n": "ñ", "\\~N": "Ñ", "\\~a": "ã", "\\~o": "õ",
        # Circumflex \^
        "\\^a": "â", "\\^e": "ê", "\\^i": "î", "\\^o": "ô", "\\^u": "û",
        # Polish l
        "\\l": "ł", "\\L": "Ł",
        # German sharp s
        "\\ss": "ß",
        # Scandinavian
        "\\aa": "å", "\\AA": "Å", "\\o": "ø", "\\O": "Ø", "\\ae": "æ", "\\AE": "Æ",
    }
    
    result = name
    for latex, char in replacements.items():
        result = result.replace(latex, char)
    
    # Handle \v{X} patterns not in the map (generic caron)
    result = re.sub(r"\\v\{(\w)\}", r"\1", result)
    
    # Handle remaining backslash escapes
    result = re.sub(r"\\['\"`^~](\w)", r"\1", result)
    result = re.sub(r"\\['\"`^~]\{(\w)\}", r"\1", result)
    
    # Clean up any remaining backslashes before letters
    result = re.sub(r"\\(\w)", r"\1", result)
    
    return result

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
TWEETED_FILE = DATA_DIR / "tweeted.json"

# Tweet character limits
TWEET_LIMITS = {
    "free": 280,
    "premium": 25000,
    "plus": 25000
}

# Hashtag mappings for exoplanet papers
EXOPLANET_HASHTAGS = {
    # Telescopes/Missions
    "jwst": "#JWST",
    "james webb": "#JWST",
    "webb telescope": "#JWST",
    "tess": "#TESS",
    "kepler": "#Kepler",
    "hubble": "#Hubble",
    "hst": "#Hubble",
    "spitzer": "#Spitzer",
    "cheops": "#CHEOPS",
    "plato": "#PLATO",
    "ariel": "#ARIEL",
    "roman": "#Roman",
    
    # Planet types
    "hot jupiter": "#HotJupiter",
    "warm jupiter": "#WarmJupiter",
    "cold jupiter": "#ColdJupiter",
    "super-earth": "#SuperEarth",
    "super earth": "#SuperEarth",
    "sub-neptune": "#SubNeptune",
    "mini-neptune": "#MiniNeptune",
    "earth-like planet": "#EarthLike",
    "earth-sized planet": "#EarthSized",
    "terrestrial planet": "#TerrestrialPlanet",
    "terrestrial exoplanet": "#TerrestrialPlanet",
    "lava world": "#LavaWorld",
    "ocean world": "#OceanWorld",
    "water world": "#WaterWorld",
    "rogue planet": "#RoguePlanet",
    "free-floating planet": "#RoguePlanet",
    
    # Exoplanet-specific terms
    "exoplanet atmosphere": "#ExoplanetAtmosphere",
    "exoplanetary atmosphere": "#ExoplanetAtmosphere",
    "transmission spectrum": "#TransmissionSpectroscopy",
    "transmission spectroscopy": "#TransmissionSpectroscopy",
    "emission spectrum": "#EmissionSpectroscopy",
    "habitable zone": "#HabitableZone",
    "habitable exoplanet": "#HabitableZone",
    "biosignature": "#Biosignatures",
    "biosignatures": "#Biosignatures",
    
    # Detection methods
    "transit method": "#TransitMethod",
    "transiting exoplanet": "#TransitMethod",
    "transiting planet": "#TransitMethod",
    "radial velocity method": "#RadialVelocity",
    "radial velocity survey": "#RadialVelocity",
    "microlensing planet": "#Microlensing",
    "direct imaging": "#DirectImaging",
    "directly imaged": "#DirectImaging",
    
    # Notable systems
    "trappist-1": "#TRAPPIST1",
    "proxima centauri b": "#ProximaCentauri",
    "proxima b": "#ProximaCentauri",
    "wasp-39": "#WASP39",
    "wasp-76": "#WASP76",
    "toi-700": "#TOI700",
    "k2-18": "#K218b",
    "55 cancri": "#55Cancri",
    "gj 1214": "#GJ1214",
    "hd 189733": "#HD189733",
    
    # Formation
    "planet formation": "#PlanetFormation",
    "planetary formation": "#PlanetFormation",
    "protoplanetary disk": "#ProtoplanetaryDisk",
    "protoplanetary disc": "#ProtoplanetaryDisk",
    "planet migration": "#PlanetMigration",
    "planetary migration": "#PlanetMigration",
}

# Hashtags for general astro-ph.EP papers
GENERAL_HASHTAGS = {
    "protoplanetary disk": "#ProtoplanetaryDisk",
    "protoplanetary disc": "#ProtoplanetaryDisk",
    "debris disk": "#DebrisDisk",
    "debris disc": "#DebrisDisk",
    "asteroid": "#Asteroids",
    "meteor": "#Meteors",
    "comet": "#Comets",
    "brown dwarf": "#BrownDwarfs",
    "planet formation": "#PlanetFormation",
    "dust grain": "#DustGrains",
    "interstellar object": "#InterstellarObject",
}

# Base hashtags
BASE_HASHTAGS_EXOPLANET = ["#Exoplanets", "#Astronomy"]
BASE_HASHTAGS_GENERAL = ["#Astronomy", "#PlanetaryScience"]
MAX_HASHTAGS = 4


def is_placeholder_image(url: str) -> bool:
    """Check if URL is a placeholder/stock image (not actual paper figure)."""
    if not url:
        return True
    placeholder_indicators = [
        "unsplash.com",
        "placeholder",
        "stock",
        "generic",
        "default"
    ]
    return any(indicator in url.lower() for indicator in placeholder_indicators)


def download_image(url: str, paper_id: str) -> str | None:
    """Download an image to a temporary file. Returns file path or None."""
    try:
        print(f"    Downloading: {url[:80]}...")
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code != 200:
            print(f"    HTTP {response.status_code}")
            return None
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if not any(t in content_type for t in ['image/png', 'image/jpeg', 'image/gif', 'image/webp']):
            # Try to detect from content
            if not response.content[:8].startswith((b'\x89PNG', b'\xff\xd8\xff', b'GIF8')):
                print(f"    Not a valid image (content-type: {content_type})")
                return None
        
        # Check size (Twitter requires images > 5KB, < 5MB)
        size = len(response.content)
        if size < 5000:
            print(f"    Image too small ({size} bytes)")
            return None
        if size > 5_000_000:
            print(f"    Image too large ({size/1024/1024:.1f} MB)")
            return None
        
        # Determine extension
        if b'\x89PNG' in response.content[:8]:
            ext = '.png'
        elif b'\xff\xd8\xff' in response.content[:8]:
            ext = '.jpg'
        elif b'GIF8' in response.content[:8]:
            ext = '.gif'
        else:
            ext = '.png'
        
        # Save to temp directory
        safe_id = paper_id.replace('/', '_').replace('.', '_')
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"arxiv_fig_{safe_id}{ext}")
        
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        print(f"    ✓ Downloaded: {temp_path} ({size/1024:.1f} KB)")
        return temp_path
        
    except Exception as e:
        print(f"    Download failed: {e}")
        return None


def fetch_paper_figure_fresh(paper_id: str) -> str | None:
    """
    Attempt to fetch Figure 1 from a paper (fresh fetch, not cached).
    Returns the local file path if successful, None otherwise.
    """
    print(f"  Fresh fetch for {paper_id}...")
    
    # Method 1: Try arXiv abstract page og:image
    try:
        abs_url = f"https://arxiv.org/abs/{paper_id}"
        response = requests.get(abs_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code == 200:
            og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', response.text)
            if og_match:
                img_url = og_match.group(1)
                if 'arxiv-logo' not in img_url and 'static' not in img_url:
                    img_path = download_image(img_url, paper_id)
                    if img_path:
                        return img_path
    except Exception as e:
        print(f"    arXiv page failed: {e}")
    
    # Method 2: Try ar5iv (HTML rendering)
    try:
        ar5iv_url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}"
        response = requests.get(ar5iv_url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code == 200:
            patterns = [
                r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*ltx_graphics[^"]*"',
                r'<figure[^>]*>.*?<img[^>]+src="([^"]+)".*?</figure>',
                r'<img[^>]+src="(/html/[^"]+\.(?:png|jpg|jpeg|gif))"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE | re.DOTALL)
                for match in matches[:3]:
                    img_url = match
                    if img_url.startswith('/'):
                        img_url = f"https://ar5iv.labs.arxiv.org{img_url}"
                    elif not img_url.startswith('http'):
                        img_url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}/{img_url}"
                    
                    img_path = download_image(img_url, paper_id)
                    if img_path:
                        return img_path
    except Exception as e:
        print(f"    ar5iv failed: {e}")
    
    # Method 3: Try arXiv HTML directly
    try:
        html_url = f"https://arxiv.org/html/{paper_id}"
        response = requests.get(html_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code == 200:
            patterns = [
                r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']',
                r'<img[^>]+class=["\'][^"\']*ltx_graphics[^"\']*["\'][^>]+src=["\']([^"\']+)["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE | re.DOTALL)
                if matches:
                    img_path = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    if img_path.startswith('/'):
                        img_url = f"https://arxiv.org{img_path}"
                    elif img_path.startswith('http'):
                        img_url = img_path
                    else:
                        img_url = f"https://arxiv.org/html/{paper_id}/{img_path}"
                    
                    result = download_image(img_url, paper_id)
                    if result:
                        return result
    except Exception as e:
        print(f"    arXiv HTML failed: {e}")
    
    print(f"    No figure found via fresh fetch")
    return None


def get_figure_for_paper(paper: dict) -> str | None:
    """
    Get figure for a paper with smart fallback chain:
    1. Use stored figure_url if it's a real figure (not Unsplash)
    2. Try fresh fetch if no stored URL or stored URL is placeholder
    3. Generate paper card as last resort
    
    Returns local file path or None.
    """
    paper_id = paper["id"]
    stored_url = paper.get("figure_url", "")
    
    print(f"📷 Getting image for {paper_id}...")
    
    # Step 1: Check stored URL
    if stored_url and not is_placeholder_image(stored_url):
        print(f"  Using stored figure_url")
        result = download_image(stored_url, paper_id)
        if result:
            return result
        print(f"  Stored URL failed, trying fresh fetch...")
    
    # Step 2: Try fresh fetch
    result = fetch_paper_figure_fresh(paper_id)
    if result:
        return result
    
    # Step 3: Generate paper card as fallback
    print(f"  Generating paper card fallback...")
    return generate_paper_card(paper)


def generate_paper_card(paper: dict) -> str | None:
    """Generate a branded paper card image as fallback."""
    try:
        # Card dimensions (Twitter optimal: 1200x675 for 16:9)
        width, height = 1200, 675
        
        # Colors
        bg_color = (15, 23, 42)  # Dark blue
        title_color = (248, 250, 252)  # White
        accent_color = (99, 102, 241)  # Indigo
        muted_color = (148, 163, 184)  # Gray
        
        # Create image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts (fallback to default)
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw accent bar at top
        draw.rectangle([(0, 0), (width, 8)], fill=accent_color)
        
        # Draw title (wrap text)
        title = paper.get("title", "Untitled")
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] > width - 100:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        y_pos = 60
        for line in lines[:3]:  # Max 3 lines
            draw.text((50, y_pos), line, fill=title_color, font=title_font)
            y_pos += 55
        
        # Draw hook if available
        tweet_hook = paper.get("tweet_hook", {})
        hook = tweet_hook.get("hook", "")
        if hook:
            hook_words = hook.split()
            hook_lines = []
            current_line = []
            for word in hook_words:
                current_line.append(word)
                test_line = " ".join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=body_font)
                if bbox[2] > width - 100:
                    current_line.pop()
                    hook_lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                hook_lines.append(" ".join(current_line))
            
            y_pos += 40
            for line in hook_lines[:3]:
                draw.text((50, y_pos), line, fill=muted_color, font=body_font)
                y_pos += 38
        
        # Draw arXiv ID at bottom
        arxiv_text = f"arXiv:{paper['id']}"
        draw.text((50, height - 80), arxiv_text, fill=accent_color, font=small_font)
        
        # Save
        safe_id = paper["id"].replace('/', '_').replace('.', '_')
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"arxiv_card_{safe_id}.png")
        img.save(temp_path, 'PNG')
        
        print(f"    ✓ Generated paper card: {temp_path}")
        return temp_path
        
    except Exception as e:
        print(f"    Paper card generation failed: {e}")
        return None


def load_papers():
    """Load papers from JSON file."""
    if not PAPERS_FILE.exists():
        print("No papers file found")
        return None
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tweeted():
    """Load list of already tweeted paper IDs."""
    if not TWEETED_FILE.exists():
        return {"tweeted_ids": [], "last_reset": None}
    
    with open(TWEETED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tweeted(data):
    """Save tweeted tracking data."""
    TWEETED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TWEETED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_twitter_client():
    """Create authenticated Twitter API v2 client and v1.1 API for media uploads."""
    required_keys = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_SECRET"
    ]
    
    missing = [k for k in required_keys if not os.environ.get(k)]
    if missing:
        print(f"Missing Twitter credentials: {', '.join(missing)}")
        return None, None
    
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
    )
    
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_SECRET"]
    )
    api_v1 = tweepy.API(auth)
    
    return client, api_v1


def get_tweet_limit():
    """Get tweet character limit based on account type."""
    premium = os.environ.get("TWITTER_PREMIUM", "").lower()
    if premium == "plus":
        return TWEET_LIMITS["plus"]
    elif premium == "true" or premium == "premium":
        return TWEET_LIMITS["premium"]
    else:
        return TWEET_LIMITS["free"]


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length, preserving words."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - len(suffix)]
    last_space = truncated.rfind(" ")
    if last_space > max_length // 2:
        truncated = truncated[:last_space]
    
    return truncated + suffix


def extract_hashtags(paper: dict, max_hashtags: int = MAX_HASHTAGS) -> list[str]:
    """Extract relevant hashtags from paper title and abstract."""
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    content = f"{title} {abstract}"
    
    is_exoplanet = paper.get("is_exoplanet_focused", True)
    hashtag_map = EXOPLANET_HASHTAGS if is_exoplanet else GENERAL_HASHTAGS
    base_hashtags = BASE_HASHTAGS_EXOPLANET if is_exoplanet else BASE_HASHTAGS_GENERAL
    
    found_hashtags = []
    for keyword, hashtag in hashtag_map.items():
        if keyword in content and hashtag not in found_hashtags:
            found_hashtags.append(hashtag)
    
    # Combine base + found, limit to max
    all_hashtags = base_hashtags.copy()
    for h in found_hashtags:
        if h not in all_hashtags:
            all_hashtags.append(h)
    
    return all_hashtags[:max_hashtags]


def format_tweet_thread_premium(paper: dict, page_url: str, hashtags: list[str], limit: int) -> tuple[str, str]:
    """Format for premium accounts (longer tweets). Hook-first format."""
    tweet_hook = paper.get("tweet_hook", {})
    hook = tweet_hook.get("hook", "")
    question = tweet_hook.get("question", "")
    
    title = paper["title"]
    authors = paper.get("authors", [])
    
    # Parse first author - authors might be a list of names or a list with one comma-separated string
    if not authors:
        author_str = "Unknown"
    else:
        # If first element contains comma, it's all authors in one string
        first_item = authors[0]
        if "," in first_item:
            first_author = first_item.split(",")[0].strip()
            first_author = clean_latex_name(first_author)
            author_str = f"{first_author} et al."
        elif len(authors) == 1:
            author_str = clean_latex_name(authors[0])
        else:
            author_str = f"{clean_latex_name(authors[0])} et al."
    
    # Build tweet: Hook first, then title + author, then question
    parts = []
    
    if hook:
        parts.append(hook)
        parts.append("")
    
    parts.append(f"📄 {title}")
    parts.append(f"👤 {author_str}")
    
    if question:
        parts.append("")
        parts.append(question)
    
    tweet1 = "\n".join(parts)
    tweet1 = tweet1.strip()
    
    if len(tweet1) > limit:
        tweet1 = truncate_text(tweet1, limit - 3)
    
    link = paper["abs_link"]
    paper_id = paper["id"]
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', paper_id)
    summary_link = f"{page_url}#paper-{safe_id}"
    hashtag_str = " ".join(hashtags)
    
    tweet2 = f"📄 arXiv: {link}\n📖 Full summary: {summary_link}\n\n{hashtag_str}"
    
    return tweet1, tweet2


def format_tweet_thread_free(paper: dict, page_url: str, hashtags: list[str]) -> tuple[str, str]:
    """Format for free accounts (280 chars). Hook-first format."""
    tweet_hook = paper.get("tweet_hook", {})
    hook = tweet_hook.get("hook", "")
    question = tweet_hook.get("question", "")
    title = paper["title"]
    authors = paper.get("authors", [])
    
    # Parse first author - authors might be a list of names or a list with one comma-separated string
    if not authors:
        author_str = "Unknown"
    else:
        # If first element contains comma, it's all authors in one string
        first_item = authors[0]
        if "," in first_item:
            first_author = first_item.split(",")[0].strip()
            first_author = clean_latex_name(first_author)
            author_str = f"{first_author} et al."
        elif len(authors) == 1:
            author_str = clean_latex_name(authors[0])
        else:
            author_str = f"{clean_latex_name(authors[0])} et al."
    
    # Build tweet: Hook first (if fits), then title + author, then question
    parts = []
    
    if hook:
        parts.append(hook)
        parts.append("")
    
    parts.append(f"📄 {title}")
    parts.append(f"👤 {author_str}")
    
    if question:
        parts.append("")
        parts.append(question)
    
    tweet1 = "\n".join(parts)
    
    # If too long, try without question
    if len(tweet1) > 280:
        parts = []
        if hook:
            parts.append(hook)
            parts.append("")
        parts.append(f"📄 {title}")
        parts.append(f"👤 {author_str}")
        tweet1 = "\n".join(parts)
    
    # If still too long, try without hook
    if len(tweet1) > 280:
        tweet1 = f"📄 {title}\n👤 {author_str}"
    
    # Final truncate if needed
    if len(tweet1) > 280:
        tweet1 = truncate_text(tweet1, 277)
    
    # Tweet 2: Links + hashtags
    link = paper["abs_link"]
    paper_id = paper["id"]
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', paper_id)
    summary_link = f"{page_url}#paper-{safe_id}"
    hashtag_str = " ".join(hashtags[:3])
    
    tweet2 = f"📄 {link}\n📖 {summary_link}\n\n{hashtag_str}"
    
    return tweet1, tweet2


def format_paper_thread(paper: dict, page_url: str) -> tuple[str, str]:
    """Create a 2-tweet thread for a paper."""
    limit = get_tweet_limit()
    hashtags = extract_hashtags(paper)
    
    print(f"Tweet limit: {limit} chars")
    print(f"Extracted hashtags: {hashtags}")
    
    if limit > 280:
        return format_tweet_thread_premium(paper, page_url, hashtags, limit)
    else:
        return format_tweet_thread_free(paper, page_url, hashtags)


def upload_media(api_v1: tweepy.API, image_path: str) -> str | None:
    """Upload an image to Twitter."""
    try:
        media = api_v1.media_upload(filename=image_path)
        print(f"Uploaded media: {media.media_id}")
        return str(media.media_id)
    except tweepy.TweepyException as e:
        print(f"Error uploading media: {e}")
        return None


def post_tweet(client: tweepy.Client, tweet_text: str, media_ids: list[str] = None, reply_to: str = None) -> str | None:
    """Post a single tweet."""
    try:
        kwargs = {"text": tweet_text}
        if media_ids:
            kwargs["media_ids"] = media_ids
        if reply_to:
            kwargs["in_reply_to_tweet_id"] = reply_to
        
        response = client.create_tweet(**kwargs)
        tweet_id = response.data["id"]
        print(f"Posted tweet: {tweet_id}")
        return tweet_id
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return None


def cleanup_temp_file(filepath: str):
    """Remove temporary file if it exists."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass


def select_best_paper(papers: list, tweeted_ids: set) -> dict | None:
    """Select the best paper to tweet based on time of day and tweetability."""
    # Get current time in Istanbul
    istanbul_tz = ZoneInfo("Europe/Istanbul")
    now = datetime.now(istanbul_tz)
    current_hour = now.hour
    current_minute = now.minute
    
    # Tweet window: 7 AM to 11 PM Istanbul (16 hours)
    tweet_start_hour = 7
    tweet_end_hour = 23
    
    if current_hour < tweet_start_hour or current_hour >= tweet_end_hour:
        print(f"Outside tweet window ({tweet_start_hour}:00-{tweet_end_hour}:00 Istanbul)")
        return None
    
    # Filter untweeted papers
    untweeted = [p for p in papers if p["id"] not in tweeted_ids]
    if not untweeted:
        return None
    
    # Sort by exoplanet focus first, then tweetability
    exo_papers = [p for p in untweeted if p.get("is_exoplanet_focused", True)]
    gen_papers = [p for p in untweeted if not p.get("is_exoplanet_focused", True)]
    
    exo_papers.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    gen_papers.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    
    # Prime time (8 AM - 12 PM, 5 PM - 11 PM Istanbul): exoplanet papers
    # Off-peak: general papers
    is_prime_time = (8 <= current_hour < 12) or (17 <= current_hour < 23)
    
    if is_prime_time and exo_papers:
        pool = exo_papers
    elif gen_papers:
        pool = gen_papers
    else:
        pool = exo_papers if exo_papers else untweeted
    
    # Smart timing: spread tweets throughout the day
    total_papers = len(papers)
    tweeted_count = len(tweeted_ids)
    remaining = total_papers - tweeted_count
    
    if remaining <= 0:
        return None
    
    # Calculate optimal interval
    minutes_in_window = (tweet_end_hour - tweet_start_hour) * 60
    minutes_elapsed = (current_hour - tweet_start_hour) * 60 + current_minute
    interval = minutes_in_window / max(total_papers, 1)
    
    expected_tweets = int(minutes_elapsed / interval) if interval > 0 else tweeted_count
    
    print(f"📊 Smart timing:")
    print(f"   Papers: {total_papers}, Tweeted: {tweeted_count}")
    print(f"   Interval: {interval:.0f} min (~{interval/60:.1f} hours)")
    print(f"   Time: {now.strftime('%H:%M')} Istanbul ({minutes_elapsed:.0f} min into window)")
    print(f"   Expected tweets by now: {expected_tweets}")
    
    if tweeted_count >= expected_tweets:
        next_tweet_min = int((tweeted_count + 1) * interval - minutes_elapsed)
        print(f"   ⏳ Next tweet in ~{next_tweet_min} min")
        print("Not time to tweet yet. Exiting.")
        sys.exit(0)
    
    return pool[0] if pool else None


def main():
    """Main function - tweet ONE paper as a 2-tweet thread with image."""
    
    # Load papers
    data = load_papers()
    if not data or not data.get("papers"):
        print("No papers available")
        return
    
    papers = data["papers"]
    papers_date = data.get("updated_at", "")[:10]
    
    # Load tweeted tracking
    tweeted_data = load_tweeted()
    tweeted_ids = set(tweeted_data.get("tweeted_ids", []))
    last_reset = tweeted_data.get("last_reset")
    
    # Reset tweeted list if papers were updated (new day)
    if last_reset != papers_date:
        print(f"New papers detected (date: {papers_date}). Resetting tweeted list.")
        tweeted_ids = set()
        tweeted_data = {
            "tweeted_ids": [],
            "last_reset": papers_date
        }
    
    # Select the best paper to tweet
    paper_to_tweet = select_best_paper(papers, tweeted_ids)
    
    if not paper_to_tweet:
        print("All papers have been tweeted today!")
        return
    
    paper_type = "🪐 EXOPLANET" if paper_to_tweet.get("is_exoplanet_focused", True) else "🔭 GENERAL"
    print(f"Selected paper: {paper_to_tweet['id']}")
    print(f"  Type: {paper_type}")
    print(f"  Tweetability: {paper_to_tweet.get('tweetability_score', 0)}")
    
    # Create Twitter clients
    client, api_v1 = create_twitter_client()
    if not client:
        print("Could not create Twitter client. Exiting.")
        return
    
    # Get page URL
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    
    # Get image using improved fallback chain
    figure_path = None
    media_ids = None
    
    if api_v1:
        figure_path = get_figure_for_paper(paper_to_tweet)
        
        if figure_path:
            media_id = upload_media(api_v1, figure_path)
            if media_id:
                media_ids = [media_id]
                print(f"📸 Image will be attached to tweet!")
            else:
                print("⚠️ Image upload failed, tweeting without image")
        else:
            print("📄 No image available, tweeting text only")
    
    # Format the thread
    tweet1_text, tweet2_text = format_paper_thread(paper_to_tweet, page_url)
    
    print(f"\nTweeting paper: {paper_to_tweet['id']}")
    print(f"\nTweet 1 ({len(tweet1_text)} chars):")
    print("-" * 50)
    print(tweet1_text)
    print("-" * 50)
    print(f"\nTweet 2 ({len(tweet2_text)} chars):")
    print("-" * 50)
    print(tweet2_text)
    print("-" * 50)
    
    # Post tweet 1 (with image)
    tweet1_id = post_tweet(client, tweet1_text, media_ids)
    
    # Clean up temp file
    if figure_path:
        cleanup_temp_file(figure_path)
    
    if tweet1_id:
        # Post tweet 2 as reply
        tweet2_id = post_tweet(client, tweet2_text, reply_to=tweet1_id)
        
        if tweet2_id:
            tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(tweeted_ids)
            save_tweeted(tweeted_data)
            print(f"\n✅ Thread posted successfully!")
            print(f"   Tweet 1: https://twitter.com/i/status/{tweet1_id}")
            print(f"   Tweet 2: https://twitter.com/i/status/{tweet2_id}")
            print(f"   Remaining papers: {len(papers) - len(tweeted_ids)}")
        else:
            print("\n⚠️ Tweet 1 posted but Tweet 2 failed")
            tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(tweeted_ids)
            save_tweeted(tweeted_data)
    else:
        print("\n❌ Failed to post tweet")
        sys.exit(1)


if __name__ == "__main__":
    main()
