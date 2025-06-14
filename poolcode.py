import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from collections import defaultdict


###################################################################################################################################################
active_pool = "Framily"
###################################################################################################################################################
def load_pool_data_from_csv(file_path):
    df = pd.read_excel(file_path)

    participant_picks = {}
    prop_answers = {}

    pick_columns = df.columns[2:15].tolist()
    prop_columns = df.columns[15:25].tolist()

    for _, row in df.iterrows():
        name = row["Name:"].strip()

        picks = {}
        for col in pick_columns:
            tier = col.replace(":", "").strip()
            selection = row[col]
            if pd.isnull(selection):
                continue
            if "," in str(selection):
                picks[tier] = [player.strip() for player in str(selection).split(",")]
            else:
                picks[tier] = selection.strip()
        participant_picks[name] = picks

        props = []
        for col in prop_columns:
            props.append(row[col])
        prop_answers[name] = props

    return participant_picks, prop_answers

# Load both pools
framily_picks, framily_props = load_pool_data_from_csv("US Open 2025 Fantasy - Framily.xlsx")
queens_picks, queens_props = load_pool_data_from_csv("US Open 2025 Fantasy - Queens.xlsx")

# Now build your structures as usual
participant_picks_all = {
    "Framily": framily_picks,
    "Queen's": queens_picks
}

prop_answers = {
    "Framily": framily_props,
    "Queen's": queens_props
}


# === Fetch live leaderboard data from ESPN ===
def fetch_leaderboard_from_html(event_id="401703515"): #<-CHANGE THE TOURNAMENT ID BASED OFF ESPN WEBSITE***
###################################################################################################################################################
    url = f"https://www.espn.com/golf/leaderboard?tournamentId={event_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')
    if len(tables) < 1:
        print("Could not find the main leaderboard table.")
        return pd.DataFrame()
    
    # Find the leaderboard table (the first table) IF THERE IS A TIE/PLAYOFF #######################################################
    leaderboard_table = tables[0]

    # Extract headers
    headers = [th.text.strip() for th in leaderboard_table.find_all('th')]

    # Extract rows
    rows = []
    for row in leaderboard_table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) == len(headers):
            rows.append([col.text.strip() for col in cols])

    df = pd.DataFrame(rows, columns=headers)
    return df

# Function to format score
def format_score(score):
    if score == "E":
        return "0"
    if score.startswith('+'):
        return score[1:]  # Remove the plus sign for positive numbers
    return score

# Function to clean up position (remove 'T')
def format_position(position):
    return position.lstrip('T')

def get_live_player_stats():
    df = fetch_leaderboard_from_html()

    player_stats_live = {}
    if 'TEE TIME' in df.columns:
        for _, row in df.iterrows():
            player_name = row['PLAYER']
            tee_time = row['TEE TIME']
            player_stats_live[player_name] = [tee_time, ""]
    elif 'SCORE' in df.columns:
        for _, row in df.iterrows():
            player_name = row['PLAYER']
            score = format_score(row['SCORE'])
            pos = format_position(row['POS'])
            player_stats_live[player_name] = [score, pos]
    else:
        print("Unexpected leaderboard structure.")

    return player_stats_live

# === Update pool player stats with live leaderboard data ===
def get_updated_player_stats(participant_picks_all, active_pool):
    player_stats_live = get_live_player_stats()

    updated_player_stats = defaultdict(dict)

    for participant, picks in participant_picks_all[active_pool].items():
        for tier, pick in picks.items():
            updated_player_stats[participant][tier] = {
                pick: player_stats_live.get(pick, ["N/A", "N/A"])
            }
return updated_player_stats

for player, (score_str, pos_str) in player_stats_live.items():
    # Convert score to integer; treat "E" (even) as 0
    try:
        score = int(score_str)
    except ValueError:
        score = 0  # Handles "E" or any other non-integer string

    # Handle position
    if pos_str in ["CUT", "WD"]:
        position = pos_str
    else:
        try:
            position = int(pos_str.replace('T', ''))
        except ValueError:
            position = 999

    player_stats[player] = [score, position]

# === Purse Payouts ===============================================================================================================================
Payout = [
  3420000, 2052000, 1292000, 912000, 760000, 683880, 640220, 598270, 558140, 519830,
  483360, 448700, 415870, 384860, 355680, 328320, 302780, 279070, 257180, 237120,
  218880, 202460, 187870, 176010, 164610, 153670, 143180, 133150, 123570, 114450,
  107160, 100770, 95300, 90740, 87100, 83630, 80260, 76970, 73780, 70680,
  67670, 64750, 61920, 59190, 56540, 53990, 51530, 49160, 46880, 44690,
  42590, 40580, 38670, 36840, 35110, 33470, 31920, 30640, 29550, 28640,
  27910, 27380, 26920, 26490, 26080, 25680, 25290, 24920, 24570, 24240,
  23940, 23740, 23570, 23420
]

# === Cut Line Threshold (Assuming 50th Place) ===
CUT_LINE_POSITION = 60 #<-MAYBE CHECK THIS VALUE depending on ties ################################################################################

# === Purse Calculation with Tie Handling ===
position_groups = defaultdict(list)
for player, (_, pos) in player_stats.items():
    position_groups[pos].append(player)

def calculate_earnings(position):
    if position > CUT_LINE_POSITION:
        return 0  # Player missed the cut, earns nothing
    
    tied_players = position_groups[position]
    num_tied = len(tied_players)
    if num_tied > 1:
        total_payout = sum(Payout[position - 1 + i] for i in range(num_tied) if position - 1 + i < len(Payout))
        return total_payout / num_tied
    else:
        return Payout[position - 1] if position - 1 < len(Payout) else 0

# === Score Display + Leaderboard ===
participant_picks = participant_picks_all[active_pool]

print("Each Participant's picks and their player's score, position, and purse winnings:")

for name, picks in participant_picks.items():
    print(f"\t{name}'s Picks and Earnings:")
    total_purse = 0
    for tier, selection in picks.items():
        players = selection if isinstance(selection, list) else [selection]
        for player in players:
            if player in player_stats:
                score, pos = player_stats[player]
                purse = calculate_earnings(pos)
                total_purse += purse
                print(f"  \t\t{player}: Score = {score}, Pos = {pos}, Purse = ${purse:,.2f}")
    print(f"\tTotal Purse for {name}: ${total_purse:,.2f}\n")

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

print(f"\n🏆 {active_pool} Pool Leaderboard 🏆")
for rank, (name, purse) in enumerate(leaderboard, start=1):
    print(f"{rank}. {name} - ${purse:,.2f}")



prop_questions = [
    "How many LIV players (of 14) will make the cut?",
    "How many Canadian players (of 4) will make the cut?🇨🇦",
    "How many LIV players (of 14) will be in top 20 and ties?",
    "Will there be a hole-in-one this week?",
    "What score (to par) will be the cutline?",
    "What will the winning score (to par) be after all 4 days?",
    "How large of a win margin will it be?",
    "Will it be the winner's first U.S. OPEN win?",
    "Which Ryder/President's cup team will the winner belong to?",
    "Who will be the 2025 U.S. Open Champion?🏆"
]

# Actual answers for scoring
actual_answers = [
    6,          #LIV players to make the cut
    4,          #Canadian players to make the cut
    3,          #LIV players in top 20 and ties
    "YES",       #Will there be a hole-in-one
    6,          #What is the cutline
    -3,       #Winning score to par
    1,          #Margin of victory
    "YES, first time U.S. Open winner",       #First major?
    "USA🇺🇸",       #Ryder/President's cup team
    "Sam Burns"   #Champion
]

def evaluate_pool(pool_name):
    print("\nCorrect Answers:")
    for i, question in enumerate(prop_questions):
        print(f"- {question}: {actual_answers[i]}")

    print(f"\n🏆 {pool_name} Pool Leaderboard 🏆")
    leaderboard = []
    for participant, guesses in prop_answers[pool_name].items():
        score = 0
        for i, guess in enumerate(guesses):
            # Standardize both for comparison
            guess_str = str(guess).strip().lower()
            actual_str = str(actual_answers[i]).strip().lower()
            if guess_str == actual_str:
                score += 1
        leaderboard.append((participant, score))

    leaderboard.sort(key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(leaderboard, 1):
        print(f"{rank}. {name} - {score} correct")

evaluate_pool(active_pool)
