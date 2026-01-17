#!/usr/bin/env python3
"""
Regenerate missing summaries for papers in papers.json.
Run this to fix papers that are missing their AI-generated summaries.

Usage:
    export ANTHROPIC_API_KEY='your-key'
    python regenerate_summaries.py
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic


PAPERS_FILE = Path(__file__).parent / "data" / "papers.json"


def generate_summary(client: anthropic.Anthropic, paper: dict) -> str:
    """Generate an accessible summary for a paper using Claude."""
    
    prompt = f"""You are a science communicator writing for a general audience. Summarize this exoplanet research paper in an accessible, engaging way.

PAPER TITLE: {paper['title']}

ABSTRACT: {paper['abstract']}

Write an extended summary (250-350 words) with these exact section headers:

**Why It Matters**
Open with the big picture significance—why should a general reader care about this research? Connect it to broader questions about planets, the search for life, or understanding our place in the universe.

**What They Did**
Explain the research methods in simple terms. Avoid jargon entirely, or if you must use a technical term, explain it immediately. Use analogies to everyday concepts when helpful.

**Key Findings**
Describe the main discoveries. What did they actually find? Use concrete numbers or comparisons when possible to make the findings tangible.

**Looking Forward**
End with implications—what does this mean for exoplanet science? What questions does it open up? How might this lead to future discoveries?

Guidelines:
- Write for someone curious about space but with no astronomy background
- Use analogies (e.g., "about the size of Neptune" or "orbiting closer than Mercury does to our Sun")
- Avoid acronyms unless you spell them out
- Be engaging and convey the excitement of discovery
- Keep paragraphs short and readable"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"  ❌ Error generating summary: {e}")
        return ""


def generate_tweet_hook(client: anthropic.Anthropic, paper: dict) -> dict:
    """Generate tweet-optimized hook for a paper."""
    
    prompt = f"""You are a science communicator crafting a tweet about an exoplanet research paper. Your goal is to maximize engagement (replies and retweets).

PAPER TITLE: {paper['title']}

ABSTRACT: {paper['abstract']}

Generate tweet content in this EXACT format (each field on its own line):

HOOK: [A concrete, attention-grabbing statement. No jargon. Max 120 chars. Start with the most interesting finding or implication, not "Astronomers discovered..." or "New research shows..."]

CLAIM: [What's new or changed because of this research. Max 100 chars. Be specific.]

EVIDENCE: [One specific detail from the paper: a number, comparison, or concrete finding. If no headline number in abstract, say "Method: [brief method description]". Max 100 chars.]

QUESTION: [A thought-provoking question designed to get replies. Ask something experts and enthusiasts would want to answer. Max 80 chars.]

Guidelines:
- NO analogies like "imagine trying to..." or "think of it like..."
- NO generic openings like "Astronomers have discovered..." or "A new study..."
- Lead with the MOST INTERESTING thing, not context
- Use technical terms that the astronomy Twitter community knows (JWST, RV, transit, etc.)
- The question should invite genuine discussion, not rhetorical"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        hook_data = {"hook": "", "claim": "", "evidence": "", "question": ""}
        
        for line in text.strip().split("\n"):
            line = line.strip()
            if line.startswith("HOOK:"):
                hook_data["hook"] = line[5:].strip()
            elif line.startswith("CLAIM:"):
                hook_data["claim"] = line[6:].strip()
            elif line.startswith("EVIDENCE:"):
                hook_data["evidence"] = line[9:].strip()
            elif line.startswith("QUESTION:"):
                hook_data["question"] = line[9:].strip()
        
        return hook_data
        
    except Exception as e:
        print(f"  ❌ Error generating tweet hook: {e}")
        return {"hook": "", "claim": "", "evidence": "", "question": ""}


def format_summary_html(summary: str) -> str:
    """Convert markdown-style summary to HTML."""
    if not summary:
        return "<p><em>Summary unavailable.</em></p>"
    
    html = re.sub(
        r'\*\*(Why It Matters|What They Did|Key Findings|Looking Forward)\*\*',
        r'<h4>\1</h4>',
        summary
    )
    
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


def main():
    print("🔄 Regenerating missing paper summaries\n")
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("   Run: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Load papers
    if not PAPERS_FILE.exists():
        print(f"❌ Papers file not found: {PAPERS_FILE}")
        return
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    papers = data.get("papers", [])
    print(f"📄 Loaded {len(papers)} papers\n")
    
    # Find papers missing summaries
    missing = []
    for paper in papers:
        has_summary = paper.get("summary_html") and paper["summary_html"] != "<p><em>Summary unavailable.</em></p>"
        has_hook = paper.get("tweet_hook") and paper["tweet_hook"].get("hook")
        
        if not has_summary or not has_hook:
            missing.append(paper)
    
    if not missing:
        print("✅ All papers already have summaries!")
        return
    
    print(f"🔍 Found {len(missing)} papers missing summaries:\n")
    for i, p in enumerate(missing, 1):
        print(f"   {i}. {p['id']}: {p['title'][:60]}...")
    
    print(f"\n🤖 Generating summaries...\n")
    
    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Generate missing content
    for i, paper in enumerate(missing, 1):
        print(f"[{i}/{len(missing)}] {paper['id']}")
        
        # Generate summary
        if not paper.get("summary_html") or paper["summary_html"] == "<p><em>Summary unavailable.</em></p>":
            print(f"  📝 Generating summary...")
            summary = generate_summary(client, paper)
            if summary:
                paper["summary"] = summary
                paper["summary_html"] = format_summary_html(summary)
                print(f"  ✅ Summary generated ({len(summary)} chars)")
            else:
                print(f"  ⚠️ Summary generation failed")
            time.sleep(0.5)
        
        # Generate tweet hook
        if not paper.get("tweet_hook") or not paper["tweet_hook"].get("hook"):
            print(f"  🎣 Generating tweet hook...")
            hook = generate_tweet_hook(client, paper)
            if hook.get("hook"):
                paper["tweet_hook"] = hook
                print(f"  ✅ Tweet hook generated")
            else:
                print(f"  ⚠️ Tweet hook generation failed")
            time.sleep(0.5)
        
        # Rate limiting
        if i < len(missing):
            time.sleep(1)
        
        print()
    
    # Update timestamp and save
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved updated papers to {PAPERS_FILE}")
    
    # Summary
    still_missing = sum(1 for p in papers if not p.get("summary_html") or p["summary_html"] == "<p><em>Summary unavailable.</em></p>")
    print(f"\n✨ Done! {len(missing) - still_missing}/{len(missing)} summaries generated successfully.")
    
    if still_missing:
        print(f"⚠️ {still_missing} papers still missing summaries (API errors)")


if __name__ == "__main__":
    main()
