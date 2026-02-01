#!/usr/bin/env python3
"""Deduplicate, sort by category, and cluster by similarity within categories."""

import json
import re
import hashlib
from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path("/root/clawd/projects/science-facts/quality_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/organized_facts.json")

def normalize(text):
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_words(text):
    """Get word set for similarity."""
    return set(normalize(text).split())

def word_similarity(text1, text2):
    """Jaccard similarity of words."""
    words1 = get_words(text1)
    words2 = get_words(text2)
    if not words1 or not words2:
        return 0.0
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union > 0 else 0.0

def get_ngrams(text, n=3):
    """Get character n-grams."""
    text = normalize(text)
    return set(text[i:i+n] for i in range(len(text) - n + 1))

def ngram_similarity(text1, text2):
    """Jaccard similarity of n-grams."""
    ng1 = get_ngrams(text1)
    ng2 = get_ngrams(text2)
    if not ng1 or not ng2:
        return 0.0
    intersection = len(ng1 & ng2)
    union = len(ng1 | ng2)
    return intersection / union if union > 0 else 0.0

def deduplicate(facts, threshold=0.75):
    """Remove near-duplicates."""
    unique = []
    seen_hashes = set()
    
    # Sort by length (keep longer versions)
    facts = sorted(facts, key=lambda f: -len(f['text']))
    
    for fact in facts:
        text = fact['text']
        text_hash = hashlib.md5(normalize(text).encode()).hexdigest()
        
        # Exact duplicate check
        if text_hash in seen_hashes:
            continue
        
        # Similarity check against existing
        is_dup = False
        for existing in unique:
            sim = ngram_similarity(text, existing['text'])
            if sim >= threshold:
                is_dup = True
                break
        
        if not is_dup:
            seen_hashes.add(text_hash)
            unique.append(fact)
    
    return unique

def cluster_by_similarity(facts):
    """Sort facts so similar ones are adjacent (greedy nearest neighbor)."""
    if len(facts) <= 1:
        return facts
    
    # Start with first fact
    ordered = [facts[0]]
    remaining = set(range(1, len(facts)))
    
    while remaining:
        last = ordered[-1]
        best_idx = None
        best_sim = -1
        
        # Find most similar to last added
        for idx in remaining:
            sim = word_similarity(last['text'], facts[idx]['text'])
            if sim > best_sim:
                best_sim = sim
                best_idx = idx
        
        if best_idx is not None:
            ordered.append(facts[best_idx])
            remaining.remove(best_idx)
    
    return ordered

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Input facts: {len(facts)}")
    
    # Deduplicate
    print("Deduplicating...")
    facts = deduplicate(facts)
    print(f"After dedup: {len(facts)}")
    
    # Group by category
    print("Grouping by category...")
    by_category = defaultdict(list)
    for fact in facts:
        cat = fact.get('category', 'general')
        by_category[cat].append(fact)
    
    print(f"Categories: {len(by_category)}")
    
    # Sort within each category by similarity
    print("Sorting by similarity within categories...")
    organized = []
    category_order = sorted(by_category.keys())
    
    for cat in category_order:
        cat_facts = by_category[cat]
        print(f"  {cat}: {len(cat_facts)} facts")
        
        # Cluster by similarity
        clustered = cluster_by_similarity(cat_facts)
        organized.extend(clustered)
    
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(organized, f, indent=2)
    
    print(f"\n=== Results ===")
    print(f"Total organized facts: {len(organized)}")
    print(f"Saved to: {OUTPUT_FILE}")
    
    # Category summary
    print(f"\nCategory breakdown:")
    for cat in category_order[:20]:
        print(f"  {cat}: {len(by_category[cat])}")
    if len(category_order) > 20:
        print(f"  ... and {len(category_order) - 20} more categories")

if __name__ == "__main__":
    main()
