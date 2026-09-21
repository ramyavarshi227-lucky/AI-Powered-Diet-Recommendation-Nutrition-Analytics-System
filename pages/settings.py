import streamlit as st
import os

def render_settings():
    st.markdown("<h1 style='color:#00E676;'>⚙ Platform Settings & Personalization</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Manage profile preferences, visual theme accent, and platform metadata.</p>", unsafe_allow_html=True)

    st.subheader("🎨 Visual Theme Accent Picker")
    current_accent = st.session_state.get("theme_accent", "#00E676")
    new_accent = st.color_picker("Choose Primary Accent Color", current_accent)
    if new_accent != current_accent:
        st.session_state.theme_accent = new_accent
        st.success("Theme accent updated!")

    st.markdown("---")
    st.subheader("📏 Measurement Units & Preferences")
    u1, u2 = st.columns(2)
    with u1:
        st.selectbox("Weight Unit", ["Metric (kg)", "Imperial (lbs)"], index=0)
        st.selectbox("Height Unit", ["Metric (cm)", "Imperial (ft/in)"], index=0)
    with u2:
        st.selectbox("Energy Unit", ["Kilocalories (kcal)", "Kilojoules (kJ)"], index=0)
        st.selectbox("Currency Preferred", ["Indian Rupee (₹)", "US Dollar ($)", "Euro (€)"], index=0)

    st.markdown("---")
    st.subheader("🔔 Notification & Reminder Preferences")
    st.checkbox("Enable Daily Hydration Reminders", value=True)
    st.checkbox("Enable Meal Time Alerts", value=True)
    st.checkbox("Enable Weekly Progress Report Notifications", value=True)

    st.markdown("---")
    st.subheader("🗑 Data Management & Reset")
    if st.button("🔄 Reset Profile Wizard & Start Over"):
        st.session_state.active_screen = "Splash Screen"
        st.session_state.profile_wizard_step = 1
        st.success("Profile wizard reset to Splash Screen!")
        st.rerun()

    st.markdown("---")
    st.subheader("ℹ️ About AI-Powered Diet Recommendation & Nutrition Analytics System")
    st.markdown("""
        **Project Name:** AI-Powered Diet Recommendation and Nutrition Analytics System  
        **Subtitle:** *“Personalized Nutrition. Intelligent Analytics. Better Decisions.”*  
        **Build Version:** 4.0.0 (Capstone Build)  
        **Machine Learning Backbone:** Scikit-Learn Ensemble Pipeline (Gradient Boosting & Random Forest)  
        **Dataset Scale:** 2,500 Synthetic Patient Records & 300+ Verified Food Database  
        **Medical Disclaimer:** This system provides educational nutrition estimates and analytics and is not a medical diagnosis or treatment tool. Consult a qualified healthcare professional for medical or dietary decisions.  
    """)


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
    render_settings()
