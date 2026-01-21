#!/usr/bin/env python3
"""
FIX for post_twitter.py - main() function

BEFORE (line ~280):
    papers_date = data.get("updated_at", "")[:10]

AFTER:
    # FIX: Use announcement_date (actual arXiv date) instead of updated_at (processing time)
    papers_date = data.get("announcement_date") or data.get("updated_at", "")[:10]
    print(f"Papers announcement date: {papers_date}")

This ensures the last_reset tracking matches the actual arXiv announcement date,
not when we processed the papers.
"""

# Here's the fixed main() function excerpt:

def main():
    """Main function - tweet ONE paper as a 2-tweet thread with image."""
    
    # Load papers
    data = load_papers()
    if not data or not data.get("papers"):
        print("No papers available")
        return
    
    papers = data["papers"]
    
    # FIX: Use announcement_date (actual arXiv date) instead of updated_at (processing time)
    # This matches how post_bluesky.py handles it
    papers_date = data.get("announcement_date") or data.get("updated_at", "")[:10]
    print(f"Papers announcement date: {papers_date}")
    
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
    
    # ... rest of function unchanged ...
