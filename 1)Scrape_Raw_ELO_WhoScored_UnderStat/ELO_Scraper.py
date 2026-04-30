import soccerdata as sd
from pathlib import Path

ClubElo = sd.ClubElo(
    proxy=None,
    no_cache=False,
    no_store=False,
    data_dir=Path(r'C:\Users\asiva\OneDrive\Desktop\Fb Match Predictor\ClubElo_Data')
)

serie_a_teams_1415_to_2526 = [
    # Regulars (present most or all seasons)
    "Inter",
    "Milan",
    "Napoli",
    "Juventus",
    "Lazio",
    "Roma",
    "Atalanta",
    "Fiorentina",
    "Bologna",
    "Torino",
    "Udinese",
    "Genoa",
    "Lecce",
    "Cagliari",
    "Verona",

    # 2021-22 to 2025-26 entrants
    "Sassuolo",
    "Empoli",
    "Sampdoria",
    "Spezia",
    "Salernitana",
    "Venezia",
    "Monza",
    "Cremonese",
    "Frosinone",
    "Parma",
    "Como",
    "Pisa",

    # 2014-15 to 2020-21 additional teams
    "Chievo",
    "Palermo",
    "Carpi",
    "Frosinone",   
    "Crotone",
    "Pescara",
    "Benevento",
    "SPAL",
    "Brescia",
    "Lecce",
    "Reggiana",
    "Cesena"
]

# Deduplicate in case of overlaps
serie_a_teams_1415_to_2526 = list(dict.fromkeys(serie_a_teams_1415_to_2526))

output_dir = Path(r'C:\Users\asiva\OneDrive\Desktop\Fb Match Predictor\ClubElo_Data')
output_dir.mkdir(parents=True, exist_ok=True)

for team in serie_a_teams_1415_to_2526:
    file_path = output_dir / f"{team}.csv"
    if not file_path.exists():
        try:
            df = ClubElo.read_team_history(team)
            df.to_csv(file_path, index=True)
            print(f"✅ Saved: {team}")
        except Exception as e:
            print(f"❌ Failed: {team} — {e}")
    else:
        print(f"⏭️  Skipped (exists): {team}")