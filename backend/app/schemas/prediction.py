from pydantic import BaseModel
from typing import List, Optional


class OutcomeProbabilities(BaseModel):
    home: float
    draw: float
    away: float


class FixtureFeatureSummary(BaseModel):
    home_elo: Optional[float] = None
    away_elo: Optional[float] = None
    elo_diff: Optional[float] = None

    home_points_last_5: Optional[float] = None
    away_points_last_5: Optional[float] = None

    home_xg_last_5: Optional[float] = None
    away_xg_last_5: Optional[float] = None
    xg_form_diff_last_5: Optional[float] = None

    home_ppda_last_5: Optional[float] = None
    away_ppda_last_5: Optional[float] = None


class FixturePrediction(BaseModel):
    fixture_id: Optional[str] = None
    season: str
    matchday: Optional[int] = None
    home_team: str
    away_team: str
    kickoff: str

    predicted_result: str
    confidence: float
    probabilities: OutcomeProbabilities

    features: FixtureFeatureSummary


class UpcomingPredictionsResponse(BaseModel):
    season: str
    matchday: Optional[int] = None
    fixtures_loaded: int
    model_name: str
    model_accuracy: Optional[float] = None
    last_refreshed: Optional[str] = None
    fixtures: List[FixturePrediction]
