#!/usr/bin/env python3
"""Scrape dedicated fact/trivia sites for interesting facts."""

import json
import re
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/generated")
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  Error: {e}")
        return None

def extract_facts(html):
    """Extract fact-like sentences from HTML."""
    if not html:
        return []
    
    # Remove scripts/styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract text
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    facts = []
    for s in sentences:
        s = s.strip()
        if len(s) < 50 or len(s) > 350:
            continue
        
        # Must start with capital
        if not s[0].isupper():
            continue
            
        # Filter for interesting content
        interesting = any(w in s.lower() for w in [
            'discovered', 'scientists', 'research', 'found', 'study',
            'first', 'only', 'largest', 'smallest', 'fastest', 'oldest',
            'million', 'billion', 'percent', 'years', 'ancient',
            'can', 'able', 'capable', 'unique', 'rare', 'surprising',
            'actually', 'despite', 'although', 'however', 'unlike'
        ])
        
        if interesting and s[0].isupper():
            facts.append(s)
    
    return facts

# Sites to scrape
URLS = [
    ("https://www.mentalfloss.com/amazingfactgenerator", "mental_floss"),
    ("https://www.sciencefocus.com/science/amazing-science-facts", "science_focus"),
    ("https://www.livescience.com/strange-news", "live_science"),
    ("https://www.iflscience.com/", "ifl_science"),
    ("https://www.smithsonianmag.com/science-nature/", "smithsonian"),
    ("https://www.nationalgeographic.com/science", "nat_geo"),
    ("https://www.newscientist.com/", "new_scientist"),
    ("https://www.popsci.com/science/", "pop_sci"),
    ("https://www.discovermagazine.com/", "discover"),
    ("https://www.sciencealert.com/", "science_alert"),
    ("https://www.atlasobscura.com/categories/science", "atlas_obscura"),
    ("https://interestingengineering.com/science", "interesting_engineering"),
    ("https://www.sciencenews.org/", "science_news"),
    ("https://www.wired.com/category/science/", "wired"),
]

def main():
    all_facts = []
    
    for url, source in URLS:
        print(f"Scraping: {source}")
        html = fetch(url)
        
        if html:
            facts = extract_facts(html)
            for f in facts:
                all_facts.append({
                    'text': f,
                    'source': source,
                    'category': 'science_general'
                })
            print(f"  Found {len(facts)} facts")
        
        time.sleep(1)
    
    # Dedupe
    seen = set()
    unique = []
    for f in all_facts:
        key = f['text'].lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(f)
    
    output_file = OUTPUT_DIR / "scraped_sites.json"
    with open(output_file, 'w') as f:
        json.dump(unique, f, indent=2)
    
    print(f"\nTotal unique: {len(unique)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
