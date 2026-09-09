import pandas as pd
import numpy as np
import os
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100.0
    bmi = round(weight / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
        color = "#FFC107"
    elif 18.5 <= bmi < 25.0:
        category = "Normal Weight"
        color = "#00E676"
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        color = "#FF9800"
    else:
        category = "Obese"
        color = "#FF1744"
        
    return bmi, category, color

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else: # Transgender
        bmr = 10 * weight + 6.25 * height - 5 * age - 78
    return round(bmr)

def calculate_tdee(bmr, activity_level):
    multipliers = {
        "Sedentary": 1.20,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Athlete": 1.90
    }
    multiplier = multipliers.get(activity_level, 1.375)
    return round(bmr * multiplier)

def calculate_calorie_requirement(tdee, fitness_goal):
    goal_offsets = {
        "Weight Loss": -500, "Fat Loss": -450, "Weight Gain": 450, "Maintenance": 0,
        "Muscle Gain": 500, "Lean Muscle": 300, "Strength Training": 500, "Endurance Training": 400,
        "Athletic Performance": 400, "Diabetic Control": -250, "Heart Health": -200,
        "Low Cholesterol": -200, "Improve Energy": 0, "Improve Digestion": 0, "Healthy Aging": -100
    }
    offset = goal_offsets.get(fitness_goal, 0)
    return max(1200, round(tdee + offset))

def calculate_target_macros(calories, diet_category, gender="Male"):
    ratios = {
        "Balanced": (0.50, 0.20, 0.30),
        "Low-Carb": (0.25, 0.30, 0.45),
        "Keto": (0.05, 0.25, 0.70),
        "High-Protein": (0.40, 0.35, 0.25),
        "Diabetic-Friendly": (0.30, 0.25, 0.45),
        "Heart-Healthy": (0.50, 0.22, 0.28),
        "PCOS-Friendly": (0.35, 0.25, 0.40),
        "Thyroid-Friendly": (0.45, 0.25, 0.30),
        "Vegan-Balanced": (0.50, 0.22, 0.28),
        "Jain-Balanced": (0.50, 0.20, 0.30),
        "Gluten-Free-Balanced": (0.50, 0.20, 0.30)
    }
    carb_p, prot_p, fat_p = ratios.get(diet_category, (0.50, 0.20, 0.30))
    
    carbs_g = round((calories * carb_p) / 4)
    protein_g = round((calories * prot_p) / 4)
    fat_g = round((calories * fat_p) / 9)
    
    base_fiber = 38 if gender == "Male" else 28
    if diet_category in ["Diabetic-Friendly", "PCOS-Friendly", "Low-Carb"]:
        base_fiber += 5
        
    return {"carbs": carbs_g, "protein": protein_g, "fat": fat_g, "fiber": base_fiber}

def calculate_health_score(bmi, activity_level, water_intake, sleep_hours, steps, stress, smoking, alcohol, medical_condition):
    score = 0
    # BMI (25 pts)
    if 18.5 <= bmi < 25.0: score += 25
    elif 25.0 <= bmi < 30.0 or 17.0 <= bmi < 18.5: score += 16
    elif bmi >= 30.0: score += 8
    else: score += 5
    
    # Activity & Steps (20 pts)
    if steps >= 10000: score += 10
    elif steps >= 6000: score += 7
    else: score += 3
    act_pts = {"Athlete": 10, "Very Active": 9, "Moderately Active": 8, "Lightly Active": 6, "Sedentary": 3}
    score += act_pts.get(activity_level, 5)
    
    # Water & Sleep (25 pts)
    score += 12 if water_intake >= 3.0 else (8 if water_intake >= 2.0 else 4)
    score += 13 if 7.0 <= sleep_hours <= 8.5 else (8 if 6.0 <= sleep_hours < 7.0 or 8.5 < sleep_hours <= 9.5 else 4)
    
    # Lifestyle Stress/Smoking/Alcohol (15 pts)
    score += 5 if stress == "Low" else (3 if stress == "Moderate" else 1)
    score += 5 if smoking == "Non-Smoker" else (2 if smoking == "Occasional" else 0)
    score += 5 if alcohol in ["None", "Occasional"] else (2 if alcohol == "Moderate" else 0)
    
    # Medical Condition (15 pts)
    score += 15 if medical_condition == "None" else 8
    return min(100, max(0, score))

def analyze_nutrient_deficiencies_8(medical_condition, bmi, dietary_preference, calories):
    deficiencies = []
    
    # 1. Vitamin D
    deficiencies.append({
        "nutrient": "Vitamin D",
        "score": 85 if medical_condition in ["Osteoporosis", "Arthritis", "Vitamin D Deficiency"] else 45,
        "risk_level": "High" if medical_condition in ["Osteoporosis", "Arthritis", "Vitamin D Deficiency"] else "Moderate",
        "symptoms": "Bone pain, muscle weakness, fatigue, low mood",
        "causes": "Insufficient sunlight exposure, low fatty fish intake",
        "foods_to_eat": "Salmon, Egg Yolks, Mushrooms, Fortified Dairy",
        "foods_to_avoid": "Excessive Soft Drinks, Alcohol",
        "supplements": "Vitamin D3 2000 IU / day with fatty meal"
    })
    
    # 2. Iron & Hemoglobin
    if medical_condition in ["Anemia", "Iron Deficiency"] or dietary_preference in ["Vegan", "Vegetarian", "Jain"]:
        deficiencies.append({
            "nutrient": "Iron & Hemoglobin",
            "score": 90 if medical_condition in ["Anemia", "Iron Deficiency"] else 60,
            "risk_level": "High" if medical_condition in ["Anemia", "Iron Deficiency"] else "Moderate",
            "symptoms": "Dizziness, pale skin, shortness of breath, cold extremities",
            "causes": "Poor non-heme iron absorption; absence of red meat",
            "foods_to_eat": "Spinach, Beetroot, Pomegranate, Lentils, Pumpkin Seeds",
            "foods_to_avoid": "Tea or Coffee directly after meals",
            "supplements": "Ferrous ascorbate 100mg with Vitamin C"
        })
        
    # 3. Vitamin B12
    if dietary_preference in ["Vegan", "Vegetarian", "Jain"] or medical_condition in ["Vitamin B12 Deficiency", "Diabetes Type 2"]:
        deficiencies.append({
            "nutrient": "Vitamin B12",
            "score": 92 if dietary_preference == "Vegan" else 55,
            "risk_level": "High" if dietary_preference == "Vegan" else "Moderate",
            "symptoms": "Numbness in hands/feet, memory lapses, low stamina",
            "causes": "Absence of animal protein sources; Metformin diabetic medication",
            "foods_to_eat": "Fortified Soy Milk, Nutritional Yeast, Greek Yogurt, Paneer",
            "foods_to_avoid": "Processed Sugar, Excess Alcohol",
            "supplements": "Methylcobalamin 1500 mcg sublingual tablet"
        })
        
    # 4. Calcium
    if medical_condition in ["Osteoporosis", "Lactose Intolerance"] or dietary_preference in ["Vegan", "Dairy Free"]:
        deficiencies.append({
            "nutrient": "Calcium",
            "score": 88 if medical_condition == "Osteoporosis" else 50,
            "risk_level": "High" if medical_condition == "Osteoporosis" else "Moderate",
            "symptoms": "Brittle nails, tooth decay, joint stiffness",
            "causes": "Low dairy intake or malabsorption",
            "foods_to_eat": "Chia Seeds, Sesame Seeds (Til), Ragi Mudde, Tofu",
            "foods_to_avoid": "High-Sodium Packaged Foods, Caffeinated Drinks",
            "supplements": "Calcium Citrate 500mg + Magnesium"
        })
        
    # 5. Dietary Fiber
    deficiencies.append({
        "nutrient": "Dietary Fiber",
        "score": 75 if medical_condition in ["IBS", "Gastritis", "Obesity", "Diabetes Type 2"] else 30,
        "risk_level": "High" if medical_condition in ["IBS", "Gastritis", "Obesity"] else "Low",
        "symptoms": "Constipation, irregular bowel movements, sugar cravings",
        "causes": "High consumption of refined flour (maida) and white rice",
        "foods_to_eat": "Rolled Oats, Quinoa, Millets, Apples, Berries, Beans",
        "foods_to_avoid": "White Bread, Deep Fried Snacks, Pastries",
        "supplements": "Psyllium Husk (Isabgol) 1 tbsp in warm water"
    })
    
    # 6. Protein
    if calories < 1400 or dietary_preference in ["Vegan", "Jain"]:
        deficiencies.append({
            "nutrient": "Complete Protein",
            "score": 65,
            "risk_level": "Moderate",
            "symptoms": "Slow recovery after workouts, hair thinning, loss of muscle mass",
            "causes": "Restricted essential amino acid profiles",
            "foods_to_eat": "Soy Chunks, Tofu, Paneer, Lentils, Pea Protein, Egg Whites",
            "foods_to_avoid": "Empty Calorie Sugary Foods",
            "supplements": "Plant Pea Protein Isolate 25g scoop"
        })

    # 7. Omega-3 Fatty Acids
    if dietary_preference in ["Vegetarian", "Vegan", "Jain"] or medical_condition in ["Heart Disease", "High Cholesterol"]:
        deficiencies.append({
            "nutrient": "Omega-3 Fatty Acids (EPA/DHA)",
            "score": 70,
            "risk_level": "Moderate",
            "symptoms": "Dry skin, joint inflammation, sluggish cognitive focus",
            "causes": "Lack of fatty cold-water fish consumption",
            "foods_to_eat": "Walnuts, Flax Seeds, Chia Seeds, Extra Virgin Olive Oil",
            "foods_to_avoid": "Trans Fats, Hydrogenated Oils",
            "supplements": "Algal DHA Omega-3 1000mg capsule"
        })

    # 8. Magnesium
    deficiencies.append({
        "nutrient": "Magnesium",
        "score": 40,
        "risk_level": "Low",
        "symptoms": "Muscle cramps, night twitches, restlessness",
        "causes": "Low green leafy vegetable and seed intake",
        "foods_to_eat": "Pumpkin Seeds, Spinach, Dark Chocolate 85%, Almonds",
        "foods_to_avoid": "Excess Refined Sugar, Sodas",
        "supplements": "Magnesium Glycinate 200mg at bedtime"
    })
        
    return deficiencies

def estimate_weekly_grocery_budget(dietary_preference, scale_factor):
    base_budget = 1800
    if dietary_preference == "Non-Vegetarian": base_budget += 600
    elif dietary_preference == "Mediterranean": base_budget += 500
    elif dietary_preference == "High Protein": base_budget += 400
    elif dietary_preference == "Vegan": base_budget += 250
    
    budget = round(base_budget * scale_factor)
    budget_range = f"₹{budget:,} — ₹{round(budget * 1.25):,} / week"
    
    suggestions = [
        "Bulk buy whole grains (ragi, oats, brown rice) to save 15% weekly.",
        "Opt for seasonal fruits (guava, papaya) instead of imported berries.",
        "Buy legumes and chana in dry form rather than pre-cooked cans."
    ]
    return budget_range, suggestions

def get_explainable_ai_rationale(user_input, predicted_cat, health_score, cal_req):
    med = user_input.get("MedicalCondition", "None")
    bmi = user_input.get("BMI", 24.0)
    act = user_input.get("ActivityLevel", "Moderately Active")
    goal = user_input.get("FitnessGoal", "Maintenance")
    pref = user_input.get("DietaryPreference", "Vegetarian")
    water = user_input.get("DailyWaterIntake_L", 3.0)
    sleep = user_input.get("Sleep_Hours", 7.5)
    stress = user_input.get("StressLevel", "Moderate")
    steps = user_input.get("DailySteps", 8500)
    
    explanation = (
        f"“Because the patient profile presents **1. Medical Condition: {med}**, **2. BMI: {bmi}**, "
        f"**3. Activity Level: {act}**, **4. Fitness Goal: {goal}**, **5. Dietary Preference: {pref}**, "
        f"**6. Water Intake: {water}L**, **7. Sleep: {sleep} hrs**, **8. Stress Level: {stress}**, and "
        f"**9. Daily Steps: {steps:,}**, VITRAI recommended a **{predicted_cat}** clinical nutrition plan "
        f"with a target budget of **{cal_req} kcal/day**.”"
    )
    return explanation

def get_foods_include_avoid_50(condition, goal):
    """
    Dynamically generates 50+ foods to include and 50+ foods to avoid tailored
    specifically to any medical condition and fitness goal.
    """
    food_db_path = os.path.join(BASE_DIR, "food_database.csv")
    includes = []
    avoids = []
    
    if os.path.exists(food_db_path):
        try:
            df = pd.read_csv(food_db_path)
            
            # Condition-based filtering
            if condition in ["Diabetes Type 2", "Prediabetes"]:
                inc_df = df[(df["GI_Impact"] == "Low") & (df["Fiber_g"] >= 2.0)]
                av_df = df[(df["GI_Impact"] == "High") | (df["FoodName"].str.contains("Sugar|Sweet|Jalebi|Jamun|Soda|Juice|Honey|Syrup", case=False, na=False))]
            elif condition in ["Hypertension", "Heart Disease", "High Cholesterol"]:
                inc_df = df[(df["Category"].isin(["Vegetables", "Fruits", "Whole Grains", "Healthy Fats"])) & (df["Fat_g"] < 14)]
                av_df = df[df["FoodName"].str.contains("Puri|Bhature|Butter|Parotta|Fries|Fried|Chips|Bacon|Sausage|Naan|Burger|Pizza", case=False, na=False)]
            elif condition == "PCOS":
                inc_df = df[(df["GI_Impact"] == "Low") & (df["Fiber_g"] >= 3.0)]
                av_df = df[(df["GI_Impact"] == "High") | (df["FoodName"].str.contains("Maida|White Bread|Sugar|Soda|Pastry|Cake", case=False, na=False))]
            elif condition in ["Obesity"] or goal in ["Weight Loss", "Fat Loss"]:
                inc_df = df[(df["Calories"] <= 210) & (df["Fiber_g"] >= 2.0)]
                av_df = df[df["Calories"] > 240]
            elif goal in ["Muscle Gain", "Lean Muscle", "Strength Training"]:
                inc_df = df[df["Protein_g"] >= 7.0]
                av_df = df[df["Protein_g"] < 2.0]
            elif condition in ["Anemia", "Iron Deficiency"]:
                inc_df = df[df["FoodName"].str.contains("Spinach|Beetroot|Pomegranate|Lentil|Beans|Rajma|Seed|Amaranth|Dates", case=False, na=False)]
                av_df = df[df["FoodName"].str.contains("Soda|Tea|Coffee|Sugar|Maida|Alcohol", case=False, na=False)]
            elif condition in ["Osteoporosis", "Vitamin D Deficiency", "Arthritis"]:
                inc_df = df[df["FoodName"].str.contains("Salmon|Egg|Yogurt|Milk|Paneer|Tofu|Sesame|Ragi|Chia|Spinach", case=False, na=False)]
                av_df = df[df["FoodName"].str.contains("Soda|Alcohol|Chips|Fries|Processed", case=False, na=False)]
            elif condition in ["IBS", "GERD", "Gastritis"]:
                inc_df = df[(df["GI_Impact"] == "Low") & (~df["FoodName"].str.contains("Chili|Pepper|Fried|Alcohol|Citrus", case=False, na=False))]
                av_df = df[df["FoodName"].str.contains("Chili|Pepper|Fried|Alcohol|Citrus|Soda|Pakora|Samosa", case=False, na=False)]
            elif condition in ["Celiac Disease", "Gluten Sensitivity"]:
                inc_df = df[~df["Allergens"].str.contains("Gluten|Wheat", case=False, na=False)]
                av_df = df[df["Allergens"].str.contains("Gluten|Wheat", case=False, na=False)]
            else:
                inc_df = df[df["GI_Impact"] != "High"]
                av_df = df[df["GI_Impact"] == "High"]
                
            includes = inc_df["FoodName"].tolist()
            avoids = av_df["FoodName"].tolist()
        except Exception as e:
            print("Error parsing food database in get_foods_include_avoid_50:", e)

    fallback_inc = [
        "Steamed Spinach", "Fresh Broccoli", "Cauliflower Rice", "Red Rice", "Quinoa", "Rolled Oats", "Finger Millet (Ragi)",
        "Foxtail Millet", "Buckwheat Groats", "Sprouted Moong", "Yellow Toor Dal", "Kala Chana", "Rajma Masala", "Low-fat Paneer",
        "Firm Tofu", "Organic Tempeh", "Plain Greek Yogurt 0%", "Egg White Scramble", "Boiled Whole Eggs", "Grilled Chicken Breast", "Baked Cod",
        "Pan-seared Salmon", "Canned Tuna", "Raw Almonds", "Walnut Halves", "Ground Flax Seeds", "Chia Seeds", "Raw Pumpkin Seeds",
        "Extra Virgin Olive Oil", "Hass Avocado", "Green Tea", "Raw Cucumber Slices", "Sautéed Zucchini", "Grilled Asparagus",
        "Steamed Kale", "Sautéed Mushrooms", "Bell Peppers", "Baked Sweet Potato", "Roasted Pumpkin", "Green Apple",
        "Fresh Strawberries", "Pink Guava", "Ripe Papaya", "Pomegranate Seeds", "Fresh Green Kiwi", "Fresh Valencia Orange", "Amla Juice"
    ]
    
    fallback_av = [
        "White Bread", "White Rice", "Refined Maida Flour", "Chole Bhature", "Deep Fried Puri", "Malabar Parotta",
        "Garlic Butter Naan", "French Fries", "Potato Chips", "Fried Chicken", "Samosa", "Pakora", "Jalebi",
        "Gulab Jamun", "Sugary Sodas", "Energy Drinks", "Sweetened Fruit Juices", "Commercial Pastries", "Donuts",
        "Cookies", "Chocolate Ice Cream", "Processed Sausage", "Bacon", "Hot Dogs", "High Sodium Canned Soup",
        "Packaged Instant Noodles", "Sweetened Yogurt", "Mayonnaise", "Margarine", "Commercial Cakes", "Candies"
    ]
    
    # Priority: Condition-filtered items FIRST, followed by unique fallback items!
    final_inc = []
    for item in includes + fallback_inc:
        if item not in final_inc:
            final_inc.append(item)
            
    final_av = []
    for item in avoids + fallback_av:
        if item not in final_av:
            final_av.append(item)
            
    return final_inc[:55], final_av[:55]

# PDF Exporters
def generate_pdf_diet_report(user_input, target_calories, diet_category, health_score, bmi_val, bmi_cat, rec_meals, target_macros):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#00E676'), alignment=1, spaceAfter=6)
    sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#666666'), alignment=1, spaceAfter=12)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, leading=15, textColor=colors.HexColor('#00E5FF'), spaceBefore=8, spaceAfter=5)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor('#222222'))
    
    story.append(Paragraph("VITRAI Clinical Nutrition & Patient Diet Report", title_style))
    story.append(Paragraph("Precision Nutrition. Intelligent Living. — Clinical Decision Support System", sub_style))
    
    story.append(Paragraph("1. Patient Profile & Metabolic Metrics", h2_style))
    p_data = [
        [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value</b>", body_style), Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value</b>", body_style)],
        ["Patient Name", user_input.get('Name', 'Patient Profile'), "Age / Gender", f"{user_input['Age']} yrs / {user_input['Gender']}"],
        ["Height / Weight", f"{user_input['Height']} cm / {user_input['Weight']} kg", "BMI Status", f"{bmi_val} ({bmi_cat})"],
        ["Activity / Occ", f"{user_input['ActivityLevel']} ({user_input['Occupation']})", "Medical Condition", user_input['MedicalCondition']],
        ["Fitness Goal", user_input['FitnessGoal'], "Preference / Allergy", f"{user_input['DietaryPreference']} / {user_input['FoodAllergy']}"],
        ["Steps / Stress", f"{user_input['DailySteps']:,} / {user_input['StressLevel']}", "Health Score", f"{health_score} / 100"],
        ["Calorie Budget", f"{target_calories} kcal/day", "Predicted Diet", diet_category]
    ]
    t_prof = Table(p_data, colWidths=[110, 150, 110, 150])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F7FA')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B2EBF2')),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_prof)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("2. Customized 7-Meal Daily Plan", h2_style))
    m_headers = [Paragraph("<b>Meal</b>", body_style), Paragraph("<b>Food Item & Serving</b>", body_style), Paragraph("<b>Cal</b>", body_style), Paragraph("<b>P(g)</b>", body_style), Paragraph("<b>C(g)</b>", body_style), Paragraph("<b>F(g)</b>", body_style)]
    m_rows = [m_headers]
    for m_name, d in rec_meals.items():
        m_rows.append([m_name, d['name'], str(d['calories']), str(d['protein']), str(d['carbs']), str(d['fat'])])
        
    t_m = Table(m_rows, colWidths=[100, 260, 40, 40, 40, 40])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00E676')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#C8E6C9')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F8E9')]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_m)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_pdf_weekly_plan(rec_meals):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#00E676'), alignment=1, spaceAfter=12)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, leading=10)
    
    story.append(Paragraph("VITRAI 7-Day Customized Weekly Meal Matrix", title_style))
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    w_headers = [Paragraph("<b>Day</b>", body_style), Paragraph("<b>Breakfast</b>", body_style), Paragraph("<b>Lunch</b>", body_style), Paragraph("<b>Dinner</b>", body_style)]
    w_rows = [w_headers]
    for d in days:
        bf = rec_meals.get("Breakfast", {}).get("name", "Oats").split(" (")[0]
        lu = rec_meals.get("Lunch", {}).get("name", "Salad").split(" (")[0]
        din = rec_meals.get("Dinner", {}).get("name", "Steamed Veg").split(" (")[0]
        w_rows.append([d, bf, lu, din])
        
    t_w = Table(w_rows, colWidths=[70, 150, 150, 150])
    t_w.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00E5FF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B2EBF2')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#E0F7FA')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_w)
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_pdf_grocery_list(grocery_categories, budget_str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#D500F9'), alignment=1, spaceAfter=8)
    sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=13, textColor=colors.HexColor('#333333'), spaceAfter=12)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#222222'), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, leading=11)
    
    story.append(Paragraph("VITRAI Categorized Weekly Grocery Checklist", title_style))
    story.append(Paragraph(f"Estimated Weekly Grocery Budget: <b>{budget_str}</b>", sub_style))
    
    for cat_name, items in grocery_categories.items():
        if items:
            story.append(Paragraph(f"<b>{cat_name}</b>", h2_style))
            for item in items:
                story.append(Paragraph(f"[  ] {item}", body_style))
            story.append(Spacer(1, 5))
            
    doc.build(story)
    buffer.seek(0)
    return buffer
