"""
DTO builders - transform internal objects into frontend-safe dictionaries.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, UTC

from core.analytics.report_compiler_v1 import compile_clinician_report_v1
from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.analytics.balanced_systems_presentation_v1 import compile_balanced_systems_v1
from core.units.display_fidelity_v1 import enrich_biomarker_row_display_fields
from core.models.biomarker import BiomarkerCluster, BiomarkerInsight
from core.models.results import AnalysisResult, AnalysisSummary, BiomarkerScore, ClusterHit
from core.models.insight import Insight, InsightSynthesisResult


def _coerce_intervention_annotations_v1(raw: Any) -> Optional[InterventionAnnotationsV1]:
    if raw is None:
        return None
    if isinstance(raw, InterventionAnnotationsV1):
        return raw
    if isinstance(raw, dict):
        try:
            return InterventionAnnotationsV1.model_validate(raw)
        except Exception:
            return None
    return None


def build_analysis_result_dto(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build frontend-safe analysis result DTO.
    
    Args:
        result: Raw analysis result data
        
    Returns:
        Frontend-safe dictionary
    """
    print("[TRACE] DTO biomarkers in result:", len(result.get("biomarkers", [])))
    meta = result.get("meta", {})
    meta = meta if isinstance(meta, dict) else {}
    insight_graph = meta.get("insight_graph", {})
    insight_graph = insight_graph if isinstance(insight_graph, dict) else {}
    report_v1 = insight_graph.get("report_v1", {})
    mh_snap = meta.get("medical_history_snapshot")
    mh_snap = mh_snap if isinstance(mh_snap, dict) else None
    ia_v1 = _coerce_intervention_annotations_v1(result.get("intervention_annotations_v1"))
    clinician_report = compile_clinician_report_v1(
        report_v1_payload=report_v1 if isinstance(report_v1, dict) else {},
        biomarker_rows=result.get("biomarkers", []) if isinstance(result.get("biomarkers"), list) else [],
        medical_history=mh_snap,
        intervention_annotations_v1=ia_v1,
    )
    meta_for_balanced = dict(meta)
    cds = result.get("consumer_domain_scores")
    if cds is not None:
        if hasattr(cds, "__iter__") and not isinstance(cds, (str, dict)):
            meta_for_balanced["consumer_domain_scores"] = [
                row.model_dump() if hasattr(row, "model_dump") else row for row in cds
            ]
        else:
            meta_for_balanced["consumer_domain_scores"] = cds
    balanced = compile_balanced_systems_v1(
        meta=meta_for_balanced,
        primary_driver_system_id=str(result.get("primary_driver_system_id", "") or ""),
    )

    return {
        "analysis_id": result.get("analysis_id", ""),
        "biomarkers": result.get("biomarkers", []),
        "clusters": result.get("clusters", []),
        "insights": result.get("insights", []),
        "status": result.get("status", "completed"),
        "created_at": result.get("created_at", datetime.now(UTC).isoformat()),
        "overall_score": result.get("overall_score"),
        "primary_driver_system_id": result.get("primary_driver_system_id", ""),
        "system_capacity_scores": result.get("system_capacity_scores", {}),
        "burden_hash": result.get("burden_hash", ""),
        "risk_assessment": result.get("risk_assessment", {}),
        "recommendations": result.get("recommendations", []),
        "result_version": result.get("result_version", "1.0.0"),
        "derived_markers": result.get("derived_markers"),
        "meta": meta,
        "clinician_report_v1": (
            clinician_report.model_dump() if clinician_report is not None else None
        ),
        "balanced_systems_v1": balanced,
        "replay_manifest": result.get("replay_manifest"),
        "interpretation_display_layer_v1": result.get("interpretation_display_layer_v1"),
        "narrative_report_v1": result.get("narrative_report_v1"),
        "consumer_domain_scores": result.get("consumer_domain_scores"),
        "intervention_annotations_v1": (
            ia_v1.model_dump() if ia_v1 is not None else None
        ),
    }


def build_biomarker_score_dto(score: BiomarkerScore) -> Dict[str, Any]:
    """
    Build frontend-safe biomarker score DTO.
    
    Args:
        score: BiomarkerScore object
        
    Returns:
        Frontend-safe dictionary
    """
    row: Dict[str, Any] = {
        "biomarker_name": score.biomarker_name,
        "value": score.value,
        "unit": score.unit,
        "score": score.score,
        "percentile": score.percentile,
        "status": score.status,
        "reference_range": score.reference_range,
        "interpretation": score.interpretation,
    }
    if score.biomarker_educational_explainer is not None:
        row["biomarker_educational_explainer"] = score.biomarker_educational_explainer.model_dump()
    if score.contribution_context is not None:
        row["contribution_context"] = score.contribution_context.model_dump()
    return row


def analysis_route_biomarker_row(b: BiomarkerScore) -> Dict[str, Any]:
    """Shape stored/API biomarker row from orchestrator DTO (includes B1A optional fields)."""
    row: Dict[str, Any] = {
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
            "source": b.reference_range.get("source", "lab") if b.reference_range else "lab",
        }
        if b.reference_range
        else {
            "min": None,
            "max": None,
            "unit": b.unit,
            "source": "lab",
        },
        "interpretation": b.interpretation,
    }
    if b.biomarker_educational_explainer is not None:
        row["biomarker_educational_explainer"] = b.biomarker_educational_explainer.model_dump()
    if b.contribution_context is not None:
        row["contribution_context"] = b.contribution_context.model_dump()
    return row


def analysis_route_biomarker_row_with_display(
    b: BiomarkerScore,
    *,
    upload_panel: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """API/stored biomarker row with LC-S8G display contract fields."""
    return enrich_biomarker_row_display_fields(
        analysis_route_biomarker_row(b),
        upload_panel=upload_panel,
    )


def extend_cluster_client_dict_from_hit(cluster_dict: Dict[str, Any], cluster: ClusterHit) -> Dict[str, Any]:
    """Merge B1A retail explainer fields onto a cluster client row when present."""
    out = dict(cluster_dict)
    sys_expl = getattr(cluster, "system_educational_explainer", None)
    if sys_expl is not None:
        out["system_educational_explainer"] = sys_expl.model_dump()
    return out


def build_biomarker_cluster_dto(cluster: BiomarkerCluster) -> Dict[str, Any]:
    """
    Build frontend-safe biomarker cluster DTO.
    
    Args:
        cluster: BiomarkerCluster object
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "cluster_id": cluster.cluster_id,
        "name": cluster.name,
        "biomarkers": cluster.biomarkers,
        "description": cluster.description,
        "severity": cluster.severity,
        "confidence": cluster.confidence
    }


def build_biomarker_insight_dto(insight: BiomarkerInsight) -> Dict[str, Any]:
    """
    Build frontend-safe biomarker insight DTO.
    
    Args:
        insight: BiomarkerInsight object
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "id": insight.insight_id,
        "title": insight.title,
        "description": insight.description,
        "biomarkers": insight.biomarkers,
        "category": insight.category,
        "severity": insight.severity,
        "confidence": insight.confidence,
        "recommendations": insight.recommendations
    }


def build_analysis_summary_dto(summary: AnalysisSummary) -> Dict[str, Any]:
    """
    Build frontend-safe analysis summary DTO.
    
    Args:
        summary: AnalysisSummary object
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "analysis_id": summary.analysis_id,
        "user_id": summary.user_id,
        "status": summary.status,
        "total_biomarkers": summary.total_biomarkers,
        "clusters_found": summary.clusters_found,
        "insights_generated": summary.insights_generated,
        "overall_score": summary.overall_score,
        "created_at": summary.created_at,
        "completed_at": summary.completed_at
    }


def build_biomarker_panel_dto(panel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build frontend-safe biomarker panel DTO.
    
    Args:
        panel_data: Raw biomarker panel data
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "biomarkers": panel_data.get("biomarkers", {}),
        "source": panel_data.get("source", ""),
        "version": panel_data.get("version", "1.0"),
        "created_at": panel_data.get("created_at"),
        "total_count": len(panel_data.get("biomarkers", {}))
    }


def build_user_dto(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build frontend-safe user DTO.
    
    Args:
        user_data: Raw user data
        
    Returns:
        Frontend-safe dictionary (excluding sensitive information)
    """
    return {
        "user_id": user_data.get("user_id", ""),
        "age": user_data.get("age"),
        "gender": user_data.get("gender"),
        "height": user_data.get("height"),
        "weight": user_data.get("weight"),
        "ethnicity": user_data.get("ethnicity"),
        "medical_history": user_data.get("medical_history", {}),
        "medications": user_data.get("medications", []),
        "supplements": user_data.get("supplements", []),
        "lifestyle_factors": user_data.get("lifestyle_factors", {}),
        # Note: email is excluded for privacy
        "created_at": user_data.get("created_at")
    }


def build_insight_dto(insight) -> Dict[str, Any]:
    """
    Build frontend-safe insight DTO.
    
    Args:
        insight: Insight object, InsightResult, or dict with insight data
        
    Returns:
        Frontend-safe dictionary
    """
    # Handle InsightResult objects (new modular insights)
    if hasattr(insight, 'insight_id') and hasattr(insight, 'version'):
        return {
            "id": insight.insight_id,
            "version": insight.version,
            "manifest_id": insight.manifest_id,
            "category": getattr(insight, 'category', 'unknown'),
            "summary": getattr(insight, 'title', ''),
            "description": getattr(insight, 'description', ''),
            "evidence": insight.evidence or {},
            "drivers": insight.drivers or {},
            "confidence": insight.confidence or 0.0,
            "severity": insight.severity or "info",
            "recommendations": insight.recommendations or [],
            "biomarkers_involved": insight.biomarkers_involved or [],
            "lifestyle_factors": getattr(insight, 'lifestyle_factors', []),
            "latency_ms": insight.latency_ms or 0,
            "error_code": insight.error_code,
            "error_detail": insight.error_detail,
            "created_at": getattr(insight, 'created_at', '')
        }
    # Handle dicts
    elif isinstance(insight, dict):
        return {
            "id": insight.get("id", ""),
            "version": insight.get("version", "v1.0.0"),
            "manifest_id": insight.get("manifest_id", ""),
            "category": insight.get("category", ""),
            "summary": insight.get("summary", ""),
            "description": insight.get("description", ""),
            "evidence": insight.get("evidence", {}),
            "drivers": insight.get("drivers", {}),
            "confidence": insight.get("confidence", 0.0),
            "severity": insight.get("severity", "info"),
            "recommendations": insight.get("recommendations", []),
            "biomarkers_involved": insight.get("biomarkers_involved", []),
            "lifestyle_factors": insight.get("lifestyle_factors", []),
            "latency_ms": insight.get("latency_ms", 0),
            "error_code": insight.get("error_code"),
            "error_detail": insight.get("error_detail"),
            "created_at": insight.get("created_at", "")
        }
    else:
        # Legacy Insight object
        return {
            "id": getattr(insight, 'id', ''),
            "version": getattr(insight, 'version', 'v1.0.0'),
            "manifest_id": getattr(insight, 'manifest_id', ''),
            "category": getattr(insight, 'category', ''),
            "summary": getattr(insight, 'summary', ''),
            "description": getattr(insight, 'description', ''),
            "evidence": getattr(insight, 'evidence', {}),
            "drivers": getattr(insight, 'drivers', {}),
            "confidence": getattr(insight, 'confidence', 0.0),
            "severity": getattr(insight, 'severity', 'info'),
            "recommendations": getattr(insight, 'recommendations', []),
            "biomarkers_involved": getattr(insight, 'biomarkers_involved', []),
            "lifestyle_factors": getattr(insight, 'lifestyle_factors', []),
            "latency_ms": getattr(insight, 'latency_ms', 0),
            "error_code": getattr(insight, 'error_code'),
            "error_detail": getattr(insight, 'error_detail'),
            "created_at": getattr(insight, 'created_at', '')
        }


def build_insight_synthesis_result_dto(result: InsightSynthesisResult) -> Dict[str, Any]:
    """
    Build frontend-safe insight synthesis result DTO.
    
    Args:
        result: InsightSynthesisResult object
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "analysis_id": result.analysis_id,
        "insights": [build_insight_dto(insight) for insight in result.insights],
        "synthesis_summary": result.synthesis_summary,
        "total_insights": result.total_insights,
        "categories_covered": result.categories_covered,
        "overall_confidence": result.overall_confidence,
        "processing_time_ms": result.processing_time_ms,
        "created_at": result.created_at
    }


def build_error_dto(error_message: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
    """
    Build frontend-safe error DTO.
    
    Args:
        error_message: Error message
        error_code: Error code
        
    Returns:
        Frontend-safe error dictionary
    """
    return {
        "error": True,
        "error_code": error_code,
        "message": error_message,
        "timestamp": datetime.now(UTC).isoformat()
    }
