"""
v5.3 Sprint 9 - Enforcement: arbitration output is permutation invariant.
"""

import json
from itertools import permutations
from pathlib import Path

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.contracts.calibration_layer_v1 import CalibrationItem
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode
from tools.run_arbitration_scenarios import run_arbitration_scenarios


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


def _runner_fixture_payload(reverse_order: bool) -> dict:
    nodes = [
        {
            "system_id": "alpha",
            "state_codes": ["system_multi_marker_derangement"],
            "transition_summary_codes": [],
            "confidence_bucket": "high",
        },
        {
            "system_id": "beta",
            "state_codes": ["system_focal_derangement", "system_bidirectional_instability"],
            "transition_summary_codes": [],
            "confidence_bucket": "moderate",
        },
        {
            "system_id": "gamma",
            "state_codes": ["system_focal_derangement"],
            "transition_summary_codes": [],
            "confidence_bucket": "low",
        },
    ]
    if reverse_order:
        nodes = list(reversed(nodes))
    return {
        "scenarios": [
            {
                "scenario_id": "perm_runner",
                "system_states": nodes,
                "baseline_calibration_tiers": {"alpha": "p2", "beta": "p2", "gamma": "p3"},
                "expected": {"primary_driver_system_id": "alpha"},
            }
        ]
    }


def test_explainability_is_invariant_under_system_order_permutations(tmp_path):
    fixture_a = tmp_path / "fixture_a.json"
    fixture_b = tmp_path / "fixture_b.json"
    fixture_a.write_text(json.dumps(_runner_fixture_payload(False), indent=2, sort_keys=True), encoding="utf-8")
    fixture_b.write_text(json.dumps(_runner_fixture_payload(True), indent=2, sort_keys=True), encoding="utf-8")

    run_a, _ = run_arbitration_scenarios(
        fixture_path=Path(fixture_a),
        output_root=tmp_path / "run_a",
        run_id="perm-runner-a",
        scenario_id="perm_runner",
        write_narrative=False,
    )
    run_b, _ = run_arbitration_scenarios(
        fixture_path=Path(fixture_b),
        output_root=tmp_path / "run_b",
        run_id="perm-runner-b",
        scenario_id="perm_runner",
        write_narrative=False,
    )
    rep_a = json.loads((run_a / "scenarios" / "perm_runner" / "explainability_report.json").read_text(encoding="utf-8"))
    rep_b = json.loads((run_b / "scenarios" / "perm_runner" / "explainability_report.json").read_text(encoding="utf-8"))
    assert (
        rep_a["arbitration_decisions"]["primary_driver_system_id"]
        == rep_b["arbitration_decisions"]["primary_driver_system_id"]
    )
    assert rep_a["replay_stamps"]["arbitration_hash"] == rep_b["replay_stamps"]["arbitration_hash"]
    assert rep_a["replay_stamps"]["explainability_hash"] == rep_b["replay_stamps"]["explainability_hash"]
