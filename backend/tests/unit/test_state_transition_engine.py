"""
v5.3 Sprint 1 - Unit tests for StateTransitionEngine_v1.
"""

from core.analytics.state_transition_engine import build_state_transition_v1
from core.contracts.insight_graph_v1 import BiomarkerNode, InsightGraphV1


def _graph(analysis_id: str, nodes: list[BiomarkerNode]) -> InsightGraphV1:
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id=analysis_id,
        biomarker_nodes=nodes,
        edges=[],
    )


def test_state_transition_hash_is_deterministic():
    current = _graph(
        "cur",
        [
            BiomarkerNode(biomarker_id="glucose", status="normal", score=80.0),
            BiomarkerNode(biomarker_id="crp", status="high", score=30.0),
        ],
    )
    prior = _graph(
        "p1",
        [
            BiomarkerNode(biomarker_id="glucose", status="normal", score=75.0),
            BiomarkerNode(biomarker_id="crp", status="high", score=35.0),
        ],
    )
    s1, t1 = build_state_transition_v1(current, [prior])
    s2, t2 = build_state_transition_v1(current, [prior])
    assert s1.state_transition_hash == s2.state_transition_hash
    assert [t.model_dump() for t in t1] == [t.model_dump() for t in t2]


def test_state_transition_rule_coverage():
    current = _graph(
        "cur",
        [
            BiomarkerNode(biomarker_id="a", status="normal", score=80.0),  # stable_normal
            BiomarkerNode(biomarker_id="b", status="low", score=25.0),  # stable_abnormal
            BiomarkerNode(biomarker_id="c", status="normal", score=75.0),  # improving
            BiomarkerNode(biomarker_id="d", status="high", score=45.0),  # worsening
            BiomarkerNode(biomarker_id="e", status="normal", score=70.0),  # insufficient_history
        ],
    )
    prior = _graph(
        "p1",
        [
            BiomarkerNode(biomarker_id="a", status="normal", score=78.0),
            BiomarkerNode(biomarker_id="b", status="low", score=20.0),
            BiomarkerNode(biomarker_id="c", status="high", score=35.0),
            BiomarkerNode(biomarker_id="d", status="normal", score=75.0),
        ],
    )

    _, transitions = build_state_transition_v1(current, [prior])
    by_id = {node.biomarker_id: node for node in transitions}

    assert by_id["a"].transition == "stable_normal"
    assert by_id["b"].transition == "stable_abnormal"
    assert by_id["c"].transition == "improving"
    assert by_id["d"].transition == "worsening"
    assert by_id["e"].transition == "insufficient_history"
