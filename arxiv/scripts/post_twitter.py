#!/usr/bin/env python3
"""
Post exoplanet papers to Twitter/X as 2-tweet threads.
Improved version with better figure fetching.

Changes:
- Uses pre-fetched figure_url from papers.json first
- Falls back to fresh fetch only if needed
- Skips Unsplash placeholders (uses paper card instead)
- Better logging for debugging
- Links now include ?date=YYYY-MM-DD for archive compatibility
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
        temp_path = os.path.join(temp_dir, f"arxiv_{safe_id}{ext}")
        
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        print(f"    ✓ Saved: {temp_path}")
        return temp_path
        
    except Exception as e:
        print(f"    Download failed: {e}")
        return None


def get_figure_for_paper(paper: dict) -> str | None:
    """Get figure image for a paper using improved fallback chain."""
    paper_id = paper["id"]
    
    print(f"\n🖼️ Getting figure for {paper_id}:")
    
    # Strategy 1: Use pre-fetched figure_url (if not placeholder)
    figure_url = paper.get("figure_url", "")
    if figure_url and not is_placeholder_image(figure_url):
        print(f"  1. Trying pre-fetched URL: {figure_url[:60]}...")
        result = download_image(figure_url, paper_id)
        if result:
            return result
        print("     Failed, trying next...")
    else:
        print(f"  1. No valid pre-fetched URL (placeholder or missing)")
    
    # Strategy 2: Try arxiv HTML page for figure
    print(f"  2. Trying fresh fetch from arXiv HTML...")
    fresh_url = fetch_figure_url_from_arxiv(paper_id)
    if fresh_url and fresh_url != figure_url:
        print(f"     Found: {fresh_url[:60]}...")
        result = download_image(fresh_url, paper_id)
        if result:
            return result
        print("     Failed, trying next...")
    else:
        print("     No figure found on arXiv page")
    
    # Strategy 3: Generate paper card
    print(f"  3. Generating paper card...")
    return generate_paper_card(paper)


def fetch_figure_url_from_arxiv(paper_id: str) -> str | None:
    """Fetch figure URL directly from arXiv HTML page."""
    try:
        abs_url = f"https://arxiv.org/abs/{paper_id}"
        response = requests.get(abs_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code != 200:
            return None
        
        html = response.text
        
        # Look for figure preview images
        patterns = [
            r'<img[^>]+src="(https://arxiv\.org/html/[^"]+/extracted/[^"]+\.(?:png|jpg|jpeg))"',
            r'<img[^>]+src="(/html/[^"]+/extracted/[^"]+\.(?:png|jpg|jpeg))"',
            r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                url = match.group(1)
                if url.startswith('/'):
                    url = f"https://arxiv.org{url}"
                if 'arxiv' in url and not is_placeholder_image(url):
                    return url
        
        return None
        
    except Exception as e:
        print(f"     Error fetching arXiv page: {e}")
        return None


def generate_paper_card(paper: dict) -> str | None:
    """Generate a simple paper card image with title and hook."""
    try:
        # Card dimensions (Twitter recommends 1200x628 for summary cards)
        width, height = 1200, 628
        
        # Colors
        bg_color = (15, 23, 42)  # Dark blue
        accent_color = (196, 30, 58)  # Red accent
        text_color = (255, 255, 255)
        muted_color = (148, 163, 184)
        
        # Create image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use system fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw accent bar at top
        draw.rectangle([(0, 0), (width, 6)], fill=accent_color)
        
        # Draw "EXOPLANET PAPERS" label
        draw.text((50, 40), "EXOPLANET PAPERS", fill=accent_color, font=small_font)
        
        # Draw title (word wrap)
        title = paper["title"]
        title_words = title.split()
        title_lines = []
        current_line = []
        
        for word in title_words:
            current_line.append(word)
            test_line = " ".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] > width - 100:
                current_line.pop()
                title_lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            title_lines.append(" ".join(current_line))
        
        y_pos = 100
        for line in title_lines[:4]:  # Max 4 lines
            draw.text((50, y_pos), line, fill=text_color, font=title_font)
            y_pos += 52
        
        # Draw hook if available
        hook = paper.get("tweet_hook", {}).get("hook", "")
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
    """Load list of already tweeted paper IDs (keeps 7 days of history)."""
    if not TWEETED_FILE.exists():
        return {"tweeted_ids": [], "history": {}, "last_reset": None}
    
    with open(TWEETED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Migrate old format to new format
    if "history" not in data:
        data["history"] = {}
        if data.get("tweeted_ids") and data.get("last_reset"):
            data["history"][data["last_reset"]] = data["tweeted_ids"]
    
    return data


def save_tweeted(data):
    """Save tweeted tracking data."""
    TWEETED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TWEETED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_all_tweeted_ids(tweeted_data: dict, days: int = 7) -> set:
    """Get all tweeted paper IDs from the last N days."""
    all_ids = set()
    history = tweeted_data.get("history", {})
    
    # Get IDs from history
    for date, ids in history.items():
        all_ids.update(ids)
    
    # Also include current tweeted_ids for backwards compatibility
    all_ids.update(tweeted_data.get("tweeted_ids", []))
    
    return all_ids


def cleanup_old_history(tweeted_data: dict, days: int = 7) -> dict:
    """Remove history older than N days."""
    from datetime import datetime, timedelta
    
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    history = tweeted_data.get("history", {})
    
    # Keep only recent dates
    new_history = {date: ids for date, ids in history.items() if date >= cutoff}
    tweeted_data["history"] = new_history
    
    return tweeted_data


def create_twitter_client():
    """Create authenticated Twitter API v2 client and v1.1 API for media uploads."""
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET")
    
    if not all([api_key, api_secret, access_token, access_secret]):
        print("Missing Twitter credentials")
        return None, None
    
    # API v2 client for posting
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    
    # API v1.1 for media uploads
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api_v1 = tweepy.API(auth)
    
    return client, api_v1


def get_tweet_limit() -> int:
    """Get tweet character limit based on account tier."""
    tier = os.environ.get("TWITTER_TIER", "free").lower()
    return TWEET_LIMITS.get(tier, 280)


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length, trying to preserve word boundaries."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - 3]
    last_space = truncated.rfind(" ")
    if last_space > max_length // 2:
        truncated = truncated[:last_space]
    
    return truncated + "..."


def extract_hashtags(paper: dict) -> list[str]:
    """Extract relevant hashtags based on paper content."""
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    is_exoplanet = paper.get("is_exoplanet_focused", True)
    
    # Start with base hashtags
    base = BASE_HASHTAGS_EXOPLANET if is_exoplanet else BASE_HASHTAGS_GENERAL
    found = []
    
    # Choose hashtag map based on paper type
    hashtag_map = EXOPLANET_HASHTAGS if is_exoplanet else GENERAL_HASHTAGS
    
    for keyword, hashtag in hashtag_map.items():
        if keyword in text and hashtag not in found:
            found.append(hashtag)
    
    # Combine: base + found (up to MAX_HASHTAGS total)
    result = list(base)
    for tag in found:
        if tag not in result and len(result) < MAX_HASHTAGS:
            result.append(tag)
    
    return result[:MAX_HASHTAGS]


def build_summary_link(page_url: str, paper_id: str, papers_date: str) -> str:
    """Build summary link with date parameter for archive compatibility."""
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', paper_id)
    # Always include date parameter so links work even after new papers are posted
    return f"{page_url}?date={papers_date}#paper-{safe_id}"


def format_tweet_thread_premium(paper: dict, page_url: str, hashtags: list[str], limit: int, papers_date: str) -> tuple[str, str]:
    """Format for premium accounts (25000 chars). Hook-first format with rich content."""
    tweet_hook = paper.get("tweet_hook", {})
    hook = tweet_hook.get("hook", "")
    question = tweet_hook.get("question", "")
    title = paper["title"]
    authors = paper.get("authors", [])
    
    # Parse first author
    if not authors:
        author_str = "Unknown"
    else:
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
    summary_link = build_summary_link(page_url, paper["id"], papers_date)
    hashtag_str = " ".join(hashtags)
    
    tweet2 = f"📄 arXiv: {link}\n📖 Full summary: {summary_link}\n\n{hashtag_str}"
    
    return tweet1, tweet2


def format_tweet_thread_free(paper: dict, page_url: str, hashtags: list[str], papers_date: str) -> tuple[str, str]:
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
    summary_link = build_summary_link(page_url, paper["id"], papers_date)
    hashtag_str = " ".join(hashtags[:3])
    
    tweet2 = f"📄 {link}\n📖 {summary_link}\n\n{hashtag_str}"
    
    return tweet1, tweet2


def format_paper_thread(paper: dict, page_url: str, papers_date: str) -> tuple[str, str]:
    """Create a 2-tweet thread for a paper."""
    limit = get_tweet_limit()
    hashtags = extract_hashtags(paper)
    
    print(f"Tweet limit: {limit} chars")
    print(f"Extracted hashtags: {hashtags}")
    
    if limit > 280:
        return format_tweet_thread_premium(paper, page_url, hashtags, limit, papers_date)
    else:
        return format_tweet_thread_free(paper, page_url, hashtags, papers_date)


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


def select_best_paper(papers: list, tweeted_ids: set, todays_count: int = None) -> dict | None:
    """Select the best paper to tweet based on time of day and tweetability.
    
    Args:
        papers: List of papers from papers.json
        tweeted_ids: Set of paper IDs tweeted in last 7 days (for duplicate prevention)
        todays_count: Number of papers tweeted TODAY (for smart timing). If None, uses len(tweeted_ids).
    """
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
    
    # Filter out hidden papers first
    visible = [p for p in papers if not p.get("hidden", False)]

    # Filter untweeted papers
    untweeted = [p for p in visible if p["id"] not in tweeted_ids]
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
    # FIX: Use today's count for timing, not 7-day count
    tweeted_count = todays_count if todays_count is not None else len(tweeted_ids)
    remaining = total_papers - tweeted_count
    
    if remaining <= 0:
        return None
    
    # Calculate optimal interval
    minutes_in_window = (tweet_end_hour - tweet_start_hour) * 60
    minutes_elapsed = (current_hour - tweet_start_hour) * 60 + current_minute
    interval = minutes_in_window / max(total_papers, 1)
    
    expected_tweets = int(minutes_elapsed / interval) if interval > 0 else tweeted_count
    
    print(f"📊 Smart timing:")
    print(f"   Papers: {total_papers}, Tweeted today: {tweeted_count}")
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
    papers_date = data.get("announcement_date") or data.get("updated_at", "")[:10]
    
    print(f"Papers date: {papers_date}")
    print(f"Total papers: {len(papers)}")
    
    # Load tweeted tracking
    tweeted_data = load_tweeted()
    last_reset = tweeted_data.get("last_reset")
    
    # Get ALL tweeted IDs from last 7 days (not just today)
    all_tweeted_ids = get_all_tweeted_ids(tweeted_data, days=7)
    print(f"Papers tweeted in last 7 days: {len(all_tweeted_ids)}")
    
    # If new day, update tracking structure
    if last_reset != papers_date:
        print(f"New day detected (was: {last_reset}, now: {papers_date})")
        
        # Save yesterday's tweets to history before resetting
        if last_reset and tweeted_data.get("tweeted_ids"):
            if "history" not in tweeted_data:
                tweeted_data["history"] = {}
            tweeted_data["history"][last_reset] = tweeted_data.get("tweeted_ids", [])
        
        # Reset today's list but keep history
        tweeted_data["tweeted_ids"] = []
        tweeted_data["last_reset"] = papers_date
        
        # Cleanup old history (older than 7 days)
        tweeted_data = cleanup_old_history(tweeted_data, days=7)
        save_tweeted(tweeted_data)
    
    # Today's tweeted IDs (for counting remaining)
    todays_tweeted_ids = set(tweeted_data.get("tweeted_ids", []))
    
    # Select the best paper to tweet (check against ALL recent tweets)
    # Pass today's count separately for smart timing
    todays_count = len(tweeted_data.get("tweeted_ids", []))
    paper_to_tweet = select_best_paper(papers, all_tweeted_ids, todays_count=todays_count)
    
    if not paper_to_tweet:
        print("All papers have been tweeted (or were tweeted recently)!")
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
    
    # Format the thread (now with papers_date)
    tweet1_text, tweet2_text = format_paper_thread(paper_to_tweet, page_url, papers_date)
    
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
            # Add to today's list
            todays_tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(todays_tweeted_ids)
            save_tweeted(tweeted_data)
            
            print(f"\n✅ Thread posted successfully!")
            print(f"   Tweet 1: https://twitter.com/i/status/{tweet1_id}")
            print(f"   Tweet 2: https://twitter.com/i/status/{tweet2_id}")
            print(f"   Tweeted today: {len(todays_tweeted_ids)}")
            print(f"   Remaining today: {len(papers) - len(todays_tweeted_ids)}")
        else:
            print("\n⚠️ Tweet 1 posted but Tweet 2 failed")
            todays_tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(todays_tweeted_ids)
            save_tweeted(tweeted_data)
    else:
        print("\n❌ Failed to post tweet")
        sys.exit(1)


if __name__ == "__main__":
    main()
