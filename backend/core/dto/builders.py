"""
DTO builders - transform internal objects into frontend-safe dictionaries.
"""

from typing import Dict, Any, List
from datetime import datetime

from core.models.biomarker import BiomarkerCluster, BiomarkerInsight
from core.models.results import AnalysisResult, AnalysisSummary


def build_analysis_result_dto(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build frontend-safe analysis result DTO.
    
    Args:
        result: Raw analysis result data
        
    Returns:
        Frontend-safe dictionary
    """
    return {
        "analysis_id": result.get("analysis_id", ""),
        "clusters": result.get("clusters", []),
        "insights": result.get("insights", []),
        "status": result.get("status", "unknown"),
        "created_at": result.get("created_at", datetime.utcnow().isoformat()),
        "overall_score": result.get("overall_score"),
        "risk_assessment": result.get("risk_assessment", {}),
        "recommendations": result.get("recommendations", [])
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
        "timestamp": datetime.utcnow().isoformat()
    }
