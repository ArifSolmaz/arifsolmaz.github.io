#!/usr/bin/env python3
"""
Post exoplanet papers to Bluesky.
Similar to Twitter posting but for Bluesky/AT Protocol.

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


def load_papers():
    """Load papers from JSON file."""
    if not PAPERS_FILE.exists():
        print("No papers file found")
        return None
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_posted():
    """Load list of already posted paper IDs."""
    if not POSTED_FILE.exists():
        return {"posted_ids": [], "last_reset": None}
    
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posted(data):
    """Save posted tracking data."""
    POSTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


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


def format_post(paper: dict, page_url: str) -> str:
    """Format a Bluesky post for a paper."""
    
    title = paper["title"]
    paper_id = paper["id"]
    safe_id = get_safe_id(paper_id)
    
    # Get hook if available
    hook = ""
    tweet_hook = paper.get("tweet_hook", {})
    if tweet_hook.get("hook"):
        hook = tweet_hook["hook"]
    
    # Build post
    arxiv_link = paper["abs_link"]
    summary_link = f"{page_url}#paper-{safe_id}"
    
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
                
                # Upload blob
                upload = client.upload_blob(img_data, mime)
                
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
    
    # Filter unposted
    unposted = [p for p in papers if p["id"] not in posted_ids]
    
    if not unposted:
        return None
    
    # Prioritize exoplanet papers
    exo = [p for p in unposted if p.get("is_exoplanet_focused", True)]
    gen = [p for p in unposted if not p.get("is_exoplanet_focused", True)]
    
    # Sort by tweetability
    exo.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    gen.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    
    # Return best exoplanet paper, or best general
    if exo:
        return exo[0]
    elif gen:
        return gen[0]
    
    return unposted[0]


def main():
    """Main function - post ONE paper to Bluesky."""
    
    # Load papers
    data = load_papers()
    if not data or not data.get("papers"):
        print("No papers available")
        return
    
    papers = data["papers"]
    papers_date = data.get("updated_at", "")[:10]
    
    # Load posted tracking
    posted_data = load_posted()
    posted_ids = set(posted_data.get("posted_ids", []))
    last_reset = posted_data.get("last_reset")
    
    # Reset if new day
    if last_reset != papers_date:
        print(f"New papers (date: {papers_date}). Resetting posted list.")
        posted_ids = set()
        posted_data = {"posted_ids": [], "last_reset": papers_date}
    
    # Select paper
    paper = select_paper(papers, posted_ids)
    
    if not paper:
        print("All papers have been posted today!")
        return
    
    print(f"Selected paper: {paper['id']}")
    print(f"  Title: {paper['title'][:60]}...")
    
    # Create session
    client = create_bluesky_session()
    if not client:
        print("Could not authenticate with Bluesky")
        return
    
    # Format post
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    post_text = format_post(paper, page_url)
    
    print(f"\nPost ({len(post_text)} chars):")
    print("-" * 40)
    print(post_text)
    print("-" * 40)
    
    # Post
    uri = post_to_bluesky(client, post_text)
    
    if uri:
        posted_ids.add(paper["id"])
        posted_data["posted_ids"] = list(posted_ids)
        save_posted(posted_data)
        print(f"\n✅ Posted successfully!")
        print(f"   Remaining papers: {len(papers) - len(posted_ids)}")
    else:
        print("\n❌ Failed to post")
        sys.exit(1)


if __name__ == "__main__":
    main()
