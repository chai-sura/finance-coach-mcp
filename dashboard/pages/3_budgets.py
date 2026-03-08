"""Budgets Analytics Page — Finance Coach"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mcp_server.tools.budgets import set_budget, get_budgets, get_budget_alerts

st.set_page_config(page_title="Budgets · Finance Coach", page_icon="🎯", layout="wide")

PAGE_COLOR = "#f39c12"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
* {{ font-family:'DM Sans',sans-serif; }}
.stApp {{ background:linear-gradient(135deg,#f0f4f8 0%,#eaf4f0 100%); }}
header,footer,#MainMenu {{ visibility:hidden; }}
.block-container {{ padding:1.8rem 2rem !important; max-width:1300px; }}
.page-hdr {{ display:flex;align-items:center;gap:14px;margin-bottom:20px; }}
.page-icon {{
    width:48px;height:48px;border-radius:14px;
    background:linear-gradient(135deg,{PAGE_COLOR},#e67e22);
    display:flex;align-items:center;justify-content:center;
    font-size:1.4rem;box-shadow:0 4px 14px rgba(243,156,18,0.3);
}}
.page-title {{ font-size:1.5rem;font-weight:700;color:#1a1a2e;margin:0; }}
.page-sub   {{ font-size:0.78rem;color:#aaa;margin:2px 0 0; }}
.metric-card {{
    background:white;border-radius:14px;padding:18px 16px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);text-align:center;
}}
.metric-val   {{ font-size:1.5rem;font-weight:700;color:#1a1a2e;margin:4px 0 2px; }}
.metric-label {{ font-size:0.70rem;color:#999;font-weight:600;text-transform:uppercase;letter-spacing:0.05em; }}
.metric-sub   {{ font-size:0.70rem;color:#bbb;margin-top:2px; }}
.chart-title  {{ font-size:0.92rem;font-weight:700;color:#1a1a2e;margin-bottom:12px;padding:0 2px; }}
.bud-card {{
    background:white;border-radius:13px;padding:15px 17px;margin-bottom:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}}
.bud-hdr  {{ display:flex;justify-content:space-between;align-items:center;margin-bottom:8px; }}
.bud-name {{ font-size:0.87rem;font-weight:600;color:#1a1a2e; }}
.bud-meta {{ font-size:0.73rem;color:#999;font-family:'DM Mono',monospace; }}
.bud-bg   {{ background:#f2f2f2;border-radius:8px;height:7px;overflow:hidden;margin-bottom:5px; }}
.bud-bar  {{ height:7px;border-radius:8px; }}
.bud-foot {{ display:flex;justify-content:space-between; }}
.bud-pct  {{ font-size:0.72rem;font-weight:600; }}
.bud-rem  {{ font-size:0.72rem;color:#aaa; }}
.stButton > button {{
    border-radius:10px !important;border:1.5px solid #e0e0e0 !important;
    background:white !important;color:#555 !important;font-size:0.82rem !important;
    font-weight:500 !important;box-shadow:0 1px 3px rgba(0,0,0,0.05) !important;
}}
.stButton > button:hover {{ border-color:{PAGE_COLOR} !important;color:{PAGE_COLOR} !important;background:#fffbf0 !important; }}
button[kind="primary"] {{
    background:linear-gradient(135deg,{PAGE_COLOR},#e67e22) !important;
    color:white !important;border:none !important;
    box-shadow:0 4px 12px rgba(243,156,18,0.25) !important;
}}
[data-testid="stForm"] {{ background:white;border-radius:16px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.06); }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='page-hdr'>
    <div class='page-icon'>🎯</div>
    <div><p class='page-title'>Budgets</p><p class='page-sub'>Set limits, track spending, stay on target</p></div>
</div>""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

result  = get_budgets()
budgets = result["budgets"]
alerts  = get_budget_alerts()

if alerts["count"] > 0:
    for a in alerts["alerts"]:
        if a["status"] == "over": st.error(f"🔴 **{a['category'].title()}** — Over budget! Spent ${a['spent']} of ${a['amount']}")
        else: st.warning(f"🟡 **{a['category'].title()}** — {a['percent_used']}% used · ${a['remaining']} remaining")
    st.markdown("<br>", unsafe_allow_html=True)

ok_cnt  = len([b for b in budgets if b["status"]=="ok"])
over_cnt= len([b for b in budgets if b["status"]=="over"])
tot_lim = sum(b["amount"] for b in budgets)
tot_spt = sum(b["spent"]  for b in budgets)
tot_rem = tot_lim - tot_spt

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Budgets</div><div class='metric-val'>{len(budgets)}</div><div class='metric-sub'>categories</div></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='metric-card'><div class='metric-label'>On Track</div><div class='metric-val' style='color:#1a936f'>{ok_cnt}</div><div class='metric-sub'>🟢 healthy</div></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='metric-card'><div class='metric-label'>Over Budget</div><div class='metric-val' style='color:#e74c3c'>{over_cnt}</div><div class='metric-sub'>🔴 exceeded</div></div>", unsafe_allow_html=True)
with m4:
    rc = "#1a936f" if tot_rem >= 0 else "#e74c3c"
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Remaining</div><div class='metric-val' style='color:{rc}'>${tot_rem:,.2f}</div><div class='metric-sub'>across all</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if budgets:
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown("<p class='chart-title'>📊 Budget vs Actual Spending</p>", unsafe_allow_html=True)
            df = pd.DataFrame(budgets)
            df["category"] = df["category"].str.title()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Budget", x=df["category"], y=df["amount"],
                                 marker_color="#d5f5e3",
                                 text=df["amount"].apply(lambda x: f"${x:,.0f}"),
                                 textposition="outside"))
            fig.add_trace(go.Bar(name="Spent", x=df["category"], y=df["spent"],
                                 marker_color=["#e74c3c" if s=="over" else "#f39c12" if s=="warning" else "#1a936f" for s in df["status"].tolist()],
                                 text=df["spent"].apply(lambda x: f"${x:,.0f}"),
                                 textposition="outside"))
            fig.update_layout(
                barmode="group", height=290, margin=dict(t=5,b=40,l=5,r=5),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#f0f0f0", showticklabels=False),
                legend=dict(orientation="h", y=-0.3, font=dict(size=11))
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.markdown("<p class='chart-title'>🥧 Budget Allocation</p>", unsafe_allow_html=True)
            df_alloc = pd.DataFrame(budgets)
            df_alloc["category"] = df_alloc["category"].str.title()
            colors = ["#1a936f","#114b5f","#f39c12","#e74c3c","#3498db","#9b59b6","#1abc9c","#e67e22","#2ecc71","#607d8b"]
            fig2 = px.pie(df_alloc, values="amount", names="category", hole=0.42,
                          color_discrete_sequence=colors)
            fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
            fig2.update_layout(
                height=290, showlegend=False, margin=dict(t=5,b=5,l=5,r=5),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Progress cards — 2 col grid
    st.markdown("<p class='chart-title'>📈 Budget Progress</p>", unsafe_allow_html=True)
    bc1, bc2 = st.columns(2, gap="medium")
    for i, b in enumerate(budgets):
        bar_color = "#e74c3c" if b["status"]=="over" else "#f39c12" if b["status"]=="warning" else "#1a936f"
        icon      = "🔴" if b["status"]=="over" else "🟡" if b["status"]=="warning" else "🟢"
        pct       = min(b["percent_used"], 100)
        rem_label = f"${b['remaining']} left" if b['remaining'] >= 0 else f"${abs(b['remaining'])} over!"
        card = f"""
        <div class='bud-card'>
            <div class='bud-hdr'>
                <span class='bud-name'>{icon} {b['category'].title()}</span>
                <span class='bud-meta'>${b['spent']} / ${b['amount']} · {b['period']}</span>
            </div>
            <div class='bud-bg'><div class='bud-bar' style='width:{pct}%;background:{bar_color}'></div></div>
            <div class='bud-foot'>
                <span class='bud-pct' style='color:{bar_color}'>{b['percent_used']}% used</span>
                <span class='bud-rem'>{rem_label}</span>
            </div>
        </div>"""
        if i % 2 == 0: bc1.markdown(card, unsafe_allow_html=True)
        else:          bc2.markdown(card, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📋 View All Budgets as Table"):
        df_t = pd.DataFrame(budgets)[["category","amount","spent","remaining","percent_used","status","period"]]
        df_t.columns = ["Category","Limit ($)","Spent ($)","Remaining ($)","Used (%)","Status","Period"]
        df_t["Category"] = df_t["Category"].str.title()
        df_t["Status"]   = df_t["Status"].str.title()
        st.dataframe(df_t, use_container_width=True, hide_index=True,
                     column_config={
                         "Limit ($)":     st.column_config.NumberColumn(format="$%.2f"),
                         "Spent ($)":     st.column_config.NumberColumn(format="$%.2f"),
                         "Remaining ($)": st.column_config.NumberColumn(format="$%.2f"),
                         "Used (%)":      st.column_config.ProgressColumn(min_value=0, max_value=100),
                     })
else:
    st.info("📭 No budgets set yet — create your first budget below!")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>➕ Set a New Budget</p>", unsafe_allow_html=True)
with st.form("bud_form"):
    c1, c2, c3 = st.columns(3)
    with c1: category = st.selectbox("Category", ["groceries","dining","rent","transport","utilities","entertainment","health","shopping","education","other"])
    with c2: amount   = st.number_input("Budget Limit ($)", min_value=1.0, step=10.0, format="%.2f")
    with c3: period   = st.selectbox("Period", ["monthly","weekly"])
    if st.form_submit_button("🎯 Set Budget", use_container_width=True, type="primary"):
        r = set_budget(category=category, amount=amount, period=period)
        if r["success"]: st.success(r["message"]); st.rerun()