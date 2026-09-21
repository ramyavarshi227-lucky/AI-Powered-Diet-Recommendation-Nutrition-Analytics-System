import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import core.nutrition_utils as nu

def render_health_analytics():
    st.markdown("<h1 style='color:#00E676;'>📊 Health Analytics & Wellness Score Transparency</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Inspect your metabolic gauges and transparent component breakdown for your Health Score.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    overall_score, components = nu.get_health_score_breakdown(p)

    st.markdown(f"### Overall Wellness Score: <span style='color:#00E676;'>{overall_score}/100</span>", unsafe_allow_html=True)

    # "WHY IS MY SCORE XX?" TRANSPARENCY EXPANDER
    with st.expander(f"🔍 WHY IS MY SCORE {overall_score}? (Component Breakdown)", expanded=True):
        c_cols = st.columns(5)
        with c_cols[0]: st.metric("Nutrition Score", f"{components['Nutrition']}/100")
        with c_cols[1]: st.metric("Hydration Score", f"{components['Hydration']}/100")
        with c_cols[2]: st.metric("Sleep Score", f"{components['Sleep']}/100")
        with c_cols[3]: st.metric("Activity Score", f"{components['Activity']}/100")
        with c_cols[4]: st.metric("Adherence Score", f"{components['Adherence']}/100")

        st.caption("Note: This is an application-defined wellness score derived from user lifestyle inputs and metabolic health guidelines, not a clinical diagnostic measurement.")

    st.markdown("---")
    st.subheader("📈 Projected Body Composition Trend (90-Day Est.)")

    bmi_val, _, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])

    weekly_deficit = (tdee - cal_req) * 7
    weekly_fat_change_kg = round(weekly_deficit / 7700.0, 2)

    days = [0, 15, 30, 45, 60, 75, 90]
    weights = [p["Weight"] - (weekly_fat_change_kg * (d / 7.0)) for d in days]

    fig_t = px.line(x=days, y=weights, labels={"x": "Days Ahead", "y": "Estimated Weight (kg)"}, markers=True)
    fig_t.update_traces(line_color="#00E5FF", line_width=3)
    fig_t.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E6ED'))
    st.plotly_chart(fig_t, use_container_width=True)

    st.info(f"💡 Projecting **{weekly_fat_change_kg:+.2f} kg** estimated fat change per week based on a daily energy delta of {tdee - cal_req} kcal.")


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
    render_health_analytics()
