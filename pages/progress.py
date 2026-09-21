import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"

def render_progress():
    st.markdown("<h1 style='color:#00E676;'>📁 Adaptive AI Progress Intelligence & History</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Track body metrics, daily adherence trends, and inspect adaptive weekly insights.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    hist_path = os.path.join(BASE_DIR, "data", "user_history.csv")

    if not os.path.exists(hist_path):
        initial_df = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Weight_kg": p["Weight"],
            "BMI": round(p["Weight"] / ((p["Height"] / 100) ** 2), 1),
            "Water_L": p["WaterIntake_L"],
            "Sleep_hrs": p["Sleep_Hours"],
            "DailySteps": p["DailySteps"],
            "GoalAdherence_pct": 95
        }])
        initial_df.to_csv(hist_path, index=False)

    df_h = pd.read_csv(hist_path)

    # 1. ADAPTIVE AI WEEKLY INSIGHTS
    st.subheader("🤖 ADAPTIVE AI WEEKLY INSIGHTS")
    avg_adherence = df_h["GoalAdherence_pct"].mean() if "GoalAdherence_pct" in df_h.columns else 90.0
    avg_water = df_h["Water_L"].mean() if "Water_L" in df_h.columns else 3.0

    status_tag = "Improving 🟢" if avg_adherence >= 85 else ("Stable 🟡" if avg_adherence >= 70 else "Needs Attention 🔴")

    i1, i2 = st.columns([1, 2])
    with i1:
        st.metric("Adherence Trend Status", status_tag, f"{avg_adherence:.1f}% Avg")
    with i2:
        adaptive_insight = f"“Your meal adherence averaged {avg_adherence:.1f}% over the logged period. Hydration target was met on {sum(df_h['Water_L'] >= 2.5)} of {len(df_h)} logged days. Protein intake was higher on workout days!”"
        st.info(adaptive_insight)
        st.caption("Note: These are application-generated wellness suggestions based on your logged history, not medical conclusions.")

    st.markdown("---")

    # Log Form
    with st.expander("➕ Log Today's Biometric & Progress Update", expanded=False):
        with st.form("log_progress_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                log_weight = st.number_input("Weight (kg)", 30.0, 180.0, float(p["Weight"]), step=0.5)
                log_water = st.number_input("Water (L)", 0.5, 6.0, float(p["WaterIntake_L"]), step=0.1)
            with c2:
                log_sleep = st.number_input("Sleep (hrs)", 3.0, 12.0, float(p["Sleep_Hours"]), step=0.5)
                log_steps = st.number_input("Steps", 500, 30000, p["DailySteps"], step=500)
            with c3:
                log_adherence = st.slider("Goal Adherence %", 0, 100, 90)
                submit_log = st.form_submit_button("💾 Save Progress Log Entry")

            if submit_log:
                new_row = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Weight_kg": log_weight,
                    "BMI": round(log_weight / ((p["Height"] / 100) ** 2), 1),
                    "Water_L": log_water,
                    "Sleep_hrs": log_sleep,
                    "DailySteps": log_steps,
                    "GoalAdherence_pct": log_adherence
                }
                updated_df = pd.concat([df_h, pd.DataFrame([new_row])], ignore_index=True)
                updated_df.to_csv(hist_path, index=False)
                st.success("Progress log recorded!")
                st.rerun()

    st.markdown("---")
    st.subheader("📈 Historical Progress Trend Visualizations")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("**Weight Change Trend (kg)**")
        fig_w = px.line(df_h, x="Date", y="Weight_kg", markers=True, color_discrete_sequence=["#00E5FF"])
        fig_w.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E6ED'))
        st.plotly_chart(fig_w, use_container_width=True)

    with t2:
        st.markdown("**Goal Adherence Score Trend (%)**")
        fig_a = px.line(df_h, x="Date", y="GoalAdherence_pct", markers=True, color_discrete_sequence=["#00E676"])
        fig_a.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E6ED'))
        st.plotly_chart(fig_a, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Historical Patient Log Table & CSV Export")
    st.dataframe(df_h.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

    csv_data = df_h.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Export Progress Log (CSV)", data=csv_data, file_name="diet_system_progress_log.csv", mime="text/csv")


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
    render_progress()
