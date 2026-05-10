"""
Deterministic builder: ReportV1 (+ optional annotations) → NarrativePayloadV1 (WP2 Path B).
"""

from __future__ import annotations

from typing import Dict, Optional

from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.narrative_payload_v1 import (
    DEFAULT_PROHIBITED_CLAIM_PATTERNS,
    NarrativeClaimBoundaryV1,
    NarrativeClaimStrengthV1,
    NarrativeIntentCodeV1,
    NarrativePayloadV1,
    NarrativeSectionIdV1,
    NarrativeSectionIntentV1,
)
from core.contracts.report_v1 import ReportV1


def _default_section_intents() -> Dict[str, NarrativeSectionIntentV1]:
    return {
        NarrativeSectionIdV1.retail_summary.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.retail_summary,
            intent_code=NarrativeIntentCodeV1.prioritise,
            permitted_source_fields=["report_v1.top_findings", "idl_bundle"],
        ),
        NarrativeSectionIdV1.lead_narrative.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.lead_narrative,
            intent_code=NarrativeIntentCodeV1.explain_mechanism,
            permitted_source_fields=[
                "report_v1.top_findings",
                "report_v1.root_cause_v1",
                "insight_graph.signal_results",
            ],
        ),
        NarrativeSectionIdV1.body_overview.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.body_overview,
            intent_code=NarrativeIntentCodeV1.reassure,
            permitted_source_fields=[
                "report_v1.top_findings",
                "interpretation_entities_v1",
                "functional_interpretation_v1",
            ],
        ),
        NarrativeSectionIdV1.next_steps_narrative.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.next_steps_narrative,
            intent_code=NarrativeIntentCodeV1.frame_next_steps,
            permitted_source_fields=[
                "report_v1.actions",
                "report_v1.top_findings",
                "pathway_explainers_v1",
            ],
        ),
        NarrativeSectionIdV1.clinician_synthesis.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.clinician_synthesis,
            intent_code=NarrativeIntentCodeV1.support_clinician_fast_read,
            permitted_source_fields=[
                "report_v1",
                "idl_bundle",
                "interpretation_entities_v1",
            ],
        ),
    }


def build_narrative_payload_v1(
    *,
    analysis_id: str,
    report_v1: ReportV1,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None,
) -> NarrativePayloadV1:
    ia = intervention_annotations_v1
    if ia is None:
        ia = report_v1.intervention_annotations_v1

    boundaries = NarrativeClaimBoundaryV1(
        allowed_claim_strength=NarrativeClaimStrengthV1.pattern_and_association_only,
        prohibited_claim_patterns=list(DEFAULT_PROHIBITED_CLAIM_PATTERNS),
        clinician_only_reserved=True,
    )

    return NarrativePayloadV1(
        analysis_id=analysis_id,
        report_v1=report_v1,
        top_findings=list(report_v1.top_findings),
        root_cause_v1=report_v1.root_cause_v1,
        intervention_annotations_v1=ia,
        section_intents=_default_section_intents(),
        claim_boundaries=boundaries,
    )
