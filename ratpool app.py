import streamlit as st
from poolcode import evaluate_pool

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

pool = st.selectbox("Select Pool", ["Queen's", "Framily"])

if st.button("Show Leaderboard"):
    evaluate_pool(pool)

import streamlit as st
from poolcode import fetch_leaderboard_from_html  # assuming you renamed this properly

st.title("🏆 PGA Championship Prop Pool Leaderboard")

# Pool selector
pool = st.selectbox("Select Pool", ["Queens", "Framily"])

# Show button
if st.button("Show Leaderboard"):
    st.write(f"## 📊 {pool} Pool Leaderboard")
    
    # Fetch the leaderboard live from ESPN
    df = fetch_leaderboard_from_html("401703511")  # replace with correct event ID

    if df.empty:
        st.error("Could not load leaderboard data. Check event ID or ESPN site structure.")
    else:
        st.dataframe(df)  # Display it in Streamlit table
