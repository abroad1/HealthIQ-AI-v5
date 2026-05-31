"""
LAYER-B-1 — narrative brief maturity regression tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.narrative_payload_builder_v1 import build_narrative_payload_v1
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.narrative_payload_v1 import (
    DEFAULT_LLM_PROHIBITED_ACTIONS,
    NarrativeSectionIdV1,
    WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS,
)
from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportMetaV1,
    ReportTopFindingV1,
    ReportV1,
)
from core.llm.validator_v2 import validate_llm_output_v2

_REPO = Path(__file__).resolve().parents[3]
_FRONTEND_RESULTS = _REPO / "frontend" / "app" / "(app)" / "results" / "page.tsx"


def _minimal_report(*, confidence: float = 0.72, with_root_cause: bool = False) -> ReportV1:
    meta = ReportMetaV1(
        signal_registry_version="reg_v1",
        signal_registry_hash_sha256="0" * 64,
        interaction_map_revision="imap_v1",
        safety_contract_version="safe_v1",
        generated_at="2026-05-31T00:00:00Z",
    )
    tf = ReportTopFindingV1(
        priority_rank=1,
        signal_id="signal_glucose_high",
        system="metabolic",
        signal_state="suboptimal",
        confidence=confidence,
        primary_metric="glucose",
        why_it_matters="Elevated glycaemic markers warrant contextual interpretation.",
    )
    return ReportV1(
        actions=ReportActionsV1(),
        meta=meta,
        top_findings=[tf],
        root_cause_v1=None,
        intervention_annotations_v1=None,
    )


@pytest.mark.regression
def test_narrative_brief_has_required_section_intents():
    payload = build_narrative_payload_v1(analysis_id="lb1-a1", report_v1=_minimal_report())
    required = {
        NarrativeSectionIdV1.hero_main_finding.value,
        NarrativeSectionIdV1.primary_finding_why.value,
        NarrativeSectionIdV1.whats_working_well.value,
        NarrativeSectionIdV1.health_systems_context.value,
        NarrativeSectionIdV1.patterns_across_body.value,
        NarrativeSectionIdV1.marker_evidence.value,
        NarrativeSectionIdV1.missing_evidence_limitations.value,
        NarrativeSectionIdV1.next_steps_narrative.value,
        NarrativeSectionIdV1.technical_clinician_detail.value,
    }
    assert required.issubset(set(payload.section_intents.keys()))
    hero = payload.section_intents[NarrativeSectionIdV1.hero_main_finding.value]
    hs = payload.section_intents[NarrativeSectionIdV1.health_systems_context.value]
    assert hero.purpose
    assert hs.purpose
    assert hero.section_id != hs.section_id


@pytest.mark.regression
def test_health_systems_evidence_boundary_blocks_hidden_subsystems_as_score_basis():
    payload = build_narrative_payload_v1(analysis_id="lb1-a2", report_v1=_minimal_report())
    boundary = payload.evidence_boundaries[NarrativeSectionIdV1.health_systems_context.value]
    for hid in WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS:
        assert hid in boundary.forbidden_as_score_basis


@pytest.mark.regression
def test_score_hierarchy_guidance_present_in_layer_b():
    payload = build_narrative_payload_v1(analysis_id="lb1-a3", report_v1=_minimal_report())
    assert payload.score_hierarchy is not None
    assert payload.score_hierarchy.overall_score_must_not_compete_with_primary_finding
    assert payload.score_hierarchy.marker_scores_must_not_dominate_main_narrative
    assert payload.score_hierarchy.guidance_lines


@pytest.mark.regression
def test_future_llm_translation_constraints_prohibit_reasoning():
    payload = build_narrative_payload_v1(analysis_id="lb1-a4", report_v1=_minimal_report())
    constraints = payload.future_llm_translation_constraints
    assert constraints is not None
    assert "reason_independently" in constraints.prohibited_actions
    assert constraints.llm_role == "translate_governed_brief_only"


@pytest.mark.regression
def test_low_confidence_lead_selects_express_uncertainty_intent():
    payload = build_narrative_payload_v1(
        analysis_id="lb1-a5",
        report_v1=_minimal_report(confidence=0.4),
    )
    retail = payload.section_intents[NarrativeSectionIdV1.retail_summary.value]
    assert retail.intent_code.value == "express_uncertainty"


@pytest.mark.regression
def test_compiler_records_narrative_brief_consumption_meta():
    payload = build_narrative_payload_v1(analysis_id="lb1-a6", report_v1=_minimal_report())
    nr = compile_narrative_report_v1(
        analysis_id="lb1-a6",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    digest = nr.meta.get("narrative_payload_v1_digest") or {}
    assert digest.get("score_hierarchy_present") is True
    assert digest.get("llm_constraints_present") is True
    brief = nr.meta.get("narrative_brief_v1") or {}
    assert brief.get("section_intent_count", 0) >= 9


@pytest.mark.regression
def test_validator_rejects_independent_reasoning_when_layer_b_constraints_present():
    prompt = {
        "biomarkers": [],
        "clusters": [],
        "layer_b_llm_prohibited_actions": list(DEFAULT_LLM_PROHIBITED_ACTIONS),
    }
    bad = {
        "insights": [
            {
                "id": "metabolic_health",
                "title": "I reasoned independently about glucose",
                "severity": "moderate",
                "confidence": 0.5,
                "evidence": [],
                "actions": [],
                "red_flags": [],
            }
        ],
        "tokens_used": 1,
        "latency_ms": 1,
    }
    with pytest.raises(ValueError, match="independent reasoning"):
        validate_llm_output_v2(prompt, bad)


@pytest.mark.regression
def test_frontend_results_page_does_not_infer_narrative_priority():
    src = _FRONTEND_RESULTS.read_text(encoding="utf-8")
    assert "knowledge_bus" not in src
    assert "Pass_3" not in src
    assert "section_intent" not in src.lower() or "narrative_report_v1" in src
