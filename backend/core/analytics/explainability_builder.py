"""
Deterministic ExplainabilityReport_v1 builder for production and tooling paths.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from core.contracts.arbitration_v1 import canonical_json_sha256
from core.contracts.explainability_report_v1 import (
    EXPLAINABILITY_REPORT_V1_VERSION,
    ExplainabilityArbitrationDecisions,
    ExplainabilityCalibrationImpact,
    ExplainabilityCausalEdgeItem,
    ExplainabilityConflictItem,
    ExplainabilityCycleCheck,
    ExplainabilityDominanceEdgeItem,
    ExplainabilityDominanceResolution,
    ExplainabilityInfluenceOrdering,
    ExplainabilityPrecedenceItem,
    ExplainabilityReplayStamps,
    ExplainabilityReportV1,
    ExplainabilityRunMetadata,
)
from core.contracts.insight_graph_v1 import InsightGraphV1


def _system_id_set(graph: InsightGraphV1) -> List[str]:
    systems = set()
    for node in graph.system_states:
        sid = str(node.system_id or "").strip()
        if sid:
            systems.add(sid)
    for edge in graph.dominance_edges:
        if edge.from_system_id:
            systems.add(edge.from_system_id)
        if edge.to_system_id:
            systems.add(edge.to_system_id)
    for edge in graph.causal_edges:
        if edge.from_system_id:
            systems.add(edge.from_system_id)
        if edge.to_system_id:
            systems.add(edge.to_system_id)
    if graph.primary_driver_system_id:
        systems.add(str(graph.primary_driver_system_id))
    for sid in graph.arbitration_result.supporting_system_ids:
        if sid:
            systems.add(str(sid))
    return sorted(systems)


def _dominance_transitive_rows(
    systems: Sequence[str],
    precedence_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, str]], bool, Dict[str, int], Dict[str, int]]:
    adjacency: Dict[str, set[str]] = {sid: set() for sid in systems}
    indegree: Dict[str, int] = {sid: 0 for sid in systems}
    direct_pairs: set[Tuple[str, str]] = set()
    direct_wins: Dict[str, int] = {sid: 0 for sid in systems}

    for row in precedence_rows:
        src = str(row.get("from_system_id", "")).strip()
        dst = str(row.get("to_system_id", "")).strip()
        if not src or not dst or src == dst:
            continue
        if src not in adjacency:
            adjacency[src] = set()
            indegree[src] = indegree.get(src, 0)
            direct_wins[src] = direct_wins.get(src, 0)
        if dst not in adjacency:
            adjacency[dst] = set()
            indegree[dst] = indegree.get(dst, 0)
            direct_wins[dst] = direct_wins.get(dst, 0)
        if dst not in adjacency[src]:
            adjacency[src].add(dst)
            indegree[dst] = indegree.get(dst, 0) + 1
            direct_pairs.add((src, dst))
            direct_wins[src] = direct_wins.get(src, 0) + 1

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

    has_cycle = len(topo) != len(adjacency)
    if has_cycle:
        return [], True, {sid: 0 for sid in adjacency.keys()}, direct_wins

    reachability: Dict[str, set[str]] = {sid: set() for sid in adjacency.keys()}
    for node in reversed(topo):
        for nxt in sorted(adjacency.get(node, set())):
            reachability[node].add(nxt)
            reachability[node].update(reachability[nxt])

    rows: List[Dict[str, str]] = []
    for src in sorted(reachability.keys()):
        for dst in sorted(reachability[src]):
            if (src, dst) in direct_pairs:
                continue
            rows.append(
                {
                    "from_system_id": src,
                    "to_system_id": dst,
                    "edge_id": f"transitive:{src}>{dst}",
                    "source": "transitive",
                }
            )
    rows.sort(key=lambda row: (row["from_system_id"], row["to_system_id"], row["edge_id"]))
    transitive_reach = {sid: len(reachability.get(sid, set())) for sid in adjacency.keys()}
    return rows, False, transitive_reach, direct_wins


def compute_influence_ordering(graph: InsightGraphV1) -> Dict[str, Any]:
    """
    Deterministic influence ordering.

    Tie-breakers: priority desc -> transitive_reach desc -> direct_wins desc -> system_id asc
    """
    systems = _system_id_set(graph)
    primary_driver_system_id = str(graph.primary_driver_system_id or "").strip()
    if not primary_driver_system_id:
        if len(systems) == 1:
            primary_driver_system_id = systems[0]
            graph.primary_driver_system_id = primary_driver_system_id
        elif len(systems) == 0:
            primary_driver_system_id = "unknown"
            graph.primary_driver_system_id = primary_driver_system_id
        else:
            raise ValueError("Missing primary_driver_system_id on InsightGraph")
    if primary_driver_system_id not in systems:
        systems = sorted(set(systems + [primary_driver_system_id]))

    precedence_rows = [
        {"from_system_id": edge.from_system_id, "to_system_id": edge.to_system_id}
        for edge in graph.dominance_edges
    ]
    _, _, transitive_reach, direct_wins = _dominance_transitive_rows(systems, precedence_rows)

    priority_by_system: Dict[str, int] = {sid: 0 for sid in systems}
    for edge in graph.causal_edges:
        src = str(edge.from_system_id or "").strip()
        if not src:
            continue
        priority_by_system[src] = max(priority_by_system.get(src, 0), int(edge.priority))

    supporting_candidates: List[str] = sorted(
        {
            str(sid).strip()
            for sid in graph.arbitration_result.supporting_system_ids
            if str(sid).strip() and str(sid).strip() != primary_driver_system_id
        }
    )
    if not supporting_candidates:
        supporting_candidates = [sid for sid in systems if sid != primary_driver_system_id]

    supporting_systems = sorted(
        supporting_candidates,
        key=lambda sid: (
            -int(priority_by_system.get(sid, 0)),
            -int(transitive_reach.get(sid, 0)),
            -int(direct_wins.get(sid, 0)),
            sid,
        ),
    )
    influence_order = [primary_driver_system_id] + supporting_systems
    return {
        "primary_driver_system_id": primary_driver_system_id,
        "supporting_systems": supporting_systems,
        "influence_order": influence_order,
        "ordering_scores": {
            sid: {
                "priority": int(priority_by_system.get(sid, 0)),
                "transitive_reach": int(transitive_reach.get(sid, 0)),
                "direct_wins": int(direct_wins.get(sid, 0)),
            }
            for sid in influence_order
        },
    }


def apply_influence_ordering(graph: InsightGraphV1) -> Dict[str, Any]:
    ordering = compute_influence_ordering(graph)
    graph.supporting_systems = list(ordering["supporting_systems"])
    graph.influence_order = list(ordering["influence_order"])
    return ordering


def build_explainability_report_v1(
    graph: InsightGraphV1,
    *,
    run_id: str,
    scenario_id: str = "",
    git_commit_short: str = "",
    generated_at_utc: str = "",
    conflict_registry_version: str = "",
    conflict_registry_hash: str = "",
    arbitration_registry_version: str = "",
    arbitration_registry_hash: str = "",
    arbitration_version: str = "",
    arbitration_hash: str = "",
) -> ExplainabilityReportV1:
    conflict_rows = [
        {
            "conflict_type": c.conflict_type,
            "conflict_id": c.conflict_id,
            "from_system_id": c.system_a,
            "to_system_id": c.system_b,
            "severity": c.conflict_severity,
            "rationale_codes": sorted(set(c.rationale_codes)),
        }
        for c in graph.conflict_set
    ]
    conflict_rows.sort(
        key=lambda row: (
            row["conflict_type"],
            row["conflict_id"],
            row["from_system_id"],
            row["to_system_id"],
            row["severity"],
        )
    )

    precedence_rows = [
        {
            "precedence_tier": int(e.precedence_tier),
            "rule_id": e.rule_id,
            "conflict_id": e.conflict_id,
            "conflict_type": e.conflict_type,
            "from_system_id": e.from_system_id,
            "to_system_id": e.to_system_id,
            "rationale_codes": sorted(set(e.rationale_codes)),
        }
        for e in graph.dominance_edges
    ]
    precedence_rows.sort(
        key=lambda row: (
            int(row["precedence_tier"]),
            row["rule_id"],
            row["from_system_id"],
            row["to_system_id"],
            row["conflict_id"],
        )
    )

    direct_rows = [
        {
            "from_system_id": str(row["from_system_id"]),
            "to_system_id": str(row["to_system_id"]),
            "edge_id": f"direct:{row['rule_id']}:{row['conflict_id']}",
            "source": "direct",
        }
        for row in precedence_rows
    ]
    direct_rows.sort(key=lambda row: (row["from_system_id"], row["to_system_id"], row["edge_id"]))

    systems = _system_id_set(graph)
    transitive_rows, has_cycle, _, _ = _dominance_transitive_rows(systems, precedence_rows)

    causal_rows = [
        {
            "edge_id": e.edge_id,
            "from_system_id": e.from_system_id,
            "to_system_id": e.to_system_id,
            "edge_code": e.edge_type,
            "priority": int(e.priority),
            "source_conflict_ids": sorted(set(e.source_conflict_ids)),
        }
        for e in graph.causal_edges
    ]
    causal_rows.sort(
        key=lambda row: (
            -int(row["priority"]),
            row["from_system_id"],
            row["to_system_id"],
            row["edge_id"],
        )
    )

    ordering = apply_influence_ordering(graph)
    primary = str(ordering["primary_driver_system_id"])

    coupled_tier = ""
    reasons: List[str] = []
    for item in graph.calibration_items:
        if item.system_id == primary:
            coupled_tier = item.priority_tier
            reasons = sorted(set(item.explanation_codes))
            break

    report = ExplainabilityReportV1(
        run_metadata=ExplainabilityRunMetadata(
            report_version=EXPLAINABILITY_REPORT_V1_VERSION,
            run_id=run_id,
            scenario_id=scenario_id,
            git_commit_short=git_commit_short,
            generated_at_utc=generated_at_utc,
        ),
        conflict_summary=[ExplainabilityConflictItem(**row) for row in conflict_rows],
        precedence_summary=[ExplainabilityPrecedenceItem(**row) for row in precedence_rows],
        dominance_resolution=ExplainabilityDominanceResolution(
            cycle_check=ExplainabilityCycleCheck(
                has_cycle=has_cycle,
                status_code="cycle_detected" if has_cycle else "acyclic",
            ),
            direct_edges=[ExplainabilityDominanceEdgeItem(**row) for row in direct_rows],
            transitive_edges=[ExplainabilityDominanceEdgeItem(**row) for row in transitive_rows],
            influence_ordering=ExplainabilityInfluenceOrdering(
                primary_driver_system_id=primary,
                supporting_systems=list(ordering["supporting_systems"]),
                influence_order=list(ordering["influence_order"]),
            ),
        ),
        causal_edges=[ExplainabilityCausalEdgeItem(**row) for row in causal_rows],
        arbitration_decisions=ExplainabilityArbitrationDecisions(
            primary_driver_system_id=primary,
            supporting_systems=list(ordering["supporting_systems"]),
            decision_trace=list(graph.arbitration_result.decision_trace_codes),
            tie_breakers=list(graph.arbitration_result.tie_breaker_codes),
        ),
        calibration_impact=ExplainabilityCalibrationImpact(
            system_id=primary,
            final_calibration_tier=coupled_tier,
            reasons=reasons,
        ),
        replay_stamps=ExplainabilityReplayStamps(
            conflict_registry_version=conflict_registry_version,
            conflict_registry_hash=conflict_registry_hash,
            arbitration_registry_version=arbitration_registry_version,
            arbitration_registry_hash=arbitration_registry_hash,
            arbitration_version=arbitration_version,
            arbitration_hash=arbitration_hash,
            explainability_hash="",
        ),
    )
    hash_payload = report.model_dump()
    hash_payload["run_metadata"] = {"scenario_id": scenario_id} if scenario_id else {}
    report.replay_stamps.explainability_hash = canonical_json_sha256(hash_payload)
    return report


def assert_single_authority_driver(
    *,
    insight_graph_driver: str,
    explainability_driver: str,
    analysis_result_driver: str,
) -> None:
    values = {
        "insight_graph.primary_driver_system_id": str(insight_graph_driver or "").strip(),
        "explainability_report.arbitration_decisions.primary_driver_system_id": str(
            explainability_driver or ""
        ).strip(),
        "analysis_result.primary_driver_system_id": str(analysis_result_driver or "").strip(),
    }
    unique = {v for v in values.values() if v}
    if len(unique) != 1:
        raise ValueError(f"Single-authority primary driver mismatch: {values}")
