"""
Budgets Page - Set and track budget limits per category.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp_server.tools.budgets import set_budget, get_budgets, get_budget_alerts

st.set_page_config(page_title="Budgets", page_icon="🎯", layout="wide")

st.title("🎯 Budgets")
st.caption("Set limits and stay on track.")
st.divider()

# BUDGET ALERTS
alerts = get_budget_alerts()
if alerts["count"] > 0:
    for alert in alerts["alerts"]:
        if alert["status"] == "over":
            st.error(f"🔴 **{alert['category'].title()}** — Over budget! Spent ${alert['spent']} of ${alert['amount']} limit")
        elif alert["status"] == "warning":
            st.warning(f"🟡 **{alert['category'].title()}** — {alert['percent_used']}% used. ${alert['remaining']} remaining")

    st.divider()

# SET BUDGET FORM
st.subheader("➕ Set a Budget")

with st.form("set_budget_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox("Category", [
            "groceries", "dining", "rent", "transport",
            "utilities", "entertainment", "health",
            "shopping", "education", "other"
        ])

    with col2:
        amount = st.number_input("Budget Limit ($)", min_value=1.0, step=10.0, format="%.2f")

    with col3:
        period = st.selectbox("Period", ["monthly", "weekly"])

    submitted = st.form_submit_button("Set Budget 🎯", use_container_width=True)

    if submitted:
        result = set_budget(
            category=category,
            amount=amount,
            period=period
        )
        if result["success"]:
            st.success(result["message"])
            st.rerun()
        else:
            st.error("Failed to set budget")

st.divider()

# BUDGET STATUS TABLE
st.subheader("📋 Budget Status This Month")

result = get_budgets()
budgets = result["budgets"]

if budgets:
    # PROGRESS BARS
    st.subheader("📊 Spending Progress")

    for b in budgets:
        col1, col2 = st.columns([3, 1])

        with col1:
            color = (
                "🔴" if b["status"] == "over" else
                "🟡" if b["status"] == "warning" else
                "🟢"
            )
            st.write(f"{color} **{b['category'].title()}**")
            progress = min(b["percent_used"] / 100, 1.0)
            st.progress(progress)

        with col2:
            st.metric(
                label="Spent / Limit",
                value=f"${b['spent']}",
                delta=f"-${b['remaining']} left" if b["remaining"] >= 0 else f"${abs(b['remaining'])} over",
                delta_color="normal" if b["remaining"] >= 0 else "inverse"
            )

    st.divider()

    # BUDGET TABLE
    st.subheader("📋 All Budgets")

    df = pd.DataFrame(budgets)
    df = df[["category", "amount", "spent", "remaining", "percent_used", "status", "period"]]
    df.columns = ["Category", "Limit ($)", "Spent ($)", "Remaining ($)", "Used (%)", "Status", "Period"]
    df["Category"] = df["Category"].str.title()
    df["Status"] = df["Status"].str.title()

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # BUDGET VS SPENT CHART
    st.subheader("📊 Budget vs Actual Spending")

    df_chart = pd.DataFrame(budgets)
    fig = px.bar(
        df_chart,
        x="category",
        y=["amount", "spent"],
        barmode="group",
        labels={"value": "Amount ($)", "category": "Category", "variable": "Type"},
        color_discrete_map={"amount": "#2ecc71", "spent": "#e74c3c"},
        text_auto=True
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📭 No budgets set yet — use the form above to set your first budget!")