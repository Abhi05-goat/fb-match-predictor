import os
import pandas as pd
from pathlib import Path


KEEP_COLUMNS = [
    "season",
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "home_yellow_cards",
    "away_yellow_cards",
    "home_red_cards",
    "away_red_cards"
]


def preprocess_whoscored_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[col for col in KEEP_COLUMNS if col in df.columns]].copy()
    df['date'] = pd.to_datetime(df['date'].astype(str).str[:10], format='%Y-%m-%d')
    return df


def increment_season(sns: str) -> str:
    p1, p2 = sns.strip().split("-")
    return f"{int(p1)+1}-{int(p2)+1}"


def store_preprocessed(start_sns: str, end_sns: str, base_dir: Path = Path('.')) -> None:
    output_dir = base_dir / 'Preprocessed Seasons'
    output_dir.mkdir(exist_ok=True)

    sns = start_sns
    while sns != end_sns:
        input_path = base_dir / 'WhoScored_Data' / f'{sns}_whoscored_fixtures.csv'

        if not input_path.exists():
            print(f"[SKIP] File not found: {input_path}")
            sns = increment_season(sns)
            continue

        df = pd.read_csv(input_path)
        df = preprocess_whoscored_data(df)
        df.to_csv(output_dir / f'{sns}.csv', index=False)
        print(f"[DONE] {sns} → {len(df)} rows")

        sns = increment_season(sns)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parents[1]
    store_preprocessed('2014-15', '2026-27', base_dir=BASE_DIR)