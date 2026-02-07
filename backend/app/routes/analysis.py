"""
Analysis routes for biomarker processing and SSE streaming.
"""

import asyncio
import uuid
from datetime import datetime, UTC
from typing import Dict, Any
from uuid import UUID, uuid4

# For ULID generation (fallback to uuid4 if ulid not available)
try:
    from ulid import ULID
    def generate_analysis_id() -> str:
        return str(ULID())
except ImportError:
    def generate_analysis_id() -> str:
        return str(uuid.uuid4())

from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

class ExportRequest(BaseModel):
    analysis_id: UUID
    format: str = "json"

class AnalysisStartRequest(BaseModel):
    """Request model for starting biomarker analysis."""
    biomarkers: Dict[str, Any]
    user: Dict[str, Any]

class AnalysisStartResponse(BaseModel):
    """Response model for analysis start."""
    analysis_id: str
    status: str
    message: str

from core.models.biomarker import BiomarkerPanel
from core.models.user import User
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.events import stream_status
from core.dto.builders import build_analysis_result_dto
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.context import ContextFactory, ValidationError

router = APIRouter()

# In-memory storage for analysis results (replaces database persistence)
_analysis_results: Dict[str, Dict[str, Any]] = {}


@router.post("/start", response_model=AnalysisStartResponse)
async def start_analysis(request: AnalysisStartRequest):
    """
    Start a new biomarker analysis.
    
    Args:
        request: Analysis request with biomarkers and user data
        
    Returns:
        AnalysisStartResponse: Contains the analysis ID
    """
    try:
        # Generate unique analysis ID
        analysis_id = generate_analysis_id()
        
        # Trace incoming payload
        data = request.dict()
        print("[TRACE] Incoming payload keys:", data.keys())
        print("[TRACE] Biomarker count:", len(data.get("biomarkers", {})))
        print("[TRACE] Route received biomarkers:", list(data.get("biomarkers", {}).keys()))
        
        # Create ContextFactory and validate payload
        context_factory = ContextFactory()
        try:
            context = context_factory.create_context(data, analysis_id)
            print(f"[TRACE] Created AnalysisContext with {len(context.biomarkers)} biomarkers, user={context.user.user_id}")
        except ValidationError as e:
            print(f"[ERROR] ContextFactory validation failed: {str(e)}")
            return AnalysisStartResponse(
                analysis_id=analysis_id,
                status="error",
                message=f"Validation failed: {str(e)}"
            )
        
        # Normalize incoming raw biomarkers to canonical form, preserving reference_range metadata
        # This ensures lab-provided ranges are not lost before orchestrator processing
        normalized = normalize_biomarkers_with_metadata(request.biomarkers)
        
        # Create orchestrator and run analysis
        orchestrator = AnalysisOrchestrator()
        
        # Run the complete pipeline: scoring → clustering → insights
        dto = orchestrator.run(normalized, request.user, assume_canonical=True)
        
        # Store result in memory (replaces database persistence)
        _analysis_results[analysis_id] = {
            "analysis_id": dto.analysis_id,
            "biomarkers": [
                {
                    "biomarker_name": b.biomarker_name,
                    "value": b.value,
                    "unit": b.unit,
                    "score": b.score,
                    "percentile": b.percentile,
                    "status": b.status,
                    "reference_range": {
                        "min": b.reference_range.get("min") if b.reference_range else None,
                        "max": b.reference_range.get("max") if b.reference_range else None,
                        "unit": b.reference_range.get("unit", b.unit) if b.reference_range else b.unit,
                        "source": b.reference_range.get("source", "lab") if b.reference_range else "lab"
                    } if b.reference_range else {
                        "min": None,
                        "max": None,
                        "unit": b.unit,
                        "source": "lab"
                    },
                    "interpretation": b.interpretation
                }
                for b in dto.biomarkers
            ],
            "clusters": [
                {
                    "cluster_id": c.cluster_id,
                    "name": c.name,
                    "category": getattr(c, "category", "other"),
                    "biomarkers": c.biomarkers,
                    "description": c.description,
                    "severity": c.severity,
                    "confidence": c.confidence,
                    "recommendations": getattr(c, "recommendations", [])
                }
                for c in dto.clusters
            ],
            "insights": [
                {
                    "id": i.insight_id,
                    "category": i.category,
                    "title": i.title,
                    "summary": getattr(i, "summary", i.title),
                    "description": i.description,
                    "confidence": i.confidence,
                    "severity": i.severity,
                    "recommendations": i.recommendations,
                    "biomarkers_involved": i.biomarkers
                }
                for i in dto.insights
            ],
            "status": dto.status,
            "created_at": dto.created_at,
            "overall_score": dto.overall_score,
            "risk_assessment": {},
            "recommendations": [],
            "result_version": "1.0.0"
        }
        
        return AnalysisStartResponse(
            analysis_id=analysis_id,
            status="completed",
            message="Analysis completed successfully"
        )
        
    except Exception as e:
        return AnalysisStartResponse(
            analysis_id=generate_analysis_id(),
            status="error",
            message=f"Analysis failed: {str(e)}"
        )


@router.get("/result")
async def get_analysis_result(analysis_id: str):
    """
    Get the final analysis result.
    
    Args:
        analysis_id: The analysis ID to get results for
        
    Returns:
        dict: Analysis result with biomarkers, clusters and insights
    """
    try:
        # Get result from in-memory storage
        result = _analysis_results.get(analysis_id)
        
        if not result:
            # Return error result if not found
            return {
                "analysis_id": analysis_id,
                "biomarkers": [],
                "clusters": [],
                "insights": [],
                "status": "error",
                "created_at": datetime.now(UTC).isoformat(),
                "overall_score": 0.0,
                "risk_assessment": {},
                "recommendations": [],
                "result_version": "1.0.0",
                "error": "Analysis not found"
            }
        
        return build_analysis_result_dto(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")


@router.get("/events")
async def stream_status(analysis_id: str):
    """
    Stream simple analysis progress events for the frontend.
    Ensures SSE stays open long enough and closes gracefully.
    """
    async def event_generator():
        # Announce start
        yield "event: status\ndata: started\n\n"
        await asyncio.sleep(1)
        # Announce completion
        yield "event: status\ndata: completed\n\n"
        # Allow time for browser to process
        await asyncio.sleep(0.1)
        # Explicit close event
        yield "event: close\ndata: done\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "http://localhost:3000",
        },
    )


@router.get("/fixture")
def load_fixture_analysis():
    """
    Load sample analysis data from fixture for testing and development.
    Returns in-memory JSON data without database dependencies.
    """
    from tests.fixtures.sample_analysis import SAMPLE_ANALYSIS
    return SAMPLE_ANALYSIS
