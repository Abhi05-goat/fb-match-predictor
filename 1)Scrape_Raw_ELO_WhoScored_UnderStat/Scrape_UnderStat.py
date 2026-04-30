from pathlib import Path
import pandas as pd
import soccerdata as sd

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "Understat_Data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

understat = sd.Understat(
    leagues="ITA-Serie A",
    seasons=[
        1415, 1516, 1617, 1718, 1819,
        1920, 2021, 2122, 2223, 2324,
        2425, 2526
    ],
    no_cache=False,
    no_store=False,
)

print("Selected leagues:", understat.leagues)
print("Selected seasons:", understat.seasons)

schedule_df = understat.read_schedule(include_matches_without_data=True)
print("\nSCHEDULE")
print(schedule_df.head())
print(schedule_df.columns)
schedule_df.to_csv(OUT_DIR / "serie_a_understat_schedule.csv", index=True)

team_stats_df = understat.read_team_match_stats()
print("\nTEAM MATCH STATS")
print(team_stats_df.head())
print(team_stats_df.columns)
team_stats_df.to_csv(OUT_DIR / "serie_a_understat_team_match_stats.csv", index=True)