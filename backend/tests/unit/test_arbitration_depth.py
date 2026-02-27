"""
v5.3 Sprint 7 - Arbitration depth engine tests.
"""

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode


def _graph() -> InsightGraphV1:
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="arb-test",
        system_states=[
            SystemStateNode(
                system_id="alpha",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="high",
            ),
            SystemStateNode(
                system_id="beta",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="gamma",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="low",
            ),
        ],
        edges=[],
    )


def test_arbitration_depth_non_empty_and_sorted():
    graph = _graph()
    conflicts = build_conflict_set_v1(graph)
    dominance = build_dominance_edges_v1(graph, conflicts)
    causal = build_causal_edges_v1(conflicts, dominance)
    primary_driver, result, _ = build_arbitration_result_v1(graph, conflicts, dominance, causal)
    assert conflicts
    assert dominance
    assert causal
    assert primary_driver
    assert result.supporting_system_ids
    ordered = [(e.from_system_id, e.to_system_id, e.edge_type) for e in causal]
    assert ordered == sorted(ordered)


def test_arbitration_hash_stability_for_same_input():
    graph = _graph()
    c1 = build_conflict_set_v1(graph)
    d1 = build_dominance_edges_v1(graph, c1)
    e1 = build_causal_edges_v1(c1, d1)
    p1, r1, s1 = build_arbitration_result_v1(graph, c1, d1, e1)

    c2 = build_conflict_set_v1(graph)
    d2 = build_dominance_edges_v1(graph, c2)
    e2 = build_causal_edges_v1(c2, d2)
    p2, r2, s2 = build_arbitration_result_v1(graph, c2, d2, e2)
    assert p1 == p2
    assert r1.model_dump() == r2.model_dump()
    assert s1.arbitration_hash == s2.arbitration_hash


def test_arbitration_tiebreakers_deterministic():
    graph = _graph()
    conflicts = build_conflict_set_v1(graph)
    dominance = build_dominance_edges_v1(graph, conflicts)
    causal = build_causal_edges_v1(conflicts, dominance)
    _, result, _ = build_arbitration_result_v1(graph, conflicts, dominance, causal)
    assert result.tie_breaker_codes
