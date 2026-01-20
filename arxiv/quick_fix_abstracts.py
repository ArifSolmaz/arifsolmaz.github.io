#!/usr/bin/env python3
"""
Quick fix script to clean arXiv metadata prefix from existing abstracts.
Run this once in your repo root to fix papers.json and archive files.

Usage: python quick_fix_abstracts.py
"""

import json
import re
from pathlib import Path

def clean_abstract(abstract: str) -> str:
    """Remove arXiv metadata prefix from abstract."""
    if not abstract:
        return ""
    
    # Pattern: arXiv:2510.09841v2 Announce Type: replace Abstract: ...
    pattern = r'^arXiv:\d+\.\d+(?:v\d+)?\s+Announce Type:\s*(?:new|replace|cross)\s+Abstract:\s*'
    cleaned = re.sub(pattern, '', abstract, flags=re.IGNORECASE)
    cleaned = re.sub(r'^Abstract:\s*', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def fix_papers_file(filepath: Path) -> int:
    """Fix abstracts in a papers JSON file. Returns count of fixed papers."""
    if not filepath.exists():
        return 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"  ⚠ Could not read {filepath}")
        return 0
    
    fixed_count = 0
    papers = data.get('papers', [])
    
    for paper in papers:
        old_abstract = paper.get('abstract', '')
        new_abstract = clean_abstract(old_abstract)
        
        if old_abstract != new_abstract:
            paper['abstract'] = new_abstract
            fixed_count += 1
    
    if fixed_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Fixed {fixed_count} abstracts in {filepath.name}")
    else:
        print(f"  - No fixes needed in {filepath.name}")
    
    return fixed_count


def main():
    print("=== Abstract Cleanup Script ===\n")
    
    # Find data directory
    data_dir = Path('arxiv/data')
    if not data_dir.exists():
        data_dir = Path('data')
    if not data_dir.exists():
        print("✗ Could not find data directory (arxiv/data or data)")
        return
    
    total_fixed = 0
    
    # Fix main papers.json
    print("Checking papers.json...")
    total_fixed += fix_papers_file(data_dir / 'papers.json')
    
    # Fix archive files
    archive_dir = data_dir / 'archive'
    if archive_dir.exists():
        print("\nChecking archive files...")
        for archive_file in sorted(archive_dir.glob('*.json')):
            if archive_file.name != 'index.json':
                total_fixed += fix_papers_file(archive_file)
    
    print(f"\n=== Done! Fixed {total_fixed} total abstracts ===")


if __name__ == '__main__':
    main()
