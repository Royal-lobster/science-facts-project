#!/usr/bin/env python3
"""Generate large batches of facts to reach 10,001 target."""

import json
from pathlib import Path

OUTPUT_DIR = Path("/root/clawd/projects/science-facts/generated")

# Mega fact list - covering many categories
MEGA_FACTS = [
    # Ancient History
    {"text": "The ancient Egyptians used mashed brains as a contraceptive.", "category": "history"},
    {"text": "Romans used crushed mouse brains as toothpaste.", "category": "history"},
    {"text": "Cleopatra spoke nine languages and was the first Ptolemaic ruler to learn Egyptian.", "category": "history"},
    {"text": "The Library of Alexandria may have contained 400,000 to 700,000 scrolls.", "category": "history"},
    {"text": "Ancient Greek statues were originally painted in bright colors.", "category": "history"},
    {"text": "Vikings used the bones of slain animals as skates.", "category": "history"},
    {"text": "The Aztecs used cacao beans as currency.", "category": "history"},
    {"text": "Ancient Babylonians were doing trigonometry 1,000 years before Pythagoras.", "category": "history"},
    {"text": "The ancient Greeks had a word, 'akrasia,' for acting against your better judgment.", "category": "linguistics"},
    {"text": "Mummies have been found with cocaine and tobacco traces, suggesting pre-Columbian trade routes.", "category": "history"},
    
    # Weather & Climate
    {"text": "Lightning strikes the Earth about 100 times per second.", "category": "meteorology"},
    {"text": "The coldest temperature ever recorded on Earth was -128.6°F in Antarctica.", "category": "meteorology"},
    {"text": "A hurricane releases as much energy as 10,000 nuclear bombs.", "category": "meteorology"},
    {"text": "Snow can fall from a cloudless sky in a phenomenon called 'diamond dust.'", "category": "meteorology"},
    {"text": "Ball lightning remains unexplained by science despite centuries of reports.", "category": "meteorology"},
    {"text": "The wind on Neptune can reach 1,200 mph — the fastest in the Solar System.", "category": "astronomy"},
    {"text": "A single lightning bolt can heat the air to 30,000 Kelvin — 5 times hotter than the Sun's surface.", "category": "meteorology"},
    {"text": "Clouds can weigh over a million pounds.", "category": "meteorology"},
    {"text": "Raindrops are not teardrop-shaped — they're flat on the bottom and rounded on top.", "category": "meteorology"},
    {"text": "Fire rainbows are actually ice crystal halos that appear in cirrus clouds.", "category": "meteorology"},
    
    # Weird Biology
    {"text": "Jellyfish are 95% water and have no brain, heart, or blood.", "category": "biology"},
    {"text": "A slug has four noses — two for smelling and two for detecting moisture.", "category": "biology"},
    {"text": "Lobsters pee out of their faces — they have urine-release nozzles under their eyes.", "category": "marine_biology"},
    {"text": "Frogs can't swallow with their eyes open — they use their eyes to push food down.", "category": "herpetology"},
    {"text": "Turtles can breathe through their butts.", "category": "herpetology"},
    {"text": "Flamingos are born with gray feathers that turn pink from their diet.", "category": "ornithology"},
    {"text": "Owls can't move their eyeballs — that's why they rotate their heads up to 270 degrees.", "category": "ornithology"},
    {"text": "Hummingbirds are the only birds that can fly backwards.", "category": "ornithology"},
    {"text": "Cuttlefish are colorblind but can produce over 1,000 color patterns.", "category": "marine_biology"},
    {"text": "The paradoxical frog grows smaller as it matures — tadpoles are 3 times larger than adults.", "category": "herpetology"},
    
    # Human Records
    {"text": "The longest hiccuping spree lasted 68 years.", "category": "human_body"},
    {"text": "The world's loudest burp measured 109.9 decibels — louder than a motorcycle.", "category": "human_body"},
    {"text": "The longest fingernails ever were over 28 feet combined.", "category": "human_body"},
    {"text": "The fastest sneeze on record traveled at 102 mph.", "category": "human_body"},
    {"text": "The longest time a person has held their breath underwater is 24 minutes.", "category": "human_body"},
    {"text": "The tallest person ever recorded was Robert Wadlow at 8 feet 11 inches.", "category": "human_body"},
    {"text": "The oldest verified person lived to 122 years and 164 days.", "category": "human_body"},
    {"text": "The human body can survive about 3 minutes without oxygen, 3 days without water, and 3 weeks without food.", "category": "human_body"},
    {"text": "The longest time between twins being born is 87 days apart.", "category": "human_body"},
    {"text": "The average person will walk about 100,000 miles in their lifetime.", "category": "human_body"},
    
    # Strange Laws of Physics
    {"text": "If you spin a ball when you drop it, it falls in a curved path (the Magnus effect).", "category": "physics"},
    {"text": "Water can boil and freeze at the same time at the right temperature and pressure.", "category": "physics"},
    {"text": "Quantum entanglement allows particles to communicate instantaneously across any distance.", "category": "physics"},
    {"text": "Time stops at the event horizon of a black hole from an outside observer's perspective.", "category": "physics"},
    {"text": "Electrons can exist in two places at once until observed.", "category": "physics"},
    {"text": "Empty space isn't empty — virtual particles pop in and out of existence constantly.", "category": "physics"},
    {"text": "The act of observation changes the behavior of particles at the quantum level.", "category": "physics"},
    {"text": "Antimatter is the most expensive substance — $62.5 trillion per gram to produce.", "category": "physics"},
    {"text": "Tachyons are theoretical particles that move faster than light and go backwards in time.", "category": "physics"},
    {"text": "If the electromagnetic force were slightly weaker, atoms couldn't form.", "category": "physics"},
    
    # Medicine Oddities
    {"text": "Doctors used to taste urine to diagnose diabetes — sweet urine indicated the disease.", "category": "medicine"},
    {"text": "Maggot therapy is FDA-approved and used to clean wounds.", "category": "medicine"},
    {"text": "Leech therapy is still used in modern medicine after reattachment surgeries.", "category": "medicine"},
    {"text": "Bee venom is being researched as a treatment for HIV.", "category": "medicine"},
    {"text": "Hookworm therapy is used to treat autoimmune diseases.", "category": "medicine"},
    {"text": "Fecal transplants can cure C. difficile infections with a 90% success rate.", "category": "medicine"},
    {"text": "The placebo effect works on animals and even operates on organs.", "category": "medicine"},
    {"text": "Blue dye from M&Ms may help spinal cord injuries.", "category": "medicine"},
    {"text": "A woman had a tumor that grew teeth and hair — a teratoma.", "category": "medicine"},
    {"text": "Phineas Gage survived having an iron rod shot through his brain, changing his personality.", "category": "neuroscience"},
    
    # Language & Communication
    {"text": "The word 'set' has the most definitions in the English dictionary — over 430.", "category": "linguistics"},
    {"text": "'Ghoti' can be pronounced as 'fish' using English phonetics.", "category": "linguistics"},
    {"text": "There's no word for 'yes' or 'no' in the Irish language.", "category": "linguistics"},
    {"text": "Esperanto is the most spoken constructed language, with about 2 million speakers.", "category": "linguistics"},
    {"text": "The Hawaiian alphabet has only 12 letters.", "category": "linguistics"},
    {"text": "The shortest complete sentence in English is 'Go.'", "category": "linguistics"},
    {"text": "The word 'bookkeeper' is the only word with three consecutive double letters.", "category": "linguistics"},
    {"text": "The word 'swims' reads the same upside down.", "category": "linguistics"},
    {"text": "The dot over 'i' and 'j' is called a tittle.", "category": "linguistics"},
    {"text": "The ampersand was once the 27th letter of the English alphabet.", "category": "linguistics"},
    
    # Tech & Internet
    {"text": "The first website ever created is still online: info.cern.ch.", "category": "technology"},
    {"text": "The first YouTube video was uploaded on April 23, 2005.", "category": "technology"},
    {"text": "Email existed before the World Wide Web.", "category": "technology"},
    {"text": "The first computer mouse was made of wood.", "category": "technology"},
    {"text": "The QWERTY keyboard was designed to slow typists down to prevent typewriter jams.", "category": "technology"},
    {"text": "The first emoji was created in 1999 by a Japanese artist.", "category": "technology"},
    {"text": "Google's name comes from 'googol' — the number 1 followed by 100 zeros.", "category": "technology"},
    {"text": "The first webcam watched a coffee pot at Cambridge University.", "category": "technology"},
    {"text": "The first text message said 'Merry Christmas.'", "category": "technology"},
    {"text": "The inventor of the web, Tim Berners-Lee, made it royalty-free for everyone.", "category": "technology"},
    
    # Money & Economics
    {"text": "There's more money in Monopoly than there is real US currency in circulation.", "category": "economics"},
    {"text": "The 100 trillion dollar bill is real — Zimbabwe printed it during hyperinflation.", "category": "economics"},
    {"text": "Pennies cost more to make than they're worth.", "category": "economics"},
    {"text": "Walt Disney was originally offered a deal that was worth $2 billion to create a theme park in Missouri.", "category": "economics"},
    {"text": "The inventor of the intermittent windshield wiper won $30 million from Ford for patent infringement.", "category": "economics"},
    {"text": "Apple has more money than the U.S. Treasury at times.", "category": "economics"},
    {"text": "The inventor of the Super Soaker was a NASA engineer.", "category": "inventions"},
    {"text": "The creator of the Rubik's Cube took over a month to solve it himself.", "category": "inventions"},
    {"text": "Bubble wrap was originally invented to be wallpaper.", "category": "inventions"},
    {"text": "Play-Doh was originally a wallpaper cleaner.", "category": "inventions"},
    
    # Random Absurdities  
    {"text": "A strawberry isn't a berry, but a banana is.", "category": "botany"},
    {"text": "Vending machines kill more people annually than sharks.", "category": "statistics"},
    {"text": "Cows have best friends and get stressed when separated.", "category": "zoology"},
    {"text": "A group of flamingos is called a 'flamboyance.'", "category": "zoology"},
    {"text": "Honey never expires — 3,000-year-old honey from Egyptian tombs was still edible.", "category": "food_science"},
    {"text": "There's a basketball court on the top floor of the U.S. Supreme Court building.", "category": "trivia"},
    {"text": "Bananas are radioactive.", "category": "physics"},
    {"text": "A jiffy is an actual unit of time — 1/100th of a second.", "category": "measurement"},
    {"text": "Nintendo was founded in 1889 as a playing card company.", "category": "history"},
    {"text": "There are more possible games of chess than atoms in the observable universe.", "category": "mathematics"},
    
    # More Biology
    {"text": "Sloths are so slow that algae grows on their fur.", "category": "zoology"},
    {"text": "Horses can't vomit due to a strong band of muscle around their esophagus.", "category": "zoology"},
    {"text": "Koalas and humans are the only animals with unique fingerprints.", "category": "zoology"},
    {"text": "A blue whale's tongue weighs as much as an elephant.", "category": "marine_biology"},
    {"text": "Butterflies taste with their feet.", "category": "entomology"},
    {"text": "Sea otters hold hands while sleeping so they don't drift apart.", "category": "marine_biology"},
    {"text": "A woodpecker's tongue wraps around its skull to cushion its brain.", "category": "ornithology"},
    {"text": "Immortal jellyfish can reverse their aging process indefinitely.", "category": "marine_biology"},
    {"text": "A cockroach can live for weeks without its head.", "category": "entomology"},
    {"text": "Electric eels can produce 860 volts of electricity.", "category": "marine_biology"},
    
    # More Chemistry
    {"text": "Diamond and graphite are both made of pure carbon but have completely different properties.", "category": "chemistry"},
    {"text": "Antimatter costs $62.5 trillion per gram to produce.", "category": "chemistry"},
    {"text": "The smell of rain is called petrichor and is caused by bacteria in the soil.", "category": "chemistry"},
    {"text": "Liquid oxygen is light blue in color.", "category": "chemistry"},
    {"text": "Gallium metal will melt in your hand because its melting point is 29.76°C.", "category": "chemistry"},
    {"text": "Astatine is so rare that less than 1 gram exists on Earth at any time.", "category": "chemistry"},
    {"text": "Glass is made primarily of sand (silicon dioxide).", "category": "chemistry"},
    {"text": "Helium is the only element that cannot freeze at normal pressure.", "category": "chemistry"},
    {"text": "Francium is so unstable that any visible amount would immediately vaporize from its own heat.", "category": "chemistry"},
    {"text": "Bromine and mercury are the only elements that are liquid at room temperature.", "category": "chemistry"},
    
    # More Space
    {"text": "The Sun makes up 99.86% of the Solar System's mass.", "category": "astronomy"},
    {"text": "If you shouted in space, no one would hear you because sound can't travel through vacuum.", "category": "physics"},
    {"text": "Astronauts can't cry properly in space because tears don't fall — they form blobs.", "category": "space"},
    {"text": "The International Space Station is the most expensive object ever built at $150 billion.", "category": "space"},
    {"text": "There's a planet where it rains glass sideways at 4,500 mph.", "category": "astronomy"},
    {"text": "Neutron stars spin up to 716 times per second.", "category": "astronomy"},
    {"text": "The largest volcano in the Solar System is on Mars — Olympus Mons.", "category": "astronomy"},
    {"text": "Venus spins backwards compared to other planets.", "category": "astronomy"},
    {"text": "There's more water on Jupiter's moon Europa than on Earth.", "category": "astronomy"},
    {"text": "The Sun will eventually become a white dwarf the size of Earth.", "category": "astronomy"},
    
    # Psychology Extras
    {"text": "The fear of long words is called hippopotomonstrosesquippedaliophobia.", "category": "psychology"},
    {"text": "The average person tells 4 lies per day.", "category": "psychology"},
    {"text": "People are more creative when they're tired.", "category": "psychology"},
    {"text": "Singing activates the same brain areas as drugs.", "category": "neuroscience"},
    {"text": "The brain can't feel pain because it has no pain receptors.", "category": "neuroscience"},
    {"text": "Nostalgia was once considered a mental illness.", "category": "psychology"},
    {"text": "The 'doorway effect' makes you forget why you entered a room.", "category": "psychology"},
    {"text": "People tend to remember incomplete tasks better than completed ones (Zeigarnik effect).", "category": "psychology"},
    {"text": "The smell of chocolate increases theta brain waves and relaxation.", "category": "neuroscience"},
    {"text": "Yawning is contagious even between humans and dogs.", "category": "psychology"},
    
    # More Earth Science
    {"text": "The deepest hole ever drilled is only 12 km deep — 0.2% of Earth's radius.", "category": "geology"},
    {"text": "Earth's core is as hot as the surface of the Sun.", "category": "geology"},
    {"text": "There are over 1 million earthquakes per year, most too small to feel.", "category": "geology"},
    {"text": "The Sahara was green with rivers and lakes just 6,000 years ago.", "category": "paleoclimate"},
    {"text": "Lightning strikes Earth about 8 million times per day.", "category": "meteorology"},
    {"text": "The Dead Sea is shrinking by about 3 feet per year.", "category": "geography"},
    {"text": "Mount Everest grows about 4mm per year due to tectonic forces.", "category": "geology"},
    {"text": "Antarctica contains 70% of Earth's fresh water.", "category": "geography"},
    {"text": "The Pacific Ocean is larger than all landmasses combined.", "category": "geography"},
    {"text": "There are more historical artifacts in the ocean than in all museums combined.", "category": "oceanography"},
    
    # More Technology
    {"text": "The first iPhone had less processing power than today's musical greeting cards.", "category": "technology"},
    {"text": "The Apollo 11 computer had less power than a modern calculator.", "category": "technology"},
    {"text": "The first commercial computer weighed 27 tons and cost $500,000.", "category": "technology"},
    {"text": "GPS satellites must account for Einstein's relativity or they'd be 10 km off daily.", "category": "technology"},
    {"text": "The first 1GB hard drive weighed 550 pounds and cost $40,000.", "category": "technology"},
    {"text": "WiFi was invented by an Australian radio astronomer.", "category": "technology"},
    {"text": "The first domain name ever registered was Symbolics.com in 1985.", "category": "technology"},
    {"text": "Nintendo's Game Boy survived a bombing in the Gulf War and still works.", "category": "technology"},
    {"text": "More people own cell phones than toothbrushes.", "category": "technology"},
    {"text": "The first alarm clock could only ring at 4 AM.", "category": "inventions"},
]

def main():
    output_file = OUTPUT_DIR / "batch_mega.json"
    
    with open(output_file, 'w') as f:
        json.dump(MEGA_FACTS, f, indent=2)
    
    print(f"Generated {len(MEGA_FACTS)} facts")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
