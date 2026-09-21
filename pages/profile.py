import streamlit as st
import core.nutrition_utils as nu

def render_profile_wizard():
    st.markdown("<h1 class='project-header'>Clinical Intake & Bio-Profiling Wizard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='project-tagline'>Enter your personal biometrics, health goals, and medical preferences for AI-powered dietary recommendations.</p>", unsafe_allow_html=True)
    st.markdown("---")

    if 'profile_wizard_step' not in st.session_state:
        st.session_state.profile_wizard_step = 1

    step = st.session_state.profile_wizard_step
    p = st.session_state.patient_profile

    st.progress(step / 6.0, text=f"Clinical Wizard Step {step} of 6 ({(step/6)*100:.0f}% Complete)")

    if step == 1:
        st.subheader("Step 1: Basic Information & Biometrics")
        c1, c2 = st.columns(2)
        with c1:
            p["Name"] = st.text_input("Patient Name", p.get("Name", "Alex Mercer"))
            p["Age"] = st.number_input("Age (Years)", 18, 100, p.get("Age", 28))
            g_opts = ["Male", "Female", "Transgender"]
            curr_g = p.get("Gender", "Male")
            g_idx = g_opts.index(curr_g) if curr_g in g_opts else 0
            p["Gender"] = st.selectbox("Gender Identity", g_opts, index=g_idx)
        with c2:
            p["Height"] = st.number_input("Height (cm)", 120, 220, p.get("Height", 175))
            p["Weight"] = st.number_input("Weight (kg)", 30.0, 200.0, float(p.get("Weight", 74.0)), step=0.5)

        bmi, cat, _ = nu.calculate_bmi(p["Weight"], p["Height"])
        bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
        st.info(f"📊 Auto-Calculated BMI: **{bmi}** ({cat}) | BMR Baseline: **{bmr} kcal/day**")

    elif step == 2:
        st.subheader("Step 2: Lifestyle & Activity Levels")
        act_opts = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"]
        curr_act = p.get("ActivityLevel", "Moderately Active")
        act_idx = act_opts.index(curr_act) if curr_act in act_opts else 2
        p["ActivityLevel"] = st.selectbox("Activity Level", act_opts, index=act_idx)

        occ_opts = ["Student", "Office Worker", "Teacher", "Homemaker", "Manual Labor", "Healthcare Worker", "Retired"]
        curr_occ = p.get("Occupation", "Office Worker")
        occ_idx = occ_opts.index(curr_occ) if curr_occ in occ_opts else 1
        p["Occupation"] = st.selectbox("Occupation", occ_opts, index=occ_idx)

        p["DailySteps"] = st.number_input("Average Daily Steps", 1000, 30000, p.get("DailySteps", 8500), step=500)
        p["WaterIntake_L"] = st.number_input("Daily Water Intake (L)", 0.5, 6.0, float(p.get("WaterIntake_L", 3.0)), step=0.1)
        p["Sleep_Hours"] = st.number_input("Nightly Sleep (Hours)", 4.0, 12.0, float(p.get("Sleep_Hours", 7.5)), step=0.5)

    elif step == 3:
        st.subheader("Step 3: Primary Fitness & Health Goals")
        goal_opts = [
            "Weight Loss", "Fat Loss", "Weight Gain", "Maintenance", "Muscle Gain", "Lean Muscle", "Strength Training",
            "Endurance Training", "Athletic Performance", "Diabetic Control", "Heart Health", "Low Cholesterol"
        ]
        curr_goal = p.get("FitnessGoal", "Weight Loss")
        goal_idx = goal_opts.index(curr_goal) if curr_goal in goal_opts else 0
        p["FitnessGoal"] = st.selectbox("Primary Goal", goal_opts, index=goal_idx)

        bud_opts = [1500, 2000, 2500, 3000, 3500, 4000, 5000]
        curr_bud = p.get("WeeklyBudget_INR", 2500)
        bud_val = curr_bud if curr_bud in bud_opts else 2500
        p["WeeklyBudget_INR"] = st.select_slider("Weekly Grocery Budget Cap (₹)", options=bud_opts, value=bud_val)

    elif step == 4:
        st.subheader("Step 4: Clinical Medical Conditions")
        med_opts = [
            "None", "Diabetes Type 2", "Prediabetes", "Hypertension", "Obesity", "High Cholesterol", "Heart Disease",
            "PCOS", "Hypothyroidism", "Hyperthyroidism", "IBS", "GERD", "Celiac Disease", "Lactose Intolerance"
        ]
        curr_med = p.get("MedicalCondition", "None")
        med_idx = med_opts.index(curr_med) if curr_med in med_opts else 0
        p["MedicalCondition"] = st.selectbox("Medical Condition", med_opts, index=med_idx)

    elif step == 5:
        st.subheader("Step 5: Clinical Food Allergies & Exclusions")
        alg_opts = [
            "None", "Nuts", "Peanuts", "Dairy", "Gluten", "Wheat", "Eggs", "Soy",
            "Seafood", "Shellfish", "Sesame", "Mustard", "Corn", "Coconut", "Citrus"
        ]
        curr_alg = p.get("FoodAllergy", "None")
        alg_idx = alg_opts.index(curr_alg) if curr_alg in alg_opts else 0
        p["FoodAllergy"] = st.selectbox("Food Allergy", alg_opts, index=alg_idx)

    elif step == 6:
        st.subheader("Step 6: Dietary Preference & Regional Taste")
        pref_opts = [
            "Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Jain", "Mediterranean",
            "South Indian", "North Indian", "High Protein", "Low Carb", "Gluten Free", "Dairy Free"
        ]
        curr_pref = p.get("DietaryPreference", "Vegetarian")
        pref_idx = pref_opts.index(curr_pref) if curr_pref in pref_opts else 0
        p["DietaryPreference"] = st.selectbox("Dietary Preference", pref_opts, index=pref_idx)

    st.markdown(" ")
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        if step > 1:
            if st.button("← Previous Step"):
                st.session_state.profile_wizard_step -= 1
                st.rerun()
    with b3:
        if step < 6:
            if st.button("Next Step →", type="primary"):
                st.session_state.profile_wizard_step += 1
                st.rerun()
        else:
            if st.button("Run AI Analysis & Generate Plan →", type="primary"):
                if 'current_meals_dict' in st.session_state:
                    del st.session_state['current_meals_dict']
                st.session_state.active_screen = "Personalized Analysis"
                st.rerun()


if __name__ == '__main__':
    if 'patient_profile' not in st.session_state:
        st.session_state.patient_profile = {
            'Name': 'Priya Sharma', 'Age': 29, 'Gender': 'Female', 'Height': 162, 'Weight': 72.0,
            'BodyFat': 26.0, 'Waist': 80.0, 'ActivityLevel': 'Moderately Active', 'Occupation': 'Office Worker',
            'DailySteps': 8500, 'ExerciseFreq': '3-4 times / week', 'WorkoutType': 'Cardio & Pilates',
            'WaterIntake_L': 3.0, 'Sleep_Hours': 7.5, 'StressLevel': 'Moderate', 'SmokingStatus': 'Non-Smoker',
            'AlcoholConsumption': 'None', 'FitnessGoal': 'Weight Loss', 'MedicalCondition': 'None',
            'FoodAllergy': 'Nuts', 'DietaryPreference': 'South Indian', 'WeeklyBudget_INR': 2500
        }
    render_profile_wizard()
