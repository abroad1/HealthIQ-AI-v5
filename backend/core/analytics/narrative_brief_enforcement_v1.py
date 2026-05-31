"""
LAYER-B-1 — enforce NarrativePayloadV1 section intents during deterministic assembly.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.contracts.narrative_payload_v1 import (
    NarrativePayloadV1,
    NarrativeSectionIdV1,
    NarrativeSectionIntentV1,
)


def _intent(payload: NarrativePayloadV1, section_id: NarrativeSectionIdV1) -> Optional[NarrativeSectionIntentV1]:
    row = payload.section_intents.get(section_id.value)
    return row if isinstance(row, NarrativeSectionIntentV1) else None


def _source_available(payload: NarrativePayloadV1, source_key: str) -> bool:
    key = (source_key or "").strip()
    if not key:
        return False
    if key == "report_v1.top_findings":
        return bool(payload.top_findings)
    if key == "report_v1.root_cause_v1":
        rc = payload.root_cause_v1
        return rc is not None and bool(getattr(rc, "findings", None))
    if key == "report_v1.actions":
        actions = getattr(payload.report_v1, "actions", None)
        return actions is not None
    if key == "report_v1":
        return payload.report_v1 is not None
    if key.startswith("report_v1."):
        return True
    if key in ("idl_bundle", "interpretation_entities_v1", "functional_interpretation_v1"):
        return True
    if key in ("insight_graph.signal_results", "pathway_explainers_v1"):
        return True
    if key in (
        "interpretation_display_layer_v1",
        "clinician_report_v1.sections.page1",
        "clinician_report_v1.data_quality",
        "clinician_report_v1",
        "balanced_systems_v1",
        "consumer_domain_scores",
        "consumer_domain_scores.evidence_completeness",
        "consumer_domain_scores.evidence_limitations_line",
        "consumer_domain_scores.marker_evidence",
        "wave1_visible_subsystems",
        "biomarkers",
        "wave1_aligned_drivers",
        "narrative_report_v1.retail_summary",
        "narrative_report_v1.clinician_synthesis",
    ):
        return True
    return False


def section_sources_available(payload: NarrativePayloadV1, section_id: NarrativeSectionIdV1) -> bool:
    """True when at least one permitted source for the section is available on the payload."""
    intent = _intent(payload, section_id)
    if intent is None:
        return True
    permitted = list(intent.permitted_source_fields or [])
    if not permitted:
        return True
    return any(_source_available(payload, src) for src in permitted)


def should_omit_section(payload: NarrativePayloadV1, section_id: NarrativeSectionIdV1) -> bool:
    intent = _intent(payload, section_id)
    if intent is None:
        return False
    if intent.fallback_rule != "omit_section_if_sources_missing":
        return False
    return not section_sources_available(payload, section_id)


def record_brief_consumption_meta(
    payload: NarrativePayloadV1,
    compiler_meta: Dict[str, Any],
) -> None:
    """Record which compiler sections were governed by the narrative brief."""
    compiler_sections = {
        "retail_summary": NarrativeSectionIdV1.retail_summary,
        "lead_narrative": NarrativeSectionIdV1.lead_narrative,
        "body_overview": NarrativeSectionIdV1.body_overview,
        "next_steps_narrative": NarrativeSectionIdV1.next_steps_narrative,
        "clinician_synthesis": NarrativeSectionIdV1.clinician_synthesis,
    }
    consumed: List[str] = []
    omitted: List[str] = []
    for name, sid in compiler_sections.items():
        if should_omit_section(payload, sid):
            omitted.append(name)
        else:
            consumed.append(name)
    compiler_meta["narrative_brief_v1"] = {
        "payload_schema_version": payload.payload_schema_version,
        "report_story_priority": list(payload.report_story_priority or []),
        "section_intent_count": len(payload.section_intents or {}),
        "evidence_boundary_count": len(payload.evidence_boundaries or {}),
        "compiler_sections_consumed": consumed,
        "compiler_sections_omitted": omitted,
        "score_hierarchy_present": payload.score_hierarchy is not None,
        "llm_constraints_present": payload.future_llm_translation_constraints is not None,
    }
