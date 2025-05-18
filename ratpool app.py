#https://ratpool.streamlit.app/
import streamlit as st
from poolcode import (
    participant_picks_all,
    player_stats,
    calculate_earnings,
    prop_questions,
    actual_answers,
    prop_answers
)

# App title
st.title("🏌️‍♂️PGA Championship 2025 Pool Leaderboard⛳️")

# Pool selector
current_pool = st.selectbox("Select Pool", ["Queen's", "Framily"])

# View toggle
view_option = st.radio("Select View", ["Pickem Leaderboard", "Prop Bets Leaderboard"])

# === Pickem Leaderboard View ===
if view_option == "Pickem Leaderboard":
    participant_picks = participant_picks_all[current_pool]
    
    st.markdown("## Each Participant's Picks and Earnings")
    
    for name, picks in participant_picks.items():
        st.markdown(f"### {name}'s Picks and Earnings:")
        total_purse = 0
        for tier, selection in picks.items():
            players = selection if isinstance(selection, list) else [selection]
            for player in players:
                if player in player_stats:
                    score, pos = player_stats[player]
                    purse = calculate_earnings(pos)
                    total_purse += purse
                    st.markdown(f"- **{player}**: Score = {score}, Pos = {pos}, Purse = ${purse:,.2f}")
        st.markdown(f"**Total Purse for {name}: ${total_purse:,.2f}**\n")

    # Build leaderboard
    leaderboard = []
    for name, picks in participant_picks.items():
        total_purse = 0
        for tier, selection in picks.items():
            players = selection if isinstance(selection, list) else [selection]
            for player in players:
                if player in player_stats:
                    _, pos = player_stats[player]
                    total_purse += calculate_earnings(pos)
        leaderboard.append((name, total_purse))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    st.markdown(f"## 🏆 {current_pool} Pickem Leaderboard 🏆")
    for rank, (name, purse) in enumerate(leaderboard, start=1):
        st.markdown(f"{rank}. **{name}** - ${purse:,.2f}")

# === Prop Bets Leaderboard View ===
elif view_option == "Prop Bets Leaderboard":
    st.markdown("## Correct Answers:")
    for i, question in enumerate(prop_questions):
        st.markdown(f"- {question}: **{actual_answers[i]}**")

    st.markdown(f"## 🏆 {current_pool} Prop Bets Leaderboard 🏆")
    leaderboard = []
    for participant, guesses in prop_answers[current_pool].items():
        score = 0
        for i, guess in enumerate(guesses):
            guess_str = str(guess).strip().lower()
            actual_str = str(actual_answers[i]).strip().lower()
            if guess_str == actual_str:
                score += 1
        leaderboard.append((participant, score))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, score) in enumerate(leaderboard, 1):
        st.markdown(f"{rank}. **{name}** - {score} correct")
