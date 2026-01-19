#!/usr/bin/env python3
"""
Split existing papers.json into daily archive files based on arXiv ID dates.

arXiv ID format: YYMM.NNNNN
- 2601.11469 = January 2026, paper #11469
- Papers announced on same day have similar sequential numbers

This script groups papers by their announcement date and creates
separate archive files for each day.
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
ARCHIVE_DIR = DATA_DIR / "archive"
ARCHIVE_INDEX = ARCHIVE_DIR / "index.json"


def is_exoplanet_focused(title: str, abstract: str) -> bool:
    """Check if paper is specifically about exoplanets."""
    text = f"{title} {abstract}".lower()
    
    strict_keywords = [
        # Core exoplanet terms
        "exoplanet", "exoplanets", "exoplanetary",
        "extrasolar planet", "extrasolar planets",
        
        # Planet types
        "hot jupiter", "warm jupiter", "cold jupiter",
        "super-earth", "super earth", "mini-neptune", "sub-neptune",
        "earth-like planet", "earth-sized planet",
        "rocky planet", "terrestrial planet",
        "gas giant planet", "ice giant planet",
        
        # Habitability
        "habitable zone", "habitable exoplanet", "habitability",
        "biosignature", "biosignatures",
        
        # Detection methods
        "microlensing planet", "microlensing bound planet",
        "transiting planet", "transiting exoplanet",
        "radial velocity planet",
        "directly imaged planet",
        
        # Surveys & missions with planet context
        "tess planet", "tess candidate", "toi-",
        "kepler planet", "kepler candidate", "kepler-",
        "k2 planet", "k2-",
        
        # Known systems
        "wasp-", "hat-p-", "hatp-",
        "trappist-1", "trappist",
        "proxima centauri b", "proxima b",
        "gj 1214", "gj 436", "hd 189733", "hd 209458",
        "55 cancri", "tau ceti",
        
        # Atmospheres
        "exoplanet atmosphere", "exoplanetary atmosphere",
        "planetary atmosphere",
        "transmission spectrum", "transmission spectroscopy",
        "emission spectrum of",
        
        # Specific contexts
        "planet occurrence", "planet frequency",
        "planet host star", "planet-hosting star",
        "spin-orbit", "orbital obliquity",
        "planet detection", "planet discovery",
        "bound planet",  # for microlensing
    ]
    
    # Check for strict keywords
    if any(keyword in text for keyword in strict_keywords):
        return True
    
    # Additional check: "planet" + specific context words
    if "planet" in text:
        planet_contexts = [
            "detected", "discovered", "confirmed", "candidate",
            "orbiting", "orbit", "transit", "radial velocity",
            "mass", "radius", "density", "atmosphere",
            "formation", "migration", "evolution",
        ]
        if any(ctx in text for ctx in planet_contexts):
            # But exclude solar system contexts
            solar_system = ["mars", "venus", "mercury", "saturn", "neptune", "uranus", "pluto", "asteroid", "comet", "interstellar"]
            if not any(ss in text for ss in solar_system):
                return True
    
    return False


# arXiv announcement schedule (Mon-Fri, no weekends)
# Papers submitted by 14:00 ET are announced at 20:00 ET same day
# The date in the ID reflects when it was submitted, not announced

# Known paper ID ranges for January 2026
# Based on actual arXiv listings:
# - Jan 19: 2601.10794 to 2601.11469 (7 papers)
# - Jan 16: 2601.09835 to 2601.10666 (11 papers)


def get_paper_date(paper_id: str) -> str:
    """Determine the announcement date from arXiv ID."""
    try:
        # Extract number part: 2601.11469v1 -> 11469
        id_part = paper_id.split("v")[0]  # Remove version
        yymm, num = id_part.split(".")
        num = int(num)
        
        # For January 2026 (2601.xxxxx)
        if yymm == "2601":
            # Based on actual arXiv listings
            if num >= 10794:  # Jan 19 range
                return "2026-01-19"
            elif num >= 9835:  # Jan 16 range  
                return "2026-01-16"
            elif num >= 8883:  # Jan 15 range (estimate)
                return "2026-01-15"
            elif num >= 7900:  # Jan 14 range (estimate)
                return "2026-01-14"
            elif num >= 6900:  # Jan 13 range (estimate)
                return "2026-01-13"
            else:
                return "2026-01-10"  # Older papers
        
        # For December 2025 (2512.xxxxx)
        if yymm == "2512":
            return "2025-12-20"  # Group all Dec papers together
        
        return "unknown"
        
    except Exception as e:
        print(f"Error parsing {paper_id}: {e}")
        return "unknown"


def main():
    print("=" * 60)
    print("Split papers.json into daily archives")
    print("=" * 60)
    
    # Load papers from ALL sources (papers.json + existing archives)
    all_papers = {}
    
    # Load from papers.json
    if PAPERS_FILE.exists():
        with open(PAPERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for p in data.get("papers", []):
            all_papers[p["id"]] = p
        print(f"Loaded {len(data.get('papers', []))} papers from papers.json")
    
    # Load from existing archive files
    if ARCHIVE_DIR.exists():
        for archive_file in sorted(ARCHIVE_DIR.glob("*.json")):
            if archive_file.name == "index.json":
                continue
            try:
                with open(archive_file, "r", encoding="utf-8") as f:
                    archive_data = json.load(f)
                for p in archive_data.get("papers", []):
                    if p["id"] not in all_papers:
                        all_papers[p["id"]] = p
                print(f"Loaded {len(archive_data.get('papers', []))} papers from {archive_file.name}")
            except Exception as e:
                print(f"Error loading {archive_file}: {e}")
    
    papers = list(all_papers.values())
    print(f"\nTotal unique papers: {len(papers)}")
    
    # Re-classify papers with improved detection
    print("\nRe-classifying papers...")
    for paper in papers:
        old_status = paper.get("is_exoplanet_focused", False)
        new_status = is_exoplanet_focused(paper["title"], paper.get("abstract", ""))
        paper["is_exoplanet_focused"] = new_status
        if old_status != new_status:
            status_str = "🪐 NOW EXOPLANET" if new_status else "📄 now general"
            print(f"  {paper['id']}: {status_str}")
    
    # Group papers by date
    papers_by_date = defaultdict(list)
    
    for paper in papers:
        date = get_paper_date(paper["id"])
        papers_by_date[date].append(paper)
        print(f"  {paper['id']} -> {date}")
    
    print(f"\nGrouped into {len(papers_by_date)} dates:")
    for date, date_papers in sorted(papers_by_date.items(), reverse=True):
        exo_count = sum(1 for p in date_papers if p.get("is_exoplanet_focused", False))
        print(f"  {date}: {len(date_papers)} papers ({exo_count} exoplanet)")
    
    # Create archive directory
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save each date as separate archive file
    all_dates = []
    
    for date, date_papers in sorted(papers_by_date.items(), reverse=True):
        if date == "unknown":
            print(f"\nSkipping {len(date_papers)} papers with unknown date")
            continue
        
        # Sort papers within the date
        date_papers.sort(
            key=lambda p: (not p.get("is_exoplanet_focused", False), -p.get("tweetability_score", 0)),
            reverse=False
        )
        
        archive_data = {
            "date": date,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "category": "astro-ph.EP",
            "paper_count": len(date_papers),
            "papers": date_papers
        }
        
        archive_file = ARCHIVE_DIR / f"{date}.json"
        with open(archive_file, "w", encoding="utf-8") as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {archive_file.name} ({len(date_papers)} papers)")
        all_dates.append(date)
    
    # Update archive index
    index = {
        "dates": sorted(all_dates, reverse=True),
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    
    with open(ARCHIVE_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated index.json with {len(all_dates)} dates")
    
    # Also update main papers.json with only the most recent date
    if all_dates:
        latest_date = sorted(all_dates, reverse=True)[0]
        latest_papers = papers_by_date[latest_date]
        
        latest_data = {
            "date": latest_date,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "category": "astro-ph.EP",
            "paper_count": len(latest_papers),
            "papers": latest_papers
        }
        
        with open(PAPERS_FILE, "w", encoding="utf-8") as f:
            json.dump(latest_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated papers.json with {latest_date} ({len(latest_papers)} papers)")


if __name__ == "__main__":
    main()
