import os 
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder  
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


Base_Dir = Path(__file__).resolve().parents[1]
df = pd.read_csv(rf'{Base_Dir}/FINAL_FEATURES_TRAIN.csv')

# df.drop(columns = ['Unnamed: 0'],inplace=True)
d_result = {"H":0,"A":2,"D":1}

# print(df.columns)

# columns to preprocess: season,home_team,away_team,date,result
# Drop season, date,home_team,away_team: Weak predictive capabilities/ Can use ELO scores to indicate home and away teams

# preprocess result
print(df['result'].unique())
# df['result'] = LabelEncoder.fit_transform(LabelEncoder,df['result'])
df['result'] = df['result'].map(d_result)

print(df.columns)

print(df['result'].unique())
splits = [
    ('2025-01-01', '21-22 to half 24-25 | Test: rest of 24-25'),
    # ('2024-08-01', '21-22 to 23-24 | Test: full 24-25'),
    # ('2025-08-01', '21-22 to full 24-25 | Test: 25-26 so far'),
    # ('2023-08-01', '21-22 to 22-23 | Test: full 23-24 + 24-25'),
]

df['date'] = pd.to_datetime(df['date'])

drop_cols = [
    'season', 'date', 'home_team', 'away_team', 'home_score', 'away_score',
    'hpg', 'apg', 'home_yellow_cards', 'away_yellow_cards',
    'home_red_cards', 'away_red_cards'
]


splits = [
    ('2025-01-01', '21-22 to half 24-25 | Test: rest of 24-25'),
    # ('2024-08-01', '21-22 to 23-24 | Test: full 24-25'),
    # ('2025-08-01', '21-22 to full 24-25 | Test: 25-26 so far'),
    # ('2023-08-01', '21-22 to 22-23 | Test: full 23-24 + 24-25'),
]

df['date'] = pd.to_datetime(df['date'])

drop_cols = [
    'season', 'date', 'home_team', 'away_team', 'home_score', 'away_score',
    'hpg', 'apg', 'home_yellow_cards', 'away_yellow_cards',
    'home_red_cards', 'away_red_cards'
]

for split_date, split_name in splits:
    split_date = pd.to_datetime(split_date)

    train_df = df[df['date'] <= split_date].copy()
    test_df = df[(df['date'] > split_date) & (df['season'] == 2425)].copy()

    train_df.drop(columns=drop_cols, inplace=True)
    test_df.drop(columns=drop_cols, inplace=True)

    df_train_draw = train_df.copy()
    df_train_draw['result'] = np.where(df_train_draw['result']==1,1,0)
    X_train_draw = df_train_draw.drop(columns=['result'])
    y_train_draw = df_train_draw['result']


    df_train_ha = train_df[train_df['result']!=1].copy()
    X_train_ha = df_train_ha.drop(columns=['result'])
    y_train_ha = df_train_ha['result']

    clf_draw = LogisticRegression(max_iter=2000)
    clf_ha = LogisticRegression(max_iter=2000)

    clf_draw.fit(X_train_draw,y_train_draw)
    clf_ha.fit(X_train_ha, y_train_ha)

    X_test = test_df.drop(columns=['result'])
    y_test = test_df['result']

    y_draw_predicted = clf_draw.predict(X_test)
    y_ha_predicted = clf_ha.predict(X_test)

    y_final_predictions = np.where(y_draw_predicted == 0,y_ha_predicted,1)

    print("Accuracy:", accuracy_score(y_test, y_final_predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_final_predictions))
    print("Classification Report:\n", classification_report(y_test, y_final_predictions))


















