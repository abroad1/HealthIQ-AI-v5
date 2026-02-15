"""
HealthIQ Analytical Substrate v1 (HAS v1) - Centralised analytical primitives.

Single source of truth for duplicated logic across scoring, clustering,
and orchestrator. No SSOT/global range lookups; lab-ranges-first only.

Location: backend/core/analytics/primitives.py
"""

from typing import Optional


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
