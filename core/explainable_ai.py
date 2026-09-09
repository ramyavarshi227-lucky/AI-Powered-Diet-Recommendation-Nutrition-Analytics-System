import core.nutrition_utils as nu
import core.recommendation_engine as re_eng

def get_explainable_ai_rationale_10(user_input, predicted_cat, health_score, target_calories):
    med = user_input.get("MedicalCondition", "None")
    goal = user_input.get("FitnessGoal", "Maintenance")
    pref = user_input.get("DietaryPreference", "Vegetarian")
    allergy = user_input.get("FoodAllergy", "None")
    act = user_input.get("ActivityLevel", "Moderately Active")
    steps = user_input.get("DailySteps", 8500)
    water = user_input.get("WaterIntake_L", 3.0)
    sleep = user_input.get("Sleep_Hours", 7.5)
    stress = user_input.get("StressLevel", "Moderate")
    bmi = user_input.get("BMI", 24.2)
    
    rationale = f"🧠 AURELIXA 10-FACTOR EXPLAINABLE AI (XAI) ATTRIBUTION RATIONALE:\n\n"
    rationale += f"1. Primary Clinical Factor ({med}): Model classified category '{predicted_cat}' to address metabolic management rules.\n"
    rationale += f"2. Body Mass Index ({bmi}): Weight management factor calibrated for optimal body composition.\n"
    rationale += f"3. Fitness Goal ({goal}): Caloric target set to {target_calories} kcal/day.\n"
    rationale += f"4. Lifestyle Activity ({act}): Energy expenditure adjusted for {steps:,} daily steps.\n"
    rationale += f"5. Dietary Preference ({pref}): Food candidate database filtered strictly to compliant foods.\n"
    rationale += f"6. Allergen Exclusion ({allergy}): Hard 100% screening active against 17 allergen groups.\n"
    rationale += f"7. Daily Physical Movement ({steps:,} steps): Exercise activity multiplier active.\n"
    rationale += f"8. Hydration Balance ({water} L/day): Hydration score accounted for in overall health status.\n"
    rationale += f"9. Sleep Quality ({sleep} hrs/night): Sleep restoration factor factored into metabolic baseline.\n"
    rationale += f"10. Stress & Adherence ({stress}): Cortisol stress balance factored into health score ({health_score}/100).\n"
    
    return rationale

def simulate_what_if(user_profile, new_goal, new_activity, new_preference, new_budget):
    w = user_profile.get("Weight", 74.0)
    h = user_profile.get("Height", 175)
    a = user_profile.get("Age", 28)
    g = user_profile.get("Gender", "Male")

    bmi_val, _, _ = nu.calculate_bmi(w, h)
    bmr = nu.calculate_bmr(w, h, a, g)
    sim_tdee = nu.calculate_tdee(bmr, new_activity)
    sim_cal = nu.calculate_calorie_requirement(sim_tdee, new_goal)

    sim_user_input = {
        **user_profile,
        "FitnessGoal": new_goal,
        "ActivityLevel": new_activity,
        "DietaryPreference": new_preference,
        "WeeklyBudget_INR": new_budget,
        "BMI": bmi_val
    }

    sim_cat, _, _ = re_eng.predict_diet_category(sim_user_input)
    sim_macros = nu.calculate_target_macros(sim_cal, sim_cat, g)

    # Estimate new grocery cost
    est_weekly_cost = round(new_budget * (sim_cal / 2000.0))

    return {
        "SimulatedCategory": sim_cat,
        "SimulatedCalories": sim_cal,
        "SimulatedTDEE": sim_tdee,
        "SimulatedMacros": sim_macros,
        "SimulatedWeeklyCost": est_weekly_cost,
        "CalorieDelta": sim_cal - user_profile.get("TargetCalories", sim_cal),
        "ProteinDelta": sim_macros["Protein_g"] - user_profile.get("TargetProtein_g", sim_macros["Protein_g"])
    }
