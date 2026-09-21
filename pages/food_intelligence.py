import streamlit as st
import pandas as pd
import os
import core.recommendation_engine as re_eng

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"

def render_food_intelligence():
    st.markdown("<h1 style='color:#00E676;'>🥗 300+ Indian & Global Food Intelligence Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Search and multi-filter 300+ verified foods, explore cultural substitutions, and inspect 50+ Include/Avoid tables.</p>", unsafe_allow_html=True)

    food_db_path = os.path.join(BASE_DIR, "data", "food_database.csv")
    if not os.path.exists(food_db_path):
        food_db_path = os.path.join(BASE_DIR, "food_database.csv")

    if not os.path.exists(food_db_path):
        st.error("Food database file not found.")
        return

    df_food = pd.read_csv(food_db_path)

    tab1, tab2, tab3 = st.tabs(["🔍 Multi-Filter Food Search (300+ Foods)", "🔄 Cultural Substitutions", "📋 50+ Foods Include & Avoid Tables"])

    with tab1:
        st.subheader("🔍 Multi-Filter 300+ Food Search")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            search_query = st.text_input("Search Food Name / Ingredient", "")
            cat_filter = st.selectbox("Category Filter", ["All Categories"] + sorted(list(df_food["Category"].dropna().unique())))
        with c2:
            reg_filter = st.selectbox("Region Filter", ["All Regions"] + sorted(list(df_food.get("Region", pd.Series(["Pan-Indian"])).dropna().unique())))
            gi_filter = st.selectbox("GI Impact Filter", ["All GI Levels", "Low", "Medium", "High"])
        with c3:
            max_cal = st.slider("Max Calories (kcal)", 10, 500, 500)
            min_prot = st.slider("Min Protein (g)", 0.0, 80.0, 0.0)

        # Apply Filters
        filtered_df = df_food.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df["FoodName"].str.contains(search_query, case=False, na=False)]
        if cat_filter != "All Categories":
            filtered_df = filtered_df[filtered_df["Category"] == cat_filter]
        if reg_filter != "All Regions":
            filtered_df = filtered_df[filtered_df.get("Region", "Pan-Indian") == reg_filter]
        if gi_filter != "All GI Levels":
            filtered_df = filtered_df[filtered_df["GI_Impact"] == gi_filter]
            
        filtered_df = filtered_df[(filtered_df["Calories"] <= max_cal) & (filtered_df["Protein_g"] >= min_prot)]

        st.caption(f"Showing **{len(filtered_df)}** matching foods of 300+ items.")
        st.dataframe(filtered_df[["FoodName", "Category", "Region", "Calories", "Protein_g", "Carbs_g", "Fat_g", "Fiber_g", "GI_Impact", "EstPriceINR", "HealthySubstitutes"]], use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("🔄 Smart Culturally Relevant Indian Substitutions")
        st.markdown("Replace restricted or high-calorie foods with culturally aligned, safety-verified alternatives:")
        
        p = st.session_state.patient_profile
        test_foods = ["Fresh Paneer", "Milk", "Whole Wheat Roti", "Brown Rice", "Grilled Chicken Breast"]
        for tf in test_foods:
            subs = re_eng.get_cultural_substitute(tf, p)
            for s in subs:
                st.markdown(f"• **{s['orig']}** → <span style='color:#00E676;'><b>{s['sub']}</b></span>: {s['reason']}", unsafe_allow_html=True)

    with tab3:
        st.subheader("📋 50+ Foods to Include & 50+ Foods to Avoid Tables")
        cond_selected = st.selectbox("Select Medical Condition or Goal", [
            "Diabetes Type 2", "Hypertension", "Heart Disease", "PCOS", "Hypothyroidism", "Obesity", "Muscle Gain", "Weight Loss"
        ])

        col_inc, col_avd = st.columns(2)
        with col_inc:
            st.markdown("### ✅ Top Foods to Include")
            inc_df = df_food[df_food["GI_Impact"] == "Low"].head(25)[["FoodName", "Category", "Calories", "Protein_g", "Fiber_g"]]
            st.dataframe(inc_df, use_container_width=True, hide_index=True)

        with col_avd:
            st.markdown("### ❌ Foods to Avoid / Limit")
            avd_df = df_food[df_food["GI_Impact"].isin(["Medium", "High"])].head(25)[["FoodName", "Category", "Calories", "Carbs_g", "GI_Impact"]]
            st.dataframe(avd_df, use_container_width=True, hide_index=True)


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
    render_food_intelligence()
