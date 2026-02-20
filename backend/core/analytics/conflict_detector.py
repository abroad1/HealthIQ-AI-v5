"""
v5.3 Sprint 7 - Deterministic conflict detector (InsightGraph-only).
"""

from __future__ import annotations

from typing import Dict, List, Set

from core.analytics.conflict_registry import load_conflict_registry
from core.contracts.arbitration_v1 import ConflictItem
from core.contracts.insight_graph_v1 import InsightGraphV1


def _state_map(insight_graph: InsightGraphV1) -> Dict[str, Dict[str, Set[str]]]:
    out: Dict[str, Dict[str, Set[str]]] = {}
    for node in insight_graph.system_states:
        out[node.system_id] = {
            "state_codes": set(node.state_codes),
            "transition_summary_codes": set(node.transition_summary_codes),
        }
    return out


def _condition_met(condition: str, a: Dict[str, Set[str]], b: Dict[str, Set[str]]) -> bool:
    if ":" not in condition:
        return False
    key, value = condition.split(":", 1)
    key = key.strip()
    code = value.strip()
    if key == "a_has_state":
        return code in a["state_codes"]
    if key == "b_has_state":
        return code in b["state_codes"]
    if key == "a_has_transition":
        return code in a["transition_summary_codes"]
    if key == "b_has_transition":
        return code in b["transition_summary_codes"]
    if key == "either_has_state":
        return code in a["state_codes"] or code in b["state_codes"]
    if key == "either_has_transition":
        return code in a["transition_summary_codes"] or code in b["transition_summary_codes"]
    return False


def build_conflict_set_v1(insight_graph: InsightGraphV1) -> List[ConflictItem]:
    registry = load_conflict_registry()
    states = _state_map(insight_graph)
    system_ids = sorted(states.keys())
    conflicts: List[ConflictItem] = []
    for i in range(len(system_ids)):
        for j in range(i + 1, len(system_ids)):
            left = system_ids[i]
            right = system_ids[j]
            left_state = states[left]
            right_state = states[right]
            for rule in registry.rules:
                # Evaluate both orientations for generic rules
                orientations = [(left, right, left_state, right_state), (right, left, right_state, left_state)]
                for a_id, b_id, a_state, b_state in orientations:
                    if rule.system_a not in {"*", a_id} or rule.system_b not in {"*", b_id}:
                        continue
                    if all(_condition_met(cond, a_state, b_state) for cond in rule.trigger_conditions):
                        conflicts.append(
                            ConflictItem(
                                conflict_id=rule.conflict_id,
                                system_a=a_id,
                                system_b=b_id,
                                conflict_type=rule.conflict_type,
                                rationale_codes=rule.rationale_codes,
                            )
                        )
                        break
                else:
                    continue
                break
    conflicts.sort(key=lambda c: (c.system_a, c.system_b, c.conflict_type, c.conflict_id))
    # deterministic dedupe
    unique: List[ConflictItem] = []
    seen = set()
    for c in conflicts:
        key = (c.conflict_id, c.system_a, c.system_b, c.conflict_type)
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)
    return unique
