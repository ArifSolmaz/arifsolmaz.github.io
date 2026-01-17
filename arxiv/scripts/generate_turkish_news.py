#!/usr/bin/env python3
"""
Convert arXiv papers with AI summaries to Turkish press-release style news articles.
Reads from papers.json, generates Turkish news, and saves to news.json.

This script runs daily after fetch_papers.py and uses the Claude API to generate
engaging Turkish science news articles from the English paper summaries.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import anthropic

# Configuration
PAPERS_FILE = Path(__file__).parent.parent / "data" / "papers.json"
NEWS_FILE = Path(__file__).parent.parent / "data" / "arxiv_news.json"
EXISTING_NEWS_FILE = Path(__file__).parent.parent / "data" / "existing_news.json"
MAX_NEWS_ITEMS = 50  # Keep last 50 news items to avoid file bloat
MAX_PAPERS_PER_DAY = 5  # Maximum papers to convert to news per day

# Turkish news generation prompt
TURKISH_NEWS_PROMPT = """Sen bir bilim gazetecisisin. Aşağıdaki akademik makale özetini, Türkçe basın bülteni tarzında popüler bilim haberi olarak yeniden yaz.

**Kaynak Makale:**
Başlık: {title}
Özet: {summary}

**Kurallar:**
1. Haber başlığı çekici ve dikkat çekici olmalı (gazete manşeti gibi)
2. İlk paragraf en önemli bulguyu vurgulamalı (piramit yazı tekniği)
3. Teknik terimleri açıkla veya Türkçe karşılıklarını kullan
4. 300-500 kelime arası olmalı
5. Markdown formatı kullan (**kalın**, *italik*)
6. Son paragrafta "neden önemli" vurgusu yap
7. Emoji KULLANMA
8. Bilimsel doğruluğu koru
9. Heyecan verici ama abartısız bir dil kullan

**Çıktı formatı (sadece JSON):**
{{
  "title": "Türkçe haber başlığı",
  "text": "Tam haber metni (markdown formatında)",
  "tags": ["etiket1", "etiket2", "etiket3"]
}}

Sadece JSON döndür, başka bir şey ekleme."""


def load_papers() -> list[dict]:
    """Load papers from papers.json."""
    if not PAPERS_FILE.exists():
        print(f"Papers file not found: {PAPERS_FILE}")
        return []
    
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data.get("papers", [])


def load_existing_news() -> list[dict]:
    """Load existing news items."""
    if not NEWS_FILE.exists():
        return []
    
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_processed_ids(news_items: list[dict]) -> set[str]:
    """Get set of paper IDs already processed into news."""
    processed = set()
    for item in news_items:
        # Extract paper ID from news ID (format: news-YYYY-MM-DD-paperid)
        if item.get("arxiv_id"):
            processed.add(item["arxiv_id"])
    return processed


def generate_turkish_news(paper: dict, client: anthropic.Anthropic) -> dict | None:
    """Generate Turkish news article from paper using Claude API."""
    
    # Get the summary (prefer extended summary if available)
    summary = paper.get("summary", paper.get("abstract", ""))
    if not summary:
        print(f"No summary for paper {paper['id']}")
        return None
    
    prompt = TURKISH_NEWS_PROMPT.format(
        title=paper["title"],
        summary=summary
    )
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text.strip()
        
        # Parse JSON from response
        # Handle potential markdown code blocks
        if content.startswith("```"):
            content = re.sub(r"^```json?\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        
        result = json.loads(content)
        return result
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for {paper['id']}: {e}")
        print(f"Response was: {content[:500]}...")
        return None
    except Exception as e:
        print(f"Error generating news for {paper['id']}: {e}")
        return None


def get_paper_figure_url(paper: dict) -> str:
    """Get figure URL for paper, or fallback to a default astronomy image."""
    # Check if paper has a figure URL
    if paper.get("figure_url"):
        return paper["figure_url"]
    
    # Try to construct arXiv HTML figure URL
    paper_id = paper["id"]
    html_base = f"https://arxiv.org/html/{paper_id}"
    
    # Fallback: use a relevant astronomy/exoplanet image
    fallbacks = [
        "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=600&q=80",  # Galaxy
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80",  # Space
        "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=600&q=80",  # Stars
        "https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=600&q=80",  # Night sky
    ]
    
    # Use paper ID hash to consistently pick same fallback for same paper
    idx = hash(paper_id) % len(fallbacks)
    return fallbacks[idx]


def create_news_item(paper: dict, turkish_data: dict, date: str) -> dict:
    """Create a news item in the required format."""
    
    # Generate unique ID
    paper_id_clean = paper["id"].replace(".", "-").replace("/", "-")
    news_id = f"news-{date}-{paper_id_clean}"
    
    # Get tags and add base astronomy tags
    tags = turkish_data.get("tags", [])
    base_tags = ["arXiv", "astronomi", "öte gezegen"]
    all_tags = list(set(base_tags + tags))[:8]  # Max 8 tags
    
    return {
        "id": news_id,
        "arxiv_id": paper["id"],
        "date": date,
        "title": turkish_data["title"],
        "image": get_paper_figure_url(paper),
        "tags": ",".join(all_tags),
        "audioMp3": "",  # Can be added later
        "audioM4a": "",
        "text": turkish_data["text"] + f"\n\n**Kaynak**: [arXiv:{paper['id']}]({paper['abs_link']})",
        "abs_link": paper.get("abs_link", f"https://arxiv.org/abs/{paper['id']}"),
        "pdf_link": paper.get("pdf_link", f"https://arxiv.org/pdf/{paper['id']}.pdf")
    }


def select_papers_for_news(papers: list[dict], processed_ids: set[str]) -> list[dict]:
    """Select papers to convert to news (prioritize by tweetability score)."""
    
    # Filter out already processed
    unprocessed = [p for p in papers if p["id"] not in processed_ids]
    
    if not unprocessed:
        print("All papers already processed")
        return []
    
    # Sort by tweetability score (higher = more interesting)
    unprocessed.sort(key=lambda p: p.get("tweetability_score", 0), reverse=True)
    
    # Take top papers
    return unprocessed[:MAX_PAPERS_PER_DAY]


def main():
    print("=" * 60)
    print("arXiv Papers → Turkish News Generator")
    print("=" * 60)
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return
    
    # Load papers
    papers = load_papers()
    if not papers:
        print("No papers to process")
        return
    
    print(f"Loaded {len(papers)} papers from papers.json")
    
    # Load existing news
    existing_news = load_existing_news()
    processed_ids = get_processed_ids(existing_news)
    print(f"Found {len(existing_news)} existing news items")
    print(f"Already processed {len(processed_ids)} paper IDs")
    
    # Select papers to convert
    selected = select_papers_for_news(papers, processed_ids)
    if not selected:
        print("No new papers to convert")
        return
    
    print(f"Selected {len(selected)} papers for Turkish news generation")
    
    # Initialize Claude client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Generate news for each paper
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_items = []
    
    for i, paper in enumerate(selected):
        print(f"\n[{i+1}/{len(selected)}] Processing: {paper['title'][:60]}...")
        
        turkish_data = generate_turkish_news(paper, client)
        if turkish_data:
            news_item = create_news_item(paper, turkish_data, today)
            new_items.append(news_item)
            print(f"  ✓ Generated: {turkish_data['title'][:50]}...")
        else:
            print(f"  ✗ Failed to generate news")
    
    if not new_items:
        print("\nNo new news items generated")
        return
    
    # Merge with existing news (new items first)
    all_news = new_items + existing_news
    
    # Trim to max items
    all_news = all_news[:MAX_NEWS_ITEMS]
    
    # Ensure output directory exists
    NEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save updated news
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"Generated {len(new_items)} new Turkish news articles")
    print(f"Total news items: {len(all_news)}")
    print(f"Saved to: {NEWS_FILE}")


if __name__ == "__main__":
    main()
