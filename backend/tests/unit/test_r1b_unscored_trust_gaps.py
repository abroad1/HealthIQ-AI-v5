"""
R-1B — regression tests for unscored_reason preservation, string lab bounds, and HbA1c unit harmonisation.
"""

from core.scoring.rules import ScoringRules
from core.analytics.primitives import coerce_optional_float
from core.pipeline.orchestrator import AnalysisOrchestrator


def test_coerce_optional_float_parses_string_bounds():
    assert coerce_optional_float("1.5") == 1.5
    assert coerce_optional_float("  2 ") == 2.0
    assert coerce_optional_float(None) is None
    assert coerce_optional_float("x") is None


def test_string_one_sided_lab_range_scores_hdl():
    rules = ScoringRules()
    ref = {
        "min": "0.9",
        "max": None,
        "unit": "mmol/L",
        "source": "lab",
    }
    score, _sr, reason = rules.calculate_biomarker_score(
        "hdl_cholesterol",
        1.2,
        None,
        None,
        input_reference_range=ref,
    )
    assert reason is None
    assert score > 0


def test_hba1c_percent_value_with_mmol_mol_range_harmonises_and_scores():
    """Value in %, IFCC range in mmol/mol — must harmonise, not mis-scale comparison."""
    rules = ScoringRules()
    ref = {
        "min": 20.0,
        "max": 42.0,
        "unit": "mmol/mol",
        "source": "lab",
    }
    score, _sr, reason = rules.calculate_biomarker_score(
        "hba1c",
        5.4,
        None,
        None,
        input_reference_range=ref,
        value_unit="%",
    )
    assert reason is None, reason
    assert 0.0 < score <= 100.0


def test_orchestrator_score_biomarkers_dict_includes_unscored_reason():
    """R-1B Defect 1 — every biomarker row in the dict must carry unscored_reason (or null) for DTO use."""
    orc = AnalysisOrchestrator()
    out = orc.score_biomarkers(
        {"triglycerides": 1.0},
        age=40,
        sex="male",
        input_reference_ranges={
            "triglycerides": {
                "min": None,
                "max": 1.7,
                "unit": "mmol/L",
                "source": "lab",
            }
        },
    )
    found = False
    for _sys, hs in out["health_system_scores"].items():
        for row in hs["biomarker_scores"]:
            found = True
            assert "unscored_reason" in row
    assert found, "expected at least one scored biomarker row for triglycerides"
