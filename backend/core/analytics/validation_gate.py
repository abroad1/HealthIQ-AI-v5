"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module E: programmatic guardian validation.

Sprint 20: zero_path_rule validates influence propagation reachability, not direct scoring.
- Lifestyle modifiers are DIRECT burden on a system (not cross-system propagation).
- zero_path_rule prevents invalid propagation (burden from unreachable systems).
- Systems that receive direct lifestyle modifiers may have final burden with path=inf.
- LIFESTYLE_ONLY_SYSTEMS (musculoskeletal, autonomic): no biomarkers; may always have path=inf.
- SYSTEMS_WITH_DIRECT_LIFESTYLE_SCORING: from lifestyle_registry system_modifiers;
  when they receive a lifestyle modifier, burden is direct, so exempt from zero_path_rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Set

from core.contracts.arbitration_v1 import canonical_json_sha256

VALIDATION_GATE_VERSION = "1.0.0"

# Lifestyle-only: no biomarkers; may have no influence path; always allow direct scoring.
LIFESTYLE_ONLY_SYSTEMS = frozenset({"musculoskeletal", "autonomic"})

# Systems that can receive direct lifestyle modifiers (from lifestyle_registry system_modifiers).
# When burden is from lifestyle, it is direct scoring—not propagation. Exempt from zero_path_rule.
SYSTEMS_WITH_DIRECT_LIFESTYLE_SCORING = frozenset({
    "cardiovascular", "metabolic", "hepatic", "immune", "musculoskeletal",
})

# Union: systems allowed to have burden with path=inf when they received lifestyle modifier.
DIRECT_SCORING_EXEMPT_IDS = LIFESTYLE_ONLY_SYSTEMS | SYSTEMS_WITH_DIRECT_LIFESTYLE_SCORING


@dataclass(frozen=True)
class ValidationResult:
    status: str
    violations: List[str] = field(default_factory=list)


def compute_burden_hash(
    *,
    adjusted_system_burden_vector: Mapping[str, float],
    system_capacity_scores: Mapping[str, int],
) -> str:
    payload = {
        "adjusted_system_burden_vector": {
            str(k): float(adjusted_system_burden_vector[k]) for k in sorted(adjusted_system_burden_vector.keys())
        },
        "system_capacity_scores": {
            str(k): int(system_capacity_scores[k]) for k in sorted(system_capacity_scores.keys())
        },
    }
    return canonical_json_sha256(payload)


def run_validation_gate_v1(
    *,
    insight_graph_system_ids: Sequence[str],
    primary_driver_system_id: str,
    supporting_systems: Sequence[str],
    influence_order: Sequence[str],
    path_distances: Mapping[str, float],
    adjusted_system_burden_vector: Mapping[str, float],
    system_capacity_scores: Mapping[str, int],
    burden_hash: str,
    allow_lifestyle_only_systems_without_influence_paths: Optional[Set[str]] = None,
) -> ValidationResult:
    violations: List[str] = []
    graph_systems = {str(x) for x in insight_graph_system_ids}
    score_keys = {str(k) for k in system_capacity_scores.keys()}
    if not score_keys.issubset(graph_systems):
        violations.append("capacity_keys_outside_insight_graph_systems")

    if primary_driver_system_id and primary_driver_system_id in system_capacity_scores:
        driver_capacity = int(system_capacity_scores[primary_driver_system_id])
        for sid in supporting_systems:
            if sid in system_capacity_scores and driver_capacity > int(system_capacity_scores[sid]):
                violations.append("primary_driver_capacity_greater_than_supporting")
                break

    sorted_by_burden = sorted(
        [str(k) for k in adjusted_system_burden_vector.keys()],
        key=lambda sid: (-float(adjusted_system_burden_vector[sid]), sid),
    )
    if [str(x) for x in influence_order] != sorted_by_burden:
        violations.append("influence_order_not_descending_adjusted_burden")

    for sid, score in system_capacity_scores.items():
        if int(score) < 0 or int(score) > 100:
            violations.append(f"capacity_out_of_range:{sid}")
    for sid, burden in adjusted_system_burden_vector.items():
        if float(burden) < 0:
            violations.append(f"negative_adjusted_burden:{sid}")

    recalculated = compute_burden_hash(
        adjusted_system_burden_vector=adjusted_system_burden_vector,
        system_capacity_scores=system_capacity_scores,
    )
    if recalculated != burden_hash:
        violations.append("burden_hash_mismatch")

    # Direct scoring (lifestyle modifiers) exempt from zero_path_rule; propagation constraints remain.
    # Only allowlisted systems (LIFESTYLE_ONLY + registry system_modifiers) may have burden with path=inf.
    exempt_ids = (allow_lifestyle_only_systems_without_influence_paths or set()) & DIRECT_SCORING_EXEMPT_IDS
    for sid in supporting_systems:
        if sid in exempt_ids:
            continue
        dist = path_distances.get(sid, float("inf"))
        if dist == float("inf") and float(adjusted_system_burden_vector.get(sid, 0.0)) != 0.0:
            violations.append(f"zero_path_rule_violation:{sid}")

    status = "PASS" if not violations else "FAIL"
    return ValidationResult(status=status, violations=sorted(set(violations)))
