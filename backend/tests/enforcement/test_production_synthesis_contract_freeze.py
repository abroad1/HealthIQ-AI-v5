"""
Sprint 7A enforcement: production InsightGraph synthesis contract freeze.
"""

from pathlib import Path


def test_synthesis_source_has_no_hardcoded_legacy_enable():
    repo_root = Path(__file__).resolve().parents[3]
    synthesis_path = repo_root / "backend" / "core" / "insights" / "synthesis.py"
    source = synthesis_path.read_text(encoding="utf-8")

    assert "allow_legacy_path = True" not in source


def test_orchestrator_public_synthesize_is_production_gated_or_passes_explainability():
    repo_root = Path(__file__).resolve().parents[3]
    orchestrator_path = repo_root / "backend" / "core" / "pipeline" / "orchestrator.py"
    source = orchestrator_path.read_text(encoding="utf-8")

    method_start = source.index("def synthesize_insights(")
    method_end = source.index("def _synthesize_from_insight_graph(")
    method_source = source[method_start:method_end]

    has_explainability_arg = "explainability_report=explainability_report" in method_source
    has_production_gate = (
        "orchestrator.synthesize_insights() is fixture/test mode only in production use orchestrator.run()"
        in method_source
    )

    assert has_explainability_arg or has_production_gate
