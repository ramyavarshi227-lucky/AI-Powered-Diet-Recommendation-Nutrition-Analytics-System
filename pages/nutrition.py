import streamlit as st
import pandas as pd
import core.nutrition_utils as nu
import core.recommendation_engine as re_eng
import core.safety_shield as ss

def render_nutrition():
    st.markdown("<h1 style='color:#00E676;'>🍽 My Nutrition & Smart Meal Swap 2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Interactive 7-meal daily schedule with 6-point Safety Shield validation & Best Match swapping.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    bmi_val, _, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])

    user_input = {**p, "BMI": bmi_val}
    predicted_cat, _, _ = re_eng.predict_diet_category(user_input)

    # 🛡 SAFETY SHIELD DEMO SCENARIO FOR JUDGES
    with st.expander("🛡 DEMO SCENARIO FOR JUDGES — Test Safety Shield Violation Live", expanded=False):
        st.markdown("Select an allergy and attempt a meal swap to demonstrate how the Safety Shield blocks restricted foods:")
        d_allergy = st.selectbox("Test Demo Allergy", ["Nuts", "Dairy", "Gluten", "Seafood", "Eggs"], index=0)
        d_food = st.text_input("Test Prohibited Food Item", "Raw Almonds (23 nuts)" if d_allergy == "Nuts" else "Fresh Paneer")
        
        if st.button("🛡 Execute Safety Validation Test"):
            demo_user = {**user_input, "FoodAllergy": d_allergy}
            is_safe, reason = ss.validate_food_safety(d_food, demo_user)
            if not is_safe:
                st.markdown(f"""
                    <div style='background: rgba(255, 23, 68, 0.15); border: 2px solid #FF1744; border-radius:12px; padding:16px; margin-top:10px;'>
                        <h4 style='color:#FF1744; margin:0;'>🛡 SAFETY SHIELD ACTIVATED — MEAL BLOCKED</h4>
                        <p style='color:#E0E6ED; font-size:0.95rem; margin:5px 0 0 0;'><b>Reason:</b> “{reason}”</p>
                        <small style='color:#8A99AD;'>Restricted food was hard-blocked from being displayed or recommended.</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Food passed safety checks.")

    st.markdown("---")

    if 'current_meals_dict' not in st.session_state:
        rec_data = re_eng.generate_7_meal_recommendation(user_input, cal_req, predicted_cat)
        st.session_state.current_meals_dict = rec_data["meals"]
        st.session_state.current_meals_summary = rec_data["summary"]

    rec_meals = st.session_state.current_meals_dict
    rec_summary = st.session_state.current_meals_summary

    # Daily Summary Bar
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1: st.metric("Daily Calories", f"{rec_summary['Calories']} kcal", f"{cal_req} Target")
    with s2: st.metric("Protein", f"{rec_summary['Protein']} g")
    with s3: st.metric("Carbohydrates", f"{rec_summary['Carbs']} g")
    with s4: st.metric("Fat", f"{rec_summary['Fat']} g")
    with s5: st.metric("Fiber", f"{rec_summary['Fiber']} g")

    st.markdown("---")
    st.subheader("📋 7 Daily Meals Schedule & Smart Swap 2.0")

    for m_type, meal in rec_meals.items():
        with st.container():
            st.markdown(f"""
                <div class='glass-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h3 style='color:#00E5FF; margin:0;'>{m_type}</h3>
                        <span class='badge-gi-{meal["gi_impact"].lower()}'>GI: {meal['gi_impact']}</span>
                    </div>
                    <h4 style='color:#E0E6ED; margin:5px 0;'>{meal['name']}</h4>
                    <p style='font-size:0.9rem; color:#00E676;'>🔥 <b>{meal['calories']} kcal</b> | 💪 <b>P: {meal['protein']}g</b> | 🍚 <b>C: {meal['carbs']}g</b> | 🥑 <b>F: {meal['fat']}g</b> | 🌾 <b>Fiber: {meal['fiber']}g</b></p>
                    <p style='font-size:0.8rem; color:#8A99AD;'><b>Preparation:</b> {meal['cooking_notes']} | <b>Est. Cost:</b> ₹{meal.get('price', 50)}</p>
                </div>
                """, unsafe_allow_html=True)

            col_a, col_b = st.columns([1, 1])

            # 1. RECOMMENDATION TRACE ("WHY THIS MEAL?")
            with col_a:
                with st.expander(f"🔍 WHY THIS MEAL? ({m_type})", expanded=False):
                    trace_checks, reasoning = re_eng.generate_recommendation_trace(meal['name'], user_input, cal_req)
                    for chk in trace_checks:
                        st.markdown(f"✓ **{chk['item']}**: <span style='color:#00E676;'>{chk['detail']}</span>", unsafe_allow_html=True)
                    st.info(f"💡 {reasoning}")

            # 2. SMART MEAL SWAP 2.0
            with col_b:
                with st.expander(f"🔄 SWAP MEAL 2.0 (Top 3 Candidates)", expanded=False):
                    swaps = re_eng.swap_single_meal_2(user_input, meal, m_type, cal_req)
                    if swaps:
                        st.markdown("**Select from Safety-Verified Alternatives:**")
                        for idx, sw in enumerate(swaps):
                            match_badge = " <span style='background:#00E676; color:#0B1020; padding:2px 8px; border-radius:12px; font-weight:800; font-size:0.75rem;'>BEST MATCH</span>" if sw['is_best_match'] else ""
                            st.markdown(f"**Alternative {idx+1}**: **{sw['name']}**{match_badge}", unsafe_allow_html=True)
                            st.markdown(f"🔥 {sw['calories']} kcal | 💪 P: {sw['protein']}g | 🍚 C: {sw['carbs']}g | 🥑 F: {sw['fat']}g | 🌾 Fib: {sw['fiber']}g | 💰 ₹{sw['price']}")
                            st.caption(f"Reason: {sw['suitability_reason']}")

                            if st.button(f"Choose Alternative {idx+1} for {m_type}", key=f"swap_btn_{m_type}_{idx}"):
                                rec_meals[m_type] = sw.copy()
                                st.session_state.current_meals_dict = rec_meals
                                st.success(f"Replaced {m_type} with {sw['name']}!")
                                st.rerun()
                    else:
                        st.warning("No alternative foods found passing all 6 Safety Shield restrictions.")

        st.markdown(" ")


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
    render_nutrition()
