import streamlit as st
import pandas as pd
import core.nutrition_utils as nu
import core.recommendation_engine as re_eng

def render_home():
    p = st.session_state.patient_profile
    
    bmi_val, bmi_cat, bmi_color = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])
    health_score = nu.calculate_health_score(bmi_val, p["ActivityLevel"], p["WaterIntake_L"], p["Sleep_Hours"], p["DailySteps"], p["StressLevel"], p["SmokingStatus"], p["AlcoholConsumption"], p["MedicalCondition"])
    
    pers_score, pers_checklist = nu.calculate_personalization_score(p)

    user_input = {**p, "BMI": bmi_val}
    predicted_cat, conf_scores, _ = re_eng.predict_diet_category(user_input)

    st.markdown(f"<h1 class='aurelixa-header'>Welcome back, {p['Name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='aurelixa-tagline'>Clinical Recommendation: <span style='color:#00E676;'>{predicted_cat}</span> | Target: <span style='color:#00E5FF;'>{cal_req} kcal/day</span></p>", unsafe_allow_html=True)

    # 1. AURELIXA PERSONALIZATION SCORE & SAFETY SHIELD BANNER
    c_p1, c_p2 = st.columns([1, 1])
    with c_p1:
        st.markdown(f"""
            <div class='glass-card' style='border-left: 5px solid #00E676;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <h4 style='color:#8A99AD; margin:0;'>🎯 AURELIXA PERSONALIZATION SCORE</h4>
                        <div style='font-size:2.8rem; font-weight:800; color:#00E676;'>{pers_score}/100</div>
                    </div>
                    <div style='font-size:3rem;'>📊</div>
                </div>
                <hr style='border-color:rgba(255,255,255,0.1); margin: 10px 0;'>
                <div style='font-size:0.85rem; line-height:1.6;'>
                    {" ".join([f"<span style='color:#00E676;'>✓</span> <b>{chk['item']}</b>: <span style='color:#8A99AD;'>{chk['detail']}</span><br>" for chk in pers_checklist])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c_p2:
        st.markdown(f"""
            <div class='glass-card' style='border-left: 5px solid #00E5FF;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <h4 style='color:#8A99AD; margin:0;'>🛡 AURELIXA SAFETY SHIELD</h4>
                        <div style='font-size:1.4rem; font-weight:700; color:#00E5FF; margin-top:5px;'>ACTIVE & VERIFIED</div>
                    </div>
                    <div style='font-size:2.8rem;'>🛡️</div>
                </div>
                <hr style='border-color:rgba(255,255,255,0.1); margin: 10px 0;'>
                <p style='font-size:0.85rem; color:#E0E6ED; margin:0;'>
                    <b>Allergy Exclusions:</b> <span style='color:#FF9800;'>{p.get('FoodAllergy', 'None')}</span><br>
                    <b>Dietary Restrictions:</b> <span style='color:#00E5FF;'>{p.get('DietaryPreference', 'Vegetarian')}</span><br>
                    <b>Medical Safeguards:</b> <span style='color:#00E676;'>{p.get('MedicalCondition', 'None')}</span><br>
                    <small style='color:#8A99AD;'>All 7 daily meals and swaps pass 6 hard validation checks prior to display.</small>
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 2. DAILY AI COACH INSIGHT
    coach_insight = f"Your current meal plan is calibrated for {cal_req} kcal/day with zero allergen triggers for '{p.get('FoodAllergy', 'None')}'. Your protein target is optimized for your {p.get('ActivityLevel', 'Moderately Active')} lifestyle!"
    if p["WaterIntake_L"] < 2.5:
        coach_insight = "💧 Your hydration is below today's 3.0L target. Increase water intake to boost metabolic expenditure."
    elif p["Sleep_Hours"] < 7.0:
        coach_insight = "🌙 Your sleep duration was under 7 hours last night. A short 20-min power nap will aid muscle recovery."

    st.markdown(f"""
        <div class='glass-card' style='background: rgba(124, 77, 255, 0.12); border: 1px solid rgba(124, 77, 255, 0.3);'>
            <h4 style='color:#7C4DFF; margin:0 0 5px 0;'>🤖 AURELIXA DAILY AI COACH INSIGHT</h4>
            <p style='font-size:1rem; color:#E0E6ED; margin:0;'>“{coach_insight}”</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. CORE METRIC GAUGES
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>HEALTH SCORE</div>
                <div class='metric-val' style='color:#00E676;'>{health_score}</div>
                <small style='color:#8A99AD;'>/ 100 Wellness</small>
            </div>
            """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>CALORIE TARGET</div>
                <div class='metric-val' style='color:#00E5FF;'>{cal_req}</div>
                <small style='color:#8A99AD;'>kcal / day</small>
            </div>
            """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>HYDRATION</div>
                <div class='metric-val' style='color:#7C4DFF;'>{p['WaterIntake_L']}L</div>
                <small style='color:#8A99AD;'>/ 3.0L Target</small>
            </div>
            """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>SLEEP</div>
                <div class='metric-val' style='color:#D500F9;'>{p['Sleep_Hours']}h</div>
                <small style='color:#8A99AD;'>/ 8.0h Target</small>
            </div>
            """, unsafe_allow_html=True)
    with m5:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>DAILY STEPS</div>
                <div class='metric-val' style='color:#FF9800;'>{p['DailySteps']:,}</div>
                <small style='color:#8A99AD;'>steps / day</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. TODAY'S 7-MEAL QUICK SCHEDULE
    st.subheader("🍽 Today's 7-Meal Personalized Schedule")

    if 'current_meals_dict' not in st.session_state:
        rec_data = re_eng.generate_7_meal_recommendation(user_input, cal_req, predicted_cat)
        st.session_state.current_meals_dict = rec_data["meals"]
        st.session_state.current_meals_summary = rec_data["summary"]

    rec_meals = st.session_state.current_meals_dict

    cols = st.columns(4)
    idx = 0
    for m_type, meal in rec_meals.items():
        with cols[idx % 4]:
            st.markdown(f"""
                <div class='glass-card' style='height:210px;'>
                    <span style='color:#8A99AD; font-size:0.75rem; font-weight:700;'>{m_type.upper()}</span>
                    <h4 style='color:#00E5FF; margin:4px 0;'>{meal['name']}</h4>
                    <p style='font-size:0.85rem; color:#00E676;'>🔥 {meal['calories']} kcal | 💪 P: {meal['protein']}g</p>
                    <p style='font-size:0.75rem; color:#8A99AD;'>Carbs: {meal['carbs']}g | Fat: {meal['fat']}g</p>
                    <span class='badge-gi-{meal["gi_impact"].lower()}'>GI: {meal['gi_impact']}</span>
                </div>
                """, unsafe_allow_html=True)
        idx += 1

    st.markdown(" ")
    st.info("💡 Tip: Navigate to **🍽 My Nutrition** to execute **1-Click Smart Meal Swapping 2.0** and inspect detailed **Recommendation Traces ('Why This Meal?')**.")
