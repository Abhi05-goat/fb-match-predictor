from fastapi import FastAPI
from backend.app.routes.health import router as health_router
from backend.app.routes.seasons import router as seasons_router
from backend.app.routes.teams import router as teams_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(seasons_router)
app.include_router(teams_router)

@app.get("/")
def root():
    return {"message":"Welcome to the Serie A analytics dashboard"}


