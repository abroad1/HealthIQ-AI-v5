"""
v5.3 Sprint 7 - Arbitration registry tests.
"""

from core.analytics.arbitration_registry import load_arbitration_registry


def test_arbitration_registry_load_and_stamp():
    reg = load_arbitration_registry()
    assert reg.dominance_rules
    assert reg.causal_edge_rules
    assert reg.scoring.tie_breakers
    assert reg.stamp.arbitration_registry_version == "1.0.0"
    assert len(reg.stamp.arbitration_registry_hash) == 64


def test_arbitration_registry_deterministic_rule_order():
    reg = load_arbitration_registry()
    dom = [(r.precedence_tier, r.rule_id) for r in reg.dominance_rules]
    assert dom == sorted(dom)
