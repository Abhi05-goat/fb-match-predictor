import pandas as pd
from pathlib import Path

Base_Dir = Path(__file__).resolve().parents[1]

# Load enriched match-level dataset
df = pd.read_csv(rf'{Base_Dir}/ML/FINAL_FEATURES_TRAIN_ENRICHED.csv')

# Clean unnamed column if present
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

# Make sure date is datetime and data is sorted chronologically
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['date', 'season', 'home_team', 'away_team']).reset_index(drop=True)

# Create a stable match id for merging rolling features back
df['match_id'] = df.index

# Build team-level long format:
# one row for home team, one row for away team
home_df = df[
    [
        'match_id', 'season', 'date',
        'home_team', 'away_team',
        'home_xg', 'away_xg',
        'home_ppda', 'away_ppda',
        'home_deep_completions', 'away_deep_completions'
    ]
].copy()

home_df = home_df.rename(columns={
    'home_team': 'team',
    'away_team': 'opponent',
    'home_xg': 'xg_for',
    'away_xg': 'xg_against',
    'home_ppda': 'ppda',
    'away_ppda': 'ppda_faced',
    'home_deep_completions': 'deep_completions',
    'away_deep_completions': 'deep_completions_allowed'
})
home_df['venue'] = 'home'

away_df = df[
    [
        'match_id', 'season', 'date',
        'home_team', 'away_team',
        'home_xg', 'away_xg',
        'home_ppda', 'away_ppda',
        'home_deep_completions', 'away_deep_completions'
    ]
].copy()

away_df = away_df.rename(columns={
    'away_team': 'team',
    'home_team': 'opponent',
    'away_xg': 'xg_for',
    'home_xg': 'xg_against',
    'away_ppda': 'ppda',
    'home_ppda': 'ppda_faced',
    'away_deep_completions': 'deep_completions',
    'home_deep_completions': 'deep_completions_allowed'
})
away_df['venue'] = 'away'

team_match_df = pd.concat([home_df, away_df], ignore_index=True)
team_match_df = team_match_df.sort_values(['team', 'date', 'match_id']).reset_index(drop=True)

rolling_source_cols = [
    'xg_for',
    'xg_against',
    'ppda',
    'ppda_faced',
    'deep_completions',
    'deep_completions_allowed'
]

# Compute leakage-safe rolling last-5 averages using only PRIOR matches
for col in rolling_source_cols:
    team_match_df[f'{col}_last_5'] = (
        team_match_df
        .groupby('team')[col]
        .transform(lambda s: s.shift(1).rolling(5, min_periods=1).mean())
    )

# Keep only the rolling columns we need to merge back
rolling_cols = [
    'match_id', 'team', 'venue',
    'xg_for_last_5',
    'xg_against_last_5',
    'ppda_last_5',
    'ppda_faced_last_5',
    'deep_completions_last_5',
    'deep_completions_allowed_last_5'
]

rolling_df = team_match_df[rolling_cols].copy()

# Split into home-side and away-side rolling features
home_roll = rolling_df[rolling_df['venue'] == 'home'].copy()
home_roll = home_roll.rename(columns={
    'team': 'home_team',
    'xg_for_last_5': 'home_xg_last_5',
    'xg_against_last_5': 'home_xga_last_5',
    'ppda_last_5': 'home_ppda_last_5',
    'ppda_faced_last_5': 'home_ppda_faced_last_5',
    'deep_completions_last_5': 'home_deep_completions_last_5',
    'deep_completions_allowed_last_5': 'home_deep_completions_allowed_last_5'
})
home_roll = home_roll.drop(columns=['venue'])

away_roll = rolling_df[rolling_df['venue'] == 'away'].copy()
away_roll = away_roll.rename(columns={
    'team': 'away_team',
    'xg_for_last_5': 'away_xg_last_5',
    'xg_against_last_5': 'away_xga_last_5',
    'ppda_last_5': 'away_ppda_last_5',
    'ppda_faced_last_5': 'away_ppda_faced_last_5',
    'deep_completions_last_5': 'away_deep_completions_last_5',
    'deep_completions_allowed_last_5': 'away_deep_completions_allowed_last_5'
})
away_roll = away_roll.drop(columns=['venue'])

# Merge rolling features back to match-level dataframe
df_final = df.merge(
    home_roll,
    on=['match_id', 'home_team'],
    how='left'
)

df_final = df_final.merge(
    away_roll,
    on=['match_id', 'away_team'],
    how='left'
)

# Add matchup-difference features
df_final['xg_form_diff_last_5'] = df_final['home_xg_last_5'] - df_final['away_xg_last_5']
df_final['xga_form_diff_last_5'] = df_final['home_xga_last_5'] - df_final['away_xga_last_5']
df_final['ppda_diff_last_5'] = df_final['home_ppda_last_5'] - df_final['away_ppda_last_5']
df_final['deep_completions_diff_last_5'] = (
    df_final['home_deep_completions_last_5'] - df_final['away_deep_completions_last_5']
)

# Drop helper column
df_final = df_final.drop(columns=['match_id'])

# Sanity check before dropping rows
new_feature_cols = [
    'home_xg_last_5', 'home_xga_last_5',
    'away_xg_last_5', 'away_xga_last_5',
    'home_ppda_last_5', 'away_ppda_last_5',
    'home_deep_completions_last_5', 'away_deep_completions_last_5',
    'xg_form_diff_last_5', 'xga_form_diff_last_5',
    'ppda_diff_last_5', 'deep_completions_diff_last_5'
]

print("Shape before dropping rolling-NaN rows:", df_final.shape)
print("\nMissing values in new rolling features:")
print(df_final[new_feature_cols].isnull().sum())

# Drop rows with incomplete rolling-history features
all_last5_cols = [col for col in df_final.columns if 'last_5' in col]
before_drop = len(df_final)
df_final = df_final.dropna(subset=all_last5_cols).reset_index(drop=True)
after_drop = len(df_final)

print(f"\n[DROP] Removed {before_drop - after_drop} rows with incomplete rolling history")
print(f"[DROP] Remaining rows: {after_drop}")

# Save final engineered dataset
df_final.to_csv(rf'{Base_Dir}/ML/FINAL_FEATURES_TRAIN_WITH_XG_PPDA_DC.csv', index=False)
print(f"\n[SAVED] {Base_Dir}/ML/FINAL_FEATURES_TRAIN_WITH_XG_PPDA_DC.csv")
