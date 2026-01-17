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
import urllib.request
import urllib.error

import anthropic


def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch the first figure from arXiv HTML version of the paper."""
    try:
        # arXiv HTML URL
        html_url = f"https://arxiv.org/html/{paper_id}"
        
        req = urllib.request.Request(html_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Look for figure images in the HTML
        # Pattern 1: <img src="..." in figure elements
        patterns = [
            r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']',
            r'<img[^>]+class=["\'][^"\']*ltx_graphics[^"\']*["\'][^>]+src=["\']([^"\']+)["\']',
            r'/html/[^"\']+/[^"\']+\.(png|jpg|jpeg|gif)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            if matches:
                img_path = matches[0] if isinstance(matches[0], str) else matches[0][0]
                # Convert relative path to absolute URL
                if img_path.startswith('/'):
                    return f"https://arxiv.org{img_path}"
                elif img_path.startswith('http'):
                    return img_path
                else:
                    return f"https://arxiv.org/html/{paper_id}/{img_path}"
        
        return None
    except Exception as e:
        print(f"  Could not fetch arXiv figure: {e}")
        return None

# Configuration
PAPERS_FILE = Path(__file__).parent.parent / "data" / "papers.json"
NEWS_FILE = Path(__file__).parent.parent / "data" / "arxiv_news.json"
EXISTING_NEWS_FILE = Path(__file__).parent.parent / "data" / "existing_news.json"
MAX_NEWS_ITEMS = 100  # Keep last 100 news items to avoid file bloat
MAX_PAPERS_PER_DAY = 50  # Process all exoplanet papers (typically 10-25 per day)

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

**ÖNEMLİ TERİM KURALLARI:**
- "exoplanet" = "ötegezegen" (TEK KELİME, "öte gezegen" DEĞİL!)
- "astronomy" = "astronomi"
- "habitable" = "yaşanabilir"
- "atmosphere" = "atmosfer"
- Etiketlerde SADECE Türkçe kullan, İngilizce kelime KULLANMA

**Çıktı formatı (sadece JSON):**
{{
  "title": "Türkçe haber başlığı",
  "text": "Tam haber metni (markdown formatında)",
  "tags": ["ötegezegen", "astronomi", "diğer-türkçe-etiketler"]
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
    """Get figure URL for paper - try arXiv first, then topic-based fallback."""
    
    # 1. Check if paper already has a figure URL
    if paper.get("figure_url"):
        return paper["figure_url"]
    
    # 2. Try to fetch actual figure from arXiv HTML
    print(f"  Trying to fetch figure from arXiv...")
    arxiv_figure = fetch_arxiv_figure(paper["id"])
    if arxiv_figure:
        print(f"  ✓ Found arXiv figure: {arxiv_figure[:60]}...")
        return arxiv_figure
    
    # 3. Fallback: Select topic-based image based on paper content
    title_lower = paper.get("title", "").lower()
    abstract_lower = paper.get("abstract", "").lower()
    content = title_lower + " " + abstract_lower
    
    # Topic-based image selection
    if any(word in content for word in ["jwst", "james webb", "webb telescope"]):
        return "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80"
    elif any(word in content for word in ["mars", "martian"]):
        return "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800&q=80"
    elif any(word in content for word in ["jupiter", "jovian", "gas giant"]):
        return "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800&q=80"
    elif any(word in content for word in ["saturn", "ring", "titan"]):
        return "https://images.unsplash.com/photo-1614724723656-457ac62c2c98?w=800&q=80"
    elif any(word in content for word in ["venus", "venusian"]):
        return "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800&q=80"
    elif any(word in content for word in ["sun", "solar", "stellar", "star"]):
        return "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=800&q=80"
    elif any(word in content for word in ["earth", "habitable", "rocky", "terrestrial"]):
        return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80"
    elif any(word in content for word in ["atmosphere", "spectrum", "spectroscopy"]):
        return "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=800&q=80"
    elif any(word in content for word in ["transit", "kepler", "tess"]):
        return "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&q=80"
    elif any(word in content for word in ["binary", "orbit", "system"]):
        return "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800&q=80"
    elif any(word in content for word in ["disk", "protoplanet", "formation"]):
        return "https://images.unsplash.com/photo-1537420327992-d6e192287183?w=800&q=80"
    elif any(word in content for word in ["water", "ocean", "ice"]):
        return "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800&q=80"
    
    # Generic space images as final fallback (varied by hash)
    generic_fallbacks = [
        "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800&q=80",
        "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=800&q=80",
        "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800&q=80",
        "https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?w=800&q=80",
        "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&q=80",
        "https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=800&q=80",
        "https://images.unsplash.com/photo-1520034475321-cbe63696469a?w=800&q=80",
        "https://images.unsplash.com/photo-1505506874110-6a7a69069a08?w=800&q=80",
    ]
    
    idx = hash(paper['id'] + paper['title']) % len(generic_fallbacks)
    return generic_fallbacks[idx]


def fix_turkish_errors(text: str) -> str:
    """Fix common Turkish spelling and grammar errors in generated text."""
    
    # Dictionary of common errors and their corrections
    corrections = {
        # Specific errors found
        "zuyereya": "süreye",
        "Zuyereya": "Süreye",
        "ötegezegenların": "ötegezegenlerin",
        "Ötegezegenların": "Ötegezegenlerin",
        "ötegezegenlar": "ötegezegenler",
        "Ötegezegenlar": "Ötegezegenler",
        "ötegezegenlarda": "ötegezegenlerde",
        "ötegezegenlara": "ötegezegenlere",
        
        # Common Turkish grammar fixes for "ötegezegen"
        "ötegezegen'in": "ötegezegenin",
        "ötegezegen'ler": "ötegezegenler",
        "ötegezegen'e": "ötegezegene",
        "ötegezegen'den": "ötegezegenden",
        
        # Spacing issues
        "öte gezegen": "ötegezegen",
        "Öte Gezegen": "Ötegezegen",
        "Öte gezegen": "Ötegezegen",
        "öte-gezegen": "ötegezegen",
        
        # Common typos in astronomy terms
        "atmospher": "atmosfer",
        "spectroscopi": "spektroskopi",
        "teleskob": "teleskop",
        "yörünğe": "yörünge",
        "güneş sistemi dışı gezegen": "ötegezegen",
        
        # Grammar suffix errors
        "gezegenlerin'in": "gezegenlerin",
        "yıldızların'ın": "yıldızların",
        "sistemlerin'in": "sistemlerin",
        
        # Capitalization for acronyms
        "jwst": "JWST",
        "Jwst": "JWST",
        " nasa ": " NASA ",
        " tess ": " TESS ",
        " esa ": " ESA ",
        " vlt ": " VLT ",
        " alma ": " ALMA ",
        
        # Punctuation spacing
        " ,": ",",
        " .": ".",
        " ;": ";",
        " :": ":",
        "  ": " ",
        
        # Common word errors
        "keşfettiler": "keşfetti",  # Plural verb with singular subject
        "açıkladılar": "açıkladı",
        "buldular": "buldu",
    }
    
    result = text
    for wrong, correct in corrections.items():
        result = result.replace(wrong, correct)
    
    # Clean up multiple spaces
    while "  " in result:
        result = result.replace("  ", " ")
    
    return result


def create_news_item(paper: dict, turkish_data: dict, date: str) -> dict:
    """Create a news item in the required format."""
    
    # Generate unique ID
    paper_id_clean = paper["id"].replace(".", "-").replace("/", "-")
    news_id = f"news-{date}-{paper_id_clean}"
    
    # Get tags and fix Turkish translations
    tags = turkish_data.get("tags", [])
    
    # Fix common keyword issues
    fixed_tags = []
    for tag in tags:
        tag = tag.strip()
        # Skip empty tags
        if not tag:
            continue
        # Fix Turkish translations (case-insensitive)
        tag_lower = tag.lower()
        if tag_lower in ["öte gezegen", "öte-gezegen", "exoplanet", "exoplanets"]:
            tag = "ötegezegen"
        elif tag_lower in ["astronomy", "astronomi̇"]:
            tag = "astronomi"
        elif tag_lower == "uzay araştırması":
            tag = "uzay-araştırması"
        elif tag_lower == "uzay keşfi":
            tag = "uzay-keşfi"
        elif tag_lower == "gezegen keşfi":
            tag = "gezegen-keşfi"
        # Remove English words that slipped through
        elif tag_lower in ["space", "planet", "research", "discovery", "telescope"]:
            continue
        
        if tag and tag not in fixed_tags:
            fixed_tags.append(tag)
    
    # Add base tags if not present
    base_tags = ["arXiv", "astronomi", "ötegezegen"]
    for bt in base_tags:
        if bt.lower() not in [t.lower() for t in fixed_tags]:
            fixed_tags.insert(0, bt)
    
    all_tags = fixed_tags[:8]  # Max 8 tags
    
    # Apply Turkish error corrections to title and text
    corrected_title = fix_turkish_errors(turkish_data["title"])
    corrected_text = fix_turkish_errors(turkish_data["text"])
    
    return {
        "id": news_id,
        "arxiv_id": paper["id"],
        "date": date,
        "title": corrected_title,
        "image": get_paper_figure_url(paper),
        "tags": ",".join(all_tags),
        "audioMp3": "",
        "audioM4a": "",
        "text": corrected_text + f"\n\n**Kaynak**: [arXiv:{paper['id']}]({paper['abs_link']})",
        "abs_link": paper.get("abs_link", f"https://arxiv.org/abs/{paper['id']}"),
        "pdf_link": paper.get("pdf_link", f"https://arxiv.org/pdf/{paper['id']}.pdf")
    }


def select_papers_for_news(papers: list[dict], processed_ids: set[str]) -> list[dict]:
    """Select papers to convert to news (only exoplanet-focused, prioritize by tweetability score)."""
    
    # Filter out already processed AND non-exoplanet papers
    unprocessed = [
        p for p in papers 
        if p["id"] not in processed_ids and p.get("is_exoplanet_focused", False)
    ]
    
    if not unprocessed:
        print("All exoplanet papers already processed (or no exoplanet papers found)")
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
