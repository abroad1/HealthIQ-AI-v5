"""
v5.3 Sprint 3 - Enforcement: precedence logic must be SSOT-driven.
"""

from pathlib import Path


_KNOWN_RULE_IDS = [
    "metabolic_over_inflammatory_progression",
    "inflammatory_over_metabolic_progression",
    "cardiovascular_over_metabolic_multi_marker",
    "renal_over_hepatic_multi_marker",
]


def test_precedence_engine_uses_registry_loader():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "precedence_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.analytics.precedence_registry import load_precedence_registry" in text
    assert "load_precedence_registry()" in text


def test_precedence_rule_ids_not_hardcoded_in_engine():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "precedence_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    offenders = [rid for rid in _KNOWN_RULE_IDS if rid in text]
    assert not offenders, "Rule IDs must not be hardcoded in precedence_engine.py: " + ", ".join(offenders)
