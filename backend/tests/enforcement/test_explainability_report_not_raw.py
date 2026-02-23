"""
v5.3 Sprint 11 - Enforcement: explainability report contains no raw panel fields.
"""

from pathlib import Path

from tools.run_arbitration_scenarios import run_arbitration_scenarios


def test_explainability_report_has_no_raw_tokens(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v2.json"
    run_dir, _ = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="enforce-explainability-not-raw",
        scenario_id="cross_system_cascade_focus",
        write_narrative=False,
    )
    text = (run_dir / "scenarios" / "cross_system_cascade_focus" / "explainability_report.json").read_text(
        encoding="utf-8"
    )
    forbidden = [
        "raw_biomarkers",
        "lab_range",
        "reference_range",
        "unit",
        "mmol",
        "mg",
        "value",
        "lower",
        "upper",
        "biomarker_panel",
    ]
    for token in forbidden:
        assert token not in text
