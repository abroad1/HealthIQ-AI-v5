"""
Sprint 12 - Enforcement: runtime clustering convergence to ClusterEngineV2.
"""

from pathlib import Path


def test_orchestrator_does_not_import_legacy_clustering_engine():
    """Orchestrator runtime must not import legacy ClusteringEngine."""
    path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.clustering.engine import ClusteringEngine" not in text, (
        "Sprint 12: orchestrator must use ClusterEngineV2 as sole runtime engine"
    )
    assert "from core.clustering.cluster_engine_v2 import ClusterEngineV2" in text, (
        "Sprint 12: orchestrator must import ClusterEngineV2"
    )


def test_legacy_engine_has_no_algorithm_if_elif_branch_chain():
    """Legacy engine must not retain explicit algorithm if/elif branch chain."""
    path = Path(__file__).parent.parent.parent / "core" / "clustering" / "engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "if self.algorithm ==" not in text
    assert "elif self.algorithm ==" not in text
