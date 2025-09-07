"""
Analysis routes for biomarker processing and SSE streaming.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any

# For ULID generation (fallback to uuid4 if ulid not available)
try:
    from ulid import ULID
    def generate_analysis_id() -> str:
        return str(ULID())
except ImportError:
    def generate_analysis_id() -> str:
        return str(uuid.uuid4())

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from core.models.biomarker import BiomarkerPanel
from core.models.user import User
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.events import stream_status
from core.dto.builders import build_analysis_result_dto
from core.canonical.normalize import normalize_panel

router = APIRouter()


class AnalysisStartRequest(BaseModel):
    """Request model for starting biomarker analysis."""
    biomarkers: Dict[str, Any]
    user: Dict[str, Any]


class AnalysisStartResponse(BaseModel):
    """Response model for analysis start."""
    analysis_id: str


@router.post("/analysis/start", response_model=AnalysisStartResponse)
async def start_analysis(request: AnalysisStartRequest):
    """
    Start a new biomarker analysis.
    
    Args:
        request: Analysis request with biomarkers and user data
        
    Returns:
        AnalysisStartResponse: Contains the analysis ID
    """
    try:
        # Generate unique analysis ID (ULID or uuid4)
        analysis_id = generate_analysis_id()
        
        # normalize incoming raw biomarkers to canonical first
        normalized = normalize_panel(request.biomarkers)
        
        # Create orchestrator and start analysis
        orchestrator = AnalysisOrchestrator()
        
        # orchestrator expects canonical-only; we tell it we already normalized
        dto = orchestrator.run(normalized, request.user, assume_canonical=True)
        
        return AnalysisStartResponse(analysis_id=analysis_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")


@router.get("/analysis/events")
@router.get("/analysis/events/")  # allow trailing slash to avoid redirects
async def analysis_events(request: Request, analysis_id: str):
    async def event_gen():
        async for chunk in stream_status(analysis_id):
            # stop if client disconnected
            if await request.is_disconnected():
                break
            yield chunk
    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/analysis/result")
async def get_analysis_result(analysis_id: str):
    """
    Get the final analysis result.
    
    Args:
        analysis_id: The analysis ID to get results for
        
    Returns:
        dict: Analysis result with clusters and insights
    """
    try:
        # For now, return a stub result
        # In production, this would fetch from persistent storage
        result = {
            "analysis_id": analysis_id,
            "clusters": [],
            "insights": [],
            "status": "complete",
            "created_at": datetime.utcnow().isoformat(),
        }
        
        return build_analysis_result_dto(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")
