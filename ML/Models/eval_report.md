# XGBoost Final Model — Evaluation Report

## Cross-Fold Summary

| Fold | Train Size | Test Size | Accuracy | H Recall | Draw Recall | A Recall |
|------|-----------|-----------|----------|----------|-------------|----------|
| Fold 1 | 2886 | 378 | 0.5238 | 0.7375 | 0.11 | 0.5847 |
| Fold 2 | 3264 | 378 | 0.5635 | 0.761 | 0.1875 | 0.6636 |
| Fold 3 | 3642 | 378 | 0.5423 | 0.74 | 0.2315 | 0.575 |

## Aggregate

| Metric | Value |
|--------|-------|
| Mean Accuracy | 0.5432 |
| Mean Draw Recall | 0.1763 |
| Mean H Recall | 0.7462 |
| Mean A Recall | 0.6078 |

## Model Config

- **Model**: XGBClassifier
- **Draw class weight**: 1.4
- **Label encoding**: H=0, D=1, A=2
- **n_features**: 37
- **Training cutoff**: 2024-08-01 (seasons 2014/15 → 2023/24)
- **Test season**: 2024/25
