from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
async def check_health():
    """
    Health check endpoint to confirm the service is running.
    """
    return {"status": "ok", "message": "Document Classification Service is running."}
