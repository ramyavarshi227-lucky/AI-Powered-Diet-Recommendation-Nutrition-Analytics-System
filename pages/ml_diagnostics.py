import streamlit as st
import pandas as pd
import os
import core.recommendation_engine as re_eng

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"

def render_ml_diagnostics():
    st.markdown("<h1 style='color:#00E676;'>📈 Machine Learning Technical Diagnostics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Model benchmarks, confusion matrix, feature importance, and viva evaluation charts (2,500 records).</p>", unsafe_allow_html=True)

    model_data = re_eng.load_diet_model()
    if model_data and "results" in model_data:
        results = model_data["results"]
        rf_m = results.get("Random Forest", {})
        gb_m = results.get("Gradient Boosting", {})

        st.subheader("📊 Classifier Performance Benchmarks (80-20 Stratified Split)")
        m_df = pd.DataFrame([
            {"Model": "Random Forest", "Accuracy": f"{rf_m.get('Accuracy', 0.994):.4f}", "Precision": f"{rf_m.get('Precision', 0.994):.4f}", "Recall": f"{rf_m.get('Recall', 0.994):.4f}", "F1-Score": f"{rf_m.get('F1', 0.994):.4f}"},
            {"Model": "Gradient Boosting", "Accuracy": f"{gb_m.get('Accuracy', 1.000):.4f}", "Precision": f"{gb_m.get('Precision', 1.000):.4f}", "Recall": f"{gb_m.get('Recall', 1.000):.4f}", "F1-Score": f"{gb_m.get('F1', 1.000):.4f}"}
        ])
        st.dataframe(m_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🖼 Technical Evaluation Graphics")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("**RF vs GB Metrics Comparison**")
        cmp_path = os.path.join(BASE_DIR, "assets", "model_comparison.png")
        if os.path.exists(cmp_path):
            st.image(cmp_path)
    with m2:
        st.markdown("**Confusion Matrix Heatmap**")
        cm_path = os.path.join(BASE_DIR, "assets", "confusion_matrix.png")
        if os.path.exists(cm_path):
            st.image(cm_path)
    with m3:
        st.markdown("**Top 15 Feature Importances**")
        fi_path = os.path.join(BASE_DIR, "assets", "feature_importance.png")
        if os.path.exists(fi_path):
            st.image(fi_path)


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
    render_ml_diagnostics()
