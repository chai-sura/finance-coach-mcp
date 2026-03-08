"""Income Analytics Page — Finance Coach"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mcp_server.tools.income  import log_income, get_income, get_income_by_source, delete_income
from mcp_server.tools.summary import get_monthly_trend

st.set_page_config(page_title="Income · Finance Coach", page_icon="💵", layout="wide")

PAGE_COLOR = "#1a936f"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
* {{ font-family:'DM Sans',sans-serif; }}
.stApp {{ background:linear-gradient(135deg,#f0f4f8 0%,#eaf4f0 100%); }}
header,footer,#MainMenu {{ visibility:hidden; }}
.block-container {{ padding:1.8rem 2rem !important; max-width:1300px; }}
.page-hdr {{ display:flex;align-items:center;gap:14px;margin-bottom:20px; }}
.page-icon {{
    width:48px;height:48px;border-radius:14px;
    background:linear-gradient(135deg,{PAGE_COLOR},#114b5f);
    display:flex;align-items:center;justify-content:center;
    font-size:1.4rem;box-shadow:0 4px 14px rgba(26,147,111,0.3);
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
.stButton > button {{
    border-radius:10px !important;border:1.5px solid #e0e0e0 !important;
    background:white !important;color:#555 !important;font-size:0.82rem !important;
    font-weight:500 !important;box-shadow:0 1px 3px rgba(0,0,0,0.05) !important;
}}
.stButton > button:hover {{ border-color:{PAGE_COLOR} !important;color:{PAGE_COLOR} !important;background:#f0faf6 !important; }}
button[kind="primary"] {{
    background:linear-gradient(135deg,{PAGE_COLOR},#114b5f) !important;
    color:white !important;border:none !important;
    box-shadow:0 4px 12px rgba(26,147,111,0.25) !important;
}}
[data-testid="stForm"] {{ background:white;border-radius:16px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.06); }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='page-hdr'>
    <div class='page-icon'>💵</div>
    <div><p class='page-title'>Income</p><p class='page-sub'>Track and analyze your earnings</p></div>
</div>""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

result  = get_income()
src_res = get_income_by_source()
income  = result["income"]
total   = result["total"]
count   = result["count"]
avg     = total / count if count > 0 else 0
top_src = max(src_res["by_source"], key=src_res["by_source"].get) if src_res["by_source"] else "—"

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Earned</div><div class='metric-val'>${total:,.2f}</div><div class='metric-sub'>{result['month']}</div></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='metric-card'><div class='metric-label'>Entries</div><div class='metric-val'>{count}</div><div class='metric-sub'>this month</div></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='metric-card'><div class='metric-label'>Avg per Entry</div><div class='metric-val'>${avg:,.2f}</div><div class='metric-sub'>average</div></div>", unsafe_allow_html=True)
with m4: st.markdown(f"<div class='metric-card'><div class='metric-label'>Top Source</div><div class='metric-val' style='font-size:1.1rem'>{top_src.title()}</div><div class='metric-sub'>highest income</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if income:
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown("<p class='chart-title'>📊 Income by Source</p>", unsafe_allow_html=True)
            df_src = pd.DataFrame(list(src_res["by_source"].items()), columns=["Source","Amount"])
            df_src["Source"] = df_src["Source"].str.title()
            df_src = df_src.sort_values("Amount", ascending=False)
            colors = ["#1a936f","#114b5f","#2ecc71","#27ae60","#1abc9c","#16a085","#0d6b56"]
            fig = px.bar(df_src, x="Source", y="Amount", color="Source",
                         color_discrete_sequence=colors, text_auto=True)
            fig.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
            fig.update_layout(
                height=290, showlegend=False, margin=dict(t=5,b=5,l=5,r=5),
                xaxis_title="", yaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#f0f0f0", showticklabels=False)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.markdown("<p class='chart-title'>📈 6-Month Income vs Expenses</p>", unsafe_allow_html=True)
            trend    = get_monthly_trend(6)
            df_trend = pd.DataFrame(trend["trend"])
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_trend["month"], y=df_trend["total_income"],
                fill='tozeroy', line=dict(color="#1a936f", width=2.5),
                fillcolor="rgba(26,147,111,0.08)", name="Income",
                marker=dict(size=6, color="#1a936f")
            ))
            fig2.add_trace(go.Scatter(
                x=df_trend["month"], y=df_trend["total_expenses"],
                line=dict(color="#e74c3c", width=2, dash="dot"),
                name="Expenses", marker=dict(size=5, color="#e74c3c")
            ))
            fig2.update_layout(
                height=290, margin=dict(t=5,b=40,l=5,r=5),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                yaxis=dict(gridcolor="#f0f0f0"),
                legend=dict(orientation="h", y=-0.35, font=dict(size=11))
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<p class='chart-title'>💰 Income vs Expenses Split — This Month</p>", unsafe_allow_html=True)
        trend_now = get_monthly_trend(1)
        if trend_now["trend"]:
            t   = trend_now["trend"][-1]
            inc = t["total_income"]
            exp = t["total_expenses"]
            sav = max(inc - exp, 0)
            df_donut = pd.DataFrame({"Label":["Expenses","Savings"],"Value":[exp, sav]})
            fig3 = px.pie(df_donut, values="Value", names="Label", hole=0.5,
                          color_discrete_map={"Expenses":"#e74c3c","Savings":"#1a936f"})
            fig3.update_traces(textposition='inside', textinfo='percent+label',
                               textfont_size=13)
            fig3.update_layout(
                height=260, margin=dict(t=5,b=5,l=5,r=5), showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<p class='chart-title'>📋 All Income This Month</p>", unsafe_allow_html=True)
if income:
    df = pd.DataFrame(income)[["date","source","amount","note","id"]]
    df.columns = ["Date","Source","Amount ($)","Note","ID"]
    df["Source"] = df["Source"].str.title()
    df = df.sort_values("Date", ascending=False)
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True,
                 column_config={"Amount ($)": st.column_config.NumberColumn(format="$%.2f")})

    with st.expander("🗑️ Delete an Income Entry"):
        options  = {f"{i['date']} · {i['source'].title()} · ${i['amount']:.2f}": i["id"] for i in income}
        selected = st.selectbox("Select to delete", list(options.keys()))
        if st.button("Delete", type="secondary"):
            r = delete_income(options[selected])
            if r["success"]: st.success(r["message"]); st.rerun()
else:
    st.info("📭 No income logged this month yet.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>➕ Log New Income</p>", unsafe_allow_html=True)
with st.form("inc_form"):
    c1, c2, c3 = st.columns(3)
    with c1: amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    with c2: source = st.selectbox("Source", ["salary","freelance","investment","bonus","gift","rental","other"])
    with c3: date   = st.date_input("Date", value=datetime.today())
    note = st.text_input("Note (optional)", placeholder="e.g. March salary deposit")
    if st.form_submit_button("💵 Log Income", use_container_width=True, type="primary"):
        r = log_income(amount=amount, source=source, date=str(date), note=note)
        if r["success"]: st.success(r["message"]); st.rerun()
        else: st.error("Failed to log.")