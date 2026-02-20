"""
v5.3 Sprint 9 - Enforcement: arbitration output is permutation invariant.
"""

from itertools import permutations

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.contracts.calibration_layer_v1 import CalibrationItem
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode


def _base_nodes():
    return [
        SystemStateNode(
            system_id="alpha",
            state_codes=["system_multi_marker_derangement"],
            rationale_codes=[],
            transition_summary_codes=[],
            confidence_bucket="high",
        ),
        SystemStateNode(
            system_id="beta",
            state_codes=["system_focal_derangement", "system_bidirectional_instability"],
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
    ]


def _calibration_seed():
    return sorted(
        [
            CalibrationItem(
                system_id="alpha",
                priority_tier="p2",
                urgency_band="routine",
                action_intensity="info",
                stability_flag="stable",
                explanation_codes=["calibration:seed"],
                applied_rule_ids=[],
            ),
            CalibrationItem(
                system_id="beta",
                priority_tier="p2",
                urgency_band="routine",
                action_intensity="info",
                stability_flag="stable",
                explanation_codes=["calibration:seed"],
                applied_rule_ids=[],
            ),
            CalibrationItem(
                system_id="gamma",
                priority_tier="p3",
                urgency_band="routine",
                action_intensity="info",
                stability_flag="stable",
                explanation_codes=["calibration:seed"],
                applied_rule_ids=[],
            ),
        ],
        key=lambda x: x.system_id,
    )


def _run_once(nodes):
    graph = InsightGraphV1(graph_version="1.0.0", analysis_id="perm", system_states=list(nodes), edges=[])
    graph.calibration_items = _calibration_seed()
    conflicts = build_conflict_set_v1(graph)
    dominance = build_dominance_edges_v1(graph, conflicts)
    causal = build_causal_edges_v1(conflicts, dominance)
    primary, result, stamp = build_arbitration_result_v1(graph, conflicts, dominance, causal)
    return {
        "primary": primary,
        "decision_trace_codes": result.decision_trace_codes,
        "tie_breaker_codes": result.tie_breaker_codes,
        "rationale_codes": result.rationale_codes,
        "hash": stamp.arbitration_hash,
    }


def test_arbitration_is_invariant_under_system_order_permutations():
    nodes = _base_nodes()
    baseline = _run_once(nodes)
    checked = 0
    for perm in permutations(nodes):
        out = _run_once(list(perm))
        assert out == baseline
        checked += 1
        if checked >= 6:
            break
