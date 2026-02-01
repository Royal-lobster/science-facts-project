#!/usr/bin/env python3
"""Deduplicate facts using n-gram similarity (no external deps)."""

import json
import re
from pathlib import Path
from collections import Counter
import hashlib

INPUT_FILE = Path("/root/clawd/projects/science-facts/consolidated_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/final_facts.json")
DUPLICATES_FILE = Path("/root/clawd/projects/science-facts/removed_duplicates.json")

# Similarity threshold
SIMILARITY_THRESHOLD = 0.75

def normalize(text):
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_ngrams(text, n=3):
    """Get character n-grams from text."""
    text = normalize(text)
    return [text[i:i+n] for i in range(len(text) - n + 1)]

def ngram_similarity(text1, text2):
    """Compute Jaccard similarity of n-grams."""
    ngrams1 = set(get_ngrams(text1))
    ngrams2 = set(get_ngrams(text2))
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    return intersection / union if union > 0 else 0.0

def get_word_set(text):
    """Get set of words for quick filtering."""
    return set(normalize(text).split())

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Total facts: {len(facts)}")
    
    # Pre-compute word sets and lengths for fast filtering
    print("Pre-computing features...")
    features = []
    for f in facts:
        text = f['text']
        features.append({
            'text': text,
            'norm': normalize(text),
            'words': get_word_set(text),
            'length': len(text)
        })
    
    print("Finding similar pairs...")
    to_remove = set()
    similar_pairs = []
    
    # Sort by length (longer facts first) to keep more detailed versions
    indices = sorted(range(len(facts)), key=lambda i: -features[i]['length'])
    
    checked = 0
    for idx, i in enumerate(indices):
        if i in to_remove:
            continue
        
        feat_i = features[i]
        
        # Compare with remaining facts
        for j in indices[idx+1:]:
            if j in to_remove:
                continue
            
            feat_j = features[j]
            
            # Quick filter: length ratio
            length_ratio = min(feat_i['length'], feat_j['length']) / max(feat_i['length'], feat_j['length'])
            if length_ratio < 0.5:
                continue
            
            # Quick filter: word overlap
            word_overlap = len(feat_i['words'] & feat_j['words']) / max(1, min(len(feat_i['words']), len(feat_j['words'])))
            if word_overlap < 0.4:
                continue
            
            # Full n-gram similarity
            sim = ngram_similarity(feat_i['text'], feat_j['text'])
            
            if sim >= SIMILARITY_THRESHOLD:
                to_remove.add(j)  # Remove shorter one (j comes after i in sorted order)
                similar_pairs.append({
                    'similarity': round(sim, 3),
                    'kept': feat_i['text'],
                    'removed': feat_j['text']
                })
        
        checked += 1
        if checked % 500 == 0:
            print(f"  Processed {checked}/{len(facts)} facts, found {len(to_remove)} duplicates")
    
    print(f"\nFound {len(to_remove)} semantic duplicates")
    
    # Filter out duplicates
    unique_facts = [f for i, f in enumerate(facts) if i not in to_remove]
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(unique_facts, f, indent=2)
    
    # Save sample of removed pairs for review
    with open(DUPLICATES_FILE, 'w') as f:
        json.dump(similar_pairs[:200], f, indent=2)
    
    print(f"\n=== Results ===")
    print(f"Original facts: {len(facts)}")
    print(f"Similar duplicates removed: {len(to_remove)}")
    print(f"Final unique facts: {len(unique_facts)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
