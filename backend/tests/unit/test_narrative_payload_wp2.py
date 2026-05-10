"""WP2 — NarrativePayloadV1 contract + deterministic builder."""

from __future__ import annotations

from core.analytics.narrative_payload_builder_v1 import build_narrative_payload_v1
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.narrative_payload_v1 import NarrativeSectionIdV1
from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportMetaV1,
    ReportTopFindingV1,
    ReportV1,
)


def _minimal_report_v1() -> ReportV1:
    meta = ReportMetaV1(
        signal_registry_version="reg_v1",
        signal_registry_hash_sha256="0" * 64,
        interaction_map_revision="imap_v1",
        safety_contract_version="safe_v1",
        generated_at="2026-05-09T00:00:00Z",
    )
    tf = ReportTopFindingV1(
        priority_rank=1,
        signal_id="signal_glucose_high",
        system="metabolic",
        signal_state="suboptimal",
        confidence=0.72,
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


def test_narrative_payload_schema_and_builder_carries_report_slices() -> None:
    rep = _minimal_report_v1()
    payload = build_narrative_payload_v1(analysis_id="wp2-a1", report_v1=rep)

    assert payload.analysis_id == "wp2-a1"
    assert len(payload.top_findings) == 1
    assert payload.top_findings[0].signal_id == "signal_glucose_high"
    assert payload.root_cause_v1 is None
    assert payload.report_v1 is rep

    keys = set(payload.section_intents.keys())
    assert keys == {
        NarrativeSectionIdV1.retail_summary.value,
        NarrativeSectionIdV1.lead_narrative.value,
        NarrativeSectionIdV1.body_overview.value,
        NarrativeSectionIdV1.next_steps_narrative.value,
        NarrativeSectionIdV1.clinician_synthesis.value,
    }


def test_compile_narrative_report_v1_accepts_payload_meta_digest() -> None:
    rep = _minimal_report_v1()
    payload = build_narrative_payload_v1(analysis_id="wp2-a2", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="wp2-a2",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    meta = nr.meta
    assert meta.get("narrative_payload_v1_present") is True
    digest = meta.get("narrative_payload_v1_digest") or {}
    assert digest.get("lead_signal_id") == "signal_glucose_high"
    assert digest.get("top_finding_count") == 1
