"""
Sprint 7 - InsightGraph Builder.

Sole assembler of InsightGraph_v1. Layer B computes; builder translates.
Input: orchestrator result structures. Output: InsightGraphV1 (JSON-serialisable).
"""

from typing import Dict, List, Any, Optional

from core.contracts.insight_graph_v1 import (
    InsightGraphV1,
    BiomarkerNode,
    INSIGHTGRAPH_V1_VERSION,
)
from core.analytics.primitives import frontend_status_from_value_and_range


def build_insight_graph_v1(
    analysis_id: str,
    scoring_result: Dict[str, Any],
    clustering_result: Dict[str, Any],
    criticality_result: Optional[Dict[str, Any]] = None,
    derived_ratios_meta: Optional[Dict[str, Any]] = None,
    input_reference_ranges: Optional[Dict[str, Any]] = None,
    filtered_biomarkers: Optional[Dict[str, Any]] = None,
    context: Any = None,
    lab_origin: Optional[Dict[str, Any]] = None,
    unit_normalisation_meta: Optional[Dict[str, Any]] = None,
) -> InsightGraphV1:
    """
    Build InsightGraph_v1 from orchestrator result structures.

    This is the ONLY place allowed to assemble the InsightGraph payload.
    Deterministic: biomarker_nodes sorted by biomarker_id.

    Args:
        analysis_id: Analysis identifier
        scoring_result: From score_biomarkers (health_system_scores with biomarker_scores)
        clustering_result: From cluster_biomarkers (clusters list)
        criticality_result: From evaluate_criticality()
        derived_ratios_meta: ratio_registry_version + ratios dict
        input_reference_ranges: Lab/SSOT reference ranges per biomarker
        filtered_biomarkers: Canonical biomarker values
        context: AnalysisContext for unit lookup
        lab_origin: Lab provider metadata (Sprint 2)
        unit_normalisation_meta: Unit normalisation metadata (Sprint 1)

    Returns:
        InsightGraphV1 instance
    """
    input_reference_ranges = input_reference_ranges or {}
    filtered_biomarkers = filtered_biomarkers or {}

    # Collect biomarker nodes: status + score only (PRD §4.7: no raw values/units/ranges)
    seen: Dict[str, Dict[str, Any]] = {}
    for system_name, system_score in scoring_result.get("health_system_scores", {}).items():
        for bs in system_score.get("biomarker_scores", []):
            name = bs.get("biomarker_name")
            if not name or name in seen:
                continue
            val = bs.get("value")
            if val is None:
                continue
            try:
                value_float = float(val)
            except (ValueError, TypeError):
                continue
            ref_range = input_reference_ranges.get(name)
            status = "unknown"
            if ref_range and isinstance(ref_range, dict):
                mn = ref_range.get("min")
                mx = ref_range.get("max")
                if isinstance(mn, (int, float)) and isinstance(mx, (int, float)):
                    status = frontend_status_from_value_and_range(value_float, float(mn), float(mx))
            score_val = bs.get("score")
            score_float = None
            if score_val is not None:
                try:
                    score_float = float(score_val)
                except (ValueError, TypeError):
                    pass
            seen[name] = {"name": name, "status": status, "score": score_float}

    # Add unscored biomarkers (status only, no score)
    for name, bm_data in filtered_biomarkers.items():
        if name in seen:
            continue
        if isinstance(bm_data, dict):
            val = bm_data.get("value", bm_data.get("measurement"))
        else:
            val = bm_data
        if val is None:
            continue
        try:
            value_float = float(val)
        except (ValueError, TypeError):
            continue
        ref_range = input_reference_ranges.get(name)
        status = "unknown"
        if ref_range and isinstance(ref_range, dict):
            mn, mx = ref_range.get("min"), ref_range.get("max")
            if isinstance(mn, (int, float)) and isinstance(mx, (int, float)):
                status = frontend_status_from_value_and_range(value_float, float(mn), float(mx))
        seen[name] = {"name": name, "status": status, "score": None}

    nodes = [
        BiomarkerNode(
            biomarker_id=v["name"],
            status=v["status"],
            score=v.get("score"),
        )
        for v in seen.values()
    ]
    nodes.sort(key=lambda n: n.biomarker_id)

    # Derived markers
    derived_markers = None
    if derived_ratios_meta:
        derived_markers = {
            "registry_version": derived_ratios_meta.get("ratio_registry_version"),
            "derived": derived_ratios_meta.get("ratios", {}),
        }

    # Cluster summary
    clusters = clustering_result.get("clusters", [])
    cluster_summary = None
    try:
        from core.analytics.cluster_schema import get_cluster_schema_version_stamp
        stamp = get_cluster_schema_version_stamp()
        cluster_summary = {
            "schema_version": stamp.get("cluster_schema_version"),
            "schema_hash": stamp.get("cluster_schema_hash"),
            "clusters": [
                {
                    "cluster_id": c.get("cluster_id", ""),
                    "name": c.get("name", ""),
                    "biomarkers": c.get("biomarkers", []),
                    "confidence": c.get("confidence", 0.0),
                    "severity": c.get("severity", "normal"),
                }
                for c in clusters
            ],
        }
    except (ImportError, FileNotFoundError, ValueError):
        cluster_summary = {
            "clusters": [
                {"cluster_id": c.get("cluster_id", ""), "name": c.get("name", ""), "biomarkers": c.get("biomarkers", []), "confidence": c.get("confidence", 0.0), "severity": c.get("severity", "normal")}
                for c in clusters
            ],
        }

    return InsightGraphV1(
        graph_version=INSIGHTGRAPH_V1_VERSION,
        analysis_id=analysis_id,
        lab_origin=lab_origin,
        unit_normalisation_meta=unit_normalisation_meta,
        derived_markers=derived_markers,
        cluster_summary=cluster_summary,
        criticality=criticality_result,
        biomarker_nodes=nodes,
        edges=[],
    )
