#!/usr/bin/env python3
"""Bulk extract facts from Wikidata using SPARQL - no LLM needed."""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

QUERIES = {
    "animals_lifespan": """
    SELECT ?animal ?animalLabel ?lifespan WHERE {
      ?animal wdt:P31 wd:Q16521;
              wdt:P2250 ?lifespan.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 500
    """,
    
    "animals_speed": """
    SELECT ?animal ?animalLabel ?speed WHERE {
      ?animal wdt:P31 wd:Q16521;
              wdt:P2052 ?speed.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300
    """,
    
    "elements_properties": """
    SELECT ?element ?elementLabel ?atomicNumber ?meltingPoint ?boilingPoint ?density WHERE {
      ?element wdt:P31 wd:Q11344;
               wdt:P1086 ?atomicNumber.
      OPTIONAL { ?element wdt:P2101 ?meltingPoint. }
      OPTIONAL { ?element wdt:P2102 ?boilingPoint. }
      OPTIONAL { ?element wdt:P2054 ?density. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """,
    
    "planets_data": """
    SELECT ?planet ?planetLabel ?mass ?radius ?orbitalPeriod ?surfaceTemp WHERE {
      ?planet wdt:P31 wd:Q634;
              wdt:P2067 ?mass.
      OPTIONAL { ?planet wdt:P2120 ?radius. }
      OPTIONAL { ?planet wdt:P2146 ?orbitalPeriod. }
      OPTIONAL { ?planet wdt:P2076 ?surfaceTemp. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """,
    
    "stars_data": """
    SELECT ?star ?starLabel ?mass ?luminosity ?distance WHERE {
      ?star wdt:P31 wd:Q523;
            wdt:P2067 ?mass.
      OPTIONAL { ?star wdt:P2060 ?luminosity. }
      OPTIONAL { ?star wdt:P2583 ?distance. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300
    """,
    
    "mountains_height": """
    SELECT ?mountain ?mountainLabel ?elevation ?country ?countryLabel WHERE {
      ?mountain wdt:P31 wd:Q8502;
                wdt:P2044 ?elevation.
      OPTIONAL { ?mountain wdt:P17 ?country. }
      FILTER(?elevation > 7000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 500
    """,
    
    "rivers_length": """
    SELECT ?river ?riverLabel ?length ?country ?countryLabel WHERE {
      ?river wdt:P31 wd:Q4022;
             wdt:P2043 ?length.
      OPTIONAL { ?river wdt:P17 ?country. }
      FILTER(?length > 1000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 500
    """,
    
    "lakes_area": """
    SELECT ?lake ?lakeLabel ?area ?depth WHERE {
      ?lake wdt:P31 wd:Q23397;
            wdt:P2046 ?area.
      OPTIONAL { ?lake wdt:P4511 ?depth. }
      FILTER(?area > 1000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
    
    "countries_population": """
    SELECT ?country ?countryLabel ?population ?area WHERE {
      ?country wdt:P31 wd:Q6256;
               wdt:P1082 ?population;
               wdt:P2046 ?area.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 250
    """,
    
    "inventions": """
    SELECT ?invention ?inventionLabel ?inventor ?inventorLabel ?date WHERE {
      ?invention wdt:P31 wd:Q39546;
                 wdt:P61 ?inventor.
      OPTIONAL { ?invention wdt:P571 ?date. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 500
    """,
    
    "scientists_discoveries": """
    SELECT ?scientist ?scientistLabel ?discovery ?discoveryLabel WHERE {
      ?scientist wdt:P31 wd:Q5;
                 wdt:P106 wd:Q901;
                 wdt:P61 ?discovery.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
    
    "diseases_causes": """
    SELECT ?disease ?diseaseLabel ?cause ?causeLabel WHERE {
      ?disease wdt:P31 wd:Q12136;
               wdt:P828 ?cause.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
    
    "minerals": """
    SELECT ?mineral ?mineralLabel ?hardness ?color ?colorLabel WHERE {
      ?mineral wdt:P31 wd:Q7946;
               wdt:P1088 ?hardness.
      OPTIONAL { ?mineral wdt:P462 ?color. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300
    """,
    
    "dinosaurs": """
    SELECT ?dino ?dinoLabel ?period ?periodLabel ?length WHERE {
      ?dino wdt:P31 wd:Q23038290.
      OPTIONAL { ?dino wdt:P2348 ?period. }
      OPTIONAL { ?dino wdt:P2043 ?length. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
    
    "volcanoes": """
    SELECT ?volcano ?volcanoLabel ?elevation ?lastEruption WHERE {
      ?volcano wdt:P31 wd:Q8072;
               wdt:P2044 ?elevation.
      OPTIONAL { ?volcano wdt:P793 ?lastEruption. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
    
    "spacecraft": """
    SELECT ?craft ?craftLabel ?launchDate ?operator ?operatorLabel WHERE {
      ?craft wdt:P31 wd:Q40218;
             wdt:P619 ?launchDate.
      OPTIONAL { ?craft wdt:P137 ?operator. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400
    """,
}

def run_query(query):
    """Execute SPARQL query against Wikidata."""
    url = WIKIDATA_ENDPOINT + "?" + urllib.parse.urlencode({
        'query': query,
        'format': 'json'
    })
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0 (educational project)'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  Query error: {e}")
        return None

def format_facts(query_name, results):
    """Convert SPARQL results to fact strings."""
    facts = []
    
    if not results or 'results' not in results:
        return facts
    
    bindings = results['results']['bindings']
    
    for b in bindings:
        try:
            if query_name == "animals_lifespan":
                name = b.get('animalLabel', {}).get('value', '')
                lifespan = b.get('lifespan', {}).get('value', '')
                if name and lifespan and not name.startswith('Q'):
                    facts.append(f"The {name} has an average lifespan of {float(lifespan):.0f} years.")
                    
            elif query_name == "animals_speed":
                name = b.get('animalLabel', {}).get('value', '')
                speed = b.get('speed', {}).get('value', '')
                if name and speed and not name.startswith('Q'):
                    facts.append(f"The {name} can reach speeds of {float(speed):.1f} km/h.")
                    
            elif query_name == "elements_properties":
                name = b.get('elementLabel', {}).get('value', '')
                atomic = b.get('atomicNumber', {}).get('value', '')
                melting = b.get('meltingPoint', {}).get('value', '')
                boiling = b.get('boilingPoint', {}).get('value', '')
                if name and atomic and not name.startswith('Q'):
                    fact = f"{name} (atomic number {atomic})"
                    if melting:
                        fact += f" melts at {float(melting):.0f}K"
                    if boiling:
                        fact += f" and boils at {float(boiling):.0f}K"
                    facts.append(fact + ".")
                    
            elif query_name == "mountains_height":
                name = b.get('mountainLabel', {}).get('value', '')
                elev = b.get('elevation', {}).get('value', '')
                country = b.get('countryLabel', {}).get('value', '')
                if name and elev and not name.startswith('Q'):
                    fact = f"{name} stands at {float(elev):.0f} meters"
                    if country and not country.startswith('Q'):
                        fact += f" in {country}"
                    facts.append(fact + ".")
                    
            elif query_name == "rivers_length":
                name = b.get('riverLabel', {}).get('value', '')
                length = b.get('length', {}).get('value', '')
                if name and length and not name.startswith('Q'):
                    facts.append(f"The {name} river stretches {float(length):.0f} kilometers.")
                    
            elif query_name == "lakes_area":
                name = b.get('lakeLabel', {}).get('value', '')
                area = b.get('area', {}).get('value', '')
                depth = b.get('depth', {}).get('value', '')
                if name and area and not name.startswith('Q'):
                    fact = f"{name} covers an area of {float(area):.0f} square kilometers"
                    if depth:
                        fact += f" with a maximum depth of {float(depth):.0f} meters"
                    facts.append(fact + ".")
                    
            elif query_name == "inventions":
                invention = b.get('inventionLabel', {}).get('value', '')
                inventor = b.get('inventorLabel', {}).get('value', '')
                if invention and inventor and not invention.startswith('Q') and not inventor.startswith('Q'):
                    facts.append(f"The {invention} was invented by {inventor}.")
                    
            elif query_name == "dinosaurs":
                name = b.get('dinoLabel', {}).get('value', '')
                period = b.get('periodLabel', {}).get('value', '')
                length = b.get('length', {}).get('value', '')
                if name and not name.startswith('Q'):
                    fact = f"{name}"
                    if period and not period.startswith('Q'):
                        fact += f" lived during the {period}"
                    if length:
                        fact += f" and could grow to {float(length):.1f} meters"
                    facts.append(fact + ".")
                    
            elif query_name == "volcanoes":
                name = b.get('volcanoLabel', {}).get('value', '')
                elev = b.get('elevation', {}).get('value', '')
                if name and elev and not name.startswith('Q'):
                    facts.append(f"The volcano {name} rises to {float(elev):.0f} meters.")
                    
            elif query_name == "minerals":
                name = b.get('mineralLabel', {}).get('value', '')
                hardness = b.get('hardness', {}).get('value', '')
                if name and hardness and not name.startswith('Q'):
                    facts.append(f"{name} has a hardness of {hardness} on the Mohs scale.")
                    
            elif query_name == "spacecraft":
                name = b.get('craftLabel', {}).get('value', '')
                date = b.get('launchDate', {}).get('value', '')
                operator = b.get('operatorLabel', {}).get('value', '')
                if name and date and not name.startswith('Q'):
                    year = date[:4] if date else ''
                    fact = f"{name} was launched in {year}"
                    if operator and not operator.startswith('Q'):
                        fact += f" by {operator}"
                    facts.append(fact + ".")
                    
            else:
                # Generic handler
                label = None
                for key in b:
                    if 'Label' in key and b[key].get('value', '') and not b[key]['value'].startswith('Q'):
                        label = b[key]['value']
                        break
                if label:
                    facts.append(f"Fact about {label}: {query_name.replace('_', ' ')}.")
                    
        except Exception as e:
            continue
            
    return facts

def main():
    all_facts = []
    
    for name, query in QUERIES.items():
        print(f"Running query: {name}...")
        results = run_query(query)
        
        if results:
            facts = format_facts(name, results)
            all_facts.extend([{
                'text': f,
                'source': 'wikidata',
                'category': name,
                'source_url': 'https://www.wikidata.org'
            } for f in facts])
            print(f"  Got {len(facts)} facts")
        
        time.sleep(2)  # Rate limiting
    
    # Save all facts
    output_file = OUTPUT_DIR / "wikidata_bulk.json"
    with open(output_file, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"\nTotal facts: {len(all_facts)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
