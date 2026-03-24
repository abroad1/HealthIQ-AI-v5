#!/usr/bin/env python3
"""
Validate user intervention / exposure record-set documents (KB-S48d).

Deterministic structural checks only. Canonical class IDs align with KB-S48a.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from scripts.validate_intervention_effects_registry import APPROVED_CLASS_IDS, FORBIDDEN_KEY_FRAGMENTS

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "user_intervention_exposure_schema_v1.yaml"
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "user_intervention_exposure_audit.md"

SCHEMA_VERSION = "1.0.0"

_INTERVENTION_TYPES = frozenset({"medication", "non_medication", "other"})
_LINK_STATUS = frozenset({"mapped", "unmapped"})
_CHANGE_EVENTS = frozenset({"started", "stopped", "changed"})
_SOURCE_TYPES = frozenset({"user_reported", "clinician_prescribed", "inferred"})
_CONFIDENCE = frozenset({"low", "moderate", "high"})

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_EXPOSURE_FIELDS = frozenset(
    {"dose_description", "frequency_description", "route_description", "intensity_description"}
)


def _collect_key_paths(obj: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                paths.append(f"{prefix}<non-string-key>")
                continue
            p = f"{prefix}.{k}" if prefix else k
            paths.append(p)
            paths.extend(_collect_key_paths(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            paths.extend(_collect_key_paths(v, f"{prefix}[{i}]"))
    return paths


def _forbidden_key_errors(obj: dict[str, Any], errors: list[str]) -> None:
    for path in _collect_key_paths(obj):
        seg = path.split(".")[-1].split("[")[0]
        low = seg.lower()
        for frag in FORBIDDEN_KEY_FRAGMENTS:
            if frag in low:
                errors.append(
                    f"Forbidden key fragment '{frag}' in key '{seg}' (path: {path})"
                )


def _parse_iso_date(s: str, field_label: str, errors: list[str]) -> None:
    if not isinstance(s, str) or not _DATE_RE.match(s):
        errors.append(f"{field_label} must be YYYY-MM-DD")
        return
    try:
        datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        errors.append(f"{field_label} is not a valid calendar date")


def _validate_exposure_detail(ed: Any, lab: str, errors: list[str]) -> None:
    if ed is None:
        return
    if not isinstance(ed, dict):
        errors.append(f"{lab} must be a map or null")
        return
    for k, v in ed.items():
        if k not in _EXPOSURE_FIELDS:
            errors.append(f"{lab} unknown key '{k}'")
        elif v is not None and not isinstance(v, str):
            errors.append(f"{lab}.{k} must be a string or null")


def _validate_record(row: dict[str, Any], lab: str, errors: list[str]) -> None:
    _forbidden_key_errors(row, errors)

    for req in (
        "intervention_record_id",
        "intervention_type",
        "entered_label",
        "canonical_class",
        "timeline",
        "provenance",
    ):
        if req not in row:
            errors.append(f"{lab}.{req} is required")

    rid = row.get("intervention_record_id")
    if not isinstance(rid, str) or not rid.strip():
        errors.append(f"{lab}.intervention_record_id must be a non-empty string")

    it = row.get("intervention_type")
    if it not in _INTERVENTION_TYPES:
        errors.append(f"{lab}.intervention_type must be one of {sorted(_INTERVENTION_TYPES)}")

    el = row.get("entered_label")
    if not isinstance(el, str) or not el.strip():
        errors.append(f"{lab}.entered_label must be a non-empty string")

    cc = row.get("canonical_class")
    if not isinstance(cc, dict):
        errors.append(f"{lab}.canonical_class must be a map")
    else:
        _forbidden_key_errors(cc, errors)
        if "link_status" not in cc:
            errors.append(f"{lab}.canonical_class.link_status is required")
        ls = cc.get("link_status")
        if ls not in _LINK_STATUS:
            errors.append(f"{lab}.canonical_class.link_status must be one of {sorted(_LINK_STATUS)}")
        elif ls == "mapped":
            if "intervention_class_id" not in cc:
                errors.append(f"{lab}.canonical_class.intervention_class_id is required when mapped")
            cid = cc.get("intervention_class_id")
            if not isinstance(cid, str) or cid not in APPROVED_CLASS_IDS:
                errors.append(
                    f"{lab}.canonical_class.intervention_class_id must be one of "
                    f"{sorted(APPROVED_CLASS_IDS)} when link_status is mapped"
                )
            extra = frozenset(cc.keys()) - frozenset({"link_status", "intervention_class_id"})
            if extra:
                errors.append(f"{lab}.canonical_class must not contain keys {sorted(extra)}")
        else:
            if "intervention_class_id" not in cc:
                errors.append(
                    f"{lab}.canonical_class.intervention_class_id is required (null) when unmapped"
                )
            elif cc.get("intervention_class_id") is not None:
                errors.append(
                    f"{lab}.canonical_class.intervention_class_id must be null when link_status is unmapped"
                )
            extra = frozenset(cc.keys()) - frozenset({"link_status", "intervention_class_id"})
            if extra:
                errors.append(f"{lab}.canonical_class must not contain keys {sorted(extra)}")

    tl = row.get("timeline")
    if not isinstance(tl, dict):
        errors.append(f"{lab}.timeline must be a map")
    else:
        _forbidden_key_errors(tl, errors)
        for req in ("effective_from_date", "effective_to_date", "is_ongoing", "change_event_type"):
            if req not in tl:
                errors.append(f"{lab}.timeline.{req} is required")
        _parse_iso_date(tl.get("effective_from_date"), f"{lab}.timeline.effective_from_date", errors)
        eto = tl.get("effective_to_date")
        if eto is not None:
            if not isinstance(eto, str):
                errors.append(f"{lab}.timeline.effective_to_date must be a string date or null")
            else:
                _parse_iso_date(eto, f"{lab}.timeline.effective_to_date", errors)
        io = tl.get("is_ongoing")
        if not isinstance(io, bool):
            errors.append(f"{lab}.timeline.is_ongoing must be a boolean")
        elif io is True and eto is not None:
            errors.append(f"{lab}.timeline.effective_to_date must be null when is_ongoing is true")
        cet = tl.get("change_event_type")
        if cet not in _CHANGE_EVENTS:
            errors.append(f"{lab}.timeline.change_event_type must be one of {sorted(_CHANGE_EVENTS)}")

    prov = row.get("provenance")
    if not isinstance(prov, dict):
        errors.append(f"{lab}.provenance must be a map")
    else:
        _forbidden_key_errors(prov, errors)
        if "source_type" not in prov:
            errors.append(f"{lab}.provenance.source_type is required")
        if "confidence" not in prov:
            errors.append(f"{lab}.provenance.confidence is required")
        st = prov.get("source_type")
        if st not in _SOURCE_TYPES:
            errors.append(f"{lab}.provenance.source_type must be one of {sorted(_SOURCE_TYPES)}")
        conf = prov.get("confidence")
        if conf not in _CONFIDENCE:
            errors.append(f"{lab}.provenance.confidence must be one of {sorted(_CONFIDENCE)}")
        if "notes" in prov:
            n = prov["notes"]
            if n is not None and not isinstance(n, str):
                errors.append(f"{lab}.provenance.notes must be a string or null")
        extra = frozenset(prov.keys()) - frozenset({"source_type", "confidence", "notes"})
        if extra:
            errors.append(f"{lab}.provenance unknown keys {sorted(extra)}")

    allowed_top = frozenset(
        {
            "intervention_record_id",
            "intervention_type",
            "entered_label",
            "canonical_class",
            "timeline",
            "provenance",
            "exposure_detail",
        }
    )
    extra_top = frozenset(row.keys()) - allowed_top
    if extra_top:
        errors.append(f"{lab} unknown top-level keys {sorted(extra_top)}")

    _validate_exposure_detail(row.get("exposure_detail"), f"{lab}.exposure_detail", errors)


def validate_user_intervention_exposure_document(doc: dict[str, Any], errors: list[str]) -> None:
    if not isinstance(doc, dict):
        errors.append("Root must be a map")
        return

    _forbidden_key_errors(doc, errors)

    if doc.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be '{SCHEMA_VERSION}'")

    records = doc.get("intervention_records")
    if not isinstance(records, list):
        errors.append("intervention_records must be a list")
        return

    seen_ids: set[str] = set()
    for i, rec in enumerate(records):
        lab = f"intervention_records[{i}]"
        if not isinstance(rec, dict):
            errors.append(f"{lab} must be a map")
            continue
        _validate_record(rec, lab, errors)
        rid = rec.get("intervention_record_id")
        if isinstance(rid, str) and rid.strip():
            if rid.strip() in seen_ids:
                errors.append(f"duplicate intervention_record_id: {rid.strip()}")
            seen_ids.add(rid.strip())


def _load_yaml(path: Path) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f), errors
    except OSError as exc:
        return None, [f"Could not read {path}: {exc}"]
    except yaml.YAMLError as exc:
        return None, [f"Invalid YAML in {path}: {exc}"]


def _write_audit(path: Path, status: str, errors: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# User Intervention / Exposure Audit",
        "",
        f"validation_status: {status}",
        "",
        "errors:",
    ]
    if errors:
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("- None")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate user intervention / exposure YAML document.")
    p.add_argument("--document", required=True, type=Path, help="Path to record-set YAML")
    p.add_argument("--audit-path", type=Path, default=DEFAULT_AUDIT_PATH)
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    doc_path = args.document.resolve()
    audit_path = args.audit_path.resolve()

    errors: list[str] = []
    doc, e0 = _load_yaml(doc_path)
    errors.extend(e0)

    if not errors and isinstance(doc, dict):
        validate_user_intervention_exposure_document(doc, errors)

    status = "FAIL" if errors else "PASS"
    _write_audit(audit_path, status, errors)

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {audit_path}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
