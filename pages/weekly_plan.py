import streamlit as st
import pandas as pd

def render_weekly_plan():
    st.markdown("<h1 style='color:#00E676;'>📅 7-Day Weekly Meal Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Comprehensive Monday through Sunday structured meal plan and weekly targets.</p>", unsafe_allow_html=True)

    if 'current_meals_dict' not in st.session_state:
        st.info("Please visit 'My Nutrition' screen first to generate meal recommendations.")
        return

    rec_meals = st.session_state.current_meals_dict
    rec_summary = st.session_state.current_meals_summary

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    w_rows = []
    for d in days:
        w_rows.append({
            "Day": d,
            "Breakfast": rec_meals.get("Breakfast", {}).get("name", "").split(" (")[0],
            "Lunch": rec_meals.get("Lunch", {}).get("name", "").split(" (")[0],
            "Dinner": rec_meals.get("Dinner", {}).get("name", "").split(" (")[0],
            "Snacks": rec_meals.get("Mid-Morning Snack", {}).get("name", "").split(" (")[0] + " / " + rec_meals.get("Evening Snack", {}).get("name", "").split(" (")[0]
        })

    st.subheader("🗓 Weekly 7-Day Meal Schedule")
    st.dataframe(pd.DataFrame(w_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📊 Weekly Nutrition & Hydration Averages")

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>WEEKLY CALORIES</div>
                <div class='metric-val' style='color:#00E5FF;'>{rec_summary['Calories'] * 7:,} kcal</div>
                <span style='font-size:0.8rem; color:#8A99AD;'>Avg {rec_summary['Calories']} kcal/day</span>
            </div>
            """, unsafe_allow_html=True)
    with w2:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>AVG PROTEIN / DAY</div>
                <div class='metric-val' style='color:#00E676;'>{rec_summary['Protein']} g</div>
                <span style='font-size:0.8rem; color:#8A99AD;'>Weekly Total: {round(rec_summary['Protein'] * 7)} g</span>
            </div>
            """, unsafe_allow_html=True)
    with w3:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>AVG CARBS / DAY</div>
                <div class='metric-val' style='color:#7C4DFF;'>{rec_summary['Carbs']} g</div>
                <span style='font-size:0.8rem; color:#8A99AD;'>Weekly Total: {round(rec_summary['Carbs'] * 7)} g</span>
            </div>
            """, unsafe_allow_html=True)
    with w4:
        st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div class='metric-lbl'>AVG FIBER / DAY</div>
                <div class='metric-val' style='color:#D500F9;'>{rec_summary['Fiber']} g</div>
                <span style='font-size:0.8rem; color:#8A99AD;'>Weekly Total: {round(rec_summary['Fiber'] * 7)} g</span>
            </div>
            """, unsafe_allow_html=True)
