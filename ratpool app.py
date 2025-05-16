#https://ratpool.streamlit.app/

import streamlit as st
from poolcode import evaluate_pool

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

active_pool = st.selectbox("Select Pool", ["Queen's", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(active_pool)

import streamlit as st
from poolcode import fetch_leaderboard_from_html  # assuming you renamed this properly

st.title("🏆 PGA Championship Prop Pool Leaderboard")

# Pool selector
active_pool = st.selectbox("Select Pool", ["Queens", "Framily"])

# Show button
if st.button("Show Leaderboard"):
    st.write(f"## 📊 {active_pool} Pool Leaderboard")
    
    # Fetch the leaderboard live from ESPN
    df = fetch_leaderboard_from_html("401703511")  # replace with correct event ID

    if df.empty:
        st.error("Could not load leaderboard data. Check event ID or ESPN site structure.")
    else:
        st.dataframe(df)  # Display it in Streamlit table


import streamlit as st
from poolcode import run_pickem_leaderboard, run_prop_bet_leaderboard

# Title
st.title("🏆 PGA Championship 2025 Pool Leaderboard")

# Dropdown to select pool
active_pool = st.selectbox("Select Pool", ["Queens", "Framily"])

# Button to show Pick'em Leaderboard
if st.button("Show Pick'em Leaderboard"):
    run_pickem_leaderboard(active_pool)

# Button to show Prop Bet Leaderboard
if st.button("Show Prop Bet Leaderboard"):
    run_prop_bet_leaderboard(active_pool)

