#!/usr/bin/env python3
"""
Validate medical_frame_identity_index_v1.yaml (MED-FRAME-2).

Governed non-runtime index — does not import SignalRegistry or SignalEvaluator.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX = ROOT / "knowledge_bus" / "governance" / "medical_frame_identity_index_v1.yaml"
DEFAULT_SCHEMA = ROOT / "knowledge_bus" / "schema" / "medical_frame_identity_index_schema_v1.yaml"

ACTIVATION_KEY_RE = re.compile(r"^signal_[a-z0-9_]+::[a-z][a-z0-9_]*$")

PROMOTION_STATES = frozenset(
    {
        "runtime_active_canonical",
        "runtime_active_legacy_unadjudicated",
        "compiled_not_promoted",
        "superseded",
        "retired",
        "deferred",
    }
)
CLINICAL_ADJUDICATION = frozenset(
    {
        "not_required",
        "required_before_activation",
        "accepted_with_rationale",
        "blocked_pending_medical_review",
    }
)
COLLISION_STATUS = frozenset(
    {
        "none",
        "real_collision_active_blocker",
        "allowed_non_runtime_collision",
        "resolved_by_supersession",
        "requires_adjudication",
    }
)
RUNTIME_AUTHORITY = frozenset({"active", "inactive", "none"})
NON_RUNTIME_PROMOTION = frozenset(
    {"compiled_not_promoted", "superseded", "retired", "deferred"}
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


def _require_str(data: dict[str, Any], key: str, errors: list[str]) -> str | None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"missing or invalid required field: {key}")
        return None
    return value.strip()


def _validate_context_inputs(value: Any, frame_id: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{frame_id}: context_inputs_supported must be a map")
        return
    for key in ("biomarker_evidence", "questionnaire_modifiers", "medication_modifiers"):
        if key not in value:
            errors.append(f"{frame_id}: context_inputs_supported missing {key}")
        elif not isinstance(value[key], bool):
            errors.append(f"{frame_id}: context_inputs_supported.{key} must be boolean")


def _validate_frame(frame: Any, errors: list[str], *, frame_required: list[str]) -> dict[str, Any] | None:
    if not isinstance(frame, dict):
        errors.append("frame entry must be a map")
        return None
    frame_id = _require_str(frame, "medical_frame_id", errors) or "<unknown>"
    for key in frame_required:
        if key == "context_inputs_supported":
            _validate_context_inputs(frame.get("context_inputs_supported"), frame_id, errors)
        elif key in ("supersedes", "superseded_by"):
            continue
        else:
            _require_str(frame, key, errors)

    promotion = frame.get("promotion_state")
    if promotion not in PROMOTION_STATES:
        errors.append(f"{frame_id}: unknown promotion_state {promotion!r}")

    clinical = frame.get("clinical_adjudication_status")
    if clinical not in CLINICAL_ADJUDICATION:
        errors.append(f"{frame_id}: unknown clinical_adjudication_status {clinical!r}")

    collision = frame.get("collision_status")
    if collision not in COLLISION_STATUS:
        errors.append(f"{frame_id}: unknown collision_status {collision!r}")

    authority = frame.get("runtime_authority_status")
    if authority not in RUNTIME_AUTHORITY:
        errors.append(f"{frame_id}: unknown runtime_authority_status {authority!r}")

    akey = frame.get("activation_key")
    if isinstance(akey, str) and not ACTIVATION_KEY_RE.fullmatch(akey):
        errors.append(f"{frame_id}: activation_key format invalid: {akey!r}")

    if promotion == "runtime_active_canonical" and collision == "real_collision_active_blocker":
        errors.append(
            f"{frame_id}: runtime_active_canonical cannot have collision_status real_collision_active_blocker"
        )

    pkg_path = frame.get("source_package_path")
    if isinstance(pkg_path, str) and promotion not in ("deferred",):
        full = ROOT / pkg_path.replace("\\", "/")
        if not full.is_dir():
            errors.append(f"{frame_id}: source_package_path does not exist: {pkg_path}")

    return frame


def validate_medical_frame_identity_index(
    index_path: Path,
    *,
    schema_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    schema_path = schema_path or DEFAULT_SCHEMA
    schema_doc, schema_errs = _load_yaml(schema_path)
    errors.extend(schema_errs)
    if schema_doc is None:
        return errors

    doc, load_errs = _load_yaml(index_path)
    errors.extend(load_errs)
    if not isinstance(doc, dict):
        return errors

    if doc.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if doc.get("runtime_consumed") is not False:
        errors.append("runtime_consumed must be false")
    if doc.get("status") != "governed_non_runtime_index":
        errors.append("status must be governed_non_runtime_index")

    frame_required = list((schema_doc.get("frame_required_fields") or []))

    families = doc.get("signal_families")
    if not isinstance(families, list) or not families:
        errors.append("signal_families must be a non-empty list")
        return errors

    seen_frame_ids: set[str] = set()
    active_activation_keys: dict[str, str] = {}

    for fam in families:
        if not isinstance(fam, dict):
            errors.append("signal_family entry must be a map")
            continue
        frames = fam.get("frames")
        if not isinstance(frames, list):
            errors.append(f"signal_family {fam.get('signal_family_id')}: frames must be a list")
            continue
        for frame in frames:
            parsed = _validate_frame(frame, errors, frame_required=frame_required)
            if parsed is None:
                continue
            mfid = parsed["medical_frame_id"]
            if mfid in seen_frame_ids:
                errors.append(f"duplicate medical_frame_id: {mfid}")
            seen_frame_ids.add(mfid)

            akey = parsed.get("activation_key", "")
            authority = parsed.get("runtime_authority_status")
            promotion = parsed.get("promotion_state")
            collision = parsed.get("collision_status")

            if authority == "active":
                if akey in active_activation_keys:
                    errors.append(
                        f"duplicate active activation_key {akey!r} on "
                        f"{active_activation_keys[akey]} and {mfid}"
                    )
                else:
                    active_activation_keys[akey] = mfid

            if promotion in NON_RUNTIME_PROMOTION and authority == "active":
                errors.append(f"{mfid}: non-runtime promotion_state cannot have active runtime authority")

            if promotion == "compiled_not_promoted" and collision not in (
                "allowed_non_runtime_collision",
                "none",
                "requires_adjudication",
            ):
                errors.append(
                    f"{mfid}: compiled_not_promoted requires allowed_non_runtime_collision or "
                    "explicit requires_adjudication"
                )

            if collision == "real_collision_active_blocker" and promotion.startswith("runtime_active"):
                errors.append(
                    f"{mfid}: real_collision_active_blocker incompatible with active runtime promotion"
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate medical frame identity index.")
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Path to medical_frame_identity_index_v1.yaml",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Path to schema file",
    )
    args = parser.parse_args(argv)
    errors = validate_medical_frame_identity_index(args.index, schema_path=args.schema)
    if errors:
        print("validation_status: FAIL", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    print("validation_status: PASS")
    print("errors: 0")
    print(f"index_path: {args.index.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
