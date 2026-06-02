#!/usr/bin/env python3
"""
Validate context_modifier_catalogue_draft_v1.yaml (CONTEXT-MOD-1).

Standalone governance validator — does not import Intelligence Core or runtime loaders.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOGUE = (
    ROOT / "knowledge_bus" / "governance" / "context_modifier_catalogue_draft_v1.yaml"
)
DEFAULT_SCHEMA = ROOT / "knowledge_bus" / "schema" / "context_modifier_catalogue_schema_v1.yaml"
DEFAULT_FRAME_INDEX = (
    ROOT / "knowledge_bus" / "governance" / "medical_frame_identity_index_v1.yaml"
)

MODIFIER_TYPES = frozenset(
    {
        "questionnaire_lifestyle",
        "questionnaire_symptom",
        "questionnaire_known_condition",
        "questionnaire_family_history",
        "supplement",
        "medication_category",
        "drug_category",
        "demographic",
    }
)
MODIFIER_EFFECTS = frozenset(
    {
        "strengthens_frame",
        "weakens_frame",
        "explains_possible_cause",
        "increases_confidence",
        "decreases_confidence",
        "adds_safety_escalation_context",
        "adds_differential_context",
        "suppresses_overclaiming",
        "requires_missing_data_caveat",
        "no_interpretive_effect",
    }
)
ALLOWED_LAYERS = frozenset(
    {
        "Layer_A_input_normalisation",
        "Layer_B_frame_assembly",
        "Layer_B_narrative_brief",
        "Presentation_safety_only",
        "Not_allowed_for_medical_inference",
    }
)


def _load_yaml(path: Path) -> tuple[Any, list[str]]:
    if not path.is_file():
        return None, [f"file not found: {path}"]
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except yaml.YAMLError as exc:
        return None, [f"invalid YAML in {path}: {exc}"]
    except OSError as exc:
        return None, [f"could not read {path}: {exc}"]


def _require_str(data: dict[str, Any], key: str, errors: list[str], *, prefix: str) -> str | None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}: missing or invalid required field: {key}")
        return None
    return value.strip()


def _load_frame_ids(index_path: Path) -> tuple[set[str], list[str]]:
    doc, errs = _load_yaml(index_path)
    if not isinstance(doc, dict):
        return set(), errs
    frame_ids: set[str] = set()
    for fam in doc.get("signal_families") or []:
        if not isinstance(fam, dict):
            continue
        for frame in fam.get("frames") or []:
            if isinstance(frame, dict) and isinstance(frame.get("medical_frame_id"), str):
                frame_ids.add(frame["medical_frame_id"])
    return frame_ids, errs


def _normalised_frame_ids(value: Any) -> list[str] | None:
    """Return non-empty frame id list, or None when unset / empty (where-specified guard)."""
    if value is None:
        return None
    if isinstance(value, list):
        ids = [item for item in value if isinstance(item, str) and item.strip()]
        return ids if ids else None
    return None


def validate_context_modifier_catalogue(
    catalogue_path: Path,
    *,
    schema_path: Path | None = None,
    frame_index_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    schema_path = schema_path or DEFAULT_SCHEMA
    frame_index_path = frame_index_path or DEFAULT_FRAME_INDEX

    schema_doc, schema_errs = _load_yaml(schema_path)
    errors.extend(schema_errs)
    if schema_doc is None:
        return errors

    doc, load_errs = _load_yaml(catalogue_path)
    errors.extend(load_errs)
    if not isinstance(doc, dict):
        return errors

    if doc.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if doc.get("runtime_consumed") is not False:
        errors.append("runtime_consumed must be false")
    if doc.get("status") != "draft_governance_non_runtime":
        errors.append("status must be draft_governance_non_runtime")

    for key in ("catalogue_id", "work_id", "generated_utc"):
        if not isinstance(doc.get(key), str) or not str(doc.get(key)).strip():
            errors.append(f"missing or invalid required top-level field: {key}")

    modifiers = doc.get("modifiers")
    if not isinstance(modifiers, list) or not modifiers:
        errors.append("modifiers must be a non-empty list")
        return errors

    frame_ids, index_errs = _load_frame_ids(frame_index_path)
    errors.extend(index_errs)

    modifier_required = list((schema_doc.get("modifier_required_fields") or []))
    seen_ids: set[str] = set()

    for entry in modifiers:
        if not isinstance(entry, dict):
            errors.append("modifier entry must be a map")
            continue
        mid = _require_str(entry, "modifier_id", errors, prefix="modifier") or "<unknown>"
        if mid in seen_ids:
            errors.append(f"duplicate modifier_id: {mid}")
        seen_ids.add(mid)

        for key in modifier_required:
            if key == "applies_to":
                applies = entry.get("applies_to")
                if not isinstance(applies, dict):
                    errors.append(f"{mid}: applies_to must be a map")
                else:
                    for sub in ("signal_family_ids", "medical_frame_ids", "biomarker_ids"):
                        if sub not in applies:
                            errors.append(f"{mid}: applies_to missing {sub}")
            elif key == "runtime_active":
                if entry.get("runtime_active") is not False:
                    errors.append(f"{mid}: runtime_active must be false")
            elif key == "requires_medical_review":
                if not isinstance(entry.get(key), bool):
                    errors.append(f"{mid}: requires_medical_review must be boolean")
            else:
                _require_str(entry, key, errors, prefix=mid)

        mtype = entry.get("modifier_type")
        if mtype not in MODIFIER_TYPES:
            errors.append(f"{mid}: unknown modifier_type {mtype!r}")

        effect = entry.get("modifier_effect")
        if effect not in MODIFIER_EFFECTS:
            errors.append(f"{mid}: unknown modifier_effect {effect!r}")

        layer = entry.get("allowed_layer")
        if layer not in ALLOWED_LAYERS:
            errors.append(f"{mid}: unknown allowed_layer {layer!r}")

        applies = entry.get("applies_to")
        if isinstance(applies, dict):
            specified_frames = _normalised_frame_ids(applies.get("medical_frame_ids"))
            if specified_frames:
                for fid in specified_frames:
                    if fid not in frame_ids:
                        errors.append(
                            f"{mid}: medical_frame_id not in identity index: {fid}"
                        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate context modifier catalogue.")
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=DEFAULT_CATALOGUE,
        help="Path to context_modifier_catalogue_draft_v1.yaml",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Path to schema file",
    )
    parser.add_argument(
        "--frame-index",
        type=Path,
        default=DEFAULT_FRAME_INDEX,
        help="Path to medical_frame_identity_index_v1.yaml",
    )
    args = parser.parse_args(argv)
    errors = validate_context_modifier_catalogue(
        args.catalogue,
        schema_path=args.schema,
        frame_index_path=args.frame_index,
    )
    if errors:
        print("validation_status: FAIL", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    print("validation_status: PASS")
    print("errors: 0")
    print(f"catalogue_path: {args.catalogue.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
