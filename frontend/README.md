# SeriePredict Streamlit Frontend

Interactive Streamlit dashboard for the FastAPI analytics backend.

## Run

Start the backend from the project root:

```powershell
uvicorn backend.app.main:app --reload
```

Start the frontend from the project root:

```powershell
streamlit run frontend/streamlit_app.py
```

The app calls:

- `GET /seasons`
- `GET /seasons/{season}/teams`
- `GET /seasons/{season}/teams/{team_name}/summary`
