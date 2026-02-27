"""
v5.3 Sprint 9 - Deterministic arbitration engine with transitive dominance.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
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


def _system_calibration_tier(insight_graph: InsightGraphV1, system_id: str) -> str:
    for item in insight_graph.calibration_items:
        if item.system_id == system_id:
            return str(item.priority_tier or "p3")
    return "p3"


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
                    rationale_codes=sorted(set(rule.rationale_codes + conflict.rationale_codes + [f"severity:{conflict.conflict_severity}"])),
                )
            )
            break
    edges.sort(key=lambda e: (e.from_system_id, e.to_system_id, e.precedence_tier, e.rule_id, e.conflict_id))
    return edges


@dataclass(frozen=True)
class _TransitiveState:
    topo_order: List[str]
    reachability: Dict[str, Set[str]]
    transitive_pairs: List[Tuple[str, str]]


def _build_transitive_state(systems: Set[str], dominance_edges: List[DominanceEdge]) -> _TransitiveState:
    adjacency: Dict[str, Set[str]] = {sid: set() for sid in systems}
    indegree: Dict[str, int] = {sid: 0 for sid in systems}
    for edge in dominance_edges:
        if edge.to_system_id not in adjacency[edge.from_system_id]:
            adjacency[edge.from_system_id].add(edge.to_system_id)
            indegree[edge.to_system_id] = indegree.get(edge.to_system_id, 0) + 1

    queue = deque(sorted([sid for sid, deg in indegree.items() if deg == 0]))
    topo: List[str] = []
    indegree_work = dict(indegree)
    while queue:
        node = queue.popleft()
        topo.append(node)
        for nxt in sorted(adjacency.get(node, set())):
            indegree_work[nxt] -= 1
            if indegree_work[nxt] == 0:
                queue.append(nxt)

    if len(topo) != len(systems):
        raise ValueError("Arbitration dominance graph contains a cycle")

    reachability: Dict[str, Set[str]] = {sid: set() for sid in systems}
    for node in reversed(topo):
        for nxt in sorted(adjacency.get(node, set())):
            reachability[node].add(nxt)
            reachability[node].update(reachability[nxt])

    direct_pairs = {(edge.from_system_id, edge.to_system_id) for edge in dominance_edges}
    transitive_pairs = sorted(
        [
            (src, dst)
            for src in sorted(reachability.keys())
            for dst in sorted(reachability[src])
            if (src, dst) not in direct_pairs
        ]
    )
    return _TransitiveState(topo_order=topo, reachability=reachability, transitive_pairs=transitive_pairs)


def build_arbitration_result_v1(
    insight_graph: InsightGraphV1,
    conflicts: List[ConflictItem],
    dominance_edges: List[DominanceEdge],
    causal_edges: List[object],
) -> Tuple[str, ArbitrationNode, ArbitrationStamp]:
    registry = load_arbitration_registry()
    systems: Set[str] = {s.system_id for s in insight_graph.system_states}
    for edge in dominance_edges:
        systems.add(edge.from_system_id)
        systems.add(edge.to_system_id)

    transitive_state = _build_transitive_state(systems, dominance_edges)
    direct_wins: Dict[str, int] = {sid: 0 for sid in systems}
    min_tier: Dict[str, int] = {sid: 10_000 for sid in systems}
    conflict_type_sum: Dict[str, int] = {sid: 0 for sid in systems}
    precedence_tier_sum: Dict[str, int] = {sid: 0 for sid in systems}
    for edge in dominance_edges:
        direct_wins[edge.from_system_id] += 1
        min_tier[edge.from_system_id] = min(min_tier[edge.from_system_id], edge.precedence_tier)
        conflict_type_sum[edge.from_system_id] += registry.scoring.conflict_type_weights.get(edge.conflict_type, 0)
        precedence_tier_sum[edge.from_system_id] += registry.scoring.precedence_tier_weights.get(str(edge.precedence_tier), 0)

    score_components = registry.scoring.score_components
    total_score: Dict[str, int] = {}
    for sid in sorted(systems):
        transitive_wins = len(transitive_state.reachability.get(sid, set()))
        calibration_weight = registry.scoring.calibration_tier_weights.get(_system_calibration_tier(insight_graph, sid), 0)
        score = (
            direct_wins.get(sid, 0) * score_components.get("direct_win_weight", 0)
            + transitive_wins * score_components.get("transitive_win_weight", 0)
            + conflict_type_sum.get(sid, 0) * score_components.get("conflict_weight", 0)
            + precedence_tier_sum.get(sid, 0) * score_components.get("precedence_tier_weight", 0)
            + calibration_weight * score_components.get("calibration_tier_weight", 0)
        )
        total_score[sid] = int(score)

    tie_breakers = registry.scoring.tie_breakers
    ranked = sorted(
        systems,
        key=lambda sid: (
            -total_score.get(sid, 0),
            -len(transitive_state.reachability.get(sid, set())),
            -direct_wins.get(sid, 0),
            min_tier.get(sid, 10_000),
            -_BUCKET_RANK.get(_system_confidence_bucket(insight_graph, sid), 0),
            sid,
        ),
    )
    primary = ranked[0] if ranked else ""
    supporting_systems = [sid for sid in ranked if sid and sid != primary]
    decision_trace_codes = sorted(
        set(
            [f"rule:{e.rule_id}" for e in dominance_edges]
            + [f"transitive:{src}>{dst}" for src, dst in transitive_state.transitive_pairs]
            + [f"score:{sid}:{total_score[sid]}" for sid in sorted(total_score.keys())]
        )
    )
    result = ArbitrationNode(
        supporting_system_ids=supporting_systems,
        decision_trace_codes=decision_trace_codes,
        tie_breaker_codes=tie_breakers,
        rationale_codes=sorted(
            {
                f"conflicts:{len(conflicts)}",
                f"dominance_edges:{len(dominance_edges)}",
                f"transitive_pairs:{len(transitive_state.transitive_pairs)}",
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
        "transitive_pairs": [[src, dst] for src, dst in transitive_state.transitive_pairs],
        "system_scores": [{"system_id": sid, "score": total_score[sid]} for sid in sorted(total_score.keys())],
        "causal_edges": [getattr(e, "model_dump", lambda: e)() for e in causal_edges],
    }
    stamp = ArbitrationStamp(
        arbitration_version=ARBITRATION_V1_VERSION,
        arbitration_hash=canonical_json_sha256(payload),
    )
    return primary, result, stamp
