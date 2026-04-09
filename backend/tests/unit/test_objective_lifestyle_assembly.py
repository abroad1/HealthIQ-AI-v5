"""CONTEXT-HARDENING-B/C — orchestrator lifestyle_inputs assembly."""

from core.analytics.lifestyle_modifier_engine import LifestyleModifierEngine
from core.analytics.lifestyle_registry_loader import load_lifestyle_registry
from core.pipeline.orchestrator import AnalysisOrchestrator


def test_assemble_merges_demographics_and_questionnaire_objective():
    orch = AnalysisOrchestrator()
    ud = {"height_cm": 180.0, "weight_kg": 80.0}
    q = {
        "waist_circumference": 34.0,
        "blood_pressure_reading": {"Systolic (mmHg)": 135, "Diastolic (mmHg)": 88},
    }
    out = orch._assemble_objective_lifestyle_inputs(ud, q)
    assert out["height_cm"] == 180.0
    assert out["weight_kg"] == 80.0
    assert abs(out["waist_circumference_cm"] - 34.0 * 2.54) < 1e-6
    assert out["systolic_bp"] == 135.0
    assert out["diastolic_bp"] == 88.0


def test_assemble_height_weight_aliases_from_user_data():
    orch = AnalysisOrchestrator()
    ud = {"height": 175.0, "weight": 72.0}
    out = orch._assemble_objective_lifestyle_inputs(ud, None)
    assert out == {"height_cm": 175.0, "weight_kg": 72.0}


def test_assemble_questionnaire_only_waist():
    orch = AnalysisOrchestrator()
    ud = {}
    q = {"waist_circumference": {"Waist circumference (cm)": 88.0}}
    out = orch._assemble_objective_lifestyle_inputs(ud, q)
    assert out == {"waist_circumference_cm": 88.0}


def test_assemble_user_waist_cm_alias_maps_to_canonical_engine_key():
    orch = AnalysisOrchestrator()
    ud = {"waist_cm": 88.0}
    out = orch._assemble_objective_lifestyle_inputs(ud, None)
    assert out == {"waist_circumference_cm": 88.0}


def test_assemble_canonical_waist_wins_over_conflicting_legacy():
    orch = AnalysisOrchestrator()
    ud = {"waist_circumference_cm": 90.0, "waist_cm": 12.0}
    out = orch._assemble_objective_lifestyle_inputs(ud, None)
    assert out == {"waist_circumference_cm": 90.0}


def test_assemble_merges_questionnaire_behavioural_engine_keys():
    """CONTEXT-HARDENING-C — smoking/alcohol/sleep from questionnaire appear in lifestyle_inputs assembly."""
    orch = AnalysisOrchestrator()
    ud = {"height_cm": 180.0, "weight_kg": 75.0}
    q = {
        "tobacco_use": "Daily use",
        "alcohol_drinks_weekly": "8-14 drinks",
        "sleep_hours_nightly": "Less than 5 hours",
    }
    out = orch._assemble_objective_lifestyle_inputs(ud, q)
    assert out["height_cm"] == 180.0
    assert out["smoking_status"] == "current"
    assert out["alcohol_units_per_week"] == 11.0
    assert out["sleep_hours"] == 4.5


def test_assemble_questionnaire_behavioural_overwrites_user_baseline():
    orch = AnalysisOrchestrator()
    ud = {
        "height_cm": 170.0,
        "weight_kg": 70.0,
        "sleep_hours": 8.0,
        "alcohol_units_per_week": 0.0,
    }
    q = {"sleep_hours_nightly": "5-6 hours", "alcohol_drinks_weekly": "15+ drinks"}
    out = orch._assemble_objective_lifestyle_inputs(ud, q)
    assert out["sleep_hours"] == 5.5
    assert out["alcohol_units_per_week"] == 20.0


def test_assembled_behavioural_inputs_activate_engine_smoking_modifier():
    """Downstream LifestyleModifierEngine consumes questionnaire-sourced smoking_status."""
    orch = AnalysisOrchestrator()
    ud = {"height_cm": 180.0, "weight_kg": 80.0}
    q = {"tobacco_use": "Daily use"}
    li = orch._assemble_objective_lifestyle_inputs(ud, q)
    engine = LifestyleModifierEngine(load_lifestyle_registry())
    result = engine.apply({"cardiovascular": 0.1, "metabolic": 0.1}, li)
    cardio = result["system_modifiers"].get("cardiovascular", {})
    names = [c["input"] for c in cardio.get("contributions", [])]
    assert "smoking_status" in names
