"""
v5.3 Sprint 4 - Enforcement: causal rules must come from SSOT registry.
"""

from pathlib import Path


_KNOWN_EDGE_IDS = [
    "edge_inflammatory_to_metabolic_driver",
    "edge_metabolic_to_cardiovascular_amplifier",
    "edge_renal_to_hepatic_constraint",
]


def test_causal_layer_engine_uses_registry_loader():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_layer_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.analytics.causal_layer_registry import load_causal_layer_registry" in text
    assert "load_causal_layer_registry()" in text


def test_causal_layer_edge_ids_not_hardcoded_in_engine():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_layer_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    offenders = [edge_id for edge_id in _KNOWN_EDGE_IDS if edge_id in text]
    assert not offenders, "Causal edge IDs must not be hardcoded in engine: " + ", ".join(offenders)
