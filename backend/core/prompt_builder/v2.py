"""
Prompt Builder v2 - Deterministic JSON prompt assembly.

Sprint 17: Compute-only implementation (not wired to runtime).
Assembles strict JSON prompts from AnalysisContext for LLM processing.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, UTC

from core.models.context import AnalysisContext


def build_prompt_v2(context: AnalysisContext) -> Dict[str, Any]:
    """
    Build deterministic JSON prompt from AnalysisContext.
    
    Args:
        context: AnalysisContext with user, biomarkers, questionnaire, etc.
        
    Returns:
        Strict JSON dict with structure:
        {
            "meta": {"result_version": "2.0", "timestamp": "..."},
            "user": {"age": int, "sex": "male|female|other"},
            "biomarkers": [... canonical rows incl. lab ranges ...],
            "completeness": {"score": float, "missing": [ids...]},
            "clusters": [{"id": str, "score": float, "band": "green|amber|red"}],
            "red_flags": [{"id": str, "reason": str}],
            "insight_stubs": [{"id": str, "reasoning_inputs": [ids...]}],
            "policy": {"rules": [...], "max_fields": 32}
        }
    """
    # Extract user demographics
    user = context.user
    user_data = {
        "age": user.age if user.age is not None else 0,
        "sex": user.gender if user.gender else "other"
    }
    
    # Normalize sex to allowed values
    if user_data["sex"] not in ["male", "female", "other"]:
        user_data["sex"] = "other"
    
    # Extract biomarkers with lab ranges (lab-range-first)
    biomarkers_list = []
    biomarker_ids = []
    
    for bm_name, bm_value in context.biomarker_panel.biomarkers.items():
        biomarker_ids.append(bm_name)
        
        bm_dict = {
            "id": bm_name,
            "value": bm_value.value,
            "unit": bm_value.unit or ""
        }
        
        # Include lab reference range if available (lab-range-first)
        if bm_value.reference_range:
            ref_range = bm_value.reference_range
            bm_dict["lab_range"] = {
                "min": ref_range.get("min"),
                "max": ref_range.get("max"),
                "unit": ref_range.get("unit", bm_value.unit),
                "source": ref_range.get("source", "lab")
            }
        else:
            bm_dict["lab_range"] = None
        
        biomarkers_list.append(bm_dict)
    
    # Calculate completeness (simplified - can be enhanced)
    # For now, use a simple heuristic: count present vs expected
    # Expected: ~20-30 common biomarkers
    expected_count = 25
    present_count = len(biomarker_ids)
    completeness_score = min(1.0, present_count / expected_count) if expected_count > 0 else 0.0
    
    # Missing biomarkers (simplified - would need SSOT to determine expected)
    missing_biomarkers = []  # Would be populated from SSOT in full implementation
    
    completeness = {
        "score": round(completeness_score, 2),
        "missing": missing_biomarkers
    }
    
    # Extract clusters if present in context (check analysis_parameters for v2 clusters)
    clusters = []
    if context.analysis_parameters:
        # Check if cluster v2 results are present
        cluster_results = context.analysis_parameters.get("clusters_v2", [])
        if cluster_results:
            for cluster in cluster_results:
                clusters.append({
                    "id": cluster.get("id", ""),
                    "score": cluster.get("score", 0),
                    "band": cluster.get("band", "green")
                })
    
    # Extract red flags (simplified - would check biomarker statuses)
    red_flags = []
    for bm_name, bm_value in context.biomarker_panel.biomarkers.items():
        # Check if biomarker has critical status
        # This is simplified - full implementation would check status/flag
        if hasattr(bm_value, 'status') and bm_value.status in ['critical', 'high']:
            red_flags.append({
                "id": bm_name,
                "reason": f"{bm_name} value {bm_value.value} {bm_value.unit} is {bm_value.status}"
            })
    
    # Generate insight stubs (simplified - would use insight registry)
    insight_stubs = []
    # For now, create basic stubs based on available biomarkers
    if "glucose" in biomarker_ids and "hba1c" in biomarker_ids:
        insight_stubs.append({
            "id": "metabolic_health",
            "reasoning_inputs": ["glucose", "hba1c"]
        })
    if "total_cholesterol" in biomarker_ids and "ldl_cholesterol" in biomarker_ids:
        insight_stubs.append({
            "id": "cardiovascular_risk",
            "reasoning_inputs": ["total_cholesterol", "ldl_cholesterol"]
        })
    
    # Policy rules
    policy = {
        "rules": [
            "no diagnosis",
            "no numeric invention",
            "cite sources only if known"
        ],
        "max_fields": 32
    }
    
    # Assemble prompt
    prompt = {
        "meta": {
            "result_version": "2.0",
            "timestamp": datetime.now(UTC).isoformat()
        },
        "user": user_data,
        "biomarkers": biomarkers_list,
        "completeness": completeness,
        "clusters": clusters,
        "red_flags": red_flags,
        "insight_stubs": insight_stubs,
        "policy": policy
    }
    
    return prompt

