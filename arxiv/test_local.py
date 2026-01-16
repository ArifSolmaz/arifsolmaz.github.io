#!/usr/bin/env python3
"""
Test script to verify everything works before deploying.
Run this locally to test paper fetching, summary generation, and tweet formatting.

Usage:
    # Test everything (no Twitter posting)
    python test_local.py

    # Test with actual Twitter posting (one tweet)
    python test_local.py --post

    # Test with specific number of papers
    python test_local.py --papers 3

Requirements:
    pip install requests anthropic tweepy
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from fetch_papers import fetch_arxiv_papers, generate_summary, format_summary_html, ARXIV_CATEGORY
from post_twitter import (
    extract_hashtags, 
    format_paper_tweet, 
    create_twitter_client,
    post_tweet,
    get_tweet_limit,
    TWEET_LIMITS
)


def test_fetch_papers(max_papers: int = 3):
    """Test fetching papers from arXiv."""
    print("=" * 60)
    print("📡 TESTING: Fetch papers from arXiv")
    print("=" * 60)
    
    try:
        papers = fetch_arxiv_papers(ARXIV_CATEGORY, max_papers)
        print(f"✅ Successfully fetched {len(papers)} papers\n")
        
        for i, paper in enumerate(papers, 1):
            print(f"Paper {i}:")
            print(f"  ID: {paper['id']}")
            print(f"  Title: {paper['title'][:80]}...")
            print(f"  Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
            print(f"  Categories: {', '.join(paper['categories'])}")
            print()
        
        return papers
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        return None


def test_generate_summaries(papers: list, max_summaries: int = 1):
    """Test AI summary generation."""
    print("=" * 60)
    print("🤖 TESTING: Generate AI summaries")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set. Skipping summary generation.")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return papers
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        for i, paper in enumerate(papers[:max_summaries]):
            print(f"\nGenerating summary for paper {i+1}: {paper['id']}")
            summary = generate_summary(client, paper)
            paper["summary"] = summary
            paper["summary_html"] = format_summary_html(summary)
            
            print(f"✅ Summary generated ({len(summary)} chars)")
            print("-" * 40)
            print(summary[:500] + "..." if len(summary) > 500 else summary)
            print("-" * 40)
        
        return papers
    except Exception as e:
        print(f"❌ Error generating summaries: {e}")
        return papers


def test_hashtag_extraction(papers: list):
    """Test hashtag extraction from papers."""
    print("\n" + "=" * 60)
    print("🏷️  TESTING: Hashtag extraction")
    print("=" * 60)
    
    for i, paper in enumerate(papers, 1):
        hashtags = extract_hashtags(paper)
        print(f"\nPaper {i}: {paper['title'][:60]}...")
        print(f"  Extracted hashtags: {' '.join(hashtags)}")


def test_tweet_formatting(papers: list):
    """Test tweet formatting for different account types."""
    print("\n" + "=" * 60)
    print("📝 TESTING: Tweet formatting")
    print("=" * 60)
    
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    
    for account_type, limit in TWEET_LIMITS.items():
        print(f"\n{'='*40}")
        print(f"Account: {account_type.upper()} ({limit} chars)")
        print("=" * 40)
        
        # Temporarily set environment for testing
        if account_type == "premium":
            os.environ["TWITTER_PREMIUM"] = "true"
        elif account_type == "plus":
            os.environ["TWITTER_PREMIUM"] = "plus"
        else:
            os.environ.pop("TWITTER_PREMIUM", None)
        
        paper = papers[0]
        tweet = format_paper_tweet(paper, page_url)
        
        print(f"Length: {len(tweet)} / {limit} chars")
        print("-" * 40)
        print(tweet)
        print("-" * 40)
        
        if len(tweet) > limit:
            print(f"⚠️  Tweet exceeds limit by {len(tweet) - limit} chars!")
        else:
            print(f"✅ Tweet fits within limit ({limit - len(tweet)} chars remaining)")


def test_twitter_connection():
    """Test Twitter API connection."""
    print("\n" + "=" * 60)
    print("🐦 TESTING: Twitter API connection")
    print("=" * 60)
    
    required_vars = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", 
        "TWITTER_ACCESS_SECRET"
    ]
    
    missing = [v for v in required_vars if not os.environ.get(v)]
    
    if missing:
        print(f"⚠️  Missing Twitter credentials: {', '.join(missing)}")
        print("   Set them with:")
        for v in missing:
            print(f"     export {v}='your-value-here'")
        return None
    
    try:
        client = create_twitter_client()
        if client:
            # Test by getting authenticated user info
            me = client.get_me()
            if me.data:
                print(f"✅ Connected to Twitter as: @{me.data.username}")
                print(f"   Name: {me.data.name}")
                print(f"   ID: {me.data.id}")
                return client
            else:
                print("❌ Could not verify Twitter connection")
                return None
    except Exception as e:
        print(f"❌ Twitter connection error: {e}")
        return None


def test_post_tweet(client, papers: list):
    """Actually post a test tweet (use with caution!)."""
    print("\n" + "=" * 60)
    print("🚀 TESTING: Post actual tweet")
    print("=" * 60)
    
    if not client:
        print("❌ No Twitter client available")
        return
    
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    paper = papers[0]
    tweet = format_paper_tweet(paper, page_url)
    
    print(f"About to post this tweet ({len(tweet)} chars):")
    print("-" * 40)
    print(tweet)
    print("-" * 40)
    
    confirm = input("\n⚠️  Are you sure you want to post this? (yes/no): ")
    
    if confirm.lower() == "yes":
        tweet_id = post_tweet(client, tweet)
        if tweet_id:
            print(f"✅ Tweet posted successfully!")
            print(f"   https://twitter.com/i/status/{tweet_id}")
        else:
            print("❌ Failed to post tweet")
    else:
        print("Cancelled.")


def save_test_data(papers: list):
    """Save test data to papers.json for website testing."""
    print("\n" + "=" * 60)
    print("💾 SAVING: Test data to papers.json")
    print("=" * 60)
    
    from datetime import datetime, timezone
    
    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    output_file = Path(__file__).parent / "data" / "papers.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(papers)} papers to {output_file}")
    print(f"\n📖 To test the website:")
    print(f"   cd {Path(__file__).parent}")
    print(f"   python -m http.server 8000")
    print(f"   Open: http://localhost:8000")


def main():
    parser = argparse.ArgumentParser(description="Test exoplanet paper system locally")
    parser.add_argument("--papers", type=int, default=3, help="Number of papers to fetch (default: 3)")
    parser.add_argument("--summaries", type=int, default=1, help="Number of summaries to generate (default: 1)")
    parser.add_argument("--post", action="store_true", help="Actually post a tweet (requires confirmation)")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching papers (use existing data)")
    args = parser.parse_args()
    
    print("\n🪐 Exoplanet Papers - Local Test Suite\n")
    
    # Step 1: Fetch papers
    if args.skip_fetch:
        print("Skipping paper fetch, loading existing data...")
        data_file = Path(__file__).parent / "data" / "papers.json"
        if data_file.exists():
            with open(data_file) as f:
                papers = json.load(f).get("papers", [])
        else:
            print("No existing data found. Run without --skip-fetch first.")
            return
    else:
        papers = test_fetch_papers(args.papers)
        if not papers:
            return
    
    # Step 2: Generate summaries
    papers = test_generate_summaries(papers, args.summaries)
    
    # Step 3: Test hashtag extraction
    test_hashtag_extraction(papers)
    
    # Step 4: Test tweet formatting
    test_tweet_formatting(papers)
    
    # Step 5: Test Twitter connection
    client = test_twitter_connection()
    
    # Step 6: Optionally post a tweet
    if args.post and client:
        test_post_tweet(client, papers)
    
    # Step 7: Save test data
    save_test_data(papers)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
