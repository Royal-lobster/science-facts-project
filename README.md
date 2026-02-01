---
license: mit
task_categories:
  - text-generation
  - question-answering
language:
  - en
tags:
  - science
  - facts
  - trivia
  - education
size_categories:
  - 10K<n<100K
---

# 10,000 Science Facts

A collection of obscure, surprising, and verifiable science facts — the kind that make you go "wait, really?"

## Examples

> The mantis shrimp's punch accelerates faster than a bullet and generates cavitation bubbles that reach temperatures close to the sun's surface.

> Tardigrades survived 10 days of exposure to the vacuum of space, cosmic radiation, and extreme temperatures aboard a European Space Agency satellite.

> The peacock uses infrasound in its mating display, producing frequencies humans cannot hear but which may be felt by potential mates.

> Human trafficking generates an estimated $150 billion per year globally, more than the GDP of most countries, with 25 million victims worldwide.

> Coffee was supposedly discovered when Ethiopian goatherds noticed their goats acting energetic after eating coffee berries.

## What's in here

**10,003 facts** across 32 categories — everything from quantum physics to parasites to the history of food.

| Category | Facts | What it covers |
|----------|-------|----------------|
| microbiology | 865 | Bacteria, viruses, parasites, pathogens |
| biology | 860 | Animals, weird creatures, animal behavior |
| astronomy | 613 | Space, stars, planets, cosmology |
| computer_science | 524 | Algorithms, computing history, AI |
| botany | 514 | Plants, trees, fungi |
| paleontology | 489 | Dinosaurs, fossils, ancient life |
| earth_science | 487 | Geology, geography, glaciers |
| food_science | 476 | Cooking chemistry, nutrition facts |
| linguistics | 469 | Languages, etymology, writing systems |
| marine_biology | 407 | Ocean creatures, deep sea |
| chemistry | 396 | Elements, materials, reactions |
| entomology | 372 | Insects (they deserve their own category) |
| economics | 359 | Game theory, behavioral economics |
| weather | 305 | Extreme weather, climate |
| inventions | 282 | Discoveries, accidental inventions |
| human_body | 278 | Anatomy, weird body facts |
| forensics | 230 | Crime science, investigation |
| music | 219 | Acoustics, sound, instruments |
| physics | 215 | Quantum mechanics, optics |
| sleep | 210 | Dreams, circadian rhythms |
| + 12 more... | | |

## Files

```
facts.json              → all 10,003 facts
categories/astronomy.json    → just astronomy facts
categories/biology.json      → just biology facts
...
```

Each fact looks like:
```json
{
  "text": "The actual fact text here.",
  "source": "https://where-it-came-from.com",
  "original_category": "the_original_category"
}
```

## Sources

Facts were gathered from:
- Wikipedia "Did You Know" archives
- Wikidata queries
- Reddit r/todayilearned (top posts)
- Academic sources and science news

All facts are sourced and verifiable — no LLM hallucinations here.

## License

MIT — do whatever you want with it.
