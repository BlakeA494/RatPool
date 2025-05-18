#https://ratpool.streamlit.app/

import streamlit as st
from poolcode import participant_picks_all, player_stats, calculate_earnings

st.title("🏌️‍♂️PGA Championship 2025 Pool Leaderboard⛳️")

current_pool = st.radio("Select Pool", ["Queen's", "Framily"])

participant_picks = participant_picks_all[current_pool]

# === Leaderboard ===
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

st.markdown(f"## 🏆 {current_pool} Pool Leaderboard 🏆")

for rank, (name, purse) in enumerate(leaderboard, start=1):
    st.markdown(f"{rank}. **{name}** - ${purse:,.2f}")
    


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


