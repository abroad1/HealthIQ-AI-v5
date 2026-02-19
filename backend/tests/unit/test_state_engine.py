"""
v5.3 Sprint 2 - Unit tests for Multi-Marker State Engine v1.
"""

from pathlib import Path

from core.analytics.state_engine import build_state_engine_v1
from core.contracts.insight_graph_v1 import BiomarkerNode, InsightGraphV1
from core.contracts.relationship_registry_v1 import RelationshipDetection
from core.contracts.state_transition_v1 import BiomarkerTransitionNode


def _graph(
    nodes: list[BiomarkerNode],
    transitions: list[BiomarkerTransitionNode],
    relationships: list[RelationshipDetection],
    cluster_confidence: dict[str, float],
    clusters: list[dict],
) -> InsightGraphV1:
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="a-1",
        biomarker_nodes=nodes,
        state_transitions=transitions,
        relationships=relationships,
        cluster_summary={"clusters": clusters},
        confidence={
            "model_version": "1.0.0",
            "system_confidence": 0.0,
            "cluster_confidence": cluster_confidence,
            "biomarker_confidence": {},
            "missing_required_biomarkers": [],
            "missing_required_clusters": [],
            "cluster_schema_version": "1.0.0",
            "cluster_schema_hash": "x",
            "ratio_registry_version": "x",
        },
        edges=[],
    )


def test_state_engine_deterministic_ordering_and_hash():
    graph = _graph(
        nodes=[
            BiomarkerNode(biomarker_id="b2", status="high", score=30.0),
            BiomarkerNode(biomarker_id="b1", status="normal", score=80.0),
        ],
        transitions=[
            BiomarkerTransitionNode(
                biomarker_id="b2",
                from_status="normal",
                to_status="high",
                transition="worsening",
                evidence_codes=["status_change"],
            )
        ],
        relationships=[],
        cluster_confidence={"sys_b": 0.65, "sys_a": 0.90},
        clusters=[
            {"cluster_id": "sys_b", "biomarkers": ["b2"]},
            {"cluster_id": "sys_a", "biomarkers": ["b1"]},
        ],
    )
    s1, stamp1 = build_state_engine_v1(graph)
    s2, stamp2 = build_state_engine_v1(graph)
    assert [n.system_id for n in s1] == ["sys_a", "sys_b"]
    assert [n.model_dump() for n in s1] == [n.model_dump() for n in s2]
    assert stamp1.state_engine_hash == stamp2.state_engine_hash


def test_state_engine_severity_logic():
    graph = _graph(
        nodes=[
            BiomarkerNode(biomarker_id="n1", status="normal", score=80.0),
            BiomarkerNode(biomarker_id="f1", status="high", score=35.0),
            BiomarkerNode(biomarker_id="m1", status="high", score=30.0),
            BiomarkerNode(biomarker_id="m2", status="low", score=25.0),
        ],
        transitions=[],
        relationships=[],
        cluster_confidence={"normal_sys": 0.9, "focal_sys": 0.9, "multi_sys": 0.9},
        clusters=[
            {"cluster_id": "normal_sys", "biomarkers": ["n1"]},
            {"cluster_id": "focal_sys", "biomarkers": ["f1"]},
            {"cluster_id": "multi_sys", "biomarkers": ["m1", "m2"]},
        ],
    )
    nodes, _ = build_state_engine_v1(graph)
    by_id = {n.system_id: n for n in nodes}
    assert "system_stable_normal" in by_id["normal_sys"].state_codes
    assert "system_focal_derangement" in by_id["focal_sys"].state_codes
    assert "system_multi_marker_derangement" in by_id["multi_sys"].state_codes
    assert "system_bidirectional_instability" in by_id["multi_sys"].state_codes


def test_state_engine_transition_rollup_logic():
    graph = _graph(
        nodes=[
            BiomarkerNode(biomarker_id="a", status="high", score=30.0),
            BiomarkerNode(biomarker_id="b", status="high", score=30.0),
            BiomarkerNode(biomarker_id="c", status="normal", score=70.0),
            BiomarkerNode(biomarker_id="d", status="normal", score=70.0),
        ],
        transitions=[
            BiomarkerTransitionNode(
                biomarker_id="a",
                from_status="normal",
                to_status="high",
                transition="worsening",
                evidence_codes=["status_change"],
            ),
            BiomarkerTransitionNode(
                biomarker_id="b",
                from_status="normal",
                to_status="high",
                transition="worsening",
                evidence_codes=["status_change"],
            ),
            BiomarkerTransitionNode(
                biomarker_id="c",
                from_status="high",
                to_status="normal",
                transition="improving",
                evidence_codes=["status_change"],
            ),
            BiomarkerTransitionNode(
                biomarker_id="d",
                from_status="high",
                to_status="normal",
                transition="improving",
                evidence_codes=["status_change"],
            ),
        ],
        relationships=[],
        cluster_confidence={"sys": 0.9},
        clusters=[{"cluster_id": "sys", "biomarkers": ["a", "b", "c", "d"]}],
    )
    states, _ = build_state_engine_v1(graph)
    codes = states[0].transition_summary_codes
    assert "system_trending_worse" in codes
    assert "system_trending_improving" in codes
    assert "system_transition_volatility" in codes


def test_state_engine_relationship_density_logic():
    rel1 = RelationshipDetection(
        relationship_id="r1",
        version="1.0.0",
        biomarkers=["x1", "x2"],
        classification_code="C1",
        severity="moderate",
        triggered=True,
        evidence=[],
    )
    rel2 = RelationshipDetection(
        relationship_id="r2",
        version="1.0.0",
        biomarkers=["x2", "x3"],
        classification_code="C2",
        severity="moderate",
        triggered=True,
        evidence=[],
    )
    graph = _graph(
        nodes=[
            BiomarkerNode(biomarker_id="x1", status="normal", score=80.0),
            BiomarkerNode(biomarker_id="x2", status="normal", score=80.0),
            BiomarkerNode(biomarker_id="x3", status="normal", score=80.0),
            BiomarkerNode(biomarker_id="y1", status="normal", score=80.0),
        ],
        transitions=[],
        relationships=[rel1, rel2],
        cluster_confidence={"dense": 0.9, "sparse": 0.9},
        clusters=[
            {"cluster_id": "dense", "biomarkers": ["x1", "x2", "x3"]},
            {"cluster_id": "sparse", "biomarkers": ["y1"]},
        ],
    )
    states, _ = build_state_engine_v1(graph)
    by_id = {n.system_id: n for n in states}
    assert "system_relationship_density_high" in by_id["dense"].rationale_codes
    assert "system_relationship_sparse" in by_id["sparse"].rationale_codes


def test_state_engine_confidence_bucket_mapping():
    graph = _graph(
        nodes=[BiomarkerNode(biomarker_id="b", status="normal", score=80.0)],
        transitions=[],
        relationships=[],
        cluster_confidence={"h": 0.85, "m": 0.84, "l": 0.30, "i": 0.29},
        clusters=[
            {"cluster_id": "h", "biomarkers": ["b"]},
            {"cluster_id": "m", "biomarkers": ["b"]},
            {"cluster_id": "l", "biomarkers": ["b"]},
            {"cluster_id": "i", "biomarkers": ["b"]},
        ],
    )
    states, _ = build_state_engine_v1(graph)
    by_id = {n.system_id: n for n in states}
    assert by_id["h"].confidence_bucket == "high"
    assert by_id["m"].confidence_bucket == "moderate"
    assert by_id["l"].confidence_bucket == "low"
    assert by_id["i"].confidence_bucket == "insufficient"


def test_state_engine_no_raw_value_access():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "state_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    forbidden = ["reference_range", "raw_biomarkers", "biomarker_panel", "units", "['value']"]
    for token in forbidden:
        assert token not in text
