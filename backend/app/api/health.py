"""
Health check API endpoints.
"""
from fastapi import APIRouter
from datetime import datetime

from app.models.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    services = {
        "api": True,
        "embeddings": True,
        "vector_store": True,
        "llm": bool(settings.OPENAI_API_KEY)
    }
    
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow(),
        services=services
    )
