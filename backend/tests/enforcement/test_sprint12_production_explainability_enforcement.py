"""
Sprint 12 enforcement: production explainability artifact + stamped prompt authority.
"""

from pathlib import Path

from tools.run_golden_panel import run_golden_panel


def test_golden_panel_runner_emits_production_explainability_artifact(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="enforce-s12-golden",
        write_narrative=False,
    )
    assert (run_dir / "analysis_result.json").exists()
    assert (run_dir / "insight_graph.json").exists()
    assert (run_dir / "replay_manifest.json").exists()
    assert (run_dir / "explainability_report.json").exists()


def test_prompt_authority_reads_stamped_explainability_fields_only():
    prompts = (Path(__file__).parent.parent.parent / "core" / "insights" / "prompts.py").read_text(
        encoding="utf-8", errors="ignore"
    )
    assert "Explainability report is required for prompt assembly" in prompts
    assert "arbitration_decisions" in prompts
    assert "influence_ordering" in prompts
    assert "precedence.get(\"primary_driver_system_id\"" not in prompts
    assert "\"supporting_systems\": list(influence_ordering.get(\"supporting_systems\", []))" in prompts
