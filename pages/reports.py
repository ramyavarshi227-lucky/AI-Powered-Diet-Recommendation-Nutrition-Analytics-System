import streamlit as st
import pandas as pd
import os
import core.nutrition_utils as nu
import core.recommendation_engine as re_eng
import core.grocery_engine as ge

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"

def render_reports():
    st.markdown("<h1 style='color:#00E676;'>📄 Clinical Reports & PDF Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Generate and download clinical PDF reports and CSV datasets.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    bmi_val, bmi_cat, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])
    health_score = nu.calculate_health_score(bmi_val, p["ActivityLevel"], p["WaterIntake_L"], p["Sleep_Hours"], p["DailySteps"], p["StressLevel"], p["SmokingStatus"], p["AlcoholConsumption"], p["MedicalCondition"])

    user_input = {**p, "BMI": bmi_val}
    predicted_cat, _, _ = re_eng.predict_diet_category(user_input)
    target_macros = nu.calculate_target_macros(cal_req, predicted_cat, p["Gender"])

    if 'current_meals_dict' not in st.session_state:
        rec_data = re_eng.generate_7_meal_recommendation(user_input, cal_req, predicted_cat)
        st.session_state.current_meals_dict = rec_data["meals"]
        st.session_state.current_meals_summary = rec_data["summary"]

    rec_meals = st.session_state.current_meals_dict
    rec_summary = st.session_state.current_meals_summary

    st.subheader("📥 ReportLab PDF Exports")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <h4>📄 Clinical Diet Report</h4>
                <p style='font-size:0.8rem; color:#8A99AD;'>Full profile summary, metabolic math, 7-meal daily schedule, and disclaimers.</p>
            </div>
            """, unsafe_allow_html=True)
        pdf_diet = nu.generate_pdf_diet_report(user_input, cal_req, predicted_cat, health_score, bmi_val, bmi_cat, rec_meals, target_macros)
        st.download_button("📄 Download Diet Report PDF", data=pdf_diet.getvalue(), file_name="diet_recommendation_report.pdf", mime="application/pdf", use_container_width=True)

    with r2:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <h4>📅 7-Day Weekly Matrix</h4>
                <p style='font-size:0.8rem; color:#8A99AD;'>Monday to Sunday structured meal plan table with disclaimers.</p>
            </div>
            """, unsafe_allow_html=True)
        pdf_week = nu.generate_pdf_weekly_plan(rec_meals)
        st.download_button("📅 Download Weekly Plan PDF", data=pdf_week.getvalue(), file_name="weekly_meal_plan.pdf", mime="application/pdf", use_container_width=True)

    with r3:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <h4>🛒 Categorized Grocery PDF</h4>
                <p style='font-size:0.8rem; color:#8A99AD;'>Categorized items, quantities, and budget breakdown in ₹.</p>
            </div>
            """, unsafe_allow_html=True)
        categories, cat_costs, total_cost, opt_sugs, is_over, savings, cost_swaps = ge.estimate_grocery_from_meals(rec_meals, p.get("DietaryPreference", "Vegetarian"), rec_summary.get("ScaleFactor", 1.0))
        budget_str = f"₹{total_cost:,} / week"
        pdf_groc = nu.generate_pdf_grocery_list(categories, budget_str)
        st.download_button("🛒 Download Grocery PDF", data=pdf_groc.getvalue(), file_name="grocery_list.pdf", mime="application/pdf", use_container_width=True)

    st.markdown("---")
    st.subheader("💾 Export Clinical CSV Logs")

    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        hist_path = os.path.join(BASE_DIR, "data", "user_history.csv")
        if os.path.exists(hist_path):
            df_hist = pd.read_csv(hist_path)
            csv_hist = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Export Progress Log CSV", data=csv_hist, file_name="patient_progress_history.csv", mime="text/csv", use_container_width=True)

    with c_exp2:
        food_path = os.path.join(BASE_DIR, "data", "food_database.csv")
        if not os.path.exists(food_path):
            food_path = os.path.join(BASE_DIR, "food_database.csv")
        if os.path.exists(food_path):
            df_food = pd.read_csv(food_path)
            csv_food = df_food.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Export Food Database CSV", data=csv_food, file_name="food_database.csv", mime="text/csv", use_container_width=True)


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
    render_reports()
