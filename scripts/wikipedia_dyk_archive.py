#!/usr/bin/env python3
"""Scrape Wikipedia 'Did you know' archives - curated facts."""

import json
import re
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")

# DYK archives by month - each has hundreds of facts
DYK_ARCHIVES = [
    "Wikipedia:Recent_additions/2024/January",
    "Wikipedia:Recent_additions/2024/February", 
    "Wikipedia:Recent_additions/2024/March",
    "Wikipedia:Recent_additions/2024/April",
    "Wikipedia:Recent_additions/2024/May",
    "Wikipedia:Recent_additions/2024/June",
    "Wikipedia:Recent_additions/2024/July",
    "Wikipedia:Recent_additions/2024/August",
    "Wikipedia:Recent_additions/2024/September",
    "Wikipedia:Recent_additions/2024/October",
    "Wikipedia:Recent_additions/2024/November",
    "Wikipedia:Recent_additions/2024/December",
    "Wikipedia:Recent_additions/2023/January",
    "Wikipedia:Recent_additions/2023/February",
    "Wikipedia:Recent_additions/2023/March",
    "Wikipedia:Recent_additions/2023/April",
    "Wikipedia:Recent_additions/2023/May",
    "Wikipedia:Recent_additions/2023/June",
    "Wikipedia:Recent_additions/2023/July",
    "Wikipedia:Recent_additions/2023/August",
    "Wikipedia:Recent_additions/2023/September",
    "Wikipedia:Recent_additions/2023/October",
    "Wikipedia:Recent_additions/2023/November",
    "Wikipedia:Recent_additions/2023/December",
]

# Also scrape the main DYK page and its subpages
EXTRA_PAGES = [
    "Wikipedia:Did_you_know",
    "Portal:Science/Did_you_know",
    "Portal:Biology/Did_you_know",
    "Portal:Physics/Did_you_know",
    "Portal:Chemistry/Did_you_know",
    "Portal:Mathematics/Did_you_know",
    "Portal:Astronomy/Did_you_know",
    "Portal:Earth_sciences/Did_you_know",
    "Portal:Medicine/Did_you_know",
    "Portal:Technology/Did_you_know",
]

def fetch_page_html(title):
    """Fetch Wikipedia page HTML."""
    encoded_title = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/wiki/{encoded_title}"
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  Error fetching {title}: {e}")
    return None

def extract_dyk_facts(html, source):
    """Extract 'Did you know that...' facts from HTML."""
    facts = []
    
    if not html:
        return facts
    
    # Pattern for DYK items - they start with "... that"
    patterns = [
        r'\.\.\.\s*that\s+([^<\n]{30,300}\?)',  # Classic DYK format
        r'<li>[^<]*\.\.\.\s*that\s+([^<]{30,300}\?)',  # In list items
        r'>\.\.\.that\s+([^<]{30,300}\?)',  # Various formats
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Clean up HTML
            fact = re.sub(r'<[^>]+>', '', match)
            fact = re.sub(r'\s+', ' ', fact).strip()
            
            # Add "Did you know that" prefix for context
            if fact and len(fact) > 30:
                full_fact = f"Did you know that {fact}"
                if not full_fact.endswith('?'):
                    full_fact += '?'
                facts.append(full_fact)
    
    # Also try to extract general interesting facts from content
    # Look for sentences starting with interesting keywords
    sentences = re.findall(r'([A-Z][^.!?<]{40,250}[.!?])', html)
    
    for sentence in sentences:
        sentence = re.sub(r'<[^>]+>', '', sentence).strip()
        
        if any(word in sentence.lower() for word in [
            'discovered', 'first', 'only', 'largest', 'smallest',
            'oldest', 'newest', 'unique', 'rare', 'million', 'billion'
        ]) and len(sentence) > 50:
            facts.append(sentence)
    
    return list(set(facts))[:150]  # Dedupe and limit

import urllib.parse

def main():
    all_facts = []
    
    print("Fetching DYK archives...")
    
    for page in DYK_ARCHIVES + EXTRA_PAGES:
        print(f"  {page}...")
        html = fetch_page_html(page)
        
        if html:
            facts = extract_dyk_facts(html, page)
            for fact in facts:
                all_facts.append({
                    'text': fact,
                    'source': f'Wikipedia DYK',
                    'source_url': f'https://en.wikipedia.org/wiki/{urllib.parse.quote(page)}',
                    'category': 'did_you_know'
                })
            print(f"    Found {len(facts)} facts")
        
        time.sleep(0.5)
    
    # Deduplicate
    seen = set()
    unique_facts = []
    for fact in all_facts:
        key = fact['text'].lower()[:100]
        if key not in seen:
            seen.add(key)
            unique_facts.append(fact)
    
    output_file = OUTPUT_DIR / "wikipedia_dyk_archive.json"
    with open(output_file, 'w') as f:
        json.dump(unique_facts, f, indent=2)
    
    print(f"\nTotal unique: {len(unique_facts)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
