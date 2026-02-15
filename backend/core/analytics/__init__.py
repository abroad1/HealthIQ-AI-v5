"""
HealthIQ Analytical Substrate (HAS) - Reusable analytical primitives.

HAS v1 provides single-source-of-truth functions for:
- position_in_range: Value position within lab reference range
- map_position_to_status: Map position to frontend status
- calculate_confidence: Consistent confidence across scoring/clustering/insights
- safe_ratio: Denominator-safe ratio for derived metrics only

Sprint 3: criticality module for biomarker criticality evaluation.
"""

from core.analytics.primitives import (
    position_in_range,
    map_position_to_status,
    calculate_confidence,
    safe_ratio,
    frontend_status_from_value_and_range,
)

from core.analytics.criticality import load_criticality_policy, evaluate_criticality
from core.analytics.ratio_registry import RatioRegistry, compute, DERIVED_IDS

__all__ = [
    "position_in_range",
    "map_position_to_status",
    "calculate_confidence",
    "safe_ratio",
    "frontend_status_from_value_and_range",
    "load_criticality_policy",
    "evaluate_criticality",
    "RatioRegistry",
    "compute",
    "DERIVED_IDS",
]
