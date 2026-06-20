"""
DOMAIN-UX1C — Governed Wave 1 subsystem evidence for Health Systems Cards.

Single authority for subsystem-to-marker mapping. Frontend must not duplicate.
Wave 1 domains only: cardiovascular, blood sugar, liver, kidney, blood / iron / oxygen.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Set, Tuple

from core.knowledge.health_system_card_evidence import (
    PILOT_COMPILED_SUBSYSTEM_IDS,
    assemble_subsystem_from_compiled_card_evidence,
)
from core.knowledge.domain_flat_card_evidence import assemble_domain_flat_evidence
from core.models.results import DomainFlatEvidenceV1, SubsystemEvidenceV1

# Stable assembly order per domain (compiled card evidence only; no hard-coded fallback).
_WAVE1_DOMAIN_SUBSYSTEM_ORDER: Dict[str, Tuple[str, ...]] = {
    "wave1_cardiovascular": (
        "wave1_cv_lipid_transport",
        "wave1_cv_homocysteine_pathway",
        "wave1_cv_vascular_strain",
    ),
    "wave1_blood_sugar": (
        "wave1_met_glycaemic_control",
        "wave1_met_insulin_metabolic",
    ),
    "wave1_liver": (
        "wave1_liv_enzyme_pattern",
        "wave1_liv_processing_context",
    ),
    "wave1_kidney": (
        "wave1_ren_glomerular_filtration",
    ),
    "wave1_blood_iron_oxygen": (
        "wave1_bio_oxygen_carrying_capacity",
    ),
}

WAVE1_DOMAIN_IDS: FrozenSet[str] = frozenset(_WAVE1_DOMAIN_SUBSYSTEM_ORDER.keys())


def _scored_marker_ids_on_rail(rail_biomarker_scores: object) -> Set[str]:
    if not isinstance(rail_biomarker_scores, list):
        return set()
    out: Set[str] = set()
    for item in rail_biomarker_scores:
        if isinstance(item, dict):
            name = item.get("biomarker_name")
        else:
            name = getattr(item, "biomarker_name", None)
        if name and str(name).strip():
            out.add(str(name).strip())
    return out


def assemble_wave1_subsystem_evidence(
    *,
    domain_id: str,
    panel_biomarker_ids: Set[str],
    rail_biomarker_scores: object,
) -> List[SubsystemEvidenceV1]:
    """
    Build governed subsystem rows for a Wave 1 domain.
    Returns empty list for unknown domain ids (Wave 2 protection).
    """
    subsystem_ids = _WAVE1_DOMAIN_SUBSYSTEM_ORDER.get(domain_id)
    if not subsystem_ids:
        return []

    scored = _scored_marker_ids_on_rail(rail_biomarker_scores)
    rows: List[SubsystemEvidenceV1] = []
    for subsystem_id in subsystem_ids:
        if subsystem_id not in PILOT_COMPILED_SUBSYSTEM_IDS:
            continue
        compiled_row = assemble_subsystem_from_compiled_card_evidence(
            subsystem_id=subsystem_id,
            panel_biomarker_ids=panel_biomarker_ids,
            scored_on_rail=scored,
        )
        if compiled_row is not None:
            rows.append(compiled_row)
    return rows


def assemble_wave1_flat_domain_evidence(
    *,
    domain_id: str,
    panel_biomarker_ids: Set[str],
    rail_biomarker_scores: object,
) -> DomainFlatEvidenceV1 | None:
    """KB-UTIL-1 flat domain evidence (Wave 1 liver only)."""
    if domain_id != "wave1_liver":
        return None
    scored = _scored_marker_ids_on_rail(rail_biomarker_scores)
    return assemble_domain_flat_evidence(
        domain_id=domain_id,
        panel_biomarker_ids=panel_biomarker_ids,
        scored_on_rail=scored,
    )
