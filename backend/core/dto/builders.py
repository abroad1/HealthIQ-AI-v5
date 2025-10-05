"""
DTO builders - transform internal objects into frontend-safe dictionaries.
"""

from typing import Dict, Any, List
from datetime import datetime, UTC

from core.models.biomarker import BiomarkerCluster, BiomarkerInsight
from core.models.results import AnalysisResult, AnalysisSummary, BiomarkerScore
from core.models.insight import Insight, InsightSynthesisResult


def build_analysis_result_dto(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build frontend-safe analysis result DTO.
    
    Args:
        result: Raw analysis result data
        
    Returns:
        Frontend-safe dictionary
    """
    # Process insights to ensure proper DTO format
    insights = result.get("insights", [])
    processed_insights = []
    
    for insight in insights:
        if isinstance(insight, dict):
            # Already in dict format from orchestrator
            processed_insights.append(insight)
        else:
            # Convert using build_insight_dto
            processed_insights.append(build_insight_dto(insight))
    
    return {
        "analysis_id": result.get("analysis_id", ""),
        "biomarkers": result.get("biomarkers", []),
        "clusters": result.get("clusters", []),
        "insights": processed_insights,
        "status": result.get("status", "complete"),
        "created_at": result.get("created_at", datetime.now(UTC).isoformat()),
        "overall_score": result.get("overall_score"),
        "risk_assessment": result.get("risk_assessment", {}),
        "recommendations": result.get("recommendations", []),
        "result_version": result.get("result_version", "1.0.0"),
        "meta": {
            **result.get("meta", {}),
            "total_insights": result.get("total_insights", len(processed_insights)),
            "modular_insights_count": result.get("modular_insights_count", 0),
            "llm_insights_count": result.get("llm_insights_count", 0),
            "processing_time_ms": result.get("processing_time_ms", 0),
            "modular_processing_time_ms": result.get("modular_processing_time_ms", 0)
        }
    }


def build_biomarker_score_dto(score: BiomarkerScore) -> Dict[str, Any]:
    """
    Build frontend-safe biomarker score DTO.
    
    Args:
        score: BiomarkerScore object
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "biomarker_name": score.biomarker_name,
        "value": score.value,
        "unit": score.unit,
        "score": score.score,
        "percentile": score.percentile,
        "status": score.status,
        "reference_range": score.reference_range,
        "interpretation": score.interpretation
    }


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
        "insight_id": insight.insight_id,
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
