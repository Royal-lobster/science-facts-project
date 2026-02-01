import json
import sys

# Load existing facts to check for duplicates
with open('final_10001_facts.json', 'r') as f:
    existing = json.load(f)

existing_texts = set(fact['text'].lower().strip() for fact in existing)

# Read new facts from stdin
new_facts = json.load(sys.stdin)

added = 0
for fact in new_facts:
    text_lower = fact['text'].lower().strip()
    if text_lower not in existing_texts:
        existing.append(fact)
        existing_texts.add(text_lower)
        added += 1

with open('final_10001_facts.json', 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Added {added} new facts. Total: {len(existing)}")
