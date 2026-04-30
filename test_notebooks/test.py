import os
import pandas as pd
from pathlib import Path

Base_Dir = Path(__file__).resolve().parents[1]
elo_dir = Base_Dir / 'ClubElo_Data'

for file in sorted(elo_dir.glob('*.csv')):
    try:
        df = pd.read_csv(file)
        print(f"\n{'='*80}")
        print(f"FILE: {file.name}")
        print("COLUMNS:", df.columns.tolist())
        print("SHAPE:", df.shape)
        print("HEAD:")
        print(df.head())
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"FILE: {file.name}")
        print("ERROR:", e)
