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

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from core.models.biomarker import BiomarkerPanel
from core.models.user import User
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.events import AnalysisEventStream
from core.dto.builders import build_analysis_result_dto

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
        
        # Create orchestrator and start analysis
        orchestrator = AnalysisOrchestrator()
        
        # Store analysis request (in production, this would be persisted)
        # For now, we'll just return the analysis ID
        # The actual processing happens via the SSE endpoint
        
        return AnalysisStartResponse(analysis_id=analysis_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")


@router.get("/analysis/events")
async def stream_analysis_events(analysis_id: str):
    """
    Stream analysis progress events via Server-Sent Events.
    
    Args:
        analysis_id: The analysis ID to stream events for
        
    Returns:
        StreamingResponse: SSE stream of analysis events
    """
    try:
        # Create event stream
        event_stream = AnalysisEventStream(analysis_id)
        
        return StreamingResponse(
            event_stream.generate_events(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stream events: {str(e)}")


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
