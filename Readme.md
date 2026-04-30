# Serie A Analytics

A full-stack football analytics project covering end-to-end data engineering, machine learning, a FastAPI backend, and a Streamlit dashboard — built on historical Serie A match data.

The project predicts match outcomes using an XGBoost classifier and surfaces team-level analytics through a live dashboard backed by a REST API.

***

## What It Does

- **Predicts** Serie A match outcomes (Home Win / Draw / Away Win) using a trained XGBoost classifier
- **Surfaces season standings** with tiebreakers (goal difference, goals scored) for any historical season
- **Profiles individual teams** across points, goals, xG, Elo, PPDA, deep completions, and discipline
- **Compares two teams** head-to-head across all key metrics with visualisations
- **Serves all data** through a structured FastAPI backend with clean JSON endpoints

***

## Tech Stack

| Layer | Tools |
|---|---|
| Data & ML | Python, Pandas, NumPy, Scikit-learn, XGBoost, CatBoost |
| Backend | FastAPI, Pydantic, Uvicorn |
| Frontend | Streamlit, Plotly |
| Versioning | Git / GitHub |

***

## Project Structure

```text
Serie-A-Analytics/
│
├── backend/
│   └── app/
│       ├── main.py
│       └── routes/
│           ├── health.py
│           ├── seasons.py
│           ├── teams.py
│           └── predictions.py
│
├── ML/
│   ├── Models/
│   │   ├── xgb_final.json
│   │   ├── feature_columns.json
│   │   ├── config.json
│   │   └── eval_report.md
│   ├── train/
│   └── test/
│
├── 1)Scrape_Raw_ELO_WhoScored_UnderStat/
├── 2)Extract_And_Preprocess_Seasons/
├── 3)Combine_Seasons/
├── 4)Split_Data_Train_Test/
├── 5)Preprocess_FeatureEngineer_Train_Test/
├── 6)Adding_XG_PPDA/
│
├── Combined.csv
├── Processed_Combined.csv
├── dashboard.py
└── README.md
```

***

## ML Pipeline

The pipeline runs sequentially across numbered notebooks/scripts:

1. **Scrape** — Pull raw match data, Elo ratings, WhoScored, and Understat sources
2. **Extract & Preprocess** — Clean and structure season-level fixture data
3. **Combine** — Merge all seasons into a single training dataset
4. **Split** — Create train/test sets with no data leakage
5. **Feature Engineering** — Build rolling 5-match form stats per team
6. **Add xG & PPDA** — Attach expected goals and pressing intensity metrics
7. **Train** — Compare XGBoost, Logistic Regression, and CatBoost classifiers
8. **Freeze** — Serialise the final XGBoost model to `ML/Models/xgb_final.json`

### Model

The final model is an XGBoost multi-class classifier predicting three outcome classes.

Key feature groups used at inference:

- Rolling form (last 5 matches): points, wins, draws, losses, goals scored/conceded
- xG (expected goals) and xG against
- PPDA (passes allowed per defensive action — a pressing intensity proxy)
- Deep completions (passes into the final third)
- Elo rating differential

***

## Backend API

Built with FastAPI. All endpoints are documented automatically at `/docs`.

### Running locally

```bash
uvicorn backend.app.main:app --reload
```

API base: `http://127.0.0.1:8000`  
Swagger docs: `http://127.0.0.1:8000/docs`

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root welcome response |
| `GET` | `/health` | API health check |
| `GET` | `/seasons` | List all available seasons |
| `GET` | `/seasons/{season}/teams` | List all teams in a season |
| `GET` | `/seasons/{season}/teams/standings` | Full league table sorted by points, GD, goals scored |
| `GET` | `/seasons/{season}/teams/{team}/summary` | Full stat profile for a team in a season |
| `GET` | `/predictions/upcoming` | Upcoming fixture predictions (XGBoost inference) |

### Standings response shape

```json
[
  {
    "team_name": "Juventus",
    "total_points": 87,
    "matches_played": 38,
    "points_per_match": 2.29,
    "wins": 26,
    "draws": 9,
    "losses": 3,
    "goal_difference": 55,
    "goals_scored": 72,
    "avg_xg": 1.55
  }
]
```

### Prediction response shape

```json
{
  "season": "2025-26",
  "matchday": 31,
  "fixtures": [
    {
      "home_team": "Inter",
      "away_team": "Milan",
      "kickoff": "2026-04-12 18:00",
      "predicted_result": "Home",
      "probabilities": {
        "home": 0.52,
        "draw": 0.24,
        "away": 0.24
      }
    }
  ]
}
```

***

## Dashboard

A Streamlit frontend connects to the FastAPI backend and provides two views.

### Running locally

```bash
streamlit run dashboard.py
```

Requires the FastAPI backend to be running at `http://127.0.0.1:8000`.

### Dashboard view

Displays a selected team's full season profile:

- Hero banner with season record
- Key metrics: points per match, Elo, xG, PPDA, deep completions, cards
- Quick Reads: season pace, goal margin, discipline load
- **Overview tab** — result profile bar chart, scoring output chart, team strength radar
- **Attack tab** — goals and xG breakdown
- **Control & Discipline tab** — PPDA gauge, card stats
- **JSON tab** — raw API response
- **Standings table** (right panel) — full league table with Champions League, Europa, and relegation zone colour coding; selected team highlighted

### Compare Teams view

Side-by-side comparison of any two teams in a season:

- Head-to-head metric matchup table (winning side highlighted)
- Radar chart comparing normalised profiles across 6 dimensions
- Grouped bar charts: per-match metrics, PPDA, Elo

***

## Current Status

| Area | Status |
|---|---|
| ML pipeline | Complete |
| XGBoost model (frozen) | Complete |
| FastAPI backend | Complete |
| Season & team stat endpoints | Complete |
| Standings endpoint (with tiebreakers) | Complete |
| Streamlit dashboard | Complete |
| Prediction endpoint (live inference) | In progress |
| Deployment | Planned |

***

## Author

**Abhivanth Sivaprakash**  
GitHub: [Abhi05-goat](https://github.com/Abhi05-goat)
