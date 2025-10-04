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

from core.models.biomarker import BiomarkerPanel
from core.models.user import User
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.events import stream_status
from core.dto.builders import build_analysis_result_dto
from core.canonical.normalize import normalize_panel
from services.storage.persistence_service import PersistenceService
from sqlalchemy.orm import Session
from config.database import get_db
from repositories.export_repository import ExportRepository
from repositories.analysis_repository import AnalysisRepository
from services.storage.export_service import ExportService

router = APIRouter()


class AnalysisStartRequest(BaseModel):
    """Request model for starting biomarker analysis."""
    biomarkers: Dict[str, Any]
    user: Dict[str, Any]


class AnalysisStartResponse(BaseModel):
    """Response model for analysis start."""
    analysis_id: str
    status: str
    message: str


@router.post("/analysis/start", response_model=AnalysisStartResponse)
async def start_analysis(request: AnalysisStartRequest, db: Session = Depends(get_db)):
    """
    Start a new biomarker analysis.
    
    Args:
        request: Analysis request with biomarkers and user data
        db: Database session
        
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
        
        # Sprint 9b - Persist analysis data
        if dto.status == "complete":
            try:
                persistence_service = PersistenceService(db)
                
                # Extract user_id from request (assuming it's in user data)
                user_id = request.user.get("user_id")
                if not user_id:
                    # Generate a temporary user_id if not provided
                    user_id = str(uuid4())
                
                # Save analysis
                analysis_uuid = persistence_service.save_analysis({
                    "analysis_id": analysis_id,
                    "status": dto.status,
                    "raw_biomarkers": request.biomarkers,
                    "questionnaire_data": request.user.get("questionnaire"),
                    "processing_time_seconds": None,  # Could be calculated
                    "analysis_version": "1.0.0",
                    "pipeline_version": "1.0.0"
                }, UUID(user_id))
                
                if analysis_uuid:
                    # Save results if analysis was persisted
                    results_data = {
                        "biomarkers": dto.biomarkers,
                        "clusters": dto.clusters,
                        "insights": dto.insights,
                        "overall_score": dto.overall_score,
                        "result_version": "1.0.0"
                    }
                    persistence_service.save_results(results_data, analysis_uuid)
                    
            except Exception as persistence_error:
                # Log persistence error but don't fail the request
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Persistence failed for analysis {analysis_id}: {str(persistence_error)}")
        
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


@router.get("/analysis/history")
async def get_analysis_history(user_id: str, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    """
    Get analysis history for a user.
    
    Args:
        user_id: User ID to get history for
        limit: Number of results to return (default: 10)
        offset: Number of results to skip (default: 0)
        db: Database session
        
    Returns:
        dict: Analysis history with pagination
    """
    try:
        persistence_service = PersistenceService(db)
        history = persistence_service.get_analysis_history(UUID(user_id), limit, offset)
        
        return {
            "history": history,
            "total": len(history),
            "page": (offset // limit) + 1,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis history: {str(e)}")


@router.get("/analysis/result")
async def get_analysis_result(analysis_id: str, db: Session = Depends(get_db)):
    """
    Get the final analysis result.
    
    Args:
        analysis_id: The analysis ID to get results for
        db: Database session
        
    Returns:
        dict: Analysis result with biomarkers, clusters and insights
    """
    try:
        persistence_service = PersistenceService(db)
        result = persistence_service.get_analysis_result(UUID(analysis_id))
        
        if not result:
            # Fallback to stub result if not found in database
            result = {
                "analysis_id": analysis_id,
                "biomarkers": [
                    {
                        "biomarker_name": "glucose",
                        "value": 95.0,
                        "unit": "mg/dL",
                        "score": 0.75,
                        "percentile": 65.0,
                        "status": "normal",
                        "reference_range": {"min": 70, "max": 100, "unit": "mg/dL"},
                        "interpretation": "Within normal range"
                    },
                    {
                        "biomarker_name": "total_cholesterol",
                        "value": 180.0,
                        "unit": "mg/dL",
                        "score": 0.85,
                        "percentile": 45.0,
                        "status": "optimal",
                        "reference_range": {"min": 150, "max": 200, "unit": "mg/dL"},
                        "interpretation": "Optimal cholesterol levels"
                    },
                    {
                        "biomarker_name": "hdl_cholesterol",
                        "value": 45.0,
                        "unit": "mg/dL",
                        "score": 0.60,
                        "percentile": 35.0,
                        "status": "low",
                        "reference_range": {"min": 40, "max": 60, "unit": "mg/dL"},
                        "interpretation": "HDL cholesterol is below optimal range"
                    }
                ],
                "clusters": [],
                "insights": [],
                "status": "complete",
                "created_at": datetime.now(UTC).isoformat(),
                "result_version": "1.0.0"
            }
        
        return build_analysis_result_dto(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")


@router.post("/analysis/export")
def export_analysis(request: ExportRequest, db: Session = Depends(get_db)):
    """
    Export analysis results in specified format.
    
    Args:
        request: Export request containing analysis_id and format
        db: Database session
        
    Returns:
        dict: Export information with download URL
    """
    fmt = request.format.upper()
    if fmt not in ("JSON", "CSV"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="unsupported_format")

    # Fetch analysis result and owning user_id
    arepo = AnalysisRepository(db)
    result = arepo.get_result_dto(request.analysis_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="analysis_not_found_or_forbidden")

    user_id = result.get("user_id")  # ensure AnalysisRepository includes user_id in DTO
    if not user_id:
        # fallback: fetch from analyses table if dto omits it
        user_id = arepo.get_user_id_for_analysis(request.analysis_id)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="analysis_not_found_or_forbidden")

    svc = ExportService()
    try:
        storage_path, size = svc.generate_and_upload(
            result_dto=result,
            user_id=UUID(user_id),
            analysis_id=request.analysis_id,
            fmt=fmt
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="export_failed") from e

    erepo = ExportRepository(db)
    exp = erepo.create_completed(
        analysis_id=request.analysis_id,
        user_id=UUID(user_id),
        format=fmt,
        storage_path=storage_path,
        file_size_bytes=size
    )

    url = svc.signed_url(storage_path)

    return {
        "export_id": str(exp.id),
        "download_url": url,
        "file_size_bytes": size
    }
