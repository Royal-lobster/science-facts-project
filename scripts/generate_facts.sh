#!/bin/bash
# Generate facts using Claude CLI in parallel

OUTPUT_DIR="/root/clawd/projects/science-facts/generated"
mkdir -p "$OUTPUT_DIR"

generate_category() {
    local category="$1"
    local count="$2"
    local output_file="$OUTPUT_DIR/${category}.json"
    
    echo "Generating $count facts for: $category"
    
    claude -p "Generate exactly $count unique, mind-blowing science facts about $category. 

Requirements:
- Each fact must be surprising, counterintuitive, or awe-inspiring
- Include specific numbers, dates, or measurements when possible
- No boring statistics like 'X weighs Y' or 'Z is N meters tall'
- Each fact should make someone say 'wow, I didn't know that!'
- Vary the topics within the category

Output as a JSON array of objects with 'text' and 'category' fields.
Example format:
[
  {\"text\": \"Octopuses have three hearts and blue blood because...\", \"category\": \"marine_biology\"},
  ...
]

Output ONLY the JSON array, no other text." --output-format json 2>/dev/null | jq '.' > "$output_file" 2>/dev/null
    
    if [ -s "$output_file" ]; then
        local fact_count=$(jq 'length' "$output_file" 2>/dev/null || echo 0)
        echo "  Generated $fact_count facts for $category"
    else
        echo "  Failed for $category, trying text extraction..."
        # Fallback: try without json output format
        claude -p "Generate exactly $count unique, mind-blowing science facts about $category. Each fact should be surprising and awe-inspiring. Output as JSON array with 'text' and 'category' fields only." 2>/dev/null > "$output_file.txt"
    fi
}

# Categories to generate (targeting ~3500 total new facts)
# Running in parallel batches

echo "=== Batch 1: Core science ==="
generate_category "quantum_physics_paradoxes_and_weird_phenomena" 150 &
generate_category "space_astronomy_black_holes_stars_universe" 150 &
generate_category "human_body_anatomy_surprising_facts" 150 &
generate_category "chemistry_elements_reactions_explosions" 150 &
wait

echo "=== Batch 2: Biology ==="
generate_category "deep_sea_creatures_ocean_mysteries" 150 &
generate_category "animal_intelligence_behavior_superpowers" 150 &
generate_category "insects_arachnids_amazing_abilities" 150 &
generate_category "plants_fungi_botanical_wonders" 150 &
wait

echo "=== Batch 3: Earth & History ==="
generate_category "geology_volcanoes_earthquakes_crystals" 150 &
generate_category "weather_climate_extreme_phenomena" 150 &
generate_category "history_of_science_discoveries_accidents" 150 &
generate_category "mathematics_paradoxes_infinity_patterns" 150 &
wait

echo "=== Batch 4: Tech & Psychology ==="
generate_category "technology_inventions_engineering_marvels" 150 &
generate_category "psychology_brain_consciousness_perception" 150 &
generate_category "medicine_diseases_cures_human_health" 150 &
generate_category "evolution_genetics_dna_mutations" 150 &
wait

echo "=== Batch 5: More categories ==="
generate_category "prehistoric_life_dinosaurs_extinction" 150 &
generate_category "viruses_bacteria_microbes_epidemics" 150 &
generate_category "sound_light_waves_physics_phenomena" 150 &
generate_category "food_science_cooking_chemistry" 150 &
wait

echo "=== Batch 6: Miscellaneous ==="
generate_category "sleep_dreams_consciousness" 100 &
generate_category "language_linguistics_communication" 100 &
generate_category "materials_nanotechnology_supermaterials" 100 &
generate_category "renewable_energy_future_technology" 100 &
wait

echo "=== Done! ==="
ls -la "$OUTPUT_DIR"
