"""
v5.3 Sprint 3 - SSOT loader for interaction precedence rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.precedence_engine_v1 import canonical_json_sha256

_ALLOWED_DOMINANCE = {"a_over_b", "b_over_a", "conditional"}
_ALLOWED_TIE_BREAKERS = {
    "persistence_beats_spike",
    "high_criticality_wins",
    "confidence_gate",
    "explicit_registry_order",
}


@dataclass(frozen=True)
class PrecedenceRegistryStamp:
    precedence_registry_version: str
    precedence_registry_hash: str


@dataclass(frozen=True)
class PrecedenceRule:
    rule_id: str
    applies_to: Dict[str, str]
    dominance: str
    conditions: List[str]
    tie_breakers: List[str]


@dataclass(frozen=True)
class LoadedPrecedenceRegistry:
    systems: List[str]
    rules: List[PrecedenceRule]
    stamp: PrecedenceRegistryStamp


_registry_cache: Optional[LoadedPrecedenceRegistry] = None


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "precedence_registry.yaml"


def _sorted_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(raw)
    systems = payload.get("systems", [])
    if isinstance(systems, list):
        payload["systems"] = sorted(str(s) for s in systems)
    rules = payload.get("rules", [])
    if isinstance(rules, list):
        payload["rules"] = sorted(
            rules,
            key=lambda r: str((r or {}).get("rule_id", "")),
        )
    return payload


def load_precedence_registry() -> LoadedPrecedenceRegistry:
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _registry_path()
    if not path.exists():
        raise FileNotFoundError(f"Precedence registry not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        raise ValueError("precedence_registry.yaml must parse to a top-level mapping")

    registry_version = str(raw.get("registry_version", "")).strip()
    if not registry_version:
        raise ValueError("precedence_registry.yaml must include registry_version")
    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("precedence_registry.yaml must include schema_version")

    systems_raw = raw.get("systems", [])
    if not isinstance(systems_raw, list) or not systems_raw:
        raise ValueError("precedence_registry.yaml systems must be a non-empty list")
    systems = sorted({str(s).strip() for s in systems_raw if str(s).strip()})
    if not systems:
        raise ValueError("precedence_registry.yaml systems must include valid system IDs")
    system_set: Set[str] = set(systems)

    rules_raw = raw.get("rules", [])
    if not isinstance(rules_raw, list) or not rules_raw:
        raise ValueError("precedence_registry.yaml rules must be a non-empty list")

    seen_rule_ids: Set[str] = set()
    rules: List[PrecedenceRule] = []
    for idx, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise ValueError(f"rules[{idx}] must be a mapping")
        rule_id = str(item.get("rule_id", "")).strip()
        if not rule_id:
            raise ValueError(f"rules[{idx}] missing rule_id")
        if rule_id in seen_rule_ids:
            raise ValueError(f"duplicate rule_id: {rule_id}")
        seen_rule_ids.add(rule_id)

        applies_to = item.get("applies_to")
        if not isinstance(applies_to, dict):
            raise ValueError(f"rule {rule_id}: applies_to must be a mapping")
        system_a = str(applies_to.get("system_a", "")).strip()
        system_b = str(applies_to.get("system_b", "")).strip()
        if not system_a or not system_b:
            raise ValueError(f"rule {rule_id}: applies_to must include system_a and system_b")
        if system_a not in system_set or system_b not in system_set:
            raise ValueError(f"rule {rule_id}: applies_to references unknown systems")
        if system_a == system_b:
            raise ValueError(f"rule {rule_id}: applies_to systems must differ")

        dominance = str(item.get("dominance", "")).strip()
        if dominance not in _ALLOWED_DOMINANCE:
            raise ValueError(f"rule {rule_id}: invalid dominance '{dominance}'")

        conditions = item.get("conditions", [])
        if not isinstance(conditions, list):
            raise ValueError(f"rule {rule_id}: conditions must be a list")
        conditions_clean = [str(c).strip() for c in conditions if str(c).strip()]

        tie_breakers = item.get("tie_breakers", [])
        if not isinstance(tie_breakers, list):
            raise ValueError(f"rule {rule_id}: tie_breakers must be a list")
        tie_breakers_clean = [str(t).strip() for t in tie_breakers if str(t).strip()]
        unknown_tie_breakers = [t for t in tie_breakers_clean if t not in _ALLOWED_TIE_BREAKERS]
        if unknown_tie_breakers:
            raise ValueError(f"rule {rule_id}: unknown tie_breakers {unknown_tie_breakers}")

        rules.append(
            PrecedenceRule(
                rule_id=rule_id,
                applies_to={"system_a": system_a, "system_b": system_b},
                dominance=dominance,
                conditions=sorted(set(conditions_clean)),
                tie_breakers=tie_breakers_clean,
            )
        )

    rules.sort(key=lambda r: r.rule_id)
    canonical_payload = _sorted_payload(raw)
    stamp = PrecedenceRegistryStamp(
        precedence_registry_version=registry_version,
        precedence_registry_hash=canonical_json_sha256(canonical_payload),
    )
    _registry_cache = LoadedPrecedenceRegistry(systems=systems, rules=rules, stamp=stamp)
    return _registry_cache
