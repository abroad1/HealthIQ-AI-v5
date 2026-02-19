"""
v5.3 Sprint 1 - Deterministic StateTransitionEngine v1.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_transition_v1 import (
    STATE_TRANSITION_V1_VERSION,
    BiomarkerTransitionNode,
    StateTransitionStamp,
    canonical_json_sha256,
)


def _status(value: object) -> str:
    s = str(value or "").strip().lower()
    if s in {"low", "normal", "high", "unknown"}:
        return s
    if s in {"optimal"}:
        return "normal"
    if s in {"elevated", "critical"}:
        return "high"
    return "unknown"


def _context_band(graph: InsightGraphV1, biomarker_id: str) -> Optional[str]:
    for node in graph.biomarker_context:
        if getattr(node, "biomarker_id", "") != biomarker_id:
            continue
        for code in getattr(node, "reason_codes", []) or []:
            if code == "score_low_band":
                return "low_band"
            if code == "score_mid_band":
                return "mid_band"
            if code == "score_high_band":
                return "high_band"
    return None


def _score_band(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    try:
        val = float(score)
    except (TypeError, ValueError):
        return None
    if 0.0 <= val <= 1.0:
        val = val * 100.0
    if val < 40.0:
        return "low_band"
    if val <= 70.0:
        return "mid_band"
    return "high_band"


def _band_rank(band: Optional[str]) -> int:
    return {"low_band": 0, "mid_band": 1, "high_band": 2}.get(str(band), -1)


def _band_direction(from_status: str, from_band: Optional[str], to_band: Optional[str]) -> Optional[str]:
    if from_band is None or to_band is None or from_band == to_band:
        return None
    fr, tr = _band_rank(from_band), _band_rank(to_band)
    if fr < 0 or tr < 0:
        return None
    if from_status in {"normal", "low"}:
        return "better" if tr > fr else "worse"
    if from_status == "high":
        return "better" if tr < fr else "worse"
    return None


def _volatile_from_priors(biomarker_id: str, priors: List[InsightGraphV1]) -> bool:
    if len(priors) < 2:
        return False
    status_seq: List[str] = []
    for graph in priors:
        by_id = {n.biomarker_id: n for n in graph.biomarker_nodes}
        node = by_id.get(biomarker_id)
        if node is None:
            continue
        status_seq.append(_status(node.status))
    if len(status_seq) < 2:
        return False
    for i in range(1, len(status_seq)):
        prev_s, cur_s = status_seq[i - 1], status_seq[i]
        if {prev_s, cur_s} == {"low", "high"}:
            return True
    return False


def build_state_transition_v1(
    current_insight_graph: InsightGraphV1,
    prior_insight_graphs: List[InsightGraphV1],
) -> Tuple[StateTransitionStamp, List[BiomarkerTransitionNode]]:
    """
    Build deterministic v1 longitudinal transitions from current + prior snapshots.

    v1 compares current status to most recent prior snapshot and optionally marks
    volatile when >=2 priors exhibit low<->high oscillation.
    """
    current_map: Dict[str, object] = {n.biomarker_id: n for n in current_insight_graph.biomarker_nodes}
    prior_recent_map: Dict[str, object] = {}
    if prior_insight_graphs:
        prior_recent_map = {n.biomarker_id: n for n in prior_insight_graphs[0].biomarker_nodes}

    transitions: List[BiomarkerTransitionNode] = []
    for biomarker_id in sorted(current_map.keys()):
        current_node = current_map[biomarker_id]
        current_status = _status(getattr(current_node, "status", "unknown"))
        current_score = getattr(current_node, "score", None)

        prior_node = prior_recent_map.get(biomarker_id)
        if prior_node is None:
            transitions.append(
                BiomarkerTransitionNode(
                    biomarker_id=biomarker_id,
                    from_status="unknown",
                    to_status=current_status,
                    transition="insufficient_history",
                    evidence_codes=["insufficient_points"],
                )
            )
            continue

        from_status = _status(getattr(prior_node, "status", "unknown"))
        from_score = getattr(prior_node, "score", None)
        evidence_codes: List[str] = []

        if _volatile_from_priors(biomarker_id, prior_insight_graphs):
            transition = "volatile"
            evidence_codes.append("status_change")
        elif from_status == "unknown" or current_status == "unknown":
            transition = "unknown"
            evidence_codes.append("status_unknown")
        elif from_status == "normal" and current_status == "normal":
            transition = "stable_normal"
        elif from_status == current_status and from_status in {"low", "high"}:
            transition = "stable_abnormal"
        elif from_status in {"low", "high"} and current_status == "normal":
            transition = "improving"
            evidence_codes.append("status_change")
        elif from_status == "normal" and current_status in {"low", "high"}:
            transition = "worsening"
            evidence_codes.append("status_change")
        else:
            transition = "unknown"
            evidence_codes.append("status_change")

        from_band = _context_band(prior_insight_graphs[0], biomarker_id) if prior_insight_graphs else None
        if from_band is None:
            from_band = _score_band(from_score)
        to_band = _context_band(current_insight_graph, biomarker_id)
        if to_band is None:
            to_band = _score_band(current_score)
        direction = _band_direction(from_status, from_band, to_band)

        if direction == "better":
            evidence_codes.append("score_band_up")
            if transition in {"stable_normal", "stable_abnormal"}:
                transition = "improving"
        elif direction == "worse":
            evidence_codes.append("score_band_down")
            if transition in {"stable_normal", "stable_abnormal"}:
                transition = "worsening"

        transitions.append(
            BiomarkerTransitionNode(
                biomarker_id=biomarker_id,
                from_status=from_status,
                to_status=current_status,
                transition=transition,  # type: ignore[arg-type]
                evidence_codes=sorted(set(evidence_codes)),
            )
        )

    transitions.sort(key=lambda n: n.biomarker_id)
    stamp_payload = {
        "state_transition_version": STATE_TRANSITION_V1_VERSION,
        "transitions": [t.model_dump() for t in transitions],
    }
    stamp = StateTransitionStamp(
        state_transition_version=STATE_TRANSITION_V1_VERSION,
        state_transition_hash=canonical_json_sha256(stamp_payload),
    )
    return stamp, transitions
