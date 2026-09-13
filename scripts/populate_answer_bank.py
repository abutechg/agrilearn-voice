import json

answer_bank = [
    # Maize & Cereals (001 - 015)
    {
        "id": "agri-001",
        "question": "How do I prepare my soil before planting maize?",
        "answer": "Clear the field, remove weeds, loosen the soil, and incorporate mature compost or manure. Ensure proper field drainage to prevent waterlogging.",
        "safetyNote": "Soil preparation depends on your local climate and soil texture."
    },
    {
        "id": "agri-002",
        "question": "When is the best time to plant maize?",
        "answer": "Plant maize at the onset of steady rains when soil moisture is sufficient and temperature is consistently above 15°C.",
        "safetyNote": "Avoid planting during dry spells unless supplemental irrigation is available."
    },
    {
        "id": "agri-003",
        "question": "How far apart should I plant maize seeds?",
        "answer": "Plant seeds 25–30 cm apart along rows, with rows spaced 75 cm apart, at a depth of 3–5 cm.",
        "safetyNote": "Spacing varies slightly depending on seed variety and machine or hand planting."
    },
    {
        "id": "agri-004",
        "question": "How do I control Fall Armyworm in maize?",
        "answer": "Inspect crops early, crush egg masses by hand, apply neem extract or biological agents like Bacillus thuringiensis, or use approved insecticides.",
        "safetyNote": "Follow pesticide label instructions strictly and wear protective gear."
    },
    {
        "id": "agri-005",
        "question": "How can I prevent mold and aflatoxin in stored maize?",
        "answer": "Harvest when fully mature, dry grains to below 13% moisture content, clean thoroughly, and store in airtight hermetic bags.",
        "safetyNote": "Aflatoxins are toxic to humans and animals; discard heavily molded grain."
    },
    {
        "id": "agri-006",
        "question": "How do I grow rice in lowland paddies?",
        "answer": "Puddle the soil, maintain controlled water levels of 5–10 cm after transplanting, and keep the field weed-free during early growth stages.",
        "safetyNote": "Proper water management helps suppress weeds and maximize yield."
    },
    {
        "id": "agri-007",
        "question": "What is the recommended spacing for upland rice?",
        "answer": "Sow seeds directly in rows 20 cm apart or space transplanted seedlings 20 cm by 20 cm in hills.",
        "safetyNote": "Maintain row uniformity to simplify manual or mechanical weeding."
    },
    {
        "id": "agri-008",
        "question": "How do I control Striga (witchweed) in sorghum and millet?",
        "answer": "Practice crop rotation with legumes like cowpea or groundnut, pull Striga plants before flowering, and use resistant crop varieties.",
        "safetyNote": "Striga seeds remain viable in soil for many years if allowed to set seed."
    },
    {
        "id": "agri-009",
        "question": "How do I fertilize maize organically?",
        "answer": "Apply well-rotted cattle or poultry manure during land preparation, and side-dress with liquid organic fertilizer or compost tea during mid-growth.",
        "safetyNote": "Ensure manure is fully composted to avoid burning plant roots."
    },
    {
        "id": "agri-010",
        "question": "Why are my maize leaves turning yellow?",
        "answer": "Yellowing lower leaves usually indicate Nitrogen deficiency, waterlogging, or root damage. Yellowing between veins may indicate Magnesium or Iron deficiency.",
        "safetyNote": "Inspect soil moisture and drainage before applying extra fertilizer."
    },
    {
        "id": "agri-011",
        "question": "How do I harvest and thresh sorghum?",
        "answer": "Harvest head clusters when grain is hard and dry, dry further on clean mats, and thresh by gentle beating or mechanical threshers.",
        "safetyNote": "Store threshed grain in moisture-proof containers."
    },
    {
        "id": "agri-012",
        "question": "How do I grow wheat in dry or semi-arid regions?",
        "answer": "Use short-duration, drought-tolerant varieties, irrigate during critical tillering and grain-filling stages, and practice conservation tillage.",
        "safetyNote": "Wheat requires cool night temperatures during early growth for good tillering."
    },
    {
        "id": "agri-013",
        "question": "What is system of rice intensification (SRI)?",
        "answer": "SRI involves transplanting young single seedlings at wider spacing, keeping soil moist but not flooded, and using organic soil enrichment.",
        "safetyNote": "SRI reduces seed and water requirements while increasing root growth."
    },
    {
        "id": "agri-014",
        "question": "How do I protect stored grains from grain borers and weevils?",
        "answer": "Use clean, airtight (hermetic) storage containers, add food-grade diatomaceous earth or inert dust, and keep storage areas cool and dry.",
        "safetyNote": "Inspect storage containers monthly for signs of pest activity."
    },
    {
        "id": "agri-015",
        "question": "How long does maize take from planting to harvest?",
        "answer": "Early-maturing varieties take 80–90 days, while medium to late varieties take 110–140 days depending on elevation and temperature.",
        "safetyNote": "Check cob husk browning and grain milk-line for exact maturity."
    },

    # Roots, Tubers & Plantain (016 - 030)
    {
        "id": "agri-016",
        "question": "How do I plant cassava cuttings?",
        "answer": "Select healthy 20–25 cm stems with at least 4–6 buds. Plant horizontally or vertically at a 45-degree angle in loose, well-drained soil.",
        "safetyNote": "Avoid cuttings from plants affected by Cassava Mosaic Disease."
    },
    {
        "id": "agri-017",
        "question": "How do I control Cassava Mosaic Disease?",
        "answer": "Plant virus-free disease-resistant varieties, rogue out infected plants early, and manage whitefly vector populations.",
        "safetyNote": "Destroy infected plants away from the field to prevent spread."
    },
    {
        "id": "agri-018",
        "question": "How do I prepare yam setts for planting?",
        "answer": "Cut clean seed yams into 200–300g pieces, treat cuts with wood ash or fungicide to prevent rot, and allow cuts to heal before planting on ridges or mounds.",
        "safetyNote": "Plant setts with the skin side facing outwards."
    },
    {
        "id": "agri-019",
        "question": "What is the best soil for sweet potatoes?",
        "answer": "Well-drained friable sandy loam soil rich in organic matter. Avoid heavy clay or overly fertile soils high in nitrogen which cause excess vine growth.",
        "safetyNote": "Excess nitrogen leads to large vines but small tubers."
    },
    {
        "id": "agri-020",
        "question": "How do I plant plantain suckers?",
        "answer": "Select healthy sword suckers, pare the corm to remove nematodes, dig holes 40x40x40 cm filled with topsoil and compost, and plant firmly.",
        "safetyNote": "Mulch around the base to retain soil moisture and suppress weeds."
    },
    {
        "id": "agri-021",
        "question": "How do I control potato late blight?",
        "answer": "Use certified disease-free seed, space plants for good airflow, avoid overhead watering, and apply preventive copper-based fungicides when conditions are wet.",
        "safetyNote": "Remove and burn infected leaves immediately."
    },
    {
        "id": "agri-022",
        "question": "How long does cassava take to mature?",
        "answer": "Early varieties mature in 9–12 months, while late-maturing industrial varieties take 12–18 months.",
        "safetyNote": "Leaving cassava in dry soil too long can make tubers woody."
    },
    {
        "id": "agri-023",
        "question": "How do I store harvested yam tubers?",
        "answer": "Store undamaged tubers in a shaded, well-ventilated traditional yam barn, tying tubers vertically on wooden frameworks.",
        "safetyNote": "Inspect regularly and remove any rotting tubers immediately."
    },
    {
        "id": "agri-024",
        "question": "How do I grow Irish potatoes from seed tubers?",
        "answer": "Sprout seed tubers in indirect light until green sprouts appear, then plant in ridges 30 cm apart and 10–15 cm deep.",
        "safetyNote": "Earth up soil around growing stems to cover expanding tubers from light."
    },
    {
        "id": "agri-025",
        "question": "What causes sweet potato weevil damage and how do I stop it?",
        "answer": "Weevils burrow into tubers causing bitter taste. Prevent by hilling up soil around roots, harvesting promptly, and rotating crops.",
        "safetyNote": "Discard infested tubers so weevils do not spread to storage."
    },
    {
        "id": "agri-026",
        "question": "How do I multiply cassava stems quickly?",
        "answer": "Use mini-cutting propagation techniques in nursery beds or plastic bags with high humidity to produce many sprouts from stem nodes.",
        "safetyNote": "Keep nursery soil moist and shaded."
    },
    {
        "id": "agri-027",
        "question": "How do I prevent banana bacterial wilt (BBW)?",
        "answer": "Remove male flowers with a wooden fork after the last hand opens, disinfect tools between plants with bleach or fire, and rogue infected mats.",
        "safetyNote": "Do not move planting materials from affected farms."
    },
    {
        "id": "agri-028",
        "question": "Why do yam tubers rot in the ground?",
        "answer": "Yam rot is caused by soil fungi, bacteria, or root-knot nematodes encouraged by waterlogged soil or unsterilized seed setts.",
        "safetyNote": "Plant on high ridges or mounds in well-drained soil."
    },
    {
        "id": "agri-029",
        "question": "How do I process cassava to remove cyanide safely?",
        "answer": "Peel, grate, ferment in bags under pressure for 2–3 days, and roast (gari) or dry thoroughly (fufu flour).",
        "safetyNote": "Proper fermentation and heat processing are required to eliminate hydrogen cyanide."
    },
    {
        "id": "agri-030",
        "question": "What fertilizer is best for yam production?",
        "answer": "Apply balanced NPK fertilizer (such as 15-15-15) 8–12 weeks after planting, followed by potassium-rich fertilizer to support tuber expansion.",
        "safetyNote": "Avoid excessive nitrogen which promotes leafy vines instead of large tubers."
    },

    # Vegetables & Horticulture (031 - 045)
    {
        "id": "agri-031",
        "question": "How do I start tomato seeds in a nursery?",
        "answer": "Sow seeds in shallow tray furrows with sterilised potting mix, cover lightly, water gently, and keep under 50% shade until germination.",
        "safetyNote": "Harden seedlings in full sun for 5–7 days before transplanting."
    },
    {
        "id": "agri-032",
        "question": "How do I control tomato yellow leaf curl virus?",
        "answer": "Manage whiteflies using yellow sticky traps, insect netting, neem oil spray, and plant resistant tomato varieties.",
        "safetyNote": "Remove infected seedling plants from nursery immediately."
    },
    {
        "id": "agri-033",
        "question": "How often should I water chili peppers?",
        "answer": "Water deeply 2–3 times a week depending on weather, keeping soil consistently moist but never waterlogged.",
        "safetyNote": "Irregular watering causes blossom end rot and flower drop."
    },
    {
        "id": "agri-034",
        "question": "What causes blossom end rot in tomatoes and peppers?",
        "answer": "Blossom end rot is caused by Calcium deficiency in developing fruit, often triggered by inconsistent watering or high soil salinity.",
        "safetyNote": "Maintain steady soil moisture and apply agricultural lime if soil is acidic."
    },
    {
        "id": "agri-035",
        "question": "How do I grow onions from seeds or sets?",
        "answer": "Plant onion sets or nursery seedlings in fertile, loose soil rich in organic matter, spaced 10 cm apart in rows 25 cm apart.",
        "safetyNote": "Keep onion beds free of weeds as onions compete poorly."
    },
    {
        "id": "agri-036",
        "question": "How do I control cabbage aphids naturally?",
        "answer": "Spray plants with soap-water solution, neem oil, or wood ash powder, and encourage natural predators like ladybird beetles.",
        "safetyNote": "Wash harvested produce thoroughly before consumption."
    },
    {
        "id": "agri-037",
        "question": "How do I stake tomato plants?",
        "answer": "Drive 1.5–2m wooden stakes next to plants at transplanting, and tie main stems loosely to stakes with twine as they grow.",
        "safetyNote": "Staking improves airflow, reduces fruit rot, and simplifies harvesting."
    },
    {
        "id": "agri-038",
        "question": "How do I grow leafy greens like spinach and amaranth?",
        "answer": "Broadcast or row-sow seeds in rich soil, water daily, thin crowded plants, and harvest outer leaves continuously.",
        "safetyNote": "Apply compost tea after partial harvests to boost regrowth."
    },
    {
        "id": "agri-039",
        "question": "How do I prevent damping-off in vegetable nurseries?",
        "answer": "Use clean well-drained seedling soil, avoid overwatering, maintain good ventilation, and sow seeds at recommended density.",
        "safetyNote": "Damping-off fungal spores thrive in cool, soggy nursery soil."
    },
    {
        "id": "agri-040",
        "question": "How do I grow okra successfully?",
        "answer": "Soak seeds overnight before planting, space 30–45 cm apart in full sun, and harvest pods every 2–3 days while young and tender.",
        "safetyNote": "Wear gloves during harvest to prevent skin irritation from pod hairs."
    },
    {
        "id": "agri-041",
        "question": "How do I control diamondback moth in cabbage and kale?",
        "answer": "Use crop rotation, intercrop with mustard or coriander, apply Bacillus thuringiensis (Bt), or use insect netting overhead.",
        "safetyNote": "Rotate chemical modes of action to prevent moth resistance."
    },
    {
        "id": "agri-042",
        "question": "What is crop pruning in tomatoes and cucumbers?",
        "answer": "Pruning involves removing side suckers (branches) below the first flower cluster to direct energy into fruit production.",
        "safetyNote": "Use clean blades to prevent transferring plant viruses."
    },
    {
        "id": "agri-043",
        "question": "How do I grow carrots in garden beds?",
        "answer": "Sow directly in deep, stone-free sandy soil, thin seedlings to 5 cm spacing, and keep soil evenly moist during germination.",
        "safetyNote": "Stony or hard soil causes cracked or misshapen carrot roots."
    },
    {
        "id": "agri-044",
        "question": "How do I grow watermelon for high sweetness?",
        "answer": "Provide full sun, warm sandy loam soil, generous watering during vegetative growth, and reduce watering as fruits mature to concentrate sugars.",
        "safetyNote": "Check tendril browning and hollow thumping sound for ripe harvest."
    },
    {
        "id": "agri-045",
        "question": "How do I manage cucumber powdery mildew?",
        "answer": "Space plants for ventilation, water at root level rather than leaves, and spray preventive baking soda or sulfur solution.",
        "safetyNote": "Avoid spraying sulfur in temperatures above 32°C."
    },

    # Legumes & Pulses (046 - 055)
    {
        "id": "agri-046",
        "question": "Why are cowpeas and beans good for soil health?",
        "answer": "Legumes form symbiotic relationships with Rhizobium bacteria to fix atmospheric nitrogen into the soil, reducing fertilizer needs.",
        "safetyNote": "Inoculating seeds with Rhizobium increases nitrogen fixation in new soils."
    },
    {
        "id": "agri-047",
        "question": "How do I control Maruca pod borers in cowpea?",
        "answer": "Plant early, intercrop with sorghum or maize, apply bio-pesticides at flowering stage, or spray recommended insecticides at peak bloom.",
        "safetyNote": "Inspect flower buds weekly to catch early infestations."
    },
    {
        "id": "agri-048",
        "question": "How do I grow groundnuts (peanuts)?",
        "answer": "Plant in light, well-drained sandy loam soil, weed early, earth up around plants during pegging, and avoid heavy nitrogen fertilizers.",
        "safetyNote": "Calcium (gypsum) at pegging prevents empty pods ('pops')."
    },
    {
        "id": "agri-049",
        "question": "How do I prevent Rosette virus in groundnuts?",
        "answer": "Plant early at close spacing to cover soil quickly, use aphid-resistant varieties, and rogue out diseased plants.",
        "safetyNote": "Rosette disease is transmitted by groundnut aphids."
    },
    {
        "id": "agri-050",
        "question": "How do I grow soybeans for high grain yield?",
        "answer": "Inoculate seed with specific Rhizobium, sow 3–5 cm deep in rows 45 cm apart, weed twice in early weeks, and harvest when pods turn brown.",
        "safetyNote": "Soybean pods shatter if left unharvested too long after drying."
    },
    {
        "id": "agri-051",
        "question": "How do I store cowpea seeds without weevil damage?",
        "answer": "Store dried seeds in hermetic bags (PICS bags), triple-bagging, or add clean ash/cooking oil to coat seed surfaces.",
        "safetyNote": "Ensure seed moisture is under 12% before hermetic sealing."
    },
    {
        "id": "agri-052",
        "question": "What is double-up legume intercropping?",
        "answer": "Planting two complementary legumes together (like pigeonpea and groundnut or cowpea) to maximize land productivity and nitrogen fixation.",
        "safetyNote": "Match maturity periods so one legume does not shade out the other."
    },
    {
        "id": "agri-053",
        "question": "How do I grow green grams (mung beans)?",
        "answer": "Sow in dry or semi-arid zones with light soils, space rows 30 cm apart, and harvest pods as they ripen and turn dark.",
        "safetyNote": "Green grams mature quickly (60–75 days) and require minimal rainfall."
    },
    {
        "id": "agri-054",
        "question": "Why do my bean flowers drop off without setting pods?",
        "answer": "Flower drop occurs due to extreme heat (>30°C), drought stress, thrips pest damage, or excess nitrogen fertilizer.",
        "safetyNote": "Provide mulching and light irrigation during hot dry snaps."
    },
    {
        "id": "agri-055",
        "question": "How do I harvest and cure groundnuts after pulling?",
        "answer": "Pull plants when pod inner shells turn brown/spotted, invert plants with pods facing up to sun-dry for 3–7 days, then pluck pods.",
        "safetyNote": "Do not leave pulled pods directly touching damp soil."
    },

    # Soil Health, Fertilizers & Organic Farming (056 - 070)
    {
        "id": "agri-056",
        "question": "How do I test my farm soil pH at home?",
        "answer": "Mix soil with distilled water and use digital pH meters or paper test strips. Soil pH 6.0–7.0 is ideal for most food crops.",
        "safetyNote": "For precise lime or fertilizer rates, send samples to a soil laboratory."
    },
    {
        "id": "agri-057",
        "question": "How do I correct acidic soil?",
        "answer": "Apply agricultural lime (calcium carbonate) or dolomitic lime based on soil test results, incorporating it 2–3 months before planting.",
        "safetyNote": "Over-liming can tie up essential micro-nutrients like zinc and iron."
    },
    {
        "id": "agri-058",
        "question": "What are cover crops and why should I plant them?",
        "answer": "Cover crops (like mucuna, lablab, or crotalaria) protect soil from erosion, suppress weeds, add organic matter, and improve water infiltration.",
        "safetyNote": "Terminate cover crops before they produce viable seeds."
    },
    {
        "id": "agri-059",
        "question": "How do I make high-quality compost tea?",
        "answer": "Steep mature compost in clean aerated water for 24–48 hours, strain liquid, and dilute to apply as a foliage spray or root drench.",
        "safetyNote": "Use compost tea within 4 hours of preparation."
    },
    {
        "id": "agri-060",
        "question": "What is crop rotation and what is the best sequence?",
        "answer": "Alternating different plant families each season (e.g., Legume -> Cereal -> Root Crop -> Leafy Vegetable) to break pest cycles and replenish nutrients.",
        "safetyNote": "Never follow crops of the same family (e.g., tomato after potato) in succession."
    },
    {
        "id": "agri-061",
        "question": "What is biochar and how does it help soil?",
        "answer": "Biochar is crushed charcoal produced from agricultural waste. Mixed into soil with compost, it holds water and nutrients for years.",
        "safetyNote": "Inoculate raw biochar with compost or manure before soil application."
    },
    {
        "id": "agri-062",
        "question": "What is minimum tillage (zero-till) farming?",
        "answer": "Disturbing soil only where seeds are placed, leaving crop residues on top to preserve soil structure, moisture, and beneficial organisms.",
        "safetyNote": "Weed management requires cover cropping, mulching, or targeted control in zero-till."
    },
    {
        "id": "agri-063",
        "question": "What is NPK fertilizer and what do the numbers mean?",
        "answer": "NPK stands for Nitrogen (leaves/stems), Phosphorus (roots/flowers), and Potassium (fruit/disease resistance). 15-15-15 contains equal parts of each.",
        "safetyNote": "Apply fertilizers based on crop growth stage and soil needs."
    },
    {
        "id": "agri-064",
        "question": "How do I make organic pesticide using neem leaves?",
        "answer": "Crush fresh neem leaves, soak in water for 24 hours, add a few drops of liquid soap as a sticker, strain, and spray on crop foliage.",
        "safetyNote": "Apply organic sprays during early morning or late evening."
    },
    {
        "id": "agri-065",
        "question": "How do I prevent soil erosion on sloping land?",
        "answer": "Construct contour bunds, plant vetiver grass hedgerows across slopes, use terracing, and maintain continuous organic soil cover.",
        "safetyNote": "Unprotected slopes lose topsoil rapidly during heavy rains."
    },
    {
        "id": "agri-066",
        "question": "What is green manure?",
        "answer": "Growing fast-growing leguminous crops and plowing them into the soil while green to decompose and enrich soil organic matter.",
        "safetyNote": "Plow in green manure 2–3 weeks before sowing the next crop."
    },
    {
        "id": "agri-067",
        "question": "How do I treat saline or salty soils?",
        "answer": "Improve subsoil drainage, flush soil with heavy applications of good quality water, and apply agricultural gypsum.",
        "safetyNote": "Avoid using salty irrigation water on affected fields."
    },
    {
        "id": "agri-068",
        "question": "Why is organic matter important in sandy soils?",
        "answer": "Organic matter acts like a sponge in sandy soil, holding water and dissolved plant nutrients that would otherwise wash away.",
        "safetyNote": "Apply compost annually as organic matter breaks down rapidly in hot climates."
    },
    {
        "id": "agri-069",
        "question": "What is vermicomposting?",
        "answer": "Using specialized earthworms (like Red Wigglers) to break down organic farm and kitchen waste into nutrient-rich worm castings.",
        "safetyNote": "Keep worm bins moist, shaded, and protected from ants and rodents."
    },
    {
        "id": "agri-070",
        "question": "How do I use wood ash in farming?",
        "answer": "Wood ash provides potassium and lime to raise acidic soil pH. It can also be sprinkled around plant bases to deter slugs and snails.",
        "safetyNote": "Do not apply wood ash around acid-loving crops or mix directly with nitrogen fertilizers."
    },

    # Irrigation & Water Management (071 - 080)
    {
        "id": "agri-071",
        "question": "What is drip irrigation and why is it efficient?",
        "answer": "Drip irrigation delivers water directly to plant roots through small tubes and emitters, saving 50–70% water compared to flooding.",
        "safetyNote": "Filter water source to prevent drip emitter clogging."
    },
    {
        "id": "agri-072",
        "question": "How do I build a simple rainwater harvesting system for my farm?",
        "answer": "Collect roof runoff into covered storage tanks, or dig contour trenches and farm ponds lined with clay or plastic tarps.",
        "safetyNote": "Keep water containers covered to prevent mosquito breeding."
    },
    {
        "id": "agri-073",
        "question": "What is mulching and how does it save water?",
        "answer": "Covering soil with dry straw, grass, or leaves reduces soil water evaporation, keeps soil cool, and prevents weed growth.",
        "safetyNote": "Keep mulch 5 cm away from main stems to avoid collar rot."
    },
    {
        "id": "agri-074",
        "question": "How do I know if I am overwatering my crops?",
        "answer": "Signs of overwatering include yellowing leaves, soft water-soaked stems, stunted growth, and green algae growth on soil surface.",
        "safetyNote": "Waterlogged roots suffocate from lack of soil oxygen."
    },
    {
        "id": "agri-075",
        "question": "What is furrow irrigation?",
        "answer": "Water is led down small shallow channels (furrows) created between crop ridges, soaking laterally into plant root zones.",
        "safetyNote": "Ensure gentle slope gradients to avoid furrow soil erosion."
    },
    {
        "id": "agri-076",
        "question": "How do I practice water harvesting with Zaï pits?",
        "answer": "Dig small pits (20–30 cm wide, 10–15 cm deep) filled with compost before rains to catch rainwater and concentrate nutrients for crops.",
        "safetyNote": "Zaï pits restore degraded, hard-baked dryland soils."
    },
    {
        "id": "agri-077",
        "question": "What is solar-powered irrigation?",
        "answer": "Using solar panels to power water pumps from wells or rivers into elevated storage tanks or drip lines without fuel costs.",
        "safetyNote": "Size solar pumps according to water table depth and daily water requirement."
    },
    {
        "id": "agri-078",
        "question": "How do I manage waterlogging after heavy flooding?",
        "answer": "Dig emergency drainage channels, clear blocked outlets, aerate wet soil once workable, and apply light nitrogen after water recedes.",
        "safetyNote": "Harvest submerged mature root crops quickly before rot sets in."
    },
    {
        "id": "agri-079",
        "question": "When is the best time of day to water plants?",
        "answer": "Early morning is best because roots absorb water before heat rises, and leaves dry quickly to discourage fungal diseases.",
        "safetyNote": "Avoid watering in mid-day heat or late evening."
    },
    {
        "id": "agri-080",
        "question": "What is subsurface drip irrigation?",
        "answer": "Burying drip lines 10–20 cm below soil surface to deliver water and nutrients directly to root zones with zero evaporation loss.",
        "safetyNote": "Requires high-grade filtration to avoid underground root intrusion."
    },

    # Tree Crops, Cash Crops & Agroforestry (081 - 090)
    {
        "id": "agri-081",
        "question": "How do I prune cocoa trees for maximum yield?",
        "answer": "Remove chupons (water shoots), dead or diseased branches, and thin interlocking canopy branches to allow sunlight and airflow.",
        "safetyNote": "Prune during dry periods to allow wounds to heal without fungal infection."
    },
    {
        "id": "agri-082",
        "question": "How do I control Black Pod Disease in cocoa?",
        "answer": "Harvest ripe pods promptly, remove infected pods every 2 weeks, improve canopy aeration, and apply copper fungicide sprays during rainy season.",
        "safetyNote": "Dispose of infected pod husks far from cocoa trees."
    },
    {
        "id": "agri-083",
        "question": "How do I plant oil palm seedlings?",
        "answer": "Dig 60x60x60 cm pits spaced 9 meters in a triangular pattern, fill with topsoil and compost, and plant healthy 12-month nursery seedlings.",
        "safetyNote": "Mulch around young palms to conserve moisture."
    },
    {
        "id": "agri-084",
        "question": "How do I manage cashew nut orchards?",
        "answer": "Space trees 9x9m, prune lower branches up to 1 meter height, weed canopy drip lines, and monitor for cashew stem borers.",
        "safetyNote": "Collect fallen ripe nuts promptly during harvest season."
    },
    {
        "id": "agri-085",
        "question": "What is agroforestry and how does it benefit smallholders?",
        "answer": "Integrating trees (like nitrogen-fixing Gliricidia or fruit trees) with food crops to provide shade, timber, fodder, and soil nutrients.",
        "safetyNote": "Select non-competitive tree species with deep root systems."
    },
    {
        "id": "agri-086",
        "question": "How do I grow coffee trees from nursery seedlings?",
        "answer": "Plant shade-grown seedlings in deep, acidic loam soil at 2x2m spacing, mulch heavily, and cap main stem to encourage lateral branching.",
        "safetyNote": "Control coffee leaf rust with resistant varieties and proper spacing."
    },
    {
        "id": "agri-087",
        "question": "How do I harvest and ferment cocoa beans properly?",
        "answer": "Extract beans within 5 days of harvesting pods, ferment in wooden boxes or leaf heaps for 5–7 days turning every 48 hours, then sun-dry.",
        "safetyNote": "Proper fermentation develops rich chocolate flavor precursor compounds."
    },
    {
        "id": "agri-088",
        "question": "How do I control mango fruit fly?",
        "answer": "Use protein bait traps, male annihilation technique (MAT) traps, collect and bury fallen fruits, and wrap developing fruits in bags.",
        "safetyNote": "Bury fallen infested fruits at least 50 cm underground."
    },
    {
        "id": "agri-089",
        "question": "How do I establish a citrus (orange/lemon) orchard?",
        "answer": "Plant grafted seedlings on disease-resistant rootstock spaced 6x6m in sunny well-drained soil, watering deeply during dry spells.",
        "safetyNote": "Inspect regularly for citrus greening vector (psyllids)."
    },
    {
        "id": "agri-090",
        "question": "How do I grow avocado trees from grafted nursery plants?",
        "answer": "Plant grafted varieties in elevated mounds of well-drained soil, protect young trees from wind, and avoid overwatering root zones.",
        "safetyNote": "Avocados are highly sensitive to root rot (Phytophthora) in waterlogged soil."
    },

    # Livestock, Poultry & Farm Management (091 - 100)
    {
        "id": "agri-091",
        "question": "How do I keep poultry (chickens) healthy organically?",
        "answer": "Provide clean dry bedding, fresh water daily, well-balanced feed, good ventilation, and natural additives like aloe vera or garlic in drinking water.",
        "safetyNote": "Follow standard vaccination schedules for Newcastle and Gumboro diseases."
    },
    {
        "id": "agri-092",
        "question": "How do I prepare a brooder house for newborn chicks?",
        "answer": "Disinfect house 7 days prior, lay clean wood shavings, pre-heat brooder area to 32–34°C 24 hours before chicks arrive, and provide warm sugar water.",
        "safetyNote": "Observe chick distribution: huddling near heat means too cold, spreading far means too hot."
    },
    {
        "id": "agri-093",
        "question": "How do I manage African Swine Fever (ASF) in pigs?",
        "answer": "Enforce strict biosecurity: restrict farm visitors, disinfect footwear and vehicles, never feed untreated restaurant waste (swill), and quarantine new stock.",
        "safetyNote": "ASF has no vaccine; biosecurity is the only defense."
    },
    {
        "id": "agri-094",
        "question": "How do I improve milk yield in dairy cows or goats?",
        "answer": "Provide continuous clean water, balanced energy-protein forage (legume hay), mineral licks, comfortable shaded housing, and regular deworming.",
        "safetyNote": "Ensure cows get clean drinking water available 24/7."
    },
    {
        "id": "agri-095",
        "question": "How do I start catfish or tilapia aquaculture in ponds?",
        "answer": "Construct well-drained earthen or concrete ponds, stock quality fingerlings from accredited hatcheries, maintain water oxygen, and feed high-protein floating pellets.",
        "safetyNote": "Monitor water quality (pH, ammonia, dissolved oxygen) weekly."
    },
    {
        "id": "agri-096",
        "question": "How do I prevent goat and sheep mortality during rainy season?",
        "answer": "Provide raised dry housing off damp ground, vaccinate against PPR (Peste des Petits Ruminants), and deworm regularly to control internal parasites.",
        "safetyNote": "Do not let goats graze wet morning pasture infested with worm larvae."
    },
    {
        "id": "agri-097",
        "question": "What is silvopasture?",
        "answer": "Integrating timber/fruit trees, forage grasses, and grazing livestock on the same land for multi-tier income and animal shade.",
        "safetyNote": "Protect young trees from livestock browsing until tall enough."
    },
    {
        "id": "agri-098",
        "question": "How do I make high-quality grass silage for dry season feeding?",
        "answer": "Chop green grass/maize at 60–65% moisture, pack tightly in pit or plastic bag to exclude air, seal completely, and ferment for 3–4 weeks.",
        "safetyNote": "Air exposure during storage causes silage spoilage and mold growth."
    },
    {
        "id": "agri-099",
        "question": "How do I control external parasites (ticks and lice) on cattle?",
        "answer": "Use rotational grazing, hand-pick ticks on small herds, apply pour-on acaricides or dip treatments according to recommended schedules.",
        "safetyNote": "Ticks transmit deadly blood diseases like East Coast Fever and Anaplasmosis."
    },
    {
        "id": "agri-100",
        "question": "What farm records should every smallholder farmer keep?",
        "answer": "Keep daily records of field activities, planting dates, input costs (seeds, fertilizer, labor), harvest yields, sales revenue, and livestock health events.",
        "safetyNote": "Record keeping reveals farm profitability and helps secure agricultural loans."
    }
]

with open("c:/Users/TAJUDEEN/Documents/New folder/sahara/benchmark/agriculture_answer_bank.json", "w", encoding="utf-8") as f:
    json.dump(answer_bank, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(answer_bank)} agricultural questions to answer bank.")
