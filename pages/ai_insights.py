import streamlit as st
import pandas as pd
import plotly.express as px
import core.nutrition_utils as nu
import core.recommendation_engine as re_eng
import core.explainable_ai as xai

def render_ai_insights():
    st.markdown("<h1 style='color:#00E676;'>🤖 AI Recommendation & What-If Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Inspect actual model prediction confidence, 10-factor XAI attribution, and run live What-If scenarios.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    bmi_val, _, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])
    health_score = nu.calculate_health_score(bmi_val, p["ActivityLevel"], p["WaterIntake_L"], p["Sleep_Hours"], p["DailySteps"], p["StressLevel"], p["SmokingStatus"], p["AlcoholConsumption"], p["MedicalCondition"])

    user_input = {**p, "BMI": bmi_val}
    predicted_cat, conf_scores, _ = re_eng.predict_diet_category(user_input)
    max_conf = max(conf_scores.values()) if conf_scores else 1.0

    st.markdown(f"### Predicted Clinical Category: <span style='color:#FF9800;'>{predicted_cat}</span> (Confidence: <span style='color:#00E676;'>{max_conf*100:.1f}%</span>)", unsafe_allow_html=True)

    # 1. CONFIDENCE-AWARE WARNING
    if max_conf < 0.60:
        st.warning("⚠️ Model confidence is limited (< 60%). Consider reviewing your profile information for underspecified inputs.")

    x1, x2 = st.columns([1, 2])
    with x1:
        st.markdown("**Confidence Probabilities**")
        prob_df = pd.DataFrame(list(conf_scores.items()), columns=["Diet Category", "Probability"]).sort_values(by="Probability", ascending=False)
        st.dataframe(prob_df, use_container_width=True, hide_index=True)
    with x2:
        st.markdown("**Probability Distribution Chart**")
        fig_p = px.bar(prob_df, x='Diet Category', y='Probability', color='Probability', color_continuous_scale='Viridis')
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E6ED'), coloraxis_showscale=False)
        st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("---")

    # 2. WHAT-IF SIMULATOR
    st.subheader("🔮 WHAT-IF SIMULATOR")
    st.markdown("Simulate how altering your goal, activity, preference, or budget cap changes your metabolic targets in real-time:")

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        sim_goal = st.selectbox("What-If Goal", ["Weight Loss", "Fat Loss", "Maintenance", "Muscle Gain", "Diabetic Control", "Keto"], index=3)
    with w2:
        sim_act = st.selectbox("What-If Activity", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"], index=4)
    with w3:
        sim_pref = st.selectbox("What-If Preference", ["Vegetarian", "Non-Vegetarian", "Vegan", "Jain", "South Indian", "North Indian"], index=0)
    with w4:
        bud_opts = [1500, 2000, 2500, 3000, 3500, 4000, 5000]
        sim_bud = st.select_slider("What-If Budget (₹)", options=bud_opts, value=3500)

    sim_results = xai.simulate_what_if(p, sim_goal, sim_act, sim_pref, sim_bud)

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1: st.metric("Simulated Category", sim_results["SimulatedCategory"])
    with sc2: st.metric("Simulated Calories", f"{sim_results['SimulatedCalories']} kcal", f"{sim_results['CalorieDelta']:+d} kcal")
    with sc3: st.metric("Simulated Protein", f"{sim_results['SimulatedMacros']['Protein_g']} g", f"{sim_results['ProteinDelta']:+d} g")
    with sc4: st.metric("Est Weekly Cost", f"₹{sim_results['SimulatedWeeklyCost']:,}")

    st.markdown("---")

    # 3. 10-FACTOR XAI NARRATIVE
    st.subheader("💡 Why Was This Recommended? (10-Factor XAI Narrative)")
    narrative = xai.get_explainable_ai_rationale_10(user_input, predicted_cat, health_score, cal_req)
    st.info(narrative)

    st.caption("Note: Machine learning models provide educational decision support suggestions and do not replace professional medical diagnosis.")


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
    render_ai_insights()
