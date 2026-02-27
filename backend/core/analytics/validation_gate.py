"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module E: programmatic guardian validation.

Sprint 20: zero_path_rule validates influence propagation reachability, not direct scoring.
- Lifestyle modifiers are DIRECT burden on a system (not cross-system propagation).
- zero_path_rule prevents invalid propagation (burden from unreachable systems).
- This is NOT a validation bypass for propagation; it permits direct system scoring when path=inf.
- Allowlist is explicit in SSOT (direct_scoring_systems_allow_no_influence_path); not derived from system_modifiers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Set

from core.analytics.lifestyle_registry_loader import load_lifestyle_registry
from core.contracts.arbitration_v1 import canonical_json_sha256

VALIDATION_GATE_VERSION = "1.0.0"

# Lifestyle-only: no biomarkers; may have no influence path; always allow direct scoring.
LIFESTYLE_ONLY_SYSTEMS = frozenset({"musculoskeletal", "autonomic"})

# Explicit SSOT allowlist; NOT derived from system_modifiers (governance-controlled).
_registry = load_lifestyle_registry()
_direct_systems = set(
    str(s) for s in (_registry.get("direct_scoring_systems_allow_no_influence_path") or [])
)
DIRECT_SCORING_ALLOWED_NO_PATH = frozenset(_direct_systems) | LIFESTYLE_ONLY_SYSTEMS


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

    # Direct scoring exempt from zero_path_rule; propagation constraints remain.
    # Only explicit SSOT allowlist (direct_scoring_systems_allow_no_influence_path + LIFESTYLE_ONLY).
    exempt_ids = (allow_lifestyle_only_systems_without_influence_paths or set()) & DIRECT_SCORING_ALLOWED_NO_PATH
    for sid in supporting_systems:
        if sid in exempt_ids:
            continue
        dist = path_distances.get(sid, float("inf"))
        if dist == float("inf") and float(adjusted_system_burden_vector.get(sid, 0.0)) != 0.0:
            violations.append(f"zero_path_rule_violation:{sid}")

    status = "PASS" if not violations else "FAIL"
    return ValidationResult(status=status, violations=sorted(set(violations)))
