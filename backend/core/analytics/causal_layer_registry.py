"""
v5.3 Sprint 4 - SSOT loader/validator for CausalLayer_v1 rules.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.causal_layer_v1 import CAUSAL_LAYER_V1_VERSION, canonical_json_sha256

_ALLOWED_EDGE_TYPES = {"driver", "amplifier", "constraint"}


@dataclass(frozen=True)
class CausalLayerRegistryStamp:
    causal_layer_registry_version: str
    causal_layer_registry_hash: str


@dataclass(frozen=True)
class CausalLayerRule:
    edge_id: str
    from_system_id: str
    to_system_id: str
    edge_type: str
    priority: int
    conditions: List[str]
    rationale_codes: List[str]


@dataclass(frozen=True)
class LoadedCausalLayerRegistry:
    rules: List[CausalLayerRule]
    stamp: CausalLayerRegistryStamp


_registry_cache: Optional[LoadedCausalLayerRegistry] = None


def _fixture_mode_enabled() -> bool:
    return os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "causal_layer_registry.yaml"


def _sorted_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(raw)
    rules = payload.get("rules", [])
    if isinstance(rules, list):
        payload["rules"] = sorted(rules, key=lambda r: str((r or {}).get("edge_id", "")))
    return payload


def load_causal_layer_registry() -> LoadedCausalLayerRegistry:
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _registry_path()
    if not path.exists():
        if _fixture_mode_enabled():
            stamp = CausalLayerRegistryStamp(
                causal_layer_registry_version=CAUSAL_LAYER_V1_VERSION,
                causal_layer_registry_hash="",
            )
            _registry_cache = LoadedCausalLayerRegistry(rules=[], stamp=stamp)
            return _registry_cache
        raise FileNotFoundError(f"Causal layer registry not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        raise ValueError("causal_layer_registry.yaml must parse to a top-level mapping")

    registry_version = str(raw.get("registry_version", "")).strip()
    if not registry_version:
        raise ValueError("causal_layer_registry.yaml must include registry_version")
    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("causal_layer_registry.yaml must include schema_version")

    rules_raw = raw.get("rules", [])
    if not isinstance(rules_raw, list):
        raise ValueError("causal_layer_registry.yaml rules must be a list")

    seen_edge_ids: Set[str] = set()
    rules: List[CausalLayerRule] = []
    for idx, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise ValueError(f"rules[{idx}] must be a mapping")
        edge_id = str(item.get("edge_id", "")).strip()
        if not edge_id:
            raise ValueError(f"rules[{idx}] missing edge_id")
        if edge_id in seen_edge_ids:
            raise ValueError(f"duplicate edge_id: {edge_id}")
        seen_edge_ids.add(edge_id)

        from_system_id = str(item.get("from_system_id", "")).strip()
        to_system_id = str(item.get("to_system_id", "")).strip()
        if not from_system_id or not to_system_id:
            raise ValueError(f"rule {edge_id}: from_system_id and to_system_id are required")
        if from_system_id == to_system_id:
            raise ValueError(f"rule {edge_id}: from_system_id and to_system_id must differ")

        edge_type = str(item.get("edge_type", "")).strip()
        if edge_type not in _ALLOWED_EDGE_TYPES:
            raise ValueError(f"rule {edge_id}: invalid edge_type '{edge_type}'")

        priority_raw = item.get("priority")
        if not isinstance(priority_raw, int):
            raise ValueError(f"rule {edge_id}: priority must be int")

        conditions = item.get("conditions", [])
        if not isinstance(conditions, list):
            raise ValueError(f"rule {edge_id}: conditions must be a list")
        conditions_clean = [str(c).strip() for c in conditions if str(c).strip()]

        rationale_codes = item.get("rationale_codes", [])
        if not isinstance(rationale_codes, list):
            raise ValueError(f"rule {edge_id}: rationale_codes must be a list")
        rationale_clean = [str(c).strip() for c in rationale_codes if str(c).strip()]

        rules.append(
            CausalLayerRule(
                edge_id=edge_id,
                from_system_id=from_system_id,
                to_system_id=to_system_id,
                edge_type=edge_type,
                priority=priority_raw,
                conditions=sorted(set(conditions_clean)),
                rationale_codes=sorted(set(rationale_clean)),
            )
        )

    rules.sort(key=lambda r: r.edge_id)
    stamp = CausalLayerRegistryStamp(
        causal_layer_registry_version=registry_version,
        causal_layer_registry_hash=canonical_json_sha256(_sorted_payload(raw)),
    )
    _registry_cache = LoadedCausalLayerRegistry(rules=rules, stamp=stamp)
    return _registry_cache
