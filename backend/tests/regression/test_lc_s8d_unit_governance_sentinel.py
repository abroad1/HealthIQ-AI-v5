"""LC-S8D — Sentinel guardrails for UK/SI unit governance."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.scoring.rules import (
    ScoringRules,
    UNSCORED_REASON_UNKNOWN_UNIT_NOT_SCORED,
)
from core.units.display_policy import load_display_unit_policy
from core.units.registry import apply_unit_normalisation, convert_value


@pytest.mark.regression
class TestLC_S8DUnitGovernanceGuards:
    def test_display_policy_authority_exists(self):
        data = load_display_unit_policy()
        assert data.get("policy_version")
        assert "hba1c" in (data.get("biomarkers") or {})

    def test_phase_a_equivalence_vectors(self):
        assert convert_value("platelets", 225.0, "K/μL")[1] == "10^9/L"
        assert convert_value("white_blood_cells", 6.4, "K/uL")[1] == "10^9/L"
        assert convert_value("sodium", 140.0, "mEq/L")[1] == "mmol/L"

    def test_unknown_unit_not_scored_against_policy(self):
        rules = ScoringRules()
        _, _, reason = rules.calculate_biomarker_score(
            "glucose",
            5.0,
            input_reference_range={"min": 3.0, "max": 6.0, "unit": "g/L", "source": "lab"},
            value_unit="g/L",
        )
        assert reason == UNSCORED_REASON_UNKNOWN_UNIT_NOT_SCORED

    def test_hematocrit_fraction_not_stored_as_percent(self):
        out = apply_unit_normalisation(
            {"hematocrit": {"value": 0.438, "unit": "L/L", "reference_range": None}}
        )
        assert out["hematocrit"]["unit"] == "L/L"
        assert out["hematocrit"]["value"] == pytest.approx(0.438, abs=0.001)

    def test_bun_alias_maps_to_urea_not_urate(self):
        from core.canonical.normalize import normalize_biomarkers_with_metadata

        out = normalize_biomarkers_with_metadata({"BUN": {"value": 7.0, "unit": "mmol/L"}})
        assert "urea" in out
        assert "urate" not in out
