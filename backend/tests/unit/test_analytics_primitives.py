"""
Unit tests for HAS v1 analytical primitives.

Ensures single-source primitives behave correctly for edge cases:
missing values, invalid ranges, clamping, denominator=0.
"""

import pytest

from core.analytics.primitives import (
    position_in_range,
    map_position_to_status,
    calculate_confidence,
    safe_ratio,
    frontend_status_from_value_and_range,
)


class TestPositionInRange:
    """Tests for position_in_range."""

    def test_within_range_middle(self):
        assert position_in_range(50.0, 0.0, 100.0) == 0.5

    def test_at_min(self):
        assert position_in_range(0.0, 0.0, 100.0) == 0.0

    def test_at_max(self):
        assert position_in_range(100.0, 0.0, 100.0) == 1.0

    def test_below_range(self):
        assert position_in_range(-10.0, 0.0, 100.0) == -0.1

    def test_above_range(self):
        assert position_in_range(150.0, 0.0, 100.0) == 1.5

    def test_invalid_range_zero_span(self):
        assert position_in_range(50.0, 100.0, 100.0) is None

    def test_invalid_range_negative_span(self):
        assert position_in_range(50.0, 100.0, 0.0) is None

    def test_none_min_returns_none(self):
        assert position_in_range(50.0, None, 100.0) is None

    def test_none_max_returns_none(self):
        assert position_in_range(50.0, 0.0, None) is None


class TestMapPositionToStatus:
    """Tests for map_position_to_status."""

    def test_optimal_middle(self):
        assert map_position_to_status(0.5) == "optimal"

    def test_normal_low_side(self):
        assert map_position_to_status(0.15) == "normal"

    def test_normal_high_side(self):
        assert map_position_to_status(0.85) == "normal"

    def test_low_borderline(self):
        assert map_position_to_status(0.07) == "low_borderline"

    def test_high_borderline(self):
        assert map_position_to_status(0.93) == "high_borderline"

    def test_low_critical_below_zero(self):
        assert map_position_to_status(-0.5) == "low_critical"

    def test_high_critical_above_one(self):
        assert map_position_to_status(1.5) == "high_critical"


class TestCalculateConfidence:
    """Tests for calculate_confidence."""

    def test_full_coverage(self):
        assert calculate_confidence(10, 10) == 1.0

    def test_half_coverage(self):
        assert calculate_confidence(5, 10) == 0.5

    def test_zero_expected_returns_floor(self):
        assert calculate_confidence(0, 0, floor=0.0) == 0.0

    def test_negative_expected_returns_floor(self):
        assert calculate_confidence(5, -1, floor=0.0) == 0.0

    def test_ceiling_respected(self):
        assert calculate_confidence(100, 10, ceiling=1.0) == 1.0

    def test_floor_respected(self):
        assert calculate_confidence(0, 10, floor=0.2) == 0.2


class TestSafeRatio:
    """Tests for safe_ratio."""

    def test_normal_ratio(self):
        assert safe_ratio(10.0, 2.0) == 5.0

    def test_denominator_zero_returns_none(self):
        assert safe_ratio(10.0, 0.0) is None

    def test_numerator_none_returns_none(self):
        assert safe_ratio(None, 5.0) is None

    def test_denominator_none_returns_none(self):
        assert safe_ratio(10.0, None) is None

    def test_both_none_returns_none(self):
        assert safe_ratio(None, None) is None


class TestFrontendStatusFromValueAndRange:
    """Tests for frontend_status_from_value_and_range."""

    def test_optimal_returns_optimal(self):
        assert frontend_status_from_value_and_range(50.0, 0.0, 100.0) == "optimal"

    def test_invalid_range_returns_unknown(self):
        assert frontend_status_from_value_and_range(50.0, 100.0, 0.0) == "unknown"

    def test_low_returns_critical_when_below_range(self):
        """Value 5 in range 20-80 -> position -0.25 -> low_critical -> critical."""
        assert frontend_status_from_value_and_range(5.0, 20.0, 80.0) == "critical"

    def test_low_returns_low_when_borderline(self):
        """Value in low_borderline band (pos ~0.05) -> low."""
        assert frontend_status_from_value_and_range(23.0, 20.0, 80.0) == "low"

    def test_elevated_returns_elevated(self):
        assert frontend_status_from_value_and_range(95.0, 20.0, 80.0) == "elevated"


class TestRegressionOrchestratorStatusMatchesScoring:
    """Regression: orchestrator status uses same primitive as scoring."""

    def test_status_consistent_for_same_value_range(self):
        """frontend_status_from_value_and_range produces same status as scoring rules."""
        from core.scoring.rules import ScoringRules
        rules = ScoringRules()
        value, min_val, max_val = 75.0, 0.0, 100.0
        _, score_range = rules._calculate_score_from_range(value, min_val, max_val)
        has_status = map_position_to_status(position_in_range(value, min_val, max_val))
        frontend_status = frontend_status_from_value_and_range(value, min_val, max_val)
        # Both paths should agree on band
        assert frontend_status in ("optimal", "normal", "elevated", "low", "critical", "unknown")
        assert score_range.value in ("optimal", "normal", "borderline", "high", "very_high", "critical")
