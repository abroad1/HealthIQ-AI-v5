"""
LC-S8 — Biomarker unit / reference range normalisation and scoring coherence.

Defect class: biomarker_value_reference_unit_incoherence

Guards:
  - Layer A converts g/L <-> g/dL (hemoglobin) and L/L <-> % (hematocrit) including one-sided refs.
  - Scoring returns unit_reference_range_incoherent when value vs lab ref units have no registry path.
  - HbA1c % vs mmol/mol remains harmonised before the coherence gate (no regression).
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.scoring.rules import (
    ScoringRules,
    ScoreRange,
    UNSCORED_REASON_UNIT_REFERENCE_RANGE_INCOHERENT,
)
from core.units.registry import (
    apply_unit_normalisation,
    value_and_reference_units_coherent_for_numeric_compare,
)


@pytest.mark.regression
class TestLC_S8UnitNormalisation:
    def test_hemoglobin_two_sided_ref_g_L_value_g_dL(self):
        out = apply_unit_normalisation(
            {
                "hemoglobin": {
                    "value": 14.0,
                    "unit": "g/dL",
                    "reference_range": {
                        "min": 135.0,
                        "max": 175.0,
                        "unit": "g/L",
                        "source": "lab",
                    },
                }
            }
        )
        row = out["hemoglobin"]
        assert row["unit"] == "g/dL"
        assert abs(float(row["value"]) - 14.0) < 1e-5
        ref = row["reference_range"]
        assert ref is not None
        assert ref["unit"] == "g/dL"
        assert abs(float(ref["min"]) - 13.5) < 0.02
        assert abs(float(ref["max"]) - 17.5) < 0.02

    def test_hematocrit_L_L_two_sided_ref_percent(self):
        out = apply_unit_normalisation(
            {
                "hematocrit": {
                    "value": 0.438,
                    "unit": "L/L",
                    "reference_range": {
                        "min": 40.0,
                        "max": 54.0,
                        "unit": "%",
                        "source": "lab",
                    },
                }
            }
        )
        row = out["hematocrit"]
        assert row["unit"] == "%"
        assert abs(float(row["value"]) - 43.8) < 0.02
        ref = row["reference_range"]
        assert ref is not None
        assert ref["unit"] == "%"
        assert abs(float(ref["min"]) - 40.0) < 0.02
        assert abs(float(ref["max"]) - 54.0) < 0.02

    def test_hemoglobin_one_sided_min_ref_converts_to_base(self):
        out = apply_unit_normalisation(
            {
                "hemoglobin": {
                    "value": 135.0,
                    "unit": "g/L",
                    "reference_range": {"min": 12.0, "unit": "g/dL", "source": "lab"},
                }
            }
        )
        row = out["hemoglobin"]
        assert row["unit"] == "g/dL"
        assert abs(float(row["value"]) - 13.5) < 0.02
        ref = row["reference_range"]
        assert ref is not None
        assert ref.get("max") is None
        assert ref["unit"] == "g/dL"
        assert abs(float(ref["min"]) - 12.0) < 0.02

    def test_hemoglobin_uk_g_L_panel_stays_coherent(self):
        """144 g/L with 130–175 g/L (UK AB) — both mass concentration in g/L before base g/dL."""
        out = apply_unit_normalisation(
            {
                "hemoglobin": {
                    "value": 144.0,
                    "unit": "g/L",
                    "reference_range": {
                        "min": 130.0,
                        "max": 175.0,
                        "unit": "g/L",
                        "source": "lab",
                    },
                }
            }
        )
        row = out["hemoglobin"]
        assert row["unit"] == "g/dL"
        assert abs(float(row["value"]) - 14.4) < 0.02
        ref = row["reference_range"]
        assert ref is not None and ref["unit"] == "g/dL"
        assert abs(float(ref["min"]) - 13.0) < 0.02
        assert abs(float(ref["max"]) - 17.5) < 0.02

    def test_hemoglobin_mixed_g_dL_value_g_L_range_converts(self):
        out = apply_unit_normalisation(
            {
                "hemoglobin": {
                    "value": 14.4,
                    "unit": "g/dL",
                    "reference_range": {
                        "min": 130.0,
                        "max": 175.0,
                        "unit": "g/L",
                        "source": "lab",
                    },
                }
            }
        )
        row = out["hemoglobin"]
        assert row["unit"] == "g/dL"
        ref = row["reference_range"]
        assert ref is not None and ref["unit"] == "g/dL"
        assert abs(float(ref["min"]) - 13.0) < 0.02
        assert abs(float(ref["max"]) - 17.5) < 0.02

    def test_hematocrit_L_L_homogeneous_range(self):
        out = apply_unit_normalisation(
            {
                "hematocrit": {
                    "value": 0.438,
                    "unit": "L/L",
                    "reference_range": {
                        "min": 0.35,
                        "max": 0.48,
                        "unit": "L/L",
                        "source": "lab",
                    },
                }
            }
        )
        row = out["hematocrit"]
        assert row["unit"] == "%"
        assert abs(float(row["value"]) - 43.8) < 0.02
        ref = row["reference_range"]
        assert ref is not None and ref["unit"] == "%"
        assert abs(float(ref["min"]) - 35.0) < 0.02
        assert abs(float(ref["max"]) - 48.0) < 0.02


@pytest.mark.regression
class TestLC_S8ScoringCoherence:
    def test_hemoglobin_incompatible_units_unscored(self):
        rules = ScoringRules()
        score, band, reason = rules.calculate_biomarker_score(
            "hemoglobin",
            14.0,
            input_reference_range={
                "min": 8.0,
                "max": 11.0,
                "unit": "mmol/L",
                "source": "lab",
            },
            value_unit="g/dL",
        )
        assert score == 0.0
        assert band == ScoreRange.CRITICAL
        assert reason == UNSCORED_REASON_UNIT_REFERENCE_RANGE_INCOHERENT

    def test_hemoglobin_coherent_g_dL_scores(self):
        rules = ScoringRules()
        score, band, reason = rules.calculate_biomarker_score(
            "hemoglobin",
            14.0,
            input_reference_range={
                "min": 12.0,
                "max": 18.0,
                "unit": "g/dL",
                "source": "lab",
            },
            value_unit="g/dL",
        )
        assert reason is None
        assert band != ScoreRange.CRITICAL or score > 0
        assert 0.0 <= score <= 100.0

    def test_hba1c_percent_value_mmol_mol_ref_harmonised_then_scores(self):
        rules = ScoringRules()
        score, band, reason = rules.calculate_biomarker_score(
            "hba1c",
            6.5,
            input_reference_range={
                "min": 48.0,
                "max": 52.0,
                "unit": "mmol/mol",
                "source": "lab",
            },
            value_unit="%",
        )
        assert reason is None
        assert 0.0 <= score <= 100.0


@pytest.mark.regression
class TestLC_S8CoherenceHelper:
    def test_helper_false_for_hemoglobin_mmol_vs_g_dL(self):
        assert not value_and_reference_units_coherent_for_numeric_compare(
            "hemoglobin", "g/dL", "mmol/L"
        )

    def test_helper_true_for_hemoglobin_g_L_vs_g_dL(self):
        assert value_and_reference_units_coherent_for_numeric_compare(
            "hemoglobin", "g/dL", "g/L"
        )
