#!/usr/bin/env python3
"""
Validate Knowledge Bus package manifest files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "package_manifest_schema.yaml"
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "package_manifest_audit.md"


def load_yaml(path: Path, label: str) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return None, [f"{label} file not found: {path}"]
    if not path.is_file():
        return None, [f"{label} path is not a file: {path}"]
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle), errors
    except yaml.YAMLError as exc:
        return None, [f"{label} is not valid YAML: {exc}"]
    except OSError as exc:
        return None, [f"{label} could not be read: {exc}"]


def as_dict(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} root must be a map")
        return {}
    return value


def validate_manifest(
    manifest: dict[str, Any],
    schema: dict[str, Any],
    manifest_path: Path,
    errors: list[str],
) -> None:
    required_fields = schema.get("required_fields")
    if not isinstance(required_fields, list):
        errors.append("schema.required_fields must be a list")
        return

    field_rules = schema.get("field_rules")
    if not isinstance(field_rules, dict):
        errors.append("schema.field_rules must be a map")
        return

    for field_name in required_fields:
        if field_name not in manifest:
            errors.append(f"Missing required field: {field_name}")

    for field_name, rule in field_rules.items():
        if field_name not in manifest:
            continue
        if not isinstance(rule, dict):
            errors.append(f"schema rule for {field_name} must be a map")
            continue
        value = manifest[field_name]
        expected_type = rule.get("type")
        if expected_type == "string":
            if not isinstance(value, str):
                errors.append(f"{field_name} must be a string")
                continue
        elif expected_type is not None:
            errors.append(f"Unsupported type rule for {field_name}: {expected_type}")
            continue

        pattern = rule.get("pattern")
        if isinstance(pattern, str) and isinstance(value, str):
            if re.fullmatch(pattern, value) is None:
                errors.append(f"{field_name} '{value}' does not match pattern '{pattern}'")

    for link_field in ("research_brief", "signal_library"):
        value = manifest.get(link_field)
        if not isinstance(value, str) or not value.strip():
            if link_field in manifest:
                errors.append(f"{link_field} must be a non-empty string")
            continue
        resolved_path = (manifest_path.parent / value).resolve()
        if not resolved_path.exists() or not resolved_path.is_file():
            errors.append(f"Referenced file not found for {link_field}: {resolved_path}")


def write_audit(audit_path: Path, status: str, errors: list[str]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Package Manifest Audit",
        "",
        f"validation_status: {status}",
        "",
        "errors:",
    ]
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- None")
    lines.append("")
    audit_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a package_manifest.yaml against schema and file references."
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to package_manifest.yaml",
    )
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to package_manifest_schema.yaml",
    )
    parser.add_argument(
        "--audit-path",
        default=str(DEFAULT_AUDIT_PATH),
        help="Path for audit markdown output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    manifest_path = Path(args.manifest)
    schema_path = Path(args.schema)
    audit_path = Path(args.audit_path)

    errors: list[str] = []

    manifest_obj, manifest_errors = load_yaml(manifest_path, "manifest")
    errors.extend(manifest_errors)
    schema_obj, schema_errors = load_yaml(schema_path, "schema")
    errors.extend(schema_errors)

    if not errors:
        manifest = as_dict(manifest_obj, "manifest", errors)
        schema = as_dict(schema_obj, "schema", errors)
        if not errors:
            validate_manifest(manifest, schema, manifest_path.resolve(), errors)

    status = "FAIL" if errors else "PASS"
    write_audit(audit_path, status, errors)

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {audit_path}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
