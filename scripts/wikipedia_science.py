#!/usr/bin/env python3
"""Scrape science article intros from Wikipedia."""

import json
import re
import urllib.request
import urllib.parse
import time
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")

# Science-related Wikipedia articles to scrape intros from
ARTICLES = [
    # Physics
    "Speed_of_light", "Gravity", "Black_hole", "Neutron_star", "Quantum_mechanics",
    "Theory_of_relativity", "Higgs_boson", "Dark_matter", "Dark_energy", "Antimatter",
    "Superconductivity", "Nuclear_fusion", "Nuclear_fission", "Plasma_(physics)",
    "Electromagnetic_radiation", "Radioactive_decay", "Half-life", "Entropy",
    
    # Chemistry
    "Periodic_table", "Chemical_bond", "Covalent_bond", "Ionic_bonding", "Acid",
    "Base_(chemistry)", "pH", "Oxidation", "Catalyst", "Polymer", "Crystal",
    "Noble_gas", "Transition_metal", "Rare_earth_element", "Radioactive_element",
    
    # Biology
    "DNA", "RNA", "Protein", "Cell_(biology)", "Mitochondria", "Chloroplast",
    "Photosynthesis", "Cellular_respiration", "Evolution", "Natural_selection",
    "Genetic_mutation", "Gene", "Chromosome", "Genome", "CRISPR", "Stem_cell",
    "Neuron", "Synapse", "Hormone", "Enzyme", "Virus", "Bacteria", "Antibiotic",
    
    # Earth Science
    "Plate_tectonics", "Earthquake", "Volcano", "Tsunami", "Hurricane",
    "Climate_change", "Greenhouse_effect", "Ozone_layer", "Water_cycle",
    "Rock_cycle", "Fossil", "Geological_time_scale", "Ice_age", "Permafrost",
    
    # Astronomy
    "Solar_System", "Sun", "Moon", "Mars", "Jupiter", "Saturn", "Exoplanet",
    "Galaxy", "Milky_Way", "Andromeda_Galaxy", "Supernova", "Pulsar", "Quasar",
    "Cosmic_microwave_background", "Big_Bang", "Hubble_Space_Telescope",
    
    # Medicine
    "Immune_system", "Vaccine", "Cancer", "Heart", "Brain", "Liver", "Kidney",
    "Blood", "Lymphatic_system", "Nervous_system", "Endocrine_system",
    "Metabolism", "Allergy", "Autoimmune_disease", "Infection",
    
    # Technology
    "Computer", "Transistor", "Semiconductor", "Integrated_circuit", "Internet",
    "Artificial_intelligence", "Machine_learning", "Quantum_computing",
    "Nanotechnology", "3D_printing", "Renewable_energy", "Solar_cell",
    
    # Mathematics
    "Prime_number", "Pi", "Infinity", "Fibonacci_number", "Golden_ratio",
    "Fractal", "Chaos_theory", "Probability", "Statistics", "Calculus",
    
    # Animals
    "Elephant", "Blue_whale", "Great_white_shark", "Octopus", "Dolphin",
    "Chimpanzee", "Honey_bee", "Ant", "Tardigrade", "Axolotl", "Platypus",
    "Electric_eel", "Komodo_dragon", "Peregrine_falcon", "Hummingbird",
    
    # Plants
    "Tree", "Flower", "Seed", "Root", "Leaf", "Phototropism", "Carnivorous_plant",
    "Redwood", "Bamboo", "Orchid", "Cactus", "Fern", "Moss", "Algae",
]

def fetch_intro(title):
    """Get first 2 sentences of Wikipedia article."""
    encoded = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded}&prop=extracts&exintro=1&explaintext=1&exsentences=3&format=json"
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                extract = page.get('extract', '')
                if extract:
                    # Clean up
                    extract = re.sub(r'\s+', ' ', extract).strip()
                    # Split into sentences and take first 2
                    sentences = re.split(r'(?<=[.!?])\s+', extract)
                    return ' '.join(sentences[:2])
    except Exception as e:
        print(f"  Error: {e}")
    return None

def main():
    facts = []
    
    for article in ARTICLES:
        print(f"Fetching: {article}")
        intro = fetch_intro(article)
        
        if intro and len(intro) > 40:
            facts.append({
                'text': intro,
                'source': f'Wikipedia: {article.replace("_", " ")}',
                'source_url': f'https://en.wikipedia.org/wiki/{article}',
                'category': 'science_general'
            })
        
        time.sleep(0.3)
    
    output_file = OUTPUT_DIR / "wikipedia_science.json"
    with open(output_file, 'w') as f:
        json.dump(facts, f, indent=2)
    
    print(f"\nTotal: {len(facts)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
