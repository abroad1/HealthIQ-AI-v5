"""
v5.3 Sprint 5 - OutcomeCalibrationLayer_v1 deterministic engine.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from core.analytics.calibration_registry import load_calibration_registry
from core.contracts.calibration_layer_v1 import (
    CALIBRATION_LAYER_V1_VERSION,
    CalibrationItem,
    CalibrationStamp,
    canonical_json_sha256,
)
from core.contracts.insight_graph_v1 import InsightGraphV1


def _state_map(insight_graph: InsightGraphV1) -> Dict[str, Dict[str, Set[str]]]:
    out: Dict[str, Dict[str, Set[str]]] = {}
    for node in insight_graph.system_states:
        out[node.system_id] = {
            "state_codes": set(node.state_codes),
            "transition_summary_codes": set(node.transition_summary_codes),
        }
    return out


def _transition_codes(insight_graph: InsightGraphV1) -> Set[str]:
    return {str(node.transition) for node in insight_graph.state_transitions}


def _precedence_codes(insight_graph: InsightGraphV1) -> Set[str]:
    out: Set[str] = set()
    precedence = insight_graph.precedence_output
    if precedence is None:
        return out
    if precedence.primary_driver_system_id:
        out.add(f"primary_driver:{precedence.primary_driver_system_id}")
    for edge in precedence.dominant_edges:
        out.add(f"dominant_edge:{edge.from_system_id}>{edge.to_system_id}")
    for code in precedence.conflicts_resolved:
        out.add(f"precedence_conflict:{code}")
    for code in precedence.rationale_codes:
        out.add(f"precedence_rationale:{code}")
    return out


def _causal_codes(insight_graph: InsightGraphV1) -> Set[str]:
    out: Set[str] = set()
    for edge in insight_graph.causal_edges:
        out.add(f"causal_edge:{edge.edge_id}")
        out.add(f"causal_edge_type:{edge.edge_type}")
        out.add(f"causal_path:{edge.from_system_id}>{edge.to_system_id}")
        for code in edge.rationale_codes:
            out.add(f"causal_rationale:{code}")
    return out


def _rule_matches(
    rule_match: Dict[str, List[str]],
    system_id: str,
    state_codes: Set[str],
    transition_summary_codes: Set[str],
    transition_codes: Set[str],
    precedence_codes: Set[str],
    causal_codes: Set[str],
) -> bool:
    required_system_ids = set(rule_match.get("required_system_ids", []))
    if required_system_ids and system_id not in required_system_ids:
        return False

    required_state_codes = set(rule_match.get("required_state_codes", []))
    if required_state_codes and not required_state_codes.issubset(state_codes):
        return False

    required_transition_codes = set(rule_match.get("required_transition_codes", []))
    if required_transition_codes:
        system_and_global = set(transition_summary_codes) | set(transition_codes)
        if not required_transition_codes.issubset(system_and_global):
            return False

    required_precedence_codes = set(rule_match.get("required_precedence_codes", []))
    if required_precedence_codes and not required_precedence_codes.issubset(precedence_codes):
        return False

    required_causal_codes = set(rule_match.get("required_causal_codes", []))
    if required_causal_codes and not required_causal_codes.issubset(causal_codes):
        return False

    return True


def build_calibration_layer_v1(insight_graph: InsightGraphV1) -> Tuple[List[CalibrationItem], CalibrationStamp]:
    registry = load_calibration_registry()
    states = _state_map(insight_graph)
    transition_codes = _transition_codes(insight_graph)
    precedence_codes = _precedence_codes(insight_graph)
    causal_codes = _causal_codes(insight_graph)

    items: List[CalibrationItem] = []
    for system_id in sorted(states.keys()):
        state_codes = states[system_id]["state_codes"]
        transition_summary_codes = states[system_id]["transition_summary_codes"]
        matched_rule = None
        for rule in registry.rules:
            if _rule_matches(
                rule_match=rule.match,
                system_id=system_id,
                state_codes=state_codes,
                transition_summary_codes=transition_summary_codes,
                transition_codes=transition_codes,
                precedence_codes=precedence_codes,
                causal_codes=causal_codes,
            ):
                matched_rule = rule
                break

        if matched_rule is None:
            items.append(
                CalibrationItem(
                    system_id=system_id,
                    priority_tier="p3",
                    urgency_band="routine",
                    action_intensity="info",
                    stability_flag="stable",
                    explanation_codes=["calibration:default"],
                    applied_rule_ids=[],
                )
            )
            continue

        outputs = matched_rule.outputs
        items.append(
            CalibrationItem(
                system_id=system_id,
                priority_tier=outputs["priority_tier"],
                urgency_band=outputs["urgency_band"],
                action_intensity=outputs["action_intensity"],
                stability_flag=outputs["stability_flag"],
                explanation_codes=sorted(set(outputs.get("explanation_codes", []))),
                applied_rule_ids=[matched_rule.rule_id],
            )
        )

    items.sort(key=lambda i: i.system_id)
    payload = {
        "version": CALIBRATION_LAYER_V1_VERSION,
        "calibration_items": [item.model_dump() for item in items],
    }
    stamp = CalibrationStamp(
        calibration_version=CALIBRATION_LAYER_V1_VERSION,
        calibration_hash=canonical_json_sha256(payload),
    )
    return items, stamp
