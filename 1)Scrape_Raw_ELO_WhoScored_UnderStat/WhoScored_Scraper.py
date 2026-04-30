import soccerdata as sd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "WhoScored_Data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def scrape_WhoScored(lg, start_sns, end_sns):
    sns = start_sns

    while True:
        if sns == end_sns:
            break

        file_path = OUT_DIR / f"{sns}_whoscored_fixtures.csv"

        if not file_path.exists():
            try:
                ws = sd.WhoScored(
                    leagues=lg,
                    seasons=sns,
                    headless=True
                )
                print(f"Scraping: {ws.seasons}")
                df = ws.read_schedule()
                df.to_csv(file_path, index=True)  # index=True to preserve game_id
                print(f"✅ Saved: {sns}")
            except Exception as e:
                print(f"❌ Failed for {sns}: {e}")
        else:
            print(f"⏭️  Skipped (exists): {sns}")

        # Increment season
        p1, p2 = sns.split("-")
        sns = f"{int(p1)+1}-{int(p2)+1}"

scrape_WhoScored("ITA-Serie A", "2014-15", "2026-27")