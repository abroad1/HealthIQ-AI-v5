"""
v5.3 Sprint 7 - Conflict registry tests.
"""

import core.analytics.conflict_registry as module
from core.analytics.conflict_registry import load_conflict_registry


def test_conflict_registry_load_and_stamp():
    reg = load_conflict_registry()
    assert reg.rules
    assert reg.stamp.conflict_registry_version == "1.0.0"
    assert len(reg.stamp.conflict_registry_hash) == 64


def test_conflict_registry_sorted_by_rank_then_id():
    reg = load_conflict_registry()
    ordered = [(r.rank, r.conflict_id) for r in reg.rules]
    assert ordered == sorted(ordered)


def test_conflict_registry_has_three_required_types():
    reg = load_conflict_registry()
    kinds = sorted({r.conflict_type for r in reg.rules})
    assert kinds == ["cross_system_cascade", "depth_gap", "severity_override"]
