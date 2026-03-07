"""
Finance Coach Dashboard - Main Homepage
Shows financial health score, monthly summary and quick stats.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

# Make sure Python finds our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.tools.summary import get_summary, get_monthly_trend
from mcp_server.tools.context import get_financial_health_score
from mcp_server.tools.advice import get_latest_advice

# PAGE CONFIG
st.set_page_config(
    page_title="Finance Coach",
    page_icon="💰",
    layout="wide"
)

# HEADER
st.title("💰 Personal Finance Coach")
st.caption("Plan your money. Build better habits.")
st.divider()

# HEALTH SCORE 
health = get_financial_health_score()
summary = get_summary()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏆 Health Score",
        value=f"{health['score']}/100",
        help="Based on savings rate, budgets and spending habits"
    )
    st.caption(health["status"])

with col2:
    st.metric(
        label="💵 Total Income",
        value=f"${summary['total_income']:,.2f}",
        help="Total income logged this month"
    )

with col3:
    st.metric(
        label="💸 Total Expenses",
        value=f"${summary['total_expenses']:,.2f}",
        help="Total expenses logged this month"
    )

with col4:
    savings_color = "normal" if summary["net_savings"] >= 0 else "inverse"
    st.metric(
        label="🏦 Net Savings",
        value=f"${summary['net_savings']:,.2f}",
        delta=f"{summary['savings_rate']}% savings rate",
        delta_color=savings_color
    )

st.divider()

# HEALTH SCORE BREAKDOWN
st.subheader("📊 Health Score Breakdown")

cols = st.columns(len(health["breakdown"]))
for i, check in enumerate(health["breakdown"]):
    with cols[i]:
        icon = "✅" if check["passed"] else "❌"
        st.metric(
            label=f"{icon} {check['check']}",
            value=f"{check['points']} pts"
        )

st.divider()

# MONTHLY TREND CHART
st.subheader("📈 6 Month Trend")

trend = get_monthly_trend(6)
trend_data = trend["trend"]

if any(t["total_income"] > 0 or t["total_expenses"] > 0 for t in trend_data):
    df_trend = pd.DataFrame(trend_data)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Income",
        x=df_trend["month"],
        y=df_trend["total_income"],
        marker_color="#2ecc71"
    ))
    fig.add_trace(go.Bar(
        name="Expenses",
        x=df_trend["month"],
        y=df_trend["total_expenses"],
        marker_color="#e74c3c"
    ))
    fig.add_trace(go.Scatter(
        name="Savings",
        x=df_trend["month"],
        y=df_trend["net_savings"],
        mode="lines+markers",
        line=dict(color="#3498db", width=2),
        marker=dict(size=8)
    ))
    fig.update_layout(
        barmode="group",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📭 No data yet — add some income and expenses to see your trend!")

st.divider()

# SPENDING BY CATEGORY PIE CHART
st.subheader("🥧 Spending by Category")

if summary["by_category"]:
    df_cat = pd.DataFrame(
        list(summary["by_category"].items()),
        columns=["Category", "Amount"]
    )
    fig_pie = px.pie(
        df_cat,
        values="Amount",
        names="Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("📭 No expenses logged yet — add some expenses to see spending breakdown!")

st.divider()

# LATEST AI ADVICE
st.subheader("🤖 Latest AI Advice")

latest = get_latest_advice()
if latest["success"]:
    st.info(latest["advice"])
    st.caption(f"Generated for {latest['month']}")
else:
    st.warning(latest["message"])
    st.page_link("pages/4_advice.py", label="👉 Click here to generate advice", icon="💡")