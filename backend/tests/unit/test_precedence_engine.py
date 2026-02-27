"""
v5.3 Sprint 3 - Unit tests for InteractionPrecedenceEngine_v1.
"""

from core.analytics.precedence_engine import build_precedence_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode


def _graph(states: list[SystemStateNode], criticality: dict | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="a-1",
        system_states=states,
        criticality=criticality or {},
        edges=[],
    )


def test_precedence_engine_hash_deterministic():
    graph = _graph(
        [
            SystemStateNode(
                system_id="metabolic",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_improving"],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="inflammatory",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_worse"],
                confidence_bucket="high",
            ),
        ]
    )
    o1, s1 = build_precedence_v1(graph)
    o2, s2 = build_precedence_v1(graph)
    assert o1.model_dump() == o2.model_dump()
    assert s1.precedence_engine_hash == s2.precedence_engine_hash


def test_conflict_case_metabolic_improving_vs_inflammatory_worsening():
    graph = _graph(
        [
            SystemStateNode(
                system_id="metabolic",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_improving"],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="inflammatory",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_worse"],
                confidence_bucket="high",
            ),
        ]
    )
    output, _ = build_precedence_v1(graph)
    assert output.primary_driver_system_id == "inflammatory"
    assert output.dominant_edges
    assert all("exercise" not in code.lower() for code in output.rationale_codes)
    assert all("stress" not in code.lower() for code in output.rationale_codes)
    assert all("infection" not in code.lower() for code in output.rationale_codes)


def test_confidence_gate_low_confidence_system_cannot_dominate():
    graph = _graph(
        [
            SystemStateNode(
                system_id="cardiovascular",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="low",
            ),
            SystemStateNode(
                system_id="metabolic",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_improving"],
                confidence_bucket="moderate",
            ),
        ]
    )
    output, _ = build_precedence_v1(graph)
    assert all(not (e.from_system_id == "cardiovascular" and e.to_system_id == "metabolic") for e in output.dominant_edges)


def test_tie_break_order_enforced():
    graph = _graph(
        [
            SystemStateNode(
                system_id="renal",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_transition_volatility"],
                confidence_bucket="high",
            ),
            SystemStateNode(
                system_id="hepatic",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_improving"],
                confidence_bucket="high",
            ),
        ]
    )
    output, _ = build_precedence_v1(graph)
    assert any(code.startswith("tie_breaker_persistence_beats_spike") for code in output.rationale_codes)
