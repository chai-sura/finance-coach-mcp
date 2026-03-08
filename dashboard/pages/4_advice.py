"""AI Advice Page — Finance Coach"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mcp_server.tools.advice  import get_advice, get_advice_history
from mcp_server.tools.summary import get_summary, get_monthly_trend
from mcp_server.tools.context import get_financial_health_score

st.set_page_config(page_title="AI Advice · Finance Coach", page_icon="🤖", layout="wide")

PAGE_COLOR = "#9b59b6"

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
    background:linear-gradient(135deg,{PAGE_COLOR},#6c3483);
    display:flex;align-items:center;justify-content:center;
    font-size:1.4rem;box-shadow:0 4px 14px rgba(155,89,182,0.3);
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
.advice-card {{
    background:white;border-radius:13px;padding:18px 20px;margin-bottom:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);border-left:4px solid {PAGE_COLOR};
}}
.advice-latest {{
    background:linear-gradient(135deg,#fdf8ff,#f8f0ff);
    border-radius:13px;padding:18px 20px;margin-bottom:12px;
    box-shadow:0 2px 10px rgba(155,89,182,0.1);border-left:4px solid {PAGE_COLOR};
}}
.advice-tag  {{ font-size:0.70rem;color:{PAGE_COLOR};font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px; }}
.advice-text {{ font-size:0.87rem;color:#333;line-height:1.75; }}
.health-row  {{ display:flex;align-items:center;gap:10px;padding:10px 13px;background:white;border-radius:10px;margin-bottom:7px;box-shadow:0 1px 4px rgba(0,0,0,0.04); }}
.stButton > button {{
    border-radius:10px !important;border:1.5px solid #e0e0e0 !important;
    background:white !important;color:#555 !important;font-size:0.82rem !important;
    font-weight:500 !important;box-shadow:0 1px 3px rgba(0,0,0,0.05) !important;
}}
.stButton > button:hover {{ border-color:{PAGE_COLOR} !important;color:{PAGE_COLOR} !important;background:#faf0ff !important; }}
button[kind="primary"] {{
    background:linear-gradient(135deg,{PAGE_COLOR},#6c3483) !important;
    color:white !important;border:none !important;
    box-shadow:0 4px 12px rgba(155,89,182,0.25) !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='page-hdr'>
    <div class='page-icon'>🤖</div>
    <div><p class='page-title'>AI Advice</p><p class='page-sub'>Personalized financial guidance powered by GPT-4o-mini</p></div>
</div>""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

summary = get_summary()
health  = get_financial_health_score()
score   = health["score"]
sc_col  = "#1a936f" if score>=80 else "#f39c12" if score>=60 else "#e74c3c"

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Health Score</div><div class='metric-val' style='color:{sc_col}'>{score}</div><div class='metric-sub'>{health['status'].split()[0]}</div></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='metric-card'><div class='metric-label'>Income</div><div class='metric-val'>${summary['total_income']:,.0f}</div><div class='metric-sub'>this month</div></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='metric-card'><div class='metric-label'>Expenses</div><div class='metric-val'>${summary['total_expenses']:,.0f}</div><div class='metric-sub'>this month</div></div>", unsafe_allow_html=True)
with m4:
    sav_col = "#1a936f" if summary['net_savings']>=0 else "#e74c3c"
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Savings Rate</div><div class='metric-val' style='color:{sav_col}'>{summary['savings_rate']}%</div><div class='metric-sub'>this month</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1], gap="medium")

with col1:
    # Generate advice
    with st.container(border=True):
        st.markdown("<p class='chart-title'>💡 Generate Fresh AI Advice</p>", unsafe_allow_html=True)
        st.caption("Personalized advice based on your actual income, expenses, and budget data.")
        if st.button("🤖 Generate Personalized Advice", type="primary", use_container_width=True):
            with st.spinner("Analyzing your finances..."):
                r = get_advice()
            if r.get("success"):
                st.success("✅ New advice generated!")
                st.markdown(f"""
                <div class='advice-latest'>
                    <div class='advice-tag'>🆕 Just Generated · {r.get('month','')}</div>
                    <div class='advice-text'>{r['advice']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.error("Failed to generate advice. Check your OpenAI API key.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Trend chart
    with st.container(border=True):
        st.markdown("<p class='chart-title'>📈 Income vs Expenses — 6 Month View</p>", unsafe_allow_html=True)
        trend    = get_monthly_trend(6)
        df_trend = pd.DataFrame(trend["trend"])
        if not df_trend.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_trend["month"], y=df_trend["total_income"],
                name="Income", line=dict(color="#1a936f", width=2.5),
                fill='tozeroy', fillcolor="rgba(26,147,111,0.07)",
                marker=dict(size=6)
            ))
            fig.add_trace(go.Scatter(
                x=df_trend["month"], y=df_trend["total_expenses"],
                name="Expenses", line=dict(color="#e74c3c", width=2),
                marker=dict(size=5)
            ))
            fig.update_layout(
                height=240, margin=dict(t=5,b=40,l=5,r=5),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                yaxis=dict(gridcolor="#f0f0f0"),
                legend=dict(orientation="h", y=-0.35, font=dict(size=11))
            )
            st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("<p class='chart-title'>🏆 Financial Health Score</p>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={
                'axis':{'range':[0,100],'tickcolor':'#ddd','tickfont':{'size':10}},
                'bar':{'color': sc_col, 'thickness': 0.25},
                'bgcolor':'#f5f5f5',
                'steps':[
                    {'range':[0,60],  'color':'#fde8e8'},
                    {'range':[60,80], 'color':'#fef9e7'},
                    {'range':[80,100],'color':'#eafaf1'},
                ],
            },
            number={'suffix':'/100','font':{'size':26,'color':sc_col}}
        ))
        fig_gauge.update_layout(
            height=200, margin=dict(t=20,b=10,l=20,r=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<p style='text-align:center;font-weight:700;color:{sc_col};font-size:0.9rem;margin:0'>{health['status']}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        checks = health.get("checks", {})
        if checks:
            for check_name, passed in checks.items():
                icon  = "✅" if passed else "❌"
                color = "#1a936f" if passed else "#e74c3c"
                label = check_name.replace("_"," ").title()
                st.markdown(f"""
                <div class='health-row'>
                    <span>{icon}</span>
                    <span style='font-size:0.82rem;font-weight:500;color:{color}'>{label}</span>
                </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Advice History
st.markdown("<p class='chart-title'>📚 Advice History</p>", unsafe_allow_html=True)
history         = get_advice_history()
history_entries = history.get("history") or history.get("advice_history") or (history if isinstance(history, list) else [])

if history_entries:
    for i, entry in enumerate(reversed(history_entries)):
        is_latest  = (i == 0)
        card_class = "advice-latest" if is_latest else "advice-card"
        tag_text   = f"🆕 Latest · {entry.get('month','')}" if is_latest else f"📅 {entry.get('month','Unknown')}"
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='advice-tag'>{tag_text}</div>
            <div class='advice-text'>{entry.get('advice','')}</div>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align:center;padding:40px 20px;background:white;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06)'>
        <div style='font-size:2.5rem;margin-bottom:12px'>🤖</div>
        <p style='color:#888;font-size:0.9rem;margin:0'>No advice generated yet.</p>
        <p style='color:#bbb;font-size:0.8rem;margin:4px 0 0'>Click <strong>Generate Personalized Advice</strong> above to get started!</p>
    </div>""", unsafe_allow_html=True)