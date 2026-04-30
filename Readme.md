# Serie A Match Predictor

A machine learning project that predicts Serie A football match outcomes using historical match data, engineered team form features, Elo ratings, xG, PPDA, and a trained XGBoost classifier.

The project includes the full pipeline from raw data collection and preprocessing to model training and a FastAPI backend for serving predictions.

## Project Overview

This project predicts whether a Serie A fixture is likely to end in a:

- Home win
- Draw
- Away win

The model is trained on historical Serie A match data and uses football-specific features such as recent team form, attacking/defensive performance, Elo strength, expected goals, and pressing metrics.

## Features

- Scrapes and processes Serie A fixture data
- Combines historical seasons into a training dataset
- Engineers rolling last-5-match team statistics
- Adds xG and PPDA-based performance indicators
- Trains multiple classifiers, including XGBoost, Logistic Regression, and CatBoost
- Freezes the final XGBoost model for backend inference
- Provides a FastAPI backend structure for prediction endpoints
- Includes health and prediction routes for API development

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- CatBoost
- FastAPI
- Pydantic
- Uvicorn
- Git / GitHub

## Project Structure

```text
Fb Match Predictor/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       │   ├── health.py
│       │   └── predictions.py
│       ├── schemas/
│       │   └── prediction.py
│       └── ml/
│           └── model_loader.py
│
├── ML/
│   ├── Models/
│   │   ├── xgb_final.json
│   │   ├── feature_columns.json
│   │   ├── config.json
│   │   └── eval_report.md
│   ├── train/
│   └── test/
│
├── 1)Scrape_Raw_ELO_WhoScored_UnderStat/
├── 2)Extract_And_Preprocess_Seasons/
├── 3)Combine_Seasons/
├── 4)Split_Data_Train_Test/
├── 5)Preprocess_FeatureEngineer_Train_Test/
├── 6)Adding_XG_PPDA/
│
├── Combined.csv
├── Processed_Combined.csv
└── README.md
