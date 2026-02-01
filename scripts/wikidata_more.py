#!/usr/bin/env python3
"""More Wikidata queries for additional facts."""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

def run_query(query, retries=2):
    url = WIKIDATA_ENDPOINT + "?" + urllib.parse.urlencode({'query': query, 'format': 'json'})
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"  Retry {attempt+1}: {e}")
            time.sleep(3)
    return None

QUERIES = [
    # Bacteria
    ("bacteria", """SELECT ?item ?itemLabel WHERE {
      ?item wdt:P31 wd:Q10876.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"{b['itemLabel']['value']} is a species of bacteria." if not b['itemLabel']['value'].startswith('Q') else None),
    
    # Fungi
    ("fungi", """SELECT ?item ?itemLabel WHERE {
      ?item wdt:P31 wd:Q764.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"{b['itemLabel']['value']} is a species of fungus." if not b['itemLabel']['value'].startswith('Q') else None),
    
    # Enzymes
    ("enzymes", """SELECT ?enzyme ?enzymeLabel ?function ?functionLabel WHERE {
      ?enzyme wdt:P31 wd:Q8047.
      OPTIONAL { ?enzyme wdt:P681 ?function }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""", lambda b: f"The enzyme {b['enzymeLabel']['value']} plays a role in biochemical processes." if not b['enzymeLabel']['value'].startswith('Q') else None),
    
    # Bones
    ("bones", """SELECT ?bone ?boneLabel WHERE {
      ?bone wdt:P31 wd:Q265868.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 250""", lambda b: f"The {b['boneLabel']['value']} is a bone in the human body." if not b['boneLabel']['value'].startswith('Q') else None),
    
    # Muscles
    ("muscles", """SELECT ?muscle ?muscleLabel WHERE {
      ?muscle wdt:P31 wd:Q7365.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"The {b['muscleLabel']['value']} is a muscle in the human body." if not b['muscleLabel']['value'].startswith('Q') else None),
    
    # Galaxies
    ("galaxies", """SELECT ?galaxy ?galaxyLabel ?distance WHERE {
      ?galaxy wdt:P31 wd:Q318.
      OPTIONAL { ?galaxy wdt:P2583 ?distance }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""", lambda b: f"The {b['galaxyLabel']['value']} is a galaxy in our universe." if not b['galaxyLabel']['value'].startswith('Q') else None),
    
    # Nebulae
    ("nebulae", """SELECT ?nebula ?nebulaLabel WHERE {
      ?nebula wdt:P31 wd:Q1054444.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"The {b['nebulaLabel']['value']} is a nebula." if not b['nebulaLabel']['value'].startswith('Q') else None),
    
    # Constellations
    ("constellations", """SELECT ?const ?constLabel ?stars WHERE {
      ?const wdt:P31 wd:Q8928.
      OPTIONAL { ?const wdt:P527 ?stars }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 100""", lambda b: f"The constellation {b['constLabel']['value']} is visible in the night sky." if not b['constLabel']['value'].startswith('Q') else None),
    
    # Ocean currents
    ("ocean_currents", """SELECT ?current ?currentLabel WHERE {
      ?current wdt:P31 wd:Q182323.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""", lambda b: f"The {b['currentLabel']['value']} is an ocean current." if not b['currentLabel']['value'].startswith('Q') else None),
    
    # Tectonic plates
    ("tectonic_plates", """SELECT ?plate ?plateLabel ?area WHERE {
      ?plate wdt:P31 wd:Q12716.
      OPTIONAL { ?plate wdt:P2046 ?area }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 50""", lambda b: f"The {b['plateLabel']['value']} is a tectonic plate." if not b['plateLabel']['value'].startswith('Q') else None),
    
    # Hurricanes
    ("hurricanes", """SELECT ?storm ?stormLabel ?date ?wind WHERE {
      ?storm wdt:P31 wd:Q5765822.
      OPTIONAL { ?storm wdt:P585 ?date }
      OPTIONAL { ?storm wdt:P2052 ?wind }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""", lambda b: f"{b['stormLabel']['value']} was a tropical cyclone." if not b['stormLabel']['value'].startswith('Q') else None),
    
    # Scientific theories
    ("theories", """SELECT ?theory ?theoryLabel ?founder ?founderLabel WHERE {
      ?theory wdt:P31 wd:Q17737.
      OPTIONAL { ?theory wdt:P61 ?founder }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"{b['theoryLabel']['value']} is a scientific theory." if not b['theoryLabel']['value'].startswith('Q') else None),
    
    # Scientific laws
    ("laws", """SELECT ?law ?lawLabel WHERE {
      ?law wdt:P31 wd:Q408891.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""", lambda b: f"{b['lawLabel']['value']} is a law of science." if not b['lawLabel']['value'].startswith('Q') else None),
    
    # Alloys
    ("alloys", """SELECT ?alloy ?alloyLabel WHERE {
      ?alloy wdt:P31 wd:Q37756.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""", lambda b: f"{b['alloyLabel']['value']} is a metal alloy." if not b['alloyLabel']['value'].startswith('Q') else None),
    
    # Polymers
    ("polymers", """SELECT ?polymer ?polymerLabel WHERE {
      ?polymer wdt:P31 wd:Q81163.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""", lambda b: f"{b['polymerLabel']['value']} is a type of polymer." if not b['polymerLabel']['value'].startswith('Q') else None),
    
    # Drugs/medications
    ("medications", """SELECT ?drug ?drugLabel ?treats ?treatsLabel WHERE {
      ?drug wdt:P31 wd:Q12140.
      OPTIONAL { ?drug wdt:P2175 ?treats }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""", lambda b: f"{b['drugLabel']['value']} is a pharmaceutical drug." if not b['drugLabel']['value'].startswith('Q') else None),
    
    # Fossils
    ("fossils", """SELECT ?fossil ?fossilLabel ?age WHERE {
      ?fossil wdt:P31 wd:Q80007.
      OPTIONAL { ?fossil wdt:P580 ?age }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"{b['fossilLabel']['value']} is a known fossil specimen." if not b['fossilLabel']['value'].startswith('Q') else None),
    
    # Particle physics
    ("particles", """SELECT ?particle ?particleLabel ?mass WHERE {
      ?particle wdt:P31 wd:Q12503.
      OPTIONAL { ?particle wdt:P2067 ?mass }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 100""", lambda b: f"The {b['particleLabel']['value']} is a subatomic particle." if not b['particleLabel']['value'].startswith('Q') else None),
    
    # Syndromes
    ("syndromes", """SELECT ?syndrome ?syndromeLabel WHERE {
      ?syndrome wdt:P31 wd:Q179630.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""", lambda b: f"{b['syndromeLabel']['value']} is a medical syndrome." if not b['syndromeLabel']['value'].startswith('Q') else None),
    
    # Phobias
    ("phobias", """SELECT ?phobia ?phobiaLabel WHERE {
      ?phobia wdt:P31 wd:Q175854.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""", lambda b: f"{b['phobiaLabel']['value']} is a type of phobia." if not b['phobiaLabel']['value'].startswith('Q') else None),
]

def main():
    all_facts = []
    
    for category, query, formatter in QUERIES:
        print(f"Querying {category}...")
        results = run_query(query)
        
        if results and 'results' in results:
            count = 0
            for binding in results['results']['bindings']:
                try:
                    fact_text = formatter(binding)
                    if fact_text:
                        all_facts.append({
                            'text': fact_text,
                            'source': 'Wikidata',
                            'source_url': 'https://www.wikidata.org',
                            'category': category
                        })
                        count += 1
                except:
                    continue
            print(f"  Got {count} facts")
        
        time.sleep(2)
    
    output_file = OUTPUT_DIR / "wikidata_more.json"
    with open(output_file, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"\nTotal: {len(all_facts)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
