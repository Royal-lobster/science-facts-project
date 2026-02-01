#!/usr/bin/env python3
"""Mega Wikidata scraper - get thousands of facts from many entity types."""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/facts_raw")
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

def run_query(query, retries=3):
    """Execute SPARQL query."""
    url = WIKIDATA_ENDPOINT + "?" + urllib.parse.urlencode({
        'query': query,
        'format': 'json'
    })
    
    headers = {'User-Agent': 'ScienceFactsBot/1.0'}
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"    Attempt {attempt+1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    return None

# Each entry: (query_template, result_formatter, category, limit)
FACT_GENERATORS = [
    # Animal facts
    ("""SELECT ?item ?itemLabel ?mass WHERE {
      ?item wdt:P31 wd:Q16521; wdt:P2067 ?mass.
      FILTER(?mass > 0.001 && ?mass < 200000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 800""",
    lambda b: f"The {b['itemLabel']['value']} weighs approximately {float(b['mass']['value']):.2f} kg.",
    "animal_weight", 800),
    
    # Bird wingspans
    ("""SELECT ?bird ?birdLabel ?wingspan WHERE {
      ?bird wdt:P31 wd:Q16521; wdt:P2050 ?wingspan.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"The {b['birdLabel']['value']} has a wingspan of {float(b['wingspan']['value']):.2f} meters.",
    "bird_wingspan", 400),
    
    # Human height records
    ("""SELECT ?person ?personLabel ?height WHERE {
      ?person wdt:P31 wd:Q5; wdt:P2048 ?height.
      FILTER(?height > 2.0 || ?height < 0.6)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"{b['personLabel']['value']} had a recorded height of {float(b['height']['value']):.2f} meters.",
    "human_height", 300),
    
    # Building heights
    ("""SELECT ?building ?buildingLabel ?height ?country ?countryLabel WHERE {
      ?building wdt:P31 wd:Q41176; wdt:P2048 ?height.
      OPTIONAL { ?building wdt:P17 ?country }
      FILTER(?height > 200)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 500""",
    lambda b: f"{b['buildingLabel']['value']} stands {float(b['height']['value']):.0f} meters tall{' in ' + b['countryLabel']['value'] if b.get('countryLabel', {}).get('value', '').strip() and not b['countryLabel']['value'].startswith('Q') else ''}.",
    "buildings", 500),
    
    # Astronomical objects distance
    ("""SELECT ?object ?objectLabel ?distance WHERE {
      ?object wdt:P31 wd:Q523; wdt:P2583 ?distance.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"The star {b['objectLabel']['value']} is approximately {float(b['distance']['value']):.2f} parsecs from Earth.",
    "star_distance", 400),
    
    # Asteroid sizes
    ("""SELECT ?asteroid ?asteroidLabel ?diameter WHERE {
      ?asteroid wdt:P31 wd:Q3863; wdt:P2386 ?diameter.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"Asteroid {b['asteroidLabel']['value']} has a diameter of {float(b['diameter']['value']):.1f} km.",
    "asteroids", 400),
    
    # Earthquakes magnitude
    ("""SELECT ?quake ?quakeLabel ?magnitude ?date ?location ?locationLabel WHERE {
      ?quake wdt:P31 wd:Q7944; wdt:P2528 ?magnitude.
      OPTIONAL { ?quake wdt:P585 ?date }
      OPTIONAL { ?quake wdt:P276 ?location }
      FILTER(?magnitude > 6)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"The {b['quakeLabel']['value']} measured {float(b['magnitude']['value']):.1f} on the Richter scale.",
    "earthquakes", 400),
    
    # Bridges span
    ("""SELECT ?bridge ?bridgeLabel ?length ?country ?countryLabel WHERE {
      ?bridge wdt:P31 wd:Q12280; wdt:P2043 ?length.
      OPTIONAL { ?bridge wdt:P17 ?country }
      FILTER(?length > 500)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"The {b['bridgeLabel']['value']} spans {float(b['length']['value']):.0f} meters.",
    "bridges", 400),
    
    # Tunnels length
    ("""SELECT ?tunnel ?tunnelLabel ?length WHERE {
      ?tunnel wdt:P31 wd:Q44377; wdt:P2043 ?length.
      FILTER(?length > 5000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The {b['tunnelLabel']['value']} extends {float(b['length']['value'])/1000:.1f} kilometers.",
    "tunnels", 300),
    
    # Dams height
    ("""SELECT ?dam ?damLabel ?height ?capacity WHERE {
      ?dam wdt:P31 wd:Q12323; wdt:P2048 ?height.
      OPTIONAL { ?dam wdt:P2234 ?capacity }
      FILTER(?height > 100)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The {b['damLabel']['value']} rises {float(b['height']['value']):.0f} meters.",
    "dams", 300),
    
    # Proteins molecular mass
    ("""SELECT ?protein ?proteinLabel ?mass WHERE {
      ?protein wdt:P31 wd:Q8054; wdt:P2067 ?mass.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The protein {b['proteinLabel']['value']} has a molecular mass of {float(b['mass']['value']):.0f} Da.",
    "proteins", 300),
    
    # Viruses
    ("""SELECT ?virus ?virusLabel ?host ?hostLabel WHERE {
      ?virus wdt:P31 wd:Q808; wdt:P2975 ?host.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The {b['virusLabel']['value']} virus infects {b['hostLabel']['value']}." if not b['hostLabel']['value'].startswith('Q') else None,
    "viruses", 300),
    
    # Isotopes half-life
    ("""SELECT ?isotope ?isotopeLabel ?halflife WHERE {
      ?isotope wdt:P31 wd:Q25276; wdt:P2114 ?halflife.
      FILTER(?halflife > 0)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"{b['isotopeLabel']['value']} has a half-life of {float(b['halflife']['value']):.2e} seconds.",
    "isotopes", 300),
    
    # Airports elevation
    ("""SELECT ?airport ?airportLabel ?elevation ?country ?countryLabel WHERE {
      ?airport wdt:P31 wd:Q94993; wdt:P2044 ?elevation.
      OPTIONAL { ?airport wdt:P17 ?country }
      FILTER(?elevation > 2000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"{b['airportLabel']['value']} sits at an elevation of {float(b['elevation']['value']):.0f} meters.",
    "airports", 300),
    
    # Glaciers area
    ("""SELECT ?glacier ?glacierLabel ?area WHERE {
      ?glacier wdt:P31 wd:Q35666; wdt:P2046 ?area.
      FILTER(?area > 100)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The {b['glacierLabel']['value']} covers {float(b['area']['value']):.0f} square kilometers.",
    "glaciers", 300),
    
    # Islands area
    ("""SELECT ?island ?islandLabel ?area WHERE {
      ?island wdt:P31 wd:Q23442; wdt:P2046 ?area.
      FILTER(?area > 1000)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"The island of {b['islandLabel']['value']} has an area of {float(b['area']['value']):.0f} square kilometers.",
    "islands", 400),
    
    # Waterfalls height
    ("""SELECT ?waterfall ?waterfallLabel ?height WHERE {
      ?waterfall wdt:P31 wd:Q34038; wdt:P2044 ?height.
      FILTER(?height > 50)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"{b['waterfallLabel']['value']} drops {float(b['height']['value']):.0f} meters.",
    "waterfalls", 300),
    
    # Deserts area
    ("""SELECT ?desert ?desertLabel ?area WHERE {
      ?desert wdt:P31 wd:Q8514; wdt:P2046 ?area.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""",
    lambda b: f"The {b['desertLabel']['value']} spans {float(b['area']['value']):.0f} square kilometers.",
    "deserts", 200),
    
    # Scientific discoveries
    ("""SELECT ?discovery ?discoveryLabel ?discoverer ?discovererLabel ?date WHERE {
      ?discovery wdt:P31 wd:Q5; wdt:P61 ?discoverer.
      OPTIONAL { ?discovery wdt:P575 ?date }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"{b['discoveryLabel']['value']} was discovered by {b['discovererLabel']['value']}." if not b['discovererLabel']['value'].startswith('Q') and not b['discoveryLabel']['value'].startswith('Q') else None,
    "discoveries", 400),
    
    # Chemical compounds boiling point
    ("""SELECT ?compound ?compoundLabel ?boilingPoint WHERE {
      ?compound wdt:P31 wd:Q11173; wdt:P2102 ?boilingPoint.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 400""",
    lambda b: f"{b['compoundLabel']['value']} boils at {float(b['boilingPoint']['value']):.1f}K.",
    "compounds", 400),
    
    # Moons orbital period
    ("""SELECT ?moon ?moonLabel ?period ?planet ?planetLabel WHERE {
      ?moon wdt:P31 wd:Q2537; wdt:P2146 ?period.
      OPTIONAL { ?moon wdt:P397 ?planet }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 300""",
    lambda b: f"The moon {b['moonLabel']['value']} completes an orbit every {float(b['period']['value']):.2f} days.",
    "moons", 300),
    
    # Caves depth
    ("""SELECT ?cave ?caveLabel ?depth WHERE {
      ?cave wdt:P31 wd:Q35509; wdt:P4511 ?depth.
      FILTER(?depth > 100)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""",
    lambda b: f"The {b['caveLabel']['value']} reaches a depth of {float(b['depth']['value']):.0f} meters.",
    "caves", 200),
    
    # Comets orbital period
    ("""SELECT ?comet ?cometLabel ?period WHERE {
      ?comet wdt:P31 wd:Q3559; wdt:P2146 ?period.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 200""",
    lambda b: f"Comet {b['cometLabel']['value']} has an orbital period of {float(b['period']['value']):.1f} years.",
    "comets", 200),
]

def main():
    all_facts = []
    
    for query, formatter, category, limit in FACT_GENERATORS:
        print(f"Querying {category}...")
        results = run_query(query)
        
        if results and 'results' in results:
            count = 0
            for binding in results['results']['bindings']:
                try:
                    # Check for Q-codes in labels (unresolved entities)
                    has_qcode = False
                    for key, val in binding.items():
                        if 'Label' in key and val.get('value', '').startswith('Q'):
                            has_qcode = True
                            break
                    
                    if has_qcode:
                        continue
                        
                    fact_text = formatter(binding)
                    if fact_text and len(fact_text) > 20:
                        all_facts.append({
                            'text': fact_text,
                            'source': 'Wikidata',
                            'source_url': 'https://www.wikidata.org',
                            'category': category
                        })
                        count += 1
                except Exception as e:
                    continue
            
            print(f"  Got {count} facts")
        else:
            print(f"  Query failed")
        
        time.sleep(3)  # Rate limiting
    
    # Deduplicate
    seen = set()
    unique = []
    for f in all_facts:
        key = f['text'].lower()
        if key not in seen:
            seen.add(key)
            unique.append(f)
    
    output_file = OUTPUT_DIR / "wikidata_mega.json"
    with open(output_file, 'w') as f:
        json.dump(unique, f, indent=2)
    
    print(f"\n=== Total unique facts: {len(unique)} ===")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
