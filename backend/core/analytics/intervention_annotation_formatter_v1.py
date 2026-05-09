"""
LC-S2+ deterministic surface formatting for InterventionAnnotationsV1.

Kept separate from intervention_annotation_compiler_v1.py (LOCKED compiler scope).
"""

from __future__ import annotations

from typing import List, Optional

from core.contracts.intervention_annotation_v1 import (
    InterventionAnnotationResolvedV1,
    InterventionAnnotationsV1,
)


def _statin_resolved_rows(ann: Optional[InterventionAnnotationsV1]) -> List[InterventionAnnotationResolvedV1]:
    if ann is None:
        return []
    return [r for r in ann.resolved if r.intervention_class_id == "lipid_lowering_statin"]


def format_intervention_annotation_narrative_appendix_v1(
    ann: Optional[InterventionAnnotationsV1],
) -> str:
    """
    Deterministic Layer B framing lines derived only from registry-emitted effects (LC-S2 surface).
    """
    rows = _statin_resolved_rows(ann)
    if not rows:
        return ""
    blocks: List[str] = []
    for res in rows:
        eff_bits: List[str] = []
        for eff in res.effects:
            mr = (eff.monitoring_relevance or "").strip()
            mr_part = f"; monitoring={mr}" if mr else ""
            eff_bits.append(
                f"{eff.effect_type} [{', '.join(eff.biomarker_ids)}] direction={eff.expected_direction}{mr_part}"
            )
        if not eff_bits:
            continue
        blocks.append(
            "Layer B intervention annotation — lipid-lowering statin (user-reported; framing only; "
            "does not alter signal states, bands, or rankings): "
            + "; ".join(eff_bits)
        )
    return "\n\n".join(blocks)


def format_intervention_annotation_clinician_page1_v1(
    ann: Optional[InterventionAnnotationsV1],
) -> str:
    """Clinician page-1 context block — registry-derived, identical semantics to narrative appendix."""
    return format_intervention_annotation_narrative_appendix_v1(ann)


def format_intervention_annotation_consumer_cv_suffix_v1(
    ann: Optional[InterventionAnnotationsV1],
) -> str:
    """Short cardiovascular-domain consequence suffix for Wave-1 consumer cards."""
    base = format_intervention_annotation_narrative_appendix_v1(ann)
    if not base:
        return ""
    return ("Medication context: " + base)[:420]
