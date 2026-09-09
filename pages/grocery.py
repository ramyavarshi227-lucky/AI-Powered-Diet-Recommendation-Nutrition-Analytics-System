import streamlit as st
import pandas as pd
import core.nutrition_utils as nu
import core.recommendation_engine as re_eng
import core.grocery_engine as ge

def render_grocery():
    st.markdown("<h1 style='color:#00E676;'>🛒 Budget-Aware Grocery Intelligence & Checklist</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00E5FF;'>Aggregated 7-day ingredient quantities, interactive item completion, and automated budget optimization.</p>", unsafe_allow_html=True)

    p = st.session_state.patient_profile
    bmi_val, _, _ = nu.calculate_bmi(p["Weight"], p["Height"])
    bmr = nu.calculate_bmr(p["Weight"], p["Height"], p["Age"], p["Gender"])
    tdee = nu.calculate_tdee(bmr, p["ActivityLevel"])
    cal_req = nu.calculate_calorie_requirement(tdee, p["FitnessGoal"])

    user_input = {**p, "BMI": bmi_val}
    predicted_cat, _, _ = re_eng.predict_diet_category(user_input)

    if 'current_meals_dict' not in st.session_state:
        rec_data = re_eng.generate_7_meal_recommendation(user_input, cal_req, predicted_cat)
        st.session_state.current_meals_dict = rec_data["meals"]
        st.session_state.current_meals_summary = rec_data["summary"]

    rec_meals = st.session_state.current_meals_dict
    rec_summary = st.session_state.current_meals_summary
    scale_factor = rec_summary.get("ScaleFactor", 1.0)

    # Budget Selector
    bud_opts = [1500, 2000, 2500, 3000, 3500, 4000, 5000]
    curr_bud = p.get("WeeklyBudget_INR", 2500)
    bud_val = curr_bud if curr_bud in bud_opts else 2500
    selected_budget = st.select_slider("Select Weekly Budget Target Cap (₹)", options=bud_opts, value=bud_val)

    categories, cat_costs, total_cost, opt_sugs, is_over, savings, cost_swaps = ge.estimate_grocery_from_meals(
        rec_meals, p.get("DietaryPreference", "Vegetarian"), scale_factor, selected_budget
    )

    b1, b2, b3 = st.columns(3)
    with b1: st.metric("Aggregated Weekly Cost", f"₹{total_cost:,}", f"{'Above Budget' if is_over else 'Within Budget'}")
    with b2: st.metric("Weekly Budget Cap", f"₹{selected_budget:,}")
    with b3: st.metric("Budget Savings Potential", f"₹{savings:,}" if is_over else "₹0", "Optimized")

    # AUTOMATED BUDGET OPTIMIZATION & PROTEIN SWAPS
    if is_over:
        st.markdown(f"""
            <div style='background: rgba(255, 152, 0, 0.15); border: 1px solid #FF9800; border-radius:12px; padding:16px; margin: 15px 0;'>
                <h4 style='color:#FF9800; margin:0;'>⚠️ BUDGET EXCEEDED — AURELIXA COST-SAVING PROTEIN SWAPS</h4>
                <p style='color:#E0E6ED; font-size:0.9rem; margin:5px 0;'>Your estimated 7-day grocery cost exceeds your target budget by <b>₹{savings:,}</b>. Below are lower-cost protein alternatives with equal nutritional value:</p>
            </div>
            """, unsafe_allow_html=True)

        for sw in cost_swaps:
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: st.markdown(f"**Expensive Item:** {sw['expensive']}")
            with c2: st.markdown(f"**Lower-Cost Alternative:** <span style='color:#00E676;'>{sw['cheaper']}</span>", unsafe_allow_html=True)
            with c3: st.markdown(f"**Savings:** <span style='color:#00E5FF;'>{sw['saved']}</span>", unsafe_allow_html=True)
            st.caption(f"Reason: {sw['reason']}")
            st.markdown("---")

    st.markdown(" ")
    st.subheader("📋 Interactive Aggregated 7-Day Grocery Checklist")

    # Interactive Checklist State
    if 'grocery_checked_items' not in st.session_state:
        st.session_state.grocery_checked_items = set()

    total_items = sum(len(items) for items in categories.values())
    checked_count = len(st.session_state.grocery_checked_items)
    completion_pct = int((checked_count / max(1, total_items)) * 100)

    st.progress(completion_pct / 100.0, text=f"Grocery Shopping Completion: {completion_pct}% ({checked_count} of {total_items} items checked)")

    for cat_name, items in categories.items():
        if items:
            with st.expander(f"🛒 {cat_name} ({len(items)} items — ₹{cat_costs.get(cat_name, 0):,})", expanded=True):
                for item in items:
                    item_key = f"{cat_name}_{item['name']}"
                    is_checked = st.checkbox(
                        f"**{item['name']}** — 7-Day Total Qty: `{item['qty']}` | Est Cost: `₹{item['price']}`",
                        value=(item_key in st.session_state.grocery_checked_items),
                        key=item_key
                    )
                    if is_checked:
                        st.session_state.grocery_checked_items.add(item_key)
                    else:
                        st.session_state.grocery_checked_items.discard(item_key)

    st.markdown("---")
    st.subheader("💡 AURELIXA Budget Optimization Tips")
    for sug in opt_sugs:
        st.markdown(f"• {sug}")
