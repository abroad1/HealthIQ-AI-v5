#!/usr/bin/env python3
"""
Validate canonical metric identifier namespace usage.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
RATIO_REGISTRY_PATH = ROOT / "backend" / "core" / "analytics" / "ratio_registry.py"
PACKAGES_DIR = ROOT / "knowledge_bus" / "packages"

CANONICAL_PATTERN = re.compile(r"^[a-z0-9_]+$")
DEFERRED_METRICS_ALLOWLIST = {
    "derived.homa_ir",
    "derived.remnant_cholesterol",
    "derived.fib_4",
}

METRIC_VALUE_KEYS = {
    "primary_metric",
    "metric_id",
    "signal_value",
    "metric",
}
METRIC_LIST_KEYS = {
    "supporting_metrics",
    "derived_metrics",
    "supporting_markers",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _is_allowed(identifier: str) -> bool:
    return identifier in DEFERRED_METRICS_ALLOWLIST


def _validate_identifier(identifier: str) -> str | None:
    if _is_allowed(identifier):
        return None
    if "." in identifier:
        return "contains '.'"
    if identifier.startswith("derived"):
        return "starts with 'derived'"
    if CANONICAL_PATTERN.fullmatch(identifier) is None:
        return "does not match ^[a-z0-9_]+$"
    return None


def _extract_ratio_registry_identifiers(path: Path) -> list[tuple[str, str]]:
    tree = ast.parse(_read_text(path))
    extracted: list[tuple[str, str]] = []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id == "DERIVED_IDS" and isinstance(node.value, ast.Tuple):
                for item in node.value.elts:
                    if isinstance(item, ast.Constant) and isinstance(item.value, str):
                        extracted.append((f"{path}:DERIVED_IDS", item.value))
            if target.id == "_DERIVED_INPUTS" and isinstance(node.value, ast.Dict):
                for key in node.value.keys:
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        extracted.append((f"{path}:_DERIVED_INPUTS", key.value))
    return extracted


def _extract_signal_library_identifiers(path: Path) -> list[tuple[str, str]]:
    data = _load_yaml(path)
    extracted: list[tuple[str, str]] = []

    def walk(node: Any, context: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                new_context = f"{context}.{key}" if context else str(key)
                if key in METRIC_VALUE_KEYS and isinstance(value, str):
                    extracted.append((new_context, value))
                elif key in METRIC_LIST_KEYS and isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, str):
                            extracted.append((f"{new_context}[{idx}]", item))
                walk(value, new_context)
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                walk(item, f"{context}[{idx}]")

    walk(data, path.as_posix())
    return extracted


def main() -> int:
    violations: list[str] = []

    if not RATIO_REGISTRY_PATH.exists():
        print(f"ERROR: Missing ratio registry: {RATIO_REGISTRY_PATH}", file=sys.stderr)
        return 1

    for source, identifier in _extract_ratio_registry_identifiers(RATIO_REGISTRY_PATH):
        reason = _validate_identifier(identifier)
        if reason:
            violations.append(f"{source} -> '{identifier}' ({reason})")

    for signal_library_path in sorted(PACKAGES_DIR.glob("*/signal_library.yaml")):
        try:
            entries = _extract_signal_library_identifiers(signal_library_path)
        except Exception as exc:
            violations.append(f"{signal_library_path}: failed to parse ({exc})")
            continue
        for source, identifier in entries:
            reason = _validate_identifier(identifier)
            if reason:
                violations.append(f"{source} -> '{identifier}' ({reason})")

    if violations:
        print("Metric namespace validation: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("Metric namespace validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
