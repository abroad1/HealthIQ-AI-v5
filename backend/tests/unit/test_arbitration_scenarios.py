"""
v5.3 Sprint 8 - Curated arbitration conflict scenarios.
"""

import json
from pathlib import Path

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.calibration_engine import build_calibration_layer_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode


def _load_scenarios():
    path = Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["scenarios"]


def _graph_from_scenario(scenario: dict) -> InsightGraphV1:
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


def test_arbitration_scenarios_expected_outcomes():
    for scenario in _load_scenarios():
        graph = _graph_from_scenario(scenario)
        conflicts = build_conflict_set_v1(graph)
        dominance_edges = build_dominance_edges_v1(graph, conflicts)
        causal_edges = build_causal_edges_v1(conflicts, dominance_edges)
        primary_driver, arbitration_result, _ = build_arbitration_result_v1(
            graph, conflicts, dominance_edges, causal_edges
        )
        graph.conflict_set = conflicts
        graph.dominance_edges = dominance_edges
        graph.causal_edges = causal_edges
        graph.primary_driver_system_id = primary_driver
        graph.arbitration_result = arbitration_result
        final_items, _ = build_calibration_layer_v1(graph, apply_arbitration_coupling=True)

        expected = scenario["expected"]
        found_conflicts = sorted({c.conflict_id for c in conflicts})
        assert found_conflicts == sorted(expected["conflict_ids"])
        assert primary_driver == expected["primary_driver_system_id"]

        found_edges = sorted([f"{e.from_system_id}>{e.to_system_id}:{e.edge_type}" for e in causal_edges])
        for edge in expected["top_causal_edges"]:
            assert edge in found_edges

        tier = ""
        for item in final_items:
            if item.system_id == primary_driver:
                tier = item.priority_tier
                break
        assert tier == expected["expected_calibration_tier"]
