#!/usr/bin/env python3
"""Scrape science fact sites directly."""

import json
import re
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")

SITES = [
    # Science Daily headlines
    ("https://www.sciencedaily.com/news/", "science_news", "Science Daily"),
    # Live Science
    ("https://www.livescience.com/animals", "animals", "Live Science"),
    ("https://www.livescience.com/space", "space", "Live Science"),
    ("https://www.livescience.com/planet-earth", "earth_science", "Live Science"),
    # Space.com
    ("https://www.space.com/science-astronomy", "astronomy", "Space.com"),
    # Nature facts pages
    ("https://www.nationalgeographic.com/animals", "animals", "National Geographic"),
]

def fetch_url(url):
    """Fetch URL content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  Error: {e}")
        return None

def extract_facts_from_html(html, source_name):
    """Extract interesting fact sentences from HTML."""
    facts = []
    
    if not html:
        return facts
    
    # Remove scripts and styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract text content
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Filter criteria
        if len(sentence) < 50 or len(sentence) > 350:
            continue
        
        # Must have good alpha ratio
        alpha = sum(c.isalpha() for c in sentence) / max(len(sentence), 1)
        if alpha < 0.65:
            continue
        
        # Look for fact-like content
        fact_words = [
            'discovered', 'scientists', 'research', 'study', 'found',
            'species', 'million', 'billion', 'years', 'first', 'largest',
            'smallest', 'fastest', 'ancient', 'new', 'rare', 'unique',
            'planet', 'star', 'galaxy', 'ocean', 'animal', 'plant',
            'brain', 'cell', 'dna', 'fossil', 'climate', 'temperature'
        ]
        
        if any(word in sentence.lower() for word in fact_words):
            # Must start with capital letter
            if sentence[0].isupper():
                facts.append(sentence)
    
    return list(set(facts))[:80]

def main():
    all_facts = []
    
    for url, category, source_name in SITES:
        print(f"Fetching: {url}")
        html = fetch_url(url)
        
        if html:
            facts = extract_facts_from_html(html, source_name)
            for fact in facts:
                all_facts.append({
                    'text': fact,
                    'source': source_name,
                    'source_url': url,
                    'category': category
                })
            print(f"  Got {len(facts)} facts")
        
        time.sleep(2)
    
    output_file = OUTPUT_DIR / "science_sites.json"
    with open(output_file, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"\nTotal: {len(all_facts)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
