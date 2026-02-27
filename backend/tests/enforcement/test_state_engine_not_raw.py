"""
v5.3 Sprint 2 - Enforcement: state engine must remain code-only and centralised.
"""

from pathlib import Path


def test_state_engine_module_exists_and_is_used():
    engine_path = Path(__file__).parent.parent.parent / "core" / "analytics" / "state_engine.py"
    orchestrator_path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    engine_text = engine_path.read_text(encoding="utf-8", errors="ignore")
    orchestrator_text = orchestrator_path.read_text(encoding="utf-8", errors="ignore")

    assert "def build_state_engine_v1(" in engine_text
    assert "from core.analytics.state_engine import build_state_engine_v1" in orchestrator_text
    assert "build_state_engine_v1(insight_graph)" in orchestrator_text


def test_state_engine_has_no_raw_access_patterns():
    engine_path = Path(__file__).parent.parent.parent / "core" / "analytics" / "state_engine.py"
    text = engine_path.read_text(encoding="utf-8", errors="ignore")
    forbidden = [
        "reference_range",
        "raw_biomarkers",
        "biomarker_panel",
        "context.user",
        "['value']",
        ".value",
        "unit",
        "units",
    ]
    offenders = [token for token in forbidden if token in text]
    assert not offenders, "State engine raw access/duplicate compute patterns found: " + ", ".join(offenders)
