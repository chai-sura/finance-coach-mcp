"""
Advice Page - Generate and view AI financial advice.
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp_server.tools.advice import get_advice, get_advice_history, get_latest_advice

st.set_page_config(page_title="AI Advice", page_icon="🤖", layout="wide")

st.title("🤖 AI Financial Advice")
st.caption("Get personalized advice powered by OpenAI GPT-4o-mini.")
st.divider()

# GENERATE ADVICE
st.subheader("💡 Generate Fresh Advice")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("Click the button below to analyze your current month's finances and get personalized advice.")

with col2:
    if st.button("🤖 Generate Advice", type="primary", use_container_width=True):
        with st.spinner("Analyzing your finances..."):
            result = get_advice()
            if result["success"]:
                st.success("Advice generated successfully!")
                st.rerun()
            else:
                st.error("Failed to generate advice. Check your OpenAI API key.")

st.divider()

# LATEST ADVICE
st.subheader("📋 Latest Advice")

latest = get_latest_advice()
if latest["success"]:
    st.info(latest["advice"])
    st.caption(f"Generated for {latest['month']}")
else:
    st.warning(latest["message"])

st.divider()

# ADVICE HISTORY
st.subheader("📚 Advice History")

history = get_advice_history()

if history["count"] > 0:
    st.caption(f"{history['count']} advice entries generated so far")

    for i, advice in enumerate(history["history"]):
        with st.expander(f"📅 {advice.get('month', 'Unknown')} — {advice.get('created_at', '')[:10]}"):
            st.write(advice["advice"])
else:
    st.info("📭 No advice history yet — generate your first advice above!")