"""
Analysis routes for biomarker processing and result retrieval.
"""

import copy
import logging
import os
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import Response
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

class ExportRequest(BaseModel):
    analysis_id: UUID
    format: str = "json"

class AnalysisStartRequest(BaseModel):
    """Request model for starting biomarker analysis."""
    model_config = ConfigDict(extra="ignore")

    biomarkers: Dict[str, Any]
    user: Dict[str, Any]
    lab_origin: Optional[Dict[str, Any]] = None
    # Canonical name: questionnaire_data. FE historically sent `questionnaire`; accept both (CONTEXT-HARDENING-A).
    questionnaire_data: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias=AliasChoices("questionnaire_data", "questionnaire"),
    )

class AnalysisStartResponse(BaseModel):
    """Response model for analysis start."""
    analysis_id: str
    status: str
    message: str

from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.dto.builders import (
    analysis_route_biomarker_row,
    build_analysis_result_dto,
    extend_cluster_client_dict_from_hit,
)
from core.canonical.normalize import normalize_biomarkers_with_metadata, detect_canonical_collisions
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.errors import CanonicalCollisionError
from core.context import ContextFactory, ValidationError
from core.units.registry import apply_unit_normalisation, UnitConversionError, UNIT_REGISTRY_VERSION
from core.units.display_policy import build_display_policy_meta
from core.dependencies.analysis_auth import (
    require_analysis_submitter,
    require_analysis_submitter_if_db,
)
from core.dependencies.auth import CurrentUser
from core.profile_bridge import ensure_profile_for_auth_user
from app.analysis_payload import (
    apply_questionnaire_medication_representation_to_user,
    apply_questionnaire_objective_waist_to_user,
    build_context_factory_payload,
    normalize_analysis_user_dict,
)
from config.database import get_db_optional
from app.analysis_pdf_export import build_summary_pdf_bytes
from app.billing_entitlement import enforce_new_analysis_entitlement
from services.storage.persistence_service import PersistenceService, CLIENT_RESULT_SHAPE_V1
from repositories import AnalysisRepository, AnalysisResultRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory cache for the current process (also persisted when DATABASE_URL is set)
_analysis_results: Dict[str, Dict[str, Any]] = {}


def _generate_analysis_id() -> str:
    """UUIDv4 string only — matches ORM Analysis.id (PostgreSQL UUID)."""
    return str(uuid4())


@router.post("/start", response_model=AnalysisStartResponse)
async def start_analysis(
    request: AnalysisStartRequest,
    auth_user: CurrentUser = Depends(require_analysis_submitter),
    db: Optional[Session] = Depends(get_db_optional),
):
    """
    Start a new biomarker analysis.
    
    Args:
        request: Analysis request with biomarkers and user data
        
    Returns:
        AnalysisStartResponse: Contains the analysis ID
    """
    try:
        if db is not None:
            enforce_new_analysis_entitlement(db, auth_user)

        # Generate unique analysis ID
        analysis_id = _generate_analysis_id()
        
        normalized_user = normalize_analysis_user_dict(request.user)
        questionnaire_for_run = request.questionnaire_data
        apply_questionnaire_objective_waist_to_user(normalized_user, questionnaire_for_run)
        apply_questionnaire_medication_representation_to_user(normalized_user, questionnaire_for_run)

        # Trace incoming payload (exclude large questionnaire bodies from key-only trace)
        print("[TRACE] Incoming payload keys:", list(request.model_dump().keys()))
        print("[TRACE] Biomarker count:", len(request.biomarkers))
        print("[TRACE] Route received biomarkers:", list(request.biomarkers.keys()))
        print("[TRACE] Questionnaire present:", questionnaire_for_run is not None)

        # Create ContextFactory and validate payload (expects `questionnaire` key + canonical user fields)
        context_factory = ContextFactory()
        context_payload = build_context_factory_payload(
            biomarkers=request.biomarkers,
            user=normalized_user,
            questionnaire=questionnaire_for_run,
        )
        try:
            context = context_factory.create_context(context_payload, analysis_id)
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
        try:
            normalized = normalize_biomarkers_with_metadata(request.biomarkers)
        except CanonicalCollisionError:
            collisions = detect_canonical_collisions(request.biomarkers)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_type": "canonical_collision",
                    "collisions": collisions,
                },
            )

        # LC-S8D Mode A: preserve pre-arbitration upload rows for uploaded-panel fidelity.
        upload_panel_observations = {
            k: copy.deepcopy(v)
            for k, v in normalized.items()
            if k != UNIT_NORMALISATION_META_KEY
        }

        # KB-HBA1C-GOV1: single Layer B HbA1c id (hba1c) before unit normalisation.
        normalized = arbitrate_hba1c_layer_b_input(normalized)

        # Sprint 1: Convert to base units at ingestion (Layer A). Deterministic; rejects unknown units.
        try:
            normalized = apply_unit_normalisation(normalized)
        except UnitConversionError as e:
            detail = str(e)
            if e.biomarker_id:
                detail = f"{detail} (biomarker={e.biomarker_id}, from_unit={e.from_unit}, expected_base_unit={e.expected_base_unit})"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unit conversion failed: {detail}"
            )
        
        # Sprint 5: Set unit-normalisation meta so orchestrator.run() can enforce invariant
        normalized[UNIT_NORMALISATION_META_KEY] = {
            "unit_normalised": True,
            "unit_registry_version": UNIT_REGISTRY_VERSION,
        }

        # HTTP entry: insight narrative (insights[]) LLM gating is resolved inside InsightSynthesizer via
        # core.insights.narrative_runtime_policy.resolve_narrative_llm_allow_llm with allow_llm=None.
        # Production defaults stay off live network LLM unless HEALTHIQ_NARRATIVE_LLM and
        # HEALTHIQ_ENABLE_LLM are both enabled (double opt-in; BE-S1B). Golden/scripts pass allow_llm explicitly.
        orchestrator = AnalysisOrchestrator()

        # Run the complete pipeline: scoring → clustering → insights
        dto = orchestrator.run(
            normalized,
            normalized_user,
            assume_canonical=True,
            questionnaire_data=questionnaire_for_run,
        )
        dto = dto.model_copy(update={"analysis_id": analysis_id})

        # Store result in memory
        lab_origin_meta = request.lab_origin or {
            "lab_provider_id": "unknown",
            "lab_provider_name": None,
            "detection_method": "unknown",
            "detection_confidence": 0.0,
            "raw_evidence": None,
        }
        meta = dict(dto.meta or {})
        meta["lab_origin"] = lab_origin_meta
        meta["display_unit_policy"] = build_display_policy_meta()
        meta["upload_panel_observations"] = upload_panel_observations
        stored = {
            "analysis_id": dto.analysis_id,
            "meta": meta,
            "replay_manifest": getattr(dto, "replay_manifest", None),
            "derived_markers": dto.derived_markers,
            "biomarkers": [analysis_route_biomarker_row(b) for b in dto.biomarkers],
            "clusters": [
                extend_cluster_client_dict_from_hit(
                    {
                    "cluster_id": c.cluster_id,
                    "name": c.name,
                    "category": getattr(c, "category", "other"),
                    "biomarkers": c.biomarkers,
                    "description": c.description,
                    "severity": c.severity,
                    "confidence": c.confidence,
                    "recommendations": getattr(c, "recommendations", [])
                    },
                    c,
                )
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
            "unmapped_biomarkers": dto.unmapped_biomarkers,
            "status": dto.status,
            "created_at": dto.created_at,
            "overall_score": dto.overall_score,
            "primary_driver_system_id": getattr(dto, "primary_driver_system_id", ""),
            "system_capacity_scores": getattr(dto, "system_capacity_scores", {}),
            "burden_hash": getattr(dto, "burden_hash", ""),
            "risk_assessment": {},
            "recommendations": [],
            "result_version": "1.0.0",
            "interpretation_display_layer_v1": (
                dto.interpretation_display_layer_v1.model_dump()
                if getattr(dto, "interpretation_display_layer_v1", None) is not None
                else None
            ),
            "narrative_report_v1": (
                dto.narrative_report_v1.model_dump()
                if getattr(dto, "narrative_report_v1", None) is not None
                else None
            ),
            "consumer_domain_scores": (
                [x.model_dump() for x in dto.consumer_domain_scores]
                if getattr(dto, "consumer_domain_scores", None) is not None
                else None
            ),
        }
        _analysis_results[analysis_id] = stored

        if db is not None:
            try:
                owner_uuid = ensure_profile_for_auth_user(db, auth_user)
                PersistenceService(db, enable_fallback=False).save_live_analysis_after_run(
                    owner_user_id=owner_uuid,
                    analysis_id=UUID(analysis_id),
                    client_result=stored,
                    raw_biomarkers=request.biomarkers,
                    questionnaire_data=request.questionnaire_data,
                )
            except Exception as exc:
                logger.exception("Failed to persist analysis for user %s", auth_user.id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Analysis completed but persistence failed",
                ) from exc
        else:
            if os.getenv("HEALTHIQ_MODE", "").lower() == "test":
                logger.warning(
                    "DATABASE_URL not set — skipping persistence (test mode only)"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="DATABASE_URL is not configured; cannot persist analysis",
                )
        
        return AnalysisStartResponse(
            analysis_id=analysis_id,
            status="completed",
            message="Analysis completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return AnalysisStartResponse(
            analysis_id=analysis_id,
            status="error",
            message=f"Analysis failed: {str(e)}"
        )


def _raw_result_payload_for_analysis_id(
    analysis_id: str,
    db: Optional[Session],
    auth_user: Optional[CurrentUser],
) -> Dict[str, Any]:
    """
    Resolve stored client-result shape: in-process cache, or DB snapshot (authenticated owner only).
    When db is None, only the in-process cache is consulted (unit tests / no DATABASE_URL).
    """
    if db is None:
        cached = _analysis_results.get(analysis_id)
        if not cached:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return cached

    if auth_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        analysis_uuid = UUID(analysis_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid analysis_id") from exc

    owner_uuid = UUID(auth_user.id)
    analysis_repo = AnalysisRepository(db)
    row = analysis_repo.get_by_id(analysis_uuid)
    if row is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if row.user_id != owner_uuid:
        raise HTTPException(status_code=403, detail="Not allowed to access this analysis")

    cached = _analysis_results.get(analysis_id)
    if cached:
        return cached

    result_repo = AnalysisResultRepository(db)
    result_orm = result_repo.get_by_analysis_id(analysis_uuid)
    if result_orm is None or not result_orm.processing_metadata:
        raise HTTPException(status_code=404, detail="Analysis result not found")

    stored = result_orm.processing_metadata.get(CLIENT_RESULT_SHAPE_V1)
    if not isinstance(stored, dict):
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return stored


@router.get("/result")
async def get_analysis_result(
    analysis_id: str,
    db: Optional[Session] = Depends(get_db_optional),
    auth_user: Optional[CurrentUser] = Depends(require_analysis_submitter_if_db),
):
    """
    Get the final analysis result.
    
    Args:
        analysis_id: The analysis ID to get results for
        
    Returns:
        dict: Analysis result with biomarkers, clusters and insights
    """
    try:
        raw = _raw_result_payload_for_analysis_id(analysis_id, db, auth_user)
        return build_analysis_result_dto(raw)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")


@router.get("/export/pdf")
async def export_analysis_summary_pdf(
    analysis_id: str,
    db: Optional[Session] = Depends(get_db_optional),
    auth_user: Optional[CurrentUser] = Depends(require_analysis_submitter_if_db),
):
    """
    Download a one-page presentable PDF summary (retail copy only; not the full clinician report).
    """
    try:
        raw = _raw_result_payload_for_analysis_id(analysis_id, db, auth_user)
        dto = build_analysis_result_dto(raw)
        if auth_user and auth_user.email:
            user_display = auth_user.email
        else:
            user_display = "User"
        pdf_bytes = build_summary_pdf_bytes(dto, user_display=user_display)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in analysis_id)[:32]
        filename = f"healthiq-summary-{safe or 'export'}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("PDF export failed for analysis_id=%s", analysis_id)
        raise HTTPException(
            status_code=500, detail=f"Failed to build PDF export: {str(e)}"
        ) from e


@router.get("/history")
async def get_analysis_history(
    limit: int = 10,
    offset: int = 0,
    auth_user: CurrentUser = Depends(require_analysis_submitter),
    db: Optional[Session] = Depends(get_db_optional),
):
    """Paginated analysis history for the authenticated user (owner-scoped)."""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="History requires database persistence",
        )
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be non-negative")

    try:
        owner_uuid = ensure_profile_for_auth_user(db, auth_user)
        svc = PersistenceService(db, enable_fallback=False)
        history = svc.get_analysis_history(owner_uuid, limit=limit, offset=offset)
        total = svc.count_analyses_for_user(owner_uuid)
        page = offset // limit + 1
        return {
            "history": history,
            "total": total,
            "page": page,
            "limit": limit,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to load analysis history for user %s", auth_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load analysis history",
        ) from exc


@router.get("/events", deprecated=True, include_in_schema=True)
async def analysis_events_removed(analysis_id: Optional[str] = None):
    """
    Legacy path: fake SSE progress was removed (R-2A).

    The analysis pipeline runs synchronously inside POST /api/analysis/start, which
    returns when processing is complete. Use GET /api/analysis/result?analysis_id=...
    to load the final payload (suitable for polling if the client starts before
    a result is ready in other integration modes).
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail={
            "error": "sse_progress_not_available",
            "message": (
                "Server-Sent Events are not used for analysis progress. "
                "Call POST /api/analysis/start; on success, poll GET /api/analysis/result "
                "with the returned analysis_id for the result payload."
            ),
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
