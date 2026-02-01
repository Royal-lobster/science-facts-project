#!/usr/bin/env python3
"""Sort facts by category, then by similarity within each category (fast version)."""

import json
import re
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("/root/clawd/projects/science-facts/quality_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/organized_facts.json")

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())

def get_keywords(text):
    """Extract key terms for sorting."""
    words = normalize(text).split()
    # Filter out common words
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                 'has', 'have', 'had', 'do', 'does', 'did', 'will', 'would',
                 'can', 'could', 'may', 'might', 'must', 'shall', 'should',
                 'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from',
                 'that', 'this', 'it', 'and', 'or', 'but', 'if', 'as', 'than'}
    return [w for w in words if w not in stopwords and len(w) > 2][:5]

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Total facts: {len(facts)}")
    
    # Group by category
    print("Grouping by category...")
    by_category = defaultdict(list)
    for fact in facts:
        cat = fact.get('category', 'general')
        by_category[cat].append(fact)
    
    print(f"Categories: {len(by_category)}")
    
    # Sort within each category by first keyword (simple clustering)
    print("Sorting within categories...")
    organized = []
    
    for cat in sorted(by_category.keys()):
        cat_facts = by_category[cat]
        # Sort by first few keywords to group similar topics
        cat_facts.sort(key=lambda f: tuple(get_keywords(f['text'])))
        
        # Add category marker for first fact
        if cat_facts:
            cat_facts[0]['_category_start'] = True
        
        organized.extend(cat_facts)
        print(f"  {cat}: {len(cat_facts)} facts")
    
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(organized, f, indent=2)
    
    print(f"\n=== Results ===")
    print(f"Total organized facts: {len(organized)}")
    print(f"Categories: {len(by_category)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
