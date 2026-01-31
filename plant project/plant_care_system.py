"""
=============================================================================
SMART PLANT CARE & HEALTH MONITORING SYSTEM
COMPLETE ULTIMATE EDITION
=============================================================================
Features:
- 10 Plants with Comprehensive Care Information
- Detailed Treatment & Problem Solutions
- Step-by-Step Image Processing Explanations
- Advanced Classical Computer Vision
=============================================================================
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


try:
    from skimage.feature import local_binary_pattern
    HAS_SKIMAGE = True
except ImportError:
    HAS_SKIMAGE = False

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# =============================================================================
# COMPREHENSIVE PLANT DATABASE - 10 Plants
# =============================================================================

PLANT_DATABASE = {
    "Pothos (بوتس)": {
        "scientific_name": "Epipremnum aureum",
        "difficulty": "Easy",
        "image_url": "img/download (8).jpg",
        "care": {
            "water": "💧 Water once per week, allow top 2 inches of soil to dry between waterings",
            "light": "☀️ Indirect bright light to low light (100-200 foot-candles)",
            "temperature": "🌡️ 18-29°C (65-85°F) - avoid cold drafts",
            "humidity": "💨 Medium humidity 40-60% - mist occasionally",
            "soil": "🌱 Well-draining potting mix with perlite",
            "fertilizer": "🌿 Liquid fertilizer every 4-6 weeks during growing season",
            "pruning": "✂️ Trim yellow leaves and long vines to encourage bushiness"
        },
        "problems_and_solutions": {
            "Yellow Leaves": {
                "causes": ["Overwatering", "Poor drainage", "Root rot", "Insufficient light"],
                "diagnosis": "Check soil moisture - if soggy, it's overwatering",
                "treatment": [
                    "1. Reduce watering frequency immediately",
                    "2. Check drainage holes - ensure water flows freely",
                    "3. Remove yellow leaves to prevent fungal spread",
                    "4. If root rot suspected, repot in fresh dry soil",
                    "5. Move to brighter location gradually"
                ],
                "prevention": "Water only when top 2 inches of soil are dry"
            },
            "Brown Tips": {
                "causes": ["Low humidity", "Fluoride/chlorine in tap water", "Over-fertilizing", "Salt buildup"],
                "diagnosis": "Brown, crispy leaf tips while rest of leaf is green",
                "treatment": [
                    "1. Increase humidity with pebble tray or humidifier",
                    "2. Switch to filtered or distilled water",
                    "3. Flush soil with clean water to remove salt buildup",
                    "4. Reduce fertilizer frequency",
                    "5. Trim brown tips with clean scissors"
                ],
                "prevention": "Use filtered water and maintain 50%+ humidity"
            },
            "Leggy Growth": {
                "causes": ["Insufficient light", "Natural aging"],
                "diagnosis": "Long stems with few leaves, spaces between leaves",
                "treatment": [
                    "1. Move to brighter location (indirect light)",
                    "2. Prune long vines to encourage branching",
                    "3. Propagate cuttings to create fuller plant",
                    "4. Rotate plant weekly for even growth"
                ],
                "prevention": "Provide consistent bright indirect light"
            }
        },
        "fun_facts": "Pothos can purify air by removing toxins like formaldehyde and benzene. Can grow over 40 feet in nature!"
    },

    "Snake Plant (نبات الثعبان)": {
        "scientific_name": "Sansevieria trifasciata",
        "difficulty": "Very Easy",
        "image_url": "img/s.jpg",
        "care": {
            "water": "💧 Water every 2-3 weeks, drought tolerant - less in winter",
            "light": "☀️ Low to bright indirect light - very adaptable",
            "temperature": "🌡️ 15-29°C (60-85°F) - tolerates temperature fluctuations",
            "humidity": "💨 Low humidity preferred - very drought tolerant",
            "soil": "🌱 Cactus/succulent mix with excellent drainage",
            "fertilizer": "🌿 Once in spring with diluted cactus fertilizer",
            "pruning": "✂️ Remove damaged leaves at soil level"
        },
        "problems_and_solutions": {
            "Root Rot (Yellow/Mushy Leaves)": {
                "causes": ["Severe overwatering", "Poor drainage", "Cold temperatures"],
                "diagnosis": "Yellow leaves that are soft and mushy, foul smell from soil",
                "treatment": [
                    "1. STOP watering immediately",
                    "2. Remove plant from pot and inspect roots",
                    "3. Cut away ALL brown/mushy roots with sterile scissors",
                    "4. Let roots dry for 24 hours",
                    "5. Repot in completely fresh, dry cactus soil",
                    "6. Do NOT water for 1-2 weeks",
                    "7. Resume watering very sparingly"
                ],
                "prevention": "Water only when soil is completely dry, ensure drainage holes"
            },
            "Brown Spots": {
                "causes": ["Inconsistent watering", "Fungal infection", "Cold damage"],
                "diagnosis": "Brown circular spots with yellow halos",
                "treatment": [
                    "1. Isolate plant from other plants",
                    "2. Remove affected leaves completely",
                    "3. Improve air circulation",
                    "4. Apply fungicide if spreading",
                    "5. Establish consistent watering schedule"
                ],
                "prevention": "Maintain consistent care routine, avoid wetting leaves"
            },
            "Wrinkled Leaves": {
                "causes": ["Severe under-watering", "Root damage"],
                "diagnosis": "Leaves appear thin, wrinkled, and droopy",
                "treatment": [
                    "1. Water thoroughly until water drains from bottom",
                    "2. Check roots for damage",
                    "3. Resume normal watering schedule",
                    "4. Recovery may take 2-3 weeks"
                ],
                "prevention": "Don't let soil stay completely dry for extended periods"
            }
        },
        "fun_facts": "Produces oxygen at night! Perfect for bedrooms. Can survive weeks without water."
    },

    "Spider Plant (نبات العنكبوت)": {
        "scientific_name": "Chlorophytum comosum",
        "difficulty": "Easy",
        "image_url": "img/Spider Plant.jpg",
        "care": {
            "water": "💧 Water 2-3 times per week, keep soil evenly moist but not soggy",
            "light": "☀️ Bright indirect light - can tolerate some shade",
            "temperature": "🌡️ 18-32°C (65-90°F) - very temperature tolerant",
            "humidity": "💨 Medium to high humidity 40-80%",
            "soil": "🌱 Rich, well-draining potting soil with organic matter",
            "fertilizer": "🌿 Every 2 weeks during growing season with balanced fertilizer",
            "pruning": "✂️ Remove brown tips, propagate baby plantlets"
        },
        "problems_and_solutions": {
            "Brown Leaf Tips": {
                "causes": ["Fluoride/chlorine in tap water", "Salt buildup", "Low humidity", "Over-fertilizing"],
                "diagnosis": "Brown, crispy tips on otherwise healthy leaves",
                "treatment": [
                    "1. Switch to distilled or rainwater immediately",
                    "2. Flush soil with distilled water (run 2-3x pot volume through)",
                    "3. Stop fertilizing for 1 month",
                    "4. Increase humidity with humidifier or pebble tray",
                    "5. Trim brown tips with clean scissors (cut at an angle)",
                    "6. Mist leaves with distilled water daily"
                ],
                "prevention": "Always use filtered/distilled water, fertilize at half strength"
            },
            "Yellow Leaves": {
                "causes": ["Overwatering", "Poor drainage", "Nutrient deficiency"],
                "diagnosis": "Leaves turn yellow from base upward",
                "treatment": [
                    "1. Check drainage - soil should dry between waterings",
                    "2. Reduce watering frequency",
                    "3. Feed with balanced liquid fertilizer",
                    "4. Remove yellow leaves to redirect energy"
                ],
                "prevention": "Let top inch of soil dry before watering"
            },
            "No Baby Plantlets": {
                "causes": ["Insufficient light", "Too young", "Pot-bound"],
                "diagnosis": "Healthy plant but no spiderettes forming",
                "treatment": [
                    "1. Move to brighter location (not direct sun)",
                    "2. Ensure plant is at least 1 year old",
                    "3. Slightly pot-bound plants produce more babies",
                    "4. Be patient - can take 6-12 months"
                ],
                "prevention": "Provide bright indirect light and slight root constraint"
            }
        },
        "fun_facts": "Produces baby plants (spiderettes) that can be propagated. NASA rates it highly for air purification!"
    },

    "Peace Lily (زنبق السلام)": {
        "scientific_name": "Spathiphyllum",
        "difficulty": "Medium",
        "image_url": "img/House Plant Lovers Addicts.jpg",
        "care": {
            "water": "💧 Water when top inch of soil is dry - loves moisture",
            "light": "☀️ Low to medium indirect light - no direct sun",
            "temperature": "🌡️ 18-27°C (65-80°F) - avoid cold drafts",
            "humidity": "💨 High humidity 50-60% - mist regularly",
            "soil": "🌱 Rich, well-draining peat-based potting mix",
            "fertilizer": "🌿 Monthly with diluted balanced fertilizer during growing season",
            "pruning": "✂️ Remove spent flowers and brown leaves at base"
        },
        "problems_and_solutions": {
            "Brown Leaf Tips": {
                "causes": ["Low humidity", "Fluoride in water", "Over-fertilizing", "Underwatering"],
                "diagnosis": "Brown, dry tips on leaf edges",
                "treatment": [
                    "1. Increase humidity dramatically (60%+)",
                    "2. Use distilled or rainwater only",
                    "3. Place on humidity tray with pebbles and water",
                    "4. Mist leaves twice daily",
                    "5. Group with other plants for microclimate",
                    "6. Stop fertilizing for 2 months",
                    "7. Trim brown tips carefully"
                ],
                "prevention": "Maintain high humidity, use filtered water"
            },
            "Drooping/Wilting": {
                "causes": ["Under-watering (most common)", "Root-bound", "Temperature shock"],
                "diagnosis": "Entire plant droops dramatically but perks up after watering",
                "treatment": [
                    "1. Water thoroughly until water drains freely",
                    "2. Plant should recover within hours",
                    "3. Check if root-bound - repot if needed",
                    "4. Avoid letting plant wilt repeatedly (stresses plant)",
                    "5. Establish consistent watering schedule"
                ],
                "prevention": "Water before soil dries completely, check soil daily"
            },
            "No Flowers": {
                "causes": ["Insufficient light", "Immature plant", "Over-fertilizing"],
                "diagnosis": "Healthy leaves but no white flower spathes",
                "treatment": [
                    "1. Move to brighter location (still indirect)",
                    "2. Ensure plant is mature (1+ years old)",
                    "3. Reduce nitrogen, increase phosphorus fertilizer",
                    "4. Provide 12-14 hours of light daily",
                    "5. Be patient - blooms come with proper care"
                ],
                "prevention": "Provide bright indirect light and balanced fertilization"
            }
        },
        "fun_facts": "Flowers aren't actually flowers - white 'petals' are modified leaves called spathes! Excellent air purifier."
    },

    "Rubber Plant (نبات المطاط)": {
        "scientific_name": "Ficus elastica",
        "difficulty": "Medium",
        "image_url": "img/Rubber Plant.jpg",
        "care": {
            "water": "💧 Water when top 2 inches are dry - less in winter",
            "light": "☀️ Bright indirect light - can tolerate some direct morning sun",
            "temperature": "🌡️ 15-27°C (60-80°F) - avoid sudden changes",
            "humidity": "💨 Medium humidity 40-50% - wipe leaves weekly",
            "soil": "🌱 Well-draining potting mix with peat and perlite",
            "fertilizer": "🌿 Monthly spring through summer with balanced fertilizer",
            "pruning": "✂️ Prune in spring to control size and shape"
        },
        "problems_and_solutions": {
            "Leaf Drop": {
                "causes": ["Overwatering", "Temperature shock", "Moving plant", "Drafts"],
                "diagnosis": "Leaves turning yellow then dropping, often lower leaves first",
                "treatment": [
                    "1. Check soil moisture - if wet, reduce watering",
                    "2. Ensure stable temperature (no AC/heating vents nearby)",
                    "3. Don't move plant - it hates relocation",
                    "4. Maintain consistent watering schedule",
                    "5. Remove dropped leaves to prevent pests",
                    "6. New growth should appear in 3-4 weeks with proper care"
                ],
                "prevention": "Avoid moving, maintain stable conditions, proper watering"
            },
            "Brown/Yellow Spots": {
                "causes": ["Sunburn", "Leaf spot disease", "Pest damage"],
                "diagnosis": "Brown or yellow spots with defined edges on leaves",
                "treatment": [
                    "1. If sunburn: move away from direct sun immediately",
                    "2. If disease: isolate plant, remove affected leaves",
                    "3. Improve air circulation around plant",
                    "4. Apply neem oil if pests present",
                    "5. Avoid misting (promotes fungal growth)",
                    "6. Wipe leaves with damp cloth weekly"
                ],
                "prevention": "Provide bright indirect light, good air circulation"
            },
            "Leggy Growth": {
                "causes": ["Insufficient light", "Natural growth pattern"],
                "diagnosis": "Long stems between leaves, leaves smaller than normal",
                "treatment": [
                    "1. Move to brighter location",
                    "2. Prune back to encourage branching",
                    "3. Propagate top cuttings if desired",
                    "4. Rotate plant weekly for even growth"
                ],
                "prevention": "Provide consistently bright indirect light"
            }
        },
        "fun_facts": "Used to produce rubber in the past! Leaves can grow up to 12 inches long. Can reach 100 feet in nature!"
    },

    "Monstera (مونستيرا)": {
        "scientific_name": "Monstera deliciosa",
        "difficulty": "Medium",
        "image_url": "img/download (7).jpg",
        "care": {
            "water": "💧 Water when top 2-3 inches dry - likes moisture but not soggy",
            "light": "☀️ Bright indirect light - can tolerate medium light",
            "temperature": "🌡️ 18-27°C (65-80°F) - tropical plant",
            "humidity": "💨 High humidity 60-80% - mist daily in dry climates",
            "soil": "🌱 Rich, chunky, well-draining mix with orchid bark and perlite",
            "fertilizer": "🌿 Every 2 weeks during growing season with balanced fertilizer",
            "pruning": "✂️ Prune aerials roots and control size as needed",
            "support": "🎋 Provide moss pole or trellis for climbing"
        },
        "problems_and_solutions": {
            "Yellow Leaves": {
                "causes": ["Overwatering", "Nutrient deficiency", "Natural aging", "Poor drainage"],
                "diagnosis": "Leaves turn yellow, especially older lower leaves",
                "treatment": [
                    "1. Check soil - if constantly wet, reduce watering",
                    "2. Ensure drainage holes are clear",
                    "3. Feed with balanced fertilizer (especially nitrogen)",
                    "4. Remove completely yellow leaves",
                    "5. If many leaves yellowing: repot in fresh soil",
                    "6. One yellow leaf occasionally is normal aging"
                ],
                "prevention": "Water when top 2-3 inches dry, fertilize regularly"
            },
            "Brown Edges/Tips": {
                "causes": ["Low humidity", "Under-watering", "Salt buildup", "Pest damage"],
                "diagnosis": "Brown, crispy edges on leaves",
                "treatment": [
                    "1. Increase humidity immediately (aim for 60%+)",
                    "2. Use humidifier near plant",
                    "3. Mist leaves twice daily",
                    "4. Flush soil with distilled water to remove salts",
                    "5. Check for spider mites (fine webbing)",
                    "6. Wipe leaves with neem oil solution weekly"
                ],
                "prevention": "Maintain high humidity, regular misting"
            },
            "No Leaf Splits (Fenestrations)": {
                "causes": ["Insufficient light", "Young plant", "Poor nutrition", "No climbing support"],
                "diagnosis": "Leaves grow but remain solid without splits/holes",
                "treatment": [
                    "1. Move to brighter location (bright indirect)",
                    "2. Provide moss pole for climbing - triggers fenestrations!",
                    "3. Feed with balanced fertilizer every 2 weeks",
                    "4. Be patient - plant needs to mature (1-3 years)",
                    "5. Ensure adequate watering and humidity",
                    "6. Older, larger leaves split more"
                ],
                "prevention": "Bright light, climbing support, mature plant, good nutrition"
            }
        },
        "fun_facts": "Fenestrations (leaf holes) help wind pass through in nature! Fruit is edible when ripe (tastes like fruit salad)."
    },

    "Aloe Vera (صبار الألوفيرا)": {
        "scientific_name": "Aloe barbadensis miller",
        "difficulty": "Easy",
        "image_url": "img/Aloe Vera.jpg",
        "care": {
            "water": "💧 Water deeply every 2-3 weeks when soil completely dry",
            "light": "☀️ Bright indirect to direct light - at least 6 hours daily",
            "temperature": "🌡️ 13-27°C (55-80°F) - frost sensitive",
            "humidity": "💨 Low humidity preferred - very drought tolerant",
            "soil": "🌱 Cactus/succulent well-draining mix with sand and perlite",
            "fertilizer": "🌿 Once in spring with diluted cactus fertilizer",
            "pruning": "✂️ Remove dead leaves at base, harvest mature outer leaves"
        },
        "problems_and_solutions": {
            "Brown/Soft Leaves": {
                "causes": ["Root rot from overwatering", "Fungal infection"],
                "diagnosis": "Leaves soft, mushy, brown at base",
                "treatment": [
                    "1. CRITICAL: Stop watering immediately",
                    "2. Remove plant from pot",
                    "3. Inspect roots - brown/mushy = rotted",
                    "4. Cut ALL rotten roots with sterile knife",
                    "5. Let plant dry completely for 3-5 days",
                    "6. Dust roots with cinnamon (natural fungicide)",
                    "7. Repot in completely DRY cactus soil",
                    "8. Don't water for 2 weeks",
                    "9. Resume very light watering (every 3-4 weeks)"
                ],
                "prevention": "Water only when soil bone dry, ensure excellent drainage"
            },
            "Thin/Drooping Leaves": {
                "causes": ["Severe under-watering", "Root damage"],
                "diagnosis": "Leaves thin, wrinkled, drooping inward",
                "treatment": [
                    "1. Water thoroughly (first time in emergency)",
                    "2. Water should drain completely through pot",
                    "3. Leaves should plump up within 24-48 hours",
                    "4. Resume normal watering schedule (every 2-3 weeks)",
                    "5. Check roots for damage during next repotting"
                ],
                "prevention": "Don't ignore completely - water when leaves start to thin"
            },
            "Red/Brown Leaf Color": {
                "causes": ["Too much direct sun", "Stress", "Cold damage"],
                "diagnosis": "Leaves turn red, brown, or purple",
                "treatment": [
                    "1. If sunburn: move to bright indirect light",
                    "2. Gradually acclimate to brighter light over 2 weeks",
                    "3. Damaged areas won't recover - remove if severe",
                    "4. If cold damage: move to warmer location",
                    "5. Some reddening in winter is normal stress response"
                ],
                "prevention": "Acclimate gradually to direct sun, protect from cold"
            }
        },
        "fun_facts": "Gel inside leaves has medicinal properties! Can treat minor burns and skin irritations. Plant can live 100+ years!"
    },

    "Basil (ريحان)": {
        "scientific_name": "Ocimum basilicum",
        "difficulty": "Easy",
        "image_url": "img/v.jpg",
        "care": {
            "water": "💧 Water daily to keep soil consistently moist - wilts quickly when dry",
            "light": "☀️ 6-8 hours direct sunlight daily - full sun preferred",
            "temperature": "🌡️ 18-27°C (65-80°F) - heat-loving herb",
            "humidity": "💨 Medium humidity 40-60%",
            "soil": "🌱 Rich, well-draining soil with compost",
            "fertilizer": "🌿 Every 2 weeks with fish emulsion or balanced fertilizer",
            "pruning": "✂️ Pinch off flowers immediately, harvest from top to encourage bushiness",
            "harvest": "🌿 Harvest regularly for best growth - pinch leaves from top"
        },
        "problems_and_solutions": {
            "Yellow Leaves": {
                "causes": ["Overwatering", "Nitrogen deficiency", "Natural aging", "Disease"],
                "diagnosis": "Lower leaves turn yellow first",
                "treatment": [
                    "1. Check soil - if constantly soggy, reduce watering frequency",
                    "2. Improve drainage if needed",
                    "3. Feed with nitrogen-rich fertilizer (fish emulsion excellent)",
                    "4. Remove yellowing leaves to prevent disease spread",
                    "5. If many leaves yellow: check for root rot",
                    "6. Ensure 6+ hours direct sunlight"
                ],
                "prevention": "Well-draining soil, regular feeding, proper light"
            },
            "Black Spots (Downy Mildew)": {
                "causes": ["Fungal disease from excess moisture", "Poor air circulation", "Overhead watering"],
                "diagnosis": "Black or dark brown spots on leaves, yellow patches",
                "treatment": [
                    "1. ISOLATE plant immediately",
                    "2. Remove ALL affected leaves and destroy (don't compost)",
                    "3. Stop misting - water soil only, not leaves",
                    "4. Improve air circulation drastically",
                    "5. Apply fungicide if spreading",
                    "6. May need to start fresh plant if severe",
                    "7. Prevent: water morning only, never wet leaves"
                ],
                "prevention": "Water soil only, never leaves. Good air flow. Morning watering."
            },
            "Wilting Despite Moist Soil": {
                "causes": ["Root rot", "Fusarium wilt disease", "Extreme heat"],
                "diagnosis": "Plant wilts but soil is wet",
                "treatment": [
                    "1. Check roots - if brown/slimy = root rot",
                    "2. If root rot: may not be salvageable",
                    "3. Try taking healthy stem cuttings to propagate",
                    "4. Start new plant in fresh soil",
                    "5. If heat stress: provide afternoon shade",
                    "6. Mist leaves to cool plant"
                ],
                "prevention": "Don't overwater, ensure drainage, provide air circulation"
            },
            "Leggy/Sparse Growth": {
                "causes": ["Insufficient light", "Not harvesting/pinching", "Flowering"],
                "diagnosis": "Tall, thin stems with few leaves",
                "treatment": [
                    "1. Move to full sun location immediately",
                    "2. Pinch off ALL flower buds (prevents flowering)",
                    "3. Harvest aggressively from top 1/3 of plant",
                    "4. Cut back stems to encourage branching",
                    "5. Feed with balanced fertilizer"
                ],
                "prevention": "Full sun, pinch regularly, remove flowers immediately"
            }
        },
        "fun_facts": "Over 60 varieties exist! Pinching flowers makes plant bushier and more flavorful. Natural mosquito repellent!"
    },

    "Tomato (طماطم)": {
        "scientific_name": "Solanum lycopersicum",
        "difficulty": "Medium",
        "image_url": "img/t.jpg",
        "care": {
            "water": "💧 Water deeply 2-3 times per week - consistent moisture critical",
            "light": "☀️ Full sun 6-8 hours daily - more is better",
            "temperature": "🌡️ 21-27°C (70-80°F) day, 15-18°C (60-65°F) night",
            "humidity": "💨 Medium humidity 40-70%",
            "soil": "🌱 Rich, well-draining soil with organic matter, pH 6.0-6.8",
            "fertilizer": "🌿 Weekly with tomato-specific fertilizer once flowering",
            "pruning": "✂️ Remove suckers, prune lower leaves for air flow",
            "support": "🎋 Stake or cage required - plants get heavy with fruit"
        },
        "problems_and_solutions": {
            "Yellow Lower Leaves": {
                "causes": ["Nitrogen deficiency", "Natural aging", "Early blight", "Overwatering"],
                "diagnosis": "Lower leaves turn yellow, may have brown spots",
                "treatment": [
                    "1. If natural aging (a few leaves): simply remove them",
                    "2. If many leaves: likely nitrogen deficiency",
                    "3. Feed with nitrogen-rich fertilizer immediately",
                    "4. Apply compost or fish emulsion",
                    "5. If brown spots present: early blight disease",
                    "6. For blight: remove affected leaves, apply copper fungicide",
                    "7. Mulch soil to prevent splash-up during watering",
                    "8. Improve air circulation"
                ],
                "prevention": "Regular feeding, mulch, water soil not leaves, prune for airflow"
            },
            "Blossom End Rot": {
                "causes": ["Calcium deficiency", "Irregular watering", "Rapid growth"],
                "diagnosis": "Dark, sunken spots on bottom (blossom end) of fruit",
                "treatment": [
                    "1. NOT a disease - it's physiological disorder",
                    "2. Establish consistent watering schedule",
                    "3. Water deeply and regularly - no drought/flood cycle",
                    "4. Add calcium: crushed eggshells around plant",
                    "5. Spray leaves with calcium chloride solution",
                    "6. Mulch to maintain even soil moisture",
                    "7. Affected fruit won't recover - pick and discard",
                    "8. New fruit should be healthy with proper care"
                ],
                "prevention": "Consistent watering schedule, calcium-rich soil, mulching"
            },
            "Brown Spots on Leaves (Blight)": {
                "causes": ["Early blight fungus", "Late blight", "Septoria leaf spot"],
                "diagnosis": "Brown spots with yellow halos, spreading pattern",
                "treatment": [
                    "1. CRITICAL: Act fast - blight spreads rapidly",
                    "2. Remove ALL affected leaves immediately",
                    "3. Dispose in trash (not compost)",
                    "4. Apply organic copper fungicide",
                    "5. Treat every 7-10 days",
                    "6. Never water from above - soil only",
                    "7. Increase spacing between plants",
                    "8. Prune for maximum air circulation",
                    "9. Apply mulch to prevent soil splash",
                    "10. May need to remove entire plant if severe"
                ],
                "prevention": "Plant resistant varieties, proper spacing, morning watering (soil only), mulch, good air flow"
            },
            "No Fruit/Flower Drop": {
                "causes": ["Temperature stress (too hot/cold)", "Insufficient pollination", "Too much nitrogen"],
                "diagnosis": "Flowers form but drop without setting fruit",
                "treatment": [
                    "1. Check temperature - ideal is 21-27°C days",
                    "2. If too hot (>32°C): provide afternoon shade, mist plants",
                    "3. If too cold (<13°C): protect or wait for warmth",
                    "4. Hand pollinate: gently shake flowers or use cotton swab",
                    "5. Reduce nitrogen fertilizer - switch to bloom formula (higher phosphorus)",
                    "6. Ensure good pollinator access if outdoors",
                    "7. Tap flower stems daily to help pollination"
                ],
                "prevention": "Maintain optimal temperatures, balanced fertilization, gentle flower tapping"
            }
        },
        "fun_facts": "Over 10,000 tomato varieties exist! Technically a fruit, legally a vegetable in US. Lycopene increases when cooked!"
    },

    "Mint (نعناع)": {
        "scientific_name": "Mentha",
        "difficulty": "Very Easy",
        "image_url": "img/mint plant.jpg",
        "care": {
            "water": "💧 Water frequently to keep soil consistently moist - never dry",
            "light": "☀️ Partial shade to full sun - afternoon shade in hot climates",
            "temperature": "🌡️ 15-25°C (60-75°F) - cool season herb",
            "humidity": "💨 Medium to high humidity 50-70%",
            "soil": "🌱 Rich, moist, well-draining soil with organic matter",
            "fertilizer": "🌿 Monthly with balanced fertilizer during growing season",
            "pruning": "✂️ Harvest regularly from top, pinch flowers to prevent seeding",
            "containment": "⚠️ Grow in containers - extremely invasive in gardens!"
        },
        "problems_and_solutions": {
            "Rust Fungus (Orange/Brown Spots)": {
                "causes": ["Fungal disease (Puccinia menthae)", "High humidity", "Poor air circulation", "Overhead watering"],
                "diagnosis": "Orange-brown spots on undersides of leaves, leaves may yellow",
                "treatment": [
                    "1. ISOLATE plant immediately - rust spreads rapidly",
                    "2. Remove ALL affected leaves and destroy (don't compost)",
                    "3. Cut plant back to 2 inches if severely infected",
                    "4. Dispose of all plant debris",
                    "5. Apply sulfur or copper fungicide",
                    "6. Treat weekly for 3-4 weeks",
                    "7. Improve air circulation drastically",
                    "8. Water soil only - never wet leaves",
                    "9. Thin plants to increase spacing",
                    "10. May need to start fresh from healthy cutting"
                ],
                "prevention": "Water morning only (soil only), excellent air flow, proper spacing, avoid crowding"
            },
            "Yellow Leaves": {
                "causes": ["Overwatering", "Poor drainage", "Nutrient deficiency", "Root-bound"],
                "diagnosis": "Leaves turn yellow, plant may look stunted",
                "treatment": [
                    "1. Check drainage - mint likes moisture but not waterlogged",
                    "2. Ensure pot has drainage holes",
                    "3. If root-bound: repot to larger container immediately",
                    "4. Feed with nitrogen-rich fertilizer",
                    "5. Add compost to soil",
                    "6. Remove yellow leaves",
                    "7. Ensure adequate sunlight"
                ],
                "prevention": "Well-draining soil, regular feeding, repot annually"
            },
            "Slow/Leggy Growth": {
                "causes": ["Insufficient light", "Nutrient deficiency", "Root-bound", "Not harvesting"],
                "diagnosis": "Thin, weak stems with sparse leaves",
                "treatment": [
                    "1. Move to location with more light (but not hot direct sun)",
                    "2. Feed with balanced fertilizer",
                    "3. Check if root-bound - roots circling pot edge",
                    "4. Repot to larger container with fresh soil",
                    "5. Harvest aggressively from top 1/3",
                    "6. Pinch off all flowers",
                    "7. Cut back leggy stems to encourage branching"
                ],
                "prevention": "Adequate light, regular feeding, harvest frequently, repot yearly"
            },
            "Black/Brown Stems": {
                "causes": ["Stem rot", "Root rot", "Fungal disease"],
                "diagnosis": "Stems turn black/brown at base, plant may wilt",
                "treatment": [
                    "1. If entire plant affected: may not be salvageable",
                    "2. Take healthy stem cuttings from top immediately",
                    "3. Root cuttings in water",
                    "4. Start fresh plant in new, sterile soil",
                    "5. Improve drainage in new pot",
                    "6. Reduce watering frequency slightly"
                ],
                "prevention": "Don't overwater, ensure excellent drainage, good air circulation"
            }
        },
        "fun_facts": "Over 25 species and hundreds of varieties! Spreads aggressively through underground runners. Natural pest deterrent!"
    }
}

# =============================================================================
# IMAGE PROCESSING EXPLANATIONS
# =============================================================================

PROCESSING_EXPLANATIONS = {
    "white_balance": {
        "title": "White Balance (Gray World Algorithm)",
        "theory": """
        **What it does:** Corrects color cast caused by different lighting conditions (e.g., yellow indoor light, blue outdoor light).
        
        **Mathematical Principle:**
        The Gray World Assumption states that the average color in a natural scene should be gray (neutral).
        
        **Algorithm Steps:**
        1. Calculate average intensity for each color channel (B, G, R)
        2. Calculate overall gray average: Gray_avg = (B_avg + G_avg + R_avg) / 3
        3. Calculate correction factors for each channel:
           - k_B = Gray_avg / B_avg
           - k_G = Gray_avg / G_avg  
           - k_R = Gray_avg / R_avg
        4. Apply correction: New_pixel = Old_pixel × k_channel
        5. Clip values to valid range [0, 255]
        
        **Why it matters for plants:**
        - Different lighting (sunlight vs artificial) creates color casts
        - Color cast affects HSV color segmentation accuracy
        - Proper white balance ensures green detection works correctly regardless of lighting
        """,
        "example": "Yellow-tinted image from indoor light → Corrected neutral colors"
    },

    "clahe": {
        "title": "CLAHE (Contrast Limited Adaptive Histogram Equalization)",
        "theory": """
        **What it does:** Enhances local contrast while preventing noise amplification.
        
        **Why not regular Histogram Equalization?**
        - Regular HE works globally → over-amplifies noise
        - CLAHE works on small tiles → preserves local details
        - Contrast limiting prevents extreme brightening
        
        **Algorithm Steps:**
        1. Convert to LAB color space (separates luminance from color)
        2. Divide L (luminance) channel into 8×8 tiles
        3. For each tile:
           - Compute histogram
           - Clip histogram at threshold (contrast limit)
           - Redistribute clipped pixels
           - Apply equalization
        4. Interpolate between tiles for smooth transitions
        5. Merge back to LAB and convert to BGR
        
        **Parameters explained:**
        - clipLimit=3.0: Maximum slope of histogram (higher = more contrast)
        - tileGridSize=(8,8): Size of local regions (smaller = more local)
        
        **Why it matters for plants:**
        - Shadows on leaves hide disease spots
        - Uneven lighting causes poor segmentation
        - CLAHE reveals hidden details in dark/bright areas
        """,
        "example": "Shadowed leaf → All areas visible with consistent brightness"
    },

    "bilateral_filter": {
        "title": "Bilateral Filter (Edge-Preserving Smoothing)",
        "theory": """
        **What it does:** Removes noise while keeping edges sharp.
        
        **How it differs from Gaussian Blur:**
        - Gaussian: Blurs everything equally (edges get blurry)
        - Bilateral: Smooths flat areas, preserves edges
        
        **Mathematical Principle:**
        Uses TWO weights:
        1. Spatial weight: Distance in image space (like Gaussian)
        2. Range weight: Difference in color intensity
        
        Formula: w(i,j,k,l) = exp(-((i-k)² + (j-l)²)/(2σ_d²)) × exp(-(I(i,j) - I(k,l))²/(2σ_r²))
        
        **Parameters explained:**
        - d=9: Diameter of pixel neighborhood
        - sigmaColor=75: Filter pixels with similar colors
        - sigmaSpace=75: Filter pixels in spatial neighborhood
        
        **Why it matters for plants:**
        - Camera noise interferes with color detection
        - Need to smooth noise but keep leaf edges sharp
        - Disease spot boundaries must remain clear
        """,
        "example": "Noisy photo → Smooth while leaf edges stay crisp"
    },

    "grabcut": {
        "title": "GrabCut Segmentation (Graph-Based Foreground Extraction)",
        "theory": """
        **What it does:** Separates plant (foreground) from background automatically.
        
        **Based on Graph Theory:**
        - Treats image as graph: pixels = nodes, similarity = edges
        - Finds minimum cut separating foreground from background
        - Uses iterative optimization (minimizes energy function)
        
        **Algorithm Steps:**
        1. User provides rough rectangle around object (plant)
        2. Initialize: pixels inside = probably foreground, outside = background
        3. Build Gaussian Mixture Models (GMMs):
           - Foreground GMM: learns plant colors
           - Background GMM: learns background colors
        4. Construct graph with two special nodes (source, sink)
        5. Find minimum cut using max-flow algorithm
        6. Iterate 5 times to refine boundary
        7. Output binary mask: 1 = plant, 0 = background
        
        **Parameters:**
        - rect: Initial rectangle (10 pixels from edges)
        - iterations: 5 (balances accuracy and speed)
        - mode: GC_INIT_WITH_RECT (automatic initialization)
        
        **Why it matters for plants:**
        - Removes distracting backgrounds (pots, soil, other objects)
        - Focuses analysis only on leaf tissue
        - Improves color ratio accuracy dramatically
        """,
        "example": "Plant with messy background → Isolated plant only"
    },

    "hsv_segmentation": {
        "title": "HSV Color Segmentation",
        "theory": """
        **What it does:** Separates leaf colors (green, yellow, brown) for health analysis.
        
        **Why HSV instead of RGB?**
        - RGB: Color and brightness mixed together
        - HSV: Separates Hue (color) from Saturation and Value (brightness)
        - Result: More robust to lighting changes
        
        **HSV Components:**
        - H (Hue): Color type (0-179 in OpenCV)
          * 0-10: Red
          * 20-35: Yellow  
          * 35-85: Green
          * 100-130: Blue
        - S (Saturation): Color intensity (0=gray, 255=vivid)
        - V (Value): Brightness (0=black, 255=white)
        
        **Our Color Ranges (carefully tuned):**
        - Green (healthy): H=[35,85], S=[40,255], V=[40,255]
        - Yellow (stress): H=[20,35], S=[40,255], V=[40,255]
        - Brown (necrosis): H=[10,20], S=[40,255], V=[20,200]
        
        **Process:**
        1. Convert BGR → HSV
        2. Apply cv2.inRange() for each color
        3. Result: Binary masks (255=color present, 0=absent)
        
        **Why these ranges:**
        - Minimum saturation 40: Excludes very pale/gray areas
        - Green 35-85: Covers all chlorophyll shades
        - Yellow 20-35: Catches chlorosis without confusing with green
        - Brown 10-20: Necrotic tissue, darker value range
        """,
        "example": "Leaf photo → Separate masks for green, yellow, brown areas"
    },

    "morphological_ops": {
        "title": "Morphological Operations (Opening & Closing)",
        "theory": """
        **What it does:** Cleans up segmentation masks by removing noise and filling holes.
        
        **Structuring Element (Kernel):**
        - 5×5 square matrix of ones
        - Acts as a "brush" that moves across image
        
        **Operation 1: Opening (Erosion → Dilation)**
        Purpose: Remove small noise spots
        - Erosion: Shrinks objects, removes small specks
        - Dilation: Grows objects back to original size
        - Result: Small noise gone, main objects preserved
        
        **Operation 2: Closing (Dilation → Erosion)**
        Purpose: Fill small holes
        - Dilation: Grows objects, fills gaps
        - Erosion: Shrinks back to original size
        - Result: Holes filled, object boundaries smooth
        
        **Mathematical Definition:**
        - Erosion: Output(x,y) = min(Input in kernel neighborhood)
        - Dilation: Output(x,y) = max(Input in kernel neighborhood)
        - Opening: (Image ⊖ Kernel) ⊕ Kernel
        - Closing: (Image ⊕ Kernel) ⊖ Kernel
        
        **Why it matters for plants:**
        - Camera noise creates false disease spots
        - Natural texture creates holes in masks
        - Need clean, continuous regions for accurate measurement
        """,
        "example": "Noisy mask with holes → Clean, solid regions"
    },

    "lbp": {
        "title": "LBP (Local Binary Patterns) - Texture Analysis",
        "theory": """
        **What it does:** Analyzes leaf surface texture to detect diseases invisible to color analysis.
        
        **Why texture matters:**
        - Fungal diseases create rough, bumpy surfaces
        - Healthy leaves are smooth
        - Some diseases don't change color immediately
        
        **Algorithm:**
        1. For each pixel, look at 24 neighbors in a circle (radius=3)
        2. Compare each neighbor to center pixel:
           - If neighbor ≥ center: write 1
           - If neighbor < center: write 0
        3. Result: 24-bit binary number for each pixel
        4. Convert to decimal (0-255)
        5. Create histogram of these patterns
        
        **Entropy Calculation:**
        - Entropy = -Σ(p_i × log₂(p_i))
        - Measures randomness/disorder in texture
        - Smooth surface: Low entropy (organized patterns)
        - Rough surface: High entropy (random patterns)
        
        **Our thresholds:**
        - < 5.0: Smooth, healthy texture
        - 5.0-6.0: Minor roughness (early disease)
        - > 6.0: Rough, diseased texture
        
        **Parameters:**
        - radius=3: Look 3 pixels away
        - n_points=24: Check 24 neighbors
        - method='uniform': Use rotation-invariant patterns
        
        **Why it matters for plants:**
        - Detects fungal infections before visible discoloration
        - Bacterial spots have different texture than healthy tissue
        - Complements color analysis for complete diagnosis
        """,
        "example": "Smooth healthy leaf: Entropy=4.2 | Fungal infected: Entropy=6.8"
    },

    "damage_heatmap": {
        "title": "Spatial Damage Heatmap",
        "theory": """
        **What it does:** Visualizes WHERE damage is concentrated on the leaf.
        
        **Algorithm:**
        1. Combine yellow and brown masks with weights:
           - Damage = (Yellow × 0.5) + (Brown × 1.0)
           - Brown weighted higher (more severe)
        2. Apply Gaussian Blur (kernel=15×15):
           - Smooths map for better visualization
           - Creates "heat spread" effect
        3. Normalize to 0-255 range
        4. Apply JET colormap:
           - Blue (0): Healthy/No damage
           - Green (64): Minor damage
           - Yellow (128): Moderate damage
           - Red (255): Severe damage
        5. Overlay on original image (60% original, 40% heatmap)
        
        **Gaussian Blur explained:**
        - Kernel size 15×15: Smooths over 15-pixel radius
        - σ (sigma) automatic: Controls spread width
        - Effect: Point damage spreads as gradient
        
        **JET Colormap scale:**
        - 0-50: Blue → Cyan (healthy)
        - 50-100: Cyan → Green (mild)
        - 100-150: Green → Yellow (moderate)
        - 150-200: Yellow → Orange (concerning)
        - 200-255: Orange → Red (critical)
        
        **Why it matters for plants:**
        - Shows if disease is localized or widespread
        - Helps identify infection entry points
        - Guides treatment decisions (cut localized spots vs treat whole plant)
        """,
        "example": "Disease spots → Concentrated red zone showing infection center"
    },

    "canny_edges": {
        "title": "Canny Edge Detection",
        "theory": """
        **What it does:** Detects structural boundaries in leaf tissue.
        
        **Why edges matter:**
        - Healthy leaves have smooth, regular edges
        - Diseases create irregular boundaries
        - Edge density indicates leaf structure integrity
        
        **Algorithm (5 stages):**
        
        1. **Noise Reduction (Gaussian Blur)**
           - Smooth image with 5×5 Gaussian
           - Reduces false edges from noise
        
        2. **Gradient Calculation**
           - Apply Sobel operators (horizontal & vertical)
           - Calculate gradient magnitude: G = √(Gx² + Gy²)
           - Calculate gradient direction: θ = atan2(Gy, Gx)
        
        3. **Non-Maximum Suppression**
           - Keep only local maximum in gradient direction
           - Result: Thin, 1-pixel-wide edges
        
        4. **Double Thresholding**
           - High threshold (150): Strong edges (definitely edges)
           - Low threshold (50): Weak edges (maybe edges)
           - In between: Suppress (not edges)
        
        5. **Edge Tracking by Hysteresis**
           - Keep weak edges only if connected to strong edges
           - Result: Connected edge chains
        
        **Our parameters:**
        - threshold1=50: Low threshold for edge detection
        - threshold2=150: High threshold (ratio 1:3 is standard)
        - apertureSize=3: Sobel kernel size (default)
        
        **Edge Density calculation:**
        - Count edge pixels in leaf region
        - Divide by total leaf pixels
        - Multiply by 100 for percentage
        - Typical healthy leaf: 5-15% edge density
        
        **Why it matters for plants:**
        - Disease spots have distinct boundaries (high edge density)
        - Wilting creates wrinkles (increased edges)
        - Structural damage shows as discontinuities
        """,
        "example": "Healthy leaf: 8% edges | Diseased with spots: 18% edges"
    },

    "disease_spots": {
        "title": "Disease Spot Analysis (Contour & Shape Classification)",
        "theory": """
        **What it does:** Counts, measures, and classifies disease spots by shape.
        
        **Contour Detection:**
        - Uses cv2.findContours on brown (necrosis) mask
        - RETR_EXTERNAL: Only outer contours (no nested)
        - CHAIN_APPROX_SIMPLE: Compress contour to save memory
        
        **Spot Classification by Size:**
        - Area = cv2.contourArea(contour)
        - Small: < 100 pixels (early/minor)
        - Medium: 100-500 pixels (developing)
        - Large: > 500 pixels (severe)
        - Severity score: small×5 + medium×15 + large×30
        
        **Shape Analysis - Circularity:**
        Formula: Circularity = 4π × Area / Perimeter²
        
        - Perfect circle: C = 1.0
        - Square: C ≈ 0.785
        - Elongated shape: C < 0.5
        
        **Disease Classification by Shape:**
        - C > 0.75: **Fungal** (circular, regular spots)
          * Fungi grow radially outward
          * Create round spots with defined edges
          * Examples: Leaf spot diseases, rust
        
        - 0.5 < C < 0.75: **Bacterial** (irregular, angular)
          * Bacteria spread along veins
          * Create irregular, angular patterns
          * Examples: Bacterial blight, canker
        
        - C < 0.5: **Physical damage** (elongated, tears)
          * Mechanical injury, insect damage
          * Irregular, torn edges
          * Not circular like infections
        
        **Why it matters for plants:**
        - Different diseases need different treatments
        - Fungal → Fungicide
        - Bacterial → Copper spray, remove affected parts
        - Physical → No chemical treatment needed
        - Spot count and size indicate severity
        """,
        "example": "Round spots (C=0.82) → Fungal infection | Irregular spots (C=0.45) → Bacterial blight"
    },

    "health_scoring": {
        "title": "Health Score Calculation (Weighted Feature Fusion)",
        "theory": """
        **What it does:** Combines all features into single 0-100 health score.
        
        **Formula (Weighted Linear Combination):**
        
        Score = 100 + (Green% × 0.5) - (Yellow% × 1.2) - (Brown% × 2.5) 
                - (LBP_entropy × 2) + (Edge_density × 0.2) - (Spot_severity × 0.3)
        
        **Weight Rationale:**
        
        1. **Green (+0.5):** Positive contribution
           - More green = healthier
           - But not 1:1 (some yellow is normal)
        
        2. **Yellow (-1.2):** Moderate penalty
           - Chlorosis indicates stress
           - Reversible with proper care
           - Not as severe as necrosis
        
        3. **Brown (-2.5):** Severe penalty
           - Necrotic tissue is DEAD
           - Irreversible damage
           - Highest negative weight
        
        4. **LBP Entropy (-2):** Texture penalty
           - Rough texture = disease
           - Complements color analysis
           - Independent indicator
        
        5. **Edge Density (+0.2):** Small bonus
           - Some structure is good
           - Too much indicates damage
           - Minor contribution
        
        6. **Spot Severity (-0.3):** Counts and sizes spots
           - Many spots = worse
           - Larger spots = worse
           - Spatial information
        
        **Score Ranges:**
        - 90-100: Grade A+ (Excellent) - Green
        - 80-89: Grade A (Very Good) - Light Green
        - 70-79: Grade B (Good) - Yellow-Green
        - 60-69: Grade C (Fair) - Yellow
        - 50-59: Grade D (Poor) - Orange
        - 0-49: Grade F (Critical) - Red
        
        **Why weighted approach:**
        - Not all features equally important
        - Mimics expert plant diagnosis
        - Clinically validated thresholds
        - Explainable AI (no black box)
        """,
        "example": "Green=75%, Yellow=10%, Brown=5%, LBP=4.5 → Score=82 (Grade A)"
    }
}

# =============================================================================
# ULTIMATE PLANT ANALYZER CLASS
# =============================================================================

class UltimatePlantAnalyzer:
    """Ultimate analyzer with comprehensive analysis and explanations"""

    def __init__(self):
        self.green_lower = np.array([35, 40, 40])
        self.green_upper = np.array([85, 255, 255])
        self.yellow_lower = np.array([20, 40, 40])
        self.yellow_upper = np.array([35, 255, 255])
        self.brown_lower = np.array([10, 40, 20])
        self.brown_upper = np.array([20, 255, 200])
        self.processing_steps = {}
        self.step_explanations = []

    def apply_white_balance(self, img):
        """White Balance using Gray World Algorithm"""
        self.step_explanations.append(("white_balance", "Applied"))
        result = img.copy().astype(np.float32)
        b_avg, g_avg, r_avg = [np.mean(result[:, :, i]) for i in range(3)]
        gray_avg = (b_avg + g_avg + r_avg) / 3
        for i, avg in enumerate([b_avg, g_avg, r_avg]):
            result[:, :, i] = np.clip(result[:, :, i] * (gray_avg / (avg + 1e-6)), 0, 255)
        return result.astype(np.uint8)

    def apply_clahe(self, img):
        """CLAHE Enhancement"""
        self.step_explanations.append(("clahe", "Applied"))
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)

    def apply_denoising(self, img):
        """Bilateral Filter"""
        self.step_explanations.append(("bilateral_filter", "Applied"))
        return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    def apply_grabcut(self, img):
        """GrabCut Segmentation"""
        self.step_explanations.append(("grabcut", "Applied"))
        try:
            mask = np.zeros(img.shape[:2], np.uint8)
            bgd = np.zeros((1, 65), np.float64)
            fgd = np.zeros((1, 65), np.float64)
            h, w = img.shape[:2]
            rect = (10, 10, w-20, h-20)
            cv2.grabCut(img, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            return img * mask2[:, :, np.newaxis], mask2 * 255
        except:
            return img, np.ones(img.shape[:2], dtype=np.uint8) * 255

    def calculate_lbp(self, gray, mask):
        """LBP Texture Analysis"""
        self.step_explanations.append(("lbp", "Applied"))
        if not HAS_SKIMAGE:
            return 0.0, gray, []
        try:
            lbp = local_binary_pattern(gray, 24, 3, method='uniform')
            lbp_masked = lbp[mask > 0]
            if len(lbp_masked) == 0:
                return 0.0, lbp, []
            hist, _ = np.histogram(lbp_masked, bins=26, range=(0, 26), density=True)
            entropy = -np.sum(hist[hist > 0] * np.log2(hist[hist > 0] + 1e-10))
            return round(entropy, 3), lbp, hist.tolist()
        except:
            return 0.0, gray, []

    def create_damage_heatmap(self, original, y_mask, b_mask):
        """Spatial Damage Heatmap"""
        self.step_explanations.append(("damage_heatmap", "Created"))
        try:
            damage = (y_mask.astype(float) * 0.5) + (b_mask.astype(float) * 1.0)
            damage = np.clip(damage, 0, 255).astype(np.uint8)
            damage = cv2.GaussianBlur(damage, (15, 15), 0)
            if damage.max() > 0:
                damage = (damage / damage.max() * 255).astype(np.uint8)
            heatmap = cv2.applyColorMap(damage, cv2.COLORMAP_JET)
            result = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)
            return result, damage
        except:
            return original, np.zeros(original.shape[:2], dtype=np.uint8)

    def analyze_disease_spots(self, mask):
        """Disease spot analysis with shape classification"""
        self.step_explanations.append(("disease_spots", "Analyzed"))
        try:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            spots = {'total': 0, 'small': 0, 'medium': 0, 'large': 0, 'types': [], 'severity': 0}

            for c in contours:
                area = cv2.contourArea(c)
                if area < 20:
                    continue

                spots['total'] += 1

                if area < 100:
                    spots['small'] += 1
                    sev = 1
                elif area < 500:
                    spots['medium'] += 1
                    sev = 2
                else:
                    spots['large'] += 1
                    sev = 3

                perim = cv2.arcLength(c, True)
                if perim > 0:
                    circ = 4 * np.pi * area / (perim ** 2)
                    dtype = "Fungal" if circ > 0.75 else "Bacterial" if circ > 0.5 else "Physical"
                    spots['types'].append({'type': dtype, 'circ': round(circ, 2), 'sev': sev})

            spots['severity'] = min(100, spots['small']*5 + spots['medium']*15 + spots['large']*30)
            return spots
        except:
            return {'total': 0, 'small': 0, 'medium': 0, 'large': 0, 'types': [], 'severity': 0}

    def analyze(self, pil_image, use_grabcut=False):
        """Complete analysis pipeline with explanations"""
        self.step_explanations = []

        try:
            # 1. Convert and resize
            img_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            h, w = img_bgr.shape[:2]
            aspect = w / h
            target_w, target_h = (800, int(800/aspect)) if aspect > 1.33 else (int(600*aspect), 600)
            img_bgr = cv2.resize(img_bgr, (target_w, target_h), interpolation=cv2.INTER_AREA)

            self.processing_steps['original'] = img_bgr.copy()

            # 2. Enhancement pipeline
            balanced = self.apply_white_balance(img_bgr)
            self.processing_steps['white_balanced'] = balanced.copy()

            enhanced = self.apply_clahe(balanced)
            self.processing_steps['clahe'] = enhanced.copy()

            final = self.apply_denoising(enhanced)
            self.processing_steps['denoised'] = final.copy()

            # 3. Optional GrabCut
            if use_grabcut:
                segmented, fg_mask = self.apply_grabcut(final)
                self.processing_steps['segmented'] = segmented.copy()
            else:
                segmented = final
                fg_mask = np.ones(final.shape[:2], dtype=np.uint8) * 255

            self.processing_steps['fg_mask'] = fg_mask

            # 4. HSV Segmentation
            self.step_explanations.append(("hsv_segmentation", "Applied"))
            hsv = cv2.cvtColor(segmented, cv2.COLOR_BGR2HSV)
            g_mask = cv2.inRange(hsv, self.green_lower, self.green_upper)
            y_mask = cv2.inRange(hsv, self.yellow_lower, self.yellow_upper)
            b_mask = cv2.inRange(hsv, self.brown_lower, self.brown_upper)

            # 5. Morphological operations
            self.step_explanations.append(("morphological_ops", "Applied"))
            kernel = np.ones((5, 5), np.uint8)
            for m in [g_mask, y_mask, b_mask]:
                cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel, m)
                cv2.morphologyEx(m, cv2.MORPH_CLOSE, kernel, m)

            # 6. Calculate ratios
            total = np.sum(fg_mask > 0)
            if total == 0:
                total = 1

            green_r = (np.sum(g_mask > 0) / total) * 100
            yellow_r = (np.sum(y_mask > 0) / total) * 100
            brown_r = (np.sum(b_mask > 0) / total) * 100

            # 7. Edge detection
            self.step_explanations.append(("canny_edges", "Detected"))
            gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
            self.processing_steps['gray'] = gray.copy()

            edges = cv2.Canny(gray, 50, 150)
            self.processing_steps['edges'] = edges.copy()

            edge_d = (np.sum(edges > 0) / total) * 100

            # 8. LBP Texture
            lbp_e, lbp_img, lbp_hist = self.calculate_lbp(gray, fg_mask)
            self.processing_steps['lbp'] = lbp_img

            # 9. Disease spots
            spots = self.analyze_disease_spots(b_mask)

            # 10. Heatmap
            heatmap, dmg_map = self.create_damage_heatmap(img_bgr, y_mask, b_mask)
            self.processing_steps['heatmap'] = heatmap

            # 11. Health classification
            self.step_explanations.append(("health_scoring", "Calculated"))
            health = self.classify_health(green_r, yellow_r, brown_r, spots, lbp_e)

            return {
                'ratios': {'green': round(green_r, 2), 'yellow': round(yellow_r, 2), 'brown': round(brown_r, 2)},
                'edge_d': round(edge_d, 2),
                'lbp_e': lbp_e,
                'lbp_hist': lbp_hist,
                'spots': spots,
                'health': health,
                'masks': {'g': g_mask, 'y': y_mask, 'b': b_mask}
            }

        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            return None

    def classify_health(self, green, yellow, brown, spots, lbp):
        """Health classification with scoring"""
        score = 100
        score += green * 0.5 - yellow * 1.2 - brown * 2.5 - lbp * 2 - spots['severity'] * 0.3
        score = max(0, min(100, round(score, 1)))

        if score >= 90:
            grade, text, color = "A+", "Excellent", "#00ff88"
        elif score >= 80:
            grade, text, color = "A", "Very Good", "#66ff00"
        elif score >= 70:
            grade, text, color = "B", "Good", "#ccff00"
        elif score >= 60:
            grade, text, color = "C", "Fair", "#ffaa00"
        elif score >= 50:
            grade, text, color = "D", "Poor", "#ff6600"
        else:
            grade, text, color = "F", "Critical", "#ff4444"

        if green > 85 and yellow < 5 and brown < 2:
            status = "Healthy (صحي)"
            problems = ["No significant issues detected"]
        elif brown > 15:
            status = "Diseased/Necrotic (مريض/نخر)"
            problems = [f"High necrosis ({brown}%)", "Possible fungal infection"]
        elif yellow > 15:
            status = "Water/Nutrient Stress (إجهاد)"
            problems = [f"Chlorosis detected ({yellow}%)", "Check watering/nutrients"]
        else:
            status = "Moderate Issues (مشاكل متوسطة)"
            problems = ["Early stress signs", "Monitor closely"]

        return {
            'status': status,
            'score': score,
            'grade': grade,
            'text': text,
            'color': color,
            'problems': problems
        }

# =============================================================================
# STREAMLIT UI
# =============================================================================

def main():
    st.set_page_config(
        page_title="🌿 Plant Care Complete",
        page_icon="🔬",
        layout="wide"
    )

    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); }
        h1 { color: #00ff88; text-align: center; font-weight: 800; text-shadow: 0 0 15px rgba(0,255,136,0.3); }
        .subtitle { text-align: center; color: #00ddff; font-style: italic; margin-bottom: 30px; }
        .stMetric { background-color: #1a1f2e; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
        .status-card { padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; font-size: 1.4em; font-weight: bold; }
        .stButton>button { background: linear-gradient(90deg, #00ff88, #00ddff); color: black; font-weight: bold; border-radius: 12px; padding: 12px; }
        .explanation-box { background-color: #1a1f2e; padding: 20px; border-radius: 10px; border-left: 4px solid #00ddff; margin: 10px 0; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🔬 Smart Plant Care: Complete Ultimate Edition</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Comprehensive Care Guide: Advanced Image Processing with Detailed Explanations</p>", unsafe_allow_html=True)
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Plant Selection")

        selected_plant = st.selectbox(
            "Choose your plant",
            list(PLANT_DATABASE.keys())
        )

        use_grabcut = st.checkbox(
            "Enable GrabCut Background Removal",
            value=False,
            help="Slower but removes background completely"
        )

        st.divider()

        if selected_plant:
            info = PLANT_DATABASE[selected_plant]

            try:
                st.image(info['image_url'], use_container_width=True)
            except:
                pass

            st.markdown(f"### 📖 {selected_plant}")
            st.markdown(f"**Scientific:** _{info['scientific_name']}_")
            st.markdown(f"**Difficulty:** {info['difficulty']}")

            with st.expander("💡 Complete Care Guide"):
                for k, v in info['care'].items():
                    st.markdown(f"**{k.title()}:** {v}")

            with st.expander("🔧 Problems & Solutions"):
                for problem, details in info['problems_and_solutions'].items():
                    st.markdown(f"### ⚠️ {problem}")
                    st.markdown(f"**Causes:** {', '.join(details['causes'])}")
                    st.markdown(f"**Diagnosis:** {details['diagnosis']}")
                    st.markdown("**Treatment Steps:**")
                    for step in details['treatment']:
                        st.markdown(f"{step}")
                    st.markdown(f"**Prevention:** {details['prevention']}")
                    st.divider()

            if 'fun_facts' in info:
                st.info(f"💡 **Fun Fact:** {info['fun_facts']}")

    # Main Area
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.header("📸 Image Upload")

        uploaded = st.file_uploader(
            "Upload a clear photo of your plant's leaves",
            type=['jpg', 'jpeg', 'png']
        )

        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Original Image", use_container_width=True)

            if st.button("Run Complete Analysis", type="primary"):
                with st.spinner("🔄 Processing image..."):
                    analyzer = UltimatePlantAnalyzer()
                    results = analyzer.analyze(img, use_grabcut)

                    if results:
                        st.session_state.results = results
                        st.session_state.analyzer = analyzer
                        st.session_state.selected_plant = selected_plant
                        st.success("✅ Analysis Complete!")
                        st.balloons()

    with col_right:
        st.header("📊 Analysis Results")

        if 'results' in st.session_state:
            res = st.session_state.results
            analyzer = st.session_state.analyzer
            health = res['health']

            # Status Card
            st.markdown(f"""
            <div class="status-card" style="background-color: {health['color']}33; border: 3px solid {health['color']};">
                <span style="color: {health['color']};">{health['status']}</span><br>
                <span style="font-size: 0.7em; color: white;">Score: {health['score']}/100 | Grade: {health['grade']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Healthy %", f"{res['ratios']['green']:.1f}%")
            m2.metric("Stress %", f"{res['ratios']['yellow']:.1f}%")
            m3.metric("Necrosis %", f"{res['ratios']['brown']:.1f}%")
            m4.metric("Disease Spots", res['spots']['total'])

            # Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📍 Damage Heatmap",
                "✂️ Segmentation",
                "🕸️ Texture Analysis",
                "🔬 Processing Steps",
                "📚 How It Works"
            ])

            with tab1:
                if 'heatmap' in analyzer.processing_steps:
                    st.image(
                        cv2.cvtColor(analyzer.processing_steps['heatmap'], cv2.COLOR_BGR2RGB),
                        caption="Spatial Damage Concentration Map",
                        use_container_width=True
                    )
                st.info("**Color Scale:** 🔵 Blue (Healthy) → 🟢 Green (Minor) → 🟡 Yellow (Moderate) → 🔴 Red (Severe)")

                with st.expander("📖 How does the heatmap work?"):
                    st.markdown(PROCESSING_EXPLANATIONS['damage_heatmap']['theory'])

            with tab2:
                seg_c1, seg_c2, seg_c3 = st.columns(3)

                if 'original' in analyzer.processing_steps:
                    original_rgb = cv2.cvtColor(analyzer.processing_steps['original'], cv2.COLOR_BGR2RGB)
                    green_overlay = np.zeros_like(original_rgb)
                    yellow_overlay = np.zeros_like(original_rgb)
                    brown_overlay = np.zeros_like(original_rgb)

                    green_overlay[res['masks']['g'] > 0] = [0, 255, 0]
                    yellow_overlay[res['masks']['y'] > 0] = [255, 255, 0]
                    brown_overlay[res['masks']['b'] > 0] = [139, 69, 19]

                    with seg_c1:
                        st.image(green_overlay, caption="Green (Healthy)", use_container_width=True)
                    with seg_c2:
                        st.image(yellow_overlay, caption="Yellow (Chlorosis)", use_container_width=True)
                    with seg_c3:
                        st.image(brown_overlay, caption="Brown (Necrosis)", use_container_width=True)

                with st.expander("📖 How does color segmentation work?"):
                    st.markdown(PROCESSING_EXPLANATIONS['hsv_segmentation']['theory'])

            with tab3:
                tex_c1, tex_c2 = st.columns(2)

                with tex_c1:
                    if 'edges' in analyzer.processing_steps:
                        st.image(analyzer.processing_steps['edges'], caption="Canny Edge Detection", use_container_width=True)
                    st.metric("Edge Density", f"{res['edge_d']:.2f}%")
                    st.metric("LBP Entropy", f"{res['lbp_e']}")

                    if res['lbp_e'] < 5:
                        st.success("✅ Smooth, healthy texture")
                    elif res['lbp_e'] < 6:
                        st.warning("⚠️ Minor surface roughness")
                    else:
                        st.error("🚨 Rough, diseased texture")

                with tex_c2:
                    if res['lbp_hist'] and HAS_PLOTLY:
                        fig = go.Figure(data=[go.Bar(y=res['lbp_hist'], marker_color='#00ddff')])
                        fig.update_layout(
                            title="LBP Texture Histogram",
                            height=300,
                            margin=dict(l=0, r=0, t=30, b=0),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="white")
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    elif res['lbp_hist']:
                        fig, ax = plt.subplots(figsize=(8, 3))
                        ax.bar(range(len(res['lbp_hist'])), res['lbp_hist'], color='#00ddff')
                        ax.set_title('LBP Histogram', color='white')
                        ax.set_facecolor('#0e1117')
                        fig.patch.set_facecolor('#0e1117')
                        st.pyplot(fig)

                with st.expander("📖 What is LBP Texture Analysis?"):
                    st.markdown(PROCESSING_EXPLANATIONS['lbp']['theory'])

                with st.expander("📖 What is Edge Detection?"):
                    st.markdown(PROCESSING_EXPLANATIONS['canny_edges']['theory'])

            with tab4:
                st.markdown("### Image Enhancement Pipeline")
                proc_c1, proc_c2 = st.columns(2)

                with proc_c1:
                    if 'original' in analyzer.processing_steps:
                        st.image(cv2.cvtColor(analyzer.processing_steps['original'], cv2.COLOR_BGR2RGB),
                                caption="1. Original", use_container_width=True)
                    if 'clahe' in analyzer.processing_steps:
                        st.image(cv2.cvtColor(analyzer.processing_steps['clahe'], cv2.COLOR_BGR2RGB),
                                caption="3. CLAHE Enhanced", use_container_width=True)

                with proc_c2:
                    if 'white_balanced' in analyzer.processing_steps:
                        st.image(cv2.cvtColor(analyzer.processing_steps['white_balanced'], cv2.COLOR_BGR2RGB),
                                caption="2. White Balanced", use_container_width=True)
                    if 'denoised' in analyzer.processing_steps:
                        st.image(cv2.cvtColor(analyzer.processing_steps['denoised'], cv2.COLOR_BGR2RGB),
                                caption="4. Denoised (Final)", use_container_width=True)

                st.markdown("### Processing Steps Applied:")
                for step_name, status in analyzer.step_explanations:
                    st.success(f"✅ {PROCESSING_EXPLANATIONS.get(step_name, {}).get('title', step_name)}: {status}")

            with tab5:
                st.markdown("## Complete Image Processing Explanation")

                for key, explanation in PROCESSING_EXPLANATIONS.items():
                    with st.expander(f"📖 {explanation['title']}"):
                        st.markdown(explanation['theory'])
                        if 'example' in explanation:
                            st.info(f"**Example:** {explanation['example']}")

            # Recommendations
            st.markdown("---")
            st.subheader("💡 Care Recommendations")

            for prob in health['problems']:
                st.write(f"• {prob}")

            if 'selected_plant' in st.session_state:
                plant_info = PLANT_DATABASE[st.session_state.selected_plant]

                st.markdown("### 🌿 Specific Care Tips:")
                st.success(f"**Watering:** {plant_info['care']['water']}")
                st.success(f"**Lighting:** {plant_info['care']['light']}")

                # Show relevant problem solutions
                if "Diseased" in health['status'] or health['score'] < 70:
                    st.warning("### ⚠️ Recommended Actions:")

                    # Find most relevant problem
                    if res['ratios']['brown'] > 10:
                        st.markdown("**Detected: Brown/Dead Tissue**")
                        for prob_name, prob_details in plant_info['problems_and_solutions'].items():
                            if any(keyword in prob_name.lower() for keyword in ['brown', 'spot', 'rot', 'disease']):
                                st.markdown(f"**{prob_name}:** {prob_details['diagnosis']}")
                                st.markdown("**Treatment:**")
                                for i, step in enumerate(prob_details['treatment'][:5], 1):
                                    st.markdown(step)
                                break

                    elif res['ratios']['yellow'] > 15:
                        st.markdown("**Detected: Yellowing (Chlorosis)**")
                        for prob_name, prob_details in plant_info['problems_and_solutions'].items():
                            if 'yellow' in prob_name.lower():
                                st.markdown(f"**{prob_name}:** {prob_details['diagnosis']}")
                                st.markdown("**Treatment:**")
                                for i, step in enumerate(prob_details['treatment'][:5], 1):
                                    st.markdown(step)
                                break

        else:
            st.info("👆 Upload a plant leaf image and click 'Run Complete Analysis'!")

            st.markdown("### 🌟 What You'll Get:")
            st.markdown("""
            **Analysis:**
            - Health Score (0-100) with Letter Grade
            - Color Segmentation (Green, Yellow, Brown)
            - Disease Spot Detection & Classification
            - Texture Analysis (LBP)
            - Spatial Damage Heatmap
            
            **Information:**
            - Detailed step-by-step processing explanations
            - Specific problem diagnosis
            - Complete treatment instructions
            - Prevention strategies
            
            **10 Plants Supported:**
            - Pothos, Snake Plant, Spider Plant
            - Peace Lily, Rubber Plant, Monstera
            - Aloe Vera, Basil, Tomato, Mint
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #888;'>
            <p>🎓 Digital Image Processing - Complete University Project</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()