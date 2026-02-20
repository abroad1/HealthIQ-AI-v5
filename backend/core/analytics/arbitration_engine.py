"""
v5.3 Sprint 7 - Deterministic arbitration engine.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from core.analytics.arbitration_registry import load_arbitration_registry
from core.contracts.arbitration_v1 import (
    ARBITRATION_V1_VERSION,
    ArbitrationNode,
    ArbitrationStamp,
    ConflictItem,
    DominanceEdge,
    canonical_json_sha256,
)
from core.contracts.insight_graph_v1 import InsightGraphV1

_BUCKET_RANK = {"insufficient": 0, "low": 1, "moderate": 2, "high": 3}


def _system_confidence_bucket(insight_graph: InsightGraphV1, system_id: str) -> str:
    for state in insight_graph.system_states:
        if state.system_id == system_id:
            return str(state.confidence_bucket or "insufficient")
    return "insufficient"


def build_dominance_edges_v1(
    insight_graph: InsightGraphV1,
    conflicts: List[ConflictItem],
) -> List[DominanceEdge]:
    registry = load_arbitration_registry()
    edges: List[DominanceEdge] = []
    for conflict in conflicts:
        applicable = [r for r in registry.dominance_rules if r.conflict_type == conflict.conflict_type]
        for rule in applicable:
            if rule.dominance == "a_over_b":
                winner, loser = conflict.system_a, conflict.system_b
            else:
                winner, loser = conflict.system_b, conflict.system_a
            edges.append(
                DominanceEdge(
                    from_system_id=winner,
                    to_system_id=loser,
                    rule_id=rule.rule_id,
                    conflict_id=conflict.conflict_id,
                    conflict_type=conflict.conflict_type,
                    precedence_tier=rule.precedence_tier,
                    rationale_codes=sorted(set(rule.rationale_codes + conflict.rationale_codes)),
                )
            )
            break
    edges.sort(key=lambda e: (e.from_system_id, e.to_system_id, e.precedence_tier, e.rule_id, e.conflict_id))
    return edges


def build_arbitration_result_v1(
    insight_graph: InsightGraphV1,
    conflicts: List[ConflictItem],
    dominance_edges: List[DominanceEdge],
    causal_edges: List[object],
) -> Tuple[ArbitrationNode, ArbitrationStamp]:
    registry = load_arbitration_registry()
    wins: Dict[str, int] = {}
    min_tier: Dict[str, int] = {}
    systems: Set[str] = {s.system_id for s in insight_graph.system_states}
    for edge in dominance_edges:
        wins[edge.from_system_id] = wins.get(edge.from_system_id, 0) + 1
        min_tier[edge.from_system_id] = min(min_tier.get(edge.from_system_id, 10_000), edge.precedence_tier)
        systems.add(edge.from_system_id)
        systems.add(edge.to_system_id)
    for sid in systems:
        wins.setdefault(sid, 0)
        min_tier.setdefault(sid, 10_000)

    tie_breakers = registry.scoring.tie_breakers
    ranked = sorted(
        systems,
        key=lambda sid: (
            -wins.get(sid, 0),
            min_tier.get(sid, 10_000),
            -_BUCKET_RANK.get(_system_confidence_bucket(insight_graph, sid), 0),
            sid,
        ),
    )
    primary = ranked[0] if ranked else ""
    result = ArbitrationNode(
        primary_driver_system_id=primary,
        tie_breaker_codes=tie_breakers,
        rationale_codes=sorted(
            {
                f"conflicts:{len(conflicts)}",
                f"dominance_edges:{len(dominance_edges)}",
                f"causal_edges:{len(causal_edges)}",
            }
        ),
    )
    payload = {
        "version": ARBITRATION_V1_VERSION,
        "arbitration_registry_hash": registry.stamp.arbitration_registry_hash,
        "result": result.model_dump(),
        "conflict_set": [c.model_dump() for c in conflicts],
        "dominance_edges": [d.model_dump() for d in dominance_edges],
        "causal_edges": [getattr(e, "model_dump", lambda: e)() for e in causal_edges],
    }
    stamp = ArbitrationStamp(
        arbitration_version=ARBITRATION_V1_VERSION,
        arbitration_hash=canonical_json_sha256(payload),
    )
    return result, stamp
