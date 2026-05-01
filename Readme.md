# 🏆 Serie A Analytics & Match Predictor

![Build Status](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

**Live Application:** [https://serieanalytics.streamlit.app/](https://serieanalytics.streamlit.app/)

A full-stack, end-to-end machine learning project designed to extract, analyze, and predict Serie A football match outcomes using historical fixture data and advanced football metrics.

The architecture separates concerns into a **FastAPI backend** handling data serving and ML model inferences, and a highly interactive **Streamlit frontend** providing a dynamic user dashboard with "Depth-upon-request" progressive data visualizations.

---

## 🌟 Feature Overview

- **End-to-End ETL Pipeline:** Scrapes, cleans, and merges raw historical data from multiple sources (ClubElo, WhoScored, UnderStat).
- **Advanced Feature Engineering:** Computes rolling averages, relative team forms, Elo rating differences, Expected Goals (xG), and Passes Allowed Per Defensive Action (PPDA).
- **Predictive ML Engine:** Uses an optimized XGBoost Multi-Class Classifier trained on 37 features to predict match probabilities (Home Win, Draw, Away Win).
- **Rule-Based AI Insights:** The frontend utilizes heuristic logic to automatically parse raw data and generate readable text insights regarding a team's pressing intensity and clinical finishing.
- **Dynamic Frontend Dashboard:** Features side-by-side N-1 season comparisons, Plotly-powered radar charts ("Team Profile Shape"), and native dynamic SVG crest injection.

---

## 🏗️ Architecture & Deployment

The application runs across two decoupled cloud environments:

1. **The Backend (Render):** A FastAPI app exposing RESTful endpoints (`/seasons`, `/teams/summary`, `/predictions`). It loads a frozen XGBoost model artifact into memory and serves predictions. 
2. **The Frontend (Streamlit Cloud):** Connects to the backend via REST, caching data and rendering high-level dashboard metrics, falling back to deep analytic expanders for raw statistics.

---

## 🚀 Upcoming Roadmap (Project Scope)

While Phase 1 (UI Overhaul & Historical Analysis) is complete, the project is actively scaling toward the following functionality:

### Real-Time Match Predictor
Refining the ETL pipeline to automatically process and append the live 2025/26 Serie A season. The frontend will feature a "Predictor Arena" tab where users can select upcoming fixtures and securely ping the XGBoost model for live win/loss probabilities.

### Player-Wise Profile Glyphs
Expanding the data scraper to drill down into player-specific statistics (e.g., progressive passes, successful tackles), mapping the top 4 players of every season onto interactive radar glyphs.

### Predictive Gamification Engine
Integrating a dedicated Database infrastructure (Supabase / PostgreSQL) to allow users to authenticate, submit their own predictions against the ML model, and climb a global community leaderboard.

---

## 💻 Tech Stack
- **Data/ML:** Python, Pandas, NumPy, Scikit-learn, XGBoost, CatBoost
- **Backend:** FastAPI, Pydantic, Uvicorn (Deployed on Render)
- **Frontend:** Streamlit, Plotly, HTML/CSS injections (Deployed on Streamlit Cloud) 

---
*Created by [Abhi05-goat](https://github.com/Abhi05-goat)*
