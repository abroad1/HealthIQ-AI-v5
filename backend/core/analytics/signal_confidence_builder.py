"""
Deterministic per-signal confidence calculator (KB-S29).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple


CONFIDENCE_REASON_ORDER: List[str] = [
    "ALL_SUPPORTING_MARKERS_PRESENT",
    "PARTIAL_SUPPORTING_MARKERS",
    "NO_SUPPORTING_MARKERS",
    "ESCALATION_MULTI_CONDITION",
    "ESCALATION_SINGLE_CONDITION",
    "REFERENCE_RANGE_COMPLETE",
    "REFERENCE_RANGE_ONE_SIDED",
    "REFERENCE_RANGE_BAND_PROFILE",
    "PRIMARY_METRIC_PRESENT",
    "PRIMARY_METRIC_ABSENT",
]
ALLOWED_CONFIDENCE_REASONS: Set[str] = set(CONFIDENCE_REASON_ORDER)


def _as_float(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _has_numeric(value: Any) -> bool:
    return isinstance(value, (int, float))


def _sorted_reasons(reasons: Set[str]) -> List[str]:
    return [token for token in CONFIDENCE_REASON_ORDER if token in reasons]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def calculate_signal_confidence(
    *,
    primary_metric: str,
    primary_metric_present: bool,
    supporting_markers: List[str],
    available_metrics: Set[str],
    signal_state: str,
    lab_ranges: Dict[str, Dict[str, Any]],
    reference_profiles: Optional[Dict[str, Dict[str, Any]]] = None,
    override_satisfied_count: Optional[int] = None,
) -> Tuple[float, List[str]]:
    reasons: Set[str] = set()
    reference_profiles = reference_profiles or {}

    unique_supporting = sorted({str(m).strip() for m in supporting_markers if str(m).strip()})
    supporting_total = len(unique_supporting)
    supporting_present = sum(1 for marker in unique_supporting if marker in available_metrics)
    if supporting_total == 0:
        coverage = 1.0
        reasons.add("NO_SUPPORTING_MARKERS")
    else:
        coverage = supporting_present / supporting_total
        if supporting_present == supporting_total:
            reasons.add("ALL_SUPPORTING_MARKERS_PRESENT")
        else:
            reasons.add("PARTIAL_SUPPORTING_MARKERS")
    confidence = 0.60 * coverage

    if primary_metric_present:
        confidence += 0.20
        reasons.add("PRIMARY_METRIC_PRESENT")
    else:
        reasons.add("PRIMARY_METRIC_ABSENT")

    ref_profile = reference_profiles.get(primary_metric)
    if isinstance(ref_profile, dict):
        confidence += 0.10
        reasons.add("REFERENCE_RANGE_BAND_PROFILE")
    else:
        ref_range = (lab_ranges or {}).get(primary_metric)
        if isinstance(ref_range, dict):
            low = _as_float(ref_range.get("min"))
            high = _as_float(ref_range.get("max"))
            if _has_numeric(low) and _has_numeric(high):
                confidence += 0.10
                reasons.add("REFERENCE_RANGE_COMPLETE")
            elif _has_numeric(low) or _has_numeric(high):
                confidence += 0.05
                reasons.add("REFERENCE_RANGE_ONE_SIDED")

    if signal_state == "at_risk" and isinstance(override_satisfied_count, int) and override_satisfied_count > 0:
        if override_satisfied_count >= 2:
            confidence += 0.10
            reasons.add("ESCALATION_MULTI_CONDITION")
        else:
            confidence += 0.05
            reasons.add("ESCALATION_SINGLE_CONDITION")

    confidence = _clamp01(confidence)
    if not primary_metric_present:
        confidence = _clamp01(confidence * 0.60)

    return round(confidence, 4), _sorted_reasons(reasons)
