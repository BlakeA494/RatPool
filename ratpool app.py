import streamlit as st
from poolcode import evaluate_pool

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

pool = st.selectbox("Select Pool", ["Queen's", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(pool)

