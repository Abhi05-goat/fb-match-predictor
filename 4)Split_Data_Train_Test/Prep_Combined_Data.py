from pathlib import Path
import os
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

df = pd.read_csv(BASE_DIR / 'Processed_Combined.csv')

print(df.head())
print(df.columns)

df_train = df[df['home_score'].notna()].copy()
df_test = df[df['home_score'].isna()].copy()

print(df_train.isna().sum())
print(df_test.isna().sum())

os.makedirs(BASE_DIR / 'ML', exist_ok=True)
os.makedirs(BASE_DIR / 'ML/train', exist_ok=True)
os.makedirs(BASE_DIR / 'ML/test', exist_ok=True)

df_train = df_train.sort_values(by=['date'])
df_test = df_test.sort_values(by=['date'])

df_train.to_csv(BASE_DIR / 'ML/train/train.csv', index=False)
df_test.to_csv(BASE_DIR / 'ML/test/test.csv', index=False)
