#!/usr/bin/env python3
"""
Post exoplanet papers to Bluesky.
Uses announcement_date from papers.json to track which papers have been posted.

Changes:
- Links now include ?date=YYYY-MM-DD for archive compatibility

Requires:
    pip install atproto requests pillow
    
Environment variables:
    BLUESKY_HANDLE: Your handle (e.g., yourname.bsky.social)
    BLUESKY_PASSWORD: Your app password (NOT your main password!)
    
To create an app password:
    1. Go to Settings → App Passwords in Bluesky
    2. Create a new app password
    3. Use that as BLUESKY_PASSWORD
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

# Optional: atproto library for richer posts
try:
    from atproto import Client, models
    HAS_ATPROTO = True
except ImportError:
    HAS_ATPROTO = False
    print("Note: Install 'atproto' for richer posts: pip install atproto")

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
POSTED_FILE = DATA_DIR / "bluesky_posted.json"

# Bluesky limits
MAX_POST_LENGTH = 300
MAX_IMAGES = 4

# Hashtags (Bluesky doesn't have real hashtags, but we can use them in text)
BASE_TAGS = ["exoplanets", "astronomy", "arxiv"]


def is_placeholder_image(url: str) -> bool:
    """Check if URL is a placeholder/stock image."""
    placeholders = [
        "unsplash.com",
        "placeholder",
        "stock",
        "generic",
        "default"
    ]
    return any(p in url.lower() for p in placeholders)


def download_image(url: str, paper_id: str) -> str | None:
    """Download image to temp file. Returns path or None."""
    if not url or is_placeholder_image(url):
        return None
    
    try:
        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; ExoplanetBot/1.0)"
        })
        
        if response.status_code == 200:
            # Determine extension
            content_type = response.headers.get("content-type", "")
            if "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            else:
                ext = ".jpg"
            
            # Save to temp file
            safe_id = paper_id.replace("/", "-").replace(".", "-")
            temp_path = os.path.join(tempfile.gettempdir(), f"bsky_{safe_id}{ext}")
            
            with open(temp_path, "wb") as f:
                f.write(response.content)
            
            print(f"📸 Downloaded image: {temp_path}")
            return temp_path
    except Exception as e:
        print(f"Image download failed: {e}")
    
    return None


def cleanup_temp_file(filepath: str):
    """Remove temporary file."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except:
        pass


def load_papers():
    """Load papers from JSON file."""
    if not PAPERS_FILE.exists():
        print("No papers file found")
        return None
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_posted():
    """Load list of already posted paper IDs (keeps 7 days of history)."""
    if not POSTED_FILE.exists():
        return {"posted_ids": [], "history": {}, "last_reset": None}
    
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Migrate old format to new format
    if "history" not in data:
        data["history"] = {}
        if data.get("posted_ids") and data.get("last_reset"):
            data["history"][data["last_reset"]] = data["posted_ids"]
    
    return data


def save_posted(data):
    """Save posted tracking data."""
    POSTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_all_posted_ids(posted_data: dict, days: int = 7) -> set:
    """Get all posted paper IDs from the last N days."""
    all_ids = set()
    history = posted_data.get("history", {})
    
    # Get IDs from history
    for date, ids in history.items():
        all_ids.update(ids)
    
    # Also include current posted_ids for backwards compatibility
    all_ids.update(posted_data.get("posted_ids", []))
    
    return all_ids


def cleanup_old_history(posted_data: dict, days: int = 7) -> dict:
    """Remove history older than N days."""
    from datetime import timedelta
    
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    history = posted_data.get("history", {})
    
    # Keep only recent dates
    new_history = {date: ids for date, ids in history.items() if date >= cutoff}
    posted_data["history"] = new_history
    
    return posted_data


def get_safe_id(paper_id: str) -> str:
    """Convert paper ID to URL-safe format."""
    return re.sub(r'[^a-zA-Z0-9]', '-', paper_id)


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length, preserving words."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - 3]
    last_space = truncated.rfind(" ")
    if last_space > max_length // 2:
        truncated = truncated[:last_space]
    
    return truncated + "..."


def build_summary_link(page_url: str, paper_id: str, papers_date: str) -> str:
    """Build summary link with date parameter for archive compatibility."""
    safe_id = get_safe_id(paper_id)
    # Always include date parameter so links work even after new papers are posted
    return f"{page_url}?date={papers_date}#paper-{safe_id}"


def format_post(paper: dict, page_url: str, papers_date: str) -> str:
    """Format a Bluesky post for a paper."""
    
    title = paper["title"]
    paper_id = paper["id"]
    
    # Get hook if available
    hook = ""
    tweet_hook = paper.get("tweet_hook", {})
    if tweet_hook.get("hook"):
        hook = tweet_hook["hook"]
    
    # Build post
    arxiv_link = paper["abs_link"]
    summary_link = build_summary_link(page_url, paper_id, papers_date)
    
    # Format: Title + hook + links
    post = f"{title}\n\n"
    
    if hook:
        post += f"{hook}\n\n"
    
    post += f"📄 {arxiv_link}\n"
    post += f"📖 Summary: {summary_link}"
    
    # Truncate if needed
    if len(post) > MAX_POST_LENGTH:
        # Try without hook
        post = f"{title}\n\n📄 {arxiv_link}\n📖 {summary_link}"
        
        if len(post) > MAX_POST_LENGTH:
            # Truncate title
            max_title = MAX_POST_LENGTH - len(f"\n\n📄 {arxiv_link}\n📖 {summary_link}") - 3
            post = f"{truncate_text(title, max_title)}\n\n📄 {arxiv_link}\n📖 {summary_link}"
    
    return post


def create_bluesky_session():
    """Create authenticated Bluesky session."""
    handle = os.environ.get("BLUESKY_HANDLE")
    password = os.environ.get("BLUESKY_PASSWORD")
    
    if not handle or not password:
        print("Missing BLUESKY_HANDLE or BLUESKY_PASSWORD")
        return None
    
    if HAS_ATPROTO:
        try:
            client = Client()
            client.login(handle, password)
            print(f"Logged in as {handle}")
            return client
        except Exception as e:
            print(f"Login failed: {e}")
            return None
    else:
        # Manual API approach
        try:
            resp = requests.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": handle, "password": password}
            )
            resp.raise_for_status()
            session = resp.json()
            print(f"Logged in as {handle}")
            return session
        except Exception as e:
            print(f"Login failed: {e}")
            return None


def post_to_bluesky(client, text: str, image_path: str = None) -> str | None:
    """Post to Bluesky. Returns post URI on success."""
    
    if HAS_ATPROTO:
        try:
            # Upload image if provided
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    img_data = f.read()
                
                # Detect mime type
                if image_path.endswith(".png"):
                    mime = "image/png"
                elif image_path.endswith(".gif"):
                    mime = "image/gif"
                else:
                    mime = "image/jpeg"
                
                # Upload blob (new atproto API - mime type auto-detected)
                upload = client.upload_blob(img_data)
                
                # Create post with image
                embed = models.AppBskyEmbedImages.Main(
                    images=[models.AppBskyEmbedImages.Image(
                        alt="Paper figure",
                        image=upload.blob
                    )]
                )
                
                response = client.send_post(text=text, embed=embed)
            else:
                response = client.send_post(text=text)
            
            print(f"Posted: {response.uri}")
            return response.uri
            
        except Exception as e:
            print(f"Post failed: {e}")
            return None
    else:
        # Manual API (no image support without atproto)
        try:
            session = client  # client is session dict in this case
            
            now = datetime.utcnow().isoformat() + "Z"
            
            resp = requests.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": text,
                        "createdAt": now,
                    }
                }
            )
            resp.raise_for_status()
            result = resp.json()
            print(f"Posted: {result.get('uri')}")
            return result.get("uri")
            
        except Exception as e:
            print(f"Post failed: {e}")
            return None


def select_paper(papers: list, posted_ids: set) -> dict | None:
    """Select best unposted paper."""
    
    # Filter out hidden papers first
    visible = [p for p in papers if not p.get("hidden", False)]
    
    # Filter unposted
    unposted = [p for p in visible if p["id"] not in posted_ids]
    
    if not unposted:
        return None
    
    # STRICT FILTER: Only post exoplanet papers!
    exo = [p for p in unposted if p.get("is_exoplanet_focused", False)]
    
    if not exo:
        non_exo_count = len([p for p in unposted if not p.get("is_exoplanet_focused", False)])
        if non_exo_count > 0:
            print(f"⚠️ {non_exo_count} non-exoplanet papers skipped (strict mode)")
        print("No exoplanet papers to post")
        return None
    
    # Sort by tweetability
    exo.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    
    return exo[0]


def main():
    """Main function - post ONE paper to Bluesky."""
    
    # Load papers
    data = load_papers()
    if not data or not data.get("papers"):
        print("No papers available")
        return
    
    papers = data["papers"]
    
    # Use announcement_date for tracking (fallback to updated_at for backwards compatibility)
    papers_date = data.get("announcement_date") or data.get("updated_at", "")[:10]
    print(f"Papers announcement date: {papers_date}")
    print(f"Total papers: {len(papers)}")
    
    # Load posted tracking
    posted_data = load_posted()
    last_reset = posted_data.get("last_reset")
    
    # Get ALL posted IDs from last 7 days (not just today)
    all_posted_ids = get_all_posted_ids(posted_data, days=7)
    print(f"Papers posted in last 7 days: {len(all_posted_ids)}")
    
    # If new day, update tracking structure
    if last_reset != papers_date:
        print(f"New day detected (was: {last_reset}, now: {papers_date})")
        
        # Save yesterday's posts to history before resetting
        if last_reset and posted_data.get("posted_ids"):
            if "history" not in posted_data:
                posted_data["history"] = {}
            posted_data["history"][last_reset] = posted_data.get("posted_ids", [])
        
        # Reset today's list but keep history
        posted_data["posted_ids"] = []
        posted_data["last_reset"] = papers_date
        
        # Cleanup old history (older than 7 days)
        posted_data = cleanup_old_history(posted_data, days=7)
        save_posted(posted_data)
    
    # Today's posted IDs (for counting remaining)
    todays_posted_ids = set(posted_data.get("posted_ids", []))
    
    # Select paper (check against ALL recent posts)
    paper = select_paper(papers, all_posted_ids)
    
    if not paper:
        print("All papers have been posted (or were posted recently)!")
        return
    
    print(f"Selected paper: {paper['id']}")
    print(f"  Title: {paper['title'][:60]}...")
    
    # Create session
    client = create_bluesky_session()
    if not client:
        print("Could not authenticate with Bluesky")
        return
    
    # Format post (now with papers_date)
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    post_text = format_post(paper, page_url, papers_date)
    
    print(f"\nPost ({len(post_text)} chars):")
    print("-" * 40)
    print(post_text)
    print("-" * 40)
    
    # Download image if available
    image_path = None
    figure_url = paper.get("figure_url", "")
    
    if figure_url and not is_placeholder_image(figure_url):
        print(f"\n📷 Downloading image from: {figure_url[:60]}...")
        image_path = download_image(figure_url, paper["id"])
        if image_path:
            print(f"   ✓ Image ready for upload")
        else:
            print(f"   ⚠ Could not download image, posting without")
    else:
        print("\n📄 No figure available, posting text only")
    
    # Post with image
    uri = post_to_bluesky(client, post_text, image_path)
    
    # Cleanup temp file
    if image_path:
        cleanup_temp_file(image_path)
    
    if uri:
        todays_posted_ids.add(paper["id"])
        posted_data["posted_ids"] = list(todays_posted_ids)
        save_posted(posted_data)
        print(f"\n✅ Posted successfully!")
        print(f"   Posted today: {len(todays_posted_ids)}")
        print(f"   Remaining today: {len(papers) - len(todays_posted_ids)}")
    else:
        print("\n❌ Failed to post")
        sys.exit(1)


if __name__ == "__main__":
    main()
