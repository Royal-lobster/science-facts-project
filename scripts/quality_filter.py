#!/usr/bin/env python3
"""Filter out low-quality facts that don't match our engaging style."""

import json
import re
from pathlib import Path

INPUT_FILE = Path("/root/clawd/projects/science-facts/final_facts.json")
OUTPUT_FILE = Path("/root/clawd/projects/science-facts/quality_facts.json")
REJECTED_FILE = Path("/root/clawd/projects/science-facts/rejected_facts.json")

# Generic endings that indicate boring facts
BORING_ENDINGS = [
    "is a species of bacteria.",
    "is a species of fungus.", 
    "is a type of polymer.",
    "is a metal alloy.",
    "is a pharmaceutical drug.",
    "is a known fossil specimen.",
    "is a medical syndrome.",
    "is a type of phobia.",
    "is a subatomic particle.",
    "is a bone in the human body.",
    "is a muscle in the human body.",
    "is a galaxy in our universe.",
    "is a nebula.",
    "is an ocean current.",
    "is a tectonic plate.",
    "was a tropical cyclone.",
    "is a scientific theory.",
    "is a law of science.",
]

# Generic patterns
BORING_PATTERNS = [
    r"^[A-Za-z]+ \(atomic number \d+\)\.$",  # Just element + atomic number
    r"^The .+ is visible in the night sky\.$",  # Generic constellation
    r"^.+ plays a role in biochemical processes\.$",  # Generic enzyme
]

def is_interesting(text):
    """Check if a fact is interesting enough to keep."""
    
    # Too short (very short facts lack context)
    if len(text) < 35:
        return False, "too_short"
    
    # Too long (probably an article intro, not a fact)
    if len(text) > 400:
        return False, "too_long"
    
    # Check boring endings
    for ending in BORING_ENDINGS:
        if text.endswith(ending):
            return False, "boring_ending"
    
    # Check boring patterns
    for pattern in BORING_PATTERNS:
        if re.match(pattern, text):
            return False, "boring_pattern"
    
    # Accept if longer than 80 chars and has good content
    # (longer facts tend to have more context/interest)
    if len(text) >= 80:
        return True, "ok"
    
    # For shorter facts, check for interesting content
    interesting_words = [
        'discovered', 'first', 'only', 'largest', 'smallest', 'fastest',
        'slowest', 'oldest', 'youngest', 'highest', 'lowest', 'deepest',
        'hottest', 'coldest', 'million', 'billion', 'trillion', 'percent',
        'unique', 'rare', 'unusual', 'surprisingly', 'remarkably', 'ancient',
        'can', 'able to', 'capable of', 'unlike', 'despite', 'although',
        'weighs', 'measures', 'reaches', 'spans', 'contains'
    ]
    
    text_lower = text.lower()
    has_interesting = any(word in text_lower for word in interesting_words)
    
    # Also accept if it has specific numbers
    has_numbers = bool(re.search(r'\d+', text))
    
    if not has_interesting and not has_numbers:
        return False, "not_interesting"
    
    return True, "ok"

def main():
    print("Loading facts...")
    with open(INPUT_FILE) as f:
        facts = json.load(f)
    
    print(f"Total facts: {len(facts)}")
    
    quality_facts = []
    rejected = []
    rejection_reasons = {}
    
    for fact in facts:
        is_good, reason = is_interesting(fact['text'])
        
        if is_good:
            quality_facts.append(fact)
        else:
            rejected.append({'text': fact['text'], 'reason': reason})
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
    
    print(f"\n=== Filtering Results ===")
    print(f"Quality facts: {len(quality_facts)}")
    print(f"Rejected: {len(rejected)}")
    print(f"\nRejection breakdown:")
    for reason, count in sorted(rejection_reasons.items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count}")
    
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(quality_facts, f, indent=2)
    
    with open(REJECTED_FILE, 'w') as f:
        json.dump(rejected[:500], f, indent=2)  # Sample of rejected
    
    print(f"\nSaved quality facts to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
