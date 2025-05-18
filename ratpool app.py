#https://ratpool.streamlit.app/

import streamlit as st
from poolcode import active_pool

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

pool_choice = st.selectbox("Select Pool", ["Queen's", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(pool_choice)

display_pickem_results(pool_choice)
