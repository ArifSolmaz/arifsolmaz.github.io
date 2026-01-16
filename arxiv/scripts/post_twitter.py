#!/usr/bin/env python3
"""
Post individual exoplanet paper summaries to Twitter/X.
Tweets ONE paper per run with dynamic hashtags extracted from paper content.
Attempts to attach Figure 1 from the paper when available.

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
# Maps common terms found in papers to appropriate hashtags
KEYWORD_HASHTAGS = {
    # Detection methods
    "transit": "#TransitMethod",
    "transiting": "#TransitMethod",
    "radial velocity": "#RadialVelocity",
    "RV": "#RadialVelocity",
    "microlensing": "#Microlensing",
    "direct imaging": "#DirectImaging",
    "astrometry": "#Astrometry",
    "photometry": "#Photometry",
    "spectroscopy": "#Spectroscopy",
    "transmission spectrum": "#TransmissionSpectroscopy",
    "emission spectrum": "#EmissionSpectroscopy",
    
    # Telescopes & Instruments
    "JWST": "#JWST",
    "James Webb": "#JWST",
    "Webb": "#JWST",
    "Hubble": "#Hubble #HST",
    "HST": "#HST",
    "TESS": "#TESS",
    "Kepler": "#Kepler",
    "K2": "#K2",
    "CHEOPS": "#CHEOPS",
    "Spitzer": "#Spitzer",
    "VLT": "#VLT",
    "Keck": "#Keck",
    "ALMA": "#ALMA",
    "HARPS": "#HARPS",
    "ESPRESSO": "#ESPRESSO",
    "NIRSpec": "#JWST #NIRSpec",
    "MIRI": "#JWST #MIRI",
    "NIRCam": "#JWST #NIRCam",
    "Roman": "#NancyGraceRoman",
    "Euclid": "#Euclid",
    "PLATO": "#PLATO",
    "Ariel": "#Ariel",
    "ELT": "#ELT",
    "GMT": "#GMT",
    "TMT": "#TMT",
    
    # Planet types
    "hot Jupiter": "#HotJupiter",
    "hot Jupiters": "#HotJupiters",
    "warm Jupiter": "#WarmJupiter",
    "cold Jupiter": "#ColdJupiter",
    "super-Earth": "#SuperEarth",
    "super Earth": "#SuperEarth",
    "super-Earths": "#SuperEarths",
    "sub-Neptune": "#SubNeptune",
    "sub Neptune": "#SubNeptune",
    "mini-Neptune": "#MiniNeptune",
    "mini Neptune": "#MiniNeptune",
    "Earth-like": "#EarthLike",
    "Earth-sized": "#EarthSized",
    "terrestrial": "#TerrestrialPlanet",
    "gas giant": "#GasGiant",
    "ice giant": "#IceGiant",
    "rocky planet": "#RockyPlanet",
    "lava world": "#LavaWorld",
    "ocean world": "#OceanWorld",
    "water world": "#WaterWorld",
    "rogue planet": "#RoguePlanet",
    "free-floating": "#RoguePlanet",
    
    # Atmospheres & Composition
    "atmosphere": "#ExoplanetAtmosphere",
    "atmospheric": "#ExoplanetAtmosphere",
    "water vapor": "#WaterVapor",
    "H2O": "#WaterVapor",
    "carbon dioxide": "#CO2",
    "CO2": "#CO2",
    "methane": "#Methane",
    "CH4": "#Methane",
    "ammonia": "#Ammonia",
    "hydrogen": "#Hydrogen",
    "helium": "#Helium",
    "oxygen": "#Oxygen",
    "nitrogen": "#Nitrogen",
    "sulfur": "#Sulfur",
    "sodium": "#Sodium",
    "potassium": "#Potassium",
    "iron": "#Iron",
    "silicate": "#Silicates",
    "clouds": "#ExoplanetClouds",
    "haze": "#ExoplanetHaze",
    "aerosol": "#Aerosols",
    
    # Habitability & Biosignatures
    "habitable": "#HabitableZone",
    "habitable zone": "#HabitableZone",
    "habitability": "#Habitability",
    "biosignature": "#Biosignatures",
    "biosignatures": "#Biosignatures",
    "biomarker": "#Biosignatures",
    "life": "#Astrobiology",
    "astrobiology": "#Astrobiology",
    "SETI": "#SETI",
    "technosignature": "#Technosignatures",
    
    # Stellar types
    "M dwarf": "#MDwarf",
    "M-dwarf": "#MDwarf",
    "red dwarf": "#RedDwarf",
    "K dwarf": "#KDwarf",
    "G dwarf": "#SunLikeStar",
    "Sun-like": "#SunLikeStar",
    "solar-type": "#SunLikeStar",
    "white dwarf": "#WhiteDwarf",
    "binary": "#BinaryStar",
    "circumbinary": "#Circumbinary",
    
    # Notable systems
    "TRAPPIST-1": "#TRAPPIST1",
    "TRAPPIST": "#TRAPPIST1",
    "Proxima": "#ProximaCentauri",
    "Proxima Centauri": "#ProximaCentauri",
    "55 Cancri": "#55Cancri",
    "GJ 1214": "#GJ1214",
    "GJ 436": "#GJ436",
    "HD 189733": "#HD189733",
    "HD 209458": "#HD209458",
    "WASP-39": "#WASP39",
    "WASP-76": "#WASP76",
    "WASP-121": "#WASP121",
    "TOI-700": "#TOI700",
    "LHS 1140": "#LHS1140",
    "K2-18": "#K218b",
    "Kepler-186": "#Kepler186",
    "Kepler-452": "#Kepler452",
    
    # Processes & Phenomena
    "migration": "#PlanetMigration",
    "formation": "#PlanetFormation",
    "protoplanetary": "#ProtoplanetaryDisk",
    "disk": "#ProtoplanetaryDisk",
    "accretion": "#Accretion",
    "tidal": "#TidalEffects",
    "tidal heating": "#TidalHeating",
    "obliquity": "#Obliquity",
    "eccentricity": "#Eccentricity",
    "resonance": "#OrbitalResonance",
    "mean motion resonance": "#OrbitalResonance",
    "MMR": "#OrbitalResonance",
    "evaporation": "#AtmosphericEscape",
    "escape": "#AtmosphericEscape",
    "mass loss": "#AtmosphericEscape",
    "photoevaporation": "#Photoevaporation",
    "interior": "#PlanetaryInterior",
    "core": "#PlanetaryCore",
    "mantle": "#PlanetaryMantle",
    "magnetic field": "#MagneticField",
    "magnetosphere": "#Magnetosphere",
    "volcanism": "#Volcanism",
    "volcanic": "#Volcanism",
    "climate": "#ExoplanetClimate",
    "temperature": "#Temperature",
    "rotation": "#Rotation",
    "tidally locked": "#TidallyLocked",
    
    # Statistics & Surveys
    "occurrence rate": "#OccurrenceRate",
    "demographics": "#ExoplanetDemographics",
    "population": "#ExoplanetPopulation",
    "catalog": "#ExoplanetCatalog",
    "survey": "#ExoplanetSurvey",
    "confirmed": "#ConfirmedExoplanet",
    "candidate": "#ExoplanetCandidate",
    "validation": "#PlanetValidation",
    
    # Machine Learning
    "machine learning": "#MachineLearning #ML",
    "deep learning": "#DeepLearning",
    "neural network": "#NeuralNetwork",
    "AI": "#AI",
    "artificial intelligence": "#AI",
}

# Base hashtags always included
BASE_HASHTAGS = ["#Exoplanets", "#Astronomy", "#arXiv"]


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
        
        # Save to temp file
        safe_id = paper_id.replace('/', '_').replace('.', '_')
        temp_path = f"/tmp/arxiv_fig_{safe_id}{ext}"
        
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        print(f"    Downloaded figure: {temp_path} ({size/1024:.1f} KB)")
        return temp_path
        
    except Exception as e:
        print(f"    Image download failed: {e}")
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


def extract_hashtags(paper: dict, max_hashtags: int = 8) -> list[str]:
    """Extract relevant hashtags from paper title and abstract."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    
    found_hashtags = set()
    
    # Check for keyword matches
    for keyword, hashtag in KEYWORD_HASHTAGS.items():
        if keyword.lower() in text:
            # Some entries have multiple hashtags
            for tag in hashtag.split():
                found_hashtags.add(tag)
    
    # Convert to list and limit
    hashtags = list(found_hashtags)
    
    # Prioritize certain categories
    priority_prefixes = ["#JWST", "#TESS", "#TRAPPIST", "#Habitable", "#Biosig", "#WASP"]
    priority = [h for h in hashtags if any(h.startswith(p) for p in priority_prefixes)]
    others = [h for h in hashtags if h not in priority]
    
    # Combine: priority first, then others
    sorted_hashtags = priority + others
    
    # Limit to max and add base hashtags
    paper_hashtags = sorted_hashtags[:max_hashtags]
    
    # Add base hashtags (always included)
    all_hashtags = BASE_HASHTAGS + paper_hashtags
    
    # Remove duplicates while preserving order
    seen = set()
    unique_hashtags = []
    for h in all_hashtags:
        if h not in seen:
            seen.add(h)
            unique_hashtags.append(h)
    
    return unique_hashtags


def extract_summary_sections(summary: str) -> dict[str, str]:
    """Extract individual sections from the AI summary."""
    sections = {
        "why_it_matters": "",
        "what_they_did": "",
        "key_findings": "",
        "looking_forward": ""
    }
    
    if not summary:
        return sections
    
    # Define section markers
    markers = {
        "why_it_matters": ["Why It Matters", "Why it Matters"],
        "what_they_did": ["What They Did", "What they Did"],
        "key_findings": ["Key Findings", "Key findings"],
        "looking_forward": ["Looking Forward", "Looking forward", "Implications"]
    }
    
    for section_key, section_markers in markers.items():
        for marker in section_markers:
            if marker in summary:
                parts = summary.split(marker)
                if len(parts) > 1:
                    content = parts[1]
                    # Clean up
                    content = content.lstrip("*: \n")
                    # Stop at next section
                    for other_markers in markers.values():
                        for other_marker in other_markers:
                            if other_marker in content and other_marker != marker:
                                content = content.split(other_marker)[0]
                    
                    # Clean and store - remove markdown ** markers
                    content = content.strip().replace("\n", " ")
                    content = content.replace("**", "")  # Remove bold markers
                    content = re.sub(r'\s+', ' ', content)
                    sections[section_key] = content
                    break
    
    return sections


def format_tweet_free(paper: dict, page_url: str, hashtags: list[str]) -> str:
    """Format tweet for free Twitter (280 chars)."""
    title = paper["title"]
    link = paper["abs_link"]
    
    # Get brief summary
    sections = extract_summary_sections(paper.get("summary", ""))
    brief = sections["why_it_matters"] or sections["key_findings"]
    
    # Build components
    hashtag_str = " ".join(hashtags[:5])  # Limit hashtags for free
    
    # Calculate available space
    fixed = f"🪐 \n\n🔗 {link}\n\n{hashtag_str}"
    available = 280 - len(fixed) - 10
    
    if brief:
        title_space = int(available * 0.5)
        brief_space = available - title_space - 5
        
        truncated_title = truncate_text(title, title_space)
        truncated_brief = truncate_text(brief, brief_space)
        
        tweet = f"🪐 {truncated_title}\n\n💡 {truncated_brief}\n\n🔗 {link}\n\n{hashtag_str}"
    else:
        truncated_title = truncate_text(title, available)
        tweet = f"🪐 {truncated_title}\n\n🔗 {link}\n\n{hashtag_str}"
    
    # Safety truncation
    if len(tweet) > 280:
        overflow = len(tweet) - 277
        hashtag_str = " ".join(hashtags[:3])
        tweet = f"🪐 {truncate_text(title, available - overflow)}\n\n🔗 {link}\n\n{hashtag_str}"
    
    return tweet[:280]


def format_tweet_premium(paper: dict, page_url: str, hashtags: list[str], limit: int) -> str:
    """Format tweet for Twitter Premium (4000 or 25000 chars)."""
    title = paper["title"]
    link = paper["abs_link"]
    authors = paper.get("authors", [])
    
    # Format authors
    if len(authors) <= 3:
        author_str = ", ".join(authors)
    else:
        author_str = f"{', '.join(authors[:3])} et al."
    
    # Get full summary sections
    sections = extract_summary_sections(paper.get("summary", ""))
    
    # Build the tweet (no markdown - Twitter doesn't support it)
    hashtag_str = " ".join(hashtags)
    
    tweet_parts = [
        f"🪐 {title}",
        f"",
        f"👥 {author_str}",
        f"🔗 {link}",
    ]
    
    # Add summary sections
    if sections["why_it_matters"]:
        tweet_parts.extend([
            "",
            "🌟 WHY IT MATTERS",
            sections["why_it_matters"]
        ])
    
    if sections["what_they_did"]:
        tweet_parts.extend([
            "",
            "🔬 WHAT THEY DID", 
            sections["what_they_did"]
        ])
    
    if sections["key_findings"]:
        tweet_parts.extend([
            "",
            "💡 KEY FINDINGS",
            sections["key_findings"]
        ])
    
    if sections["looking_forward"]:
        tweet_parts.extend([
            "",
            "🔭 LOOKING FORWARD",
            sections["looking_forward"]
        ])
    
    # Add link to full page and hashtags
    tweet_parts.extend([
        "",
        f"📖 Full summary with all papers: {page_url}",
        "",
        hashtag_str
    ])
    
    tweet = "\n".join(tweet_parts)
    
    # Truncate if needed
    if len(tweet) > limit:
        tweet = tweet[:limit-3] + "..."
    
    return tweet


def format_paper_tweet(paper: dict, page_url: str) -> str:
    """Create a tweet for a single paper."""
    limit = get_tweet_limit()
    hashtags = extract_hashtags(paper)
    
    print(f"Tweet limit: {limit} chars")
    print(f"Extracted hashtags: {hashtags}")
    
    if limit > 280:
        return format_tweet_premium(paper, page_url, hashtags, limit)
    else:
        return format_tweet_free(paper, page_url, hashtags)


def upload_media(api_v1: tweepy.API, image_path: str) -> str | None:
    """Upload an image to Twitter. Returns media_id on success."""
    try:
        media = api_v1.media_upload(filename=image_path)
        print(f"Uploaded media: {media.media_id}")
        return str(media.media_id)
    except tweepy.TweepyException as e:
        print(f"Error uploading media: {e}")
        return None


def post_tweet(client: tweepy.Client, tweet_text: str, media_ids: list[str] = None) -> str | None:
    """Post a single tweet with optional media. Returns tweet ID on success."""
    try:
        if media_ids:
            response = client.create_tweet(text=tweet_text, media_ids=media_ids)
        else:
            response = client.create_tweet(text=tweet_text)
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
    """Main function - tweet ONE paper with figure if available."""
    
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
    
    # Find next paper to tweet
    paper_to_tweet = None
    for paper in papers:
        if paper["id"] not in tweeted_ids:
            paper_to_tweet = paper
            break
    
    if not paper_to_tweet:
        print("All papers have been tweeted today!")
        return
    
    # Create Twitter clients (v2 for tweeting, v1.1 for media upload)
    client, api_v1 = create_twitter_client()
    if not client:
        print("Could not create Twitter client. Exiting.")
        return
    
    # Get page URL
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    
    # Try to fetch a figure for the paper
    figure_path = None
    media_ids = None
    
    if api_v1:  # Only try if we have v1.1 API for media upload
        figure_path = fetch_paper_figure(paper_to_tweet["id"])
        
        if figure_path:
            media_id = upload_media(api_v1, figure_path)
            if media_id:
                media_ids = [media_id]
                print(f"📸 Figure will be attached to tweet!")
            else:
                print("⚠️ Figure upload failed, tweeting without image")
        else:
            print("📄 No figure found, tweeting text only")
    
    # Format and post tweet
    tweet_text = format_paper_tweet(paper_to_tweet, page_url)
    print(f"\nTweeting paper: {paper_to_tweet['id']}")
    print(f"Tweet ({len(tweet_text)} chars):\n")
    print("-" * 50)
    print(tweet_text)
    print("-" * 50)
    
    tweet_id = post_tweet(client, tweet_text, media_ids)
    
    # Clean up temp file
    if figure_path:
        cleanup_temp_file(figure_path)
    
    if tweet_id:
        # Mark as tweeted
        tweeted_ids.add(paper_to_tweet["id"])
        tweeted_data["tweeted_ids"] = list(tweeted_ids)
        save_tweeted(tweeted_data)
        print(f"\n✅ Successfully tweeted! Remaining papers: {len(papers) - len(tweeted_ids)}")
    else:
        print("\n❌ Failed to post tweet")
        sys.exit(1)


if __name__ == "__main__":
    main()