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
Machine Learning Pipeline
The project follows this workflow:

Collect raw Serie A match data from multiple football data sources.
Extract and preprocess season-level fixture data.
Combine multiple seasons into one dataset.
Split the data into train and test sets.
Engineer rolling team form features.
Add xG and PPDA-based metrics.
Train and compare classification models.
Freeze the final XGBoost model for backend use.
Serve predictions through a FastAPI backend.
Model
The final model is an XGBoost multi-class classifier trained to predict match outcomes.

The frozen model artifact is stored at:

text

ML/Models/xgb_final.json
Supporting model files:

text

ML/Models/feature_columns.json
ML/Models/config.json
ML/Models/eval_report.md
Backend API
The backend is built with FastAPI.

Run the API locally
bash

uvicorn backend.app.main:app --reload
Then open:

text

http://127.0.0.1:8000
API documentation:

text

http://127.0.0.1:8000/docs
Available Endpoints
Root
http

GET /
Returns a welcome response for the API.

Health Check
http

GET /health
Returns the current API health status.

Upcoming Predictions
http

GET /predictions/upcoming
Returns upcoming fixture predictions.

At the current stage, this endpoint is being prepared for full model-backed inference using the frozen XGBoost classifier.

Example API Response
json

{
  "season": "2025-26",
  "matchday": 31,
  "fixtures": [
    {
      "home_team": "Inter",
      "away_team": "Milan",
      "kickoff": "2026-04-12 18:00",
      "predicted_result": "Home",
      "probabilities": {
        "home": 0.52,
        "draw": 0.24,
        "away": 0.24
      }
    }
  ]
}
Current Status
The machine learning pipeline and final XGBoost model artifact are in place.

The backend currently includes:

FastAPI application setup
Health check route
Prediction route scaffold
Pydantic response schemas
Model loader module prepared for backend inference integration
Next development steps:

Load the frozen XGBoost model inside the backend
Connect feature inputs to the prediction endpoint
Generate predictions for upcoming Serie A fixtures
Add frontend/dashboard support
Improve API documentation and deployment readiness
Purpose
This project was built to explore practical sports analytics, machine learning classification, feature engineering, and backend API development using real football data.

It is designed as an end-to-end portfolio project covering:

Data scraping
Data cleaning
Feature engineering
Model training
Model evaluation
Backend API development
Deployment preparation
Author
Abhi
GitHub: Abhi05-goat
