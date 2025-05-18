#https://ratpool.streamlit.app/

import streamlit as st
from poolcode import active_pool

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

active_pool = st.selectbox("Select Pool", ["Queen's", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(active_pool)

display_pickem_results(active_pool)
