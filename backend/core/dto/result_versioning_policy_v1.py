"""
LAUNCH-CORE-3 — Immutable snapshot classification and stale-result detection.

Read-only assessment of persisted client-result payloads. Does not mutate stored results.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple

from core.dto.persisted_replay_contract_v1 import (
    CURRENT_RESULT_VERSION,
    PersistedCompatibilityAssessment,
    assess_persisted_result_compatibility,
)

CURRENT_COMPLETENESS_POLICY_ID = "launch_core_1_subsystem_union_v1"
CURRENT_RESULT_VERSIONING_POLICY_ID = "launch_core_3_immutable_snapshot_v1"

# Known UAT analysis IDs (LAUNCH-CORE-2) — documented for audit cross-check only.
REFERENCE_STALE_ANALYSIS_IDS = frozenset(
    {
        "18e14232-9f93-45e6-820c-004ab5a16235",
        "bb695d3c-453e-4e49-abff-ae80587b4248",
    }
)
REFERENCE_CURRENT_ANALYSIS_ID = "746f2b0a-b470-4d87-8ed8-e2c3d1e68c02"


@dataclass(frozen=True)
class ResultVersioningAssessment:
    base: PersistedCompatibilityAssessment
    stale_reasons: tuple[str, ...]
    stale: bool
    completeness_policy_id: str | None
    regeneration_available: bool


def _subsystem_marker_union(row: Dict[str, Any]) -> Tuple[int, int]:
    included: set[str] = set()
    expected: set[str] = set()
    for sub in row.get("subsystems") or []:
        if not isinstance(sub, dict):
            continue
        for mid in sub.get("included_marker_ids") or []:
            if str(mid).strip():
                included.add(str(mid).strip())
                expected.add(str(mid).strip())
        for mid in sub.get("missing_marker_ids") or []:
            if str(mid).strip():
                expected.add(str(mid).strip())
    if not expected:
        return 0, 0
    return len(included), len(expected)


def detect_launch_core_stale_reasons(stored: Dict[str, Any]) -> List[str]:
    """Heuristic stale markers for pre-LAUNCH-CORE-1 persisted DTOs (no destructive refresh)."""
    reasons: List[str] = []
    meta = stored.get("meta") if isinstance(stored.get("meta"), dict) else {}
    policy = str(meta.get("completeness_policy_id") or "").strip()
    if policy and policy != CURRENT_COMPLETENESS_POLICY_ID:
        reasons.append(f"completeness_policy_mismatch:{policy}")
    elif not policy:
        reasons.append("completeness_policy_missing")

    scores = stored.get("consumer_domain_scores")
    if not isinstance(scores, list):
        return reasons

    for row in scores:
        if not isinstance(row, dict):
            continue
        domain_id = str(row.get("domain_id") or "").strip()
        card_num = row.get("evidence_completeness_numerator")
        card_den = row.get("evidence_completeness_denominator")
        union_num, union_den = _subsystem_marker_union(row)
        if (
            union_den > 0
            and isinstance(card_num, int)
            and isinstance(card_den, int)
            and (card_num, card_den) != (union_num, union_den)
        ):
            reasons.append(f"card_subsystem_completeness_mismatch:{domain_id}")

        for sub in row.get("subsystems") or []:
            if not isinstance(sub, dict):
                continue
            trace = str(sub.get("source_trace") or "")
            if "wave1_subsystem_evidence_v1:" in trace:
                reasons.append(f"legacy_hard_coded_subsystem_trace:{sub.get('subsystem_id')}")
            missing = sub.get("missing_marker_ids") or []
            if "total_bilirubin" in missing:
                reasons.append("legacy_total_bilirubin_false_missing")

    return list(dict.fromkeys(reasons))


def assess_result_versioning(stored: Dict[str, Any]) -> ResultVersioningAssessment:
    base = assess_persisted_result_compatibility(stored)
    extra = detect_launch_core_stale_reasons(stored)
    merged = tuple(dict.fromkeys((*base.stale_reasons, *extra)))
    meta = stored.get("meta") if isinstance(stored.get("meta"), dict) else {}
    policy = str(meta.get("completeness_policy_id") or "").strip() or None
    stale = bool(merged)
    return ResultVersioningAssessment(
        base=base,
        stale_reasons=merged,
        stale=stale,
        completeness_policy_id=policy,
        regeneration_available=False,
    )


def build_result_versioning_metadata(stored: Dict[str, Any]) -> Dict[str, Any]:
    """API-safe metadata block; does not alter persisted payload."""
    assessment = assess_result_versioning(stored)
    status = "stale" if assessment.stale else "current"
    if not assessment.base.compatible:
        status = "incompatible"

    user_message = None
    if status == "stale":
        user_message = (
            "This result was generated with an older analysis engine. "
            "Scores and marker details may not match the latest HealthIQ presentation rules."
        )
    elif status == "incompatible":
        user_message = (
            "This saved result cannot be displayed with the current results page contract."
        )

    return {
        "immutable_snapshot": True,
        "result_status": status,
        "stale_reasons": list(assessment.stale_reasons),
        "result_version": str(stored.get("result_version") or "").strip() or None,
        "current_result_version": CURRENT_RESULT_VERSION,
        "completeness_policy_id": assessment.completeness_policy_id,
        "current_completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID,
        "result_versioning_policy_id": CURRENT_RESULT_VERSIONING_POLICY_ID,
        "regeneration_policy": "versioned_regeneration_required",
        "regeneration_available": assessment.regeneration_available,
        "launch_user_behaviour": "display_stale_warning",
        "planned_user_behaviour": "regenerate_as_new_version",
        "user_message": user_message,
        "render_blockers": list(assessment.base.render_blockers),
        "compatible": assessment.base.compatible,
    }


def stamp_current_policy_meta(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Apply to new analysis runs at persistence time (metadata only)."""
    out = dict(meta)
    out["completeness_policy_id"] = CURRENT_COMPLETENESS_POLICY_ID
    out["result_versioning_policy_id"] = CURRENT_RESULT_VERSIONING_POLICY_ID
    return out
