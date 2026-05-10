"""
Sentinel regression guard — NarrativePayloadV1 assembly surface (LC-S3).

Guards the payload-primary Layer C assembly path introduced in LC-S3.
Complements test_narrative_compiler_why_surface_regression.py, which guards
the legacy insight_graph path only.

Marked @pytest.mark.regression so Sentinel picks these up via -m regression.
"""

from __future__ import annotations

import pytest

from core.analytics.narrative_payload_builder_v1 import build_narrative_payload_v1
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportMetaV1,
    ReportTopFindingV1,
    ReportV1,
)
from core.contracts.root_cause_v1 import (
    RootCauseConfirmatoryTestV1,
    RootCauseEvidenceItemV1,
    RootCauseFindingV1,
    RootCauseHypothesisV1,
    RootCauseMissingItemV1,
    RootCauseV1,
)


def _baseline_report() -> ReportV1:
    meta = ReportMetaV1(
        signal_registry_version="reg_v1",
        signal_registry_hash_sha256="0" * 64,
        interaction_map_revision="imap_v1",
        safety_contract_version="safe_v1",
        generated_at="2026-05-10T00:00:00Z",
    )
    lead = ReportTopFindingV1(
        priority_rank=1,
        signal_id="signal_glucose_high",
        system="metabolic",
        signal_state="suboptimal",
        confidence=0.72,
        confidence_reasons=["marker_vs_lab_range"],
        primary_metric="glucose",
        supporting_markers=["hba1c"],
        why_it_matters="Glycaemic signals sit outside the optimal band on this snapshot.",
    )
    secondary = ReportTopFindingV1(
        priority_rank=2,
        signal_id="signal_ldl_cholesterol_high",
        system="lipid",
        signal_state="suboptimal",
        confidence=0.58,
        primary_metric="ldl_cholesterol",
        why_it_matters="LDL particle burden adds lipid-context priority behind the lead.",
    )
    hyp = RootCauseHypothesisV1(
        hypothesis_id="hyp_sentinel_baseline",
        title="Nutrient–enzyme cofactor limitation",
        summary="May reflect one-carbon pathway strain alongside glycaemic pressure.",
        hypothesis_confidence=0.61,
        evidence_for=[
            RootCauseEvidenceItemV1(item="Glucose above personalised optimal band.", marker_refs=["glucose"])
        ],
        evidence_against=[
            RootCauseEvidenceItemV1(item="Limited fasting context captured here.", marker_refs=[])
        ],
        missing_data=[
            RootCauseMissingItemV1(marker_id="fasting_insulin", reason="Not present on this panel.")
        ],
        confirmatory_tests=[
            RootCauseConfirmatoryTestV1(
                test_id="t_follow_labs",
                display_name="Clinician-directed metabolic follow-up labs",
                rationale="Layer B lists structured confirmatory options only.",
            )
        ],
        safety_class="standard",
    )
    finding = RootCauseFindingV1(
        signal_id="signal_glucose_high",
        primary_metric="glucose",
        signal_state="suboptimal",
        signal_confidence=0.72,
        hypotheses=[hyp],
    )
    return ReportV1(
        actions=ReportActionsV1(),
        meta=meta,
        top_findings=[lead, secondary],
        root_cause_v1=RootCauseV1(findings=[finding]),
        intervention_annotations_v1=None,
    )


@pytest.mark.regression
def test_payload_assembly_five_sections_populated() -> None:
    """When NarrativePayloadV1 is supplied, all five governed sections must be non-empty."""
    rep = _baseline_report()
    payload = build_narrative_payload_v1(analysis_id="sentinel-reg-a", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="sentinel-reg-a",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert nr.meta.get("lc_s3_assembly_version") == "1", "LC-S3 assembly path not taken"
    for field in ("retail_summary", "lead_narrative", "body_overview", "next_steps_narrative", "clinician_synthesis"):
        assert getattr(nr, field).strip(), f"Section '{field}' must be non-empty under payload assembly"


@pytest.mark.regression
def test_payload_assembly_absent_payload_preserves_legacy_shape() -> None:
    """Without a payload, compiler must take the legacy path — no LC-S3 metadata emitted."""
    nr = compile_narrative_report_v1(
        analysis_id="sentinel-reg-b",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=None,
    )
    assert nr.meta.get("narrative_payload_v1_present") is None, "Legacy path must not set payload flag"
    assert nr.meta.get("lc_s3_assembly_version") is None, "Legacy path must not set assembly version"


@pytest.mark.regression
def test_payload_assembly_no_prescriptive_language_in_next_steps() -> None:
    """Next-steps section must not emit medication, supplement, or treatment recommendations."""
    rep = _baseline_report()
    payload = build_narrative_payload_v1(analysis_id="sentinel-reg-c", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="sentinel-reg-c",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    low = nr.next_steps_narrative.lower()
    for banned in ("medication recommendation", "supplement recommendation", "treatment recommendation"):
        assert banned not in low, f"Prohibited claim '{banned}' found in next_steps_narrative"


@pytest.mark.regression
def test_payload_assembly_lead_signal_present_in_consumer_copy() -> None:
    """Lead signal identifier or humanised form must appear in retail_summary or body_overview."""
    rep = _baseline_report()
    payload = build_narrative_payload_v1(analysis_id="sentinel-reg-d", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="sentinel-reg-d",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    blob = (nr.retail_summary + nr.body_overview).lower()
    assert "signal_glucose_high" in blob or "glucose high" in blob, (
        "Lead signal not surfaced in consumer copy"
    )


@pytest.mark.regression
def test_payload_assembly_claim_boundary_enforcement() -> None:
    """Default prohibited claim patterns must be absent from all assembled sections."""
    rep = _baseline_report()
    payload = build_narrative_payload_v1(analysis_id="sentinel-reg-e", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="sentinel-reg-e",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    prohibited = [
        "diagnosis", "diagnoses", "diagnostic", "confirms", "confirmed",
        "rules out", "guarantees", "treatment recommendation",
        "medication recommendation", "supplement recommendation",
    ]
    for section_name in ("retail_summary", "lead_narrative", "body_overview", "next_steps_narrative", "clinician_synthesis"):
        text = getattr(nr, section_name).lower()
        for pattern in prohibited:
            assert pattern not in text, (
                f"Prohibited claim '{pattern}' found in {section_name} after boundary enforcement"
            )
