"""
ARCH-RT-4 — Compiled hypothesis artefact validator and loader.

Fail-closed. Semver schema 1.0.0 only — never use legacy load_root_cause_hypotheses v1 loader.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import yaml

SCHEMA_VERSION = "1.0.0"
PILOT_SIGNAL_ID = "signal_vitamin_d_low"

_SOURCE_PROVENANCE = frozenset(
    {"explicit", "source_document_derived", "package_id_inferred", "manual_pilot"}
)
_EVIDENCE_STRENGTH = frozenset({"strong", "moderate", "weak", "contextual"})


@dataclass(frozen=True)
class CompiledHypothesisRow:
    hypothesis_id: str
    rank: int
    title: str
    physiological_claim: str
    evidence_strength: str
    missing_data_policy: str
    evidence_for: Tuple[str, ...]
    evidence_against: Tuple[str, ...]
    contradiction_markers: Tuple[str, ...]
    caveats: Tuple[str, ...]
    confirmatory_tests: Tuple[str, ...]
    summary_template: Optional[str] = None
    legacy_hypothesis_id: Optional[str] = None


@dataclass(frozen=True)
class CompiledHypothesisArtefact:
    schema_version: str
    artefact_id: str
    hypothesis_set_id: str
    signal_id: str
    activation_key: str
    source_spec_ids: Tuple[str, ...]
    source_spec_provenance: str
    compile_manifest_ref: str
    hypotheses: Tuple[CompiledHypothesisRow, ...]
    provenance: Mapping[str, Any]
    source_document: Optional[str] = None


class CompiledHypothesisValidationError(ValueError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def compiled_hypotheses_dir() -> Path:
    return _repo_root() / "knowledge_bus" / "compiled" / "hypotheses"


def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def validate_compiled_hypothesis_payload(payload: Mapping[str, Any], *, path: str = "<memory>") -> None:
    if not isinstance(payload, dict):
        raise CompiledHypothesisValidationError(f"{path}: root must be a mapping")

    errors: List[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        _err(errors, f"schema_version must be {SCHEMA_VERSION}")

    for key in (
        "artefact_id",
        "hypothesis_set_id",
        "signal_id",
        "activation_key",
        "compile_manifest_ref",
    ):
        val = payload.get(key)
        if not isinstance(val, str) or not val.strip():
            _err(errors, f"missing or invalid {key}")

    prov = payload.get("source_spec_provenance")
    if prov not in _SOURCE_PROVENANCE:
        _err(errors, f"invalid source_spec_provenance: {prov!r}")

    spec_ids = payload.get("source_spec_ids")
    if not isinstance(spec_ids, list) or not spec_ids:
        _err(errors, "source_spec_ids must be a non-empty list")
    elif not all(isinstance(x, str) and x.strip() for x in spec_ids):
        _err(errors, "source_spec_ids items must be non-empty strings")

    doc = payload.get("source_document")
    if doc is not None and (not isinstance(doc, str) or not doc.strip()):
        _err(errors, "source_document must be non-empty string when present")

    rows = payload.get("hypotheses")
    if not isinstance(rows, list) or not rows:
        _err(errors, "hypotheses must be a non-empty list")
    else:
        seen: Set[str] = set()
        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                _err(errors, f"hypotheses[{idx}] must be a mapping")
                continue
            hid = row.get("hypothesis_id")
            if not isinstance(hid, str) or not hid.strip():
                _err(errors, f"hypotheses[{idx}].hypothesis_id required")
            elif hid in seen:
                _err(errors, f"duplicate hypothesis_id: {hid}")
            else:
                seen.add(hid)
            rank = row.get("rank")
            if not isinstance(rank, int) or rank < 1:
                _err(errors, f"hypotheses[{idx}].rank must be int >= 1")
            for req in ("title", "physiological_claim", "missing_data_policy"):
                v = row.get(req)
                if not isinstance(v, str) or not str(v).strip():
                    _err(errors, f"hypotheses[{idx}].{req} required")
            summary = row.get("summary_template")
            if summary is not None and (not isinstance(summary, str) or not summary.strip()):
                _err(errors, f"hypotheses[{idx}].summary_template must be non-empty when present")
            strength = row.get("evidence_strength")
            if strength not in _EVIDENCE_STRENGTH:
                _err(errors, f"hypotheses[{idx}].evidence_strength invalid")
            for list_key in (
                "evidence_for",
                "evidence_against",
                "contradiction_markers",
                "caveats",
                "confirmatory_tests",
            ):
                lst = row.get(list_key, [])
                if lst is None:
                    continue
                if not isinstance(lst, list) or not all(isinstance(x, str) for x in lst):
                    _err(errors, f"hypotheses[{idx}].{list_key} must be a list of strings")

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        _err(errors, "provenance must be a mapping")
    else:
        if provenance.get("artefact_kind") != "compiled_hypothesis_v1":
            _err(errors, "provenance.artefact_kind must be compiled_hypothesis_v1")
        if provenance.get("compile_status") not in ("pilot_manual", "compile_pipeline"):
            _err(errors, "provenance.compile_status invalid")

    if errors:
        raise CompiledHypothesisValidationError(f"{path}: {'; '.join(errors)}")


def parse_compiled_hypothesis_payload(payload: Mapping[str, Any]) -> CompiledHypothesisArtefact:
    validate_compiled_hypothesis_payload(payload)
    hypotheses: List[CompiledHypothesisRow] = []
    for row in payload["hypotheses"]:
        hypotheses.append(
            CompiledHypothesisRow(
                hypothesis_id=str(row["hypothesis_id"]).strip(),
                rank=int(row["rank"]),
                title=str(row["title"]).strip(),
                physiological_claim=str(row["physiological_claim"]).strip(),
                evidence_strength=str(row["evidence_strength"]).strip(),
                missing_data_policy=str(row["missing_data_policy"]).strip(),
                summary_template=(
                    str(row["summary_template"]).strip() if row.get("summary_template") else None
                ),
                evidence_for=tuple(str(x).strip() for x in (row.get("evidence_for") or [])),
                evidence_against=tuple(str(x).strip() for x in (row.get("evidence_against") or [])),
                contradiction_markers=tuple(
                    str(x).strip() for x in (row.get("contradiction_markers") or [])
                ),
                caveats=tuple(str(x).strip() for x in (row.get("caveats") or [])),
                confirmatory_tests=tuple(
                    str(x).strip() for x in (row.get("confirmatory_tests") or [])
                ),
                legacy_hypothesis_id=(
                    str(row["legacy_hypothesis_id"]).strip()
                    if row.get("legacy_hypothesis_id")
                    else None
                ),
            )
        )
    prov = payload.get("provenance") or {}
    return CompiledHypothesisArtefact(
        schema_version=SCHEMA_VERSION,
        artefact_id=str(payload["artefact_id"]).strip(),
        hypothesis_set_id=str(payload["hypothesis_set_id"]).strip(),
        signal_id=str(payload["signal_id"]).strip(),
        activation_key=str(payload["activation_key"]).strip(),
        source_spec_ids=tuple(str(x).strip() for x in payload["source_spec_ids"]),
        source_spec_provenance=str(payload["source_spec_provenance"]).strip(),
        compile_manifest_ref=str(payload["compile_manifest_ref"]).strip(),
        hypotheses=tuple(hypotheses),
        provenance=prov,
        source_document=(
            str(payload["source_document"]).strip() if payload.get("source_document") else None
        ),
    )


def load_compiled_hypothesis_artefact(signal_id: str) -> CompiledHypothesisArtefact:
    path = compiled_hypotheses_dir() / f"{signal_id}.yaml"
    if not path.is_file():
        raise CompiledHypothesisValidationError(f"missing compiled hypothesis artefact: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    validate_compiled_hypothesis_payload(payload, path=str(path))
    artefact = parse_compiled_hypothesis_payload(payload)
    if artefact.signal_id != signal_id:
        raise CompiledHypothesisValidationError(
            f"{path}: signal_id {artefact.signal_id!r} != filename {signal_id!r}"
        )
    return artefact


@lru_cache(maxsize=4)
def _cached_artefact(signal_id: str) -> CompiledHypothesisArtefact:
    return load_compiled_hypothesis_artefact(signal_id)


def get_compiled_hypothesis_artefact(signal_id: str) -> CompiledHypothesisArtefact:
    return _cached_artefact(signal_id)


def validate_confirmatory_test_refs(artefact: CompiledHypothesisArtefact) -> None:
    """Fail-closed when compiled artefact references unknown confirmatory test ids."""
    from core.knowledge.load_confirmatory_tests_registry import load_confirmatory_tests_registry_v1

    registry = load_confirmatory_tests_registry_v1()
    known = set(registry["tests_by_id"].keys())
    for row in artefact.hypotheses:
        missing = [tid for tid in row.confirmatory_tests if tid not in known]
        if missing:
            raise CompiledHypothesisValidationError(
                f"unknown confirmatory_tests for {row.hypothesis_id}: {', '.join(missing)}"
            )


def runtime_summary_for_hypothesis(row: CompiledHypothesisRow) -> str:
    """
    ARCH-RT-5 presentation mapping: summary_template is runtime wording;
    physiological_claim is governed clinical reasoning (not direct retail text).
    """
    if row.summary_template and row.summary_template.strip():
        return row.summary_template.strip()[:200]
    return row.physiological_claim.strip()[:200]


def artefact_as_shadow_dict(artefact: CompiledHypothesisArtefact) -> Dict[str, Any]:
    """Shadow payload shape for registry comparison (not legacy v1 YAML schema)."""
    return {
        "schema_version": artefact.schema_version,
        "artefact_id": artefact.artefact_id,
        "signal_id": artefact.signal_id,
        "activation_key": artefact.activation_key,
        "source_spec_ids": list(artefact.source_spec_ids),
        "source_spec_provenance": artefact.source_spec_provenance,
        "compile_manifest_ref": artefact.compile_manifest_ref,
        "hypotheses": [
            {
                "hypothesis_id": h.hypothesis_id,
                "title": h.title,
                "physiological_claim": h.physiological_claim,
                "summary_template": h.summary_template,
                "runtime_summary": runtime_summary_for_hypothesis(h),
                "evidence_strength": h.evidence_strength,
                "evidence_for": list(h.evidence_for),
                "evidence_against": list(h.evidence_against),
                "missing_data_policy": h.missing_data_policy,
                "confirmatory_tests": list(h.confirmatory_tests),
            }
            for h in artefact.hypotheses
        ],
        "path": str(compiled_hypotheses_dir() / f"{artefact.signal_id}.yaml"),
    }
