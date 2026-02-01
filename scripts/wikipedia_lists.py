#!/usr/bin/env python3
"""Scrape Wikipedia list pages for facts - no LLM needed."""

import json
import re
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")

# Wikipedia list pages with interesting facts
LIST_PAGES = [
    ("List_of_animal_names", "animals"),
    ("List_of_longest-living_organisms", "biology"),
    ("List_of_largest_organisms", "biology"),
    ("List_of_venomous_animals", "biology"),
    ("List_of_poisonous_animals", "biology"),
    ("List_of_deadliest_animals_to_humans", "biology"),
    ("List_of_animals_by_number_of_neurons", "neuroscience"),
    ("List_of_animals_displaying_homosexual_behavior", "biology"),
    ("List_of_longest_rivers", "geography"),
    ("List_of_largest_lakes", "geography"),
    ("List_of_tallest_mountains", "geography"),
    ("List_of_deepest_caves", "geography"),
    ("List_of_largest_volcanic_eruptions", "geology"),
    ("List_of_impact_craters_on_Earth", "geology"),
    ("List_of_exoplanets", "astronomy"),
    ("List_of_nearest_stars", "astronomy"),
    ("List_of_most_massive_stars", "astronomy"),
    ("List_of_largest_known_stars", "astronomy"),
    ("List_of_chemical_elements", "chemistry"),
    ("List_of_unsolved_problems_in_physics", "physics"),
    ("List_of_unsolved_problems_in_chemistry", "chemistry"),
    ("List_of_unsolved_problems_in_biology", "biology"),
    ("List_of_human_body_parts_named_after_people", "anatomy"),
    ("List_of_Nobel_laureates_in_Physics", "physics"),
    ("List_of_Nobel_laureates_in_Chemistry", "chemistry"),
    ("List_of_Nobel_laureates_in_Physiology_or_Medicine", "medicine"),
    ("List_of_common_misconceptions", "general"),
    ("List_of_inventors", "technology"),
    ("List_of_multiple_discoveries", "science_history"),
]

def fetch_page(title):
    """Fetch Wikipedia page content via API."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=extracts&explaintext=1&format=json"
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                return page.get('extract', '')
    except Exception as e:
        print(f"  Error fetching {title}: {e}")
    return None

def extract_facts_from_text(text, category):
    """Extract fact-like sentences from Wikipedia text."""
    facts = []
    
    if not text:
        return facts
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        # Skip very short or very long sentences
        if len(sentence) < 40 or len(sentence) > 400:
            continue
            
        # Skip sentences that are likely headers or formatting
        if sentence.startswith('==') or sentence.endswith('=='):
            continue
            
        # Skip sentences with too many numbers (likely tables)
        if len(re.findall(r'\d+', sentence)) > 5:
            continue
            
        # Skip sentences that are mostly punctuation or special chars
        alpha_ratio = len(re.findall(r'[a-zA-Z]', sentence)) / max(len(sentence), 1)
        if alpha_ratio < 0.6:
            continue
            
        # Keep sentences with interesting keywords
        interesting = any(word in sentence.lower() for word in [
            'discovered', 'invented', 'largest', 'smallest', 'first', 'only',
            'fastest', 'slowest', 'highest', 'lowest', 'oldest', 'youngest',
            'unique', 'rare', 'extinct', 'ancient', 'million', 'billion',
            'scientist', 'research', 'found that', 'known as', 'called',
            'approximately', 'about', 'nearly', 'over', 'under', 'between',
            'species', 'animal', 'planet', 'star', 'element', 'chemical',
            'temperature', 'pressure', 'energy', 'light', 'sound', 'wave'
        ])
        
        if interesting:
            # Clean up the sentence
            sentence = sentence.strip()
            if not sentence.endswith('.'):
                sentence += '.'
            facts.append(sentence)
    
    return facts[:100]  # Limit per page

def main():
    all_facts = []
    
    for page_title, category in LIST_PAGES:
        print(f"Fetching: {page_title}...")
        content = fetch_page(page_title)
        
        if content:
            facts = extract_facts_from_text(content, category)
            for fact in facts:
                all_facts.append({
                    'text': fact,
                    'source': f'Wikipedia: {page_title.replace("_", " ")}',
                    'source_url': f'https://en.wikipedia.org/wiki/{page_title}',
                    'category': category
                })
            print(f"  Extracted {len(facts)} facts")
        
        time.sleep(1)  # Rate limiting
    
    # Save
    output_file = OUTPUT_DIR / "wikipedia_lists.json"
    with open(output_file, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"\nTotal: {len(all_facts)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
