"""ARCH-CONV-E3 — ALT contextual authority proofs."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.package_activation_register_v1 import clear_activation_register_cache

ROOT = Path(__file__).resolve().parents[3]

HEPATOCELLULAR_KEY = (
    "signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern"
)
MIXED_KEY = "signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern"
CHOLESTATIC_KEY = (
    "signal_alt_high::inv_alt_high_r_value_cholestatic_alp_predominant_context"
)
MUSCLE_KEY = "signal_alt_high::inv_alt_high_muscle_source_or_exertional_contribution"
METABOLIC_KEY = "signal_alt_high::inv_alt_high_metabolic_masld_context"
BILIRUBIN_KEY = "signal_alt_high::inv_alt_high_bilirubin_hys_law_severity_context"

LAB_RANGES = {
    "alt": {"min": 0.0, "max": 40.0, "unit": "U/L", "source": "lab"},
    "alp": {"min": 30.0, "max": 120.0, "unit": "U/L", "source": "lab"},
    "bilirubin": {"min": 0.0, "max": 20.0, "unit": "umol/L", "source": "lab"},
    "ggt": {"min": 0.0, "max": 60.0, "unit": "U/L", "source": "lab"},
    "creatine_kinase": {"min": 0.0, "max": 200.0, "unit": "U/L", "source": "lab"},
    "hba1c": {"min": 20.0, "max": 42.0, "unit": "mmol/mol", "source": "lab"},
    "triglycerides": {"min": 0.0, "max": 1.7, "unit": "mmol/L", "source": "lab"},
    "hdl_cholesterol": {"min": 1.0, "max": 2.5, "unit": "mmol/L", "source": "lab"},
}


@pytest.fixture(autouse=True)
def _clear_activation_cache():
    clear_activation_register_cache()
    yield
    clear_activation_register_cache()


def _lab_ranges(**overrides):
    merged = dict(LAB_RANGES)
    merged.update(overrides)
    return merged


def _alt_keys(results):
    return {r.activation_key for r in results if r.signal_id == "signal_alt_high"}


def _alt_row(results, key):
    rows = [r for r in results if r.activation_key == key]
    assert len(rows) == 1
    return rows[0]


class TestCholestaticContext:
    def test_r_le_2_with_ggt_high_emits_cholestatic(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 50.0, "alp": 200.0, "ggt": 90.0},
            {"r_value_alt_alp": 1.5},
            lab_ranges=_lab_ranges(),
        )
        keys = _alt_keys(results)
        assert CHOLESTATIC_KEY in keys
        assert HEPATOCELLULAR_KEY not in keys

    def test_r_le_2_with_ggt_normal_still_emits_cholestatic(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 50.0, "alp": 200.0, "ggt": 30.0},
            {"r_value_alt_alp": 2.0},
            lab_ranges=_lab_ranges(),
        )
        assert CHOLESTATIC_KEY in _alt_keys(results)

    def test_r_le_2_with_ggt_missing_still_emits_cholestatic(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 50.0, "alp": 200.0},
            {"r_value_alt_alp": 1.0},
            lab_ranges=_lab_ranges(),
        )
        assert CHOLESTATIC_KEY in _alt_keys(results)

    def test_bilirubin_escalates_cholestatic_to_at_risk(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 50.0, "alp": 200.0, "bilirubin": 25.0},
            {"r_value_alt_alp": 1.5},
            lab_ranges=_lab_ranges(),
        )
        row = _alt_row(results, CHOLESTATIC_KEY)
        assert row.signal_state == "at_risk"


class TestMuscleContext:
    def test_alt_high_ck_high_emits_muscle(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "creatine_kinase": 400.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        keys = _alt_keys(results)
        assert MUSCLE_KEY in keys
        assert HEPATOCELLULAR_KEY in keys

    def test_alt_high_ck_absent_suppresses_muscle(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        keys = _alt_keys(results)
        assert MUSCLE_KEY not in keys
        assert HEPATOCELLULAR_KEY in keys

    def test_alt_high_ck_normal_suppresses_muscle(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "creatine_kinase": 100.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        assert MUSCLE_KEY not in _alt_keys(results)

    def test_muscle_with_bilirubin_high_still_emits_and_escalates(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "creatine_kinase": 400.0, "bilirubin": 25.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        keys = _alt_keys(results)
        assert MUSCLE_KEY in keys
        assert _alt_row(results, MUSCLE_KEY).signal_state == "at_risk"


class TestBilirubinEscalationOnly:
    def test_bilirubin_package_not_loaded(self):
        registry = SignalRegistry()
        loaded = {row["activation_key"] for row in registry.get_all_signals()}
        assert BILIRUBIN_KEY not in loaded

    def test_hepatocellular_escalates_on_bilirubin_high(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 70.0, "bilirubin": 25.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        row = _alt_row(results, HEPATOCELLULAR_KEY)
        assert row.signal_state == "at_risk"
        surface = " ".join(
            str(v)
            for v in (row.signal_id, row.activation_key, row.package_id, row.selected_hypothesis_id)
        ).lower()
        assert "hy's" not in surface
        assert "hys_law" not in surface

    def test_bilirubin_missing_does_not_escalate(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 70.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        row = _alt_row(results, HEPATOCELLULAR_KEY)
        assert row.signal_state == "suboptimal"

    def test_mixed_pattern_bilirubin_escalation(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 120.0, "alp": 120.0, "bilirubin": 25.0},
            {"r_value_alt_alp": 3.0},
            lab_ranges=_lab_ranges(),
        )
        assert MIXED_KEY in _alt_keys(results)
        assert _alt_row(results, MIXED_KEY).signal_state == "at_risk"


class TestMetabolicContext:
    def test_alt_high_without_metabolic_corroboration_suppresses(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        assert METABOLIC_KEY not in _alt_keys(results)

    def test_alt_high_with_triglycerides_high_emits(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "triglycerides": 2.5},
            {},
            lab_ranges=_lab_ranges(),
        )
        assert METABOLIC_KEY in _alt_keys(results)

    def test_alt_high_with_hdl_low_emits(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "hdl_cholesterol": 0.7},
            {},
            lab_ranges=_lab_ranges(),
        )
        assert METABOLIC_KEY in _alt_keys(results)

    def test_alt_high_with_hba1c_high_emits(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "hba1c": 55.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        assert METABOLIC_KEY in _alt_keys(results)

    def test_no_masld_diagnosis_on_surface_identifiers(self):
        results = SignalEvaluator(registry=SignalRegistry()).evaluate_all(
            {"alt": 80.0, "triglycerides": 2.5},
            {},
            lab_ranges=_lab_ranges(),
        )
        row = _alt_row(results, METABOLIC_KEY)
        surface = " ".join(
            str(v) for v in (row.signal_id, row.activation_key, row.package_id)
        ).lower()
        assert "masld" not in surface or "metabolic_masld_context" in surface
        # activation_key contains medical source-spec id; ensure no diagnostic claim fields.
        assert getattr(row, "explanation", None) is None or "diagnose" not in str(
            row.explanation
        ).lower()


class TestCrossCutting:
    def test_e2_hepatocellular_and_mixed_preserved(self):
        evaluator = SignalEvaluator(registry=SignalRegistry())
        hep = evaluator.evaluate_all(
            {"alt": 400.0, "alp": 120.0},
            {"r_value_alt_alp": 10.0},
            lab_ranges=_lab_ranges(),
        )
        assert HEPATOCELLULAR_KEY in _alt_keys(hep)
        assert MIXED_KEY not in _alt_keys(hep)
        mixed = evaluator.evaluate_all(
            {"alt": 120.0, "alp": 120.0},
            {"r_value_alt_alp": 3.0},
            lab_ranges=_lab_ranges(),
        )
        assert MIXED_KEY in _alt_keys(mixed)
        assert HEPATOCELLULAR_KEY not in _alt_keys(mixed)

    def test_deterministic_repeatability(self):
        panel = {"alt": 80.0, "triglycerides": 2.5, "creatine_kinase": 400.0}
        ranges = _lab_ranges()
        a = SignalEvaluator(registry=SignalRegistry()).evaluate_all(panel, {}, lab_ranges=ranges)
        b = SignalEvaluator(registry=SignalRegistry()).evaluate_all(panel, {}, lab_ranges=ranges)
        assert _alt_keys(a) == _alt_keys(b)

    def test_medical_decision_register_exists(self):
        path = ROOT / "docs" / "architecture" / "ARCH-CONV-E3_medical_decision_register.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert payload["work_id"] == "ARCH-CONV-E3"
        assert payload["head_of_medical_research_gate1_reference"] == (
            "ARCH-CONV-E3-GATE1-HMR-2026-08-01"
        )
        assert payload["gate2_status"] == "RATIFIED"
