"""
DOMAIN-UX1C — Governed Wave 1 subsystem evidence for Health Systems Cards.

Single authority for subsystem-to-marker mapping. Frontend must not duplicate.
Wave 1 domains only: cardiovascular, blood sugar, liver.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Sequence, Set, Tuple

from core.models.results import SubsystemEvidenceV1

# --- Subsystem definitions (stable ids + consumer labels + expected canonical markers) ---

@dataclass(frozen=True)
class _Wave1SubsystemDef:
    subsystem_id: str
    subsystem_label: str
    expected_marker_ids: Tuple[str, ...]
    source_trace: str


_WAVE1_CV_LIPID = _Wave1SubsystemDef(
    subsystem_id="wave1_cv_lipid_transport",
    subsystem_label="Lipid transport",
    expected_marker_ids=(
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "tc_hdl_ratio",
    ),
    source_trace="wave1_subsystem_evidence_v1:wave1_cardiovascular:lipid_transport",
)

_WAVE1_CV_HCY = _Wave1SubsystemDef(
    subsystem_id="wave1_cv_homocysteine_pathway",
    subsystem_label="Homocysteine pathway",
    expected_marker_ids=("homocysteine",),
    source_trace="wave1_subsystem_evidence_v1:wave1_cardiovascular:homocysteine_pathway",
)

_WAVE1_CV_VASCULAR = _Wave1SubsystemDef(
    subsystem_id="wave1_cv_vascular_strain",
    subsystem_label="Vascular strain context",
    expected_marker_ids=("crp",),
    source_trace="wave1_subsystem_evidence_v1:wave1_cardiovascular:vascular_strain",
)

_WAVE1_MET_GLYCAEMIC = _Wave1SubsystemDef(
    subsystem_id="wave1_met_glycaemic_control",
    subsystem_label="Glycaemic control",
    expected_marker_ids=("glucose", "hba1c"),
    source_trace="wave1_subsystem_evidence_v1:wave1_blood_sugar:glycaemic_control",
)

_WAVE1_MET_INSULIN = _Wave1SubsystemDef(
    subsystem_id="wave1_met_insulin_metabolic",
    subsystem_label="Insulin and metabolic context",
    expected_marker_ids=("insulin", "triglycerides"),
    source_trace="wave1_subsystem_evidence_v1:wave1_blood_sugar:insulin_metabolic",
)

_WAVE1_LIV_ENZYMES = _Wave1SubsystemDef(
    subsystem_id="wave1_liv_enzyme_pattern",
    subsystem_label="Liver enzyme pattern",
    expected_marker_ids=("alt", "ast", "ggt"),
    source_trace="wave1_subsystem_evidence_v1:wave1_liver:enzyme_pattern",
)

_WAVE1_LIV_PROCESSING = _Wave1SubsystemDef(
    subsystem_id="wave1_liv_processing_context",
    subsystem_label="Liver processing context",
    expected_marker_ids=("alp", "albumin", "bilirubin", "total_bilirubin"),
    source_trace="wave1_subsystem_evidence_v1:wave1_liver:processing_context",
)

WAVE1_DOMAIN_SUBSYSTEM_DEFS: Dict[str, Tuple[_Wave1SubsystemDef, ...]] = {
    "wave1_cardiovascular": (_WAVE1_CV_LIPID, _WAVE1_CV_HCY, _WAVE1_CV_VASCULAR),
    "wave1_blood_sugar": (_WAVE1_MET_GLYCAEMIC, _WAVE1_MET_INSULIN),
    "wave1_liver": (_WAVE1_LIV_ENZYMES, _WAVE1_LIV_PROCESSING),
}

WAVE1_DOMAIN_IDS: FrozenSet[str] = frozenset(WAVE1_DOMAIN_SUBSYSTEM_DEFS.keys())


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


def _partition_subsystem_markers(
    *,
    expected: Sequence[str],
    panel_biomarker_ids: Set[str],
    scored_on_rail: Set[str],
) -> Tuple[List[str], List[str]]:
    expected_set = set(expected)
    present_or_scored = (panel_biomarker_ids | scored_on_rail) & expected_set
    included = sorted(present_or_scored)
    missing = sorted(expected_set - present_or_scored)
    return included, missing


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
    defs = WAVE1_DOMAIN_SUBSYSTEM_DEFS.get(domain_id)
    if not defs:
        return []

    scored = _scored_marker_ids_on_rail(rail_biomarker_scores)
    rows: List[SubsystemEvidenceV1] = []
    for spec in defs:
        included, missing = _partition_subsystem_markers(
            expected=spec.expected_marker_ids,
            panel_biomarker_ids=panel_biomarker_ids,
            scored_on_rail=scored,
        )
        rows.append(
            SubsystemEvidenceV1(
                subsystem_id=spec.subsystem_id,
                subsystem_label=spec.subsystem_label,
                included_marker_ids=included,
                missing_marker_ids=missing,
                status_label=None,
                evidence_role=None,
                source_trace=spec.source_trace,
            )
        )
    return rows
