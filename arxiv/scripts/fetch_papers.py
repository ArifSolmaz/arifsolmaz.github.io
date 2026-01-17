#!/usr/bin/env python3
"""
Fetch exoplanet papers from arXiv and generate accessible AI summaries.
This script is run on weekdays by GitHub Actions.

Note: arXiv publication schedule:
- Papers submitted Mon-Thu by 14:00 ET are announced the next day
- Papers submitted Fri-Sun are announced on Monday
- No announcements on weekends

NEW: Also generates tweet-optimized hooks for better Twitter engagement.
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import requests
from xml.etree import ElementTree as ET


# Configuration
ARXIV_CATEGORY = "astro-ph.EP"
MAX_PAPERS = 15
FETCH_MULTIPLIER = 4  # Fetch more to filter down to MAX_PAPERS
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "papers.json"

# Keywords to identify exoplanet-related papers
# Papers must contain at least one of these in title or abstract
EXOPLANET_KEYWORDS = [
    # Core terms
    "exoplanet", "exoplanets", "exoplanetary",
    "extrasolar planet", "extrasolar planets",
    
    # Planet types
    "hot jupiter", "hot jupiters",
    "warm jupiter", "warm jupiters",
    "cold jupiter", "cold jupiters",
    "super-earth", "super earth", "super-earths",
    "sub-neptune", "sub neptune", "sub-neptunes", "mini-neptune",
    "earth-like planet", "earth-sized planet", "earth analog",
    "terrestrial planet", "terrestrial exoplanet",
    "gas giant planet",
    "ice giant planet",
    "rocky planet", "rocky exoplanet",
    "lava world", "lava planet",
    "ocean world", "water world",
    "rogue planet", "free-floating planet",
    
    # Detection methods
    "transit method", "transiting planet", "transiting exoplanet",
    "transit detection", "transit survey",
    "radial velocity planet", "rv detection",
    "doppler detection",
    "microlensing planet",
    "direct imaging planet", "directly imaged planet",
    "transit timing variation", "ttv",
    
    # Atmosphere studies
    "exoplanet atmosphere", "planetary atmosphere",
    "atmospheric characterization",
    "transmission spectrum", "transmission spectroscopy",
    "emission spectrum", "emission spectroscopy",
    "thermal emission",
    "atmospheric escape", "atmospheric evaporation",
    "exoplanet spectroscopy",
    
    # Habitability
    "habitable zone", "habitable exoplanet", "habitable planet",
    "habitability",
    "biosignature", "biosignatures",
    "potentially habitable",
    
    # Specific missions/instruments for exoplanets
    "tess planet", "tess candidate",
    "kepler planet", "kepler candidate",
    "k2 planet",
    "jwst exoplanet", "jwst planet",
    "cheops",
    "plato mission",
    "ariel mission",
    "harps planet",
    "espresso planet",
    
    # Planetary systems
    "planetary system", "planet system",
    "multi-planet system", "multiplanet",
    "planet host star", "planet-hosting",
    "star-planet interaction",
    "planet occurrence", "planet frequency",
    
    # Formation & evolution (exoplanet context)
    "planet formation",
    "planet migration",
    "protoplanetary disk",  # Often about forming exoplanets
    "debris disk",
    "planet-disk interaction",
    "core accretion",
    "gravitational instability planet",
    
    # Notable systems
    "trappist-1", "trappist 1",
    "proxima centauri b", "proxima b",
    "55 cancri",
    "gj 1214",
    "gj 436",
    "hd 189733",
    "hd 209458",
    "wasp-39", "wasp-76", "wasp-121", "wasp-18", "wasp-12",
    "toi-700",
    "lhs 1140",
    "k2-18",
    "kepler-186", "kepler-452", "kepler-22",
    "hr 8799",
    "beta pictoris",
    "51 pegasi",
    "tau ceti",
    "gliese 581", "gliese 667",
    "l 98-59",
    "toi-175", "toi-270",
    "hat-p", "hatp",
    "kelt-", 
    "tres-",
    "corot-",
    "ogle-",
    "xo-",
]

# Keywords to EXCLUDE (solar system focused, not exoplanets)
EXCLUDE_KEYWORDS = [
    "mars rover", "mars mission", "martian surface",
    "lunar surface", "moon landing", "apollo",
    "jupiter mission", "juno mission",
    "saturn ring", "cassini",
    "venus atmosphere", "venus mission",
    "mercury messenger",
    "new horizons",
    "asteroid mining", "asteroid deflection",
    "near-earth asteroid", "near earth asteroid",
    "meteorite",
    "comet tail", "cometary activity",
    "kuiper belt object",
    "trans-neptunian",
    "dwarf planet ceres", "dwarf planet pluto",
]

# Tweetability scoring keywords (for picking most engaging paper)
TWEETABILITY_KEYWORDS = {
    # High engagement topics (+3)
    "jwst": 3, "james webb": 3,
    "habitable": 3, "habitability": 3,
    "biosignature": 3, "biosignatures": 3,
    "earth-like": 3, "earthlike": 3, "earth-sized": 3,
    "water world": 3, "ocean world": 3,
    "life": 3,
    "trappist": 3, "proxima": 3,
    
    # Discovery/novelty language (+2)
    "first": 2, "discovery": 2, "discovered": 2,
    "detection": 2, "detected": 2, "detect": 2,
    "new": 2, "novel": 2,
    "confirmed": 2, "confirmation": 2,
    "breakthrough": 2,
    
    # Popular instruments (+1)
    "tess": 1, "kepler": 1, "gaia": 1, "hubble": 1,
    "alma": 1, "vlt": 1,
    
    # Technical/instrumentation (-2)
    "calibration": -2, "pipeline": -2, "systematic": -2,
    "correction": -2, "reduction": -2,
}


def is_exoplanet_paper(title: str, abstract: str) -> bool:
    """Check if a paper is related to exoplanet science."""
    text = f"{title} {abstract}".lower()
    
    # Check for exclusion keywords first
    for keyword in EXCLUDE_KEYWORDS:
        if keyword.lower() in text:
            # But still include if it also has strong exoplanet keywords
            has_exoplanet_keyword = any(
                kw.lower() in text for kw in ["exoplanet", "exoplanetary", "extrasolar"]
            )
            if not has_exoplanet_keyword:
                return False
    
    # Check for exoplanet keywords
    for keyword in EXOPLANET_KEYWORDS:
        if keyword.lower() in text:
            return True
    
    return False


def calculate_tweetability_score(paper: dict) -> int:
    """Calculate how 'tweetable' a paper is based on keywords."""
    text = f"{paper['title']} {paper['abstract']}".lower()
    score = 0
    
    for keyword, points in TWEETABILITY_KEYWORDS.items():
        if keyword.lower() in text:
            score += points
    
    return score


def fetch_arxiv_papers(category: str, max_results: int = 15) -> list[dict]:
    """Fetch recent papers from arXiv API and filter for exoplanet content."""
    
    # Fetch more papers than needed to ensure enough after filtering
    fetch_count = max_results * FETCH_MULTIPLIER
    
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": fetch_count,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    
    # Parse XML
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    
    all_papers = []
    for entry in root.findall("atom:entry", ns):
        # Extract ID
        arxiv_id = entry.find("atom:id", ns).text
        paper_id = arxiv_id.split("/abs/")[-1]
        
        # Extract title (clean whitespace)
        title = entry.find("atom:title", ns).text
        title = " ".join(title.split())
        
        # Extract abstract
        abstract = entry.find("atom:summary", ns).text
        abstract = " ".join(abstract.split())
        
        # Extract authors
        authors = [
            author.find("atom:name", ns).text 
            for author in entry.findall("atom:author", ns)
        ]
        
        # Extract categories
        categories = [
            cat.get("term") 
            for cat in entry.findall("atom:category", ns)
        ]
        
        # Extract dates
        published = entry.find("atom:published", ns).text
        updated = entry.find("atom:updated", ns).text
        
        # Build links
        pdf_link = f"https://arxiv.org/pdf/{paper_id}.pdf"
        abs_link = f"https://arxiv.org/abs/{paper_id}"
        
        all_papers.append({
            "id": paper_id,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "categories": categories,
            "published": published,
            "updated": updated,
            "pdf_link": pdf_link,
            "abs_link": abs_link
        })
    
    # Filter for exoplanet papers only
    exoplanet_papers = [
        p for p in all_papers 
        if is_exoplanet_paper(p["title"], p["abstract"])
    ]
    
    # Calculate tweetability score for each paper
    for paper in exoplanet_papers:
        paper["tweetability_score"] = calculate_tweetability_score(paper)
    
    print(f"Fetched {len(all_papers)} total papers, {len(exoplanet_papers)} are exoplanet-related")
    
    # Return up to max_results
    return exoplanet_papers[:max_results]


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
        print(f"Error generating summary for {paper['id']}: {e}")
        return ""


def generate_tweet_hook(client: anthropic.Anthropic, paper: dict) -> dict:
    """Generate tweet-optimized hook, evidence, and question for a paper."""
    
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
- The question should invite genuine discussion, not rhetorical

Example good output:
HOOK: Water vapor detected in a sub-Neptune atmosphere just 22 light-years away
CLAIM: First atmospheric characterization of a potentially habitable-zone world around an M dwarf
EVIDENCE: JWST NIRSpec found H2O absorption at 3σ confidence in GJ 1214b's transmission spectrum
QUESTION: What biosignatures should we prioritize searching for in sub-Neptune atmospheres?"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        
        # Parse the response
        hook_data = {
            "hook": "",
            "claim": "",
            "evidence": "",
            "question": ""
        }
        
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
        print(f"Error generating tweet hook for {paper['id']}: {e}")
        return {
            "hook": "",
            "claim": "",
            "evidence": "",
            "question": ""
        }


def format_summary_html(summary: str) -> str:
    """Convert markdown-style summary to HTML."""
    if not summary:
        return "<p><em>Summary unavailable.</em></p>"
    
    # Convert **Header** to <h4>Header</h4>
    html = re.sub(
        r'\*\*(Why It Matters|What They Did|Key Findings|Looking Forward)\*\*',
        r'<h4>\1</h4>',
        summary
    )
    
    # Split into paragraphs
    paragraphs = html.split('\n\n')
    formatted = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h4>'):
            formatted.append(p)
        else:
            # Handle single newlines within paragraphs
            p = p.replace('\n', ' ')
            formatted.append(f'<p>{p}</p>')
    
    return '\n'.join(formatted)


def main():
    """Main function to fetch papers and generate summaries."""
    
    print(f"Fetching papers from arXiv {ARXIV_CATEGORY}...")
    papers = fetch_arxiv_papers(ARXIV_CATEGORY, MAX_PAPERS)
    print(f"Found {len(papers)} papers")
    
    if len(papers) == 0:
        print("No papers found. Exiting.")
        return
    
    # Check if we already have these papers (to avoid regenerating summaries)
    existing_ids = set()
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_ids = {p["id"] for p in existing_data.get("papers", [])}
                existing_papers = {p["id"]: p for p in existing_data.get("papers", [])}
        except (json.JSONDecodeError, KeyError):
            existing_papers = {}
    else:
        existing_papers = {}
    
    new_paper_ids = {p["id"] for p in papers}
    
    # Check if paper list is identical
    if new_paper_ids == existing_ids:
        print("No new papers since last update. Skipping summary generation.")
        # Still update the timestamp
        existing_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        return
    
    # Initialize Anthropic client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Summaries will be empty.")
        client = None
    else:
        client = anthropic.Anthropic(api_key=api_key)
    
    # Generate summaries and tweet hooks (reuse existing ones when possible)
    for i, paper in enumerate(papers):
        # Check if we already have content for this paper
        if paper["id"] in existing_papers:
            existing = existing_papers[paper["id"]]
            if existing.get("summary_html"):
                print(f"Reusing existing summary for {paper['id']}")
                paper["summary"] = existing["summary"]
                paper["summary_html"] = existing["summary_html"]
                # Also reuse tweet hook if exists
                if existing.get("tweet_hook"):
                    paper["tweet_hook"] = existing["tweet_hook"]
                # Preserve tweetability score if already calculated
                if existing.get("tweetability_score") is not None:
                    paper["tweetability_score"] = existing["tweetability_score"]
                continue
        
        print(f"Generating content {i+1}/{len(papers)}: {paper['id']}")
        
        if client:
            # Generate long-form summary
            summary = generate_summary(client, paper)
            paper["summary"] = summary
            paper["summary_html"] = format_summary_html(summary)
            
            # Generate tweet-optimized hook
            time.sleep(0.5)  # Brief pause between API calls
            tweet_hook = generate_tweet_hook(client, paper)
            paper["tweet_hook"] = tweet_hook
            
            # Rate limiting - be nice to the API
            if i < len(papers) - 1:
                time.sleep(1)
        else:
            paper["summary"] = ""
            paper["summary_html"] = "<p><em>Summary unavailable.</em></p>"
            paper["tweet_hook"] = {
                "hook": "",
                "claim": "",
                "evidence": "",
                "question": ""
            }
    
    # Prepare output data
    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "category": ARXIV_CATEGORY,
        "paper_count": len(papers),
        "papers": papers
    }
    
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(papers)} papers to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
