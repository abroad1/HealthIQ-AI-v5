"""
CLIN-PRIORITY-CORE-1 — Single loader for compiled prioritisation rules.

Consumes knowledge_bus/compiled/prioritisation/compiled_prioritisation_rules.yaml.
Tests and runtime must share this loader (no second authority source).
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

_CACHE: Optional["LoadedPrioritisationPackage"] = None


def _repo_root() -> Path:
    # backend/core/analytics/prioritisation_registry.py → repo root
    return Path(__file__).resolve().parents[3]


def _default_rules_path() -> Path:
    return (
        _repo_root()
        / "knowledge_bus"
        / "compiled"
        / "prioritisation"
        / "compiled_prioritisation_rules.yaml"
    )


def _default_manifest_path() -> Path:
    return (
        _repo_root()
        / "knowledge_bus"
        / "compiled"
        / "manifests"
        / "clin_priority_prioritisation_six_domain_v1.yaml"
    )


def content_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PrioritisationPackageStamp:
    package_id: str
    package_version: str
    contract_version: str
    ruleset_version: str
    compile_run_id: str
    package_hash: str
    compiler_name: str
    compiler_version: str


@dataclass(frozen=True)
class LoadedPrioritisationPackage:
    raw: Dict[str, Any]
    stamp: PrioritisationPackageStamp
    finding_types: Dict[str, Dict[str, Any]]
    quarantine_namespaces: List[Dict[str, Any]]
    excluded_unset_thresholds: List[Dict[str, Any]]
    scenarios_in_scope: List[str]


def _fixture_mode_enabled() -> bool:
    return os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}


def _validate_raw(raw: Dict[str, Any]) -> None:
    required = [
        "schema_version",
        "package_id",
        "package_version",
        "contract_version",
        "ruleset_version",
        "compiler_name",
        "compiler_version",
        "finding_types",
        "quarantine_namespaces",
    ]
    for key in required:
        if key not in raw:
            raise ValueError(f"compiled prioritisation rules missing required field: {key}")
    if str(raw.get("contract_version")) != "0.6.3":
        raise ValueError("contract_version must be 0.6.3 for CLIN-PRIORITY-CORE-1")
    if str(raw.get("ruleset_version")) != "0.5":
        raise ValueError("ruleset_version must be 0.5 for CLIN-PRIORITY-CORE-1")
    finding_types = raw.get("finding_types")
    if not isinstance(finding_types, list) or not finding_types:
        raise ValueError("finding_types must be a non-empty list")
    # Fail closed: never allow [U] thresholds to be compiled as numeric rules
    for item in raw.get("excluded_unset_thresholds", []) or []:
        if not isinstance(item, dict) or not str(item.get("id", "")).strip():
            raise ValueError("excluded_unset_thresholds entries must have id")


def load_prioritisation_package(
    rules_path: Optional[Path] = None,
    *,
    force_reload: bool = False,
) -> LoadedPrioritisationPackage:
    """Load the single compiled prioritisation authority."""
    global _CACHE
    if _CACHE is not None and not force_reload and rules_path is None:
        return _CACHE

    path = Path(rules_path) if rules_path is not None else _default_rules_path()
    if not path.exists():
        if _fixture_mode_enabled():
            empty = LoadedPrioritisationPackage(
                raw={},
                stamp=PrioritisationPackageStamp(
                    package_id="fixture_empty",
                    package_version="0.0.0",
                    contract_version="0.6.3",
                    ruleset_version="0.5",
                    compile_run_id="fixture",
                    package_hash="",
                    compiler_name="fixture",
                    compiler_version="0.0.0",
                ),
                finding_types={},
                quarantine_namespaces=[],
                excluded_unset_thresholds=[],
                scenarios_in_scope=[],
            )
            if rules_path is None:
                _CACHE = empty
            return empty
        raise FileNotFoundError(f"Compiled prioritisation rules not found: {path}")

    text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(text) or {}
    if not isinstance(raw, dict):
        raise ValueError("compiled prioritisation rules must be a mapping")
    _validate_raw(raw)

    package_hash = content_sha256(text)
    compile_run_id = f"clin-priority-six-domain-{package_hash[:12]}"
    stamp = PrioritisationPackageStamp(
        package_id=str(raw["package_id"]),
        package_version=str(raw["package_version"]),
        contract_version=str(raw["contract_version"]),
        ruleset_version=str(raw["ruleset_version"]),
        compile_run_id=compile_run_id,
        package_hash=package_hash,
        compiler_name=str(raw["compiler_name"]),
        compiler_version=str(raw["compiler_version"]),
    )

    finding_types: Dict[str, Dict[str, Any]] = {}
    for row in raw.get("finding_types", []):
        if not isinstance(row, dict):
            continue
        ft = str(row.get("finding_type", "")).strip()
        if not ft:
            raise ValueError("finding_type entry missing finding_type")
        if ft in finding_types:
            raise ValueError(f"duplicate finding_type in compiled rules: {ft}")
        finding_types[ft] = row

    loaded = LoadedPrioritisationPackage(
        raw=raw,
        stamp=stamp,
        finding_types=finding_types,
        quarantine_namespaces=list(raw.get("quarantine_namespaces") or []),
        excluded_unset_thresholds=list(raw.get("excluded_unset_thresholds") or []),
        scenarios_in_scope=[str(x) for x in (raw.get("scenarios_in_scope") or [])],
    )
    if rules_path is None:
        _CACHE = loaded
    return loaded


def clear_prioritisation_package_cache() -> None:
    global _CACHE
    _CACHE = None


def default_manifest_path() -> Path:
    return _default_manifest_path()
