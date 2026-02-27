"""
v5.3 Sprint 4 - Unit tests for CausalLayer_v1 engine.
"""

from core.analytics.causal_layer_engine import build_causal_layer_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.precedence_engine_v1 import DominantEdge, PrecedenceOutput
from core.contracts.state_engine_v1 import SystemStateNode
from core.contracts.state_transition_v1 import BiomarkerTransitionNode


def _graph() -> InsightGraphV1:
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="a-1",
        system_states=[
            SystemStateNode(
                system_id="inflammatory",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_worse"],
                confidence_bucket="high",
            ),
            SystemStateNode(
                system_id="metabolic",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=["system_trending_worse"],
                confidence_bucket="high",
            ),
            SystemStateNode(
                system_id="cardiovascular",
                state_codes=["system_bidirectional_instability"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="renal",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="hepatic",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
        ],
        state_transitions=[
            BiomarkerTransitionNode(
                biomarker_id="x",
                from_status="normal",
                to_status="high",
                transition="worsening",
                evidence_codes=["status_change"],
            )
        ],
        precedence_output=PrecedenceOutput(
            primary_driver_system_id="inflammatory",
            dominant_edges=[DominantEdge(from_system_id="renal", to_system_id="hepatic", rule_id="r")],
            conflicts_resolved=["conflict_trend_opposition"],
            rationale_codes=["rule_applied:xyz"],
        ),
        edges=[],
    )


def test_causal_layer_rule_eval_and_ordering():
    graph = _graph()
    edges, _ = build_causal_layer_v1(graph)
    assert edges
    ordered = sorted(edges, key=lambda e: (-e.priority, e.from_system_id, e.to_system_id, e.edge_id))
    assert [e.model_dump() for e in edges] == [e.model_dump() for e in ordered]


def test_causal_layer_rationale_codes_sorted_unique():
    graph = _graph()
    edges, _ = build_causal_layer_v1(graph)
    for edge in edges:
        assert edge.rationale_codes == sorted(set(edge.rationale_codes))


def test_causal_layer_hash_deterministic():
    graph = _graph()
    edges1, stamp1 = build_causal_layer_v1(graph)
    edges2, stamp2 = build_causal_layer_v1(graph)
    assert [e.model_dump() for e in edges1] == [e.model_dump() for e in edges2]
    assert stamp1.causal_layer_hash == stamp2.causal_layer_hash
