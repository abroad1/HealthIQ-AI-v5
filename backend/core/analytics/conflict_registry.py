"""
v5.3 Sprint 7 - Conflict registry loader/validator.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.arbitration_v1 import canonical_json_sha256


@dataclass(frozen=True)
class ConflictRegistryStamp:
    conflict_registry_version: str
    conflict_registry_hash: str


@dataclass(frozen=True)
class ConflictRule:
    conflict_id: str
    system_a: str
    system_b: str
    conflict_type: str
    trigger_conditions: List[str]
    rationale_codes: List[str]
    rank: int


@dataclass(frozen=True)
class LoadedConflictRegistry:
    rules: List[ConflictRule]
    stamp: ConflictRegistryStamp


_registry_cache: Optional[LoadedConflictRegistry] = None


def _fixture_mode_enabled() -> bool:
    return os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "conflict_registry.yaml"


def load_conflict_registry() -> LoadedConflictRegistry:
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _registry_path()
    if not path.exists():
        if _fixture_mode_enabled():
            _registry_cache = LoadedConflictRegistry(
                rules=[],
                stamp=ConflictRegistryStamp(conflict_registry_version="1.0.0", conflict_registry_hash=""),
            )
            return _registry_cache
        raise FileNotFoundError(f"Conflict registry not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("conflict_registry.yaml must be a mapping")
    version = str(raw.get("registry_version", "")).strip()
    schema = str(raw.get("schema_version", "")).strip()
    if not version or not schema:
        raise ValueError("conflict_registry.yaml requires registry_version and schema_version")
    rules_raw = raw.get("conflict_definitions", [])
    if not isinstance(rules_raw, list):
        raise ValueError("conflict_definitions must be a list")

    seen: Set[str] = set()
    rules: List[ConflictRule] = []
    for idx, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise ValueError(f"conflict_definitions[{idx}] must be a mapping")
        conflict_id = str(item.get("conflict_id", "")).strip()
        if not conflict_id:
            raise ValueError(f"conflict_definitions[{idx}] missing conflict_id")
        if conflict_id in seen:
            raise ValueError(f"duplicate conflict_id: {conflict_id}")
        seen.add(conflict_id)
        system_a = str(item.get("system_a", "*")).strip() or "*"
        system_b = str(item.get("system_b", "*")).strip() or "*"
        conflict_type = str(item.get("conflict_type", "")).strip()
        if not conflict_type:
            raise ValueError(f"rule {conflict_id} missing conflict_type")
        conditions = item.get("trigger_conditions", [])
        rationale_codes = item.get("rationale_codes", [])
        precedence = item.get("precedence", {})
        if not isinstance(conditions, list) or not all(isinstance(x, str) for x in conditions):
            raise ValueError(f"rule {conflict_id} trigger_conditions must be list[str]")
        if not isinstance(rationale_codes, list) or not all(isinstance(x, str) for x in rationale_codes):
            raise ValueError(f"rule {conflict_id} rationale_codes must be list[str]")
        if not isinstance(precedence, dict) or not isinstance(precedence.get("rank"), int):
            raise ValueError(f"rule {conflict_id} precedence.rank must be int")
        rules.append(
            ConflictRule(
                conflict_id=conflict_id,
                system_a=system_a,
                system_b=system_b,
                conflict_type=conflict_type,
                trigger_conditions=sorted(set(str(x).strip() for x in conditions if str(x).strip())),
                rationale_codes=sorted(set(str(x).strip() for x in rationale_codes if str(x).strip())),
                rank=int(precedence["rank"]),
            )
        )

    rules.sort(key=lambda r: (r.rank, r.conflict_id))
    canonical_payload: Dict[str, Any] = {
        "registry_version": version,
        "schema_version": schema,
        "conflict_definitions": [
            {
                "conflict_id": r.conflict_id,
                "system_a": r.system_a,
                "system_b": r.system_b,
                "conflict_type": r.conflict_type,
                "trigger_conditions": r.trigger_conditions,
                "rationale_codes": r.rationale_codes,
                "precedence": {"rank": r.rank},
            }
            for r in rules
        ],
    }
    stamp = ConflictRegistryStamp(
        conflict_registry_version=version,
        conflict_registry_hash=canonical_json_sha256(canonical_payload),
    )
    _registry_cache = LoadedConflictRegistry(rules=rules, stamp=stamp)
    return _registry_cache
