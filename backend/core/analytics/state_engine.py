"""
v5.3 Sprint 2 - Deterministic Multi-Marker State Engine v1.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import (
    STATE_ENGINE_V1_VERSION,
    StateEngineStamp,
    SystemStateNode,
    canonical_json_sha256,
)


def _cluster_confidence(insight_graph: InsightGraphV1, system_id: str) -> float:
    confidence = getattr(insight_graph, "confidence", None)
    if confidence is None:
        return 0.0
    dump = confidence.model_dump() if hasattr(confidence, "model_dump") else confidence
    if not isinstance(dump, dict):
        return 0.0
    cluster_conf = dump.get("cluster_confidence", {})
    if not isinstance(cluster_conf, dict):
        return 0.0
    try:
        return float(cluster_conf.get(system_id, 0.0))
    except (TypeError, ValueError):
        return 0.0


def _confidence_bucket(value: float) -> str:
    if value >= 0.85:
        return "high"
    if value >= 0.60:
        return "moderate"
    if value >= 0.30:
        return "low"
    return "insufficient"


def _status(value: Any) -> str:
    s = str(value or "").strip().lower()
    if s in {"low", "normal", "high", "unknown"}:
        return s
    if s in {"optimal"}:
        return "normal"
    if s in {"elevated", "critical"}:
        return "high"
    return "unknown"


def build_state_engine_v1(
    insight_graph: InsightGraphV1,
) -> Tuple[List[SystemStateNode], StateEngineStamp]:
    cluster_summary = insight_graph.cluster_summary if isinstance(insight_graph.cluster_summary, dict) else {}
    cluster_items = cluster_summary.get("clusters", [])
    if not isinstance(cluster_items, list):
        cluster_items = []

    biomarker_by_id = {n.biomarker_id: n for n in insight_graph.biomarker_nodes}
    transition_by_id = {n.biomarker_id: n for n in insight_graph.state_transitions}
    relationship_items = [r for r in insight_graph.relationships if getattr(r, "triggered", False)]

    out: List[SystemStateNode] = []
    for cluster in sorted(cluster_items, key=lambda c: str((c or {}).get("cluster_id", ""))):
        if not isinstance(cluster, dict):
            continue
        system_id = str(cluster.get("cluster_id", "")).strip()
        if not system_id:
            continue
        biomarkers = cluster.get("biomarkers", [])
        if not isinstance(biomarkers, list):
            biomarkers = []
        biomarker_ids = sorted(str(b) for b in biomarkers if str(b).strip())

        high_count = 0
        low_count = 0
        normal_count = 0
        unknown_count = 0
        for biomarker_id in biomarker_ids:
            status = _status(getattr(biomarker_by_id.get(biomarker_id), "status", "unknown"))
            if status == "high":
                high_count += 1
            elif status == "low":
                low_count += 1
            elif status == "normal":
                normal_count += 1
            else:
                unknown_count += 1

        state_codes: List[str] = []
        abnormal_count = high_count + low_count
        if high_count == 0 and low_count == 0:
            state_codes.append("system_stable_normal")
        if abnormal_count == 1:
            state_codes.append("system_focal_derangement")
        if abnormal_count >= 2:
            state_codes.append("system_multi_marker_derangement")
        if high_count > 0 and low_count > 0:
            state_codes.append("system_bidirectional_instability")

        worsening = 0
        improving = 0
        for biomarker_id in biomarker_ids:
            transition = str(getattr(transition_by_id.get(biomarker_id), "transition", "")).strip().lower()
            if transition == "worsening":
                worsening += 1
            elif transition == "improving":
                improving += 1
        transition_summary_codes: List[str] = []
        if worsening >= 2:
            transition_summary_codes.append("system_trending_worse")
        if improving >= 2:
            transition_summary_codes.append("system_trending_improving")
        if worsening > 0 and improving > 0:
            transition_summary_codes.append("system_transition_volatility")

        rel_count = 0
        biomarker_set = set(biomarker_ids)
        for rel in relationship_items:
            rel_biomarkers = getattr(rel, "biomarkers", [])
            if not isinstance(rel_biomarkers, list):
                continue
            if any(str(b) in biomarker_set for b in rel_biomarkers):
                rel_count += 1
        rationale_codes: List[str] = []
        if rel_count >= 2:
            rationale_codes.append("system_relationship_density_high")
        elif rel_count == 0:
            rationale_codes.append("system_relationship_sparse")

        rationale_codes.extend(
            [
                f"high_count_{high_count}",
                f"low_count_{low_count}",
                f"normal_count_{normal_count}",
                f"unknown_count_{unknown_count}",
            ]
        )

        out.append(
            SystemStateNode(
                system_id=system_id,
                state_codes=sorted(set(state_codes)),
                rationale_codes=sorted(set(rationale_codes)),
                transition_summary_codes=sorted(set(transition_summary_codes)),
                confidence_bucket=_confidence_bucket(_cluster_confidence(insight_graph, system_id)),
            )
        )

    out.sort(key=lambda node: node.system_id)
    payload = {
        "version": STATE_ENGINE_V1_VERSION,
        "system_states": [n.model_dump() for n in out],
    }
    stamp = StateEngineStamp(
        state_engine_version=STATE_ENGINE_V1_VERSION,
        state_engine_hash=canonical_json_sha256(payload),
    )
    return out, stamp
