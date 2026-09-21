import re

def validate_food_safety(food_name, user_profile, allergens_str="", row_dict=None):
    allergy = user_profile.get("FoodAllergy", "None")
    pref = user_profile.get("DietaryPreference", "Vegetarian")
    med = user_profile.get("MedicalCondition", "None")
    goal = user_profile.get("FitnessGoal", "Maintenance")

    name_lower = food_name.lower()
    allergens_lower = str(allergens_str).lower()

    # 1. ALLERGY CHECK
    if allergy and allergy != "None":
        allergy_keywords = {
            "Nuts": ["almond", "walnut", "pistachio", "cashew", "nut", "brazil nut", "hazelnut", "pecan", "pine nut"],
            "Peanuts": ["peanut"],
            "Dairy": ["milk", "yogurt", "cheese", "paneer", "whey", "cream", "butter", "ghee", "curd", "feta", "mozzarella", "ricotta", "naan", "bhatura", "raita", "cheesy", "skyar", "skyr"],
            "Gluten": ["wheat", "toast", "bread", "flour", "pasta", "bhatura", "puri", "parotta", "semolina", "rava", "dalia", "barley", "rye", "spelt", "freekeh", "seitan", "upma", "thepla", "semiya"],
            "Wheat": ["wheat", "toast", "bread", "flour", "pasta", "bhatura", "puri", "parotta", "semolina", "rava", "dalia", "seitan", "upma", "thepla", "semiya"],
            "Eggs": ["egg", "omelet", "frittata", "scramble"],
            "Soy": ["tofu", "tempeh", "soy", "edamame", "soya", "chaap"],
            "Seafood": ["salmon", "tuna", "cod", "tilapia", "sardines", "mackerel", "anchovies", "fish", "prawn", "crab", "lobster", "seafood", "pomfret", "surmai", "bangda"],
            "Shellfish": ["shrimp", "prawn", "crab", "lobster", "shellfish"],
            "Sesame": ["sesame", "til", "tahini", "kanchipuram"],
            "Mustard": ["mustard", "sarson"],
            "Corn": ["corn", "polenta", "makki"],
            "Coconut": ["coconut", "appam", "avial", "chettinad", "thoran", "poriyal"],
            "Chocolate": ["chocolate", "cacao", "cocoa"],
            "Citrus": ["lemon", "lime", "orange", "grapefruit", "amla", "mosambi", "citrus"],
            "Artificial Sweeteners": ["artificial", "aspartame", "sucralose", "diet"]
        }
        
        # Check explicit allergens string
        if allergy.lower() in allergens_lower:
            return False, f"This food contains explicit allergen tag '{allergy}' associated with your selected allergy restriction."

        keywords = allergy_keywords.get(allergy, [allergy.lower()])
        for kw in keywords:
            if kw in name_lower:
                return False, f"This food contains '{kw.title()}' which violates your selected '{allergy}' allergy restriction."

    # 2. DIETARY PREFERENCE CHECK
    if row_dict:
        if pref == "Vegan" and not row_dict.get("IsVegan", True):
            return False, "This food contains animal-derived or dairy ingredients violating your Vegan preference."
        if pref == "Vegetarian" and not row_dict.get("IsVegetarian", True):
            return False, "This food contains meat, poultry, or fish violating your Vegetarian preference."
        if pref == "Eggetarian" and not (row_dict.get("IsVegetarian", True) or row_dict.get("IsEggetarian", False)):
            return False, "This food contains meat or fish violating your Eggetarian preference."
        if pref == "Jain" and not row_dict.get("IsJain", True):
            return False, "This food contains root vegetables (onion, garlic, potato) or animal products violating Jain restrictions."

    is_nonveg = any(w in name_lower for w in ["chicken", "salmon", "tuna", "cod", "tilapia", "turkey", "beef", "mutton", "shrimp", "prawn", "crab", "lobster", "fish", "meat", "duck", "pomfret", "surmai", "bangda", "errachi"])
    is_egg = any(w in name_lower for w in ["egg", "omelet", "frittata"])
    is_dairy = any(w in name_lower for w in ["yogurt", "cheese", "paneer", "whey", "cream", "butter", "ghee", "curd", "feta", "mozzarella", "ricotta", "milk", "raita", "skyr"])
    is_root_veg = any(w in name_lower for w in ["onion", "garlic", "potato", "beetroot", "carrot", "radish", "turnip", "ginger", "arbi", "jimikand"])
    is_gluten = any(w in name_lower for w in ["wheat", "toast", "bread", "flour", "pasta", "bhatura", "puri", "parotta", "semolina", "rava", "dalia", "barley", "rye", "spelt", "freekeh", "seitan", "thepla", "semiya"])

    if pref == "Vegan" and (is_nonveg or is_egg or is_dairy):
        return False, "This food contains non-vegan ingredients (meat/egg/dairy) violating your Vegan dietary preference."
    if pref == "Vegetarian" and (is_nonveg or is_egg):
        return False, "This food contains meat/poultry/fish/egg violating your Vegetarian dietary preference."
    if pref == "Eggetarian" and is_nonveg:
        return False, "This food contains meat or seafood violating your Eggetarian dietary preference."
    if pref == "Jain" and (is_nonveg or is_egg or is_root_veg):
        return False, "This food contains root vegetables or animal products violating Jain strict dietary rules."
    if pref == "Gluten Free" and is_gluten:
        return False, "This food contains gluten-bearing wheat/barley/rye grains violating your Gluten Free preference."
    if pref == "Dairy Free" and is_dairy:
        return False, "This food contains dairy products (milk/cheese/paneer/ghee/curd) violating your Dairy Free preference."

    # 3. MEDICAL RULE CHECK
    if med in ["Celiac Disease"] and is_gluten:
        return False, "Gluten grains are strictly prohibited for Celiac Disease clinical safety."
    if med in ["Lactose Intolerance"] and is_dairy:
        return False, "Dairy products containing lactose are restricted for Lactose Intolerance safety."
    if med in ["Diabetes Type 2", "Prediabetes"]:
        high_gi_sweets = ["jaggery", "sugar", "sweet pongal", "bhatura", "chole bhature", "garlic butter naan", "puri"]
        for sw in high_gi_sweets:
            if sw in name_lower:
                return False, f"High glycemic sugar/refined item '{sw.title()}' is restricted for Diabetes glycemic control."
    if med in ["Hypertension", "Heart Disease", "High Cholesterol"]:
        high_sat_fat = ["mutton", "beef", "butter chicken", "malai kofta", "bhatura"]
        for hsf in high_sat_fat:
            if hsf in name_lower:
                return False, f"High saturated fat item '{hsf.title()}' is restricted for Heart Health and Cholesterol management."

    return True, "Passed all 6 Safety Shield validation checks."
