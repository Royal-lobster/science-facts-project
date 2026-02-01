#!/usr/bin/env python3
"""Deduplicate facts using embeddings to find semantically similar ones."""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys

INPUT_FILE = Path("/root/clawd/projects/science-facts/consolidated_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/final_facts.json")
DUPLICATES_FILE = Path("/root/clawd/projects/science-facts/removed_duplicates.json")

# Similarity threshold - facts above this are considered duplicates
SIMILARITY_THRESHOLD = 0.92

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Total facts: {len(facts)}")
    
    # Extract texts
    texts = [f['text'] for f in facts]
    
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Computing embeddings (this may take a few minutes)...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    
    print("Finding similar pairs...")
    # Process in batches to avoid memory issues
    batch_size = 1000
    to_remove = set()
    similar_pairs = []
    
    for i in range(0, len(embeddings), batch_size):
        batch_end = min(i + batch_size, len(embeddings))
        batch_embeddings = embeddings[i:batch_end]
        
        # Compare with all embeddings after current position
        for j in range(i, len(embeddings), batch_size):
            if j < i:
                continue
            
            compare_end = min(j + batch_size, len(embeddings))
            compare_embeddings = embeddings[j:compare_end]
            
            # Compute similarity matrix
            sim_matrix = cosine_similarity(batch_embeddings, compare_embeddings)
            
            # Find pairs above threshold
            for bi, row in enumerate(sim_matrix):
                global_i = i + bi
                for bj, sim in enumerate(row):
                    global_j = j + bj
                    
                    # Skip self-comparison and already processed pairs
                    if global_j <= global_i:
                        continue
                    
                    if sim >= SIMILARITY_THRESHOLD:
                        # Keep the longer/more detailed fact, remove the shorter one
                        if len(texts[global_i]) >= len(texts[global_j]):
                            to_remove.add(global_j)
                        else:
                            to_remove.add(global_i)
                        
                        similar_pairs.append({
                            'similarity': float(sim),
                            'kept': texts[global_i] if global_i not in to_remove else texts[global_j],
                            'removed': texts[global_j] if global_i not in to_remove else texts[global_i]
                        })
        
        print(f"  Processed {batch_end}/{len(embeddings)} facts, found {len(to_remove)} duplicates so far")
    
    print(f"\nFound {len(to_remove)} semantic duplicates")
    
    # Filter out duplicates
    unique_facts = [f for i, f in enumerate(facts) if i not in to_remove]
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(unique_facts, f, indent=2)
    
    with open(DUPLICATES_FILE, 'w') as f:
        json.dump(similar_pairs[:500], f, indent=2)  # Save sample of removed pairs
    
    print(f"\n=== Results ===")
    print(f"Original facts: {len(facts)}")
    print(f"Semantic duplicates removed: {len(to_remove)}")
    print(f"Final unique facts: {len(unique_facts)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Duplicate pairs sample: {DUPLICATES_FILE}")

if __name__ == "__main__":
    main()
