#!/usr/bin/env python3
"""
Post individual exoplanet paper summaries to Twitter/X as 2-tweet threads.
Tweets ONE paper per run, selecting the most "tweetable" untweeted paper.

IMPROVEMENTS:
- Posts as 2-tweet thread (hook first, links second)
- Fixed hashtag matching (lowercase keys)
- Reduced hashtags (2-4 max)
- Generates fallback "paper card" images
- Selects most engaging paper based on tweetability score

Supports Twitter Premium for longer tweets:
- Free: 280 characters
- Premium: 4,000 characters  
- Premium+: 25,000 characters

Set TWITTER_PREMIUM environment variable to 'true' or 'plus' to enable.
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
import tweepy


# Configuration
PAPERS_FILE = Path(__file__).parent.parent / "data" / "papers.json"
TWEETED_FILE = Path(__file__).parent.parent / "data" / "tweeted.json"

# Tweet length by account type
TWEET_LIMITS = {
    "free": 280,
    "premium": 4000,
    "plus": 25000
}

# Keyword to hashtag mapping for exoplanet research
# STRICT matching: Use multi-word phrases to avoid false positives
# Only match terms that are EXPLICITLY about the topic

KEYWORD_HASHTAGS = {
    # === HIGH CONFIDENCE MATCHES (multi-word, specific) ===
    
    # Telescopes & Instruments - specific phrases
    "jwst": "#JWST",
    "james webb": "#JWST",
    "webb space telescope": "#JWST",
    "tess mission": "#TESS",
    "tess planet": "#TESS",
    "tess candidate": "#TESS",
    "kepler mission": "#Kepler",
    "kepler planet": "#Kepler",
    "alma observation": "#ALMA",
    "harps spectrograph": "#HARPS",
    "espresso spectrograph": "#ESPRESSO",
    "hubble space": "#Hubble",
    "vlt observation": "#VLT",
    "keck observation": "#Keck",
    "gaia dr": "#Gaia",
    
    # Planet types - specific phrases
    "hot jupiter": "#HotJupiter",
    "warm jupiter": "#WarmJupiter",
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
    
    # Detection methods - specific phrases
    "transit method": "#TransitMethod",
    "transiting exoplanet": "#TransitMethod",
    "transiting planet": "#TransitMethod",
    "radial velocity method": "#RadialVelocity",
    "radial velocity survey": "#RadialVelocity",
    "microlensing planet": "#Microlensing",
    "direct imaging": "#DirectImaging",
    "directly imaged": "#DirectImaging",
    
    # Notable systems - exact matches
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
    
    # Formation - specific phrases
    "planet formation": "#PlanetFormation",
    "planetary formation": "#PlanetFormation",
    "protoplanetary disk": "#ProtoplanetaryDisk",
    "protoplanetary disc": "#ProtoplanetaryDisk",
    "planet migration": "#PlanetMigration",
    "planetary migration": "#PlanetMigration",
}

# Hashtags for general astro-ph.EP papers (not exoplanet-focused)
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

# Base hashtags by paper type
BASE_HASHTAGS_EXOPLANET = ["#Exoplanets", "#Astronomy"]
BASE_HASHTAGS_GENERAL = ["#Astronomy", "#PlanetaryScience"]

# Maximum hashtags to include (including base)
MAX_HASHTAGS = 4


def fetch_paper_figure(paper_id: str) -> str | None:
    """
    Attempt to fetch Figure 1 from a paper.
    Returns the local file path if successful, None otherwise.
    
    Tries multiple sources:
    1. arXiv HTML page (og:image meta tag)
    2. ar5iv.org HTML rendering
    """
    
    print(f"  Attempting to fetch figure for {paper_id}...")
    
    # Method 1: Try arXiv abstract page og:image (often contains a figure preview)
    try:
        abs_url = f"https://arxiv.org/abs/{paper_id}"
        response = requests.get(abs_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code == 200:
            # Look for og:image meta tag
            og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', response.text)
            if og_match:
                img_url = og_match.group(1)
                # Skip placeholder images
                if 'arxiv-logo' not in img_url and 'static' not in img_url:
                    img_path = download_image(img_url, paper_id)
                    if img_path:
                        return img_path
    except Exception as e:
        print(f"    arXiv page fetch failed: {e}")
    
    # Method 2: Try ar5iv (HTML rendering of papers)
    try:
        ar5iv_url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}"
        response = requests.get(ar5iv_url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code == 200:
            # Look for figure images
            patterns = [
                r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*ltx_graphics[^"]*"',
                r'<figure[^>]*>.*?<img[^>]+src="([^"]+)".*?</figure>',
                r'<img[^>]+src="(/html/[^"]+\.(?:png|jpg|jpeg|gif))"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE | re.DOTALL)
                for match in matches[:3]:  # Try first 3 matches
                    img_url = match
                    if img_url.startswith('/'):
                        img_url = f"https://ar5iv.labs.arxiv.org{img_url}"
                    elif not img_url.startswith('http'):
                        img_url = f"https://ar5iv.labs.arxiv.org/html/{paper_id}/{img_url}"
                    
                    img_path = download_image(img_url, paper_id)
                    if img_path:
                        return img_path
    except Exception as e:
        print(f"    ar5iv fetch failed: {e}")
    
    print(f"    No figure found for {paper_id}")
    return None


def download_image(url: str, paper_id: str) -> str | None:
    """Download an image to a temporary file. Returns file path or None."""
    try:
        import tempfile
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ExoplanetBot/1.0)'
        })
        
        if response.status_code != 200:
            return None
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if not any(t in content_type for t in ['image/png', 'image/jpeg', 'image/gif', 'image/webp']):
            # Try to detect from content
            if not response.content[:8].startswith((b'\x89PNG', b'\xff\xd8\xff', b'GIF8')):
                return None
        
        # Check size (Twitter requires images > 5KB, < 5MB)
        size = len(response.content)
        if size < 5000 or size > 5_000_000:
            print(f"    Image size {size} bytes - skipping (too small or large)")
            return None
        
        # Determine extension
        if b'\x89PNG' in response.content[:8]:
            ext = '.png'
        elif b'\xff\xd8\xff' in response.content[:8]:
            ext = '.jpg'
        elif b'GIF8' in response.content[:8]:
            ext = '.gif'
        else:
            ext = '.png'  # Default
        
        # Save to cross-platform temp directory
        safe_id = paper_id.replace('/', '_').replace('.', '_')
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"arxiv_fig_{safe_id}{ext}")
        
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        print(f"    Downloaded figure: {temp_path} ({size/1024:.1f} KB)")
        return temp_path
        
    except Exception as e:
        print(f"    Image download failed: {e}")
        return None


def generate_paper_card(paper: dict) -> str | None:
    """
    Generate a branded "paper card" image as fallback when no figure is available.
    Returns the local file path if successful, None otherwise.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("    PIL not available for paper card generation")
        return None
    
    try:
        import tempfile
        import platform
        
        # Card dimensions (Twitter recommends 1200x675 for cards)
        width, height = 1200, 675
        
        # Colors
        bg_color = "#0f172a"  # Dark blue
        accent_color = "#6366f1"  # Indigo
        text_color = "#f8fafc"  # Near white
        muted_color = "#94a3b8"  # Gray
        
        # Create image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw accent bar at top
        draw.rectangle([(0, 0), (width, 8)], fill=accent_color)
        
        # Try to load fonts (with cross-platform support)
        title_font = None
        body_font = None
        small_font = None
        
        # Font paths for different operating systems
        font_paths = []
        if platform.system() == "Windows":
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
                "C:/Windows/Fonts/calibri.ttf",
            ]
        else:  # Linux/Mac
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
            ]
        
        # Try to load a font
        for font_path in font_paths:
            try:
                title_font = ImageFont.truetype(font_path, 42)
                body_font = ImageFont.truetype(font_path, 28)
                small_font = ImageFont.truetype(font_path, 22)
                break
            except:
                continue
        
        # Fallback to default if no font found
        if title_font is None:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Wrap and draw title
        title = paper["title"]
        # Simple word wrap
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
        
        # Limit to 4 lines
        if len(lines) > 4:
            lines = lines[:4]
            lines[-1] = lines[-1][:50] + "..."
        
        y_pos = 60
        for line in lines:
            draw.text((50, y_pos), line, fill=text_color, font=title_font)
            y_pos += 55
        
        # Draw hook/key insight if available
        tweet_hook = paper.get("tweet_hook", {})
        hook = tweet_hook.get("hook", "")
        if hook:
            # Wrap hook text
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
        
        # Draw planet emoji (as text, won't render as emoji but shows intent)
        draw.text((width - 100, height - 80), "🪐", fill=accent_color, font=small_font)
        
        # Save to cross-platform temp directory
        safe_id = paper["id"].replace('/', '_').replace('.', '_')
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"arxiv_card_{safe_id}.png")
        img.save(temp_path, 'PNG')
        
        print(f"    Generated paper card: {temp_path}")
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
    
    # v2 client for tweeting
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
    )
    
    # v1.1 API for media uploads (v2 doesn't support media upload directly)
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
    """
    Extract relevant hashtags from paper title and abstract.
    Uses strict matching to avoid false positives.
    """
    text = f"{paper['title']} {paper['abstract']}".lower()
    is_exoplanet = paper.get('is_exoplanet_focused', False)
    
    found_hashtags = []
    
    # Choose which keyword set to use based on paper type
    if is_exoplanet:
        keyword_set = KEYWORD_HASHTAGS
        base_tags = BASE_HASHTAGS_EXOPLANET.copy()
    else:
        keyword_set = GENERAL_HASHTAGS
        base_tags = BASE_HASHTAGS_GENERAL.copy()
    
    # Check for keyword matches (all keys are lowercase)
    for keyword, hashtag in keyword_set.items():
        if keyword in text:
            # Avoid duplicates
            if hashtag not in found_hashtags and hashtag not in base_tags:
                found_hashtags.append(hashtag)
    
    # If no specific hashtags found, that's okay - we'll use base tags
    # Prioritize high-value hashtags for exoplanet papers
    if is_exoplanet:
        priority_prefixes = ["#JWST", "#Habitable", "#Biosig", "#TRAPPIST", "#EarthLike", "#SuperEarth"]
        priority = [h for h in found_hashtags if any(h.startswith(p) for p in priority_prefixes)]
        others = [h for h in found_hashtags if h not in priority]
        found_hashtags = priority + others
    
    # Build final list: base tags + content-specific tags (up to max)
    result = base_tags[:2]  # Always include 2 base tags
    remaining_slots = max_hashtags - len(result)
    
    for h in found_hashtags[:remaining_slots]:
        if h not in result:
            result.append(h)
    
    return result


def is_prime_time_pst() -> bool:
    """
    Check if current time is PST prime time for tweeting exoplanet papers.
    Prime time PST: 8 AM - 12 PM and 5 PM - 11 PM
    
    In UTC (PST = UTC - 8):
    - 8 AM - 12 PM PST = 16:00 - 20:00 UTC
    - 5 PM - 11 PM PST = 01:00 - 07:00 UTC
    """
    from datetime import datetime, timezone
    
    now_utc = datetime.now(timezone.utc)
    hour = now_utc.hour
    
    # Morning prime time: 16:00-20:00 UTC (8 AM - 12 PM PST)
    # Evening prime time: 01:00-07:00 UTC (5 PM - 11 PM PST)
    morning_prime = 16 <= hour < 20
    evening_prime = 1 <= hour < 7
    
    return morning_prime or evening_prime


def select_best_paper(papers: list, tweeted_ids: set) -> dict | None:
    """
    Select the best untweeted paper based on time of day.
    
    - During PST prime time: prioritize exoplanet-focused papers
    - During off-peak: tweet other astro-ph.EP papers
    - Falls back to any untweeted paper if preferred category is empty
    """
    untweeted = [p for p in papers if p["id"] not in tweeted_ids]
    
    if not untweeted:
        return None
    
    prime_time = is_prime_time_pst()
    
    # Separate exoplanet and non-exoplanet papers
    exoplanet_papers = [p for p in untweeted if p.get("is_exoplanet_focused", True)]
    other_papers = [p for p in untweeted if not p.get("is_exoplanet_focused", True)]
    
    # Sort each group by tweetability
    exoplanet_papers.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    other_papers.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    
    if prime_time:
        # Prime time: prefer exoplanet papers, fall back to others
        print(f"🌟 PRIME TIME (PST) - Prioritizing exoplanet papers")
        if exoplanet_papers:
            return exoplanet_papers[0]
        elif other_papers:
            print(f"   No exoplanet papers left, using general astro-ph.EP")
            return other_papers[0]
    else:
        # Off-peak: prefer other papers, fall back to exoplanets
        print(f"📋 OFF-PEAK - Tweeting general astro-ph.EP papers")
        if other_papers:
            return other_papers[0]
        elif exoplanet_papers:
            print(f"   No general papers left, using exoplanet paper")
            return exoplanet_papers[0]
    
    return None


def format_tweet_thread_free(paper: dict, page_url: str, hashtags: list[str]) -> tuple[str, str]:
    """Format 2-tweet thread for free Twitter (280 chars each)."""
    
    tweet_hook = paper.get("tweet_hook", {})
    hook = tweet_hook.get("hook", "")
    claim = tweet_hook.get("claim", "")
    evidence = tweet_hook.get("evidence", "")
    question = tweet_hook.get("question", "")
    
    # Tweet 1: Hook + question (no links, image attached)
    if hook and question:
        tweet1 = f"{hook}\n\n{question}"
    elif hook:
        tweet1 = hook
    else:
        # Fallback to title
        tweet1 = truncate_text(paper["title"], 250)
    
    # Ensure tweet 1 fits
    if len(tweet1) > 280:
        tweet1 = truncate_text(tweet1, 277)
    
    # Tweet 2: Links + hashtags
    link = paper["abs_link"]
    paper_id = paper["id"]
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', paper_id)
    summary_link = f"{page_url}#paper-{safe_id}"
    
    hashtag_str = " ".join(hashtags)
    
    tweet2 = f"📄 {link}\n📖 Full summary: {summary_link}\n\n{hashtag_str}"
    
    # Ensure tweet 2 fits
    if len(tweet2) > 280:
        # Reduce hashtags
        hashtag_str = " ".join(hashtags[:2])
        tweet2 = f"📄 {link}\n📖 {summary_link}\n\n{hashtag_str}"
    
    return tweet1, tweet2


def format_tweet_thread_premium(paper: dict, page_url: str, hashtags: list[str], limit: int) -> tuple[str, str]:
    """Format 2-tweet thread for Twitter Premium."""
    
    tweet_hook = paper.get("tweet_hook", {})
    hook = tweet_hook.get("hook", "")
    claim = tweet_hook.get("claim", "")
    evidence = tweet_hook.get("evidence", "")
    question = tweet_hook.get("question", "")
    
    title = paper["title"]
    authors = paper.get("authors", [])
    
    # Format authors
    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) <= 2:
        author_str = " & ".join(authors)
    else:
        author_str = f"{authors[0]} et al."
    
    # Tweet 1: Full content (no links, image attached)
    parts = [title, "", author_str, ""]
    
    if hook:
        parts.extend([hook, ""])
    if claim:
        parts.extend([claim, ""])
    if evidence:
        parts.extend([evidence, ""])
    if question:
        parts.extend(["", question])
    
    tweet1 = "\n".join(parts)
    
    # Clean up multiple blank lines
    while "\n\n\n" in tweet1:
        tweet1 = tweet1.replace("\n\n\n", "\n\n")
    
    tweet1 = tweet1.strip()
    
    # Truncate if needed
    if len(tweet1) > limit:
        tweet1 = truncate_text(tweet1, limit - 3)
    
    # Tweet 2: Links + hashtags
    link = paper["abs_link"]
    paper_id = paper["id"]
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', paper_id)
    summary_link = f"{page_url}#paper-{safe_id}"
    
    hashtag_str = " ".join(hashtags)
    
    tweet2 = f"📄 arXiv: {link}\n📖 Full summary: {summary_link}\n\n{hashtag_str}"
    
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
    """Upload an image to Twitter. Returns media_id on success."""
    try:
        media = api_v1.media_upload(filename=image_path)
        print(f"Uploaded media: {media.media_id}")
        return str(media.media_id)
    except tweepy.TweepyException as e:
        print(f"Error uploading media: {e}")
        return None


def post_tweet(client: tweepy.Client, tweet_text: str, media_ids: list[str] = None, reply_to: str = None) -> str | None:
    """Post a single tweet with optional media and reply. Returns tweet ID on success."""
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
            print(f"Cleaned up temp file: {filepath}")
    except Exception as e:
        print(f"Could not clean up {filepath}: {e}")


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
    
    # Select the best paper to tweet based on time of day
    paper_to_tweet = select_best_paper(papers, tweeted_ids)
    
    if not paper_to_tweet:
        print("All papers have been tweeted today!")
        return
    
    paper_type = "🪐 EXOPLANET" if paper_to_tweet.get("is_exoplanet_focused", True) else "🔭 GENERAL"
    print(f"Selected paper: {paper_to_tweet['id']}")
    print(f"  Type: {paper_type}")
    print(f"  Tweetability: {paper_to_tweet.get('tweetability_score', 0)}")
    
    # Create Twitter clients (v2 for tweeting, v1.1 for media upload)
    client, api_v1 = create_twitter_client()
    if not client:
        print("Could not create Twitter client. Exiting.")
        return
    
    # Get page URL
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    
    # Try to get an image (figure or fallback card)
    figure_path = None
    media_ids = None
    
    if api_v1:  # Only try if we have v1.1 API for media upload
        # Try to fetch actual figure first
        figure_path = fetch_paper_figure(paper_to_tweet["id"])
        
        # If no figure, generate a paper card
        if not figure_path:
            print("  Generating fallback paper card...")
            figure_path = generate_paper_card(paper_to_tweet)
        
        if figure_path:
            media_id = upload_media(api_v1, figure_path)
            if media_id:
                media_ids = [media_id]
                print(f"📸 Image will be attached to tweet!")
            else:
                print("⚠️ Image upload failed, tweeting without image")
        else:
            print("📄 No image available, tweeting text only")
    
    # Format the 2-tweet thread
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
    
    # Post tweet 1 (with image, no links)
    tweet1_id = post_tweet(client, tweet1_text, media_ids)
    
    # Clean up temp file after upload
    if figure_path:
        cleanup_temp_file(figure_path)
    
    if tweet1_id:
        # Post tweet 2 as reply (with links)
        tweet2_id = post_tweet(client, tweet2_text, reply_to=tweet1_id)
        
        if tweet2_id:
            # Mark as tweeted
            tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(tweeted_ids)
            save_tweeted(tweeted_data)
            print(f"\n✅ Thread posted successfully!")
            print(f"   Tweet 1: https://twitter.com/i/status/{tweet1_id}")
            print(f"   Tweet 2: https://twitter.com/i/status/{tweet2_id}")
            print(f"   Remaining papers: {len(papers) - len(tweeted_ids)}")
        else:
            print("\n⚠️ Tweet 1 posted but Tweet 2 failed")
            # Still mark as tweeted to avoid duplicate tweet 1s
            tweeted_ids.add(paper_to_tweet["id"])
            tweeted_data["tweeted_ids"] = list(tweeted_ids)
            save_tweeted(tweeted_data)
    else:
        print("\n❌ Failed to post tweet")
        sys.exit(1)


if __name__ == "__main__":
    main()
