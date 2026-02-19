"""
v5.3 Sprint 1 - Enforcement: state transition logic must be centralised.
"""

from pathlib import Path


def test_state_transition_engine_module_exists():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "state_transition_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "build_state_transition_v1" in text
    assert "STATE_TRANSITION_V1_VERSION" in text


def test_orchestrator_uses_state_transition_engine_and_snapshot_linker():
    path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.analytics.state_transition_engine import build_state_transition_v1" in text
    assert "from core.analytics.snapshot_linker import link_prior_snapshot_insight_graphs" in text
    assert "state_transition_version" in text
    assert "state_transition_hash" in text
