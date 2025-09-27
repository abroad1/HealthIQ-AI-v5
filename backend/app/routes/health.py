"""
Health check routes for the HealthIQ-AI v5 backend.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        dict: Status confirmation with timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }

