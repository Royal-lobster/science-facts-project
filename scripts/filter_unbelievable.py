#!/usr/bin/env python3
"""Filter for truly unbelievable/surprising facts, not just data points."""

import json
import re
from pathlib import Path

INPUT_FILE = Path("/root/clawd/projects/science-facts/quality_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/unbelievable_facts.json")

# Patterns that indicate boring data, not interesting facts
BORING_PATTERNS = [
    r"^The .+ has an average lifespan of \d+ years\.$",
    r"^The .+ weighs approximately [\d.]+ kg\.$",
    r"^The .+ river stretches [\d,]+ kilometers\.$",
    r"^The .+ covers an area of [\d,]+ square kilometers\.$",
    r"^.+ stands at [\d,]+ meters",
    r"^The .+ has a wingspan of [\d.]+ meters\.$",
    r"^The .+ drops [\d,]+ meters\.$",
    r"^The .+ spans [\d,]+ meters\.$",
    r"^.+ rises to [\d,]+ meters\.$",
    r"^.+ extends [\d.]+ kilometers\.$",
    r"^The island of .+ has an area of",
    r"^The .+ is a tectonic plate\.$",
    r"^The .+ is an ocean current\.$",
    r"^Asteroid .+ has a diameter of",
    r"^The star .+ is approximately [\d.]+ parsecs",
    r"^.+ had a recorded height of [\d.]+ meters\.$",
    r"^.+ \(atomic number \d+\)",
    r"^The .+ measured [\d.]+ on the Richter scale\.$",
    r"^The volcano .+ rises to",
    r"^Comet .+ has an orbital period of",
    r"^The moon .+ completes an orbit every",
    r"^The .+ reaches a depth of [\d,]+ meters\.$",
    r"^The .+ spans [\d,]+ square kilometers\.$",
    r"^.+ sits at an elevation of [\d,]+ meters\.$",
]

# Words/phrases that suggest interesting facts
INTERESTING_MARKERS = [
    'surprisingly', 'remarkably', 'incredibly', 'amazingly', 'astonishingly',
    'counterintuitively', 'unexpectedly', 'paradoxically', 'bizarrely',
    'only', 'first', 'unique', 'rare', 'extinct', 'discovered',
    'can actually', 'able to', 'capable of', 'unlike any other',
    'more than', 'less than', 'times', 'percent', 'despite',
    'although', 'even though', 'however', 'but', 'yet',
    'scientists found', 'research shows', 'studies reveal',
    'no one knew', 'long believed', 'thought to be', 'turns out',
    'myth', 'misconception', 'contrary to', 'opposite of',
    'survive', 'withstand', 'resist', 'immune', 'regenerate',
    'communicate', 'remember', 'recognize', 'solve', 'learn',
    'billion', 'million', 'trillion', 'thousand times',
    'before', 'after', 'since', 'until', 'ever',
    'fastest', 'slowest', 'largest', 'smallest', 'oldest', 'youngest',
    'hottest', 'coldest', 'deepest', 'highest', 'longest', 'shortest',
    'most', 'least', 'only known', 'never', 'always', 'every',
    'secret', 'hidden', 'unknown', 'mysterious', 'strange', 'weird',
    'deadly', 'dangerous', 'lethal', 'toxic', 'venomous', 'poisonous',
    'ancient', 'prehistoric', 'extinct', 'fossilized',
    'invented', 'created', 'designed', 'built', 'developed',
    'accident', 'mistake', 'coincidence', 'serendipity',
]

def is_boring_stat(text):
    """Check if this is just a boring statistic."""
    for pattern in BORING_PATTERNS:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False

def has_wow_factor(text):
    """Check if fact has interesting/surprising content."""
    text_lower = text.lower()
    
    # If it's long enough and not a boring stat, it's probably interesting
    if len(text) >= 60:
        return True
    
    # For shorter facts, be more selective
    for marker in INTERESTING_MARKERS:
        if marker in text_lower:
            return True
    
    return False

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Total input: {len(facts)}")
    
    unbelievable = []
    boring_count = 0
    no_wow_count = 0
    
    for fact in facts:
        text = fact['text']
        
        # Skip boring stats
        if is_boring_stat(text):
            boring_count += 1
            continue
        
        # Check for wow factor
        if has_wow_factor(text):
            unbelievable.append(fact)
        else:
            no_wow_count += 1
    
    print(f"\n=== Filtering Results ===")
    print(f"Boring stats removed: {boring_count}")
    print(f"No wow factor: {no_wow_count}")
    print(f"Unbelievable facts kept: {len(unbelievable)}")
    
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(unbelievable, f, indent=2)
    
    print(f"\nSaved to: {OUTPUT_FILE}")
    
    # Show samples
    print("\n=== Sample unbelievable facts ===")
    import random
    for fact in random.sample(unbelievable, min(10, len(unbelievable))):
        print(f"• {fact['text'][:150]}...")
        print()

if __name__ == "__main__":
    main()
