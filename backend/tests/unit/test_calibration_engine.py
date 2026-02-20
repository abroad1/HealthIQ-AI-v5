"""
v5.3 Sprint 5 - Unit tests for calibration engine.
"""

from pathlib import Path

from core.analytics.calibration_engine import build_calibration_layer_v1
from core.contracts.arbitration_v1 import ConflictItem, DominanceEdge as ArbitrationDominanceEdge
from core.contracts.arbitration_v1 import CausalEdge
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
                transition_summary_codes=["system_trending_improving"],
                confidence_bucket="high",
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
            dominant_edges=[DominantEdge(from_system_id="renal", to_system_id="hepatic", rule_id="r1")],
            conflicts_resolved=[],
            rationale_codes=[],
        ),
        causal_edges=[
            CausalEdge(
                edge_id="e1",
                from_system_id="inflammatory",
                to_system_id="metabolic",
                edge_type="driver",
                priority=100,
                rationale_codes=["x"],
                source_conflict_ids=[],
            )
        ],
        edges=[],
    )


def test_calibration_engine_deterministic_output_ordering():
    graph = _graph()
    items, _ = build_calibration_layer_v1(graph)
    assert [i.system_id for i in items] == sorted(i.system_id for i in items)


def test_calibration_engine_tie_break_by_rank():
    graph = _graph()
    items, _ = build_calibration_layer_v1(graph)
    by_id = {i.system_id: i for i in items}
    assert by_id["inflammatory"].priority_tier == "p0"
    assert by_id["inflammatory"].applied_rule_ids == ["calibration_inflammatory_p0_urgent"]


def test_calibration_engine_default_when_no_match():
    graph = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="a-2",
        system_states=[
            SystemStateNode(
                system_id="hormonal",
                state_codes=["system_stable_normal"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="high",
            )
        ],
        precedence_output=PrecedenceOutput(
            primary_driver_system_id="",
            dominant_edges=[],
            conflicts_resolved=[],
            rationale_codes=[],
        ),
        causal_edges=[],
        edges=[],
    )
    items, _ = build_calibration_layer_v1(graph)
    assert len(items) == 1
    item = items[0]
    assert item.system_id == "hormonal"
    assert item.priority_tier == "p3"
    assert item.urgency_band == "routine"
    assert item.action_intensity == "info"
    assert item.stability_flag == "stable"
    assert item.explanation_codes == ["calibration:default"]
    assert item.applied_rule_ids == []


def test_calibration_engine_hash_deterministic():
    graph = _graph()
    i1, s1 = build_calibration_layer_v1(graph)
    i2, s2 = build_calibration_layer_v1(graph)
    assert [x.model_dump() for x in i1] == [x.model_dump() for x in i2]
    assert s1.calibration_hash == s2.calibration_hash


def test_calibration_coupling_promotes_primary_driver_tier_deterministically():
    graph = _graph()
    # Synthetic arbitration depth signals
    graph.primary_driver_system_id = "inflammatory"
    graph.conflict_set = [
        ConflictItem(
            conflict_id="c1",
            system_a="inflammatory",
            system_b="metabolic",
            conflict_type="depth_gap",
            conflict_severity="moderate",
            rationale_codes=[],
        ),
        ConflictItem(
            conflict_id="c2",
            system_a="inflammatory",
            system_b="hepatic",
            conflict_type="severity_override",
            conflict_severity="high",
            rationale_codes=[],
        ),
    ]
    graph.dominance_edges = [
        ArbitrationDominanceEdge(
            from_system_id="inflammatory",
            to_system_id="metabolic",
            rule_id="r1",
            conflict_id="c1",
            conflict_type="depth_gap",
            precedence_tier=10,
            rationale_codes=[],
        ),
        ArbitrationDominanceEdge(
            from_system_id="inflammatory",
            to_system_id="hepatic",
            rule_id="r2",
            conflict_id="c2",
            conflict_type="severity_override",
            precedence_tier=10,
            rationale_codes=[],
        ),
    ]
    base_items, _ = build_calibration_layer_v1(graph, apply_arbitration_coupling=False)
    coupled_items, _ = build_calibration_layer_v1(graph, apply_arbitration_coupling=True)
    base = {i.system_id: i for i in base_items}
    coupled = {i.system_id: i for i in coupled_items}
    rank = {"p3": 0, "p2": 1, "p1": 2, "p0": 3}
    assert rank[coupled["inflammatory"].priority_tier] >= rank[base["inflammatory"].priority_tier]
    assert any(code.startswith("calibration:arbitration_coupling_depth:") for code in coupled["inflammatory"].explanation_codes)


def test_calibration_engine_no_raw_fields_dependency():
    p = Path(__file__).parent.parent.parent / "core" / "analytics" / "calibration_engine.py"
    text = p.read_text(encoding="utf-8", errors="ignore")
    forbidden = ["biomarker_panel", "raw_biomarkers", "reference_range", "lab_range", "['value']", ".unit"]
    for token in forbidden:
        assert token not in text
