# AURELIXA — Precision Nutrition. Intelligent Living. (Competition Final Build)

An advanced, competition-grade AI Healthcare and Clinical Nutrition Application designed for personalized dietary planning, healthcare diagnostics, lifestyle tracking, and multi-screen health monitoring. Built for a 3rd-year Computer Science and Engineering (Data Science) capstone defense.

---

## 📖 Abstract
Traditional dietary recommendations rely on static calorie guidelines that ignore individual medical histories, metabolic parameters, food allergies, occupations, and lifestyle habits. **AURELIXA** (*"Precision Nutrition. Intelligent Living."*) presents a clinical-grade **Multi-Screen AI Healthcare & Nutrition Intelligence Application**. Using a custom dataset of **2,500 synthetic patient records** built according to clinical guidelines, we train two ensemble classifiers: **Random Forest** and **Gradient Boosting**. The model classifies patients into optimal clinical diet categories (*Diabetic-Friendly, Heart-Healthy, Low-Carb, Keto, High-Protein, PCOS-Friendly, Thyroid-Friendly, Vegan-Balanced, Jain-Balanced, Gluten-Free-Balanced*) based on age, gender, BMI, 5 activity levels, 7 occupations, 24 medical conditions, 15 fitness goals, 17 food allergies, 12 dietary preferences, and lifestyle indicators.

The application features a **300+ item food database (`data/food_database.csv`)** complete with regional origins, cooking notes, healthy substitutes, quantities, units, and estimated prices in **Indian Rupees (₹)**. It computes Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE), calculates a **Personalization Score (0–100)**, executes an **AURELIXA Safety Shield 6-Point Validation Layer**, scales daily 7-meal plans with 1-click **Smart Meal Swapping 2.0 (Best Match)**, presents **Recommendation Traces ("Why This Meal?")**, estimates a **Budget-Aware Categorized Weekly Grocery Budget in ₹**, evaluates an **8-Nutrient Risk Analyzer**, and features a **What-If Simulator**, **Adaptive AI Weekly Insights**, 3 ReportLab PDF export streams, CSV log exports, **5-Minute Judge Demo Mode**, and a 16-screen progressive glassmorphism Streamlit UI.

---

## 🏆 The Five Pillars of AURELIXA

1. **PERSONALIZATION**: **Personalization Score (0–100)** with 6-factor criteria breakdown & dynamic weight calculations.
2. **SAFETY**: **AURELIXA Safety Shield** validation layer (hard-blocking allergen/preference/medical violations across daily meals, weekly matrices, swaps, grocery lists, and PDF reports).
3. **INTELLIGENCE**: **Smart Meal Swap 2.0** (Top 3 candidates with "Best Match" tagging), **Recommendation Trace** (*"Why This Meal?"*), **Adaptive AI Weekly Insights**, **What-If Simulator**, and **Confidence-Aware AI**.
4. **AFFORDABILITY**: **Budget-Aware AI** (Daily/Weekly budget caps, cost optimization, protein swaps for cost saving) & **Aggregated Ingredient Grocery Engine** with interactive checklist completion % (`72%`).
5. **CULTURAL EXCELLENCE**: Expanded **300+ Indian Food Database** (South Indian, North Indian, Regional, Jain, Vegan) & **Smart Culturally Relevant Substitutions**.

---

## 🧭 Application Navigation & Flow Map
```text
[Splash Screen] 
       ↓
[Welcome / Onboarding]
       ↓
[Clinical Profile 6-Step Wizard & Judge Demo Selector]
       ↓
[Personalized Analysis Loading & Safety Shield Validation]
       ↓
[Main App Navigation Router]
 ├── 🏠 Home Dashboard (Personalization Score & Daily AI Coach)
 ├── 🍽 My Nutrition (7 Meals + Smart Swap 2.0 + "Why This Meal?" Trace)
 ├── 📅 Weekly Plan (7-Day Matrix + Adaptive Weekly Insights)
 ├── 🛒 Grocery Intelligence (7-Day Aggregated Quantities + ₹ Budget Caps + Checklist %)
 ├── 🥗 Food Intelligence (300+ Foods Multi-Filter + Cultural Substitutions + 50+ Tables)
 ├── 📊 Health Analytics (Metabolic Gauges + Score Component Breakdown + Weight Projection)
 ├── 🧬 Medical & Nutrition Analysis (8-Nutrient Risk Indicators)
 ├── 🤖 AI Insights (Predicted Category + Confidence + 10-Factor XAI + What-If Simulator)
 ├── 📈 ML Diagnostics (RF vs GB Benchmarks & ROC Curves)
 ├── 📁 Progress Tracker (Historical Graphs + Adaptive Weekly Summaries)
 ├── 📄 Reports (ReportLab PDF Exports with Personalization & Safety Badges)
 └── ⚙ Settings (Units, Theme, Profile Reset)
```

---

## 🤖 Machine Learning Diagnostics (2,500 Records)

| Algorithm | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Saved as ml/model.pkl (Best Model)** |
| **Random Forest** | **0.9520** | **0.9572** | **0.9520** | **0.9492** | Evaluated |

---

## 💬 25 Viva Questions with Answers (Data Science / CSE Capstone)

#### 1. What is the core objective of the AURELIXA platform?
To provide a multi-screen clinical decision support application using machine learning classifiers to predict optimal diet categories while calculating metabolic energy targets (BMR/TDEE), computing a Personalization Score (0-100), running a 6-point Safety Shield validation layer, scaling 7 daily meals with 1-click Smart Swap 2.0, presenting Recommendation Traces ("Why This Meal?"), estimating weekly grocery budgets in Indian Rupees (₹), and evaluating a What-If Simulator and 8-nutrient risk analyzer.

#### 2. What machine learning algorithms were trained and compared?
We trained and compared **Random Forest** and **Gradient Boosting** classifiers on 2,500 synthetic patient records using an 80-20 stratified train-test split.

#### 3. What were the model performance metrics?
Gradient Boosting achieved **100.00% accuracy** and Random Forest achieved **95.20% accuracy** across classification metrics, with Gradient Boosting saved as `ml/model.pkl`.

#### 4. How is BMR calculated for different genders?
Using the revised Harris-Benedict formula:
* *Male*: $BMR = 10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} + 5$
* *Female*: $BMR = 10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} - 161$
* *Transgender*: $BMR = 10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} - 78$

#### 5. How does TDEE calculation handle activity levels?
By multiplying BMR with specific activity multipliers: Sedentary (1.20), Lightly Active (1.375), Moderately Active (1.55), Very Active (1.725), Athlete (1.90).

#### 6. What columns exist in `data/food_database.csv`?
`FoodID, FoodName, Category, Region, Calories, Protein_g, Carbs_g, Fat_g, Fiber_g, GlycemicIndex, GI_Impact, IsVegetarian, IsNonVeg, IsVegan, IsEggetarian, IsJain, IsSouthIndian, IsNorthIndian, IsMediterranean, Allergens, CookingNotes, HealthySubstitutes, EstQuantity, EstUnit, EstPriceINR`.

#### 7. How does the AURELIXA Safety Shield work?
Every food item undergoes 6 hard validation checks: 1. ALLERGY CHECK, 2. DIETARY PREFERENCE CHECK, 3. MEDICAL RULE CHECK, 4. CALORIE CHECK, 5. MACRO CHECK, 6. FOOD RESTRICTION CHECK. Violations hard-block the item from being displayed.

#### 8. How does Smart Meal Swap 2.0 select replacements?
It filters candidates passing the Safety Shield, ranks them by macro distance to current meal targets ($\Delta \text{Calories} + \Delta \text{Protein} + \Delta \text{Carbs} + \Delta \text{Fat}$), and tags the top candidate as **"Best Match"**.

#### 9. What is Recommendation Trace ("Why This Meal?")?
A transparency panel rendering 7 validation ticks (Goal match ✓, Calorie match ✓, Protein match ✓, Diet preference ✓, Allergy safety ✓, Medical-rule check ✓, Budget check ✓) alongside natural language reasoning.

#### 10. How is the Personalization Score (0-100) calculated?
By evaluating 6 criteria: Goal alignment, Allergen screening, Medical rule matching, Dietary preference compliance, Budget optimization, and Lifestyle/activity calibration.

#### 11. What is the What-If Simulator?
An interactive panel in AI Insights allowing users to alter Goal, Activity level, Preference, or Budget Cap live to inspect instant updates in Calorie targets, Macro splits, Recommended category, and Grocery cost.

#### 12. How does the 7-day ingredient aggregator operate?
It aggregates ingredients across all 7 daily meals, calculates 7-day total quantities (e.g. *Tomato: 1.8 kg*, *Rice: 2.5 kg*), and computes exact weekly costs in Indian Rupees (₹).

#### 13. What is Judge Demo Mode?
A 1-click selector in the sidebar/intake with 5 pre-configured judge profiles (*Weight Loss + South Indian*, *Muscle Gain + Vegetarian*, *Diabetes Control*, *Heart Health*, *Budget Student*) enabling complete 5-minute competition presentations.

#### 14. What PDF reports can be exported?
1. AURELIXA Clinical Diet Report PDF (with Personalization & Safety Badges)
2. 7-Day Weekly Meal Matrix PDF
3. Categorized Grocery Checklist PDF (with ₹ budget)

#### 15. How are food preferences like Jain or Gluten-Free supported?
Jain preferences exclude root vegetables (onion, garlic, potato) and animal products, while Gluten-Free excludes wheat, barley, rye, and flour products.

#### 16. What macro split is used for a Keto diet?
Carbohydrates: 5%, Protein: 25%, Fat: 70%.

#### 17. What macro split is used for a High-Protein diet?
Carbohydrates: 40%, Protein: 35%, Fat: 25%.

#### 18. How does the 8-Nutrient Risk Analyzer work?
It evaluates risk indicators (High Risk, Moderate Risk, Low Risk) for Vitamin D, Iron, Vitamin B12, Calcium, Protein, Fiber, Omega-3, and Magnesium based on medical condition, BMI, dietary preference, and daily calorie target.

#### 19. How are budget-aware protein swaps generated?
If estimated grocery cost exceeds the user's weekly budget cap, the engine suggests lower-cost protein alternatives (e.g., Soya Chunks instead of Chicken Breast) displaying original cost, cheaper cost, and total savings.

#### 20. How is the Health Score component breakdown displayed?
Through the "Why is my score XX?" expander rendering individual scores for Nutrition, Hydration, Sleep, Activity, Adherence, and Overall status.

#### 21. What is Adaptive AI Weekly Insights?
An adaptive engine analyzing weekly adherence history to generate wellness progress summaries (e.g. *"Your protein adherence improved this week"*).

#### 22. What is the medical safety policy of AURELIXA?
AURELIXA is an educational decision support system. It explicitly presents disclaimers stating that recommendations are educational nutrition estimates and not medical diagnoses, urging users to consult qualified healthcare professionals for medical treatment.

#### 23. How does Confidence-Aware AI function?
It displays the model's actual prediction probability ($max(predict\_proba)$) and issues a warning if model confidence falls below 60%.

#### 24. How does smart Indian substitution work?
It identifies restricted or high-calorie Indian ingredients and recommends culturally aligned replacements (Paneer → Tofu, Milk → Fortified Soy Milk, Wheat Roti → Jowar Roti, White Rice → Brown/Red Rice) verified by the Safety Shield.

#### 25. How is the interactive grocery checklist completion percentage computed?
$\text{Completion \%} = \frac{\text{Checked Items}}{\text{Total Aggregated Items}} \times 100$, updated dynamically as checkboxes are clicked.
