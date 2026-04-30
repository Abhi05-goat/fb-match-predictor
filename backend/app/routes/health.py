from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Health"]
)


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "SeriePredict API is running"
    }
