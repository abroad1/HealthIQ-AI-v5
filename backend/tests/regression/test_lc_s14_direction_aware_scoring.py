"""
LC-S14 — Direction-aware scoring framework regression.

Governed biomarker_directionality policy replaces hardcoded per-marker scoring exceptions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import pytest
import yaml

from core.analytics.scoring_policy_registry import load_scoring_policy
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.scoring.rules import ScoreRange, ScoringRules
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)
_RULES_PATH = _REPO_ROOT / "backend" / "core" / "scoring" / "rules.py"


def _lab_ref(min_v: float, max_v: float, unit: str = "U/L") -> Dict[str, Any]:
    return {"min": min_v, "max": max_v, "unit": unit, "source": "lab"}


def _score(name: str, value: float, ref: Dict[str, Any]) -> Tuple[float, ScoreRange]:
    rules = ScoringRules()
    score, score_range, unscored = rules.calculate_biomarker_score(
        name, value, input_reference_range=ref
    )
    assert unscored is None, f"{name} unscored: {unscored}"
    return float(score), score_range


def _harmonise_test_panel_units(biomarkers: Dict[str, Any]) -> None:
    for entry in biomarkers.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("unit") == "\u03bcmol/L":
            entry["unit"] = "\u00b5mol/L"
        rr = entry.get("reference_range")
        if isinstance(rr, dict) and rr.get("unit") == "\u03bcmol/L":
            rr["unit"] = "\u00b5mol/L"


def _prepare_ab_fixture_panel() -> Dict[str, Any]:
    raw = json.loads(_AB_PANEL.read_text(encoding="utf-8"))
    biomarkers = dict(raw["biomarkers"])
    _harmonise_test_panel_units(biomarkers)
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


@pytest.mark.regression
def test_lc_s14_no_hardcoded_alt_bypass_in_rules() -> None:
    text = _RULES_PATH.read_text(encoding="utf-8")
    assert 'biomarker_name == "alt"' not in text
    assert "biomarker_name == 'alt'" not in text


@pytest.mark.regression
@pytest.mark.parametrize(
    "marker,value,ref",
    [
        ("alt", 7.0, _lab_ref(10.0, 49.0)),
        ("ast", 5.0, _lab_ref(10.0, 40.0)),
        ("ggt", 8.0, _lab_ref(10.0, 60.0)),
        ("alp", 30.0, _lab_ref(40.0, 130.0)),
    ],
)
def test_lc_s14_low_enzyme_not_critical(marker: str, value: float, ref: Dict[str, Any]) -> None:
    score, score_range = _score(marker, value, ref)
    assert score_range != ScoreRange.CRITICAL
    assert score >= 45.0


@pytest.mark.regression
@pytest.mark.parametrize(
    "marker,value,ref",
    [
        ("alt", 120.0, _lab_ref(10.0, 49.0)),
        ("ast", 80.0, _lab_ref(10.0, 40.0)),
        ("ggt", 90.0, _lab_ref(10.0, 60.0)),
        ("alp", 200.0, _lab_ref(40.0, 130.0)),
    ],
)
def test_lc_s14_high_enzyme_remains_concerning(marker: str, value: float, ref: Dict[str, Any]) -> None:
    score, score_range = _score(marker, value, ref)
    assert score < 70.0
    assert score_range in (ScoreRange.CRITICAL, ScoreRange.HIGH, ScoreRange.VERY_HIGH)


@pytest.mark.regression
def test_lc_s14_protective_high_hdl_and_apoa1() -> None:
    hdl_score, hdl_range = _score("hdl_cholesterol", 2.0, _lab_ref(1.0, 1.5, "mmol/L"))
    assert hdl_score >= 90.0
    assert hdl_range in (ScoreRange.OPTIMAL, ScoreRange.NORMAL)

    apo_score, apo_range = _score("apoa1", 1.8, _lab_ref(0.79, 1.69, "g/L"))
    assert apo_score >= 90.0
    assert apo_range in (ScoreRange.OPTIMAL, ScoreRange.NORMAL)


@pytest.mark.regression
def test_lc_s14_low_protective_markers_remain_concerning() -> None:
    hdl_score, hdl_range = _score("hdl_cholesterol", 0.8, _lab_ref(1.0, 1.5, "mmol/L"))
    assert hdl_score < 70.0
    assert hdl_range == ScoreRange.CRITICAL

    apo_score, apo_range = _score("apoa1", 0.5, _lab_ref(0.79, 1.69, "g/L"))
    assert apo_score < 70.0
    assert apo_range == ScoreRange.CRITICAL


@pytest.mark.regression
def test_lc_s14_bidirectional_marker_unchanged_symmetric() -> None:
    """Glucose without directionality override keeps symmetric high-side concern."""
    ref = _lab_ref(3.9, 5.6, "mmol/L")
    low_score, _ = _score("glucose", 3.0, ref)
    high_score, high_range = _score("glucose", 8.0, ref)
    assert low_score < high_score or high_range in (ScoreRange.CRITICAL, ScoreRange.HIGH)
    assert ScoringRules().get_biomarker_direction_class("glucose") == "bidirectional_concern"


@pytest.mark.regression
def test_lc_s14_directionality_policy_loaded_from_ssot() -> None:
    policy = load_scoring_policy()
    block = policy.raw.get("biomarker_directionality") or {}
    assert block.get("default_class") == "bidirectional_concern"
    markers = block.get("markers") or {}
    assert markers.get("alt", {}).get("direction_class") == "high_only_concern"
    assert markers.get("hdl_cholesterol", {}).get("direction_class") == "protective_high"


@pytest.mark.regression
def test_lc_s14_invalid_direction_class_rejected_by_policy_validator() -> None:
    path = _REPO_ROOT / "backend" / "ssot" / "scoring_policy.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw = dict(raw)
    block = dict(raw.get("biomarker_directionality") or {})
    markers = dict(block.get("markers") or {})
    markers["alt"] = {"direction_class": "not_a_real_class"}
    block["markers"] = markers
    raw["biomarker_directionality"] = block

    from core.analytics import scoring_policy_registry as reg

    reg._policy_cache = None
    try:
        with pytest.raises(ValueError, match="allowed_classes"):
            reg._validate_policy(raw)
    finally:
        reg._policy_cache = None


@pytest.mark.regression
def test_lc_s14_orchestrator_ab_homocysteine_lead_preserved() -> None:
    dto = AnalysisOrchestrator().run(
        _prepare_ab_fixture_panel(),
        {"age": 45, "sex": "male"},
        assume_canonical=True,
        fixed_analysis_id="lc-s14-ab-lead",
    )
    assert dto.status == "completed"
    meta = dto.meta or {}
    wave1 = meta.get("wave1_aligned_drivers") or {}
    drivers = wave1.get("drivers") if isinstance(wave1, dict) else []
    if isinstance(drivers, list):
        joined = " ".join(str(d) for d in drivers).lower()
        assert "homocysteine" in joined or dto.primary_driver_system_id


@pytest.mark.regression
def test_lc_s14_lab_range_authority_unchanged() -> None:
    rules = ScoringRules()
    score, score_range, reason = rules.calculate_biomarker_score("glucose", 5.0, input_reference_range=None)
    assert reason is not None
    assert score_range == ScoreRange.CRITICAL
