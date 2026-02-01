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

<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/microscope_1f52c.png" width="100" />
</p>

<h1 align="center">Science Facts</h1>

<p align="center">
  <strong>10,000 obscure, surprising, and verifiable science facts</strong><br/>
  The kind that make you go "wait, really?"
</p>

---

## 🤔 What is this?

A curated dataset of **10,003 science facts** across 32 categories — from quantum physics to parasites to the history of food.

Every fact is:
- **Sourced** — from Wikipedia, Wikidata, academic sources
- **Verifiable** — no LLM hallucinations
- **Surprising** — passes the "dinner party test"

---

## ✨ Examples

> The mantis shrimp's punch accelerates faster than a bullet and generates cavitation bubbles that reach temperatures close to the sun's surface.

> Tardigrades survived 10 days of exposure to the vacuum of space, cosmic radiation, and extreme temperatures aboard a European Space Agency satellite.

> The peacock uses infrasound in its mating display, producing frequencies humans cannot hear but which may be felt by potential mates.

> Coffee was supposedly discovered when Ethiopian goatherds noticed their goats acting energetic after eating coffee berries.

---

## 📊 Categories

| Category | Count | What's inside |
|----------|------:|---------------|
| 🦠 microbiology | 865 | Bacteria, viruses, parasites |
| 🐾 biology | 860 | Animals, weird creatures |
| 🌌 astronomy | 613 | Space, stars, planets |
| 💻 computer_science | 524 | Algorithms, computing history |
| 🌿 botany | 514 | Plants, trees, fungi |
| 🦴 paleontology | 489 | Dinosaurs, fossils |
| 🌍 earth_science | 487 | Geology, geography |
| 🍳 food_science | 476 | Cooking chemistry, nutrition |
| 🗣️ linguistics | 469 | Languages, etymology |
| 🐠 marine_biology | 407 | Ocean creatures |
| ⚗️ chemistry | 396 | Elements, materials |
| 🐛 entomology | 372 | Insects |
| 📈 economics | 359 | Game theory |
| 🌦️ weather | 305 | Extreme weather, climate |
| 💡 inventions | 282 | Discoveries, accidents |
| 🫀 human_body | 278 | Anatomy, weird body facts |
| 🔍 forensics | 230 | Crime science |
| 🎵 music | 219 | Acoustics, sound |
| ⚛️ physics | 215 | Quantum mechanics |
| 😴 sleep | 210 | Dreams, circadian rhythms |
| *+ 12 more...* | | |

---

## 📁 Files

```
facts.json                    # All 10,003 facts
categories/
├── astronomy.json            # 613 facts
├── biology.json              # 860 facts
├── chemistry.json            # 396 facts
└── ...                       # 32 categories total
```

---

## 🔧 Usage

```python
import json

# Load everything
with open('facts.json') as f:
    facts = json.load(f)

# Load a specific category
with open('categories/astronomy.json') as f:
    space_facts = json.load(f)

# Each fact
{
  "text": "The actual fact here.",
  "source": "https://source-url.com",
  "original_category": "astronomy"
}
```

---

## 📚 Sources

- Wikipedia "Did You Know" archives
- Wikidata SPARQL queries
- Reddit r/todayilearned (top posts)
- Academic and science news sources

---

## 📝 License

MIT — do whatever you want with it.

---

<div align="center">

**Built for curious minds 🧠**

</div>
