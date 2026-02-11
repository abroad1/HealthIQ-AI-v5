"""
Tests for lab-range-only scoring rule: lab-provided biomarkers use ONLY lab reference
ranges; never SSOT/global. Unscored when lab range missing, with reason.
"""

import pytest
from unittest.mock import patch

from core.scoring.rules import (
    ScoringRules,
    ScoreRange,
    UNSCORED_REASON,
    DERIVED_RATIOS,
    DERIVED_RATIO_BOUNDS,
)
from core.scoring.engine import ScoringEngine


class TestHDLWithLabBounds:
    """HDL with lab bounds must be scored using those bounds (canonical key: hdl)."""

    def test_hdl_with_lab_bounds_gets_scored(self):
        rules = ScoringRules()
        lab_range = {"min": 40.0, "max": 60.0, "unit": "mg/dL", "source": "lab"}
        score, score_range, reason = rules.calculate_biomarker_score(
            "hdl", 50.0, input_reference_range=lab_range
        )
        assert reason is None
        assert score > 0
        assert score_range in (ScoreRange.OPTIMAL, ScoreRange.NORMAL, ScoreRange.BORDERLINE)


class TestLDLWithLabBounds:
    """LDL with lab bounds must be scored using those bounds (canonical key: ldl)."""

    def test_ldl_with_lab_bounds_gets_scored(self):
        rules = ScoringRules()
        lab_range = {"min": 0.0, "max": 100.0, "unit": "mg/dL", "source": "lab"}
        score, score_range, reason = rules.calculate_biomarker_score(
            "ldl", 80.0, input_reference_range=lab_range
        )
        assert reason is None
        assert score > 0


class TestHDLWithoutLabBounds:
    """HDL without lab bounds must be unscored with reason missing_lab_reference_range."""

    def test_hdl_without_lab_bounds_is_unscored_with_reason(self):
        rules = ScoringRules()
        score, score_range, reason = rules.calculate_biomarker_score("hdl", 50.0)
        assert reason == UNSCORED_REASON
        assert UNSCORED_REASON == "missing_lab_reference_range"
        assert score == 0.0


class TestLDLWithoutLabBounds:
    """LDL without lab bounds must be unscored with reason missing_lab_reference_range."""

    def test_ldl_without_lab_bounds_is_unscored_with_reason(self):
        rules = ScoringRules()
        score, score_range, reason = rules.calculate_biomarker_score("ldl", 120.0)
        assert reason == UNSCORED_REASON


class TestDerivedRatioTcHdlRatio:
    """tc_hdl_ratio (derived) uses DERIVED_RATIO_BOUNDS when lab did not provide it."""

    def test_tc_hdl_ratio_without_lab_bounds_uses_derived_ratio_table(self):
        rules = ScoringRules()
        score, score_range, reason = rules.calculate_biomarker_score("tc_hdl_ratio", 4.0)
        assert reason is None
        assert score > 0
        assert "tc_hdl_ratio" in DERIVED_RATIOS
        assert "tc_hdl_ratio" in DERIVED_RATIO_BOUNDS

    def test_tc_hdl_ratio_with_lab_bounds_uses_lab(self):
        rules = ScoringRules()
        lab_range = {"min": 2.0, "max": 5.0, "unit": "ratio", "source": "lab"}
        score, score_range, reason = rules.calculate_biomarker_score(
            "tc_hdl_ratio", 3.5, input_reference_range=lab_range
        )
        assert reason is None
        assert score > 0


class TestSSOTNeverInvoked:
    """SSOT/global range lookup must NEVER be invoked in scoring paths."""

    def test_scoring_rules_has_no_resolver(self):
        """ScoringRules must not use CanonicalResolver - no SSOT access possible."""
        rules = ScoringRules()
        assert not hasattr(rules, "resolver"), "ScoringRules must not have resolver"

    def test_no_ssot_import_in_rules(self):
        """Scoring rules module must not import CanonicalResolver."""
        import core.scoring.rules as rules_module
        assert "CanonicalResolver" not in dir(rules_module)

    def test_full_scoring_flow_never_calls_ssot(self):
        """Full engine scoring must not invoke any SSOT reference range lookup."""
        with patch("core.canonical.resolver.CanonicalResolver.get_reference_range") as mock_get:
            engine = ScoringEngine()
            biomarkers = {"hdl": 50.0, "ldl": 90.0}
            input_reference_ranges = {
                "hdl": {"min": 40.0, "max": 60.0, "unit": "mg/dL"},
                "ldl": {"min": 0.0, "max": 100.0, "unit": "mg/dL"},
            }
            engine.score_biomarkers(biomarkers, input_reference_ranges=input_reference_ranges)
            mock_get.assert_not_called()


class TestEngineIntegration:
    """Scoring engine integration: hdl/ldl with lab bounds scored, without unscored."""

    def test_engine_hdl_with_lab_bounds_scored(self):
        engine = ScoringEngine()
        biomarkers = {"hdl": 50.0}
        input_reference_ranges = {"hdl": {"min": 40.0, "max": 60.0, "unit": "mg/dL"}}
        result = engine.score_biomarkers(
            biomarkers, input_reference_ranges=input_reference_ranges
        )
        hdl_scores = [
            s for sys_score in result.health_system_scores.values()
            for s in sys_score.biomarker_scores
            if s.biomarker_name == "hdl"
        ]
        assert len(hdl_scores) == 1
        assert hdl_scores[0].score > 0
        assert getattr(hdl_scores[0], "unscored_reason", None) is None

    def test_engine_ldl_with_lab_bounds_scored(self):
        engine = ScoringEngine()
        biomarkers = {"ldl": 90.0}
        input_reference_ranges = {"ldl": {"min": 0.0, "max": 100.0, "unit": "mg/dL"}}
        result = engine.score_biomarkers(
            biomarkers, input_reference_ranges=input_reference_ranges
        )
        ldl_scores = [
            s for sys_score in result.health_system_scores.values()
            for s in sys_score.biomarker_scores
            if s.biomarker_name == "ldl"
        ]
        assert len(ldl_scores) == 1
        assert ldl_scores[0].score > 0

    def test_engine_hdl_without_lab_bounds_unscored_with_reason(self):
        engine = ScoringEngine()
        biomarkers = {"hdl": 50.0}
        result = engine.score_biomarkers(biomarkers)
        hdl_scores = [
            s for sys_score in result.health_system_scores.values()
            for s in sys_score.biomarker_scores
            if s.biomarker_name == "hdl"
        ]
        assert len(hdl_scores) == 1
        assert hdl_scores[0].unscored_reason == UNSCORED_REASON
        assert hdl_scores[0].score == 0.0

    def test_engine_ldl_without_lab_bounds_unscored_with_reason(self):
        engine = ScoringEngine()
        biomarkers = {"ldl": 120.0}
        result = engine.score_biomarkers(biomarkers)
        ldl_scores = [
            s for sys_score in result.health_system_scores.values()
            for s in sys_score.biomarker_scores
            if s.biomarker_name == "ldl"
        ]
        assert len(ldl_scores) == 1
        assert ldl_scores[0].unscored_reason == UNSCORED_REASON
