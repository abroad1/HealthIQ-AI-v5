"""N-4 — lifestyle interpretation bridge engine (deterministic, no InsightGraph mutation)."""

from __future__ import annotations

from core.analytics.lifestyle_interpretation_bridge_engine import compute_lifestyle_interpretation_bridges_v1


def _ref(lo: float, hi: float) -> dict:
    return {"min": lo, "max": hi, "unit": "x", "source": "lab"}


def test_alcohol_bridge_active_with_coherence():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={"alcohol_units_per_week": 20.0},
        questionnaire_responses={},
        biomarkers={
            "homocysteine": {"value": 18.0, "unit": "umol/L"},
        },
        reference_ranges={
            "homocysteine": _ref(5.0, 15.0),
        },
    )
    assert out["alcohol_methylation_macrocytosis"]["active"] is True
    assert out["alcohol_methylation_macrocytosis"]["alcohol_intake_tier"] == "elevated"


def test_alcohol_bridge_inactive_without_lab_coherence():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={"alcohol_units_per_week": 20.0},
        questionnaire_responses={},
        biomarkers={},
        reference_ranges={},
    )
    assert out["alcohol_methylation_macrocytosis"]["active"] is False
    assert out["alcohol_methylation_macrocytosis"]["rationale_codes"] == []


def test_renal_bridge_active_fluid_and_egfr():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={"fluid_intake_liters": 0.8},
        questionnaire_responses={"daily_fluid_intake": "Less than 1 litre"},
        biomarkers={"egfr": {"value": 88.0}},
        reference_ranges={"egfr": _ref(60.0, 999.0)},
    )
    assert out["hydration_activity_renal"]["active"] is True


def test_renal_bridge_active_high_activity():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={},
        questionnaire_responses={"vigorous_exercise_days": "4+ days"},
        biomarkers={"creatinine": {"value": 88.0, "unit": "umol/L"}},
        reference_ranges={"creatinine": _ref(59.0, 104.0)},
    )
    assert out["hydration_activity_renal"]["active"] is True


def test_renal_bridge_inactive_without_renal_markers():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={"fluid_intake_liters": 0.5},
        questionnaire_responses={},
        biomarkers={"homocysteine": {"value": 10.0}},
        reference_ranges={},
    )
    assert out["hydration_activity_renal"]["active"] is False


def test_glycaemic_fasting_active():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={},
        questionnaire_responses={"dietary_pattern": "Intermittent fasting"},
        biomarkers={"hba1c": {"value": 32.0, "unit": "mmol/mol"}},
        reference_ranges={"hba1c": _ref(20.0, 42.0)},
    )
    assert out["fasting_dietary_glycaemic"]["active"] is True


def test_glycaemic_inactive_without_hba1c():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={},
        questionnaire_responses={"dietary_pattern": "Intermittent fasting"},
        biomarkers={},
        reference_ranges={},
    )
    assert out["fasting_dietary_glycaemic"]["active"] is False


def test_glycaemic_inactive_when_hba1c_high():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={},
        questionnaire_responses={"fasting_hours": "15+ hours"},
        biomarkers={"hba1c": {"value": 50.0, "unit": "mmol/mol"}},
        reference_ranges={"hba1c": _ref(20.0, 42.0)},
    )
    assert out["fasting_dietary_glycaemic"]["active"] is False


def test_trace_version_present():
    out = compute_lifestyle_interpretation_bridges_v1(
        lifestyle_inputs={},
        questionnaire_responses={},
        biomarkers={},
        reference_ranges={},
    )
    assert out["bridge_asset_version"]
    assert out["bridge_asset_id"] == "lifestyle_interpretation_bridges_v1"
    assert len(out["trace"]["inputs_fingerprint_sha256"]) == 64
