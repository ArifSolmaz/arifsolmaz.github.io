#!/usr/bin/env python3
"""
Test script to verify everything works before deploying.
Run this locally to test paper fetching, summary generation, tweet hooks, and thread formatting.

Usage:
    # Test everything (no Twitter posting)
    python test_local.py

    # Test with actual Twitter posting (one tweet thread)
    python test_local.py --post

    # Test with specific number of papers
    python test_local.py --papers 3

Requirements:
    pip install requests anthropic tweepy pillow
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from fetch_papers import (
    fetch_arxiv_papers, 
    generate_summary, 
    generate_tweet_hook,
    format_summary_html, 
    calculate_tweetability_score,
    ARXIV_CATEGORY
)
from post_twitter import (
    extract_hashtags, 
    format_paper_thread, 
    create_twitter_client,
    post_tweet,
    select_best_paper,
    generate_paper_card,
    get_tweet_limit,
    TWEET_LIMITS
)


def test_fetch_papers(max_papers: int = 25):
    """Test fetching papers from arXiv."""
    print("=" * 60)
    print("📡 TESTING: Fetch papers from arXiv (daily batch)")
    print("=" * 60)
    
    try:
        papers = fetch_arxiv_papers(ARXIV_CATEGORY, max_papers)
        
        # Count by type
        exo_count = sum(1 for p in papers if p.get('is_exoplanet_focused', False))
        gen_count = len(papers) - exo_count
        
        print(f"✅ Returning {len(papers)} papers for website/tweeting")
        print(f"   🪐 Exoplanet-focused: {exo_count}")
        print(f"   🔭 General astro-ph.EP: {gen_count}\n")
        
        # Show first 10 of each type
        exo_papers = [p for p in papers if p.get('is_exoplanet_focused', False)]
        gen_papers = [p for p in papers if not p.get('is_exoplanet_focused', False)]
        
        print("Top exoplanet papers (prime time tweets):")
        for i, paper in enumerate(exo_papers[:5], 1):
            print(f"  {i}. 🪐 Score: {paper.get('tweetability_score', 0):+3} | {paper['title'][:50]}...")
        
        print("\nTop general papers (off-peak tweets):")
        for i, paper in enumerate(gen_papers[:5], 1):
            print(f"  {i}. 🔭 Score: {paper.get('tweetability_score', 0):+3} | {paper['title'][:50]}...")
        
        print()
        return papers
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        import traceback
        traceback.print_exc()
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


def test_generate_tweet_hooks(papers: list, max_hooks: int = 1):
    """Test tweet hook generation."""
    print("\n" + "=" * 60)
    print("🎣 TESTING: Generate tweet hooks")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set. Skipping hook generation.")
        return papers
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        for i, paper in enumerate(papers[:max_hooks]):
            print(f"\nGenerating tweet hook for paper {i+1}: {paper['id']}")
            hook_data = generate_tweet_hook(client, paper)
            paper["tweet_hook"] = hook_data
            
            print(f"✅ Tweet hook generated")
            print("-" * 40)
            print(f"HOOK: {hook_data.get('hook', '(empty)')}")
            print(f"CLAIM: {hook_data.get('claim', '(empty)')}")
            print(f"EVIDENCE: {hook_data.get('evidence', '(empty)')}")
            print(f"QUESTION: {hook_data.get('question', '(empty)')}")
            print("-" * 40)
        
        return papers
    except Exception as e:
        print(f"❌ Error generating tweet hooks: {e}")
        return papers


def test_hashtag_extraction(papers: list):
    """Test hashtag extraction from papers."""
    print("\n" + "=" * 60)
    print("🏷️  TESTING: Hashtag extraction (STRICT matching)")
    print("=" * 60)
    
    # Test a few exoplanet papers
    exo_papers = [p for p in papers if p.get('is_exoplanet_focused', False)]
    gen_papers = [p for p in papers if not p.get('is_exoplanet_focused', False)]
    
    print("\n🪐 Exoplanet papers:")
    for paper in exo_papers[:5]:
        hashtags = extract_hashtags(paper)
        print(f"  • {paper['title'][:50]}...")
        print(f"    → {' '.join(hashtags)}")
    
    print("\n🔭 General papers:")
    for paper in gen_papers[:5]:
        hashtags = extract_hashtags(paper)
        print(f"  • {paper['title'][:50]}...")
        print(f"    → {' '.join(hashtags)}")


def test_thread_formatting(papers: list):
    """Test tweet thread formatting for different account types."""
    print("\n" + "=" * 60)
    print("📝 TESTING: Tweet thread formatting")
    print("=" * 60)
    
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    
    for account_type, limit in TWEET_LIMITS.items():
        print(f"\n{'='*50}")
        print(f"Account: {account_type.upper()} ({limit} chars)")
        print("=" * 50)
        
        # Temporarily set environment for testing
        if account_type == "premium":
            os.environ["TWITTER_PREMIUM"] = "true"
        elif account_type == "plus":
            os.environ["TWITTER_PREMIUM"] = "plus"
        else:
            os.environ.pop("TWITTER_PREMIUM", None)
        
        paper = papers[0]
        tweet1, tweet2 = format_paper_thread(paper, page_url)
        
        print(f"\nTweet 1 (hook + image): {len(tweet1)} chars")
        print("-" * 40)
        print(tweet1)
        print("-" * 40)
        
        if len(tweet1) > limit:
            print(f"⚠️  Tweet 1 exceeds limit by {len(tweet1) - limit} chars!")
        else:
            print(f"✅ Tweet 1 fits within limit ({limit - len(tweet1)} chars remaining)")
        
        print(f"\nTweet 2 (links): {len(tweet2)} chars")
        print("-" * 40)
        print(tweet2)
        print("-" * 40)
        
        if len(tweet2) > limit:
            print(f"⚠️  Tweet 2 exceeds limit by {len(tweet2) - limit} chars!")
        else:
            print(f"✅ Tweet 2 fits within limit ({limit - len(tweet2)} chars remaining)")


def test_paper_card_generation(papers: list):
    """Test fallback paper card image generation."""
    print("\n" + "=" * 60)
    print("🖼️  TESTING: Paper card image generation")
    print("=" * 60)
    
    try:
        from PIL import Image
        print("✅ PIL available")
        
        paper = papers[0]
        card_path = generate_paper_card(paper)
        
        if card_path:
            print(f"✅ Paper card generated: {card_path}")
            # Get file size
            import os
            size = os.path.getsize(card_path)
            print(f"   File size: {size/1024:.1f} KB")
        else:
            print("❌ Paper card generation failed")
            
    except ImportError:
        print("⚠️  PIL not installed. Install with: pip install pillow")


def test_tweetability_scoring(papers: list):
    """Test tweetability scoring and paper selection."""
    print("\n" + "=" * 60)
    print("📊 TESTING: Tweetability scoring & time-based selection")
    print("=" * 60)
    
    # Separate by type (default to False since we now use stricter matching)
    exoplanet_papers = [p for p in papers if p.get('is_exoplanet_focused', False)]
    other_papers = [p for p in papers if not p.get('is_exoplanet_focused', False)]
    
    print(f"\nPaper breakdown:")
    print(f"  🪐 Exoplanet-focused: {len(exoplanet_papers)}")
    print(f"  🔭 General astro-ph.EP: {len(other_papers)}")
    
    # Show top 5 of each type
    print("\nTop exoplanet papers (for prime time):")
    for i, p in enumerate(sorted(exoplanet_papers, key=lambda x: -x.get('tweetability_score', 0))[:5], 1):
        print(f"  {i}. 🪐 Score: {p.get('tweetability_score', 0):+3d} | {p['title'][:50]}...")
    
    print("\nTop general papers (for off-peak):")
    for i, p in enumerate(sorted(other_papers, key=lambda x: -x.get('tweetability_score', 0))[:5], 1):
        print(f"  {i}. 🔭 Score: {p.get('tweetability_score', 0):+3d} | {p['title'][:50]}...")
    
    # Test time-based selection
    from datetime import datetime, timezone
    now_utc = datetime.now(timezone.utc)
    
    # Import the function
    from post_twitter import is_prime_time_pst, select_best_paper
    
    prime_time = is_prime_time_pst()
    print(f"\nCurrent time: {now_utc.strftime('%H:%M')} UTC")
    print(f"Prime time PST: {'YES 🌟' if prime_time else 'NO 📋'}")
    
    if prime_time:
        print("🌟 PRIME TIME - Would tweet exoplanet papers")
    else:
        print("📋 OFF-PEAK - Would tweet general papers")
    
    # Simulate selection
    selected = select_best_paper(papers, set())
    if selected:
        is_exo = "🪐 EXOPLANET" if selected.get('is_exoplanet_focused', False) else "🔭 GENERAL"
        print(f"Would tweet: {is_exo} - {selected['id']}")


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
        client, api_v1 = create_twitter_client()
        if client:
            # Test by getting authenticated user info
            me = client.get_me()
            if me.data:
                print(f"✅ Connected to Twitter as: @{me.data.username}")
                print(f"   Name: {me.data.name}")
                print(f"   ID: {me.data.id}")
                return client, api_v1
            else:
                print("❌ Could not verify Twitter connection")
                return None
    except Exception as e:
        print(f"❌ Twitter connection error: {e}")
        return None


def test_post_thread(client, api_v1, papers: list):
    """Actually post a test thread (use with caution!)."""
    print("\n" + "=" * 60)
    print("🚀 TESTING: Post actual tweet thread")
    print("=" * 60)
    
    if not client:
        print("❌ No Twitter client available")
        return
    
    page_url = os.environ.get("PAGE_URL", "https://arifsolmaz.github.io/arxiv")
    paper = papers[0]
    tweet1, tweet2 = format_paper_thread(paper, page_url)
    
    print(f"About to post this thread:\n")
    print("Tweet 1:")
    print("-" * 40)
    print(tweet1)
    print("-" * 40)
    print("\nTweet 2 (reply):")
    print("-" * 40)
    print(tweet2)
    print("-" * 40)
    
    confirm = input("\n⚠️  Are you sure you want to post this? (yes/no): ")
    
    if confirm.lower() == "yes":
        # Post tweet 1
        tweet1_id = post_tweet(client, tweet1)
        if tweet1_id:
            print(f"✅ Tweet 1 posted: https://twitter.com/i/status/{tweet1_id}")
            
            # Post tweet 2 as reply
            tweet2_id = post_tweet(client, tweet2, reply_to=tweet1_id)
            if tweet2_id:
                print(f"✅ Tweet 2 posted: https://twitter.com/i/status/{tweet2_id}")
            else:
                print("❌ Failed to post tweet 2")
        else:
            print("❌ Failed to post tweet 1")
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
    parser.add_argument("--papers", type=int, default=25, help="Max papers to fetch (default: 25)")
    parser.add_argument("--summaries", type=int, default=1, help="Number of summaries to generate (default: 1)")
    parser.add_argument("--hooks", type=int, default=1, help="Number of tweet hooks to generate (default: 1)")
    parser.add_argument("--post", action="store_true", help="Actually post a tweet thread (requires confirmation)")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching papers (use existing data)")
    args = parser.parse_args()
    
    print("\n🪐 Exoplanet Papers - Local Test Suite (IMPROVED)\n")
    
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
    
    # Step 3: Generate tweet hooks
    papers = test_generate_tweet_hooks(papers, args.hooks)
    
    # Step 4: Test tweetability scoring
    test_tweetability_scoring(papers)
    
    # Step 5: Test hashtag extraction
    test_hashtag_extraction(papers)
    
    # Step 6: Test thread formatting
    test_thread_formatting(papers)
    
    # Step 7: Test paper card generation
    test_paper_card_generation(papers)
    
    # Step 8: Test Twitter connection
    twitter_result = test_twitter_connection()
    
    # Step 9: Optionally post a thread
    if args.post and twitter_result:
        client, api_v1 = twitter_result
        test_post_thread(client, api_v1, papers)
    
    # Step 10: Save test data
    save_test_data(papers)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n📋 Summary of improvements:")
    print("   • Tweet hooks: Hook → Claim → Evidence → Question format")
    print("   • Hashtags: Fixed lowercase matching, limited to 2-4 tags")
    print("   • Threading: Tweet 1 (content + image), Tweet 2 (links)")
    print("   • Selection: Papers ranked by tweetability score")
    print("   • Images: Fallback paper card when no figure available")
    print("   • Website: Share button added to paper modals")


if __name__ == "__main__":
    main()
