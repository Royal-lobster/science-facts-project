# Science Facts Project

A collection of 10,001 obscure, verifiable science facts.

## Project Structure

```
science-facts-project/
├── README.md              # This file
├── schema.json            # Fact data schema
├── scripts/               # Python scripts for scraping/processing
├── data/
│   ├── raw/              # Raw facts by source (wikipedia, wikidata, etc.)
│   ├── intermediate/     # Processing stages, batch outputs
│   └── final/            # Final curated datasets
├── archive/              # Rejected/duplicate facts
└── logs/                 # Agent status logs
```

## Final Outputs

- `data/final/final_10001_facts.json` - The complete 10,001 facts
- `data/final/quality_facts.json` - Quality-filtered subset
- `data/final/final_facts.json` - Alternative final version

---

# Original Plan

## Philosophy
- **LLMs for formatting, not fabrication** — source facts from existing verified datasets
- **Parallel execution** — multiple sub-agents working on different categories/sources
- **Quality > Quantity** — maintain "genuinely obscure, counterintuitive, verifiable" bar

---

## Phase 1: Data Sources Research

### High-Quality Fact Sources
| Source | Type | Notes |
|--------|------|-------|
| Wikipedia "Did You Know" | Curated facts | ~8000+ archived facts, human-vetted |
| Reddit r/todayilearned | Crowdsourced | Top posts require sources |
| Wikidata | Structured | Query for unusual properties |
| NASA/NOAA/NIH fact sheets | Official | Government science agencies |
| arXiv abstracts | Academic | Recent discoveries |
| Nature/Science "News" | Journalism | Breakthrough summaries |
| QI (Quite Interesting) archives | Curated | Famous for obscure facts |
| Mental Floss / Atlas Obscura | Editorial | Pre-vetted unusual facts |
| Snopes "True" facts | Verified | Already fact-checked |
| Academic "fun facts" compilations | Papers | Scientists love trivia |

### Potential APIs/Datasets
- Wikipedia API (DYK archives)
- Pushshift/Reddit API (top r/todayilearned)
- Wikidata SPARQL queries
- Open Trivia Database
- Kaggle science datasets

---

## Phase 2: Category Expansion

### Current Categories (15)
physics_quantum_mechanics, biology_strange_creatures, chemistry_materials, 
neuroscience_brain, medicine_human_body, astronomy_space, geology_earth_science,
oceanography_marine, mathematics_logic, psychology_cognition, serendipitous_discoveries,
genetics_evolution, ecology_environment, technology_engineering, archaeology_history_of_science

### Proposed New Categories (~15-20 more)
| Category | Target Facts | Notes |
|----------|--------------|-------|
| computer_science_information | 400+ | Algorithms, complexity, crypto |
| linguistics_language | 300+ | Etymology, phonetics, writing systems |
| microbiology_pathogens | 400+ | Bacteria, viruses, fungi, prions |
| botany_plants | 350+ | Plant behavior, evolution, chemistry |
| entomology_insects | 300+ | Insect-specific (huge diversity) |
| paleontology_fossils | 350+ | Dinosaurs, ancient life, mass extinctions |
| climatology_weather | 300+ | Extreme weather, climate history |
| food_science_nutrition | 300+ | Cooking chemistry, metabolism |
| music_acoustics | 250+ | Sound physics, perception, instruments |
| economics_game_theory | 250+ | Paradoxes, behavioral economics |
| sleep_dreams | 200+ | Sleep science, circadian, dreams |
| optics_light | 250+ | Vision, colors, optical phenomena |
| anthropology_culture | 300+ | Human societies, rituals, universals |
| parasitology | 200+ | Parasites deserve their own category |
| materials_science | 300+ | Beyond chemistry - metamaterials, alloys |
| forensics_crime_science | 250+ | CSI-style science |
| sports_biomechanics | 200+ | Athletic performance, records |
| veterinary_animal_medicine | 200+ | Animal-specific medical facts |

### Target Distribution (~10001 total)
- Expand existing categories: ~5000 facts (avg ~333 per category)
- New categories: ~5000 facts (avg ~250-300 per category)

---

## Phase 3: Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     COORDINATOR (main session)                   │
│  - Assigns tasks to sub-agents                                  │
│  - Merges results                                               │
│  - Deduplicates (semantic similarity)                           │
│  - Quality review                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ SOURCE AGENT  │     │ SOURCE AGENT  │     │ SOURCE AGENT  │
│ (Wikipedia)   │     │ (Reddit TIL)  │     │ (Wikidata)    │
│               │     │               │     │               │
│ 1. Scrape     │     │ 1. Scrape     │     │ 1. Query      │
│ 2. Extract    │     │ 2. Extract    │     │ 2. Extract    │
│ 3. Format     │     │ 3. Format     │     │ 3. Format     │
│ 4. Categorize │     │ 4. Categorize │     │ 4. Categorize │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  facts_raw/*.json │
                    │  (per-source)     │
                    └───────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  MERGE & DEDUPE   │
                    │  - Semantic hash  │
                    │  - Remove dupes   │
                    │  - Quality filter │
                    └───────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  facts.json       │
                    │  (final 10001)    │
                    └───────────────────┘
```

---

## Phase 4: Sub-Agent Tasks

### Source Agents (parallel)
Each agent works independently on one source:

1. **Wikipedia DYK Agent**
   - Scrape "Did You Know" archives (2004-present)
   - Extract facts, reformat to our style
   - Target: 2000+ facts

2. **Reddit TIL Agent**
   - Top posts from r/todayilearned (all time + yearly)
   - Filter for science-related
   - Target: 1500+ facts

3. **Wikidata Query Agent**
   - SPARQL queries for unusual records/properties
   - "Longest", "smallest", "only", "first" etc.
   - Target: 1000+ facts

4. **Academic Trivia Agent**
   - Search for "fun facts" + "[field]" papers
   - Science communication articles
   - Target: 1000+ facts

5. **Government Science Agent**
   - NASA, NOAA, NIH, USGS fact pages
   - Target: 500+ facts

6. **Existing Compilations Agent**
   - QI, Mental Floss, Atlas Obscura archives
   - Target: 1500+ facts

### Category Expansion Agents (parallel)
For new categories, dedicated research:

7. **Computer Science Agent** — Target: 400 facts
8. **Linguistics Agent** — Target: 300 facts
9. **Microbiology Agent** — Target: 400 facts
10. **Botany Agent** — Target: 350 facts
... (one per new category)

---

## Phase 5: LLM Usage Rules

### ✅ LLMs CAN:
- Reformat raw facts into consistent style
- Categorize facts into appropriate categories
- Check for near-duplicates (semantic similarity)
- Summarize long facts into punchy one-liners
- Identify which facts meet "obscure" threshold

### ❌ LLMs CANNOT:
- Generate facts from scratch
- Fill in missing details
- "Enhance" facts with unverified additions
- Claim certainty about unverified claims

### Formatting Prompt Template
```
Given this raw fact from [SOURCE]:
"[RAW_FACT]"

Reformat to match this style (punchy, specific, surprising):
- "Tardigrades survived exposure to space vacuum, intense radiation, and temperatures from -272°C to 150°C."
- "The mantis shrimp's punch accelerates faster than a bullet and generates cavitation bubbles reaching sun-surface temperatures."

Rules:
- Keep all specific numbers/names from original
- Don't add information not in the source
- Make it one sentence if possible
- End with period, no em-dash unless adding context
```

---

## Phase 6: Quality Criteria

A fact passes if it meets ALL:
1. **Verifiable** — Has a source (we track provenance)
2. **Specific** — Contains concrete details (numbers, names, dates)
3. **Surprising** — Not common knowledge (passes "dinner party test")
4. **Accurate** — Matches scientific consensus (no fringe claims)
5. **Unique** — Not a duplicate or near-duplicate of existing fact

---

## Phase 7: Execution Order

### Day 1: Research & Setup
- [ ] Test data source accessibility
- [ ] Write scraping scripts for each source
- [ ] Set up output directories
- [ ] Create fact schema with provenance tracking

### Day 2-3: Parallel Extraction
- [ ] Spawn source agents (6 parallel)
- [ ] Each outputs to `facts_raw/{source}.json`
- [ ] Progress tracking

### Day 4: Merge & Quality
- [ ] Combine all raw facts
- [ ] Deduplicate (semantic + exact)
- [ ] Quality filter
- [ ] Manual review of edge cases

### Day 5: Final Assembly
- [ ] Categorize all facts
- [ ] Balance category distribution
- [ ] Generate final facts.json
- [ ] Update counts and metadata

---

## File Structure

```
/root/clawd/projects/science-facts/
├── PLAN.md                 # This file
├── facts.json              # Current 1001 facts (source of truth)
├── facts_10001.json        # Final expanded version
├── scripts/
│   ├── scrape_wikipedia_dyk.py
│   ├── scrape_reddit_til.py
│   ├── query_wikidata.py
│   └── format_facts.py
├── facts_raw/
│   ├── wikipedia_dyk.json
│   ├── reddit_til.json
│   ├── wikidata.json
│   └── ...
└── logs/
    └── agent_progress.md
```

---

## Questions Before Starting

1. **Scope confirmation**: 10001 total or 10001 *new* (so 11001 total)?
2. **Timeline**: Any deadline, or quality over speed?
3. **New categories**: Approve proposed list or modify?
4. **Provenance**: Track source URL per fact? (Adds complexity but enables verification)
5. **Review process**: Want to approve batches, or trust the pipeline?

---

*Ready to execute on your go.*
