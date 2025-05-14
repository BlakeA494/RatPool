import streamlit as st
from 2025 PGA Championship import evaluate_pool

st.title("🏆 Masters 2025 Prop Pool Leaderboard")

pool = st.selectbox("Select Pool", ["Queens", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(pool)

