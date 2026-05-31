"""LC-S3 — NarrativePayloadV1-primary deterministic narrative assembly."""

from __future__ import annotations

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


def _report_with_root_cause() -> ReportV1:
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
        hypothesis_id="hyp_lc_s3_a",
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
    rc = RootCauseV1(findings=[finding])
    return ReportV1(
        actions=ReportActionsV1(),
        meta=meta,
        top_findings=[lead, secondary],
        root_cause_v1=rc,
        intervention_annotations_v1=None,
    )


def test_lc_s3_compiler_uses_payload_and_populates_five_sections() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-a", report_v1=rep)
    ig = {"primary_driver_system_id": "metabolic", "supporting_systems": ["lipid"], "system_capacity_scores": {}}
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-a",
        meta={},
        insight_graph=ig,
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert nr.meta.get("narrative_payload_v1_present") is True
    assert nr.meta.get("lc_s3_assembly_version") == "1.1"
    for field in (
        "retail_summary",
        "lead_narrative",
        "body_overview",
        "next_steps_narrative",
        "clinician_synthesis",
    ):
        assert getattr(nr, field).strip(), f"{field} should be non-empty under LC-S3"


def test_lc_s3_lead_signal_echoed_in_consumer_copy() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-b", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-b",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    blob = (nr.retail_summary + nr.body_overview).lower()
    assert "signal_glucose_high" in blob or "glucose high" in blob


def test_lc_s3_hypothesis_block_surfaces_without_invention() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-c", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-c",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert "Nutrient–enzyme cofactor limitation" in nr.lead_narrative
    assert "hyp_lc_s3_a" not in nr.lead_narrative


def test_lc_s3_next_steps_avoids_prescriptive_artefacts() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-d", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-d",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    low = nr.next_steps_narrative.lower()
    assert "medication recommendation" not in low
    assert "supplement recommendation" not in low
    assert "treatment recommendation" not in low


def test_lc_s3_clinician_block_has_fast_read_header() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-e", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-e",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert "Clinician fast-read" in nr.clinician_synthesis
    assert "Nutrient–enzyme cofactor limitation" in nr.clinician_synthesis


def test_lc_s3_secondary_ranked_echoes_second_finding() -> None:
    rep = _report_with_root_cause()
    payload = build_narrative_payload_v1(analysis_id="lc-s3-f", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-f",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert "Other patterns noted on this panel" in nr.secondary_narratives or "Other patterns considered on this panel" in nr.secondary_narratives
    assert "ldl" in nr.secondary_narratives.lower()


def test_lc_s3_missing_root_cause_handled_without_raise() -> None:
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
        confidence=0.5,
        primary_metric="glucose",
        why_it_matters="Markers warrant contextual review.",
    )
    rep = ReportV1(
        actions=ReportActionsV1(),
        meta=meta,
        top_findings=[lead],
        root_cause_v1=None,
        intervention_annotations_v1=None,
    )
    payload = build_narrative_payload_v1(analysis_id="lc-s3-g", report_v1=rep)
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-g",
        meta={},
        insight_graph={"primary_driver_system_id": "metabolic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert nr.retail_summary.strip()
    assert nr.meta.get("lc_s3_assembly_version") == "1.1"


def test_lc_s3_absent_payload_preserves_legacy_shape() -> None:
    nr = compile_narrative_report_v1(
        analysis_id="lc-s3-h",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=None,
    )
    assert nr.meta.get("narrative_payload_v1_present") is None
    assert nr.meta.get("lc_s3_assembly_version") is None
