#!/usr/bin/env python3
"""
Test script to debug arXiv figure fetching.
Run this to see what images are found.
"""

import re
import requests

def fetch_arxiv_figure(paper_id: str) -> str | None:
    """Try to fetch figure from arXiv HTML with improved patterns."""
    
    # Try the new arXiv HTML beta
    urls_to_try = [
        f"https://arxiv.org/html/{paper_id}",
        f"https://ar5iv.labs.arxiv.org/html/{paper_id}",
    ]
    
    for url in urls_to_try:
        print(f"Trying: {url}")
        try:
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                print(f"  Status: {response.status_code}")
                continue
            
            html = response.text
            print(f"  Got HTML: {len(html)} bytes")
            
            # Multiple patterns to try (ordered by specificity)
            patterns = [
                # arXiv HTML beta - figures with ltx_figure class
                r'<figure[^>]*class="[^"]*ltx_figure[^"]*"[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']',
                
                # Standard figure with img inside
                r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg))["\']',
                
                # Images with ltx_graphics class (common in arXiv)
                r'<img[^>]+class=["\'][^"\']*ltx_graphics[^"\']*["\'][^>]+src=["\']([^"\']+)["\']',
                
                # Any img with src containing the paper ID pattern
                r'<img[^>]+src=["\']([^"\']*(?:x\d+|figure|fig)[^"\']*\.(?:png|jpg|jpeg|gif|svg))["\']',
                
                # Generic figure images
                r'<img[^>]+src=["\']([^"\']+/[^"\']+\.(?:png|jpg|jpeg|gif))["\']',
            ]
            
            for i, pattern in enumerate(patterns):
                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                if matches:
                    print(f"  Pattern {i+1} found {len(matches)} matches:")
                    for j, match in enumerate(matches[:5]):
                        img_path = match if isinstance(match, str) else match[0]
                        print(f"    {j+1}. {img_path[:80]}...")
                    
                    # Get the first valid match
                    img_path = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    
                    # Skip small icons, logos, etc.
                    skip_patterns = ['icon', 'logo', 'arrow', 'button', 'nav', 'menu', '1x1', 'pixel']
                    if any(skip in img_path.lower() for skip in skip_patterns):
                        print(f"    Skipping (looks like icon): {img_path}")
                        continue
                    
                    # Convert to absolute URL
                    if img_path.startswith('//'):
                        img_url = f"https:{img_path}"
                    elif img_path.startswith('/'):
                        base = url.split('/html/')[0]
                        img_url = f"{base}{img_path}"
                    elif img_path.startswith('http'):
                        img_url = img_path
                    else:
                        # Relative path - need to include paper ID folder
                        # url = https://arxiv.org/html/2601.08883v1
                        # img_path = Fig1_Lifesrequirements.png
                        # result = https://arxiv.org/html/2601.08883v1/Fig1_Lifesrequirements.png
                        img_url = f"{url}/{img_path}"
                    
                    print(f"  ✓ Found figure: {img_url}")
                    return img_url
            
            print(f"  No figures found with any pattern")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    return None


def main():
    # Test with the paper that failed
    paper_id = "2601.08883v1"
    print(f"Testing figure fetch for: {paper_id}\n")
    
    result = fetch_arxiv_figure(paper_id)
    
    if result:
        print(f"\n✅ SUCCESS: {result}")
    else:
        print(f"\n❌ FAILED: No figure found")


if __name__ == "__main__":
    main()
