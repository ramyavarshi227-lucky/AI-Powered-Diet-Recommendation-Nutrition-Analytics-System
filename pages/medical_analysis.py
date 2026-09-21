import streamlit as st
import core.nutrition_utils as nu
import core.deficiency_engine as de

def render_medical_analysis():
    st.markdown("<h1 style='color:#00E676;'>🧬 Medical & Nutritional Risk Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Educational risk indicators across 8 essential micronutrients and dietary factors.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    bmi_val, _, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])

    deficiencies = de.analyze_nutritional_deficiencies_8(
        p["MedicalCondition"], bmi_val, p["DietaryPreference"], cal_req
    )

    st.markdown("---")
    st.warning("⚠️ **Educational Disclaimer**: These nutritional risk indicators are estimated educational suggestions for dietary planning. Consider discussing persistent concerns with a qualified healthcare professional.")

    d_cols = st.columns(4)
    for idx, def_item in enumerate(deficiencies):
        col_idx = idx % 4
        with d_cols[col_idx]:
            risk_color = "#FF1744" if "High" in def_item['risk_level'] else "#FF9800"
            st.markdown(f"""
                <div class='glass-card' style='height: 380px; display:flex; flex-direction:column; justify-content:space-between;'>
                    <div>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                            <h4 style='color:#FF9800; margin:0;'>{def_item['nutrient']}</h4>
                            <span style='background:rgba(255,23,68,0.15); color:{risk_color}; padding:2px 6px; border-radius:10px; font-size:0.75rem; font-weight:700;'>{def_item['risk_level']}</span>
                        </div>
                        <p style='font-size:0.8rem; margin:4px 0;'><b>Symptoms:</b> {def_item['symptoms']}</p>
                        <p style='font-size:0.8rem; margin:2px 0; color:#8A99AD;'><b>Causes:</b> {def_item['causes']}</p>
                        <p style='font-size:0.8rem; margin:2px 0; color:#00E676;'><b>Eat:</b> {def_item['foods_to_eat']}</p>
                        <p style='font-size:0.8rem; margin:2px 0; color:#FF1744;'><b>Limit:</b> {def_item['foods_to_avoid']}</p>
                    </div>
                    <div style='background:rgba(0,229,255,0.05); padding:6px; border-radius:6px; font-size:0.75rem; color:#00E5FF;'>
                        <b>💊 Supplement:</b> {def_item['supplements']}
                    </div>
                </div>
                """, unsafe_allow_html=True)


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
    render_medical_analysis()
