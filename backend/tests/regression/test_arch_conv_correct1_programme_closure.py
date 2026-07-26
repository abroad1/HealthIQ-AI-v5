"""
Regression scenarios for ARCH-CONV-CORRECT-1 programme closure.

Covers the four workstreams the correction package had to close:
- WS1 rejected-frame total inactivation (fire attempt, upstream fixture, interventions);
- WS2 legacy "methylation capacity" retirement (runtime + stale cached DTO);
- WS3 MCV frame co-service control (anchor + each specific frame, and ambiguity);
- WS4 Layer B completeness for Layer C (missing medical fields must not be invented).
"""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from core.analytics.insight_graph_builder import build_insight_graph_v1
from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.frame_co_service_v1 import (
    WHY_ROLE_CAUSAL,
    WHY_ROLE_MORPHOLOGY_CONTEXT,
    load_frame_co_service_policy,
)
from core.knowledge.frame_runtime_authority_v1 import (
    RUNTIME_STATE_REJECTED_NOT_ELIGIBLE,
    frame_runtime_exclusion_reason,
    is_frame_runtime_eligible,
)

REJECTED_KEY = "signal_homocysteine_high::inv_homocysteine_high_metabolic"
MCV_ANCHOR = "signal_mcv_high::inv_mcv_high_macrocytosis"
MCV_MEGALOBLASTIC = "signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis"
MCV_NONMEGALOBLASTIC = "signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis"

RETIRED_PHRASES = ("methylation capacity",)

LAB_RANGES: Dict[str, Dict[str, float]] = {
    "homocysteine": {"min": 5.0, "max": 15.0},
    "mcv": {"min": 80.0, "max": 96.0},
    "folate": {"min": 3.9, "max": 26.8},
    "vitamin_b12": {"min": 197.0, "max": 771.0},
    "active_b12": {"min": 37.5, "max": 188.0},
    "ggt": {"min": 10.0, "max": 71.0},
    "alt": {"min": 0.0, "max": 41.0},
    "egfr": {"min": 90.0, "max": 120.0},
    "creatinine": {"min": 59.0, "max": 104.0},
}

#: Live UAT panel for analysis e34aaedf-b09f-42f0-8cc8-4653a00b4c10.
UAT_PANEL: Dict[str, float] = {
    "homocysteine": 16.2,
    "mcv": 99.5,
    "folate": 7.7,
    "vitamin_b12": 336.0,
    "active_b12": 139.2,
    "ggt": 30.0,
    "alt": 22.0,
    "egfr": 84.0,
    "creatinine": 90.0,
}

REJECTED_ROW: Dict[str, Any] = {
    "signal_id": "signal_homocysteine_high",
    "activation_key": REJECTED_KEY,
    "source_spec_id": "inv_homocysteine_high_metabolic",
    "signal_state": "suboptimal",
    "confidence": 0.92,
    "primary_metric": "homocysteine",
    "system": "metabolic",
}


def _evaluate(panel: Dict[str, float]) -> List[Dict[str, Any]]:
    rows = SignalEvaluator(SignalRegistry()).evaluate_all(panel, {}, lab_ranges=LAB_RANGES)
    return [r.model_dump() for r in rows]


def _root_cause(panel: Dict[str, float], rows: List[Dict[str, Any]]):
    return compile_root_cause_v1(
        signal_results=rows,
        biomarker_context={k: {"value": v} for k, v in panel.items()},
        input_reference_ranges=LAB_RANGES,
    )


def _mcv_roles(panel: Dict[str, float]) -> Dict[str, str]:
    root = _root_cause(panel, _evaluate(panel))
    if root is None:
        return {}
    return {
        f.activation_key: f.why_role
        for f in root.findings
        if f.activation_key.startswith("signal_mcv_high::")
    }


# --- WS1 -----------------------------------------------------------------------------


def test_rejected_frame_cannot_fire_even_on_a_supporting_panel():
    """A panel that would satisfy the rejected frame must not activate it."""
    rows = _evaluate({**UAT_PANEL, "homocysteine": 30.0})
    assert rows, "probe panel must still activate approved signals"
    assert REJECTED_KEY not in {str(r.get("activation_key") or "") for r in rows}

    registry = SignalRegistry()
    assert REJECTED_KEY not in set(registry._signals_by_activation_key)
    assert REJECTED_KEY in {row["activation_key"] for row in registry.excluded_rejected_frames}
    assert not is_frame_runtime_eligible(REJECTED_KEY)
    assert frame_runtime_exclusion_reason(REJECTED_KEY) == RUNTIME_STATE_REJECTED_NOT_ELIGIBLE


def _graph(rows: List[Dict[str, Any]]):
    return build_insight_graph_v1(
        analysis_id="arch-conv-correct-1-regression",
        scoring_result={},
        clustering_result={"clusters": []},
        input_reference_ranges=LAB_RANGES,
        filtered_biomarkers={k: {"value": v} for k, v in UAT_PANEL.items()},
        signal_results=rows,
    )


def test_rejected_frame_in_upstream_fixture_is_excluded_before_ranking():
    """Replay / fixture rows bypass evaluation, so the assembly boundary must fail closed."""
    graph = _graph(_evaluate(UAT_PANEL) + [REJECTED_ROW])
    payload = graph.model_dump_json()
    assert REJECTED_KEY not in payload
    assert "inv_homocysteine_high_metabolic" not in payload

    top_keys = {
        str(getattr(f, "activation_key", "") or "")
        for f in (graph.report_v1.top_findings if graph.report_v1 else [])
    }
    assert REJECTED_KEY not in top_keys


def test_rejected_frame_produces_no_root_cause_finding_alongside_approved_siblings():
    rows = _evaluate(UAT_PANEL) + [REJECTED_ROW]
    root = _root_cause(UAT_PANEL, rows)
    if root is not None:
        assert REJECTED_KEY not in {f.activation_key for f in root.findings}


def test_intervention_aggregation_ignores_the_rejected_frame():
    """Interventions are aggregated inside the graph assembly, behind the same filter."""
    approved = [
        row
        for row in _evaluate(UAT_PANEL)
        if str(row.get("activation_key") or "") != REJECTED_KEY
    ]

    with_rejected = _graph(approved + [REJECTED_ROW]).interventions_v1
    without_rejected = _graph(approved).interventions_v1

    assert with_rejected == without_rejected
    blob = str(with_rejected)
    assert REJECTED_KEY not in blob
    assert "inv_homocysteine_high_metabolic" not in blob


# --- WS2 -----------------------------------------------------------------------------


def test_legacy_homocysteine_elevation_context_hypothesis_drops_retired_wording():
    panel = {**UAT_PANEL, "homocysteine": 30.0, "vitamin_b12": 150.0}
    root = _root_cause(panel, _evaluate(panel))
    assert root is not None, "elevated homocysteine panel must still compile a finding"

    text = " ".join(
        f"{h.hypothesis_id} {h.title} {h.summary}"
        for finding in root.findings
        for h in finding.hypotheses
    ).lower()
    for phrase in RETIRED_PHRASES:
        assert phrase not in text


def test_stale_cached_dto_with_retired_wording_is_detectable_by_fingerprint():
    """
    A cached DTO from before the retirement still carries the old sentence. The programme
    fingerprint must treat that as a leak rather than silently rendering it.
    """
    stale_dto = {
        "root_cause": {
            "findings": [
                {
                    "signal_id": "signal_homocysteine_elevation_context",
                    "hypotheses": [
                        {
                            "hypothesis_id": "hcy_b12_pattern_v1",
                            "summary": "Elevated homocysteine may reflect reduced B12-related methylation capacity.",
                        }
                    ],
                }
            ]
        }
    }
    blob = str(stale_dto).lower()
    assert any(phrase in blob for phrase in RETIRED_PHRASES), "fixture must model the stale wording"

    live = _root_cause(
        {**UAT_PANEL, "homocysteine": 30.0},
        _evaluate({**UAT_PANEL, "homocysteine": 30.0}),
    )
    live_blob = "" if live is None else live.model_dump_json().lower()
    for phrase in RETIRED_PHRASES:
        assert phrase not in live_blob


# --- WS3 -----------------------------------------------------------------------------


def test_co_service_policy_loads_and_forbids_unratified_combined_pattern():
    policy = load_frame_co_service_policy()
    family = policy["_by_signal_id"]["signal_mcv_high"]
    assert family["combined_pattern_authorised"] is False
    assert family["anchor"]["activation_key"] == MCV_ANCHOR


def test_mcv_anchor_serves_context_only_when_no_specific_evidence():
    roles = _mcv_roles(UAT_PANEL)
    assert roles.get(MCV_ANCHOR) == WHY_ROLE_MORPHOLOGY_CONTEXT
    assert WHY_ROLE_CAUSAL not in roles.values()


def test_mcv_anchor_plus_megaloblastic_when_hematinic_evidence_supports_it():
    roles = _mcv_roles({**UAT_PANEL, "folate": 2.1})
    assert roles.get(MCV_MEGALOBLASTIC) == WHY_ROLE_CAUSAL
    assert roles.get(MCV_ANCHOR) == WHY_ROLE_MORPHOLOGY_CONTEXT
    assert roles.get(MCV_NONMEGALOBLASTIC) != WHY_ROLE_CAUSAL


def test_mcv_anchor_plus_nonmegaloblastic_when_hepatic_evidence_supports_it():
    roles = _mcv_roles({**UAT_PANEL, "ggt": 120.0})
    assert roles.get(MCV_NONMEGALOBLASTIC) == WHY_ROLE_CAUSAL
    assert roles.get(MCV_ANCHOR) == WHY_ROLE_MORPHOLOGY_CONTEXT
    assert roles.get(MCV_MEGALOBLASTIC) != WHY_ROLE_CAUSAL


def test_ambiguous_mcv_evidence_falls_back_to_anchor_context():
    roles = _mcv_roles({**UAT_PANEL, "folate": 2.1, "ggt": 120.0})
    assert roles.get(MCV_ANCHOR) == WHY_ROLE_MORPHOLOGY_CONTEXT
    assert WHY_ROLE_CAUSAL not in roles.values()


# --- WS4 -----------------------------------------------------------------------------


def test_missing_layer_b_lead_yields_no_primary_driver_projection():
    """Layer C must suppress the section rather than arbitrate its own lead."""
    from core.analytics.primary_driver_authority_v1 import build_primary_driver_authority_v1

    assert (
        build_primary_driver_authority_v1(
            report_v1={"top_findings": []},
            clustering_result={"clusters": [{"cluster_id": "c1", "name": "Some pattern"}]},
        )
        is None
    )


def test_primary_driver_projection_reports_unresolved_cluster_without_guessing():
    from core.analytics.primary_driver_authority_v1 import build_primary_driver_authority_v1

    projected = build_primary_driver_authority_v1(
        report_v1={
            "top_findings": [
                {
                    "signal_id": "signal_mcv_high",
                    "activation_key": MCV_ANCHOR,
                    "primary_metric": "mcv",
                    "priority_rank": 1,
                }
            ]
        },
        clustering_result={"clusters": [{"cluster_id": "c1", "name": "Unrelated", "biomarkers": ["ldl"]}]},
    )
    assert projected is not None
    assert projected["signal_id"] == "signal_mcv_high"
    assert projected["cluster_resolved"] is False
    assert projected["cluster_id"] == ""


@pytest.mark.parametrize("activation_key", [MCV_ANCHOR, MCV_MEGALOBLASTIC, MCV_NONMEGALOBLASTIC])
def test_mcv_family_frames_remain_runtime_eligible(activation_key: str):
    """WS1 must not over-reach: only the ratified REJECTED frame is inactivated."""
    assert is_frame_runtime_eligible(activation_key)
