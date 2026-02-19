"""
v5.3 Sprint 5 - Enforcement: calibration policy must be registry-driven.
"""

from pathlib import Path


_KNOWN_RULE_IDS = [
    "calibration_inflammatory_p0_urgent",
    "calibration_driver_p1_soon",
    "calibration_amplifier_p2_monitor",
    "calibration_constraint_p2_routine",
]


def test_calibration_engine_uses_registry_loader():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "calibration_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.analytics.calibration_registry import load_calibration_registry" in text
    assert "load_calibration_registry()" in text


def test_calibration_rule_ids_not_hardcoded_in_engine():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "calibration_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    offenders = [rule_id for rule_id in _KNOWN_RULE_IDS if rule_id in text]
    assert not offenders, "Calibration rule IDs must not be hardcoded in engine: " + ", ".join(offenders)


def test_orchestrator_stamps_calibration_from_insight_graph():
    path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "build_calibration_layer_v1(insight_graph)" in text
    assert "calibration_version=getattr(insight_graph, \"calibration_version\", \"\")" in text
    assert "calibration_hash=getattr(insight_graph, \"calibration_hash\", \"\")" in text
