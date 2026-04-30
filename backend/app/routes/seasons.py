import pandas as pd 
from fastapi import APIRouter 
from pathlib import Path

# Initialize the directory of the dataset to load it and store it as a pandas df object.
BASE_DIR = Path(__file__).resolve().parents[3]
file_path = BASE_DIR/ "ML" / "FINAL_FEATURES_TRAIN_ENRICHED.csv"
df = pd.read_csv(rf"{file_path}")
temp_df = df[df['season']!=2526]

router = APIRouter(
    tags = ["seasons"]
)

@router.get("/seasons")
def list_seasons():
    return {"seasons":temp_df['season'].unique().tolist()} # -> {"seasons":[1415,1516,1617,1718,1819,1920,2021,2122,2223,2324,2425]}