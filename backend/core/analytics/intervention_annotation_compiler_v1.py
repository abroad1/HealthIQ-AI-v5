"""
KB-S48e deterministic runtime intervention annotation compiler.

Consumes user intervention/exposure documents (mapped rows) and the intervention-effects
registry. Produces parallel InterventionAnnotationsV1 — no signal threshold or state changes.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from core.contracts.intervention_annotation_v1 import (
    InterventionAnnotationEffectV1,
    InterventionAnnotationResolvedV1,
    InterventionAnnotationUnresolvedV1,
    InterventionAnnotationsV1,
)
from core.knowledge.load_intervention_effects_registry_v1 import load_intervention_effects_registry_v1

# Must match validate_user_intervention_exposure.APPROVED_INTERVENTION_CLASS_IDS (test drift guard).
_APPROVED_INTERVENTION_CLASS_IDS: Set[str] = {
    "lipid_lowering_statin",
    "systemic_glucocorticoid",
    "thyroid_hormone_replacement",
    "raas_inhibitor",
    "thiazide_or_loop_diuretic",
    "biguanide_metformin",
    "ppi_long_term_high_dose",
    "sex_hormone_therapy",
}

_EFFECT_TYPES = {
    "interpretation_confounder",
    "expected_biomarker_effect",
    "monitoring_relevance",
    "caveat_only",
}
_DIRECTIONS = {"lower", "raise", "variable", "mixed", "context_dependent"}


def approved_intervention_class_ids_v1() -> frozenset[str]:
    return frozenset(_APPROVED_INTERVENTION_CLASS_IDS)


def _effects_from_registry_row(class_row: Dict[str, Any]) -> List[InterventionAnnotationEffectV1]:
    out: List[InterventionAnnotationEffectV1] = []
    raw = class_row.get("interpretation_effects")
    if not isinstance(raw, list):
        return out
    for eff in raw:
        if not isinstance(eff, dict):
            continue
        et = eff.get("effect_type")
        if et not in _EFFECT_TYPES:
            continue
        bids = eff.get("biomarker_ids")
        if not isinstance(bids, list):
            continue
        biomarker_ids = [str(x).strip() for x in bids if isinstance(x, str) and str(x).strip()]
        if not biomarker_ids:
            continue
        ed = eff.get("expected_direction")
        if ed not in _DIRECTIONS:
            continue
        mr = eff.get("monitoring_relevance")
        mr_out: Optional[str] = None
        if isinstance(mr, str) and mr.strip():
            mr_out = mr.strip()[:500]
        out.append(
            InterventionAnnotationEffectV1(
                effect_type=et,
                biomarker_ids=biomarker_ids,
                expected_direction=ed,
                monitoring_relevance=mr_out,
            )
        )
    return out


def build_intervention_annotations_v1(
    user_intervention_document: Optional[Dict[str, Any]] = None,
) -> Optional[InterventionAnnotationsV1]:
    """
    Build parallel annotations from a user intervention record-set dict (KB-S48d shape).
    Returns None when there is no document, no records list, or nothing to emit after parsing.
    """
    if not user_intervention_document or not isinstance(user_intervention_document, dict):
        return None
    records = user_intervention_document.get("intervention_records")
    if not isinstance(records, list) or not records:
        return None

    classes_by_id, reg_ver, reg_id = load_intervention_effects_registry_v1()
    resolved: List[InterventionAnnotationResolvedV1] = []
    unresolved: List[InterventionAnnotationUnresolvedV1] = []

    for rec in records:
        if not isinstance(rec, dict):
            continue
        rid = rec.get("intervention_record_id")
        if not isinstance(rid, str) or not rid.strip():
            continue
        label = rec.get("entered_label")
        if not isinstance(label, str) or not label.strip():
            continue
        cc = rec.get("canonical_class")
        if not isinstance(cc, dict):
            continue
        ls = cc.get("link_status")
        if ls == "unmapped":
            if cc.get("intervention_class_id") is not None:
                continue
            unresolved.append(
                InterventionAnnotationUnresolvedV1(
                    intervention_record_id=rid.strip(),
                    entered_label=label.strip()[:500],
                )
            )
            continue
        if ls != "mapped":
            continue
        cid = cc.get("intervention_class_id")
        if not isinstance(cid, str) or cid not in _APPROVED_INTERVENTION_CLASS_IDS:
            continue
        class_row = classes_by_id.get(cid)
        if not class_row:
            continue
        effects = _effects_from_registry_row(class_row)
        resolved.append(
            InterventionAnnotationResolvedV1(
                intervention_record_id=rid.strip(),
                entered_label=label.strip()[:500],
                intervention_class_id=cid,
                effects=effects,
            )
        )

    if not resolved and not unresolved:
        return None
    return InterventionAnnotationsV1(
        registry_schema_version=reg_ver,
        registry_id=reg_id or "intervention_effects_registry_v1",
        resolved=resolved,
        unresolved=unresolved,
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
