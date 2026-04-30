import os 
import pandas as pd 
from pathlib import Path
import numpy as np


Base_Dir = Path(__file__).resolve().parents[1] # One level above the current absolute file directory.

df_train = pd.read_csv(rf'{Base_Dir}/ML/train/train.csv')
df_test = pd.read_csv(rf'{Base_Dir}/ML/test/test.csv')

def load_elo_file(path: str) -> pd.DataFrame:
    df_elo = pd.read_csv(path)

    rename_map = {}
    if 'from' in df_elo.columns:
        rename_map['from'] = 'From'
    if 'elo' in df_elo.columns:
        rename_map['elo'] = 'Elo'
    if 'to' in df_elo.columns:
        rename_map['to'] = 'To'
    if 'team' in df_elo.columns:
        rename_map['team'] = 'Club'
    if 'rank' in df_elo.columns:
        rename_map['rank'] = 'Rank'
    if 'country' in df_elo.columns:
        rename_map['country'] = 'Country'
    if 'level' in df_elo.columns:
        rename_map['level'] = 'Level'

    df_elo = df_elo.rename(columns=rename_map)

    required_cols = ['From', 'Elo']
    missing = [col for col in required_cols if col not in df_elo.columns]
    if missing:
        raise ValueError(f"Missing columns {missing} in {path}. Found: {df_elo.columns.tolist()}")

    df_elo['From'] = pd.to_datetime(df_elo['From'])
    return df_elo.sort_values('From').reset_index(drop=True)


Elo_team_names = sorted(os.listdir(f'{Base_Dir}/ClubElo_Data'))

df_train['home_team'].replace({'Parma Calcio 1913': 'Parma',
    'AC Milan': 'Milan',
    'AC Carpi': 'Carpi'},inplace=True)
df_test['home_team'].replace({'Parma Calcio 1913': 'Parma',
    'AC Milan': 'Milan',
    'AC Carpi': 'Carpi'},inplace=True)

df_train['away_team'].replace({'Parma Calcio 1913': 'Parma',
    'AC Milan': 'Milan',
    'AC Carpi': 'Carpi'},inplace=True)
df_test['away_team'].replace({'Parma Calcio 1913': 'Parma',
    'AC Milan': 'Milan',
    'AC Carpi': 'Carpi'},inplace=True)

# 1) Result Column FE
df_train['result'] = np.where(df_train['home_score']>df_train['away_score'],'H',
                        np.where(df_train['home_score']==df_train['away_score'],'D','A'))


# print(df_train.head(20))

# 2) home elo, away elo, and elo diffs FE 
home_elo_scores = []
away_elo_scores = []
elo_diffs = []

for index,row in df_train.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']

    date = row['date']
    date_str = date
    date = pd.to_datetime(date)

    home_elo_path = rf'{Base_Dir}/ClubElo_Data/{home_team}.csv'
    away_elo_path = rf'{Base_Dir}/ClubElo_Data/{away_team}.csv'

    df_home_elo = load_elo_file(home_elo_path)
    df_away_elo = load_elo_file(away_elo_path)

    home_elo_score = np.round(df_home_elo[df_home_elo['From'] <= date].iloc[-1]['Elo'], 2)
    away_elo_score = np.round(df_away_elo[df_away_elo['From'] <= date].iloc[-1]['Elo'], 2)

    elo_diff = np.round((home_elo_score - away_elo_score),2)

    home_elo_scores.append(home_elo_score)
    away_elo_scores.append(away_elo_score)
    elo_diffs.append(elo_diff)


df_train['home_elo'] = home_elo_scores
df_train['away_elo'] = away_elo_scores
df_train['elo_diff'] = elo_diffs 

df_train.to_csv(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/f4_features_engineered.csv')

# print(df_train.columns)
# print(len(df_train))


# 3) Points' features FE
# Load the feature-engineered dataset
df = pd.read_csv(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/f4_features_engineered.csv')

# Create home points gained (hpg)
# 3 points for win, 1 for draw, 0 for loss
df['hpg'] = np.where(df['result']=='H',3,
                        np.where(df['result']=='D',1,0))

# Create away points gained (apg)
df['apg'] = np.where(df['result']=='A',3,
                        np.where(df['result']=='D',1,0))

# Get unique seasons
seasons = df['season'].unique()

# Preview data
print(df.head())

# Loop through each season separately
for season in seasons:
    # Filter data for the current season
    df_s = df[df['season']==season]
    print(f'{season}')

    # Initialize lists to store features
    # hpl5_home → last 5 home matches points (home only)
    # apl5_away → last 5 away matches points (away only)
    # hpl5 → last 5 overall matches points (home + away)
    # apl5 → last 5 overall matches points (home + away)
    hpl5_home = []
    apl5_away = []
    hpl5 = []
    apl5 = []
    
    print(df_s.head())

    # Iterate through each match (row-wise)
    for index,rows in df_s.iterrows():
        # Extract match info
        home_team = rows['home_team']
        away_team = rows['away_team']
        date = pd.to_datetime(rows['date'])

        print(type(date))

        # -----------------------------
        # HOME TEAM - LAST 5 HOME MATCHES
        # -----------------------------
        df_home_team = df_s[df_s['home_team']==home_team]
        df_home_team = df_home_team[pd.to_datetime(df_home_team['date'])<date]

        # Sum of last 5 home matches (home perspective only)
        hpl5_home.append(np.sum(df_home_team['hpg'][-5:]))

        # -----------------------------
        # AWAY TEAM - LAST 5 AWAY MATCHES
        # -----------------------------
        df_away_team = df_s[df_s['away_team']==away_team]
        df_away_team = df_away_team[pd.to_datetime(df_away_team['date'])<date]

        # Sum of last 5 away matches (away perspective only)
        apl5_away.append(np.sum(df_away_team['apg'][-5:]))

        # -----------------------------
        # HOME TEAM - LAST 5 OVERALL MATCHES
        # (both home and away)
        # -----------------------------
        df_home_team_last5 = df_s.loc[
        ((df_s['home_team'] == home_team) | (df_s['away_team'] == home_team)) &
        (pd.to_datetime(df_s['date']) < date)
        ].sort_values('date').tail(5)

        # -----------------------------
        # AWAY TEAM - LAST 5 OVERALL MATCHES
        # -----------------------------
        df_away_team_last5 = df_s.loc[
        ((df_s['home_team'] == away_team) | (df_s['away_team'] == away_team)) &
        (pd.to_datetime(df_s['date']) < date)
        ].sort_values('date').tail(5)

        # Calculate total points for home team from last 5 matches
        temp = 0
        for index,row in df_home_team_last5.iterrows():
            if row['home_team'] == home_team:
                temp += row['hpg']   # home match → use hpg
            else:
                temp += row['apg']   # away match → use apg

        hpl5.append(temp)

        # Calculate total points for away team from last 5 matches
        temp = 0
        for index,row in df_home_team_last5.iterrows():
            if row['home_team'] == away_team:
                temp += row['hpg']
            else:
                temp += row['apg']

        apl5.append(temp)

    # Assign computed features back to seasonal dataframe
    df_s['hpl5'] = hpl5
    df_s['apl5'] = apl5
    df_s['hpl5_home'] = hpl5_home
    df_s['apl5_away'] = apl5_away 

    # Ensure directory exists for saving season-wise outputs
    os.makedirs(f'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons/',exist_ok=True)

    # Save season-wise feature file
    df_s.to_csv(f'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons/{season}_hpl5_apl5.csv',index=False)

# Directory containing all season-wise files
hpl5_apl5_dir = rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons'

# Combine all season files into one dataframe
ls = []
for file in os.listdir(hpl5_apl5_dir):
    df = pd.read_csv(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons/{file}')   # read each file
    ls.append(df)

# Concatenate all season data
df = pd.concat(ls,ignore_index=True)

df.drop(columns = ['Unnamed: 0'],inplace = True)

# Save final combined dataset
df.to_csv(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Combined_apl5_hpl5_home_away.csv')


    
# 4) Last 5 matches detailed stats FE (wins/draws/losses/goals/cards)
os.makedirs(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons_Final',exist_ok=True)
df = pd.read_csv(rf'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Combined_apl5_hpl5_home_away.csv')

seasons = df['season'].unique()

for season in seasons:
    df_s = df[df['season']==season]

    home_wins_last_5 = []
    home_draws_last_5 = []
    home_losses_last_5 = []

    away_wins_last_5 = []
    away_draws_last_5 = []
    away_losses_last_5 = []

    home_goals_scored_last_5 = []
    home_goals_conceded_last_5 = []

    away_goals_scored_last_5 = []
    away_goals_conceded_last_5 = []

    home_yellows_last_5 = []
    away_yellows_last_5 = []

    home_reds_last_5 = []
    away_reds_last_5 = []

    for index, rows in df_s.iterrows():
        home_team = rows['home_team']
        away_team = rows['away_team']
        date = pd.to_datetime(rows['date'])

        # ---------------- HOME TEAM LAST 5 ----------------
        df_home_last5 = df_s.loc[
            ((df_s['home_team'] == home_team) | (df_s['away_team'] == home_team)) &
            (pd.to_datetime(df_s['date']) < date)
        ].sort_values('date').tail(5)

        w = d = l = 0
        gs = gc = 0
        yc = rc = 0

        for i, row in df_home_last5.iterrows():
            if row['home_team'] == home_team:
                gs += row['home_score']
                gc += row['away_score']
                yc += row['home_yellow_cards']
                rc += row['home_red_cards']

                if row['result'] == 'H':
                    w += 1
                elif row['result'] == 'D':
                    d += 1
                else:
                    l += 1
            else:
                gs += row['away_score']
                gc += row['home_score']
                yc += row['away_yellow_cards']
                rc += row['away_red_cards']

                if row['result'] == 'A':
                    w += 1
                elif row['result'] == 'D':
                    d += 1
                else:
                    l += 1

        home_wins_last_5.append(w)
        home_draws_last_5.append(d)
        home_losses_last_5.append(l)
        home_goals_scored_last_5.append(gs)
        home_goals_conceded_last_5.append(gc)
        home_yellows_last_5.append(yc)
        home_reds_last_5.append(rc)

        # ---------------- AWAY TEAM LAST 5 ----------------
        df_away_last5 = df_s.loc[
            ((df_s['home_team'] == away_team) | (df_s['away_team'] == away_team)) &
            (pd.to_datetime(df_s['date']) < date)
        ].sort_values('date').tail(5)

        w = d = l = 0
        gs = gc = 0
        yc = rc = 0

        for i, row in df_away_last5.iterrows():
            if row['home_team'] == away_team:
                gs += row['home_score']
                gc += row['away_score']
                yc += row['home_yellow_cards']
                rc += row['home_red_cards']

                if row['result'] == 'H':
                    w += 1
                elif row['result'] == 'D':
                    d += 1
                else:
                    l += 1
            else:
                gs += row['away_score']
                gc += row['home_score']
                yc += row['away_yellow_cards']
                rc += row['away_red_cards']

                if row['result'] == 'A':
                    w += 1
                elif row['result'] == 'D':
                    d += 1
                else:
                    l += 1

        away_wins_last_5.append(w)
        away_draws_last_5.append(d)
        away_losses_last_5.append(l)
        away_goals_scored_last_5.append(gs)
        away_goals_conceded_last_5.append(gc)
        away_yellows_last_5.append(yc)
        away_reds_last_5.append(rc)

    df_s['home_wins_last_5'] = home_wins_last_5
    df_s['home_draws_last_5'] = home_draws_last_5
    df_s['home_losses_last_5'] = home_losses_last_5

    df_s['away_wins_last_5'] = away_wins_last_5
    df_s['away_draws_last_5'] = away_draws_last_5
    df_s['away_losses_last_5'] = away_losses_last_5

    df_s['home_goals_scored_last_5'] = home_goals_scored_last_5
    df_s['home_goals_conceded_last_5'] = home_goals_conceded_last_5

    df_s['away_goals_scored_last_5'] = away_goals_scored_last_5
    df_s['away_goals_conceded_last_5'] = away_goals_conceded_last_5

    df_s['home_yellows_last_5'] = home_yellows_last_5
    df_s['away_yellows_last_5'] = away_yellows_last_5

    df_s['home_reds_last_5'] = home_reds_last_5
    df_s['away_reds_last_5'] = away_reds_last_5

    df_s.to_csv(f'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons_Final/{season}_full_last5_stats.csv', index=False)

# Combine again
final_ls = []
for file in os.listdir(f'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons_Final'):
    df_temp = pd.read_csv(f'{Base_Dir}/5)Preprocess_FeatureEngineer_Train_Test/Seasons_Final/{file}')
    final_ls.append(df_temp)

df_final = pd.concat(final_ls, ignore_index=True)

print(df_final.columns)

df_final.to_csv(rf'{Base_Dir}/ML/FINAL_FEATURES_TRAIN.csv', index=False)














        

        
    

    

    

    
    
    

    

    





