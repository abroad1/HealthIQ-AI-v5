"""
v5.3 Sprint 8 - Arbitration report scenario assertions.
"""

import json
from pathlib import Path

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.calibration_engine import build_calibration_layer_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode
from tools.run_golden_panel import build_arbitration_report


def _load_scenarios():
    path = Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))["scenarios"]


def _to_graph(scenario: dict) -> InsightGraphV1:
    nodes = [
        SystemStateNode(
            system_id=s["system_id"],
            state_codes=s["state_codes"],
            rationale_codes=[],
            transition_summary_codes=s["transition_summary_codes"],
            confidence_bucket=s["confidence_bucket"],
        )
        for s in scenario["system_states"]
    ]
    return InsightGraphV1(graph_version="1.0.0", analysis_id=scenario["scenario_id"], system_states=nodes, edges=[])


def test_arbitration_report_contains_expected_values_for_curated_scenarios():
    for scenario in _load_scenarios():
        graph = _to_graph(scenario)
        conflicts = build_conflict_set_v1(graph)
        dominance = build_dominance_edges_v1(graph, conflicts)
        causal = build_causal_edges_v1(conflicts, dominance)
        primary, arb_node, _ = build_arbitration_result_v1(graph, conflicts, dominance, causal)
        graph.conflict_set = conflicts
        graph.dominance_edges = dominance
        graph.causal_edges = causal
        graph.primary_driver_system_id = primary
        graph.arbitration_result = arb_node
        final_items, _ = build_calibration_layer_v1(graph, apply_arbitration_coupling=True)
        graph.calibration_items = final_items
        report = build_arbitration_report(
            insight_graph=graph.model_dump(),
            replay_manifest={"arbitration_version": "1.0.0", "arbitration_hash": "h"},
            run_id=scenario["scenario_id"],
        )
        expected = scenario["expected"]
        assert report["arbitration_decisions"]["primary_driver_system_id"] == expected["primary_driver_system_id"]
        found_conflict_ids = sorted({c["conflict_id"] for c in report["conflict_summary"]})
        assert found_conflict_ids == sorted(expected["conflict_ids"])
        found_edges = sorted([f"{e['from_system_id']}>{e['to_system_id']}:{e['edge_code']}" for e in report["causal_edges"]])
        for edge in expected["top_causal_edges"]:
            assert edge in found_edges
        assert report["calibration_impact"]["final_calibration_tier"] == expected["expected_calibration_tier"]
