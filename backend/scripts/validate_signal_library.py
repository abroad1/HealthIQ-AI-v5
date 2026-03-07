#!/usr/bin/env python3
"""
HealthIQ Knowledge Bus signal library validator.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


CATEGORY_ORDER = [
    "yaml load",
    "root structure",
    "metadata",
    "signal identity",
    "dependencies",
    "thresholds",
    "activation logic",
    "forbidden fields",
    "cycle detection",
]


@dataclass
class ValidationState:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    category_errors: dict[str, list[str]] = field(
        default_factory=lambda: {category: [] for category in CATEGORY_ORDER}
    )
    category_warnings: dict[str, list[str]] = field(
        default_factory=lambda: {category: [] for category in CATEGORY_ORDER}
    )

    def add_error(self, category: str, message: str) -> None:
        self.errors.append(f"[{category}] {message}")
        if category in self.category_errors:
            self.category_errors[category].append(message)

    def add_warning(self, category: str, message: str) -> None:
        self.warnings.append(f"[{category}] {message}")
        if category in self.category_warnings:
            self.category_warnings[category].append(message)


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def read_yaml_file(path: Path, label: str, state: ValidationState) -> Any | None:
    if not path.exists():
        state.add_error("yaml load", f"{label} file not found: {path}")
        return None
    if not path.is_file():
        state.add_error("yaml load", f"{label} path is not a file: {path}")
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        state.add_error("yaml load", f"{label} is not valid YAML: {exc}")
    except OSError as exc:
        state.add_error("yaml load", f"{label} could not be read: {exc}")
    return None


def check_type(
    value: Any,
    expected: str,
    category: str,
    message: str,
    state: ValidationState,
) -> bool:
    type_map = {
        "string": str,
        "number": (int, float),
        "list": list,
        "map": dict,
    }
    py_type = type_map.get(expected)
    if py_type is None:
        state.add_error(category, f"Unsupported schema type rule '{expected}' for {message}")
        return False

    if expected == "number":
        valid = isinstance(value, py_type) and not isinstance(value, bool)
    else:
        valid = isinstance(value, py_type)

    if not valid:
        state.add_error(
            category,
            f"{message} must be of type {expected}",
        )
    return valid


def validate_pattern(
    value: str,
    pattern: str,
    category: str,
    message: str,
    state: ValidationState,
) -> None:
    if re.fullmatch(pattern, value) is None:
        state.add_error(category, f"{message} does not match pattern '{pattern}'")


def validate_root_structure(schema: dict[str, Any], library: dict[str, Any], state: ValidationState) -> None:
    required_root_fields = schema.get("root_required_fields")
    if not isinstance(required_root_fields, list):
        state.add_error("root structure", "schema.root_required_fields must be a list")
        required_root_fields = []

    for field_name in required_root_fields:
        if field_name not in library:
            state.add_error("root structure", f"Missing required root field '{field_name}'")

    if "library" not in library:
        state.add_error("root structure", "Missing root field 'library'")
    elif not isinstance(library.get("library"), dict):
        state.add_error("root structure", "Field 'library' must be a map")

    if "signals" not in library:
        state.add_error("root structure", "Missing root field 'signals'")
    elif not isinstance(library.get("signals"), list):
        state.add_error("root structure", "Field 'signals' must be a list")


def validate_metadata(schema: dict[str, Any], library: dict[str, Any], state: ValidationState) -> None:
    library_block = library.get("library")
    if not isinstance(library_block, dict):
        state.add_error("metadata", "Cannot validate metadata because 'library' is not a map")
        return

    required_fields = schema.get("library_required_fields")
    if not isinstance(required_fields, list):
        state.add_error("metadata", "schema.library_required_fields must be a list")
        required_fields = []

    rules = schema.get("library_field_rules")
    if not isinstance(rules, dict):
        state.add_error("metadata", "schema.library_field_rules must be a map")
        rules = {}

    for field_name in required_fields:
        if field_name not in library_block:
            state.add_error("metadata", f"library.{field_name} is required")

    for field_name in ("schema_version", "package_id", "library_name", "description"):
        if field_name not in library_block:
            continue
        value = library_block[field_name]
        field_rule = rules.get(field_name, {})
        if not isinstance(field_rule, dict):
            state.add_error("metadata", f"schema rule for library.{field_name} must be a map")
            continue
        expected_type = field_rule.get("type")
        if isinstance(expected_type, str):
            if not check_type(value, expected_type, "metadata", f"library.{field_name}", state):
                continue
        if isinstance(value, str):
            pattern = field_rule.get("pattern")
            if isinstance(pattern, str):
                validate_pattern(value, pattern, "metadata", f"library.{field_name}", state)
            min_length = field_rule.get("min_length")
            if isinstance(min_length, int) and len(value) < min_length:
                state.add_error(
                    "metadata",
                    f"library.{field_name} must be at least {min_length} characters",
                )

    package_id = library_block.get("package_id")
    if isinstance(package_id, str) and re.fullmatch(r"^KBP-\d{4}$", package_id) is None:
        state.add_error("metadata", "library.package_id must match '^KBP-\\d{4}$'")

    schema_version_pattern = (
        rules.get("schema_version", {}).get("pattern")
        if isinstance(rules.get("schema_version"), dict)
        else None
    )
    schema_version = library_block.get("schema_version")
    if isinstance(schema_version, str) and isinstance(schema_version_pattern, str):
        validate_pattern(
            schema_version,
            schema_version_pattern,
            "metadata",
            "library.schema_version",
            state,
        )


def validate_signal_identity(schema: dict[str, Any], library: dict[str, Any], state: ValidationState) -> list[dict[str, Any]]:
    signals = library.get("signals")
    if not isinstance(signals, list):
        state.add_error("signal identity", "Cannot validate signals because root 'signals' is not a list")
        return []

    required_fields = schema.get("signal_required_fields")
    if not isinstance(required_fields, list):
        state.add_error("signal identity", "schema.signal_required_fields must be a list")
        required_fields = []

    signal_field_rules = schema.get("signal_field_rules")
    if not isinstance(signal_field_rules, dict):
        state.add_error("signal identity", "schema.signal_field_rules must be a map")
        signal_field_rules = {}

    signal_id_pattern = None
    signal_id_rule = signal_field_rules.get("signal_id")
    if isinstance(signal_id_rule, dict) and isinstance(signal_id_rule.get("pattern"), str):
        signal_id_pattern = signal_id_rule["pattern"]
    else:
        state.add_error("signal identity", "schema.signal_field_rules.signal_id.pattern missing")

    seen_signal_ids: set[str] = set()
    valid_signal_rows: list[dict[str, Any]] = []

    for idx, signal in enumerate(signals):
        prefix = f"signals[{idx}]"
        if not isinstance(signal, dict):
            state.add_error("signal identity", f"{prefix} must be a map")
            continue
        valid_signal_rows.append(signal)

        for field_name in required_fields:
            if field_name not in signal:
                state.add_error("signal identity", f"{prefix}.{field_name} is required")

        signal_id = signal.get("signal_id")
        if not isinstance(signal_id, str):
            state.add_error("signal identity", f"{prefix}.signal_id must be a string")
            continue

        if signal_id_pattern and re.fullmatch(signal_id_pattern, signal_id) is None:
            state.add_error(
                "signal identity",
                f"{prefix}.signal_id '{signal_id}' does not match '{signal_id_pattern}'",
            )
        if signal_id in seen_signal_ids:
            state.add_error("signal identity", f"Duplicate signal_id '{signal_id}'")
        seen_signal_ids.add(signal_id)

    return valid_signal_rows


def _validate_dependency_map(
    category: str,
    signal_label: str,
    dep_map: Any,
    required_keys: list[str],
    dep_rules: dict[str, Any],
    state: ValidationState,
) -> None:
    if not isinstance(dep_map, dict):
        state.add_error(category, f"{signal_label} must be a map")
        return

    for dep_key in required_keys:
        if dep_key not in dep_map:
            state.add_error(category, f"{signal_label}.{dep_key} is required")
            continue
        dep_value = dep_map[dep_key]
        if not isinstance(dep_value, list):
            state.add_error(category, f"{signal_label}.{dep_key} must be a list")
            continue

        rule = dep_rules.get(dep_key)
        if not isinstance(rule, dict):
            state.add_error(category, f"schema dependency_map_rules.{dep_key} must be a map")
            continue
        item_pattern = rule.get("item_pattern")
        if not isinstance(item_pattern, str):
            state.add_error(category, f"schema dependency_map_rules.{dep_key}.item_pattern missing")
            continue

        for item_idx, item in enumerate(dep_value):
            field_name = f"{signal_label}.{dep_key}[{item_idx}]"
            if not isinstance(item, str):
                state.add_error(category, f"{field_name} must be a string")
                continue
            if re.fullmatch(item_pattern, item) is None:
                state.add_error(category, f"{field_name} value '{item}' does not match '{item_pattern}'")

            if dep_key in {"biomarkers", "derived_metrics"} and item.strip() == "":
                state.add_error(category, f"{field_name} must be a non-empty string")


def validate_dependencies(schema: dict[str, Any], signals: list[dict[str, Any]], state: ValidationState) -> None:
    signal_rules = schema.get("signal_field_rules")
    if not isinstance(signal_rules, dict):
        state.add_error("dependencies", "schema.signal_field_rules must be a map")
        return

    dependencies_rule = signal_rules.get("dependencies")
    optional_dependencies_rule = signal_rules.get("optional_dependencies")
    dependency_map_rules = schema.get("dependency_map_rules")
    if not isinstance(dependency_map_rules, dict):
        state.add_error("dependencies", "schema.dependency_map_rules must be a map")
        dependency_map_rules = {}

    dependencies_required_fields: list[str] = []
    if isinstance(dependencies_rule, dict) and isinstance(dependencies_rule.get("required_fields"), list):
        dependencies_required_fields = dependencies_rule["required_fields"]
    else:
        state.add_error("dependencies", "schema.signal_field_rules.dependencies.required_fields must be a list")

    optional_required_fields: list[str] = []
    if isinstance(optional_dependencies_rule, dict):
        maybe_fields = optional_dependencies_rule.get("required_fields")
        if isinstance(maybe_fields, list):
            optional_required_fields = maybe_fields
        else:
            state.add_error(
                "dependencies",
                "schema.signal_field_rules.optional_dependencies.required_fields must be a list",
            )

    for idx, signal in enumerate(signals):
        signal_label = f"signals[{idx}]"
        dependencies = signal.get("dependencies")
        _validate_dependency_map(
            "dependencies",
            f"{signal_label}.dependencies",
            dependencies,
            dependencies_required_fields,
            dependency_map_rules,
            state,
        )

        optional_dependencies = signal.get("optional_dependencies")
        if optional_dependencies is not None:
            _validate_dependency_map(
                "dependencies",
                f"{signal_label}.optional_dependencies",
                optional_dependencies,
                optional_required_fields,
                dependency_map_rules,
                state,
            )


def validate_thresholds(schema: dict[str, Any], signals: list[dict[str, Any]], state: ValidationState) -> None:
    required_fields = schema.get("threshold_required_fields")
    if not isinstance(required_fields, list):
        state.add_error("thresholds", "schema.threshold_required_fields must be a list")
        required_fields = []

    threshold_rules = schema.get("threshold_field_rules")
    if not isinstance(threshold_rules, dict):
        state.add_error("thresholds", "schema.threshold_field_rules must be a map")
        threshold_rules = {}

    operator_rule = threshold_rules.get("operator")
    allowed_operators = []
    if isinstance(operator_rule, dict) and isinstance(operator_rule.get("allowed"), list):
        allowed_operators = operator_rule["allowed"]
    else:
        state.add_error("thresholds", "schema.threshold_field_rules.operator.allowed must be a list")

    for signal_idx, signal in enumerate(signals):
        thresholds = signal.get("thresholds")
        label = f"signals[{signal_idx}].thresholds"
        if not isinstance(thresholds, list):
            state.add_error("thresholds", f"{label} must be a list")
            continue
        if len(thresholds) == 0:
            state.add_error("thresholds", f"{label} must contain at least one threshold")

        for threshold_idx, threshold in enumerate(thresholds):
            threshold_label = f"{label}[{threshold_idx}]"
            if not isinstance(threshold, dict):
                state.add_error("thresholds", f"{threshold_label} must be a map")
                continue

            for field_name in required_fields:
                if field_name not in threshold:
                    state.add_error("thresholds", f"{threshold_label}.{field_name} is required")

            operator = threshold.get("operator")
            if not isinstance(operator, str):
                state.add_error("thresholds", f"{threshold_label}.operator must be a string")
                continue

            if operator not in allowed_operators:
                state.add_error(
                    "thresholds",
                    f"{threshold_label}.operator '{operator}' is not in allowed operators {allowed_operators}",
                )

            if operator == "range":
                if "min_value" not in threshold or "max_value" not in threshold:
                    state.add_error(
                        "thresholds",
                        f"{threshold_label} with operator 'range' requires min_value and max_value",
                    )
                else:
                    if not check_type(
                        threshold.get("min_value"),
                        "number",
                        "thresholds",
                        f"{threshold_label}.min_value",
                        state,
                    ):
                        continue
                    check_type(
                        threshold.get("max_value"),
                        "number",
                        "thresholds",
                        f"{threshold_label}.max_value",
                        state,
                    )
            else:
                if "value" not in threshold:
                    state.add_error(
                        "thresholds",
                        f"{threshold_label} with operator '{operator}' requires value",
                    )
                else:
                    check_type(
                        threshold.get("value"),
                        "number",
                        "thresholds",
                        f"{threshold_label}.value",
                        state,
                    )


def validate_activation_logic(schema: dict[str, Any], signals: list[dict[str, Any]], state: ValidationState) -> None:
    signal_rules = schema.get("signal_field_rules")
    forbidden_patterns = schema.get("forbidden_patterns")

    allowed_values: list[str] = []
    if isinstance(signal_rules, dict):
        activation_rule = signal_rules.get("activation_logic")
        if isinstance(activation_rule, dict) and isinstance(activation_rule.get("allowed"), list):
            allowed_values = activation_rule["allowed"]
        else:
            state.add_error("activation logic", "schema.signal_field_rules.activation_logic.allowed must be a list")
    else:
        state.add_error("activation logic", "schema.signal_field_rules must be a map")

    explicit_forbidden: list[str] = []
    if isinstance(forbidden_patterns, dict) and isinstance(forbidden_patterns.get("activation_logic"), list):
        explicit_forbidden = forbidden_patterns["activation_logic"]
    else:
        state.add_error("activation logic", "schema.forbidden_patterns.activation_logic must be a list")

    for idx, signal in enumerate(signals):
        value = signal.get("activation_logic")
        label = f"signals[{idx}].activation_logic"
        if not isinstance(value, str):
            state.add_error("activation logic", f"{label} must be a string")
            continue

        if value in explicit_forbidden:
            state.add_error("activation logic", f"{label} '{value}' is explicitly forbidden")
            continue
        if value not in allowed_values:
            state.add_error(
                "activation logic",
                f"{label} '{value}' is not in allowed values {allowed_values}",
            )


def _scan_for_forbidden_fields(
    node: Any,
    forbidden: set[str],
    path: str,
    category: str,
    state: ValidationState,
) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            current = f"{path}.{key}" if path else key
            if key in forbidden:
                state.add_error(category, f"Forbidden field '{key}' found at '{current}'")
            _scan_for_forbidden_fields(value, forbidden, current, category, state)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            _scan_for_forbidden_fields(item, forbidden, f"{path}[{idx}]", category, state)


def validate_forbidden_fields(schema: dict[str, Any], signals: list[dict[str, Any]], state: ValidationState) -> None:
    forbidden_patterns = schema.get("forbidden_patterns")
    if not isinstance(forbidden_patterns, dict):
        state.add_error("forbidden fields", "schema.forbidden_patterns must be a map")
        return
    fields = forbidden_patterns.get("forbidden_fields")
    if not isinstance(fields, list):
        state.add_error("forbidden fields", "schema.forbidden_patterns.forbidden_fields must be a list")
        return
    forbidden = {f for f in fields if isinstance(f, str)}
    for idx, signal in enumerate(signals):
        _scan_for_forbidden_fields(
            signal,
            forbidden,
            path=f"signals[{idx}]",
            category="forbidden fields",
            state=state,
        )


def build_signal_graph(signals: list[dict[str, Any]], state: ValidationState) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    valid_signal_ids = {
        signal["signal_id"]
        for signal in signals
        if isinstance(signal.get("signal_id"), str)
    }

    for idx, signal in enumerate(signals):
        signal_id = signal.get("signal_id")
        if not isinstance(signal_id, str):
            continue
        dependencies = signal.get("dependencies")
        optional_dependencies = signal.get("optional_dependencies")
        edges: list[str] = []

        if isinstance(dependencies, dict):
            dep_signals = dependencies.get("signals")
            if isinstance(dep_signals, list):
                for dep_idx, dep_signal_id in enumerate(dep_signals):
                    ref = f"signals[{idx}].dependencies.signals[{dep_idx}]"
                    if not isinstance(dep_signal_id, str):
                        state.add_error("dependencies", f"{ref} must be a string")
                        continue
                    if dep_signal_id not in valid_signal_ids:
                        state.add_error(
                            "dependencies",
                            f"{ref} references unknown signal_id '{dep_signal_id}'",
                        )
                    edges.append(dep_signal_id)

        if isinstance(optional_dependencies, dict):
            optional_dep_signals = optional_dependencies.get("signals")
            if isinstance(optional_dep_signals, list):
                for dep_idx, dep_signal_id in enumerate(optional_dep_signals):
                    ref = f"signals[{idx}].optional_dependencies.signals[{dep_idx}]"
                    if not isinstance(dep_signal_id, str):
                        state.add_error("dependencies", f"{ref} must be a string")
                        continue
                    if dep_signal_id not in valid_signal_ids:
                        state.add_error(
                            "dependencies",
                            f"{ref} references unknown signal_id '{dep_signal_id}'",
                        )
                    edges.append(dep_signal_id)

        graph[signal_id] = edges

    return graph


def detect_cycles(graph: dict[str, list[str]], state: ValidationState) -> None:
    visited: set[str] = set()
    in_stack: set[str] = set()
    stack: list[str] = []

    def dfs(node: str) -> None:
        visited.add(node)
        in_stack.add(node)
        stack.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in graph:
                continue
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in in_stack:
                cycle_start = stack.index(neighbor)
                cycle_path = stack[cycle_start:] + [neighbor]
                state.add_error(
                    "cycle detection",
                    "Circular signal dependency detected: " + " -> ".join(cycle_path),
                )

        in_stack.remove(node)
        stack.pop()

    for node in graph:
        if node not in visited:
            dfs(node)


def write_architecture_audit(
    output_dir: Path,
    package_id: str,
    schema_version: str,
    validator_status: str,
    signal_count: int,
    state: ValidationState,
) -> None:
    category_lines = []
    for category in CATEGORY_ORDER:
        errors = state.category_errors.get(category, [])
        warnings = state.category_warnings.get(category, [])
        status = "PASS" if not errors else "FAIL"
        category_lines.append(
            f"- {category}: {status} (errors={len(errors)}, warnings={len(warnings)})"
        )

    error_lines = "\n".join(f"- {entry}" for entry in state.errors) if state.errors else "- None"
    warning_lines = (
        "\n".join(f"- {entry}" for entry in state.warnings) if state.warnings else "- None"
    )

    content = (
        "# Architecture Audit\n\n"
        "## Header\n"
        f"- package_id: {package_id}\n"
        f"- schema_version: {schema_version}\n"
        f"- validator_status: {validator_status}\n\n"
        "## Summary\n"
        f"- total signals: {signal_count}\n"
        f"- total errors: {len(state.errors)}\n"
        f"- total warnings: {len(state.warnings)}\n\n"
        "## Validation Results by Category\n"
        f"{chr(10).join(category_lines)}\n\n"
        "## Errors\n"
        f"{error_lines}\n\n"
        "## Warnings\n"
        f"{warning_lines}\n"
    )

    audit_path = output_dir / "architecture_audit.md"
    with audit_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def write_knowledge_status(
    output_dir: Path,
    package_id: str,
    state: ValidationState,
) -> None:
    has_errors = len(state.errors) > 0
    validator_status = "FAIL" if has_errors else "PASS"
    status = "FAILED" if has_errors else "READY_FOR_IMPLEMENTATION"
    ready_for_implementation = not has_errors
    payload = {
        "package_id": package_id,
        "status": status,
        "validator_status": validator_status,
        "ready_for_implementation": ready_for_implementation,
        "validated_utc": utc_now_iso(),
        "errors": state.errors,
        "warnings": state.warnings,
    }
    status_path = output_dir / "knowledge_status.json"
    with status_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")


def validate_signal_library(schema_path: Path, library_path: Path, output_dir: Path) -> int:
    state = ValidationState()

    schema_obj = read_yaml_file(schema_path, "schema", state)
    library_obj = read_yaml_file(library_path, "library", state)

    if schema_obj is None or library_obj is None:
        package_id = "UNKNOWN"
        schema_version = "UNKNOWN"
        output_dir.mkdir(parents=True, exist_ok=True)
        write_architecture_audit(
            output_dir=output_dir,
            package_id=package_id,
            schema_version=schema_version,
            validator_status="FAIL",
            signal_count=0,
            state=state,
        )
        write_knowledge_status(output_dir=output_dir, package_id=package_id, state=state)
        return 1

    if not isinstance(schema_obj, dict):
        state.add_error("yaml load", "schema root must be a map")
    if not isinstance(library_obj, dict):
        state.add_error("yaml load", "library root must be a map")

    if not isinstance(schema_obj, dict) or not isinstance(library_obj, dict):
        package_id = "UNKNOWN"
        schema_version = "UNKNOWN"
        output_dir.mkdir(parents=True, exist_ok=True)
        write_architecture_audit(
            output_dir=output_dir,
            package_id=package_id,
            schema_version=schema_version,
            validator_status="FAIL",
            signal_count=0,
            state=state,
        )
        write_knowledge_status(output_dir=output_dir, package_id=package_id, state=state)
        return 1

    validate_root_structure(schema_obj, library_obj, state)
    validate_metadata(schema_obj, library_obj, state)

    signals = validate_signal_identity(schema_obj, library_obj, state)
    validate_dependencies(schema_obj, signals, state)
    validate_thresholds(schema_obj, signals, state)
    validate_activation_logic(schema_obj, signals, state)
    validate_forbidden_fields(schema_obj, signals, state)

    graph = build_signal_graph(signals, state)
    detect_cycles(graph, state)

    library_meta = library_obj.get("library")
    package_id = (
        library_meta.get("package_id")
        if isinstance(library_meta, dict) and isinstance(library_meta.get("package_id"), str)
        else "UNKNOWN"
    )
    schema_version = (
        library_meta.get("schema_version")
        if isinstance(library_meta, dict) and isinstance(library_meta.get("schema_version"), str)
        else "UNKNOWN"
    )

    validator_status = "FAIL" if state.errors else "PASS"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_architecture_audit(
        output_dir=output_dir,
        package_id=package_id,
        schema_version=schema_version,
        validator_status=validator_status,
        signal_count=len(library_obj.get("signals", [])) if isinstance(library_obj.get("signals"), list) else 0,
        state=state,
    )
    write_knowledge_status(output_dir=output_dir, package_id=package_id, state=state)
    return 1 if state.errors else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Knowledge Bus signal library YAML against schema contract."
    )
    parser.add_argument(
        "--library",
        required=True,
        help="Path to signal library YAML file.",
    )
    parser.add_argument(
        "--schema",
        required=True,
        help="Path to signal library schema YAML file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where architecture_audit.md and knowledge_status.json will be written.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    library_path = Path(args.library)
    schema_path = Path(args.schema)
    output_dir = Path(args.output_dir)

    return validate_signal_library(
        schema_path=schema_path,
        library_path=library_path,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    raise SystemExit(main())