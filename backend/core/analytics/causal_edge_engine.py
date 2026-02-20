"""
v5.3 Sprint 7 - Deterministic causal edge engine from arbitration SSOT.
"""

from __future__ import annotations

from typing import List, Tuple

from core.analytics.arbitration_registry import load_arbitration_registry
from core.contracts.arbitration_v1 import CausalEdge, ConflictItem, DominanceEdge


def build_causal_edges_v1(
    conflicts: List[ConflictItem],
    dominance_edges: List[DominanceEdge],
) -> List[CausalEdge]:
    registry = load_arbitration_registry()
    edges: List[CausalEdge] = []
    by_conflict = {
        (d.conflict_id, d.from_system_id, d.to_system_id): d for d in dominance_edges
    }
    conflicts_by_id = {c.conflict_id: c for c in conflicts}
    for rule in registry.causal_edge_rules:
        for d in dominance_edges:
            if d.conflict_type != rule.conflict_type:
                continue
            conflict = conflicts_by_id.get(d.conflict_id)
            if conflict is None:
                continue
            from_system_id = d.from_system_id
            to_system_id = d.to_system_id
            if rule.direction == "loser_to_winner":
                from_system_id, to_system_id = to_system_id, from_system_id
            elif rule.direction == "a_to_b":
                from_system_id, to_system_id = conflict.system_a, conflict.system_b
            elif rule.direction == "b_to_a":
                from_system_id, to_system_id = conflict.system_b, conflict.system_a
            elif rule.direction == "winner_to_loser":
                pass
            edges.append(
                CausalEdge(
                    edge_id=f"{rule.edge_rule_id}:{d.conflict_id}",
                    from_system_id=from_system_id,
                    to_system_id=to_system_id,
                    edge_type=rule.edge_type,  # type: ignore[arg-type]
                    priority=rule.priority,
                    rationale_codes=sorted(set(rule.rationale_codes + d.rationale_codes)),
                    source_conflict_ids=[d.conflict_id],
                )
            )

    # deterministic ordering + dedupe
    edges.sort(key=lambda e: (e.from_system_id, e.to_system_id, e.edge_type, e.edge_id))
    uniq: List[CausalEdge] = []
    seen = set()
    for e in edges:
        key = (e.edge_id, e.from_system_id, e.to_system_id, e.edge_type)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(e)
    return uniq
