"""
Sprint 7 enforcement: stale analytics cluster schema imports are forbidden.
"""

from pathlib import Path


def test_no_stale_analytics_cluster_schema_imports():
    repo_root = Path(__file__).resolve().parents[3]

    builder_path = repo_root / "backend" / "core" / "analytics" / "insight_graph_builder.py"
    builder_source = builder_path.read_text(encoding="utf-8")
    assert "core.analytics.cluster_schema" not in builder_source

    orchestrator_path = repo_root / "backend" / "core" / "pipeline" / "orchestrator.py"
    orchestrator_source = orchestrator_path.read_text(encoding="utf-8")
    assert "core.analytics.cluster_schema" not in orchestrator_source
