import os

def analyze_nutritional_deficiencies_8(medical_condition, bmi, dietary_preference, calories):
    """
    Evaluates 8 estimated nutritional risk indicators based on patient parameters.
    Returns structured risk objects with clear educational non-diagnostic disclaimers.
    """
    deficiencies = []
    
    # 1. Vitamin D
    deficiencies.append({
        "nutrient": "Vitamin D",
        "score": 85 if medical_condition in ["Osteoporosis", "Arthritis", "Vitamin D Deficiency"] else 45,
        "risk_level": "High Risk Indicator" if medical_condition in ["Osteoporosis", "Arthritis", "Vitamin D Deficiency"] else "Moderate Risk Indicator",
        "symptoms": "Bone tenderness, muscle fatigue, low mood, impaired immune response",
        "causes": "Limited sunlight exposure, lack of fatty fish and fortified dairy intake",
        "foods_to_eat": "Pan-seared Salmon Fillet, Egg Yolks, Mushrooms, Fortified Soy/Dairy Milk",
        "foods_to_avoid": "Excessive Soft Drinks, Alcohol, High Sodium Snacks",
        "supplements": "Vitamin D3 2000 IU / day with a fat-containing meal",
        "disclaimer": "Educational risk indicator. Consider discussing persistent symptoms with a qualified physician."
    })
    
    # 2. Iron & Hemoglobin
    if medical_condition in ["Anemia", "Iron Deficiency"] or dietary_preference in ["Vegan", "Vegetarian", "Jain"]:
        deficiencies.append({
            "nutrient": "Iron & Hemoglobin",
            "score": 90 if medical_condition in ["Anemia", "Iron Deficiency"] else 60,
            "risk_level": "High Risk Indicator" if medical_condition in ["Anemia", "Iron Deficiency"] else "Moderate Risk Indicator",
            "symptoms": "Lightheadedness, pale skin tone, shortness of breath, cold hands & feet",
            "causes": "Absence of heme iron sources; tannic acid inhibition from tea/coffee",
            "foods_to_eat": "Steamed Spinach, Beetroot, Pomegranate, Lentils, Kala Chana, Pumpkin Seeds",
            "foods_to_avoid": "Caffeinated Tea/Coffee consumed directly after mealtime",
            "supplements": "Ferrous ascorbate 100mg co-administered with Vitamin C",
            "disclaimer": "Educational risk indicator. Perform serum ferritin blood tests before high-dose supplementation."
        })
        
    # 3. Vitamin B12
    if dietary_preference in ["Vegan", "Vegetarian", "Jain"] or medical_condition in ["Vitamin B12 Deficiency", "Diabetes Type 2"]:
        deficiencies.append({
            "nutrient": "Vitamin B12 (Cobalamin)",
            "score": 92 if dietary_preference == "Vegan" else 55,
            "risk_level": "High Risk Indicator" if dietary_preference == "Vegan" else "Moderate Risk Indicator",
            "symptoms": "Tingling sensation in extremities, memory lapses, brain fog, fatigue",
            "causes": "Lack of animal protein in plant diets; Metformin medication interaction",
            "foods_to_eat": "Fortified Soy Milk, Nutritional Yeast, Plain Greek Yogurt, Cottage Cheese",
            "foods_to_avoid": "Refined Sugars, Heavy Alcohol",
            "supplements": "Methylcobalamin 1500 mcg sublingual tablet daily",
            "disclaimer": "Educational risk indicator. Consult a medical professional for serum B12 lab evaluation."
        })
        
    # 4. Calcium
    if medical_condition in ["Osteoporosis", "Lactose Intolerance"] or dietary_preference in ["Vegan", "Dairy Free"]:
        deficiencies.append({
            "nutrient": "Calcium",
            "score": 88 if medical_condition == "Osteoporosis" else 50,
            "risk_level": "High Risk Indicator" if medical_condition == "Osteoporosis" else "Moderate Risk Indicator",
            "symptoms": "Brittle nails, tooth decay, joint stiffness, muscle twitches",
            "causes": "Low dairy intake or reduced intestinal calcium absorption",
            "foods_to_eat": "Chia Seeds, Black Sesame Seeds (Til), Finger Millet (Ragi), Firm Tofu",
            "foods_to_avoid": "High Sodium Packaged Foods, Carbonated Sodas",
            "supplements": "Calcium Citrate 500mg + Magnesium",
            "disclaimer": "Educational risk indicator. Monitor bone density (DEXA) with your healthcare specialist."
        })
        
    # 5. Dietary Fiber
    deficiencies.append({
        "nutrient": "Dietary Fiber",
        "score": 75 if medical_condition in ["IBS", "Gastritis", "Obesity", "Diabetes Type 2"] else 30,
        "risk_level": "High Risk Indicator" if medical_condition in ["IBS", "Gastritis", "Obesity"] else "Low Risk Indicator",
        "symptoms": "Irregular bowel movements, sluggish digestion, post-meal glucose spikes",
        "causes": "High consumption of refined white flour (maida), white rice, and low produce intake",
        "foods_to_eat": "Rolled Oats, Quinoa, Millets, Apples, Berries, Rajma, Sprouted Moong",
        "foods_to_avoid": "White Bread, Deep Fried Puri/Bhature, Commercial Pastries",
        "supplements": "Psyllium Husk (Isabgol) 1 tbsp in warm water before bedtime",
        "disclaimer": "Educational risk indicator. Increase water intake gradually alongside dietary fiber."
    })
    
    # 6. Complete Protein
    if calories < 1400 or dietary_preference in ["Vegan", "Jain"]:
        deficiencies.append({
            "nutrient": "Complete Protein",
            "score": 65,
            "risk_level": "Moderate Risk Indicator",
            "symptoms": "Delayed exercise recovery, hair thinning, loss of lean muscle mass",
            "causes": "Restricted essential amino acid profiles in non-varied plant diets",
            "foods_to_eat": "Soy Chunks, Firm Tofu, Paneer, Lentils, Pea Protein, Egg Whites",
            "foods_to_avoid": "Empty Calorie Sugary Foods",
            "supplements": "Plant Pea Protein Isolate 25g scoop",
            "disclaimer": "Educational risk indicator. Ensure balanced daily essential amino acid distribution."
        })

    # 7. Omega-3 Fatty Acids
    if dietary_preference in ["Vegetarian", "Vegan", "Jain"] or medical_condition in ["Heart Disease", "High Cholesterol"]:
        deficiencies.append({
            "nutrient": "Omega-3 Fatty Acids (EPA/DHA)",
            "score": 70,
            "risk_level": "Moderate Risk Indicator",
            "symptoms": "Dry skin patches, joint stiffness, sluggish cognitive focus",
            "causes": "Absence of cold-water fatty fish consumption",
            "foods_to_eat": "Walnut Halves, Ground Flax Seeds, Chia Seeds, Extra Virgin Olive Oil",
            "foods_to_avoid": "Trans Fats, Hydrogenated Margarine Oils",
            "supplements": "Algal DHA Omega-3 1000mg softgel capsule",
            "disclaimer": "Educational risk indicator. Consult physician if taking blood-thinning medications."
        })

    # 8. Magnesium
    deficiencies.append({
        "nutrient": "Magnesium",
        "score": 40,
        "risk_level": "Low Risk Indicator",
        "symptoms": "Night muscle cramps, leg twitches, restless sleep",
        "causes": "Suboptimal green leafy vegetable, nut, and seed intake",
        "foods_to_eat": "Raw Pumpkin Seeds, Steamed Spinach, Dark Chocolate 85%, Raw Almonds",
        "foods_to_avoid": "Excess Refined Sugar, Sugary Energy Drinks",
        "supplements": "Magnesium Glycinate 200mg at bedtime",
        "disclaimer": "Educational risk indicator. Consider discussing persistent concerns with a qualified healthcare professional."
    })
        
    return deficiencies
