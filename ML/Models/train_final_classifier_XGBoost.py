import os
import json
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, recall_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

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

for col in df.columns:
    if col not in drop_cols:
        print(col)

# ── Temporal folds ────────────────────────────────────────────────────────────
fold_dates = [
    ('2022-08-01', 2223, 'Fold 1 | Train: 14-15→21-22 | Test: 22-23'),
    ('2023-08-01', 2324, 'Fold 2 | Train: 14-15→22-23 | Test: 23-24'),
    ('2024-08-01', 2425, 'Fold 3 | Train: 14-15→23-24 | Test: 24-25 ← FINAL HOLDOUT'),
]

draw_weights   = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
fold_results   = []

# ── Model save directory ──────────────────────────────────────────────────────
MODELS_DIR = Base_Dir / 'Models'
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PARAMS = {
    'objective':             'multi:softmax',
    'num_class':             3,
    'n_estimators':          500,
    'max_depth':             4,
    'learning_rate':         0.03,
    'subsample':             0.8,
    'colsample_bytree':      0.8,
    'reg_lambda':            5,
    'random_state':          42,
    'eval_metric':           'mlogloss',
    'early_stopping_rounds': 40,
    'verbosity':             0,
}

BEST_LOCKED_WEIGHT = 1.4


for fold_idx, (split_date, test_season, split_name) in enumerate(fold_dates):
    split_date = pd.to_datetime(split_date)

    X_train_df = df[df['date'] < split_date].copy()
    X_test_df  = df[df['season'] == test_season].copy()

    X_train_df = X_train_df.drop(columns=drop_cols)
    X_test_df  = X_test_df.drop(columns=drop_cols)

    y_train = X_train_df.pop('result').to_numpy()
    y_test  = X_test_df.pop('result').to_numpy()

    # ── Save feature column order (from Fold 3 — the final training set) ──────
    feature_columns = X_train_df.columns.tolist()

    X_train_df = X_train_df.fillna(0)
    X_test_df  = X_test_df.fillna(0)

    X_train = X_train_df
    y_train = y_train
    X_test = X_test_df

    print(f"\n{'='*80}")
    print(f"Split: {split_name}")
    print(f"Train size: {len(X_train_df)} | Test size: {len(X_test_df)}")

    # ── Draw weight sweep (Fold 1 & 2 only) ───────────────────────────────────
    if fold_idx < 2:
        print(f"\n── Draw weight sweep ──")
        best_draw_recall = -1
        best_weight      = 1.0

        for draw_weight in draw_weights:
            sample_weights = np.where(y_train == 1, draw_weight, 1.0)
            clf = XGBClassifier(**MODEL_PARAMS)
            clf.fit(X_train, y_train, sample_weight=sample_weights,
                    eval_set=[(X_test, y_test)], verbose=False)
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

    # ── Final eval ────────────────────────────────────────────────────────────
    print(f"\n── Final eval with draw_weight={BEST_LOCKED_WEIGHT} ──")
    sample_weights_final = np.where(y_train == 1, BEST_LOCKED_WEIGHT, 1.0)

    clf_final = XGBClassifier(**MODEL_PARAMS)
    clf_final.fit(X_train, y_train, sample_weight=sample_weights_final,
                  eval_set=[(X_test, y_test)], verbose=False)
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
        'accuracy':    round(acc, 4),
        'h_recall':    round(float(recalls[0]), 4),
        'draw_recall': round(float(recalls[1]), 4),
        'a_recall':    round(float(recalls[2]), 4),
    })

    # ── Freeze Fold 3 artifacts ───────────────────────────────────────────────
    if fold_idx == 2:
        print(f"\n{'='*80}")
        print("[SAVING] Freezing Fold 3 model artifacts...")

        # 1) XGBoost model weights
        model_path = MODELS_DIR / 'xgb_final.json'
        clf_final.save_model(str(model_path))
        print(f"  [✓] Model weights     → {model_path}")


        # 3) Feature column order
        features_path = MODELS_DIR / 'feature_columns.json'
        with open(features_path, 'w') as f:
            json.dump(feature_columns, f, indent=4)
        print(f"  [✓] Feature columns   → {features_path}")

        # 4) Config / params
        config = {
            'model_type':        'XGBClassifier',
            'draw_weight':       BEST_LOCKED_WEIGHT,
            'label_encoding':    {'H': 0, 'D': 1, 'A': 2},
            'model_params':      MODEL_PARAMS,
            'training_cutoff':   str(split_date.date()),
            'test_season':       test_season,
            'n_features':        len(feature_columns),
        }
        config_path = MODELS_DIR / 'config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"  [✓] Config/params     → {config_path}")


# ── Cross-fold summary ────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print("CROSS-FOLD SUMMARY")
summary_df = pd.DataFrame(fold_results)
print(summary_df.to_string(index=False))
print(f"\nMean Accuracy   : {summary_df['accuracy'].mean():.4f}")
print(f"Mean Draw Recall: {summary_df['draw_recall'].mean():.4f}")
print(f"Mean H Recall   : {summary_df['h_recall'].mean():.4f}")
print(f"Mean A Recall   : {summary_df['a_recall'].mean():.4f}")

# 5) Evaluation metrics markdown
metrics_md = f"""# XGBoost Final Model — Evaluation Report

## Cross-Fold Summary

| Fold | Train Size | Test Size | Accuracy | H Recall | Draw Recall | A Recall |
|------|-----------|-----------|----------|----------|-------------|----------|
"""
for r in fold_results:
    metrics_md += f"| {r['fold']} | {r['train_size']} | {r['test_size']} | {r['accuracy']} | {r['h_recall']} | {r['draw_recall']} | {r['a_recall']} |\n"

metrics_md += f"""
## Aggregate

| Metric | Value |
|--------|-------|
| Mean Accuracy | {summary_df['accuracy'].mean():.4f} |
| Mean Draw Recall | {summary_df['draw_recall'].mean():.4f} |
| Mean H Recall | {summary_df['h_recall'].mean():.4f} |
| Mean A Recall | {summary_df['a_recall'].mean():.4f} |

## Model Config

- **Model**: XGBClassifier
- **Draw class weight**: {BEST_LOCKED_WEIGHT}
- **Label encoding**: H=0, D=1, A=2
- **n_features**: {len(feature_columns)}
- **Training cutoff**: 2024-08-01 (seasons 2014/15 → 2023/24)
- **Test season**: 2024/25
"""

metrics_path = MODELS_DIR / 'eval_report.md'
with open(metrics_path, 'w', encoding='utf-8') as f:
    f.write(metrics_md)
print(f"  [✓] Eval report       → {metrics_path}")
print(f"\n[DONE] All artifacts saved to {MODELS_DIR}")