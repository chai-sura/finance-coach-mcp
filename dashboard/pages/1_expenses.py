"""
Expenses Page - Log and view expenses.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp_server.tools.expenses import log_expense, get_expenses, get_expenses_by_category, delete_expense

st.set_page_config(page_title="Expenses", page_icon="💸", layout="wide")

st.title("💸 Expenses")
st.caption("Log and track your spending.")
st.divider()

# LOG EXPENSE FORM
st.subheader("➕ Log New Expense")

with st.form("log_expense_form"):
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        category = st.selectbox("Category", [
            "groceries", "dining", "rent", "transport",
            "utilities", "entertainment", "health",
            "shopping", "education", "other"
        ])

    with col2:
        date = st.date_input("Date")
        note = st.text_input("Note (optional)", placeholder="e.g. Whole Foods run")

    submitted = st.form_submit_button("Log Expense 💸", use_container_width=True)

    if submitted:
        result = log_expense(
            amount=amount,
            category=category,
            date=str(date),
            note=note
        )
        if result["success"]:
            st.success(result["message"])
            st.rerun()
        else:
            st.error("Failed to log expense")

st.divider()

# EXPENSES TABLE
st.subheader("📋 This Month's Expenses")

result = get_expenses()
expenses = result["expenses"]

if expenses:
    st.metric("Total Spent", f"${result['total']:,.2f}", f"{result['count']} transactions")

    df = pd.DataFrame(expenses)
    df = df[["date", "category", "amount", "note", "id"]]
    df.columns = ["Date", "Category", "Amount ($)", "Note", "ID"]
    df = df.sort_values("Date", ascending=False)

    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    st.divider()

    # DELETE EXPENSE
    st.subheader("🗑️ Delete an Expense")

    expense_options = {
        f"{e['date']} | {e['category']} | ${e['amount']}": e["id"]
        for e in expenses
    }

    selected = st.selectbox("Select expense to delete", list(expense_options.keys()))

    if st.button("Delete Selected Expense", type="secondary"):
        result = delete_expense(expense_options[selected])
        if result["success"]:
            st.success(result["message"])
            st.rerun()
        else:
            st.error(result["message"])

    st.divider()

    # SPENDING BY CATEGORY CHART
    st.subheader("🥧 Spending by Category")

    cat_result = get_expenses_by_category()
    if cat_result["by_category"]:
        df_cat = pd.DataFrame(
            list(cat_result["by_category"].items()),
            columns=["Category", "Amount"]
        )
        fig = px.pie(
            df_cat,
            values="Amount",
            names="Category",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📭 No expenses logged this month yet — use the form above to add one!")