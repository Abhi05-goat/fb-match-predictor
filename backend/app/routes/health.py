from fastapi import APIRouter 
from pathlib import Path
import pandas as pd

router = APIRouter(
    tags = ["Health"]
)

# Initialize the directory of the dataset to load it and store it as a pandas df object.
BASE_DIR = Path(__file__).resolve().parents[3]
file_path = BASE_DIR/ "ML" / "FINAL_FEATURES_TRAIN_ENRICHED.csv"
df = pd.read_csv(rf"{file_path}")
temp_df = df[df['season']!=2526]

@router.get("/health/dataset")
def loaded_df():
    return {"test":df.head().to_dict()}

