import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

Base_Dir = Path(__file__).resolve().parents[1]
df = pd.read_csv(rf'{Base_Dir}/FINAL_FEATURES_TRAIN_WITH_XG_PPDA_DC.csv')

# ── Label encoding ────────────────────────────────────────────────────────────
d_result = {'H': 0, 'D': 1, 'A': 2}
if df['result'].dtype == object:
    df['result'] = df['result'].map(d_result)

df['date'] = pd.to_datetime(df['date'])

# ── Columns to drop ───────────────────────────────────────────────────────────
drop_cols = [
    'season', 'date', 'home_team', 'away_team',
    'home_score', 'away_score',
    'hpg', 'apg',
    'home_yellow_cards', 'away_yellow_cards',
    'home_red_cards', 'away_red_cards',
    'home_xg', 'away_xg',
    'home_ppda', 'away_ppda',
    'home_deep_completions', 'away_deep_completions',
]

# ── Temporal folds ────────────────────────────────────────────────────────────
fold_dates = [
    ('2022-08-01', 2223, 'Fold 1 | Train: 14-15→21-22 | Test: 22-23'),
    ('2023-08-01', 2324, 'Fold 2 | Train: 14-15→22-23 | Test: 23-24'),
    ('2024-08-01', 2425, 'Fold 3 | Train: 14-15→23-24 | Test: 24-25 ← FINAL HOLDOUT'),
]

# ── Draw weight sweep values ──────────────────────────────────────────────────
draw_weights = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

fold_results = []

for fold_idx, (split_date, test_season, split_name) in enumerate(fold_dates):
    split_date = pd.to_datetime(split_date)

    X_train_df = df[df['date'] < split_date].copy()
    X_test_df  = df[df['season'] == test_season].copy()

    X_train_df = X_train_df.drop(columns=drop_cols)
    X_test_df  = X_test_df.drop(columns=drop_cols)

    y_train = X_train_df.pop('result').to_numpy()
    y_test  = X_test_df.pop('result').to_numpy()

    X_train_df = X_train_df.fillna(0)
    X_test_df  = X_test_df.fillna(0)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_df)
    X_test  = scaler.transform(X_test_df)

    print(f"\n{'='*80}")
    print(f"Split: {split_name}")
    print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")

    # ── Draw weight sweep (Fold 1 & 2 only) ───────────────────────────────────
    if fold_idx < 2:
        print(f"\n── Draw weight sweep ──")
        best_draw_recall = -1
        best_weight      = 1.0

        for draw_weight in draw_weights:
            clf = LogisticRegression(
                max_iter=2000,
                class_weight={0: 1, 1: draw_weight, 2: 1},
            )
            clf.fit(X_train, y_train)
            y_pred      = clf.predict(X_test)
            acc         = accuracy_score(y_test, y_pred)
            recalls     = recall_score(y_test, y_pred, average=None, labels=[0, 1, 2])
            draw_recall = recalls[1]

            print(f"  draw_weight={draw_weight:.1f} → Acc: {acc:.4f} | "
                  f"Draw Recall: {draw_recall:.4f} | "
                  f"H Recall: {recalls[0]:.4f} | A Recall: {recalls[2]:.4f}")

            if draw_recall > best_draw_recall:
                best_draw_recall = draw_recall
                best_weight      = draw_weight

        print(f"\n  ✓ Best draw weight for {split_name[:6]}: {best_weight} "
              f"(Draw Recall: {best_draw_recall:.4f})")

    # ── Final eval with locked weight ─────────────────────────────────────────
    best_locked_weight = 1.4

    print(f"\n── Final eval with draw_weight={best_locked_weight} ──")
    clf_final = LogisticRegression(
        max_iter=2000,
        class_weight={0: 1, 1: best_locked_weight, 2: 1},
    )
    clf_final.fit(X_train, y_train)
    y_pred = clf_final.predict(X_test)

    acc     = accuracy_score(y_test, y_pred)
    cm      = confusion_matrix(y_test, y_pred)
    report  = classification_report(y_test, y_pred, target_names=['Home', 'Draw', 'Away'])
    recalls = recall_score(y_test, y_pred, average=None, labels=[0, 1, 2])

    print(f"\nAccuracy : {acc:.4f}")
    print(f"Confusion Matrix:\n{cm}")
    print(f"Classification Report:\n{report}")

    fold_results.append({
        'fold':        split_name[:6],
        'train_size':  len(X_train),
        'test_size':   len(X_test),
        'accuracy':    acc,
        'h_recall':    recalls[0],
        'draw_recall': recalls[1],
        'a_recall':    recalls[2],
    })

# ── Cross-fold summary ────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print("CROSS-FOLD SUMMARY")
summary_df = pd.DataFrame(fold_results)
print(summary_df.to_string(index=False))
print(f"\nMean Accuracy   : {summary_df['accuracy'].mean():.4f}")
print(f"Mean Draw Recall: {summary_df['draw_recall'].mean():.4f}")
print(f"Mean H Recall   : {summary_df['h_recall'].mean():.4f}")
print(f"Mean A Recall   : {summary_df['a_recall'].mean():.4f}")