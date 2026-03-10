import json

import pytest

import core.analytics.scoring_policy_registry as scoring_policy_registry
from core.scoring.rules import ScoringRules, ScoreRange


def _reset_policy_cache() -> None:
    scoring_policy_registry._policy_cache = None


def test_scoring_policy_hash_is_deterministic():
    _reset_policy_cache()
    p1 = scoring_policy_registry.load_scoring_policy()
    _reset_policy_cache()
    p2 = scoring_policy_registry.load_scoring_policy()
    assert p1.stamp.scoring_policy_hash == p2.stamp.scoring_policy_hash
    assert json.dumps(p1.raw, sort_keys=True) == json.dumps(p2.raw, sort_keys=True)


def test_scoring_policy_validation_fails_without_policy_version(tmp_path, monkeypatch):
    bad = tmp_path / "scoring_policy.yaml"
    bad.write_text(
        "schema_version: '1.0'\n"
        "systems: {metabolic: {min_biomarkers_required: 1, system_weight: 1.0, biomarkers: []}}\n"
        "biomarkers: {}\n"
        "status_map: {normal: normal}\n"
        "score_curve: {optimal_band: {min: 0.2, max: 0.8, score: 100.0}}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: bad)
    _reset_policy_cache()
    with pytest.raises(ValueError, match="policy_version"):
        scoring_policy_registry.load_scoring_policy()


def test_scoring_policy_validation_fails_on_invalid_band_range(tmp_path, monkeypatch):
    bad = tmp_path / "scoring_policy.yaml"
    bad.write_text(
        "policy_version: '1.0.0'\n"
        "schema_version: '1.0'\n"
        "systems:\n"
        "  metabolic:\n"
        "    min_biomarkers_required: 1\n"
        "    system_weight: 1.0\n"
        "    biomarkers: [glucose]\n"
        "biomarkers:\n"
        "  glucose:\n"
        "    scoring_type: range_position\n"
        "    weight: 1.0\n"
        "    bands:\n"
        "      optimal: {min: 100, max: 70}\n"
        "      normal: {min: 70, max: 100}\n"
        "      borderline: {min: 100, max: 125}\n"
        "      high: {min: 125, max: 200}\n"
        "      very_high: {min: 200, max: 300}\n"
        "      critical: {min: 300, max: 1000}\n"
        "status_map: {normal: normal}\n"
        "score_curve: {optimal_band: {min: 0.2, max: 0.8, score: 100.0}}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: bad)
    _reset_policy_cache()
    with pytest.raises(ValueError, match="min must be < max"):
        scoring_policy_registry.load_scoring_policy()


def test_scoring_rules_golden_curve_regression_points():
    """
    Golden regression points to prove scoring output continuity.
    These points match legacy piecewise score-curve behavior.
    """
    rules = ScoringRules()
    score_mid, range_mid = rules._calculate_score_from_range(85.0, 70.0, 100.0)
    assert score_mid == pytest.approx(100.0)
    assert range_mid == ScoreRange.OPTIMAL

    score_low_edge, range_low_edge = rules._calculate_score_from_range(73.0, 70.0, 100.0)
    assert score_low_edge == pytest.approx(90.0)
    assert range_low_edge in (ScoreRange.BORDERLINE, ScoreRange.NORMAL)

    score_high_out, range_high_out = rules._calculate_score_from_range(110.0, 70.0, 100.0)
    assert score_high_out == pytest.approx(13.3333333333, rel=1e-6, abs=2e-5)
    assert range_high_out == ScoreRange.CRITICAL


def test_scoring_policy_validation_fails_when_system_execution_order_missing_system(
    tmp_path, monkeypatch
):
    bad = tmp_path / "scoring_policy.yaml"
    bad.write_text(
        "policy_version: '1.0.0'\n"
        "schema_version: '1.0'\n"
        "systems:\n"
        "  metabolic:\n"
        "    min_biomarkers_required: 1\n"
        "    system_weight: 1.0\n"
        "    biomarkers: [glucose]\n"
        "  cardiovascular:\n"
        "    min_biomarkers_required: 1\n"
        "    system_weight: 1.0\n"
        "    biomarkers: [glucose]\n"
        "system_execution_order: [metabolic]\n"
        "biomarkers:\n"
        "  glucose:\n"
        "    scoring_type: range_position\n"
        "    weight: 1.0\n"
        "    bands:\n"
        "      optimal: {min: 70, max: 100}\n"
        "      normal: {min: 70, max: 100}\n"
        "      borderline: {min: 100, max: 125}\n"
        "      high: {min: 125, max: 200}\n"
        "      very_high: {min: 200, max: 300}\n"
        "      critical: {min: 300, max: 1000}\n"
        "status_map: {normal: normal}\n"
        "score_curve: {optimal_band: {min: 0.2, max: 0.8, score: 100.0}}\n"
        "derived_ratio_policy_bounds: {}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(scoring_policy_registry, "_policy_path", lambda: bad)
    _reset_policy_cache()
    with pytest.raises(ValueError, match="system_execution_order must include all systems"):
        scoring_policy_registry.load_scoring_policy()
