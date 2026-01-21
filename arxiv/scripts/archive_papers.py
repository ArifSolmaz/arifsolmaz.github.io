#!/usr/bin/env python3
"""
Archive today's papers to the archive folder.
Run after fetch_papers.py to maintain paper history.

Creates:
- data/archive/YYYY-MM-DD.json (copy of today's papers)
- data/archive/index.json (list of available dates)

FIX: Now uses announcement_date (actual arXiv date) instead of updated_at (processing time)
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
ARCHIVE_DIR = DATA_DIR / "archive"
INDEX_FILE = ARCHIVE_DIR / "index.json"

# Keep archives for this many days (to limit storage)
MAX_ARCHIVE_DAYS = 90


def archive_papers():
    """Archive today's papers and update index."""
    
    if not PAPERS_FILE.exists():
        print("No papers.json found")
        return
    
    # Load current papers
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    papers = data.get("papers", [])
    if not papers:
        print("No papers to archive")
        return
    
    # FIX: Use announcement_date (actual arXiv date) instead of updated_at (processing time)
    # This ensures archive files match arXiv's actual announcement schedule
    date_str = data.get("announcement_date")
    
    # Fallback to updated_at for backwards compatibility with old data
    if not date_str:
        updated_at = data.get("updated_at", "")
        if updated_at:
            try:
                date_str = updated_at[:10]  # YYYY-MM-DD
            except:
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        else:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    print(f"📅 Archiving papers for announcement date: {date_str}")
    
    # Create archive directory
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy papers to archive
    archive_file = ARCHIVE_DIR / f"{date_str}.json"
    shutil.copy(PAPERS_FILE, archive_file)
    print(f"Archived {len(papers)} papers to {archive_file}")
    
    # Update index
    update_index()
    
    # Cleanup old archives
    cleanup_old_archives()


def update_index():
    """Update the archive index with all available dates."""
    
    # Find all archive files
    archive_files = sorted(ARCHIVE_DIR.glob("????-??-??.json"), reverse=True)
    
    dates = []
    for f in archive_files:
        date_str = f.stem  # filename without extension
        
        # Validate it's a date
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            dates.append(date_str)
        except ValueError:
            continue
    
    # Create index
    index = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "dates": dates,
        "count": len(dates)
    }
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    print(f"Updated archive index with {len(dates)} dates")


def cleanup_old_archives():
    """Remove archives older than MAX_ARCHIVE_DAYS."""
    
    archive_files = sorted(ARCHIVE_DIR.glob("????-??-??.json"))
    
    if len(archive_files) <= MAX_ARCHIVE_DAYS:
        return
    
    # Remove oldest files
    files_to_remove = archive_files[:-MAX_ARCHIVE_DAYS]
    
    for f in files_to_remove:
        if f.name != "index.json":
            f.unlink()
            print(f"Removed old archive: {f.name}")


if __name__ == "__main__":
    archive_papers()
