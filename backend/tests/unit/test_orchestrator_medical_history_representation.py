"""MEDICATION-CAVEAT-A — pipeline medical_history dict completeness (no DB)."""

from core.pipeline.orchestrator import AnalysisOrchestrator


def test_create_analysis_context_medical_history_includes_qrisk_and_long_term_classes():
    orchestrator = AnalysisOrchestrator()
    q = {
        "biological_sex": "Male",
        "date_of_birth": "1988-05-15",
        "height": {"Feet": 5, "Inches": 10},
        "weight": {"Weight (lbs)": 175},
        "ethnicity": "White/Caucasian",
        "chronic_conditions": ["None"],
        "current_medications": "None",
        "long_term_medications": ["Corticosteroids"],
        "medical_conditions": ["None"],
        "regular_migraines": "No",
        "supplements": ["Vitamin D"],
    }
    biomarkers = {
        "total_cholesterol": {"value": 180, "unit": "mg/dL"},
        "hdl_cholesterol": {"value": 45, "unit": "mg/dL"},
    }
    context = orchestrator.create_analysis_context(
        analysis_id="test_med_repr",
        raw_biomarkers=biomarkers,
        user_data={},
        questionnaire_data=q,
    )
    mh = context.medical_history
    assert mh is not None
    assert mh["medications"] == ["None"]
    assert mh["supplements"] == ["Vitamin D"]
    assert mh["long_term_medication_classes"] == ["Corticosteroids"]
    assert mh["corticosteroids"] is True
    assert mh["hiv_treatments"] is False
    assert context.user.supplements == ["Vitamin D"]
    assert context.user.medications == ["None"]
