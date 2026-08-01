"""ARCH-CONV-E2 — r_value_alt_alp metric, band selection, and collision coexistence."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.ratio_registry import (
    classify_r_value_alt_alp,
    compute,
)
from core.analytics.signal_authority_collision_resolver import (
    apply_signal_authority_collision_policy,
    load_signal_authority_collision_model,
    validate_signal_authority_collision_model,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.package_activation_register_v1 import clear_activation_register_cache
from core.models.signal import SignalResult

ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = (
    ROOT / "knowledge_bus" / "governance" / "signal_authority_collision_model_v1.yaml"
)

HEPATOCELLULAR_KEY = (
    "signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern"
)
MIXED_KEY = "signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern"
CHOLESTATIC_KEY = (
    "signal_alt_high::inv_alt_high_r_value_cholestatic_alp_predominant_context"
)
S24_ALT_KEY = "signal_alt_high::inv_alt_high_hepatocellular_injury"
ALP_KEY = "signal_alp_high::inv_alp_high_bone_biliary"
GGT_KEY = "signal_ggt_high::inv_ggt_high_hepatic"

LAB_RANGES = {
    "alt": {"min": 0.0, "max": 40.0, "unit": "U/L", "source": "lab"},
    "alp": {"min": 30.0, "max": 120.0, "unit": "U/L", "source": "lab"},
    "bilirubin": {"min": 0.0, "max": 20.0, "unit": "umol/L", "source": "lab"},
    "ggt": {"min": 0.0, "max": 60.0, "unit": "U/L", "source": "lab"},
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


class TestRValueMetric:
    def test_formula_correctness(self):
        # ALT 400 / 40 = 10x ULN; ALP 120 / 120 = 1x ULN → R = 10
        out = compute(
            {"alt": 400.0, "alp": 120.0},
            reference_ranges=_lab_ranges(),
        )
        entry = out["derived"]["r_value_alt_alp"]
        assert entry["value"] == pytest.approx(10.0, abs=0.001)
        assert entry["source"] == "computed"
        assert entry["classification"] == "hepatocellular"
        assert entry["uln_inputs"]["pairing"] == "same_panel_snapshot"
        assert entry["uln_inputs"]["uln_source"] == "lab"

    @pytest.mark.parametrize(
        "r,expected",
        [
            (1.999, "cholestatic_alp_predominant"),
            (2.0, "cholestatic_alp_predominant"),
            (2.001, "mixed"),
            (4.999, "mixed"),
            (5.0, "hepatocellular"),
            (5.001, "hepatocellular"),
        ],
    )
    def test_classify_boundaries(self, r, expected):
        assert classify_r_value_alt_alp(r) == expected

    @pytest.mark.parametrize(
        "alt,alp,expected_class",
        [
            (80.0, 120.0, "cholestatic_alp_predominant"),  # R = 2.0
            (81.0, 120.0, "mixed"),  # R = 2.025
            (199.0, 120.0, "mixed"),  # R = 4.975
            (200.0, 120.0, "hepatocellular"),  # R = 5.0
        ],
    )
    def test_computed_boundary_cases(self, alt, alp, expected_class):
        out = compute(
            {"alt": alt, "alp": alp},
            reference_ranges=_lab_ranges(),
        )
        entry = out["derived"]["r_value_alt_alp"]
        assert entry["classification"] == expected_class
        assert classify_r_value_alt_alp(entry["value"]) == expected_class

    def test_missing_alt_fails_closed(self):
        out = compute({"alp": 120.0}, reference_ranges=_lab_ranges())
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "alt_result_missing"

    def test_missing_alp_fails_closed(self):
        out = compute({"alt": 80.0}, reference_ranges=_lab_ranges())
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "alp_result_missing"

    def test_missing_alt_uln_fails_closed(self):
        ranges = _lab_ranges()
        del ranges["alt"]
        out = compute({"alt": 80.0, "alp": 120.0}, reference_ranges=ranges)
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "alt_uln_missing"

    def test_missing_alp_uln_fails_closed(self):
        ranges = _lab_ranges()
        del ranges["alp"]
        out = compute({"alt": 80.0, "alp": 120.0}, reference_ranges=ranges)
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "alp_uln_missing"

    def test_zero_uln_fails_closed(self):
        out = compute(
            {"alt": 80.0, "alp": 120.0},
            reference_ranges=_lab_ranges(
                alt={"min": 0.0, "max": 0.0, "unit": "U/L", "source": "lab"}
            ),
        )
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] in {
            "alt_uln_invalid_bounds",
            "alt_uln_non_positive",
        }

    def test_non_lab_uln_fails_closed(self):
        out = compute(
            {"alt": 80.0, "alp": 120.0},
            reference_ranges=_lab_ranges(
                alt={"min": 0.0, "max": 40.0, "unit": "U/L", "source": "ratio_registry"}
            ),
        )
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "alt_uln_not_lab_source"

    def test_no_reference_ranges_fails_closed(self):
        out = compute({"alt": 80.0, "alp": 120.0})
        assert "r_value_alt_alp" not in out["derived"]
        assert out["omitted"]["r_value_alt_alp"] == "reference_ranges_missing"

    def test_deterministic_repeatability(self):
        panel = {"alt": 160.0, "alp": 120.0}
        ranges = _lab_ranges()
        a = compute(panel, reference_ranges=ranges)
        b = compute(panel, reference_ranges=ranges)
        assert a["derived"]["r_value_alt_alp"] == b["derived"]["r_value_alt_alp"]
        assert a["omitted"] == b["omitted"]


def _signal_row(activation_key: str, signal_id: str, package_id: str) -> SignalResult:
    source_spec_id = activation_key.split("::", 1)[1]
    primary = "alt" if signal_id == "signal_alt_high" else signal_id.replace("signal_", "").replace("_high", "")
    return SignalResult(
        signal_id=signal_id,
        activation_key=activation_key,
        source_spec_id=source_spec_id,
        package_id=package_id,
        system="hepatic",
        signal_state="suboptimal",
        signal_value=100.0,
        primary_metric=primary,
    )


class TestCollisionAndFrameSelection:
    def test_collision_model_loads_with_alt_axis(self):
        model = load_signal_authority_collision_model(model_path=MODEL_PATH)
        validate_signal_authority_collision_model(model, model_path=MODEL_PATH)
        group_ids = {g["authority_group_id"] for g in model["authority_groups"]}
        assert "liver_injury_axis" in group_ids
        assert "alt_biochemical_pattern_axis" in group_ids

    def test_alp_ggt_suppression_preserved_with_s24_alt_present(self):
        results = [
            _signal_row(ALP_KEY, "signal_alp_high", "pkg_s24_alp_high_bone_biliary"),
            _signal_row(GGT_KEY, "signal_ggt_high", "pkg_s24_ggt_high_hepatic"),
            _signal_row(
                S24_ALT_KEY,
                "signal_alt_high",
                "pkg_s24_alt_high_hepatocellular_injury",
            ),
        ]
        filtered = apply_signal_authority_collision_policy(
            results,
            signal_biomarkers={"alp": 200.0, "ggt": 100.0, "alt": 400.0},
            signal_derived={"r_value_alt_alp": 10.0},
            lab_ranges=_lab_ranges(),
            model_path=MODEL_PATH,
        )
        keys = {row.activation_key for row in filtered}
        assert ALP_KEY in keys
        assert S24_ALT_KEY in keys
        assert GGT_KEY not in keys

    def test_s24_alt_loads_and_r_value_frames_do_not(self):
        registry = SignalRegistry()
        loaded = {row["activation_key"] for row in registry.get_all_signals()}
        assert S24_ALT_KEY in loaded
        assert HEPATOCELLULAR_KEY not in loaded
        assert MIXED_KEY not in loaded
        assert CHOLESTATIC_KEY not in loaded
        alt = [row for row in registry.get_all_signals() if row["signal_id"] == "signal_alt_high"]
        assert [row["activation_key"] for row in alt] == [S24_ALT_KEY]

    def test_evaluator_emits_s24_alt_even_when_r_value_present(self):
        """Foundational ALT-high must not be suppressed when R-value is available."""
        evaluator = SignalEvaluator(registry=SignalRegistry())
        results = evaluator.evaluate_all(
            {"alt": 400.0, "alp": 120.0},
            {"r_value_alt_alp": 10.0},
            lab_ranges=_lab_ranges(),
        )
        alt = [r for r in results if r.signal_id == "signal_alt_high"]
        assert [r.activation_key for r in alt] == [S24_ALT_KEY]

    def test_evaluator_emits_s24_alt_when_r_value_absent(self):
        """Missing ULN/R-value must not suppress foundational ALT-high signalling."""
        evaluator = SignalEvaluator(registry=SignalRegistry())
        results = evaluator.evaluate_all(
            {"alt": 120.0, "alp": 120.0},
            {},
            lab_ranges=_lab_ranges(),
        )
        alt = [r for r in results if r.signal_id == "signal_alt_high"]
        assert [r.activation_key for r in alt] == [S24_ALT_KEY]

    def test_cholestatic_r_value_frame_remains_withheld(self):
        registry = SignalRegistry()
        loaded = {row["activation_key"] for row in registry.get_all_signals()}
        assert CHOLESTATIC_KEY not in loaded

    def test_promotion_decisions_are_recorded(self):
        packages = ROOT / "knowledge_bus" / "packages"
        expected = {
            "pkg_kb52c_alt_high_hepatocellular_injury_pattern": "PROMOTE_BUT_WITHHOLD",
            "pkg_kb52c_alt_high_mixed_biochemical_pattern": "PROMOTE_BUT_WITHHOLD",
            "pkg_kb52c_alt_high_cholestatic_alp_predominant_context": "PROMOTE_BUT_WITHHOLD",
            "pkg_kb52c_alt_high_muscle_source_or_exertional_pattern": "DEFERRED_WITH_EXPLICIT_REASON",
            "pkg_kb52c_alt_high_bilirubin_severity_context": "DEFERRED_WITH_EXPLICIT_REASON",
            "pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern": "PROMOTE_BUT_WITHHOLD",
        }
        for package_id, decision in expected.items():
            payload = yaml.safe_load(
                (packages / package_id / "package_manifest.yaml").read_text(encoding="utf-8")
            )
            assert payload["promotion_decision"] == decision

    def test_gate1_medical_decision_register_records_s24_foundational(self):
        payload = yaml.safe_load(
            (ROOT / "docs" / "architecture" / "ARCH-CONV-E2_medical_decision_register.yaml")
            .read_text(encoding="utf-8")
        )
        assert payload["head_of_medical_research_gate1_reference"] == (
            "ARCH-CONV-E2-GATE1-HMR-2026-07-31"
        )
        assert payload["anthony_gate2_reference"] == "ARCH-CONV-E2-GATE2-ANTHONY-PENDING"
        assert payload["gate1_decisions"]["s24_supersession_by_r_value_frames"] == (
            "NOT_APPROVED"
        )
        assert "foundational active ALT-high authority" in payload["gate1_decision_statement"]
