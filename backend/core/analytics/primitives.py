"""
HealthIQ Analytical Substrate v1 (HAS v1) - Centralised analytical primitives.

Single source of truth for duplicated logic across scoring, clustering,
and orchestrator. No SSOT/global range lookups; lab-ranges-first only.

Location: backend/core/analytics/primitives.py
"""

from typing import Any, Optional


def coerce_optional_float(x: Any) -> Optional[float]:
    """
    Best-effort parse for live lab JSON (numbers often arrive as strings).
    """
    if x is None:
        return None
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip()
        if not s:
            return None
        try:
            return float(s)
        except ValueError:
            return None
    return None


def position_in_range(
    value: float,
    low: float,
    high: float,
) -> Optional[float]:
    """
    Return value position within reference range as 0..1 (clamped).

    Position 0 = at min, 1 = at max. Values outside range extend beyond 0/1.
    Returns None if range is invalid (low >= high) or inputs are insufficient.

    Args:
        value: Observed value
        low: Minimum of reference range
        high: Maximum of reference range

    Returns:
        Position; may be <0 or >1 when value is outside range.
        None if range_span <= 0.
    """
    if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
        return None
    range_span = high - low
    if range_span <= 0:
        return None
    pos = (value - low) / range_span
    return round(pos, 6)


def position_in_one_sided_lab_range(
    value: float,
    low: Optional[float],
    high: Optional[float],
) -> Optional[float]:
    """
    Map value to a 0..1 style position for one-sided commercial lab ranges.

    max-only: in-range (value <= high) uses a mid-band position; above max is high-side.
    min-only: in-range (value >= low) uses a mid-band position; below min is low-side.

    When both bounds are numeric and low < high, delegates to :func:`position_in_range`.
    """
    has_low = isinstance(low, (int, float))
    has_high = isinstance(high, (int, float))
    if has_low and has_high and float(low) < float(high):
        return position_in_range(value, float(low), float(high))
    if has_high and not has_low:
        return 0.55 if value <= float(high) else 1.02
    if has_low and not has_high:
        return 0.55 if value >= float(low) else 0.02
    return None


def has_valid_numeric_lab_range(ref_min: Optional[float], ref_max: Optional[float]) -> bool:
    """True if the lab range can support scoring: two-sided with span, or any one-sided bound."""
    has_min = isinstance(ref_min, (int, float))
    has_max = isinstance(ref_max, (int, float))
    if has_min and has_max:
        return float(ref_min) < float(ref_max)  # type: ignore[arg-type]
    return has_min or has_max


def frontend_status_from_lab_reference(
    value: float,
    min_val: Optional[float],
    max_val: Optional[float],
    *,
    biomarker_name: Optional[str] = None,
) -> str:
    """
    Frontend status from lab reference, including one-sided commercial ranges.

    When ``biomarker_name`` is set, applies the same direction-aware position override
    as scoring (LC-S14) so low enzyme values are not labelled critical on retail surfaces.
    """
    if biomarker_name:
        from core.scoring.rules import ScoringRules

        rules = ScoringRules()
        direction_pos = rules._directionality_position_override(
            biomarker_name,
            float(value),
            float(min_val) if isinstance(min_val, (int, float)) else None,
            float(max_val) if isinstance(max_val, (int, float)) else None,
        )
        if direction_pos is not None:
            has_status = map_position_to_status(direction_pos)
            return has_status_to_frontend(has_status)
    pos = position_in_one_sided_lab_range(value, min_val, max_val)
    if pos is None:
        return "unknown"
    has_status = map_position_to_status(pos)
    return has_status_to_frontend(has_status)


def map_position_to_status(
    pos: float,
    *,
    low_critical: float = 0.0,
    low_borderline: float = 0.1,
    optimal_low: float = 0.2,
    optimal_high: float = 0.8,
    high_borderline: float = 0.9,
    high_critical: float = 1.0,
) -> str:
    """
    Map position-in-range to status string.

    Thresholds define band boundaries. Used consistently by scoring and DTO builders.
    Aligns with scoring logic: optimal = middle 60%, normal = 80%, borderline at 0.05/0.95.

    Args:
        pos: Position from position_in_range (may be <0 or >1)
        low_critical: Below this = low_critical
        low_borderline: low_critical <= pos < this = low_borderline
        optimal_low/high: optimal band (middle 60%)
        high_borderline: outer normal boundary
        high_critical: above this = high_critical

    Returns:
        One of: low_critical, low_borderline, normal, optimal, high_borderline, high_critical
    """
    if pos < low_critical:
        return "low_critical"
    if pos < low_borderline:
        return "low_borderline"
    if pos < optimal_low:
        return "normal"
    if pos <= optimal_high:
        return "optimal"
    if pos <= high_borderline:
        return "normal"
    if pos <= high_critical:
        return "high_borderline"
    return "high_critical"


def calculate_confidence(
    n_present: int,
    n_expected: int,
    *,
    floor: float = 0.0,
    ceiling: float = 1.0,
) -> float:
    """
    Calculate confidence from presence ratio.

    Formula: min(ceiling, max(floor, n_present / n_expected)).
    Rationale: Linear ratio is simple, interpretable, and sufficient for
    data-completeness and biomarker-coverage confidence. Avoids overfitting
    to any single domain. Used by scoring, clustering, and insights.

    Args:
        n_present: Number of items present
        n_expected: Expected total (denominator)
        floor: Minimum confidence
        ceiling: Maximum confidence

    Returns:
        Confidence in [floor, ceiling]
    """
    if n_expected <= 0:
        return floor
    ratio = n_present / n_expected
    return max(floor, min(ceiling, ratio))


def safe_ratio(
    numerator: Optional[float],
    denominator: Optional[float],
) -> Optional[float]:
    """
    Compute numerator/denominator with zero/None safety.

    For derived ratios only. No bounds here; bounds remain in
    DERIVED_RATIO_BOUNDS or caller.

    Args:
        numerator: Numerator value
        denominator: Denominator value

    Returns:
        numerator/denominator if denominator is non-zero and both are numeric,
        else None.
    """
    if numerator is None or denominator is None:
        return None
    if not isinstance(numerator, (int, float)) or not isinstance(denominator, (int, float)):
        return None
    if denominator == 0:
        return None
    return numerator / denominator


# --- Status mapping: HAS primitives -> frontend API strings ---
# Frontend expects: optimal, normal, elevated, low, critical, unknown
# map_position_to_status returns: low_critical, low_borderline, normal, high_borderline, high_critical

STATUS_FROM_HAS_TO_FRONTEND = {
    "low_critical": "critical",
    "low_borderline": "low",
    "normal": "normal",
    "optimal": "optimal",
    "high_borderline": "elevated",
    "high_critical": "elevated",
}


def has_status_to_frontend(has_status: str) -> str:
    """
    Map HAS primitive status to frontend API status.

    Frontend expects: optimal, normal, elevated, low, critical, unknown.
    """
    return STATUS_FROM_HAS_TO_FRONTEND.get(has_status, "unknown")


def frontend_status_from_value_and_range(
    value: float,
    min_val: float,
    max_val: float,
) -> str:
    """
    Single source of truth for frontend status from value and lab reference range.

    Used by both scoring (via rules) and orchestrator DTO building.
    No SSOT lookup - lab range only.

    Returns one of: optimal, normal, elevated, low, critical, unknown.
    """
    pos = position_in_range(value, min_val, max_val)
    if pos is None:
        return "unknown"
    has_status = map_position_to_status(pos)
    return has_status_to_frontend(has_status)
