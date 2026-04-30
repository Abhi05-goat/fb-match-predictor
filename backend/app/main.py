from fastapi import FastAPI

from backend.app.routes.health import router as health_router
from backend.app.routes.predictions import router as predictions_router

app = FastAPI(
    title="SerieAPredict API",
    description="Backend API for Serie A match outcome predictions",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(predictions_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SeriePredict API",
        "docs": "/docs",
        "health": "/health"
    }
