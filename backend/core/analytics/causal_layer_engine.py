"""
v5.3 Sprint 4 - Deterministic CausalLayer_v1 engine.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from core.analytics.causal_layer_registry import load_causal_layer_registry
from core.contracts.causal_layer_v1 import (
    CAUSAL_LAYER_V1_VERSION,
    CausalEdgeNode,
    CausalLayerStamp,
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


def _global_transition_codes(insight_graph: InsightGraphV1) -> Set[str]:
    return {str(node.transition) for node in insight_graph.state_transitions}


def _precedence_codes(insight_graph: InsightGraphV1) -> Dict[str, Set[str]]:
    output = insight_graph.precedence_output
    if output is None:
        return {
            "primary_driver": set(),
            "dominant_edges": set(),
            "conflicts": set(),
            "rationale": set(),
        }
    dominant_edges = {
        f"{edge.from_system_id}>{edge.to_system_id}"
        for edge in (output.dominant_edges or [])
    }
    return {
        "primary_driver": {str(output.primary_driver_system_id or "")},
        "dominant_edges": dominant_edges,
        "conflicts": set(output.conflicts_resolved or []),
        "rationale": set(output.rationale_codes or []),
    }


def _condition_met(
    condition: str,
    from_system_id: str,
    to_system_id: str,
    system_codes: Dict[str, Dict[str, Set[str]]],
    transition_codes: Set[str],
    precedence_codes: Dict[str, Set[str]],
) -> bool:
    parts = condition.split(":")
    if not parts:
        return False
    key = parts[0].strip()

    from_state_codes = system_codes.get(from_system_id, {}).get("state_codes", set())
    to_state_codes = system_codes.get(to_system_id, {}).get("state_codes", set())
    from_transition_codes = system_codes.get(from_system_id, {}).get("transition_summary_codes", set())
    to_transition_codes = system_codes.get(to_system_id, {}).get("transition_summary_codes", set())

    if key == "requires_state":
        if len(parts) < 2:
            return False
        code = parts[1].strip()
        return code in from_state_codes or code in to_state_codes

    if key == "requires_transition":
        if len(parts) < 2:
            return False
        code = parts[1].strip()
        return code in from_transition_codes or code in to_transition_codes or code in transition_codes

    if key == "requires_precedence":
        if len(parts) < 3:
            return False
        p_type = parts[1].strip()
        value = ":".join(parts[2:]).strip()
        if p_type == "primary_driver":
            return value in precedence_codes["primary_driver"]
        if p_type == "dominant_edge":
            return value in precedence_codes["dominant_edges"]
        if p_type == "conflict":
            return value in precedence_codes["conflicts"]
        if p_type == "rationale":
            return value in precedence_codes["rationale"]
        return False

    return False


def build_causal_layer_v1(insight_graph: InsightGraphV1) -> Tuple[List[CausalEdgeNode], CausalLayerStamp]:
    registry = load_causal_layer_registry()
    system_codes = _state_map(insight_graph)
    transition_codes = _global_transition_codes(insight_graph)
    precedence_codes = _precedence_codes(insight_graph)

    edges: List[CausalEdgeNode] = []
    for rule in registry.rules:
        if rule.from_system_id not in system_codes or rule.to_system_id not in system_codes:
            continue
        if not all(
            _condition_met(
                condition=condition,
                from_system_id=rule.from_system_id,
                to_system_id=rule.to_system_id,
                system_codes=system_codes,
                transition_codes=transition_codes,
                precedence_codes=precedence_codes,
            )
            for condition in rule.conditions
        ):
            continue
        edges.append(
            CausalEdgeNode(
                edge_id=rule.edge_id,
                from_system_id=rule.from_system_id,
                to_system_id=rule.to_system_id,
                edge_type=rule.edge_type,  # type: ignore[arg-type]
                priority=rule.priority,
                rationale_codes=sorted(set(rule.rationale_codes)),
            )
        )

    edges.sort(key=lambda e: (-e.priority, e.from_system_id, e.to_system_id, e.edge_id))
    payload = {
        "version": CAUSAL_LAYER_V1_VERSION,
        "registry_hash": registry.stamp.causal_layer_registry_hash,
        "causal_edges": [e.model_dump() for e in edges],
    }
    stamp = CausalLayerStamp(
        causal_layer_version=CAUSAL_LAYER_V1_VERSION,
        causal_layer_hash=canonical_json_sha256(payload),
    )
    return edges, stamp
