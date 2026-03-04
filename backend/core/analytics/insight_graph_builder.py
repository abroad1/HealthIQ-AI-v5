"""
Sprint 7 - InsightGraph Builder.

Sole assembler of InsightGraph_v1. Layer B computes; builder translates.
Input: orchestrator result structures. Output: InsightGraphV1 (JSON-serialisable).
"""

import os
from typing import Dict, List, Any, Optional

from core.contracts.insight_graph_v1 import (
    InsightGraphV1,
    BiomarkerNode,
    INSIGHTGRAPH_V1_VERSION,
    LayerCFeatureBundleV1,
    MetabolicAgeFeatureV1,
    HeartFeatureV1,
    InflammationFeatureV1,
    FatigueFeatureV1,
    DetoxFeatureV1,
)
from core.analytics.primitives import frontend_status_from_value_and_range
from core.analytics.confidence_builder import build_confidence_model_v1
from core.analytics.relationship_registry import (
    evaluate_relationships,
    load_relationship_registry,
)
from core.analytics.biomarker_context_builder import build_biomarker_context_v1


def _as_float(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        inner = value.get("value", value.get("measurement"))
        if isinstance(inner, (int, float)):
            return float(inner)
    return None


def _severity_from_count(count: int) -> str:
    if count >= 4:
        return "critical"
    if count >= 3:
        return "high"
    if count >= 2:
        return "moderate"
    if count >= 1:
        return "mild"
    return "normal"


def _build_layer_c_features(filtered_biomarkers: Dict[str, Any], derived_ratios_meta: Optional[Dict[str, Any]]) -> LayerCFeatureBundleV1:
    ratios = {}
    if isinstance(derived_ratios_meta, dict) and isinstance(derived_ratios_meta.get("ratios"), dict):
        ratios = derived_ratios_meta.get("ratios", {})

    def ratio(name: str) -> Optional[float]:
        if name in filtered_biomarkers:
            return _as_float(filtered_biomarkers.get(name))
        entry = ratios.get(name)
        if isinstance(entry, dict):
            return _as_float(entry.get("value"))
        return None

    glucose = _as_float(filtered_biomarkers.get("glucose"))
    insulin = _as_float(filtered_biomarkers.get("insulin"))
    hba1c = _as_float(filtered_biomarkers.get("hba1c"))
    age = _as_float(filtered_biomarkers.get("age")) or 0.0
    bmi = _as_float(filtered_biomarkers.get("bmi"))
    tc_hdl_ratio = ratio("tc_hdl_ratio")
    tg_hdl_ratio = ratio("tg_hdl_ratio")
    ldl_hdl_ratio = ratio("ldl_hdl_ratio")
    nlr = ratio("nlr")
    homa_ir = (glucose * insulin) / 405.0 if (glucose and insulin and glucose > 0 and insulin > 0) else 0.0
    metabolic_flags: List[str] = []
    if homa_ir > 2.5:
        metabolic_flags.append("insulin_resistance")
    if hba1c is not None and hba1c > 5.7:
        metabolic_flags.append("elevated_hba1c")
    if tc_hdl_ratio is not None and tc_hdl_ratio > 4.0:
        metabolic_flags.append("elevated_tc_hdl_ratio")
    if tg_hdl_ratio is not None and tg_hdl_ratio > 2.0:
        metabolic_flags.append("elevated_tg_hdl_ratio")
    if bmi is not None and bmi > 25:
        metabolic_flags.append("elevated_bmi")
    metabolic_age = max(age + (2 * len(metabolic_flags)), age)

    heart_flags: List[str] = []
    if ldl_hdl_ratio is not None and ldl_hdl_ratio > 3.5:
        heart_flags.append("elevated_ldl_hdl_ratio")
    if tc_hdl_ratio is not None and tc_hdl_ratio > 4.0:
        heart_flags.append("elevated_tc_hdl_ratio")
    if tg_hdl_ratio is not None and tg_hdl_ratio > 2.0:
        heart_flags.append("elevated_tg_hdl_ratio")

    crp = _as_float(filtered_biomarkers.get("crp"))
    ferritin = _as_float(filtered_biomarkers.get("ferritin"))
    wbc = _as_float(filtered_biomarkers.get("white_blood_cells"))
    inflammation_flags: List[str] = []
    if crp is not None and crp > 1.0:
        inflammation_flags.append("elevated_crp")
    if nlr is not None and nlr > 2.0:
        inflammation_flags.append("elevated_nlr")
    if ferritin is not None and ferritin > 300:
        inflammation_flags.append("elevated_ferritin")
    if wbc is not None and wbc > 10:
        inflammation_flags.append("elevated_wbc")

    fatigue_causes: List[str] = []
    if ferritin is not None and ferritin < 15:
        fatigue_causes.append("iron_deficiency")
    if _as_float(filtered_biomarkers.get("tsh")) is not None and _as_float(filtered_biomarkers.get("tsh")) > 4.5:
        fatigue_causes.append("hypothyroidism")
    if _as_float(filtered_biomarkers.get("b12")) is not None and _as_float(filtered_biomarkers.get("b12")) < 200:
        fatigue_causes.append("vitamin_deficiency")
    if crp is not None and crp > 1.0:
        fatigue_causes.append("inflammatory_fatigue")

    creatinine = _as_float(filtered_biomarkers.get("creatinine"))
    egfr = _as_float(filtered_biomarkers.get("egfr"))
    egfr_source = "measured" if egfr is not None else "unknown"
    if egfr is None and creatinine and creatinine > 0 and age > 0:
        egfr = max(0.0, min(200.0, 175.0 * (creatinine ** -1.154) * (age ** -0.203)))
        egfr_source = "estimated"
    urea_creatinine_ratio = ratio("urea_creatinine_ratio") or ratio("bun_creatinine_ratio")
    detox_flags: List[str] = []
    if _as_float(filtered_biomarkers.get("alt")) is not None and _as_float(filtered_biomarkers.get("alt")) > 40:
        detox_flags.append("elevated_alt")
    if creatinine is not None and creatinine > 1.2:
        detox_flags.append("elevated_creatinine")
    if egfr is not None and egfr < 60:
        detox_flags.append("reduced_egfr")
    if urea_creatinine_ratio is not None and urea_creatinine_ratio > 20:
        detox_flags.append("elevated_urea_creatinine_ratio")

    return LayerCFeatureBundleV1(
        metabolic_age=MetabolicAgeFeatureV1(
            metabolic_age=round(metabolic_age, 1),
            age_delta_years=round(metabolic_age - age, 1),
            homa_ir=round(homa_ir, 2),
            severity=_severity_from_count(len(metabolic_flags)),
            confidence=min(0.95, 0.7 + (0.04 * len(metabolic_flags))),
            risk_flags=sorted(set(metabolic_flags)),
            recommendations=["Focus on metabolic recovery"] if metabolic_flags else ["Maintain current metabolic health"],
        ),
        heart_insight=HeartFeatureV1(
            heart_resilience_score=max(0.0, 100.0 - (12.0 * len(heart_flags))),
            severity=_severity_from_count(len(heart_flags)),
            confidence=min(0.95, 0.75 + (0.04 * len(heart_flags))),
            risk_factors=sorted(set(heart_flags)),
            ldl_hdl_ratio=round(ldl_hdl_ratio, 2) if ldl_hdl_ratio is not None else None,
            tc_hdl_ratio=round(tc_hdl_ratio, 2) if tc_hdl_ratio is not None else None,
            tg_hdl_ratio=round(tg_hdl_ratio, 2) if tg_hdl_ratio is not None else None,
            recommendations=["Support cardiovascular resilience"] if heart_flags else ["Maintain cardiovascular baseline"],
        ),
        inflammation=InflammationFeatureV1(
            inflammation_burden_score=min(100.0, 20.0 * len(inflammation_flags)),
            severity=_severity_from_count(len(inflammation_flags)),
            confidence=min(0.95, 0.8 + (0.03 * len(inflammation_flags))),
            risk_factors=sorted(set(inflammation_flags)),
            nlr=round(nlr, 2) if nlr is not None else None,
            recommendations=["Reduce inflammatory burden"] if inflammation_flags else ["Maintain low inflammatory status"],
        ),
        fatigue_root_cause=FatigueFeatureV1(
            severity=("critical" if len(fatigue_causes) >= 3 else "high" if len(fatigue_causes) >= 2 else "moderate" if fatigue_causes else "normal"),
            confidence=min(0.95, 0.7 + (0.04 * len(fatigue_causes))),
            root_causes=sorted(set(fatigue_causes)),
            iron_status="deficient" if "iron_deficiency" in fatigue_causes else "normal",
            thyroid_status="hypothyroid" if "hypothyroidism" in fatigue_causes else "normal",
            vitamin_status="deficient" if "vitamin_deficiency" in fatigue_causes else "normal",
            inflammation_status="moderate_inflammation" if "inflammatory_fatigue" in fatigue_causes else "normal",
            cortisol_status="unknown",
            recommendations=["Address fatigue root causes"] if fatigue_causes else ["Maintain anti-fatigue baseline"],
        ),
        detox_filtration=DetoxFeatureV1(
            detox_filtration_score=max(0.0, 100.0 - (15.0 * len(detox_flags))),
            liver_score=max(0.0, 100.0 - (12.0 * len([f for f in detox_flags if f.startswith("elevated_")]))),
            kidney_score=max(0.0, 100.0 - (15.0 * len([f for f in detox_flags if f in {"reduced_egfr", "elevated_creatinine", "elevated_urea_creatinine_ratio"}]))),
            severity=_severity_from_count(len(detox_flags)),
            confidence=min(0.95, 0.75 + (0.04 * len(detox_flags))),
            risk_factors=sorted(set(detox_flags)),
            egfr=round(egfr, 1) if egfr is not None else None,
            egfr_source=egfr_source,
            urea_creatinine_ratio=round(urea_creatinine_ratio, 2) if urea_creatinine_ratio is not None else None,
            recommendations=["Support detox and filtration resilience"] if detox_flags else ["Maintain detox/filtration baseline"],
        ),
    )


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

    def _to_relationship_status(status: Any) -> str:
        """Normalize frontend/legacy statuses into RelationshipRegistry vocabulary."""
        s = str(status or "").strip().lower()
        if s in {"low"}:
            return "low"
        if s in {"normal", "optimal"}:
            return "normal"
        if s in {"high", "elevated", "critical"}:
            return "high"
        return "unknown"

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

    # Safe marker views for RelationshipRegistry (status/score only, deterministic)
    panel_view = {
        v["name"]: {
            "status": _to_relationship_status(v.get("status")),
            "score": v.get("score"),
        }
        for v in seen.values()
    }
    derived_markers_view: Dict[str, Dict[str, Any]] = {}
    if derived_markers and isinstance(derived_markers.get("derived"), dict):
        for derived_id in sorted(derived_markers["derived"].keys()):
            marker = panel_view.get(derived_id, {})
            derived_markers_view[derived_id] = {
                "status": _to_relationship_status(marker.get("status")),
                "score": marker.get("score"),
            }

    # Sprint 8: Confidence model (deterministic, Layer B only)
    available = set(seen.keys())
    confidence_model = build_confidence_model_v1(
        available_biomarkers=available,
        cluster_results=clustering_result,
        criticality_result=criticality_result,
        derived_markers=derived_markers,
    )

    # Cluster summary
    clusters = clustering_result.get("clusters", [])
    cluster_summary = None
    try:
        from core.clustering.cluster_schema_loader import get_cluster_schema_version_stamp
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

    # Sprint 10: RelationshipRegistry evaluation (cluster-agnostic, deterministic)
    relationship_detections = []
    relationship_stamp = None
    mode = os.getenv("HEALTHIQ_MODE", "").strip().lower()
    fixture_mode = mode in {"fixture", "fixtures"}
    try:
        registry = load_relationship_registry()
    except (ImportError, FileNotFoundError, ValueError):
        # Determinism hardening: fail loudly in normal runtime.
        # Soft-fail allowed only for explicit fixture-only mode.
        if not fixture_mode:
            raise
        registry = None

    if registry is not None:
        relationship_stamp = registry.stamp
        relationship_detections = evaluate_relationships(
            panel_view=panel_view,
            derived_markers_view=derived_markers_view,
            registry=registry,
        )

    # Sprint 11: BiomarkerContext_v1 (safe explanatory context for Layer C)
    context_nodes, context_stamp = build_biomarker_context_v1(
        {
            "biomarker_nodes": [n.model_dump() for n in nodes],
            "confidence": confidence_model.model_dump() if hasattr(confidence_model, "model_dump") else {},
            "cluster_summary": cluster_summary or {},
            "relationships": [
                r.model_dump() if hasattr(r, "model_dump") else r for r in relationship_detections
            ],
        }
    )
    layer_c_features = _build_layer_c_features(
        filtered_biomarkers=filtered_biomarkers,
        derived_ratios_meta=derived_ratios_meta,
    )

    return InsightGraphV1(
        graph_version=INSIGHTGRAPH_V1_VERSION,
        analysis_id=analysis_id,
        lab_origin=lab_origin,
        unit_normalisation_meta=unit_normalisation_meta,
        derived_markers=derived_markers,
        cluster_summary=cluster_summary,
        criticality=criticality_result,
        confidence=confidence_model,
        relationship_registry_version=(
            relationship_stamp.relationship_registry_version if relationship_stamp else None
        ),
        relationship_registry_hash=(
            relationship_stamp.relationship_registry_hash if relationship_stamp else None
        ),
        relationships=relationship_detections,
        biomarker_context_version=context_stamp.biomarker_context_version,
        biomarker_context_hash=context_stamp.biomarker_context_hash,
        biomarker_context=context_nodes,
        layer_c_features=layer_c_features,
        biomarker_nodes=nodes,
        edges=[],
    )
