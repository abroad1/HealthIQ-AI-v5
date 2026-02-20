"""
v5.3 Sprint 7 - Enforcement: arbitration depth must use SSOT registries.
"""

from pathlib import Path


def test_engines_load_registries_not_hardcoded_matrices():
    conflict_detector = (
        Path(__file__).parent.parent.parent / "core" / "analytics" / "conflict_detector.py"
    ).read_text(encoding="utf-8", errors="ignore")
    arbitration_engine = (
        Path(__file__).parent.parent.parent / "core" / "analytics" / "arbitration_engine.py"
    ).read_text(encoding="utf-8", errors="ignore")
    causal_edge_engine = (
        Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_edge_engine.py"
    ).read_text(encoding="utf-8", errors="ignore")

    assert "load_conflict_registry()" in conflict_detector
    assert "load_arbitration_registry()" in arbitration_engine
    assert "load_arbitration_registry()" in causal_edge_engine


def test_orchestrator_wires_arbitration_depth_stamps():
    orchestrator = (
        Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    ).read_text(encoding="utf-8", errors="ignore")
    assert "build_conflict_set_v1(insight_graph)" in orchestrator
    assert "build_dominance_edges_v1(insight_graph, conflict_set)" in orchestrator
    assert "build_causal_edges_v1(conflict_set, dominance_edges)" in orchestrator
    assert "build_arbitration_result_v1(" in orchestrator
    assert "arbitration_version=getattr(insight_graph, \"arbitration_version\", \"\")" in orchestrator
    assert "arbitration_hash=getattr(insight_graph, \"arbitration_hash\", \"\")" in orchestrator
