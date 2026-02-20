"""
v5.3 Sprint 8 - Enforcement for single-authority primary driver field.
"""

from pathlib import Path


def test_only_arbitration_writes_final_primary_driver_field():
    orchestrator = (Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py").read_text(
        encoding="utf-8", errors="ignore"
    )
    marker = "insight_graph.primary_driver_system_id = primary_driver_system_id"
    assert marker in orchestrator
    assert orchestrator.count("primary_driver_system_id =") == 1


def test_prompt_uses_arbitration_driver_not_precedence_candidate():
    prompts = (Path(__file__).parent.parent.parent / "core" / "insights" / "prompts.py").read_text(
        encoding="utf-8", errors="ignore"
    )
    assert "ig.get(\"primary_driver_system_id\"" in prompts
    assert "precedence.get(\"primary_driver_system_id\"" not in prompts


def test_precedence_engine_does_not_write_final_driver_field():
    precedence_engine = (
        Path(__file__).parent.parent.parent / "core" / "analytics" / "precedence_engine.py"
    ).read_text(encoding="utf-8", errors="ignore")
    assert "insight_graph.primary_driver_system_id" not in precedence_engine
