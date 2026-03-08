"""
Finance Coach — Main Dashboard
"""
import streamlit as st
import sys, os, json
from datetime import datetime
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai import OpenAI
from dotenv import load_dotenv
from mcp_server.tools.expenses import log_expense
from mcp_server.tools.income   import log_income
from mcp_server.tools.budgets  import set_budget, get_budgets, get_budget_alerts
from mcp_server.tools.summary  import get_summary
from mcp_server.tools.context  import get_financial_health_score
from mcp_server.tools.advice   import get_advice

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Finance Coach", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
* { font-family:'DM Sans',sans-serif; box-sizing:border-box; }
.stApp { background:linear-gradient(135deg,#f0f4f8 0%,#eaf4f0 100%); }
header,footer,#MainMenu { visibility:hidden; }
.block-container { padding:1.5rem !important; }
[data-testid="stSidebar"] { display:none; }

/* ── LEFT PANEL ── */
.brand { display:flex;align-items:center;gap:10px;margin-bottom:4px; }
.brand-logo {
    width:40px;height:40px;
    background:linear-gradient(135deg,#1a936f,#114b5f);
    border-radius:12px;display:flex;align-items:center;justify-content:center;
    font-size:1.15rem;box-shadow:0 4px 14px rgba(26,147,111,0.35);
}
.brand-name { font-size:1.2rem;font-weight:700;color:#1a1a2e;margin:0; }
.brand-sub  { font-size:0.73rem;color:#bbb;margin:0 0 20px 0; }

.section-label {
    font-size:0.68rem;font-weight:700;color:#ccc;
    letter-spacing:0.1em;text-transform:uppercase;margin:18px 0 8px;
}

/* ── STAT CARDS ── */
.stat-card {
    background:white;border-radius:14px;padding:14px 16px;margin-bottom:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);border:1px solid rgba(255,255,255,0.9);
}
.stat-lbl { font-size:0.75rem;color:#999;font-weight:500;margin-bottom:5px; }
.stat-row { display:flex;justify-content:space-between;align-items:baseline; }
.stat-val { font-size:1.05rem;font-weight:700;color:#1a1a2e; }
.stat-badge { font-size:0.70rem;font-weight:600; }
.prog-bg  { background:#f0f0f0;border-radius:8px;height:5px;margin-top:8px;overflow:hidden; }
.prog-fill{ height:5px;border-radius:8px; }

/* ── NAV LINKS ── */
[data-testid="stPageLink"] a {
    display:flex;align-items:center;gap:8px;
    padding:9px 12px;border-radius:10px;
    font-size:0.82rem;font-weight:500;color:#555;
    text-decoration:none;transition:all 0.18s;
    background:white;margin-bottom:6px;
    box-shadow:0 1px 4px rgba(0,0,0,0.05);
    border:1px solid #f0f0f0;
}
[data-testid="stPageLink"] a:hover {
    background:#f0faf6;color:#1a936f;border-color:#1a936f;
}

/* ── CHAT HEADER ── */
.chat-header {
    background:white;border-radius:16px 16px 0 0;
    padding:14px 18px;border-bottom:1px solid #f2f2f2;
    display:flex;align-items:center;gap:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}
.chat-av {
    width:42px;height:42px;
    background:linear-gradient(135deg,#1a936f,#114b5f);
    border-radius:13px;display:flex;align-items:center;
    justify-content:center;font-size:1.15rem;
    box-shadow:0 4px 10px rgba(26,147,111,0.3);
}
.chat-name { font-weight:700;font-size:0.94rem;color:#1a1a2e; }
.chat-sub  { font-size:0.72rem;color:#aaa;margin-top:1px; }
.dot {
    width:7px;height:7px;background:#1a936f;border-radius:50%;
    display:inline-block;margin-right:4px;
    box-shadow:0 0 0 2px rgba(26,147,111,0.2);
}

/* ── MESSAGES ── */
.m-ai { display:flex;gap:9px;margin:12px 4px;align-items:flex-start; }
.m-av {
    width:28px;height:28px;border-radius:8px;flex-shrink:0;margin-top:2px;
    background:linear-gradient(135deg,#1a936f,#114b5f);
    display:flex;align-items:center;justify-content:center;font-size:0.8rem;
    box-shadow:0 2px 6px rgba(26,147,111,0.2);
}
.m-ai-b {
    background:#f7f8fc;border-radius:0 13px 13px 13px;
    padding:10px 14px;max-width:84%;
    font-size:0.86rem;line-height:1.65;color:#2d2d2d;
    border:1px solid #eef0f6;
}
.m-user { display:flex;justify-content:flex-end;margin:12px 4px; }
.m-user-b {
    background:linear-gradient(135deg,#1a936f,#114b5f);
    color:white;border-radius:13px 13px 0 13px;
    padding:10px 14px;max-width:72%;
    font-size:0.86rem;line-height:1.65;
    box-shadow:0 4px 10px rgba(26,147,111,0.2);
}
.m-time      { font-size:0.65rem;color:#ccc;margin-top:3px;padding-left:2px; }
.m-time-user { font-size:0.65rem;color:rgba(255,255,255,0.45);margin-top:3px;text-align:right; }

.badges { margin:0 4px 8px 38px; }
.badge-tool {
    display:inline-flex;align-items:center;gap:3px;
    background:#fff3e0;color:#e67e22;border:1px solid #fad7a0;
    border-radius:20px;padding:2px 9px;font-size:0.67rem;font-weight:600;margin-right:4px;
}
.badge-ok {
    display:inline-flex;align-items:center;gap:3px;
    background:#e8faf2;color:#1a936f;border:1px solid #a9dfbf;
    border-radius:20px;padding:2px 9px;font-size:0.67rem;font-weight:600;
}

/* ── CHIPS ── */
.chip-row .stButton > button {
    border-radius:20px !important;font-size:0.69rem !important;
    padding:3px 11px !important;height:26px !important;
    border:1.5px solid #e0e0e0 !important;background:white !important;
    color:#666 !important;font-weight:500 !important;
    box-shadow:0 1px 2px rgba(0,0,0,0.04) !important;white-space:nowrap !important;
}
.chip-row .stButton > button:hover {
    border-color:#1a936f !important;color:#1a936f !important;background:#f0faf6 !important;
}

/* ── TEXT INPUT as chat bar ── */
div[data-testid="stTextInput"] input {
    border-radius:14px !important;border:1.5px solid #ddd !important;
    background:white !important;padding:11px 16px !important;
    font-size:0.87rem !important;color:#333 !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.05) !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:#1a936f !important;
    box-shadow:0 0 0 3px rgba(26,147,111,0.1) !important;outline:none !important;
}
div[data-testid="stTextInput"] label { display:none !important; }

/* ── SEND BUTTON ── */
div[data-testid="stButton"] button[kind="primary"] {
    background:linear-gradient(135deg,#1a936f,#114b5f) !important;
    border:none !important;border-radius:12px !important;
    color:white !important;font-weight:600 !important;
    box-shadow:0 4px 12px rgba(26,147,111,0.3) !important;height:44px !important;
}

/* ── RIGHT PANEL ── */
.r-card {
    background:white;border-radius:14px;padding:16px;margin-bottom:12px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);border:1px solid rgba(255,255,255,0.9);
}
.r-card-hdr { display:flex;justify-content:space-between;align-items:center;margin-bottom:14px; }
.r-card-ttl { font-size:0.87rem;font-weight:700;color:#1a1a2e; }
.bud-item { margin-bottom:12px; }
.bud-row  { display:flex;justify-content:space-between;align-items:center;margin-bottom:5px; }
.bud-name { font-size:0.81rem;font-weight:600;color:#333; }
.bud-val  { font-size:0.73rem;color:#999;font-family:'DM Mono',monospace; }
.bud-sub  { font-size:0.68rem;color:#ccc;margin-top:3px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"👋 Hi! I'm your personal Finance Coach.\n\nI can log expenses, track income, set budgets, and give personalized advice. Just talk to me naturally!\n\nTry: *'I spent $50 on groceries'* or *'I earned $3000 salary'* or *'What's my summary?'*","time":datetime.now().strftime("%I:%M %p"),"tool":None}]

for k,v in [("show_fab",False),("show_exp_modal",False),("show_inc_modal",False),("show_bud_modal",False),("prefill",""),("ikey",0)]:
    if k not in st.session_state: st.session_state[k] = v


# ── AI AGENT
def process_message(user_input: str) -> dict:
    tools: Any = [
        {"type":"function","function":{"name":"log_expense","description":"Log expense when user mentions spending","parameters":{"type":"object","properties":{"amount":{"type":"number"},"category":{"type":"string","description":"groceries,dining,rent,transport,utilities,entertainment,health,shopping,education,other"},"date":{"type":"string","description":"YYYY-MM-DD"},"note":{"type":"string"}},"required":["amount","category"]}}},
        {"type":"function","function":{"name":"log_income","description":"Log income when user mentions earning money","parameters":{"type":"object","properties":{"amount":{"type":"number"},"source":{"type":"string","description":"salary,freelance,investment,bonus,gift,rental,other"},"date":{"type":"string"},"note":{"type":"string"}},"required":["amount","source"]}}},
        {"type":"function","function":{"name":"set_budget","description":"Set a spending budget","parameters":{"type":"object","properties":{"category":{"type":"string"},"amount":{"type":"number"},"period":{"type":"string","description":"monthly or weekly"}},"required":["category","amount"]}}},
        {"type":"function","function":{"name":"get_summary","description":"Get financial summary","parameters":{"type":"object","properties":{"month":{"type":"integer"},"year":{"type":"integer"}}}}},
        {"type":"function","function":{"name":"get_advice","description":"Give financial advice and tips","parameters":{"type":"object","properties":{"month":{"type":"integer"},"year":{"type":"integer"}}}}},
    ]
    conv: Any = [{"role":"system","content":f"You are a warm, smart personal finance coach. Today: {datetime.now().strftime('%B %d, %Y')}. Always call the right tool for money actions. After tool use, respond briefly (2-3 sentences) and encouragingly."}]
    for m in st.session_state.messages[-8:]:
        if m["role"] in ["user","assistant"] and m.get("content"):
            conv.append({"role":m["role"],"content":m["content"]})
    conv.append({"role":"user","content":user_input})

    r = client.chat.completions.create(model="gpt-4o-mini",messages=conv,tools=tools,tool_choice="auto",max_tokens=300,temperature=0.7)
    msg  = r.choices[0].message
    tool = None

    if msg.tool_calls:
        tc   = msg.tool_calls[0]
        tool = tc.function.name  # type: ignore
        args = json.loads(tc.function.arguments)  # type: ignore
        fn   = {"log_expense":log_expense,"log_income":log_income,"set_budget":set_budget,"get_summary":get_summary,"get_advice":get_advice}.get(tool, lambda **_: {})
        res  = fn(**args)
        conv.extend([msg, {"role":"tool","tool_call_id":tc.id,"content":str(res)}])  # type: ignore
        reply = client.chat.completions.create(model="gpt-4o-mini",messages=conv,max_tokens=200,temperature=0.7).choices[0].message.content
    else:
        reply = msg.content
    return {"reply": reply, "tool": tool}


# ── MODALS
@st.dialog("💸 Log New Expense")
def expense_modal():
    with st.form("me"):
        c1,c2 = st.columns(2)
        with c1: amt = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        with c2: cat = st.selectbox("Category", ["groceries","dining","rent","transport","utilities","entertainment","health","shopping","education","other"])
        d = st.date_input("Date")
        n = st.text_input("Note", placeholder="e.g. Whole Foods run")
        if st.form_submit_button("💸 Log Expense", use_container_width=True):
            r = log_expense(amount=amt, category=cat, date=str(d), note=n)
            if r["success"]: st.success(r["message"]); st.session_state.show_exp_modal=False; st.rerun()

@st.dialog("💵 Log New Income")
def income_modal():
    with st.form("mi"):
        c1,c2 = st.columns(2)
        with c1: amt = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        with c2: src = st.selectbox("Source", ["salary","freelance","investment","bonus","gift","rental","other"])
        d = st.date_input("Date")
        n = st.text_input("Note", placeholder="e.g. March salary")
        if st.form_submit_button("💵 Log Income", use_container_width=True):
            r = log_income(amount=amt, source=src, date=str(d), note=n)
            if r["success"]: st.success(r["message"]); st.session_state.show_inc_modal=False; st.rerun()

@st.dialog("🎯 Set Budget")
def budget_modal():
    with st.form("mb"):
        c1,c2 = st.columns(2)
        with c1: cat = st.selectbox("Category", ["groceries","dining","rent","transport","utilities","entertainment","health","shopping","education","other"])
        with c2: per = st.selectbox("Period", ["monthly","weekly"])
        amt = st.number_input("Limit ($)", min_value=1.0, step=10.0, format="%.2f")
        if st.form_submit_button("🎯 Set Budget", use_container_width=True):
            r = set_budget(category=cat, amount=amt, period=per)
            if r["success"]: st.success(r["message"]); st.session_state.show_bud_modal=False; st.rerun()

if st.session_state.show_exp_modal: expense_modal()
if st.session_state.show_inc_modal: income_modal()
if st.session_state.show_bud_modal: budget_modal()


# ── DATA
summary = get_summary()
health  = get_financial_health_score()
budgets = get_budgets()["budgets"]
alerts  = get_budget_alerts()


# ══════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════
L, C, R = st.columns([1.1, 2.7, 1.2], gap="medium")


# ─── LEFT ───────────────────────────────
with L:
    st.markdown("""
    <div class='brand'>
        <div class='brand-logo'>💰</div>
        <p class='brand-name'>Finance Coach</p>
    </div>
    <p class='brand-sub'>Smart MCP-powered assistant</p>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-label'>This Month</div>", unsafe_allow_html=True)

    sc    = health["score"]
    sc_cl = "#1a936f" if sc>=80 else "#f39c12" if sc>=60 else "#e74c3c"
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-lbl'>🏆 Health Score</div>
        <div class='stat-row'>
            <span class='stat-val'>{sc}<span style='font-size:0.72rem;color:#ccc;font-weight:400'> / 100</span></span>
            <span class='stat-badge' style='color:{sc_cl}'>{health["status"].split()[0]}</span>
        </div>
        <div class='prog-bg'><div class='prog-fill' style='width:{sc}%;background:{sc_cl}'></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-lbl'>💵 Income</div>
        <div class='stat-row'>
            <span class='stat-val'>${summary['total_income']:,.2f}</span>
            <span class='stat-badge' style='color:#1a936f'>+{summary['income_count']} entries</span>
        </div>
        <div class='prog-bg'><div class='prog-fill' style='width:100%;background:#1a936f'></div></div>
    </div>
    """, unsafe_allow_html=True)

    ep = min((summary['total_expenses']/summary['total_income']*100) if summary['total_income']>0 else 0, 100)
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-lbl'>💸 Expenses</div>
        <div class='stat-row'>
            <span class='stat-val'>${summary['total_expenses']:,.2f}</span>
            <span class='stat-badge' style='color:#e74c3c'>{ep:.0f}% of income</span>
        </div>
        <div class='prog-bg'><div class='prog-fill' style='width:{ep}%;background:#e74c3c'></div></div>
    </div>
    """, unsafe_allow_html=True)

    sc2   = "#1a936f" if summary['net_savings']>=0 else "#e74c3c"
    sp    = min(abs(summary['savings_rate']), 100)
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-lbl'>🏦 Net Savings</div>
        <div class='stat-row'>
            <span class='stat-val' style='color:{sc2}'>${summary['net_savings']:,.2f}</span>
            <span class='stat-badge' style='color:{sc2}'>{summary['savings_rate']}% rate</span>
        </div>
        <div class='prog-bg'><div class='prog-fill' style='width:{sp}%;background:{sc2}'></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Analytics Pages</div>", unsafe_allow_html=True)
    st.page_link("pages/1_expenses.py",  label="💸  Expenses")
    st.page_link("pages/2_income.py",    label="💵  Income")
    st.page_link("pages/3_budgets.py",   label="🎯  Budgets")
    st.page_link("pages/4_advice.py",    label="🤖  AI Advice")


# ─── CENTER ─────────────────────────────
with C:
    st.markdown("""
    <div class='chat-header'>
        <div class='chat-av'>🤖</div>
        <div>
            <div class='chat-name'>AI Finance Coach</div>
            <div class='chat-sub'><span class='dot'></span>Online · powered by GPT-4o-mini + MCP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_box = st.container(height=430, border=True)
    with chat_box:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                content = msg["content"].replace("\n","<br>")
                st.markdown(f"""
                <div class='m-ai'>
                    <div class='m-av'>🤖</div>
                    <div>
                        <div class='m-ai-b'>{content}</div>
                        <div class='m-time'>{msg.get('time','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
                if msg.get("tool"):
                    st.markdown(f"""
                    <div class='badges'>
                        <span class='badge-tool'>🔧 {msg['tool'].replace('_',' ').title()}</span>
                        <span class='badge-ok'>✅ Saved</span>
                    </div>""", unsafe_allow_html=True)
            elif msg["role"] == "user":
                st.markdown(f"""
                <div class='m-user'>
                    <div>
                        <div class='m-user-b'>{msg['content']}</div>
                        <div class='m-time-user'>{msg.get('time','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # Chips
    st.markdown("<div class='chip-row'>", unsafe_allow_html=True)
    prompts = {"Expense":"I spent $__ on ","Income":"I earned $__ from ","Budget":"Set $__ monthly budget for ","Summary":"Show my financial summary","Advice":"Give me financial advice"}
    cols = st.columns(5)
    for col, (label, prompt) in zip(cols, prompts.items()):
        with col:
            if st.button(label, key=f"chip_{label}", use_container_width=True):
                st.session_state.prefill = prompt
                st.session_state.ikey  += 1
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Input row
    ic, bc = st.columns([5, 1])
    with ic:
        user_input = st.text_input(
            "chat", value=st.session_state.prefill,
            placeholder="Type a message… e.g. 'I spent $45 on dining'",
            key=f"inp_{st.session_state.ikey}", label_visibility="collapsed"
        )
    with bc:
        send = st.button("Send →", key="send", use_container_width=True, type="primary")

    typed = (user_input or "").strip()
    if send and typed:
        st.session_state.prefill = ""
        st.session_state.messages.append({"role":"user","content":typed,"time":datetime.now().strftime("%I:%M %p"),"tool":None})
        with st.spinner("Thinking..."):
            result = process_message(typed)
        st.session_state.messages.append({"role":"assistant","content":result["reply"],"time":datetime.now().strftime("%I:%M %p"),"tool":result["tool"]})
        st.session_state.ikey += 1
        st.rerun()


# ─── RIGHT ──────────────────────────────
with R:
    # Budget status card
    st.markdown(f"""
    <div class='r-card'>
        <div class='r-card-hdr'>
            <span class='r-card-ttl'>🎯 Budget Status</span>
            <span style='font-size:0.72rem;color:#bbb'>{datetime.now().strftime('%b %Y')}</span>
        </div>
    """, unsafe_allow_html=True)

    if budgets:
        for b in budgets:
            bc    = "#e74c3c" if b["status"]=="over" else "#f39c12" if b["status"]=="warning" else "#1a936f"
            icon  = "🔴" if b["status"]=="over" else "🟡" if b["status"]=="warning" else "🟢"
            pct   = min(b["percent_used"], 100)
            st.markdown(f"""
            <div class='bud-item'>
                <div class='bud-row'>
                    <span class='bud-name'>{icon} {b['category'].title()}</span>
                    <span class='bud-val'>${b['spent']} / ${b['amount']}</span>
                </div>
                <div class='prog-bg'><div class='prog-fill' style='width:{pct}%;background:{bc}'></div></div>
                <div class='bud-sub'>{b['percent_used']}% used · ${b['remaining']} left</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<p style='color:#ccc;font-size:0.8rem;text-align:center;padding:10px 0'>No budgets yet.<br><span style='color:#1a936f'>Try: "Set $300 for groceries"</span></p>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if alerts["count"] > 0:
        for a in alerts["alerts"]:
            if a["status"]=="over": st.error(f"**{a['category'].title()}** exceeded budget!")
            else: st.warning(f"**{a['category'].title()}** at {a['percent_used']}%")

    # Quick Add
    st.markdown("<div class='section-label' style='margin-top:16px'>Quick Add</div>", unsafe_allow_html=True)
    if st.button("➕  New Entry", use_container_width=True, key="fab"):
        st.session_state.show_fab = not st.session_state.show_fab

    if st.session_state.show_fab:
        f1, f2 = st.columns(2)
        with f1:
            if st.button("Expense", use_container_width=True, key="fe"):
                st.session_state.show_exp_modal=True; st.session_state.show_fab=False; st.rerun()
            if st.button("Budget",  use_container_width=True, key="fb"):
                st.session_state.show_bud_modal=True; st.session_state.show_fab=False; st.rerun()
        with f2:
            if st.button("Income",  use_container_width=True, key="fi"):
                st.session_state.show_inc_modal=True; st.session_state.show_fab=False; st.rerun()