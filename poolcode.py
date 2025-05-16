import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict

#https://ratpool.streamlit.app/
###################################################################################################################################################
#In between these lines is everything that must be changed year-year

# === CONFIG: TOGGLE BETWEEN POOLS HERE ===
active_pool = "Framily"  # Change to "Queen's", or "Framily" as needed

# === All participant picks across both pools ===
participant_picks_all = {
    "Framily": {
        "Blake": {"Tier 1": "Rory McIlroy", "Tier 2": "Ludvig Åberg", "Tier 3": "Brooks Koepka", "Tier 4": "Shane Lowry", "Tier 5": "Sepp Straka", "Tier 6": "Tony Finau",
                  "Tier 7": "Patrick Reed", "Tier 8": "Adam Scott", "Tier 9": "Taylor Pendrith", "Tier 10": ["Lucas Glover", "Si Woo Kim"], "Top Amateur/CFT": "Tyler Collet"
        },
        "Bill": {"Tier 1": "Rory McIlroy", "Tier 2": "Justin Thomas", "Tier 3": "Jon Rahm", "Tier 4": "Jordan Spieth", "Tier 5": "Jason Day", "Tier 6": "Tony Finau",
                  "Tier 7": "Patrick Reed", "Tier 8": "Dustin Johnson", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Rickie Fowler", "Sergio Garcia"], "Top Amateur/CFT": "Bobby Gates"
        },
        "Barry": {"Tier 1": "Rory McIlroy", "Tier 2": "Ludvig Åberg", "Tier 3": "Jon Rahm", "Tier 4": "Shane Lowry", "Tier 5": "Min Woo Lee", "Tier 6": "Wydham Clark",
                  "Tier 7": "Sahith Theegala", "Tier 8": "Matt Fitzpatrick", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Sam Burns", "Rickie Fowler"], "Top Amateur/CFT": "Brian Bergstol"
        },
        "Zach": {"Tier 1": "Scottie Scheffler", "Tier 2": "Ludvig Åberg", "Tier 3": "Jon Rahm", "Tier 4": "Corey Conners", "Tier 5": "Sepp Straka", "Tier 6": "Will Zalatoris",
                  "Tier 7": "Patrick Reed", "Tier 8": "Dustin Johnson", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Si Woo Kim", "Keegan Bradley"], "Top Amateur/CFT": "Ryan Lenahan"
        },
        "Graydon": {"Tier 1": "Scottie Scheffler", "Tier 2": "Ludvig Åberg", "Tier 3": "Hideki Matsuyama", "Tier 4": "Viktor Hovland", "Tier 5": "Min Woo Lee", "Tier 6": "Russell Henley",
                  "Tier 7": "Max Homa", "Tier 8": "Akshay Bhatia", "Tier 9": "Nick Taylor", "Tier 10": ["Lucas Glover", "Robert Macintyre"], "Top Amateur/CFT": "Justin Hicks"
        },
        "Shane": {"Tier 1": "Rory McIlroy", "Tier 2": "Bryson DeChambeau", "Tier 3": "Jon Rahm", "Tier 4": "Jordan Spieth", "Tier 5": "Min Woo Lee", "Tier 6": "Tony Finau",
                  "Tier 7": "Cameron Smith", "Tier 8": "Adam Scott", "Tier 9": "Nick Taylor", "Tier 10": ["Cameron Davis", "Keegan Bradley"], "Top Amateur/CFT": "Jesse Droemer"
        },
        "Brandon": {"Tier 1": "Scottie Scheffler", "Tier 2": "Xander Schauffele", "Tier 3": "Brooks Koepka", "Tier 4": "Shane Lowry", "Tier 5": "Min Woo Lee", "Tier 6": "Will Zalatoris",
                  "Tier 7": "Max Homa", "Tier 8": "Adam Scott", "Tier 9": "Nick Taylor", "Tier 10": ["Rickie Fowler", "Keegan Bradley"], "Top Amateur/CFT": "Dylan Newman"
        },
        "Jamie": {"Tier 1": "Scottie Scheffler", "Tier 2": "Justin Thomas", "Tier 3": "Brooks Koepka", "Tier 4": "Viktor Hovland", "Tier 5": "Justin Rose", "Tier 6": "Will Zalatoris",
                  "Tier 7": "Patrick Reed", "Tier 8": "Dustin Johnson", "Tier 9": "Adam Hadwin", "Tier 10": ["Rickie Fowler", "Sergio Garcia"], "Top Amateur/CFT": "Tyler Collet"
        }
    },
    "Queen's": {
        "Blake": {"Tier 1": "Rory McIlroy", "Tier 2": "Ludvig Åberg", "Tier 3": "Brooks Koepka", "Tier 4": "Jordan Spieth", "Tier 5": "Jason Day", "Tier 6": "Russell Henley",
                  "Tier 7": "Sahith Theegala", "Tier 8": "Adam Scott", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Rickie Fowler", "Si Woo Kim"], "Top Amateur/CFT": "Tyler Collet"
        },
        "Zain": {"Tier 1": "Scottie Scheffler", "Tier 2": "Bryson DeChambeau", "Tier 3": "Hideki Matsuyama", "Tier 4": "Tommy Fleetwood", "Tier 5": "Min Woo Lee", "Tier 6": "Tony Finau",
                  "Tier 7": "Max Homa", "Tier 8": "Akshay Bhatia", "Tier 9": "Nick Taylor", "Tier 10": ["Cameron Young", "Rickie Fowler"], "Top Amateur/CFT": "Michael Block"
        },
        "Cam": {"Tier 1": "Rory McIlroy", "Tier 2": "Ludvig Åberg", "Tier 3": "Joaquin Niemann", "Tier 4": "Corey Conners", "Tier 5": "Min Woo Lee", "Tier 6": "Wyndham Clark",
                  "Tier 7": "Cameron Smith", "Tier 8": "Akshay Bhatia", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Aaron Rai", "Phil Mickelson"], "Top Amateur/CFT": "Michael Block"
        },
        "Dylan": {"Tier 1": "Scottie Scheffler", "Tier 2": "Bryson DeChambeau", "Tier 3": "Hideki Matsuyama", "Tier 4": "Jordan Spieth", "Tier 5": "Justin Rose", "Tier 6": "Russell Henley",
                  "Tier 7": "Patrick Reed", "Tier 8": "Matt Fitzpatrick", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Sam Burns", "Keegan Bradley"], "Top Amateur/CFT": "Greg Koch"
        },
        "McBurney": {"Tier 1": "Rory McIlroy", "Tier 2": "Justin Thomas", "Tier 3": "Brooks Koepka", "Tier 4": "Jordan Spieth", "Tier 5": "Min Woo Lee", "Tier 6": "Will Zalatoris",
                  "Tier 7": "Patrick Reed", "Tier 8": "Akshay Bhatia", "Tier 9": "Taylor Pendrith", "Tier 10": ["Byeong-Hun An", "Sam Burns"], "Top Amateur/CFT": "Michael Block"
        },
        "Karyn": {"Tier 1": "Rory McIlroy", "Tier 2": "Ludvig Åberg", "Tier 3": "Hideki Matsuyama", "Tier 4": "Corey Conners", "Tier 5": "Justin Rose", "Tier 6": "Tom Kim",
                  "Tier 7": "Max Homa", "Tier 8": "Matt Fitzpatrick", "Tier 9": "Nick Taylor", "Tier 10": ["Rickie Fowler", "Sam Burns"], "Top Amateur/CFT": "Michael Block"
        },
        "Sean": {"Tier 1": "Scottie Scheffler", "Tier 2": "Justin Thomas", "Tier 3": "Hideki Matsuyama", "Tier 4": "Shane Lowry", "Tier 5": "Sepp Straka", "Tier 6": "Tom Kim",
                  "Tier 7": "Sahith Theegala", "Tier 8": "Akshay Bhatia", "Tier 9": "Adam Hadwin", "Tier 10": ["Nicolai Højgaard", "Rasmus Højgaard"], "Top Amateur/CFT": "Larkin Gross"
        },
        "Shivam": {"Tier 1": "Rory McIlroy", "Tier 2": "Justin Thomas", "Tier 3": "Hideki Matsuyama", "Tier 4": "Corey Conners", "Tier 5": "Justin Rose", "Tier 6": "Will Zalatoris",
                  "Tier 7": "Sahith Theegala", "Tier 8": "Akshay Bhatia", "Tier 9": "Mackenzie Hughes", "Tier 10": ["Austin Eckroat", "Cameron Young"], "Top Amateur/CFT": "Rupe Taylor"
        }
    }
}

# === Fetch live leaderboard data from ESPN ===
def fetch_leaderboard_from_html(event_id="401703511"): #<-CHANGE THE TOURNAMENT ID BASED OFF ESPN WEBSITE***
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

# Example usage: Fetch live leaderboard data
df = fetch_leaderboard_from_html()

# Parse the necessary columns for player names, scores, and positions
player_stats_live = {}
for index, row in df.iterrows():
    player_name = row['PLAYER']
    score = row['SCORE']
    position = row['POS']

    # Format the score and position before storing
    formatted_score = format_score(score)
    formatted_position = format_position(position)

    # Store the player's stats in the dictionary
    player_stats_live[player_name] = [formatted_score, formatted_position]

# === Update pool player stats with live leaderboard data ===
updated_player_stats = defaultdict(dict)

for participant, picks in participant_picks_all[active_pool].items():
    for tier, pick in picks.items():
        if isinstance(pick, list):  # Multi-player picks
            updated_player_stats[participant][tier] = {
                player: player_stats_live.get(player, ["N/A", "N/A"]) for player in pick
            }
        else:  # Single-player picks
            updated_player_stats[participant][tier] = {
                pick: player_stats_live.get(pick, ["N/A", "N/A"])
            }
player_stats = {}

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
    3600000, 2160000, 1360000, 960000, 800000, 714000, 668000, 624000, 582000, 543000, 
    504000, 468000, 434000, 401000, 371000, 343000, 316000, 291000, 268000, 247000, 
    228000, 211000, 196000, 181000, 167000, 153000, 147000, 141000, 135000, 130000, 
    124000, 119000, 114000, 109000, 104000, 100000, 95000, 91000, 87000, 83000, 
    79000, 75000, 71000, 68000, 64000, 60000, 56000, 53000, 51000, 49000, 
    47000, 46000, 45000, 44000, 43000, 42000, 41000, 40000, 39000, 38000, 
    37000, 36000, 35000, 34000, 33000, 32000, 31000, 30000, 29000, 28000
]

# === Cut Line Threshold (Assuming 50th Place) ===
CUT_LINE_POSITION = 70 #<-MAYBE CHECK THIS VALUE depending on ties ################################################################################

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

#####################def run_pickem_leaderboard(active_pool):
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

################################################################################################################################

#current_pool = "Framily" 

prop_questions = [
    "How many LIV players will make the cut?",
    "How many Canadian players will make the cut?",
    "How many LIV players will be in the top 15 and ties?",
    "Will there be a hole-in-one this week?",
    "What will the cutline be?",
    "What will be the winning score to par after all 4 days?",
    "How large of a win margin will it be?",
    "Will this be the winner's first major?",
    "Who will win the 2025 PGA Championship?"
]

# Actual answers for scoring
actual_answers = [
    5,          #LIV players to make the cut
    1,          #Canadian players to make the cut
    1,          #LIV players in top 15 and ties
    "Yes",       #Will there be a hole-in-one
    1,          #What is the cutline
    "-5",       #Winning score to par
    1,          #Margin of victory
    "Yes",       #First major?
    "Davis & Gerard"    #Champion
]

# Participants' answers (compact format)
prop_answers = {
    "Queen's": {
        "Blake":   [6, 3, 3, "No", 3, -13, 2, "No", "Spieth"],
        "Zain":    [5, 3, 3, "Yes", -1, -8, 1, "Yes", "Fleetwood"],
        "Cam":     [9, 3, 4, "No", 1, -16, 1, "No", "McIlroy"],
        "Dylan":   [7, 2, 4, "No", -2, -11, 2, "No", "Scheffler"],
        "McBurney":[6, 2, 3, "No", 6, -5, 2, "No", "McIlroy"],
        "Karyn":   [8, 2, 2, "No", 3, -13, 2, "No", "McIlroy"],
        "Sean":    [4, 1, 2, "Yes", -2, -10, 2, "No", "Scheffler"],
        "Shivam":  [4, 3, 1, "Yes", 3, -14, 2, "No", "Thomas"]
    },
    "Framily": {
        "Blake":   [6, 2, 3, "No", 3, -13, 2, "No", "Morikawa"],
        "Bill":    [4, 2, 3, "No", 3, -10, 2, "No", "McIlroy"],
        "Barry":   [10, 3, 3, "Yes", 5, -10, 2, "No", "McIlroy"],
        "Zach":    [8, 3, 2, "Yes", 3, -13, 1, "No", "Åberg"],
        "Graydon": [9, 3, 3, "No", 0, -19, 2, "No", "Scheffler"],
        "Shane":   [8, 2, 3, "No", 2, -12, 2, "No", "McIlroy"],
        "Brandon": [9, 3, 3, "No", 4, -13, 2, "No", "Koepka"],
        "Jamie":   [9, 3, 5, "No", 2, -17, 2, "No", "Scheffler"]
    }
}

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

evaluate_pool(active_pool) #(current_pool)

