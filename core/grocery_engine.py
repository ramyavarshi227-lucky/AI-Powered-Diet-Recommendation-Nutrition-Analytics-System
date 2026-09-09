import pandas as pd
import numpy as np

def estimate_grocery_from_meals(meal_schedule, dietary_preference="Vegetarian", portion_scale_factor=1.0, user_weekly_budget=2500):
    categories = {
        "Vegetables & Greens": [],
        "Fresh Fruits": [],
        "Whole Grains & Millets": [],
        "Proteins & Pulses": [],
        "Dairy & Alternatives": [],
        "Healthy Fats & Seeds": [],
        "Spices & Oils": []
    }
    
    ingredient_summary = {}

    for m_type, meal in meal_schedule.items():
        fname = meal.get("name", "Food Item").split(" (")[0]
        qty_num = float(meal.get("qty", "100").split()[0]) if isinstance(meal.get("qty"), str) else 100.0
        unit = meal.get("unit", "g")
        price = float(meal.get("price", 50))

        # Aggregate across 7 days
        weekly_qty = round((qty_num * 7 * portion_scale_factor) / 100.0, 1)
        if unit == "g":
            if weekly_qty >= 1000:
                final_qty_str = f"{round(weekly_qty / 1000.0, 1)} kg"
            else:
                final_qty_str = f"{round(weekly_qty)} g"
        elif unit == "ml":
            if weekly_qty >= 1000:
                final_qty_str = f"{round(weekly_qty / 1000.0, 1)} L"
            else:
                final_qty_str = f"{round(weekly_qty)} ml"
        else:
            final_qty_str = f"{round(weekly_qty)} {unit}"

        item_cost = round(price * portion_scale_factor * 7)

        ingredient_summary[fname] = {
            "name": fname,
            "qty": final_qty_str,
            "unit": unit,
            "price": item_cost
        }

        # Categorize
        name_lower = fname.lower()
        if any(w in name_lower for w in ["spinach", "broccoli", "cabbage", "cucumber", "carrots", "beetroot", "zucchini", "asparagus", "kale", "mushroom", "peppers", "potato", "pumpkin", "karela", "lauki", "turai", "bhindi", "parwal", "tindora", "ash gourd"]):
            categories["Vegetables & Greens"].append(ingredient_summary[fname])
        elif any(w in name_lower for w in ["apple", "banana", "orange", "mosambi", "berry", "strawberries", "raspberries", "blueberries", "papaya", "guava", "kiwi", "watermelon", "pomegranate", "pear", "grapes", "mango", "pineapple", "avocado", "figs", "dates"]):
            categories["Fresh Fruits"].append(ingredient_summary[fname])
        elif any(w in name_lower for w in ["oats", "rice", "quinoa", "millet", "ragi", "bajra", "jowar", "barley", "roti", "bread", "buckwheat", "dalia", "poha", "pasta"]):
            categories["Whole Grains & Millets"].append(ingredient_summary[fname])
        elif any(w in name_lower for w in ["egg", "chicken", "turkey", "salmon", "cod", "tuna", "paneer", "tofu", "tempeh", "chana", "rajma", "dal", "lentils", "soy", "protein", "edamame", "seitan"]):
            categories["Proteins & Pulses"].append(ingredient_summary[fname])
        elif any(w in name_lower for w in ["yogurt", "milk", "curd", "cheese", "ricotta", "skyr"]):
            categories["Dairy & Alternatives"].append(ingredient_summary[fname])
        elif any(w in name_lower for w in ["almond", "walnut", "pistachio", "cashew", "flax", "chia", "pumpkin seeds", "sunflower seeds", "sesame", "olive oil", "avocado oil", "peanut butter", "ghee", "coconut oil"]):
            categories["Healthy Fats & Seeds"].append(ingredient_summary[fname])
        else:
            categories["Spices & Oils"].append(ingredient_summary[fname])

    total_weekly_cost = sum(item["price"] for cat in categories.values() for item in cat)
    
    category_costs = {cat: sum(item["price"] for item in items) for cat, items in categories.items() if items}

    # Budget Optimization & Protein Swaps
    is_over_budget = total_weekly_cost > user_weekly_budget
    savings = max(0, total_weekly_cost - user_weekly_budget)
    
    optimization_suggestions = [
        f"Buy whole grains (Ragi, Jowar, Brown Rice) in 5 kg bulk bags to save up to 20% on monthly food costs.",
        f"Opt for local seasonal fruits (Guava, Papaya, Banana) instead of imported berries for equal antioxidant value.",
        f"Batch meal-prep yellow moong dal and chole on Sundays to reduce weekday prep time and fuel consumption.",
        f"Use cold-pressed gingelly or mustard oil for tempering to maximize healthy fats within your budget."
    ]

    cost_saving_swaps = [
        {"expensive": "Grilled Chicken Breast (₹160/500g)", "cheaper": "Organic Soya Chunks (₹45/200g)", "saved": "₹115", "reason": "Soya chunks provide equal 50g protein per 100g at 70% lower cost."},
        {"expensive": "Fresh Paneer (₹90/200g)", "cheaper": "Sprouted Green Moong (₹40/250g)", "saved": "₹50", "reason": "Sprouted moong delivers high fiber protein with zero saturated fat."},
        {"expensive": "Imported Salmon Fillet (₹450/250g)", "cheaper": "Local Mackerel / Bangda (₹180/500g)", "saved": "₹270", "reason": "Mackerel offers superior Omega-3 EPA/DHA fatty acids at a fraction of the cost."}
    ]

    return categories, category_costs, total_weekly_cost, optimization_suggestions, is_over_budget, savings, cost_saving_swaps
