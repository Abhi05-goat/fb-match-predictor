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
from sklearn.ensemble import GradientBoostingClassifier
from catboost import CatBoostClassifier
from sklearn.svm import SVC

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

for split_date, split_name in splits:
    split_date = pd.to_datetime(split_date)

    X_train = df[df['date'] <= split_date].copy()
    X_test = df[(df['date'] > split_date) & (df['season'] == 2425)].copy()

    X_train.drop(columns=drop_cols, inplace=True)
    X_test.drop(columns=drop_cols, inplace=True)

    print(X_train.dtypes)
    
    y_train = np.array(X_train['result'])
    y_test = np.array(X_test['result'])

    X_train.drop(columns=['result'], inplace=True)
    X_test.drop(columns=['result'], inplace=True)

    print(f"\n{'='*80}")
    print(f"Split: {split_name}")
    print(f"Split date: {split_date.date()}")
    print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")

    y_test_df = pd.DataFrame(y_test, columns=['result'])
    total_classes_count = len(y_test_df)

    # home_test_counts = len(y_test_df[y_test_df['result'] == 0])
    # draw_test_counts = len(y_test_df[y_test_df['result'] == 1])
    # away_test_counts = len(y_test_df[y_test_df['result'] == 2])

    # Crafting a few dumb baselines. - To see how much better each model being trained is than a dumb always one class baseline.

    # print(f"Home Counts: {home_test_counts}")
    # print(f"Draw Counts: {draw_test_counts}")
    # print(f"Away Counts: {away_test_counts}")
    # print(f"Total class count: {total_classes_count}")
    # print(f"Only home preds baseline: {home_test_counts / total_classes_count}")
    # print(f"Only draw preds baseline: {draw_test_counts / total_classes_count}")
    # print(f"Only away preds baseline: {away_test_counts / total_classes_count}")

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Training the Multinomial LR

    clf = LogisticRegression(max_iter=2000, class_weight={0:1,1:1,2:1})

    # Training the RandomForestClassifier 
    # clf = RandomForestClassifier(
    # n_estimators=301,
    # max_depth=10,
    # min_samples_leaf=5,
    # random_state=42,
    # n_jobs=-1
    # )

    # Training the XGBoost Classifier
    
    # clf = XGBClassifier(
    # objective='multi:softmax',
    # num_class=3,
    # n_estimators=300,
    # max_depth=5,
    # learning_rate=0.05,
    # subsample=0.8,
    # colsample_bytree=0.8,
    # random_state=42,
    # eval_metric='mlogloss'
    # )

    # The Gradient boosting classifier
    # clf = GradientBoostingClassifier(
    # n_estimators=200,
    # learning_rate=0.05,
    # max_depth=3,
    # random_state=42
    # )
    
    # Catboost clf
    # clf = CatBoostClassifier(
    # iterations=300,
    # depth=6,
    # learning_rate=0.05,
    # loss_function='MultiClass',
    # eval_metric='MultiClass',
    # random_seed=42,
    # verbose=0
    # )

    # SVM clf
    # clf = SVC(
    # kernel='rbf',
    # C=1.0,
    # gamma='scale',
    # random_state=42
    # )

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
#-----------------------------------------------------------------------------------------------------------






