#https://ratpool.streamlit.app/

import streamlit as st
from poolcode import participant_picks_all, player_stats, calculate_earnings, prop_questions, actual_answers, prop_answers

st.title("🏆 PGA Championship 2025 Pool Leaderboard")

# Dropdown with 4 options
view_option = st.radio("Select View", [
    "Queen's Picks",
    "Queen's Props",
    "Framily Picks",
    "Framily Props"
])

# === Pick'em Results Display ===
def display_pickem_results(pool_name):
    participant_picks = participant_picks_all[pool_name]

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
        st.markdown("---")

    # Leaderboard
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

    st.markdown(f"## 🏆 {pool_name} Pool Leaderboard 🏆")
    for rank, (name, purse) in enumerate(leaderboard, start=1):
        st.markdown(f"{rank}. **{name}** - ${purse:,.2f}")

# === Prop Bets Leaderboard Display ===
def display_prop_results(pool_name):
    st.markdown(f"## 📝 {pool_name} Prop Bet Results")

    st.markdown("### Correct Answers:")
    for i, question in enumerate(prop_questions):
        st.markdown(f"- **{question}**: {actual_answers[i]}")

    st.markdown(f"### 🏆 {pool_name} Prop Bet Leaderboard")

    leaderboard = []
    for participant, guesses in prop_answers[pool_name].items():
        score = 0
        for i, guess in enumerate(guesses):
            guess_str = str(guess).strip().lower()
            actual_str = str(actual_answers[i]).strip().lower()
            if guess_str == actual_str:
                score += 1
        leaderboard.append((participant, score))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, score) in enumerate(leaderboard, 1):
        st.markdown(f"{rank}. **{name}** — {score} correct")

# === Render Selected View ===
if "Picks" in view_option:
    pool_name = "Queen's" if "Queen's" in view_option else "Framily"
    display_pickem_results(pool_name)
else:
    pool_name = "Queen's" if "Queen's" in view_option else "Framily"
    display_prop_results(pool_name)
