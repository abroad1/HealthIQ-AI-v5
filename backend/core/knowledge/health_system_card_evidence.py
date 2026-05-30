"""
ARCH-RT-3 — Compiled health-system card evidence loader and validator.

Loads governed YAML artefacts from knowledge_bus/compiled/health_system_cards/.
Fail-closed on invalid structure. No runtime investigation-spec or PSI reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import yaml

from core.canonical.resolver import CanonicalResolver
from core.models.results import (
    MarkerDisplayLabelV1,
    SubsystemEvidenceV1,
    SubsystemMarkerEvidenceV1,
)

SCHEMA_VERSION = "1.0.0"
PILOT_SUBSYSTEM_ID = "wave1_met_glycaemic_control"
WAVE1_COMPILED_SUBSYSTEM_IDS: frozenset[str] = frozenset(
    {
        "wave1_met_glycaemic_control",
        "wave1_cv_lipid_transport",
        "wave1_cv_homocysteine_pathway",
        "wave1_cv_vascular_strain",
        "wave1_met_insulin_metabolic",
        "wave1_liv_enzyme_pattern",
        "wave1_liv_processing_context",
    }
)
PILOT_COMPILED_SUBSYSTEM_IDS = WAVE1_COMPILED_SUBSYSTEM_IDS

_MARKER_ROLES = frozenset(
    {
        "score_contributor",
        "confidence_contributor",
        "contextual_marker",
        "mechanism_marker",
        "differential_marker",
        "exclusion_marker",
        "missing_for_confidence",
        "optional_deeper_marker",
    }
)
_RELATIONSHIP_KINDS = frozenset(
    {
        "direct_score_input",
        "confidence_input",
        "contextual_support",
        "mechanism_context",
        "differential_context",
        "exclusion_gate",
        "optional_depth",
    }
)
_PRESENCE_POLICIES = frozenset(
    {"required_for_subsystem", "optional_on_panel", "contextual_only"}
)
_VISIBILITY_TIERS = frozenset({"scored_subsystem", "contextual_evidence", "hidden_v1"})
_FORBIDDEN_MARKER_IDS = frozenset({"total_bilirubin"})


@dataclass(frozen=True)
class CardEvidenceMarkerDef:
    marker_id: str
    display_label: str
    marker_role: str
    relationship_kind: str
    presence_policy: str
    rationale_short: Optional[str] = None


@dataclass(frozen=True)
class CardEvidenceArtefact:
    schema_version: str
    artefact_id: str
    domain_id: str
    subsystem_id: str
    subsystem_label: str
    visibility_tier: str
    source_spec_ids: Tuple[str, ...]
    compile_manifest_ref: str
    markers: Tuple[CardEvidenceMarkerDef, ...]
    provenance: Mapping[str, Any]
    missing_policy_line: Optional[str] = None
    mechanism_line: Optional[str] = None


class CardEvidenceValidationError(ValueError):
    """Raised when a card evidence artefact fails schema validation."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def schema_path() -> Path:
    return _repo_root() / "knowledge_bus" / "schema" / "health_system_card_evidence_schema_v1.yaml"


def compiled_cards_dir() -> Path:
    return _repo_root() / "knowledge_bus" / "compiled" / "health_system_cards"


def _require_str(data: Mapping[str, Any], key: str, errors: List[str]) -> Optional[str]:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"missing or invalid string field: {key}")
        return None
    return value.strip()


def _require_enum(value: Optional[str], allowed: frozenset[str], field: str, errors: List[str]) -> Optional[str]:
    if value not in allowed:
        errors.append(f"{field} must be one of {sorted(allowed)}; got {value!r}")
        return None
    return value


def validate_card_evidence_payload(payload: Mapping[str, Any], *, path: str = "<memory>") -> None:
    """Fail-closed validation against health_system_card_evidence_schema_v1."""
    errors: List[str] = []

    if not isinstance(payload, dict):
        raise CardEvidenceValidationError(f"{path}: root must be a mapping")

    schema_version = _require_str(payload, "schema_version", errors)
    if schema_version and schema_version != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    for key in (
        "artefact_id",
        "domain_id",
        "subsystem_id",
        "subsystem_label",
        "compile_manifest_ref",
    ):
        _require_str(payload, key, errors)

    visibility = _require_str(payload, "visibility_tier", errors)
    _require_enum(visibility, _VISIBILITY_TIERS, "visibility_tier", errors)

    source_spec_ids = payload.get("source_spec_ids")
    if not isinstance(source_spec_ids, list) or not source_spec_ids:
        errors.append("source_spec_ids must be a non-empty list")
    elif not all(isinstance(x, str) and x.strip() for x in source_spec_ids):
        errors.append("source_spec_ids items must be non-empty strings")

    markers_raw = payload.get("markers")
    if not isinstance(markers_raw, list) or not markers_raw:
        errors.append("markers must be a non-empty list")
    else:
        seen: Set[str] = set()
        for idx, item in enumerate(markers_raw):
            if not isinstance(item, dict):
                errors.append(f"markers[{idx}] must be a mapping")
                continue
            marker_id = _require_str(item, "marker_id", errors)
            if marker_id:
                if marker_id in _FORBIDDEN_MARKER_IDS:
                    errors.append(
                        f"markers[{idx}].marker_id forbidden: {marker_id} "
                        "(WAVE1-EQUIV1 bilirubin canonical policy)"
                    )
                if marker_id in seen:
                    errors.append(f"duplicate marker_id: {marker_id}")
                seen.add(marker_id)
            _require_str(item, "display_label", errors)
            role = _require_str(item, "marker_role", errors)
            _require_enum(role, _MARKER_ROLES, f"markers[{idx}].marker_role", errors)
            rel = _require_str(item, "relationship_kind", errors)
            _require_enum(rel, _RELATIONSHIP_KINDS, f"markers[{idx}].relationship_kind", errors)
            pol = _require_str(item, "presence_policy", errors)
            _require_enum(pol, _PRESENCE_POLICIES, f"markers[{idx}].presence_policy", errors)
            rationale = item.get("rationale_short")
            if rationale is not None and (not isinstance(rationale, str) or not rationale.strip()):
                errors.append(f"markers[{idx}].rationale_short must be a non-empty string when present")

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be a mapping")
    else:
        kind = _require_str(provenance, "artefact_kind", errors)
        if kind and kind != "health_system_card_evidence_v1":
            errors.append("provenance.artefact_kind must be health_system_card_evidence_v1")
        status = _require_str(provenance, "compile_status", errors)
        if status and status not in ("pilot_manual", "compile_pipeline"):
            errors.append("provenance.compile_status invalid")
        spec_prov = provenance.get("source_spec_provenance")
        if spec_prov is not None and spec_prov not in (
            "explicit",
            "inferred_from_package_manifest",
        ):
            errors.append("provenance.source_spec_provenance invalid")

    for opt in ("missing_policy_line", "mechanism_line"):
        val = payload.get(opt)
        if val is not None and (not isinstance(val, str) or not val.strip()):
            errors.append(f"{opt} must be a non-empty string when present")

    if errors:
        joined = "; ".join(errors)
        raise CardEvidenceValidationError(f"{path}: {joined}")


def parse_card_evidence_payload(payload: Mapping[str, Any]) -> CardEvidenceArtefact:
    validate_card_evidence_payload(payload)
    markers: List[CardEvidenceMarkerDef] = []
    for item in payload["markers"]:
        markers.append(
            CardEvidenceMarkerDef(
                marker_id=str(item["marker_id"]).strip(),
                display_label=str(item["display_label"]).strip(),
                marker_role=str(item["marker_role"]).strip(),
                relationship_kind=str(item["relationship_kind"]).strip(),
                presence_policy=str(item["presence_policy"]).strip(),
                rationale_short=(
                    str(item["rationale_short"]).strip()
                    if item.get("rationale_short")
                    else None
                ),
            )
        )
    prov = payload.get("provenance") or {}
    return CardEvidenceArtefact(
        schema_version=str(payload["schema_version"]).strip(),
        artefact_id=str(payload["artefact_id"]).strip(),
        domain_id=str(payload["domain_id"]).strip(),
        subsystem_id=str(payload["subsystem_id"]).strip(),
        subsystem_label=str(payload["subsystem_label"]).strip(),
        visibility_tier=str(payload["visibility_tier"]).strip(),
        source_spec_ids=tuple(str(x).strip() for x in payload["source_spec_ids"]),
        compile_manifest_ref=str(payload["compile_manifest_ref"]).strip(),
        markers=tuple(markers),
        provenance=prov,
        missing_policy_line=(
            str(payload["missing_policy_line"]).strip()
            if payload.get("missing_policy_line")
            else None
        ),
        mechanism_line=(
            str(payload["mechanism_line"]).strip()
            if payload.get("mechanism_line")
            else None
        ),
    )


def load_card_evidence_artefact(subsystem_id: str) -> CardEvidenceArtefact:
    path = compiled_cards_dir() / f"{subsystem_id}.yaml"
    if not path.is_file():
        raise CardEvidenceValidationError(f"missing compiled card evidence artefact: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    validate_card_evidence_payload(payload, path=str(path))
    artefact = parse_card_evidence_payload(payload)
    if artefact.subsystem_id != subsystem_id:
        raise CardEvidenceValidationError(
            f"{path}: subsystem_id {artefact.subsystem_id!r} does not match filename {subsystem_id!r}"
        )
    return artefact


@lru_cache(maxsize=8)
def _cached_artefact(subsystem_id: str) -> CardEvidenceArtefact:
    return load_card_evidence_artefact(subsystem_id)


def get_card_evidence_artefact(subsystem_id: str) -> CardEvidenceArtefact:
    if subsystem_id not in PILOT_COMPILED_SUBSYSTEM_IDS:
        raise CardEvidenceValidationError(f"no compiled card evidence registered for {subsystem_id!r}")
    return _cached_artefact(subsystem_id)


def _partition_markers(
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


@lru_cache(maxsize=1)
def _marker_display_label_map() -> Dict[str, str]:
    resolver = CanonicalResolver()
    out: Dict[str, str] = {}
    for canonical_id, definition in resolver.load_biomarkers().items():
        preferred = (definition.consumer_display_name or "").strip()
        out[canonical_id] = preferred if preferred else canonical_id
    return out


def _labels_for_marker_ids(marker_ids: Sequence[str]) -> List[MarkerDisplayLabelV1]:
    labels = _marker_display_label_map()
    rows: List[MarkerDisplayLabelV1] = []
    for marker_id in marker_ids:
        display_label = labels.get(marker_id, marker_id)
        rows.append(MarkerDisplayLabelV1(id=marker_id, display_label=display_label))
    return rows


def assemble_subsystem_from_compiled_card_evidence(
    *,
    subsystem_id: str,
    panel_biomarker_ids: Set[str],
    scored_on_rail: Set[str],
) -> Optional[SubsystemEvidenceV1]:
    """
    Build SubsystemEvidenceV1 from compiled artefact for registered pilot subsystems.
    Returns None when visibility_tier is hidden_v1 (suppressed from DTO emission).
    """
    artefact = get_card_evidence_artefact(subsystem_id)
    if artefact.visibility_tier == "hidden_v1":
        return None

    expected_ids = [m.marker_id for m in artefact.markers]
    included, missing = _partition_markers(
        expected=expected_ids,
        panel_biomarker_ids=panel_biomarker_ids,
        scored_on_rail=scored_on_rail,
    )

    marker_evidence: List[SubsystemMarkerEvidenceV1] = []
    by_id = {m.marker_id: m for m in artefact.markers}
    for marker_id in expected_ids:
        spec = by_id[marker_id]
        marker_evidence.append(
            SubsystemMarkerEvidenceV1(
                marker_id=marker_id,
                display_label=spec.display_label,
                marker_role=spec.marker_role,
                relationship_kind=spec.relationship_kind,
                presence_policy=spec.presence_policy,
                rationale_short=spec.rationale_short,
            )
        )

    source_trace = (
        f"health_system_card_evidence_v1:{artefact.artefact_id}:"
        f"{artefact.compile_manifest_ref}"
    )

    return SubsystemEvidenceV1(
        subsystem_id=artefact.subsystem_id,
        subsystem_label=artefact.subsystem_label,
        included_marker_ids=included,
        missing_marker_ids=missing,
        included_markers=_labels_for_marker_ids(included),
        missing_markers=_labels_for_marker_ids(missing),
        status_label=None,
        evidence_role=None,
        source_trace=source_trace,
        card_evidence_schema_version=artefact.schema_version,
        visibility_tier=artefact.visibility_tier,
        source_spec_ids=list(artefact.source_spec_ids),
        compile_manifest_ref=artefact.compile_manifest_ref,
        mechanism_line=artefact.mechanism_line,
        missing_policy_line=artefact.missing_policy_line,
        marker_evidence=marker_evidence,
    )
