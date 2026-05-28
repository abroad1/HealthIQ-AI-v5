#!/usr/bin/env python3
"""
Validate compile_manifest.yaml against knowledge_bus/schema/compile_manifest_schema_v1.yaml.

ARCH-RT-1 foundation validator — schema shape only; does not invoke compilers.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "compile_manifest_schema_v1.yaml"
ACTIVATION_KEY_PATTERN = re.compile(r"^signal_[a-z0-9_]+::[a-z][a-z0-9_]*$")


def load_yaml(path: Path, label: str) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return None, [f"{label} file not found: {path}"]
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), errors
    except yaml.YAMLError as exc:
        return None, [f"{label} is not valid YAML: {exc}"]
    except OSError as exc:
        return None, [f"{label} could not be read: {exc}"]


def _require_str(
    data: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    pattern: str | None = None,
    enum: list[str] | None = None,
) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"Missing or invalid required field: {key}")
        return
    if enum is not None and value not in enum:
        errors.append(f"{key} '{value}' not in {enum}")
    if pattern is not None and re.fullmatch(pattern, value) is None:
        errors.append(f"{key} '{value}' does not match pattern '{pattern}'")


def _validate_source_spec(item: Any, index: int, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"source_specs[{index}] must be a map")
        return
    for key in ("source_spec_id", "source_path", "source_hash", "source_hash_algorithm"):
        if key not in item:
            errors.append(f"source_specs[{index}] missing {key}")
    algo = item.get("source_hash_algorithm")
    if algo is not None and algo != "sha256":
        errors.append(f"source_specs[{index}] unsupported source_hash_algorithm: {algo}")


def _validate_output(item: Any, index: int, errors: list[str], compile_mode: str) -> None:
    if not isinstance(item, dict):
        errors.append(f"outputs[{index}] must be a map")
        return
    for key in ("output_type", "output_path", "output_hash", "output_hash_algorithm"):
        if key not in item:
            errors.append(f"outputs[{index}] missing {key}")
    out_type = item.get("output_type")
    if compile_mode == "activation" and out_type in (
        "signal_library",
        "research_brief",
        "package_manifest",
    ):
        ak = item.get("activation_key")
        if not isinstance(ak, str) or ACTIVATION_KEY_PATTERN.fullmatch(ak) is None:
            errors.append(
                f"outputs[{index}] activation_key required for activation output type {out_type}"
            )
        sid = item.get("source_spec_id")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"outputs[{index}] source_spec_id required for activation outputs")


def validate_compile_manifest(manifest: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest root must be a map"]

    for field in schema.get("root_required_fields") or []:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    compile_mode = manifest.get("compile_mode")
    _require_str(
        manifest,
        "compile_mode",
        errors,
        enum=(schema.get("field_rules") or {}).get("compile_mode", {}).get("enum"),
    )
    _require_str(manifest, "compile_id", errors)
    _require_str(manifest, "compiler_name", errors)
    _require_str(manifest, "compiler_version", errors)
    _require_str(
        manifest,
        "source_contract_version",
        errors,
        pattern=r"^\d+\.\d+\.\d+$",
    )
    _require_str(
        manifest,
        "translation_rules_version",
        errors,
        pattern=r"^\d+\.\d+\.\d+$",
    )
    _require_str(manifest, "compiled_at_utc", errors)
    _require_str(manifest, "compiled_by", errors)
    _require_str(
        manifest,
        "provenance_status",
        errors,
        enum=(schema.get("field_rules") or {}).get("provenance_status", {}).get("enum"),
    )

    source_specs = manifest.get("source_specs")
    if not isinstance(source_specs, list) or not source_specs:
        errors.append("source_specs must be a non-empty list")
    elif isinstance(source_specs, list):
        for idx, item in enumerate(source_specs):
            _validate_source_spec(item, idx, errors)

    outputs = manifest.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        errors.append("outputs must be a non-empty list")
    elif isinstance(outputs, list) and isinstance(compile_mode, str):
        for idx, item in enumerate(outputs):
            _validate_output(item, idx, errors, compile_mode)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate compile_manifest.yaml")
    parser.add_argument("--manifest", required=True, help="Path to compile_manifest.yaml")
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to compile_manifest_schema_v1.yaml",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    schema_path = Path(args.schema)

    manifest, errors = load_yaml(manifest_path, "manifest")
    if manifest is None:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    schema, schema_errors = load_yaml(schema_path, "schema")
    if schema is None:
        for err in schema_errors:
            print(err, file=sys.stderr)
        return 1

    if not isinstance(manifest, dict) or not isinstance(schema, dict):
        print("manifest and schema roots must be maps", file=sys.stderr)
        return 1

    validation_errors = validate_compile_manifest(manifest, schema)
    if validation_errors:
        for err in validation_errors:
            print(err, file=sys.stderr)
        return 1

    print(f"PASS: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
