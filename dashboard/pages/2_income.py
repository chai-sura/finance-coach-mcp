"""
Income Page - Log and view income entries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp_server.tools.income import log_income, get_income, get_income_by_source, delete_income

st.set_page_config(page_title="Income", page_icon="💵", layout="wide")

st.title("💵 Income")
st.caption("Log and track your earnings.")
st.divider()

# LOG INCOME FORM
st.subheader("➕ Log New Income")

with st.form("log_income_form"):
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        source = st.selectbox("Source", [
            "salary", "freelance", "investment",
            "bonus", "gift", "rental", "other"
        ])

    with col2:
        date = st.date_input("Date")
        note = st.text_input("Note (optional)", placeholder="e.g. March salary")

    submitted = st.form_submit_button("Log Income 💵", use_container_width=True)

    if submitted:
        result = log_income(
            amount=amount,
            source=source,
            date=str(date),
            note=note
        )
        if result["success"]:
            st.success(result["message"])
            st.rerun()
        else:
            st.error("Failed to log income")

st.divider()

# INCOME TABLE
st.subheader("📋 This Month's Income")

result = get_income()
income = result["income"]

if income:
    st.metric("Total Earned", f"${result['total']:,.2f}", f"{result['count']} entries")

    df = pd.DataFrame(income)
    df = df[["date", "source", "amount", "note", "id"]]
    df.columns = ["Date", "Source", "Amount ($)", "Note", "ID"]
    df = df.sort_values("Date", ascending=False)

    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    st.divider()

    # DELETE INCOME
    st.subheader("🗑️ Delete an Income Entry")

    income_options = {
        f"{i['date']} | {i['source']} | ${i['amount']}": i["id"]
        for i in income
    }

    selected = st.selectbox("Select income to delete", list(income_options.keys()))

    if st.button("Delete Selected Income", type="secondary"):
        result = delete_income(income_options[selected])
        if result["success"]:
            st.success(result["message"])
            st.rerun()
        else:
            st.error(result["message"])

    st.divider()

    # INCOME BY SOURCE CHART
    st.subheader("📊 Income by Source")

    source_result = get_income_by_source()
    if source_result["by_source"]:
        df_source = pd.DataFrame(
            list(source_result["by_source"].items()),
            columns=["Source", "Amount"]
        )
        fig = px.bar(
            df_source,
            x="Source",
            y="Amount",
            color="Source",
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto=True
        )
        fig.update_layout(
            xaxis_title="Source",
            yaxis_title="Amount ($)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📭 No income logged this month yet — use the form above to add one!")