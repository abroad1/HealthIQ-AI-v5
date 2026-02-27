"""
v5.3 Sprint 3 - Deterministic Interaction Precedence Engine v1.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from core.analytics.precedence_registry import load_precedence_registry
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.precedence_engine_v1 import (
    PRECEDENCE_ENGINE_V1_VERSION,
    DominantEdge,
    PrecedenceOutput,
    PrecedenceStamp,
    canonical_json_sha256,
)

_BUCKET_RANK = {"insufficient": 0, "low": 1, "moderate": 2, "high": 3}


def _bucket_rank(bucket: str) -> int:
    return _BUCKET_RANK.get(str(bucket).strip().lower(), 0)


def _criticality_bucket(insight_graph: InsightGraphV1, system_id: str) -> str:
    criticality = insight_graph.criticality if isinstance(insight_graph.criticality, dict) else {}
    per_system = criticality.get("system_confidence", {})
    if not isinstance(per_system, dict):
        return "insufficient"
    try:
        value = float(per_system.get(system_id, 0.0))
    except (TypeError, ValueError):
        return "insufficient"
    if value >= 85.0:
        return "high"
    if value >= 60.0:
        return "moderate"
    if value >= 30.0:
        return "low"
    return "insufficient"


def _is_abnormal_state_codes(state_codes: Set[str]) -> bool:
    return bool(
        {
            "system_focal_derangement",
            "system_multi_marker_derangement",
            "system_bidirectional_instability",
        }
        & state_codes
    )


def _is_conflict(a: Dict[str, object], b: Dict[str, object]) -> Optional[str]:
    a_trans = set(a.get("transition_summary_codes", []))
    b_trans = set(b.get("transition_summary_codes", []))
    a_states = set(a.get("state_codes", []))
    b_states = set(b.get("state_codes", []))

    a_improving = "system_trending_improving" in a_trans
    b_improving = "system_trending_improving" in b_trans
    a_worsening = "system_trending_worse" in a_trans
    b_worsening = "system_trending_worse" in b_trans

    if (a_improving and b_worsening) or (a_worsening and b_improving):
        return "conflict_trend_opposition"
    if _is_abnormal_state_codes(a_states) and b_improving:
        return "conflict_abnormal_vs_improving"
    if _is_abnormal_state_codes(b_states) and a_improving:
        return "conflict_abnormal_vs_improving"
    return None


def _condition_met(
    condition: str,
    a_state: Dict[str, object],
    b_state: Dict[str, object],
    a_criticality: str,
    b_criticality: str,
) -> bool:
    if ":" not in condition:
        return False
    key, value = condition.split(":", 1)
    value = value.strip()
    a_states = set(a_state.get("state_codes", []))
    b_states = set(b_state.get("state_codes", []))
    a_trans = set(a_state.get("transition_summary_codes", []))
    b_trans = set(b_state.get("transition_summary_codes", []))
    a_bucket = str(a_state.get("confidence_bucket", "insufficient"))
    b_bucket = str(b_state.get("confidence_bucket", "insufficient"))

    if key == "a_has_state":
        return value in a_states
    if key == "b_has_state":
        return value in b_states
    if key == "a_has_transition":
        return value in a_trans
    if key == "b_has_transition":
        return value in b_trans
    if key == "a_confidence_at_least":
        return _bucket_rank(a_bucket) >= _bucket_rank(value)
    if key == "b_confidence_at_least":
        return _bucket_rank(b_bucket) >= _bucket_rank(value)
    if key == "a_criticality_at_least":
        return _bucket_rank(a_criticality) >= _bucket_rank(value)
    if key == "b_criticality_at_least":
        return _bucket_rank(b_criticality) >= _bucket_rank(value)
    if key == "a_has_volatility":
        return value in a_trans
    if key == "b_has_volatility":
        return value in b_trans
    return False


def _apply_tie_breakers(
    winner: Optional[str],
    loser: Optional[str],
    tie_breakers: List[str],
    a_id: str,
    b_id: str,
    a_state: Dict[str, object],
    b_state: Dict[str, object],
    a_criticality: str,
    b_criticality: str,
    system_order: Dict[str, int],
) -> Tuple[Optional[str], Optional[str], List[str]]:
    rationale: List[str] = []
    for tie in tie_breakers:
        if tie == "confidence_gate":
            if winner == a_id and _bucket_rank(str(a_state.get("confidence_bucket", ""))) < 2:
                if _bucket_rank(str(b_state.get("confidence_bucket", ""))) >= 2:
                    winner, loser = b_id, a_id
                    rationale.append("tie_breaker_confidence_gate_swap")
                else:
                    winner, loser = None, None
                    rationale.append("tie_breaker_confidence_gate_block")
            elif winner == b_id and _bucket_rank(str(b_state.get("confidence_bucket", ""))) < 2:
                if _bucket_rank(str(a_state.get("confidence_bucket", ""))) >= 2:
                    winner, loser = a_id, b_id
                    rationale.append("tie_breaker_confidence_gate_swap")
                else:
                    winner, loser = None, None
                    rationale.append("tie_breaker_confidence_gate_block")
        elif tie == "high_criticality_wins":
            a_rank = _bucket_rank(a_criticality)
            b_rank = _bucket_rank(b_criticality)
            if a_rank > b_rank:
                winner, loser = a_id, b_id
                rationale.append("tie_breaker_high_criticality_wins_a")
            elif b_rank > a_rank:
                winner, loser = b_id, a_id
                rationale.append("tie_breaker_high_criticality_wins_b")
        elif tie == "persistence_beats_spike":
            a_trans = set(a_state.get("transition_summary_codes", []))
            b_trans = set(b_state.get("transition_summary_codes", []))
            a_volatile = "system_transition_volatility" in a_trans
            b_volatile = "system_transition_volatility" in b_trans
            if a_volatile and not b_volatile:
                winner, loser = b_id, a_id
                rationale.append("tie_breaker_persistence_beats_spike_b")
            elif b_volatile and not a_volatile:
                winner, loser = a_id, b_id
                rationale.append("tie_breaker_persistence_beats_spike_a")
        elif tie == "explicit_registry_order":
            if winner is None:
                if system_order.get(a_id, 10_000) <= system_order.get(b_id, 10_000):
                    winner, loser = a_id, b_id
                else:
                    winner, loser = b_id, a_id
                rationale.append("tie_breaker_explicit_registry_order")
    return winner, loser, rationale


def build_precedence_v1(insight_graph: InsightGraphV1) -> Tuple[PrecedenceOutput, PrecedenceStamp]:
    registry = load_precedence_registry()
    system_order = {sid: i for i, sid in enumerate(registry.systems)}
    states = {}
    for node in insight_graph.system_states:
        states[node.system_id] = {
            "system_id": node.system_id,
            "state_codes": sorted(set(node.state_codes)),
            "transition_summary_codes": sorted(set(node.transition_summary_codes)),
            "confidence_bucket": node.confidence_bucket,
        }

    pairs: List[Tuple[str, str, str]] = []
    system_ids = sorted(states.keys())
    for i in range(len(system_ids)):
        for j in range(i + 1, len(system_ids)):
            a_id, b_id = system_ids[i], system_ids[j]
            conflict = _is_conflict(states[a_id], states[b_id])
            if conflict:
                pairs.append((a_id, b_id, conflict))

    edges: List[DominantEdge] = []
    conflicts_resolved: List[str] = []
    rationale_codes: List[str] = []

    for left, right, conflict_code in pairs:
        conflicts_resolved.append(conflict_code)
        applicable = [
            r
            for r in registry.rules
            if {r.applies_to["system_a"], r.applies_to["system_b"]} == {left, right}
        ]
        if not applicable:
            continue

        for rule in applicable:
            a_id = rule.applies_to["system_a"]
            b_id = rule.applies_to["system_b"]
            a_state = states.get(a_id)
            b_state = states.get(b_id)
            if a_state is None or b_state is None:
                continue
            a_criticality = _criticality_bucket(insight_graph, a_id)
            b_criticality = _criticality_bucket(insight_graph, b_id)
            conditions_met = all(
                _condition_met(c, a_state, b_state, a_criticality, b_criticality) for c in rule.conditions
            )

            winner: Optional[str] = None
            loser: Optional[str] = None
            if rule.dominance == "a_over_b":
                winner, loser = a_id, b_id
            elif rule.dominance == "b_over_a":
                winner, loser = b_id, a_id
            elif rule.dominance == "conditional" and conditions_met:
                winner, loser = a_id, b_id

            if rule.dominance == "conditional" and not conditions_met:
                rationale_codes.append(f"rule_skipped_conditions:{rule.rule_id}")
                continue

            winner, loser, tie_rationale = _apply_tie_breakers(
                winner=winner,
                loser=loser,
                tie_breakers=rule.tie_breakers,
                a_id=a_id,
                b_id=b_id,
                a_state=a_state,
                b_state=b_state,
                a_criticality=a_criticality,
                b_criticality=b_criticality,
                system_order=system_order,
            )
            rationale_codes.extend(tie_rationale)
            if winner and loser:
                edges.append(DominantEdge(from_system_id=winner, to_system_id=loser, rule_id=rule.rule_id))
                rationale_codes.append(f"rule_applied:{rule.rule_id}")
                break

    edges.sort(key=lambda e: (e.from_system_id, e.to_system_id, e.rule_id))
    wins: Dict[str, int] = {}
    for edge in edges:
        wins[edge.from_system_id] = wins.get(edge.from_system_id, 0) + 1
    for sid in system_ids:
        wins.setdefault(sid, 0)

    if wins:
        top_count = max(wins.values())
        candidates = sorted([sid for sid, count in wins.items() if count == top_count])
    else:
        candidates = []
    if not candidates:
        primary_driver = ""
    elif len(candidates) == 1:
        primary_driver = candidates[0]
    else:
        candidates.sort(
            key=lambda sid: (
                -_bucket_rank(str(states[sid].get("confidence_bucket", "insufficient"))),
                system_order.get(sid, 10_000),
                sid,
            )
        )
        primary_driver = candidates[0]

    output = PrecedenceOutput(
        primary_driver_system_id=primary_driver,
        dominant_edges=edges,
        conflicts_resolved=sorted(set(conflicts_resolved)),
        rationale_codes=sorted(set(rationale_codes)),
    )

    payload = {
        "version": PRECEDENCE_ENGINE_V1_VERSION,
        "registry_hash": registry.stamp.precedence_registry_hash,
        "output": output.model_dump(),
    }
    stamp = PrecedenceStamp(
        precedence_engine_version=PRECEDENCE_ENGINE_V1_VERSION,
        precedence_engine_hash=canonical_json_sha256(payload),
    )
    return output, stamp
