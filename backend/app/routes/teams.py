import pandas as pd 
from fastapi import APIRouter 
from pathlib import Path

# Initialize the directory of the dataset to load it and store it as a pandas df object.
BASE_DIR = Path(__file__).resolve().parents[3]
file_path = BASE_DIR/ "ML" / "FINAL_FEATURES_TRAIN_ENRICHED.csv"
df = pd.read_csv(rf"{file_path}")
temp_df = df[df['season']!=2526]

router = APIRouter(
    tags = ["teams"]
)


@router.get("/seasons/{season}/teams")
def return_teams_for_season(season:int):    
    t_df = temp_df[temp_df['season']==season]
    teams_list = t_df['home_team'].unique()
    return {"teams":teams_list.tolist()} # -> {"teams":[AC Milan, Inter, Juventus, Napoli, Roma, Lazio, Fiorentina, Atalanta,...]}

@router.get("/seasons/{season}/teams/standings")
def return_standings(season: int):
    t_df = temp_df[temp_df['season']==season]
    columns = ['total_points','team_name','matches_played','points_per_match','wins','draws','losses','avg_xg','goal_difference','goals_scored']
    teams_list = t_df['home_team'].unique()
    d = {}
    for col in columns:
        d[col] = []
    for team in teams_list:
        team_stats = return_team_stats(season,team)
        d['total_points'].append(team_stats['total_points'])
        d['team_name'].append(team) 
        d['matches_played'].append(team_stats['matches_played'])
        d['points_per_match'].append(team_stats['points_per_match'])
        d['wins'].append(team_stats['wins'])
        d['draws'].append(team_stats['draws'])
        d['losses'].append(team_stats['losses'])
        d['avg_xg'].append(team_stats['average_xg'])
        d['goals_scored'].append(team_stats['goals_scored'])
        d['goal_difference'].append(team_stats['goal_difference'])

    standings_df = pd.DataFrame(d)
    standings_df = standings_df.sort_values(
        by=['total_points', 'goal_difference', 'goals_scored'],
        ascending=False
    ).reset_index(drop=True)

    standings_df.index += 1
    standings_df.index.name = 'rank'

    return standings_df.to_dict(orient='records')




@router.get("/seasons/{season}/teams/{team_name}/summary")
def return_team_stats(season: int, team_name: str):
    t_df = temp_df[temp_df['season']==season]
    # Matches Played
    matches_played = t_df[(t_df['home_team'] == team_name) | (t_df['away_team'] == team_name)].shape[0] 

    t_df =  t_df[(t_df['home_team'] == team_name) | (t_df['away_team'] == team_name)]  

    # Total Points, wins, draws, losses
    points,wins,draws,losses = 0,0,0,0 
    for key,value in t_df.iterrows():
        if value['home_team'] == team_name:
            if value['result'] == "H":
                points += 3
                wins += 1
            elif value['result'] == "D":
                points += 1
                draws += 1
            else:
                losses += 1
        else:
            if value['result'] == "A":
                points += 3
                wins += 1
            elif value['result'] == "D":
                points += 1
                draws += 1 
            else:
                losses += 1

    total_points = points
    
    # Goals scored and conceded 
    goals_scored = (
        t_df.loc[t_df["home_team"] == team_name, "home_score"].sum()
        + t_df.loc[t_df["away_team"] == team_name, "away_score"].sum()
    )

    goals_conceded = (
        t_df.loc[t_df["home_team"] == team_name, "away_score"].sum()
        + t_df.loc[t_df["away_team"] == team_name, "home_score"].sum()
    )

    # average elo score
    home_elo_score_sum = t_df.loc[t_df['home_team']==team_name,"home_elo"].sum()
    away_elo_score_sum = t_df.loc[t_df['away_team']==team_name,"away_elo"].sum()

    total_elo_score = home_elo_score_sum + away_elo_score_sum
    average_elo_score = total_elo_score / matches_played

    # xG
    home_xg_sum = t_df.loc[t_df['home_team'] == team_name, "home_xg"].sum()
    away_xg_sum = t_df.loc[t_df['away_team'] == team_name, "away_xg"].sum()
    total_xg = home_xg_sum + away_xg_sum
    avg_xg = total_xg / matches_played 


    # PPDA (average, not sum)
    home_ppda_sum = t_df.loc[t_df['home_team'] == team_name, "home_ppda"].sum()
    away_ppda_sum = t_df.loc[t_df['away_team'] == team_name, "away_ppda"].sum()
    total_ppda = home_ppda_sum + away_ppda_sum
    average_ppda = total_ppda / matches_played if matches_played != 0 else 0


    # Deep completions
    home_deep_completions_sum = t_df.loc[t_df['home_team'] == team_name, "home_deep_completions"].sum()
    away_deep_completions_sum = t_df.loc[t_df['away_team'] == team_name, "away_deep_completions"].sum()
    total_deep_completions = home_deep_completions_sum + away_deep_completions_sum


    # Cards
    home_red_cards_sum = t_df.loc[t_df['home_team'] == team_name, "home_red_cards"].sum()
    away_red_cards_sum = t_df.loc[t_df['away_team'] == team_name, "away_red_cards"].sum()
    total_red_cards = home_red_cards_sum + away_red_cards_sum

    home_yellow_cards_sum = t_df.loc[t_df['home_team'] == team_name, "home_yellow_cards"].sum()
    away_yellow_cards_sum = t_df.loc[t_df['away_team'] == team_name, "away_yellow_cards"].sum()
    total_yellow_cards = home_yellow_cards_sum + away_yellow_cards_sum


    goal_difference = goals_scored - goals_conceded

    points_per_match = total_points / matches_played
    goals_scored_per_match = goals_scored / matches_played
    goals_conceded_per_match = goals_conceded / matches_played
    xg_per_match = total_xg / matches_played
    deep_completions_per_match = total_deep_completions / matches_played
    yellow_cards_per_match = total_yellow_cards / matches_played
    red_cards_per_match = total_red_cards / matches_played

    return {
        "season": int(season),
        "team_name": str(team_name),
        "matches_played": int(matches_played),

        "total_points": int(total_points),
        "points_per_match": round(float(points_per_match), 2),

        "wins": int(wins),
        "draws": int(draws),
        "losses": int(losses),

        "goals_scored": int(goals_scored),
        "goals_conceded": int(goals_conceded),
        "goal_difference": int(goal_difference),
        "goals_scored_per_match": round(float(goals_scored_per_match), 2),
        "goals_conceded_per_match": round(float(goals_conceded_per_match), 2),

        "average_elo_score": round(float(average_elo_score), 2),

        "total_xg": round(float(total_xg), 2),
        "average_xg": round(float(avg_xg), 2),
        "xg_per_match": round(float(xg_per_match), 2),

        "average_ppda": round(float(average_ppda), 2),

        "total_deep_completions": int(total_deep_completions),
        "deep_completions_per_match": round(float(deep_completions_per_match), 2),

        "total_red_cards": int(total_red_cards),
        "red_cards_per_match": round(float(red_cards_per_match), 2),

        "total_yellow_cards": int(total_yellow_cards),
        "yellow_cards_per_match": round(float(yellow_cards_per_match), 2)
    }
