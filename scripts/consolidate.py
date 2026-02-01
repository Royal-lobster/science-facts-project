#!/usr/bin/env python3
"""Consolidate all facts and remove duplicates."""

import json
import os
import hashlib
from pathlib import Path

FACTS_DIR = Path("/root/clawd/projects/science-facts/facts_raw")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/consolidated_facts.json")

def normalize_text(text):
    """Normalize text for comparison."""
    return ' '.join(text.lower().split())

def text_hash(text):
    """Create hash of normalized text."""
    return hashlib.md5(normalize_text(text).encode()).hexdigest()

def extract_facts(data, source_file):
    """Extract facts from various JSON structures."""
    facts = []
    
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get('facts', data.get('data', data.get('results', [])))
        if not isinstance(items, list):
            items = [data]
    else:
        return facts
    
    for item in items:
        if isinstance(item, str):
            facts.append({
                'text': item,
                'source_file': source_file,
                'category': source_file.replace('.json', '')
            })
        elif isinstance(item, dict):
            # Try various field names for the fact text
            text = item.get('text') or item.get('fact') or item.get('content') or item.get('description') or item.get('title')
            if text and len(text) > 20:  # Skip very short entries
                facts.append({
                    'text': text,
                    'source_file': source_file,
                    'source_url': item.get('source_url') or item.get('url') or item.get('source'),
                    'category': item.get('category') or item.get('topic') or source_file.replace('.json', '')
                })
    
    return facts

def main():
    all_facts = []
    seen_hashes = set()
    duplicates = 0
    
    # Process all JSON files
    for json_file in sorted(FACTS_DIR.glob("*.json")):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            facts = extract_facts(data, json_file.name)
            
            for fact in facts:
                h = text_hash(fact['text'])
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    all_facts.append(fact)
                else:
                    duplicates += 1
            
            print(f"{json_file.name}: {len(facts)} facts extracted")
            
        except Exception as e:
            print(f"{json_file.name}: ERROR - {e}")
    
    # Save consolidated facts
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Total unique facts: {len(all_facts)}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Saved to: {OUTPUT_FILE}")
    
    # Category breakdown
    categories = {}
    for fact in all_facts:
        cat = fact.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nCategory breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    main()
