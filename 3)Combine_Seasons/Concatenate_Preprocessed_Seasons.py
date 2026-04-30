from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
input_dir = BASE_DIR / 'Preprocessed Seasons'
output_combined = BASE_DIR / 'Combined.csv'
output_sorted = BASE_DIR / 'Processed_Combined.csv'

files = sorted(input_dir.glob('*.csv'))
print([f.name for f in files])

dfs = []
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)
    print(f"[LOADED] {file.name} -> {len(df)} rows")

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(output_combined, index=False)

combined_df['date'] = pd.to_datetime(combined_df['date'])
combined_df = combined_df.sort_values(by=['date']).reset_index(drop=True)
combined_df.to_csv(output_sorted, index=False)

print(f"\n[DONE] Combined rows: {len(combined_df)}")
print(f"[SAVED] {output_combined}")
print(f"[SAVED] {output_sorted}")
