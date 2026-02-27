"""
Sprint 8 - Confidence Model Builder (Layer B only).

Deterministic confidence from cluster schema, available biomarkers, and optional criticality.
No probabilistic logic. No medical heuristics.
"""

from typing import Dict, List, Any, Optional, Set

from core.contracts.confidence_model_v1 import ConfidenceModelV1, CONFIDENCE_MODEL_V1_VERSION


def build_confidence_model_v1(
    available_biomarkers: Set[str],
    cluster_results: Optional[Dict[str, Any]] = None,
    criticality_result: Optional[Dict[str, Any]] = None,
    derived_markers: Optional[Dict[str, Any]] = None,
) -> ConfidenceModelV1:
    """
    Build ConfidenceModel_v1 from Layer B outputs.

    Args:
        available_biomarkers: Set of canonical biomarker IDs present (normalized).
        cluster_results: Clustering result {clusters: [...]}; optional.
        criticality_result: From evaluate_criticality(); optional.
        derived_markers: {registry_version, derived}; optional.

    Returns:
        ConfidenceModelV1 instance (deterministic)
    """
    try:
        from core.analytics.cluster_schema import load_cluster_schema, compute_cluster_status
    except ImportError:
        return _empty_model(derived_markers)

    schema = load_cluster_schema()
    clusters_def = schema.clusters

    # Biomarker confidence: 1.0 if present and valid, 0.0 if required but missing
    all_required: Set[str] = set()
    for cdef in clusters_def.values():
        all_required.update(cdef.required)

    biomarker_confidence: Dict[str, float] = {}
    for bid in available_biomarkers:
        biomarker_confidence[bid] = 1.0
    for bid in all_required:
        if bid not in biomarker_confidence:
            biomarker_confidence[bid] = 0.0

    # Cluster confidence: proportion of required markers present
    cluster_confidence: Dict[str, float] = {}
    missing_required_clusters: List[str] = []
    missing_required_biomarkers: Set[str] = set()

    for cluster_id, cdef in sorted(clusters_def.items()):
        status = compute_cluster_status(cdef, available_biomarkers)
        req_total = len(cdef.required)
        req_missing = status.get("required_missing", set())

        if req_total == 0:
            cluster_confidence[cluster_id] = 1.0
        else:
            present = req_total - len(req_missing)
            cluster_confidence[cluster_id] = round(present / req_total, 4)

        if req_missing:
            missing_required_clusters.append(cluster_id)
            missing_required_biomarkers.update(req_missing)

    # Deterministic ordering
    missing_required_biomarkers_list = sorted(missing_required_biomarkers)
    missing_required_clusters_list = sorted(missing_required_clusters)

    # System confidence: equal-weighted average of cluster_confidence
    if cluster_confidence:
        system_confidence = round(
            sum(cluster_confidence.values()) / len(cluster_confidence),
            4,
        )
    else:
        system_confidence = 0.0

    # Schema version refs
    ratio_version = ""
    if derived_markers:
        ratio_version = str(derived_markers.get("registry_version", ""))
    if not ratio_version:
        try:
            from core.analytics.ratio_registry import RatioRegistry
            ratio_version = str(RatioRegistry.version)
        except ImportError:
            pass

    return ConfidenceModelV1(
        model_version=CONFIDENCE_MODEL_V1_VERSION,
        system_confidence=system_confidence,
        cluster_confidence=dict(sorted(cluster_confidence.items())),
        biomarker_confidence=dict(sorted(biomarker_confidence.items())),
        missing_required_biomarkers=missing_required_biomarkers_list,
        missing_required_clusters=missing_required_clusters_list,
        cluster_schema_version=schema.version,
        cluster_schema_hash=schema.schema_hash,
        ratio_registry_version=ratio_version,
    )


def _empty_model(derived_markers: Optional[Dict[str, Any]]) -> ConfidenceModelV1:
    """Return minimal model when cluster schema unavailable."""
    ratio_version = ""
    if derived_markers:
        ratio_version = str(derived_markers.get("registry_version", ""))
    if not ratio_version:
        try:
            from core.analytics.ratio_registry import RatioRegistry
            ratio_version = str(RatioRegistry.version)
        except ImportError:
            pass
    return ConfidenceModelV1(
        model_version=CONFIDENCE_MODEL_V1_VERSION,
        system_confidence=0.0,
        cluster_confidence={},
        biomarker_confidence={},
        missing_required_biomarkers=[],
        missing_required_clusters=[],
        cluster_schema_version="",
        cluster_schema_hash="",
        ratio_registry_version=ratio_version,
    )
