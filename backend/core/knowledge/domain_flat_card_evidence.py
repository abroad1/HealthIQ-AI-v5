"""
KB-UTIL-1 — Compiled domain-flat card evidence loader (Wave 1 liver flat model).

Loads governed YAML from knowledge_bus/compiled/health_system_cards/.
No runtime Pass 3 JSON or package file reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, List, Mapping, Optional, Set, Tuple

import yaml

from core.knowledge.health_system_card_evidence import (
    CardEvidenceMarkerDef,
    CardEvidenceValidationError,
    _FORBIDDEN_MARKER_IDS,
    _MARKER_ROLES,
    _PRESENCE_POLICIES,
    _RELATIONSHIP_KINDS,
    _labels_for_marker_ids,
    _partition_markers,
    _require_enum,
    _require_str,
    compiled_cards_dir,
)
from core.models.results import DomainFlatEvidenceV1, SubsystemMarkerEvidenceV1

WAVE1_DOMAIN_FLAT_DOMAIN_IDS: frozenset[str] = frozenset({"wave1_liver"})


@dataclass(frozen=True)
class DomainFlatEvidenceArtefact:
    schema_version: str
    artefact_id: str
    domain_id: str
    domain_label: str
    compile_manifest_ref: str
    markers: Tuple[CardEvidenceMarkerDef, ...]
    provenance: Mapping[str, Any]
    domain_summary_line: Optional[str] = None
    mechanism_line: Optional[str] = None
    missing_policy_line: Optional[str] = None
    evidence_limitations_line: Optional[str] = None
    source_spec_ids: Tuple[str, ...] = ()


def validate_domain_flat_payload(payload: Mapping[str, Any], *, path: str = "<memory>") -> None:
    errors: List[str] = []
    if not isinstance(payload, dict):
        raise CardEvidenceValidationError(f"{path}: root must be a mapping")

    schema_version = _require_str(payload, "schema_version", errors)
    if schema_version and schema_version != "1.0.0":
        errors.append("schema_version must be 1.0.0")

    kind = _require_str(payload, "artefact_kind", errors)
    if kind and kind != "domain_flat_card_evidence_v1":
        errors.append("artefact_kind must be domain_flat_card_evidence_v1")

    for key in ("artefact_id", "domain_id", "domain_label", "compile_manifest_ref"):
        _require_str(payload, key, errors)

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
                    errors.append(f"markers[{idx}].marker_id forbidden: {marker_id}")
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

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be a mapping")
    else:
        pkind = _require_str(provenance, "artefact_kind", errors)
        if pkind and pkind != "domain_flat_card_evidence_v1":
            errors.append("provenance.artefact_kind must be domain_flat_card_evidence_v1")
        status = _require_str(provenance, "compile_status", errors)
        if status and status not in (
            "pilot_manual",
            "compile_pipeline",
            "kb_util1_package_enrichment",
        ):
            errors.append("provenance.compile_status invalid")

    for opt in (
        "domain_summary_line",
        "mechanism_line",
        "missing_policy_line",
        "evidence_limitations_line",
    ):
        val = payload.get(opt)
        if val is not None and (not isinstance(val, str) or not val.strip()):
            errors.append(f"{opt} must be a non-empty string when present")

    if errors:
        raise CardEvidenceValidationError(f"{path}: {'; '.join(errors)}")


def parse_domain_flat_payload(payload: Mapping[str, Any]) -> DomainFlatEvidenceArtefact:
    validate_domain_flat_payload(payload)
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
    source_spec_ids = payload.get("source_spec_ids") or []
    if not isinstance(source_spec_ids, list):
        source_spec_ids = []
    return DomainFlatEvidenceArtefact(
        schema_version=str(payload["schema_version"]).strip(),
        artefact_id=str(payload["artefact_id"]).strip(),
        domain_id=str(payload["domain_id"]).strip(),
        domain_label=str(payload["domain_label"]).strip(),
        compile_manifest_ref=str(payload["compile_manifest_ref"]).strip(),
        markers=tuple(markers),
        provenance=payload.get("provenance") or {},
        domain_summary_line=(
            str(payload["domain_summary_line"]).strip()
            if payload.get("domain_summary_line")
            else None
        ),
        mechanism_line=(
            str(payload["mechanism_line"]).strip()
            if payload.get("mechanism_line")
            else None
        ),
        missing_policy_line=(
            str(payload["missing_policy_line"]).strip()
            if payload.get("missing_policy_line")
            else None
        ),
        evidence_limitations_line=(
            str(payload["evidence_limitations_line"]).strip()
            if payload.get("evidence_limitations_line")
            else None
        ),
        source_spec_ids=tuple(str(x).strip() for x in source_spec_ids if str(x).strip()),
    )


def load_domain_flat_evidence_artefact(domain_id: str) -> DomainFlatEvidenceArtefact:
    if domain_id not in WAVE1_DOMAIN_FLAT_DOMAIN_IDS:
        raise CardEvidenceValidationError(f"no domain-flat artefact registered for {domain_id!r}")
    path = compiled_cards_dir() / "wave1_liver_flat_v1.yaml"
    if not path.is_file():
        raise CardEvidenceValidationError(f"missing domain-flat artefact: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    validate_domain_flat_payload(payload, path=str(path))
    artefact = parse_domain_flat_payload(payload)
    if artefact.domain_id != domain_id:
        raise CardEvidenceValidationError(
            f"{path}: domain_id mismatch expected {domain_id}, got {artefact.domain_id}"
        )
    return artefact


@lru_cache(maxsize=4)
def _cached_domain_flat(domain_id: str) -> DomainFlatEvidenceArtefact:
    return load_domain_flat_evidence_artefact(domain_id)


def assemble_domain_flat_evidence(
    *,
    domain_id: str,
    panel_biomarker_ids: Set[str],
    scored_on_rail: Set[str],
) -> Optional[DomainFlatEvidenceV1]:
    artefact = _cached_domain_flat(domain_id)
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
    return DomainFlatEvidenceV1(
        domain_id=artefact.domain_id,
        domain_label=artefact.domain_label,
        domain_summary_line=artefact.domain_summary_line,
        mechanism_line=artefact.mechanism_line,
        missing_policy_line=artefact.missing_policy_line,
        evidence_limitations_line=artefact.evidence_limitations_line,
        included_marker_ids=included,
        missing_marker_ids=missing,
        included_markers=_labels_for_marker_ids(included),
        missing_markers=_labels_for_marker_ids(missing),
        marker_evidence=marker_evidence,
    )
