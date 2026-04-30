from fastapi import APIRouter

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)
@router.get("/upcoming")
def get_upcoming_predictions():
    return {
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
            },
            {
                "home_team": "Juventus",
                "away_team": "Fiorentina",
                "kickoff": "2026-04-12 20:45",
                "predicted_result": "Home",
                "probabilities": {
                    "home": 0.46,
                    "draw": 0.28,
                    "away": 0.26
                }
            },
            {
                "home_team": "Lazio",
                "away_team": "Roma",
                "kickoff": "2026-04-13 15:00",
                "predicted_result": "Away",
                "probabilities": {
                    "home": 0.31,
                    "draw": 0.29,
                    "away": 0.40
                }
            }
        ]
    }
