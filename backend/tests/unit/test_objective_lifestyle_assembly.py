"""CONTEXT-HARDENING-B — orchestrator objective lifestyle_inputs assembly."""

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
