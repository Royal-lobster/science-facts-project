#!/usr/bin/env python3
"""Quick fact generator from multiple Wikipedia categories."""

import json
import re
import urllib.request
import urllib.parse
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")

# Wikipedia API to get random pages from categories
CATEGORIES = [
    "Superlatives",
    "Scientific_records",
    "Scientific_phenomena",
    "Extreme_points_of_Earth",
    "Biological_records",
    "Animal_intelligence",
    "Prehistoric_life",
    "Exoplanets",
    "Solar_System",
    "Human_anatomy",
    "Medical_phenomena",
    "Chemical_elements",
    "Chemical_compounds",
    "Physics",
    "Astronomy",
    "Biology",
    "Chemistry",
    "Earth_sciences",
    "Neuroscience",
    "Evolutionary_biology",
    "Marine_biology",
    "Botany",
    "Mycology",
    "Ornithology",
    "Entomology",
    "Meteorology",
    "Seismology",
    "Volcanology",
]

def fetch_category_members(category, limit=50):
    """Get pages in a category."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&cmlimit={limit}&cmtype=page&format=json"
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return [m['title'] for m in data.get('query', {}).get('categorymembers', [])]
    except:
        return []

def fetch_page_intro(title):
    """Get the first paragraph of a Wikipedia page."""
    encoded = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded}&prop=extracts&exintro=1&explaintext=1&format=json"
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                extract = page.get('extract', '')
                if extract and len(extract) > 50:
                    return extract[:500]  # First 500 chars
    except:
        pass
    return None

def extract_first_sentence(text):
    """Extract the first complete sentence."""
    if not text:
        return None
    
    # Find first sentence
    match = re.search(r'^([A-Z][^.!?]*[.!?])', text)
    if match:
        sentence = match.group(1).strip()
        if len(sentence) > 40 and len(sentence) < 300:
            return sentence
    return None

def main():
    all_facts = []
    
    for category in CATEGORIES:
        print(f"Processing category: {category}")
        pages = fetch_category_members(category, limit=30)
        
        for title in pages[:20]:  # Limit pages per category
            intro = fetch_page_intro(title)
            if intro:
                fact = extract_first_sentence(intro)
                if fact:
                    all_facts.append({
                        'text': fact,
                        'source': f'Wikipedia: {title}',
                        'source_url': f'https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}',
                        'category': category.lower().replace('_', ' ')
                    })
            
            time.sleep(0.3)  # Rate limit
        
        print(f"  Got {len([f for f in all_facts if f['category'] == category.lower().replace('_', ' ')])} facts")
    
    # Deduplicate
    seen = set()
    unique = []
    for f in all_facts:
        key = f['text'].lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(f)
    
    output_file = OUTPUT_DIR / "quick_facts.json"
    with open(output_file, 'w') as f:
        json.dump(unique, f, indent=2)
    
    print(f"\nTotal unique: {len(unique)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
