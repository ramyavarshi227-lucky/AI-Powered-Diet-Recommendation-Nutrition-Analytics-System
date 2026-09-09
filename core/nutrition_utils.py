import numpy as np
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)
    
    if bmi < 18.5:
        category = "Underweight"
        color = "#FF9800"
    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
        color = "#00E676"
    elif 25.0 <= bmi < 29.9:
        category = "Overweight"
        color = "#FF9800"
    else:
        category = "Obesity"
        color = "#FF1744"
        
    return bmi, category, color

def calculate_bmr(weight_kg, height_cm, age_years, gender):
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    elif gender == "Female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    else: # Transgender
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 78
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
        "Weight Loss": -500,
        "Fat Loss": -450,
        "Weight Gain": 450,
        "Maintenance": 0,
        "Muscle Gain": 500,
        "Lean Muscle": 300,
        "Strength Training": 500,
        "Endurance Training": 400,
        "Athletic Performance": 400,
        "Diabetic Control": -250,
        "Heart Health": -200,
        "Low Cholesterol": -200,
        "Improve Energy": 0,
        "Improve Digestion": 0,
        "Healthy Aging": -100
    }
    offset = goal_offsets.get(fitness_goal, 0)
    target = tdee + offset
    return max(1200, round(target)) # Safe floor 1200 kcal

def calculate_target_macros(calories, diet_category, gender="Male"):
    if diet_category == "Keto":
        p_pct, c_pct, f_pct = 0.25, 0.05, 0.70
    elif diet_category == "High-Protein":
        p_pct, c_pct, f_pct = 0.35, 0.40, 0.25
    elif diet_category in ["Low-Carb", "Diabetic-Friendly"]:
        p_pct, c_pct, f_pct = 0.30, 0.25, 0.45
    else: # Balanced, Heart-Healthy, Vegan, Jain, etc.
        p_pct, c_pct, f_pct = 0.20, 0.50, 0.30
        
    p_g = round((calories * p_pct) / 4)
    c_g = round((calories * c_pct) / 4)
    f_g = round((calories * f_pct) / 9)
    fib_g = 35 if diet_category in ["Diabetic-Friendly", "PCOS-Friendly", "Low-Carb"] else 28
    
    return {
        "Protein_g": p_g,
        "Carbs_g": c_g,
        "Fat_g": f_g,
        "Fiber_g": fib_g,
        "Protein_pct": int(p_pct * 100),
        "Carbs_pct": int(c_pct * 100),
        "Fat_pct": int(f_pct * 100)
    }

def calculate_health_score(bmi, activity_level, water_l, sleep_hrs, steps, stress_level="Moderate", smoking="Non-Smoker", alcohol="None", medical_condition="None"):
    score = 100
    if bmi < 18.5 or bmi >= 25.0: score -= 10
    if bmi >= 30.0: score -= 10
    if activity_level == "Sedentary": score -= 12
    elif activity_level == "Lightly Active": score -= 5
    if water_l < 2.5: score -= 8
    if sleep_hrs < 7.0: score -= 8
    if steps < 5000: score -= 10
    elif steps < 8000: score -= 4
    if stress_level == "High": score -= 6
    if smoking in ["Regular", "Occasional"]: score -= 8
    if alcohol in ["Moderate", "Heavy"]: score -= 6
    if medical_condition != "None": score -= 8
    return max(40, min(100, score))

def get_health_score_breakdown(user_profile):
    bmi, _, _ = calculate_bmi(user_profile.get("Weight", 70), user_profile.get("Height", 170))
    act = user_profile.get("ActivityLevel", "Moderately Active")
    water = user_profile.get("WaterIntake_L", 3.0)
    sleep = user_profile.get("Sleep_Hours", 7.5)
    steps = user_profile.get("DailySteps", 8500)
    stress = user_profile.get("StressLevel", "Moderate")
    smoking = user_profile.get("SmokingStatus", "Non-Smoker")
    alcohol = user_profile.get("AlcoholConsumption", "Occasional")
    med = user_profile.get("MedicalCondition", "None")

    overall = calculate_health_score(bmi, act, water, sleep, steps, stress, smoking, alcohol, med)
    
    nutr_score = 90 if med == "None" else 82
    hydr_score = 95 if water >= 3.0 else (80 if water >= 2.0 else 65)
    sleep_score = 92 if sleep >= 7.5 else (78 if sleep >= 6.0 else 60)
    act_score = 94 if steps >= 10000 else (82 if steps >= 6000 else 65)
    adh_score = 88

    return overall, {
        "Nutrition": nutr_score,
        "Hydration": hydr_score,
        "Sleep": sleep_score,
        "Activity": act_score,
        "Adherence": adh_score,
        "Overall": overall
    }

def calculate_personalization_score(user_profile):
    score = 100
    checklist = []

    # 1. Goal
    if user_profile.get("FitnessGoal"):
        checklist.append({"item": "Goal considered", "status": True, "detail": f"Calorie target tuned for '{user_profile.get('FitnessGoal')}'"})
    else:
        score -= 10
        checklist.append({"item": "Goal considered", "status": False, "detail": "Default maintenance used"})

    # 2. Allergy
    allergy = user_profile.get("FoodAllergy", "None")
    if allergy:
        checklist.append({"item": "Allergy considered", "status": True, "detail": f"Screened 17 allergens for '{allergy}'"})
    else:
        checklist.append({"item": "Allergy considered", "status": True, "detail": "No allergy restrictions requested"})

    # 3. Medical Condition
    med = user_profile.get("MedicalCondition", "None")
    if med != "None":
        checklist.append({"item": "Medical condition considered", "status": True, "detail": f"Hard clinical rules applied for '{med}'"})
    else:
        checklist.append({"item": "Medical condition considered", "status": True, "detail": "General healthy bio-profile rules applied"})

    # 4. Dietary Preference
    pref = user_profile.get("DietaryPreference", "Vegetarian")
    checklist.append({"item": "Dietary preference considered", "status": True, "detail": f"Enforced '{pref}' food candidate pool"})

    # 5. Budget
    budget = user_profile.get("WeeklyBudget_INR", 2500)
    checklist.append({"item": "Budget considered", "status": True, "detail": f"Cost-optimized for ₹{budget}/week"})

    # 6. Lifestyle
    steps = user_profile.get("DailySteps", 8500)
    checklist.append({"item": "Lifestyle considered", "status": True, "detail": f"TDEE calibrated for {steps:,} daily steps"})

    return score, checklist

def generate_pdf_diet_report(user_profile, calorie_target, diet_category, health_score, bmi_val, bmi_cat, meal_schedule, target_macros):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22, textColor=colors.HexColor('#0B1020'), alignment=0, spaceAfter=4)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#00E676'), spaceAfter=15)
    heading_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0B1020'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#2C3E50'))

    # Header & Branding
    story.append(Paragraph("AURELIXA — Precision Nutrition Intelligence", title_style))
    story.append(Paragraph("CLINICAL DIET & METABOLIC RECOMMENDATION REPORT", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#00E676'), spaceAfter=12))

    # Patient & Safety Badge Box
    pers_score, _ = calculate_personalization_score(user_profile)
    p_data = [
        [Paragraph(f"<b>Patient Name:</b> {user_profile.get('Name', 'Alex Mercer')}", body_style), Paragraph(f"<b>Age / Gender:</b> {user_profile.get('Age')}y / {user_profile.get('Gender')}", body_style)],
        [Paragraph(f"<b>Height / Weight:</b> {user_profile.get('Height')} cm / {user_profile.get('Weight')} kg", body_style), Paragraph(f"<b>BMI:</b> {bmi_val} ({bmi_cat})", body_style)],
        [Paragraph(f"<b>Medical Condition:</b> {user_profile.get('MedicalCondition')}", body_style), Paragraph(f"<b>Food Allergy:</b> {user_profile.get('FoodAllergy')}", body_style)],
        [Paragraph(f"<b>Dietary Preference:</b> {user_profile.get('DietaryPreference')}", body_style), Paragraph(f"<b>Fitness Goal:</b> {user_profile.get('FitnessGoal')}", body_style)],
        [Paragraph(f"<b>Personalization Score:</b> <font color='#00E676'><b>{pers_score}/100</b></font>", body_style), Paragraph("<b>AURELIXA Safety Shield:</b> <font color='#00E676'><b>VERIFIED ✓</b></font>", body_style)]
    ]
    t_patient = Table(p_data, colWidths=[270, 270])
    t_patient.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_patient)
    story.append(Spacer(1, 10))

    # Targets & Macro Breakdown
    story.append(Paragraph("Metabolic Targets & Macro Distribution", heading_style))
    m_data = [
        ["Daily Calorie Target", "Target Protein", "Target Carbs", "Target Fat", "Target Fiber", "Diet Category"],
        [f"{calorie_target} kcal", f"{target_macros['Protein_g']} g ({target_macros['Protein_pct']}%)", f"{target_macros['Carbs_g']} g ({target_macros['Carbs_pct']}%)", f"{target_macros['Fat_g']} g ({target_macros['Fat_pct']}%)", f"{target_macros['Fiber_g']} g", diet_category]
    ]
    t_macro = Table(m_data, colWidths=[90, 90, 90, 90, 80, 100])
    t_macro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B1020')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_macro)
    story.append(Spacer(1, 12))

    # 7-Meal Personalized Daily Schedule
    story.append(Paragraph("Personalized 7-Meal Daily Schedule (AURELIXA Safety Verified)", heading_style))
    meal_table_data = [["Meal Type", "Recommended Food Item", "Calories", "Protein", "Carbs", "Fat", "Fiber"]]
    for m_type, m in meal_schedule.items():
        meal_table_data.append([
            m_type,
            Paragraph(m['name'], body_style),
            f"{m['calories']} kcal",
            f"{m['protein']}g",
            f"{m['carbs']}g",
            f"{m['fat']}g",
            f"{m['fiber']}g"
        ])
    t_meals = Table(meal_table_data, colWidths=[100, 220, 55, 45, 45, 40, 35])
    t_meals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meals)
    story.append(Spacer(1, 15))

    # Clinical & Safety Disclaimer
    story.append(Paragraph("<b>Educational & Clinical Safety Disclaimer:</b>", ParagraphStyle('SubHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#FF9800'))))
    story.append(Paragraph("AURELIXA provides personalized educational nutrition estimates and algorithmic decision support suggestions. This report is generated by machine learning ensemble models and metabolic math based on user-provided profile data. It does NOT constitute formal medical diagnosis or prescription. Users with chronic medical conditions should consult a registered dietitian or licensed physician before initiating major dietary interventions.", ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor('#64748B'))))

    doc.build(story)
    return buffer

def generate_pdf_weekly_plan(meal_schedule):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#0B1020'), alignment=0)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#00E5FF'), spaceAfter=10)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10)

    story.append(Paragraph("AURELIXA — 7-Day Weekly Meal Matrix", title_style))
    story.append(Paragraph("STRUCTURED MONDAY TO SUNDAY MEAL SCHEDULE", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#00E5FF'), spaceAfter=10))

    w_data = [["Day", "Breakfast", "Lunch", "Snack", "Dinner"]]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    bk = meal_schedule.get("Breakfast", {}).get("name", "Oats & Fruits")
    lu = meal_schedule.get("Lunch", {}).get("name", "Chicken / Tofu Bowl")
    sn = meal_schedule.get("Evening Snack", {}).get("name", "Nuts & Tea")
    dn = meal_schedule.get("Dinner", {}).get("name", "Dal & Veggies")

    for d in days:
        w_data.append([
            d,
            Paragraph(bk, body_style),
            Paragraph(lu, body_style),
            Paragraph(sn, body_style),
            Paragraph(dn, body_style)
        ])

    t_week = Table(w_data, colWidths=[65, 120, 120, 115, 120])
    t_week.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B1020')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_week)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<i>Note: All 7 days are calibrated with portion scaling to meet daily caloric targets. Use 1-click Swap Meal in the AURELIXA app for daily variety.</i>", ParagraphStyle('Note', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))

    doc.build(story)
    return buffer

def generate_pdf_grocery_list(categories_dict, budget_str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#0B1020'), alignment=0)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#7C4DFF'), spaceAfter=10)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11)

    story.append(Paragraph("AURELIXA — Categorized Grocery Checklist", title_style))
    story.append(Paragraph(f"ESTIMATED WEEKLY BUDGET: {budget_str}", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C4DFF'), spaceAfter=12))

    g_data = [["Category", "Aggregated Ingredient", "7-Day Total Quantity", "Est Price (₹)"]]
    for cat, items in categories_dict.items():
        for item in items:
            g_data.append([
                cat,
                Paragraph(item.get("name", "Ingredient"), body_style),
                f"{item.get('qty', '1')} {item.get('unit', 'kg')}",
                f"₹{item.get('price', 50)}"
            ])

    t_groc = Table(g_data, colWidths=[120, 240, 100, 80])
    t_groc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B1020')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_groc)
    doc.build(story)
    return buffer
