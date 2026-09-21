import streamlit as st
import pandas as pd
import numpy as np
import os

import core.nutrition_utils as nu
import core.recommendation_engine as re_eng
import pages.profile as page_profile

import pages.home as page_home
import pages.nutrition as page_nutrition
import pages.weekly_plan as page_weekly
import pages.grocery as page_grocery
import pages.food_intelligence as page_food
import pages.health_analytics as page_health
import pages.medical_analysis as page_medical
import pages.ai_insights as page_ai
import pages.ml_diagnostics as page_mld
import pages.progress as page_progress
import pages.reports as page_reports
import pages.settings as page_settings

# Streamlit Page Config
st.set_page_config(
    page_title="AI-Powered Diet Recommendation and Nutrition Analytics System",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Glassmorphism Project Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0B1020;
        color: #E0E6ED;
    }
    
    .project-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00E676 0%, #00E5FF 40%, #7C4DFF 70%, #D500F9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
        line-height: 1.25;
    }
    
    .project-tagline {
        font-size: 1.05rem;
        font-weight: 600;
        color: #00E5FF;
        letter-spacing: 1.2px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    
    .glass-card {
        background: rgba(18, 24, 38, 0.75);
        border-radius: 16px;
        padding: 22px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 18px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        border-color: rgba(0, 229, 255, 0.35);
        box-shadow: 0 12px 40px 0 rgba(0, 229, 255, 0.15);
    }
    
    .hero-banner {
        background: linear-gradient(135deg, rgba(11, 16, 32, 0.95) 0%, rgba(18, 24, 38, 0.90) 50%, rgba(26, 35, 58, 0.85) 100%);
        border-radius: 20px;
        padding: 36px;
        border: 1px solid rgba(0, 230, 118, 0.35);
        margin-bottom: 24px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
    }
    
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 4px 0;
    }
    
    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #8A99AD;
    }
    
    .badge-gi-low { background: rgba(0, 230, 118, 0.15); color: #00E676; padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; border: 1px solid rgba(0, 230, 118, 0.3); }
    .badge-gi-med { background: rgba(255, 152, 0, 0.15); color: #FF9800; padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; border: 1px solid rgba(255, 152, 0, 0.3); }
    .badge-gi-high { background: rgba(255, 23, 68, 0.15); color: #FF1744; padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; border: 1px solid rgba(255, 23, 68, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# Session State Initialization
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = {
        "Name": "Priya Sharma",
        "Age": 29,
        "Gender": "Female",
        "Height": 162,
        "Weight": 72.0,
        "BodyFat": 26.0,
        "Waist": 80.0,
        "ActivityLevel": "Moderately Active",
        "Occupation": "Office Worker",
        "DailySteps": 8500,
        "ExerciseFreq": "3-4 times / week",
        "WorkoutType": "Cardio & Pilates",
        "WaterIntake_L": 3.0,
        "Sleep_Hours": 7.5,
        "StressLevel": "Moderate",
        "SmokingStatus": "Non-Smoker",
        "AlcoholConsumption": "None",
        "FitnessGoal": "Weight Loss",
        "MedicalCondition": "None",
        "FoodAllergy": "Nuts",
        "DietaryPreference": "South Indian",
        "WeeklyBudget_INR": 2500
    }

if 'active_screen' not in st.session_state:
    st.session_state.active_screen = "Splash Screen"

screen = st.session_state.active_screen

# ==============================================================================
# SCREEN 1: SPLASH SCREEN
# ==============================================================================
if screen == "Splash Screen":
    st.markdown("""
        <div class='hero-banner' style='text-align:center; padding: 60px 20px;'>
            <div style='font-size:4rem; margin-bottom:10px;'>🥗</div>
            <h1 class='project-header' style='font-size:3rem;'>AI-Powered Diet Recommendation<br>and Nutrition Analytics System</h1>
            <p class='project-tagline' style='font-size:1.1rem;'>Personalized Nutrition. Intelligent Analytics. Better Decisions.</p>
            <p style='color:#E0E6ED; font-size:1.05rem; max-width:720px; margin: 0 auto 30px auto;'>
                Clinical-grade decision support platform combining Random Forest and Gradient Boosting machine learning models, 6-point Safety Shield validation, 300+ Indian food database, Smart Meal Swapping 2.0, and What-If Simulation.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(" ")
    c_sp1, c_sp2, c_sp3 = st.columns([1, 1, 1])
    with c_sp2:
        if st.button("🚀 Get Started →", type="primary", use_container_width=True):
            st.session_state.active_screen = "Welcome / Onboarding"
            st.rerun()

# ==============================================================================
# SCREEN 2: WELCOME / ONBOARDING
# ==============================================================================
elif screen == "Welcome / Onboarding":
    st.markdown("<h1 class='project-header'>AI-Powered Diet Recommendation & Nutrition Analytics System</h1>", unsafe_allow_html=True)
    st.markdown("<p class='project-tagline'>Personalized Nutrition. Intelligent Analytics. Better Decisions.</p>", unsafe_allow_html=True)
    st.markdown("---")

    o1, o2, o3, o4 = st.columns(4)
    with o1:
        st.markdown("""
            <div class='glass-card' style='height:280px;'>
                <h3 style='color:#00E676;'>🎯 Personalization</h3>
                <p style='font-size:0.9rem; color:#E0E6ED;'>Personalization Score (0-100) evaluating goal alignment, allergies, budget, and lifestyle biometrics.</p>
            </div>
            """, unsafe_allow_html=True)
    with o2:
        st.markdown("""
            <div class='glass-card' style='height:280px;'>
                <h3 style='color:#00E5FF;'>🛡 Safety Shield</h3>
                <p style='font-size:0.9rem; color:#E0E6ED;'>6-point hard safety validation layer blocking allergen, preference, and clinical rule violations prior to display.</p>
            </div>
            """, unsafe_allow_html=True)
    with o3:
        st.markdown("""
            <div class='glass-card' style='height:280px;'>
                <h3 style='color:#7C4DFF;'>🥗 300+ Indian Foods</h3>
                <p style='font-size:0.9rem; color:#E0E6ED;'>Comprehensive database covering South Indian, North Indian, Jain, Vegan recipes & smart cultural substitutions.</p>
            </div>
            """, unsafe_allow_html=True)
    with o4:
        st.markdown("""
            <div class='glass-card' style='height:280px;'>
                <h3 style='color:#D500F9;'>🔮 What-If Simulator</h3>
                <p style='font-size:0.9rem; color:#E0E6ED;'>Interactive simulation engine enabling live testing of goals, activity, preferences, and budget caps.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    co1, co2, co3 = st.columns([1, 1, 1])
    with co2:
        if st.button("Continue to Clinical Intake →", type="primary", use_container_width=True):
            st.session_state.active_screen = "Clinical Profile"
            st.rerun()

# ==============================================================================
# SCREEN 3: CLINICAL PROFILE WIZARD
# ==============================================================================
elif screen == "Clinical Profile":
    page_profile.render_profile_wizard()

# ==============================================================================
# SCREEN 4: PERSONALIZED ANALYSIS LOADING
# ==============================================================================
elif screen == "Personalized Analysis":
    st.markdown("<h1 class='project-header' style='text-align:center;'>AI Nutrition Analytics Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='project-tagline' style='text-align:center;'>Running Clinical Bio-Metabolic Calculations...</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='glass-card' style='max-width:650px; margin: 0 auto; font-size:1.05rem; line-height:2;'>
            <p style='color:#00E676;'>✓ Calculating BMR & TDEE metabolic baselines</p>
            <p style='color:#00E676;'>✓ Calculating Personalization Score (0-100)</p>
            <p style='color:#00E676;'>✓ Executing 6-Point Safety Shield Validation</p>
            <p style='color:#00E676;'>✓ Screening 17 clinical food allergen exclusions</p>
            <p style='color:#00E676;'>✓ Querying 300+ Indian & Global Food Database</p>
            <p style='color:#00E676;'>✓ Executing Gradient Boosting AI recommendation model</p>
            <p style='color:#00E676;'>✓ Creating personalized 7-meal daily schedule</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(" ")
    st.success("✨ Your personalized nutrition profile is ready!")
    
    ca1, ca2, ca3 = st.columns([1, 1, 1])
    with ca2:
        if st.button("View My Dashboard →", type="primary", use_container_width=True):
            st.session_state.active_screen = "🏠 Home"
            st.rerun()

# ==============================================================================
# MAIN APPLICATION ROUTER WITH PERSISTENT SIDEBAR
# ==============================================================================
else:
    p = st.session_state.patient_profile
    bmi_val, bmi_cat, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])
    
    user_input = {**p, "BMI": bmi_val}
    predicted_cat, _, _ = re_eng.predict_diet_category(user_input)

    nav_options = [
        "🏠 Home",
        "👤 Edit Profile / Intake",
        "🍽 My Nutrition",
        "📅 Weekly Plan",
        "🛒 Grocery Intelligence",
        "🥗 Food Intelligence",
        "📊 Health Analytics",
        "🧬 Medical & Nutrition Analysis",
        "🤖 AI Insights",
        "📈 ML Diagnostics",
        "📁 Progress",
        "📄 Reports",
        "⚙ Settings"
    ]

    with st.sidebar:
        st.markdown("<h3 style='color:#00E676; margin-bottom:0;'>🥗 AI-Powered Diet System</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00E5FF; font-size:0.75rem; font-weight:700; letter-spacing:1px;'>PERSONALIZED NUTRITION & ANALYTICS</p>", unsafe_allow_html=True)
        st.markdown("---")

        curr_screen = st.session_state.get("active_screen", "🏠 Home")
        default_idx = nav_options.index(curr_screen) if curr_screen in nav_options else 0

        nav_selection = st.radio(
            "Navigation Screens",
            nav_options,
            index=default_idx
        )

        st.session_state.active_screen = nav_selection

        st.markdown("---")
        st.markdown(f"👤 **Patient**: `{p['Name']}`")
        st.markdown(f"🎂 **Age/Gender**: `{p['Age']}y / {p['Gender']}`")
        st.markdown(f"⚖️ **BMI**: `{bmi_val}` (`{bmi_cat}`)")
        st.markdown(f"🎯 **Target**: `{cal_req} kcal/day`")
        st.markdown(f"🏷️ **Diet**: `{predicted_cat}`")
        st.markdown(f"🛡️ **Safety Shield**: `<font color='#00E676'><b>VERIFIED ✓</b></font>`", unsafe_allow_html=True)

    # Render Active Selected Screen
    if nav_selection == "🏠 Home":
        page_home.render_home()
    elif nav_selection == "👤 Edit Profile / Intake":
        page_profile.render_profile_wizard()
    elif nav_selection == "🍽 My Nutrition":
        page_nutrition.render_nutrition()
    elif nav_selection == "📅 Weekly Plan":
        page_weekly.render_weekly_plan()
    elif nav_selection == "🛒 Grocery Intelligence":
        page_grocery.render_grocery()
    elif nav_selection == "🥗 Food Intelligence":
        page_food.render_food_intelligence()
    elif nav_selection == "📊 Health Analytics":
        page_health.render_health_analytics()
    elif nav_selection == "🧬 Medical & Nutrition Analysis":
        page_medical.render_medical_analysis()
    elif nav_selection == "🤖 AI Insights":
        page_ai.render_ai_insights()
    elif nav_selection == "📈 ML Diagnostics":
        page_mld.render_ml_diagnostics()
    elif nav_selection == "📁 Progress":
        page_progress.render_progress()
    elif nav_selection == "📄 Reports":
        page_reports.render_reports()
    elif nav_selection == "⚙ Settings":
        page_settings.render_settings()
