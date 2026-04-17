from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.routers import health, classify
from src.model_loader import classifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load Model on Startup
    logger.info("Initializing Document Classification System...")
    classifier.load()
    yield
    # Cleanup on Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Document Classification API",
    description="API for classifying text files into categories.",
    version="1.0.0",
    lifespan=lifespan
)

# Exception handler to catch any unhandled errors gracefully
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )

# Include Routers
app.include_router(health.router)
app.include_router(classify.router)

# To run locally: uvicorn src.main:app --reload
