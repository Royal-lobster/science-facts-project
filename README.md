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

# Science Facts Dataset

A curated collection of **10,003 obscure, verifiable science facts** across 32 categories.

## Dataset Description

Each fact is:
- **Verifiable** — sourced from Wikipedia, Wikidata, academic sources
- **Specific** — contains concrete details (numbers, names, dates)
- **Surprising** — not common knowledge

## Structure

```
science-facts/
├── facts.json           # All 10,003 facts
└── categories/          # Facts split by category
    ├── astronomy.json   # 613 facts
    ├── biology.json     # 860 facts
    ├── chemistry.json   # 396 facts
    └── ... (32 categories)
```

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| microbiology | 865 | Bacteria, viruses, parasites, pathogens |
| biology | 860 | Animals, zoology, animal behavior |
| astronomy | 613 | Space, cosmology, planets, stars |
| computer_science | 524 | Algorithms, computing history, information theory |
| botany | 514 | Plants, trees, fungi |
| paleontology | 489 | Fossils, dinosaurs, ancient life |
| earth_science | 487 | Geology, geography, glaciers |
| food_science | 476 | Cooking chemistry, nutrition |
| linguistics | 469 | Language, etymology, writing systems |
| marine_biology | 407 | Ocean life, fish, marine mammals |
| chemistry | 396 | Materials, reactions, elements |
| entomology | 372 | Insects |
| economics | 359 | Game theory, behavioral economics |
| trivia | 349 | Miscellaneous interesting facts |
| weather | 305 | Meteorology, climate, extreme weather |
| inventions | 282 | Discoveries, engineering, serendipity |
| human_body | 278 | Anatomy, physiology |
| history | 252 | Science history, archaeology |
| forensics | 230 | Crime science, investigation |
| music | 219 | Acoustics, sound, instruments |
| physics | 215 | Quantum mechanics, optics, energy |
| sleep | 210 | Sleep science, dreams, circadian rhythms |
| technology | 192 | Engineering, aviation, gadgets |
| genetics | 177 | DNA, evolution, heredity |
| neuroscience | 108 | Brain science |
| medicine | 90 | Medical facts, diseases |
| psychology | 66 | Cognitive science, behavior |
| mathematics | 62 | Numbers, logic, measurement |
| oceanography | 60 | Ocean science |
| architecture | 38 | Buildings, structures |
| other | 24 | Uncategorized |
| culture | 15 | Anthropology, philosophy |

## Fact Schema

```json
{
  "text": "The mantis shrimp's punch accelerates faster than a bullet...",
  "source": "https://en.wikipedia.org/wiki/Mantis_shrimp",
  "original_category": "marine_biology"
}
```

## Usage

```python
import json

# Load all facts
with open('facts.json') as f:
    facts = json.load(f)

# Load a specific category
with open('categories/astronomy.json') as f:
    astronomy_facts = json.load(f)
```

## License

MIT License

## Citation

```bibtex
@dataset{science_facts_2024,
  title={Science Facts Dataset},
  year={2024},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/datasets/Royal-lobster/science-facts}}
}
```
