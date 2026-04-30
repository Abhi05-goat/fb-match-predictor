import pandas as pd
from pathlib import Path

Base_Dir = Path(__file__).resolve().parents[1]

# ── Load ──────────────────────────────────────────────────────────────────────
df_final = pd.read_csv(rf'{Base_Dir}/ML/FINAL_FEATURES_TRAIN.csv')
df_final = df_final.drop(columns=['Unnamed: 0'], errors='ignore')

df_U = pd.read_csv(rf'{Base_Dir}/Understat_Data/serie_a_understat_team_match_stats.csv')

df_U = df_U[[
    'season', 'date', 'home_team', 'away_team',
    'home_xg', 'away_xg',
    'home_ppda', 'away_ppda',
    'home_deep_completions', 'away_deep_completions'
]].copy()


# ── Team name normalisation ───────────────────────────────────────────────────
TEAM_NAME_MAP = {
    'Parma Calcio 1913': 'Parma',
    'AC Milan':          'Milan',
    'AC Carpi':          'Carpi',
}

def normalise_teams(df: pd.DataFrame) -> pd.DataFrame:
    df['home_team'] = df['home_team'].replace(TEAM_NAME_MAP)
    df['away_team'] = df['away_team'].replace(TEAM_NAME_MAP)
    return df

df_final = normalise_teams(df_final)
df_U     = normalise_teams(df_U)


# ── Season encoding normalisation ─────────────────────────────────────────────
def season_to_int(val) -> int:
    s = str(val).strip()
    if '-' in s:
        parts = s.split('-')
        return int(parts[0][-2:] + parts[1][-2:])
    return int(s)


df_final['season'] = df_final['season'].apply(season_to_int)
df_U['season']     = df_U['season'].apply(season_to_int)


# ── Date normalisation ────────────────────────────────────────────────────────
df_final['date'] = pd.to_datetime(df_final['date']).dt.normalize()
df_U['date']     = pd.to_datetime(df_U['date']).dt.normalize()


# ── Deduplicate Understat before merge ────────────────────────────────────────
before = len(df_U)
df_U = df_U.drop_duplicates(subset=['season', 'date', 'home_team', 'away_team'], keep='first')
print(f"[Understat] Dropped {before - len(df_U)} duplicate rows")


# ── Merge ─────────────────────────────────────────────────────────────────────
df_merged = df_final.merge(
    df_U,
    on=['season', 'date', 'home_team', 'away_team'],
    how='left'
)

if len(df_merged) != len(df_final):
    print(f"[WARNING] Row count changed: {len(df_final)} → {len(df_merged)}, deduping...")
    df_merged = df_merged.drop_duplicates(
        subset=['season', 'date', 'home_team', 'away_team'],
        keep='first'
    )
    print(f"[WARNING] Deduped back to: {len(df_merged)} rows")


# ── Drop rows with no Understat coverage ──────────────────────────────────────
understat_cols = [
    'home_xg', 'away_xg',
    'home_ppda', 'away_ppda',
    'home_deep_completions', 'away_deep_completions'
]

before = len(df_merged)
df_merged = df_merged.dropna(subset=understat_cols)
dropped = before - len(df_merged)
print(f"\n[DROP] Removed {dropped} rows with no Understat coverage ({dropped/before*100:.1f}%)")
print(f"[DROP] Remaining rows: {len(df_merged)}")


# ── Sanity check ──────────────────────────────────────────────────────────────
print("\nFinal shape:", df_merged.shape)
print("\nMissing values after drop:")
print(df_merged[understat_cols].isnull().sum())


# ── Save ──────────────────────────────────────────────────────────────────────
df_merged.to_csv(rf'{Base_Dir}/ML/FINAL_FEATURES_TRAIN_ENRICHED.csv', index=False)
print("\n[SAVED] FINAL_FEATURES_TRAIN_ENRICHED.csv")