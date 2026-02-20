"""
v5.3 Sprint 10 - Enforcement for ArbitrationScenarioRunner_v1 purity.
"""

from pathlib import Path


def test_arbitration_scenario_runner_has_no_raw_panel_tokens():
    p = Path(__file__).parent.parent.parent / "tools" / "run_arbitration_scenarios.py"
    text = p.read_text(encoding="utf-8", errors="ignore")
    banned = [
        "biomarker_panel",
        "raw_biomarkers",
        "reference_range",
        "lab_range",
        "value",
        "unit",
        "mmol",
        "mg",
        "lower",
        "upper",
    ]
    for token in banned:
        assert token not in text
