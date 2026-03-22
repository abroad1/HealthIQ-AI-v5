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


def _as_field_rules(raw: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        errors.append(f"{label} must be a map")
        return {}
    normalised: dict[str, dict[str, Any]] = {}
    for field_name, rule in raw.items():
        if not isinstance(field_name, str) or not field_name.strip():
            errors.append(f"{label} contains an invalid field name")
            continue
        if not isinstance(rule, dict):
            errors.append(f"schema rule for {field_name} in {label} must be a map")
            continue
        normalised[field_name] = rule
    return normalised


def _validate_field_rule(
    field_name: str,
    value: Any,
    rule: dict[str, Any],
    errors: list[str],
) -> None:
    expected_type = rule.get("type")
    if expected_type == "string":
        if not isinstance(value, str):
            errors.append(f"{field_name} must be a string")
            return
    elif expected_type is not None:
        errors.append(f"Unsupported type rule for {field_name}: {expected_type}")
        return

    enum_values = rule.get("enum")
    if enum_values is not None:
        if not isinstance(enum_values, list) or not all(isinstance(x, str) for x in enum_values):
            errors.append(f"schema enum rule for {field_name} must be a list[string]")
        elif isinstance(value, str) and value not in enum_values:
            errors.append(
                f"{field_name} '{value}' is not one of allowed values {enum_values}"
            )

    pattern = rule.get("pattern")
    if isinstance(pattern, str) and isinstance(value, str):
        if re.fullmatch(pattern, value) is None:
            errors.append(f"{field_name} '{value}' does not match pattern '{pattern}'")


def validate_manifest(
    manifest: dict[str, Any],
    schema: dict[str, Any],
    manifest_path: Path,
    errors: list[str],
    *,
    require_behavioural_impact: bool,
    require_engine_compatibility: bool,
    authoritative_engine_compatibility: str | None,
) -> None:
    required_fields = schema.get("required_fields")
    if not isinstance(required_fields, list):
        errors.append("schema.required_fields must be a list")
        return

    field_rules = _as_field_rules(schema.get("field_rules"), "schema.field_rules", errors)
    optional_field_rules = _as_field_rules(
        schema.get("optional_fields"), "schema.optional_fields", errors
    )
    merged_field_rules = dict(field_rules)
    for field_name, rule in optional_field_rules.items():
        merged_field_rules.setdefault(field_name, rule)

    for field_name in required_fields:
        if field_name not in manifest:
            errors.append(f"Missing required field: {field_name}")

    if require_behavioural_impact:
        value = manifest.get("behavioural_impact")
        if not isinstance(value, str) or not value.strip():
            errors.append("Missing required field: behavioural_impact")
    if require_engine_compatibility:
        value = manifest.get("engine_compatibility")
        if not isinstance(value, str) or not value.strip():
            errors.append("Missing required field: engine_compatibility")

    for field_name, rule in merged_field_rules.items():
        if field_name not in manifest:
            continue
        value = manifest[field_name]
        _validate_field_rule(field_name, value, rule, errors)

    if authoritative_engine_compatibility:
        value = manifest.get("engine_compatibility")
        if isinstance(value, str) and value.strip() and value != authoritative_engine_compatibility:
            errors.append(
                "engine_compatibility must match authoritative value "
                f"'{authoritative_engine_compatibility}'"
            )

    for link_field in ("research_brief", "signal_library"):
        value = manifest.get(link_field)
        if not isinstance(value, str) or not value.strip():
            if link_field in manifest:
                errors.append(f"{link_field} must be a non-empty string")
            continue
        resolved_path = (manifest_path.parent / value).resolve()
        if not resolved_path.exists() or not resolved_path.is_file():
            errors.append(f"Referenced file not found for {link_field}: {resolved_path}")

    im = manifest.get("intelligence_model")
    if im is not None:
        if not isinstance(im, str) or not im.strip():
            errors.append("intelligence_model must be a non-empty string when present")
        else:
            resolved_im = (manifest_path.parent / im.strip()).resolve()
            if not resolved_im.exists() or not resolved_im.is_file():
                errors.append(f"Referenced file not found for intelligence_model: {resolved_im}")


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
    parser.add_argument(
        "--require-behavioural-impact",
        action="store_true",
        help="Require behavioural_impact field in manifest.",
    )
    parser.add_argument(
        "--require-engine-compatibility",
        action="store_true",
        help="Require engine_compatibility field in manifest.",
    )
    parser.add_argument(
        "--authoritative-engine-compatibility",
        default="",
        help="Authoritative engine_compatibility value to enforce when present.",
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
            forward_requirements = schema.get("forward_requirements")
            if (
                not args.authoritative_engine_compatibility
                and isinstance(forward_requirements, dict)
                and isinstance(forward_requirements.get("engine_compatibility"), dict)
            ):
                maybe_authoritative = forward_requirements["engine_compatibility"].get("authoritative_value")
                if isinstance(maybe_authoritative, str):
                    args.authoritative_engine_compatibility = maybe_authoritative
            validate_manifest(
                manifest,
                schema,
                manifest_path.resolve(),
                errors,
                require_behavioural_impact=args.require_behavioural_impact,
                require_engine_compatibility=args.require_engine_compatibility,
                authoritative_engine_compatibility=(
                    args.authoritative_engine_compatibility.strip() or None
                ),
            )

    status = "FAIL" if errors else "PASS"
    write_audit(audit_path, status, errors)

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {audit_path}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
