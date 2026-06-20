"""
P1-8 — Tests for governed lab_range_only biomarker scoring rules.

Uses an isolated fixture policy; does not activate thyroid production scoring.
"""

import pytest

import core.analytics.scoring_policy_registry as scoring_policy_registry
import core.scoring.rules as scoring_rules_module
from core.scoring.engine import ScoringEngine
from core.scoring.rules import (
    SCORING_TYPE_LAB_RANGE_ONLY,
    SCORING_TYPE_RANGE_POSITION,
    ScoreRange,
    ScoringRules,
    UNSCORED_REASON,
)


def _reset_policy_cache() -> None:
    scoring_policy_registry._policy_cache = None


_FIXTURE_POLICY = """\
policy_version: "9.9.9-fixture"
schema_version: "1.0"
systems:
  hormonal:
    min_biomarkers_required: 1
    system_weight: 1.0
    biomarkers: [fixture_lab_range_marker]
  metabolic:
    min_biomarkers_required: 1
    system_weight: 1.0
    biomarkers: [fixture_band_marker]
system_execution_order: [metabolic, hormonal]
biomarkers:
  fixture_lab_range_marker:
    scoring_type: lab_range_only
    unit: "mIU/L"
    weight: 1.0
  fixture_band_marker:
    scoring_type: range_position
    unit: "mmol/L"
    weight: 1.0
    bands:
      optimal: {min: 3.9, max: 5.6}
      normal: {min: 3.9, max: 5.6}
      borderline: {min: 5.6, max: 6.9}
      high: {min: 6.9, max: 11.1}
      very_high: {min: 11.1, max: 16.7}
      critical: {min: 16.7, max: 55.6}
biomarker_directionality:
  default_class: bidirectional_concern
  allowed_classes:
    - bidirectional_concern
    - high_only_concern
    - low_only_concern
  informational_position: 0.05
  protective_in_range_position: 0.75
  markers:
    fixture_lab_range_marker:
      direction_class: low_only_concern
status_map:
  normal: normal
  optimal: optimal
score_curve:
  optimal_band: {min: 0.2, max: 0.8, score: 100.0}
  normal_band: {min: 0.1, max: 0.9, score: 90.0}
  normal_low: {start: 0.1, end: 0.2, score_start: 90.0, score_end: 100.0}
  normal_high: {start: 0.8, end: 0.9, score_start: 100.0, score_end: 90.0}
  borderline_band: {min: 0.05, max: 0.95, score: 70.0}
  borderline_low: {start: 0.05, end: 0.1, score_start: 70.0, score_end: 90.0}
  borderline_high: {start: 0.9, end: 0.95, score_start: 90.0, score_end: 70.0}
  low_noncritical: {start: 0.0, end: 0.05, score_start: 50.0, score_end: 70.0}
  low_critical: {base_score: 10.0, excess_multiplier: 50.0}
  high_noncritical: {start: 0.95, end: 1.0, score_start: 70.0, score_end: 50.0}
  high_critical: {base_score: 30.0, excess_multiplier: 50.0}
derived_ratio_policy_bounds: {}
derived_ratios: []
scoring_runtime:
  unscored_reason_missing_lab_reference_range: missing_lab_reference_range
"""


@pytest.fixture
def fixture_policy_path(tmp_path, monkeypatch):
    path = tmp_path / "scoring_policy.yaml"
    path.write_text(_FIXTURE_POLICY, encoding="utf-8")
    monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: path)
    _reset_policy_cache()
    monkeypatch.setattr(scoring_rules_module, "_POLICY", scoring_policy_registry.load_scoring_policy())
    yield path
    _reset_policy_cache()


class TestLabRangeOnlyRuleConstruction:
    def test_lab_range_only_rule_loads_without_bands(self, fixture_policy_path):
        rules = ScoringRules()
        rule = rules.get_biomarker_rule("fixture_lab_range_marker")
        assert rule is not None
        assert rule.scoring_type == SCORING_TYPE_LAB_RANGE_ONLY
        assert rule.is_lab_range_only
        assert rule.unit == "mIU/L"
        assert rule.optimal_range is None
        assert rule.normal_range is None

    def test_band_marker_still_loads_with_bands(self, fixture_policy_path):
        rules = ScoringRules()
        rule = rules.get_biomarker_rule("fixture_band_marker")
        assert rule is not None
        assert rule.scoring_type == SCORING_TYPE_RANGE_POSITION
        assert rule.optimal_range is not None
        assert rule.normal_range is not None

    def test_lab_range_only_rejects_bands_in_policy(self, tmp_path, monkeypatch):
        bad = tmp_path / "scoring_policy.yaml"
        bad.write_text(
            _FIXTURE_POLICY.replace(
                "fixture_lab_range_marker:\n    scoring_type: lab_range_only",
                "fixture_lab_range_marker:\n    scoring_type: lab_range_only\n    bands:\n      optimal: {min: 0, max: 1}",
            ),
            encoding="utf-8",
        )
        monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: bad)
        _reset_policy_cache()
        with pytest.raises(ValueError, match="must not declare bands"):
            scoring_policy_registry.load_scoring_policy()

    def test_lab_range_only_requires_unit(self, tmp_path, monkeypatch):
        bad = tmp_path / "scoring_policy.yaml"
        bad.write_text(
            _FIXTURE_POLICY.replace('unit: "mIU/L"', 'unit: ""'),
            encoding="utf-8",
        )
        monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: bad)
        _reset_policy_cache()
        with pytest.raises(ValueError, match="requires unit"):
            scoring_policy_registry.load_scoring_policy()


class TestLabRangeOnlyScoring:
    def test_scores_from_lab_reference_range(self, fixture_policy_path):
        rules = ScoringRules()
        lab_range = {"min": 0.4, "max": 4.0, "unit": "mIU/L", "source": "lab"}
        score, score_range, reason = rules.calculate_biomarker_score(
            "fixture_lab_range_marker",
            2.0,
            input_reference_range=lab_range,
            value_unit="mIU/L",
        )
        assert reason is None
        assert score > 0
        assert score_range in (ScoreRange.OPTIMAL, ScoreRange.NORMAL, ScoreRange.BORDERLINE)

    def test_missing_lab_range_fails_closed(self, fixture_policy_path):
        rules = ScoringRules()
        score, score_range, reason = rules.calculate_biomarker_score(
            "fixture_lab_range_marker", 2.0
        )
        assert reason == UNSCORED_REASON
        assert score == 0.0
        assert score_range == ScoreRange.CRITICAL

    def test_directionality_respected_for_low_only(self, fixture_policy_path):
        rules = ScoringRules()
        lab_range = {"min": 0.4, "max": 4.0, "unit": "mIU/L", "source": "lab"}
        score, _, reason = rules.calculate_biomarker_score(
            "fixture_lab_range_marker",
            0.2,
            input_reference_range=lab_range,
            value_unit="mIU/L",
        )
        assert reason is None
        assert score > 0

    def test_band_methods_reject_lab_range_only_rule(self, fixture_policy_path):
        rules = ScoringRules()
        rule = rules.get_biomarker_rule("fixture_lab_range_marker")
        with pytest.raises(ValueError, match="lab_range_only"):
            rules._determine_score_range(1.0, rule)


class TestLabRangeOnlyEngineIntegration:
    def test_system_orchestration_scores_lab_range_only_member(self, fixture_policy_path):
        rules = ScoringRules()
        engine = ScoringEngine(rules=rules)
        canonical = {"fixture_lab_range_marker": 2.0}
        lab_ranges = {
            "fixture_lab_range_marker": {"min": 0.4, "max": 4.0, "unit": "mIU/L"},
        }
        hormonal = engine._score_health_system(
            "hormonal",
            canonical,
            None,
            None,
            None,
            input_reference_ranges=lab_ranges,
        )
        assert len(hormonal.biomarker_scores) == 1
        assert hormonal.biomarker_scores[0].score > 0
        assert hormonal.biomarker_scores[0].unscored_reason is None

    def test_fixture_policy_has_no_thyroid_markers(self, fixture_policy_path):
        policy = scoring_policy_registry.load_scoring_policy()
        biomarker_ids = set(policy.raw.get("biomarkers", {}).keys())
        thyroid_ids = {"tsh", "free_t3", "free_t4", "ft3", "ft4"}
        assert biomarker_ids.isdisjoint(thyroid_ids)


class TestProductionPolicyUnchanged:
    def test_production_policy_has_no_lab_range_only_entries(self):
        _reset_policy_cache()
        policy = scoring_policy_registry.load_scoring_policy()
        for biomarker_id, spec in policy.raw.get("biomarkers", {}).items():
            assert spec.get("scoring_type", SCORING_TYPE_RANGE_POSITION) == SCORING_TYPE_RANGE_POSITION, (
                f"Unexpected scoring_type on production biomarker {biomarker_id}"
            )

    def test_production_hormonal_rail_still_inert(self):
        _reset_policy_cache()
        policy = scoring_policy_registry.load_scoring_policy()
        hormonal = policy.raw["systems"]["hormonal"]
        assert hormonal["biomarkers"] == []
        assert hormonal["system_weight"] == 0.0
