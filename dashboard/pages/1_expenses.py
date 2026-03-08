"""
Expenses Analytics Page — Finance Coach
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mcp_server.tools.expenses import log_expense, get_expenses, get_expenses_by_category, delete_expense
from mcp_server.tools.summary  import get_monthly_trend

st.set_page_config(page_title="Expenses · Finance Coach", page_icon="💸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
* { font-family:'DM Sans',sans-serif; box-sizing:border-box; }
.stApp { background:linear-gradient(135deg,#f0f4f8 0%,#eaf4f0 100%); }
header,footer,#MainMenu { visibility:hidden; }
.block-container { padding:1.8rem 2rem !important; max-width:1300px; }

.page-hdr { display:flex;align-items:center;gap:14px;margin-bottom:6px; }
.page-icon {
    width:48px;height:48px;border-radius:14px;
    background:linear-gradient(135deg,#e74c3c,#c0392b);
    display:flex;align-items:center;justify-content:center;
    font-size:1.4rem;box-shadow:0 4px 14px rgba(231,76,60,0.3);
}
.page-title { font-size:1.5rem;font-weight:700;color:#1a1a2e;margin:0; }
.page-sub   { font-size:0.78rem;color:#aaa;margin:2px 0 0; }

.metric-card {
    background:white;border-radius:14px;padding:18px 16px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
    border:1px solid rgba(255,255,255,0.9);text-align:center;
}
.metric-val   { font-size:1.55rem;font-weight:700;color:#1a1a2e;margin:4px 0 2px; }
.metric-label { font-size:0.72rem;color:#999;font-weight:500;text-transform:uppercase;letter-spacing:0.04em; }
.metric-sub   { font-size:0.71rem;color:#bbb;margin-top:2px; }

.chart-card {
    background:white;border-radius:16px;padding:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
    border:1px solid rgba(255,255,255,0.9);
}

.stButton > button {
    border-radius:10px !important;border:1.5px solid #e0e0e0 !important;
    background:white !important;color:#555 !important;
    font-size:0.82rem !important;font-weight:500 !important;
    box-shadow:0 1px 3px rgba(0,0,0,0.05) !important;
}
.stButton > button:hover { border-color:#1a936f !important;color:#1a936f !important;background:#f0faf6 !important; }
button[kind="primary"] {
    background:linear-gradient(135deg,#e74c3c,#c0392b) !important;
    color:white !important;border:none !important;
    box-shadow:0 4px 12px rgba(231,76,60,0.3) !important;
}
[data-testid="stForm"] {
    background:white;border-radius:16px;padding:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='page-hdr'>
    <div class='page-icon'>💸</div>
    <div>
        <p class='page-title'>Expenses</p>
        <p class='page-sub'>Track, analyze and manage your spending</p>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Data
result   = get_expenses()
cat_res  = get_expenses_by_category()
expenses = result["expenses"]

# ── Metric cards
m1, m2, m3, m4 = st.columns(4)
total = result["total"]
count = result["count"]
avg   = total / count if count > 0 else 0
top_cat = max(cat_res["by_category"], key=cat_res["by_category"].get) if cat_res["by_category"] else "—"

with m1:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Spent</div><div class='metric-val'>${total:,.2f}</div><div class='metric-sub'>{result['month']}</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Transactions</div><div class='metric-val'>{count}</div><div class='metric-sub'>this month</div></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Avg per Entry</div><div class='metric-val'>${avg:,.2f}</div><div class='metric-sub'>average</div></div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Top Category</div><div class='metric-val' style='font-size:1.1rem'>{top_cat.title()}</div><div class='metric-sub'>highest spend</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts
if expenses:
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("**🥧 Spending by Category**")
        df_cat = pd.DataFrame(list(cat_res["by_category"].items()), columns=["Category","Amount"])
        df_cat["Category"] = df_cat["Category"].str.title()
        colors = ["#1a936f","#e74c3c","#f39c12","#3498db","#9b59b6","#1abc9c","#e67e22","#2ecc71","#e91e63","#607d8b"]
        fig = px.pie(df_cat, values="Amount", names="Category", hole=0.42, color_discrete_sequence=colors)
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        fig.update_layout(height=300, showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("**📈 6-Month Spending Trend**")
        trend    = get_monthly_trend(6)
        df_trend = pd.DataFrame(trend["trend"])
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_trend["month"], y=df_trend["total_expenses"],
            fill='tozeroy', line=dict(color="#e74c3c", width=2.5),
            fillcolor="rgba(231,76,60,0.08)", name="Expenses",
            marker=dict(size=6, color="#e74c3c")
        ))
        fig2.update_layout(
            height=300, margin=dict(t=10,b=30,l=10,r=10),
            xaxis_title="Month", yaxis_title="Amount ($)",
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#f5f5f5")
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Category bar chart
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("**📊 Spending Breakdown by Category**")
    df_bar = pd.DataFrame(list(cat_res["by_category"].items()), columns=["Category","Amount"])
    df_bar["Category"] = df_bar["Category"].str.title()
    df_bar = df_bar.sort_values("Amount", ascending=True)
    fig3 = px.bar(df_bar, x="Amount", y="Category", orientation='h',
                  color="Amount", color_continuous_scale=[[0,"#ffeaa7"],[0.5,"#e17055"],[1,"#e74c3c"]],
                  text="Amount")
    fig3.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig3.update_layout(
        height=max(200, len(df_bar)*45), margin=dict(t=10,b=10,l=10,r=80),
        coloraxis_showscale=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, showticklabels=False), yaxis_title=""
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ── Table + Delete
if expenses:
    st.markdown("**📋 All Expenses This Month**")
    df = pd.DataFrame(expenses)[["date","category","amount","note","id"]]
    df.columns = ["Date","Category","Amount ($)","Note","ID"]
    df["Category"] = df["Category"].str.title()
    df = df.sort_values("Date", ascending=False)
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True,
                 column_config={"Amount ($)": st.column_config.NumberColumn(format="$%.2f")})

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🗑️ Delete an Expense"):
        options  = {f"{e['date']} · {e['category'].title()} · ${e['amount']:.2f}{' · ' + e['note'] if e.get('note') else ''}": e["id"] for e in expenses}
        selected = st.selectbox("Select to delete", list(options.keys()))
        if st.button("Delete", type="secondary"):
            r = delete_expense(options[selected])
            if r["success"]: st.success(r["message"]); st.rerun()

else:
    st.info("📭 No expenses logged this month yet. Use the form below!")

st.markdown("<br>", unsafe_allow_html=True)

# ── Log Form
st.markdown("**➕ Log New Expense**")
with st.form("exp_form"):
    c1, c2, c3 = st.columns(3)
    with c1: amount   = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    with c2: category = st.selectbox("Category", ["groceries","dining","rent","transport","utilities","entertainment","health","shopping","education","other"])
    with c3: date     = st.date_input("Date", value=datetime.today())
    note = st.text_input("Note (optional)", placeholder="e.g. Whole Foods weekend run")
    if st.form_submit_button("💸 Log Expense", use_container_width=True, type="primary"):
        r = log_expense(amount=amount, category=category, date=str(date), note=note)
        if r["success"]: st.success(r["message"]); st.rerun()
        else: st.error("Failed to log. Check your data.")