#!/usr/bin/env python3
"""
Validate Knowledge Bus research_brief.yaml against governance schema.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "research_brief_schema.yaml"
DEFAULT_BIOMARKER_REGISTRY_PATH = ROOT / "backend" / "ssot" / "biomarkers.yaml"
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "research_audit.md"

BIOMARKER_PATTERN = re.compile(r"^[a-z0-9_]+$")
DERIVED_METRIC_PATTERN = re.compile(r"^[a-z0-9_]+$")
ALLOWED_EVIDENCE_STRENGTH = {"exploratory", "moderate", "strong", "consensus"}


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


def validate_required_root_fields(
    schema: dict[str, Any],
    brief: dict[str, Any],
    errors: list[str],
) -> None:
    required = schema.get("root_required_fields")
    if not isinstance(required, list):
        errors.append("schema.root_required_fields must be a list")
        return
    for field_name in required:
        if field_name not in brief:
            errors.append(f"Missing required root field: {field_name}")


def validate_sources(brief: dict[str, Any], errors: list[str]) -> None:
    sources = brief.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        return
    if len(sources) == 0:
        errors.append("sources must contain at least one item")
        return

    for idx, source in enumerate(sources):
        prefix = f"sources[{idx}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be a map")
            continue

        for required_key in ("paper_title", "journal", "year"):
            if required_key not in source:
                errors.append(f"{prefix}.{required_key} is required")

        paper_title = source.get("paper_title")
        if "paper_title" in source and (not isinstance(paper_title, str) or not paper_title.strip()):
            errors.append(f"{prefix}.paper_title must be a non-empty string")

        journal = source.get("journal")
        if "journal" in source and (not isinstance(journal, str) or not journal.strip()):
            errors.append(f"{prefix}.journal must be a non-empty string")

        year = source.get("year")
        if "year" in source:
            if not isinstance(year, (int, float)) or isinstance(year, bool):
                errors.append(f"{prefix}.year must be numeric")
            elif year < 1900 or year > 2100:
                errors.append(f"{prefix}.year must be between 1900 and 2100")

        if "doi" in source and source["doi"] is not None and not isinstance(source["doi"], str):
            errors.append(f"{prefix}.doi must be a string when provided")
        if "url" in source and source["url"] is not None and not isinstance(source["url"], str):
            errors.append(f"{prefix}.url must be a string when provided")


def extract_registry_keys(registry: dict[str, Any], errors: list[str]) -> set[str]:
    root = registry.get("biomarkers")
    if not isinstance(root, dict):
        errors.append("biomarker registry missing map key: biomarkers")
        return set()
    return set(root.keys())


def validate_biomarkers(
    brief: dict[str, Any],
    registry_keys: set[str],
    errors: list[str],
) -> list[str]:
    validated: list[str] = []
    biomarkers = brief.get("biomarkers")
    if not isinstance(biomarkers, list):
        errors.append("biomarkers must be a list")
        return validated
    if len(biomarkers) == 0:
        errors.append("biomarkers must contain at least one item")
        return validated

    for idx, biomarker in enumerate(biomarkers):
        label = f"biomarkers[{idx}]"
        if not isinstance(biomarker, str):
            errors.append(f"{label} must be a string")
            continue
        if BIOMARKER_PATTERN.fullmatch(biomarker) is None:
            errors.append(f"{label} '{biomarker}' does not match ^[a-z0-9_]+$")
            continue
        if biomarker not in registry_keys:
            errors.append(f"{label} '{biomarker}' not found in SSOT biomarker registry")
            continue
        validated.append(biomarker)
    return sorted(set(validated))


def validate_derived_metrics(
    brief: dict[str, Any],
    errors: list[str],
) -> list[str]:
    validated: list[str] = []
    derived_metrics = brief.get("derived_metrics")
    if derived_metrics is None:
        return validated
    if not isinstance(derived_metrics, list):
        errors.append("derived_metrics must be a list when provided")
        return validated

    for idx, metric in enumerate(derived_metrics):
        label = f"derived_metrics[{idx}]"
        if not isinstance(metric, str):
            errors.append(f"{label} must be a string")
            continue
        if DERIVED_METRIC_PATTERN.fullmatch(metric) is None:
            errors.append(f"{label} '{metric}' does not match ^[a-z0-9_]+$")
            continue
        validated.append(metric)
    return sorted(set(validated))


def validate_evidence_strength(brief: dict[str, Any], errors: list[str]) -> None:
    value = brief.get("evidence_strength")
    if not isinstance(value, str):
        errors.append("evidence_strength must be a string")
        return
    if value not in ALLOWED_EVIDENCE_STRENGTH:
        errors.append(
            "evidence_strength must be one of: exploratory, moderate, strong, consensus"
        )


def write_audit(
    audit_path: Path,
    status: str,
    errors: list[str],
    validated_biomarkers: list[str],
    validated_metrics: list[str],
) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Research Audit",
        "",
        f"validation_status: {status}",
        "derived_metrics_registry: NOT_AVAILABLE",
        "",
        "errors:",
    ]
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- None")

    lines.extend(["", "validated_biomarkers:"])
    if validated_biomarkers:
        lines.extend(f"- {item}" for item in validated_biomarkers)
    else:
        lines.append("- None")

    lines.extend(["", "validated_metrics:"])
    if validated_metrics:
        lines.extend(f"- {item}" for item in validated_metrics)
    else:
        lines.append("- None")

    lines.append("")
    audit_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Knowledge Bus research_brief.yaml."
    )
    parser.add_argument(
        "--brief",
        required=True,
        help="Path to research_brief.yaml file to validate.",
    )
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to research brief schema YAML.",
    )
    parser.add_argument(
        "--biomarkers-registry",
        default=str(DEFAULT_BIOMARKER_REGISTRY_PATH),
        help="Path to SSOT biomarkers registry YAML.",
    )
    parser.add_argument(
        "--audit-path",
        default=str(DEFAULT_AUDIT_PATH),
        help="Audit output path. Default: backend/artifacts/research_audit.md",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    brief_path = Path(args.brief)
    schema_path = Path(args.schema)
    biomarker_registry_path = Path(args.biomarkers_registry)
    audit_path = Path(args.audit_path)

    errors: list[str] = []

    schema_obj, schema_errors = load_yaml(schema_path, "schema")
    errors.extend(schema_errors)
    brief_obj, brief_errors = load_yaml(brief_path, "research brief")
    errors.extend(brief_errors)
    registry_obj, registry_errors = load_yaml(
        biomarker_registry_path, "biomarker registry"
    )
    errors.extend(registry_errors)

    validated_biomarkers: list[str] = []
    validated_metrics: list[str] = []

    if not errors:
        schema = as_dict(schema_obj, "schema", errors)
        brief = as_dict(brief_obj, "research brief", errors)
        registry = as_dict(registry_obj, "biomarker registry", errors)

        if not errors:
            validate_required_root_fields(schema, brief, errors)
            validate_sources(brief, errors)
            registry_keys = extract_registry_keys(registry, errors)
            validated_biomarkers = validate_biomarkers(brief, registry_keys, errors)
            validated_metrics = validate_derived_metrics(brief, errors)
            validate_evidence_strength(brief, errors)

    status = "FAIL" if errors else "PASS"
    write_audit(
        audit_path=audit_path,
        status=status,
        errors=errors,
        validated_biomarkers=validated_biomarkers,
        validated_metrics=validated_metrics,
    )

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"validated_biomarkers: {len(validated_biomarkers)}")
    print(f"validated_metrics: {len(validated_metrics)}")
    print(f"audit_path: {audit_path}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
