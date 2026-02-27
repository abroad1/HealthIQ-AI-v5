"""
v5.3 Sprint 5 - Calibration registry loader/validator (SSOT-driven).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.calibration_layer_v1 import (
    CALIBRATION_LAYER_V1_VERSION,
    canonical_json_sha256,
)

_ALLOWED_PRIORITY_TIER = {"p0", "p1", "p2", "p3"}
_ALLOWED_URGENCY_BAND = {"urgent", "soon", "routine", "monitor"}
_ALLOWED_ACTION_INTENSITY = {"high", "medium", "low", "info"}
_ALLOWED_STABILITY_FLAG = {"stable", "unstable", "insufficient"}


@dataclass(frozen=True)
class CalibrationRegistryStamp:
    calibration_registry_version: str
    calibration_registry_hash: str


@dataclass(frozen=True)
class CalibrationRule:
    rule_id: str
    match: Dict[str, List[str]]
    outputs: Dict[str, Any]
    rank: int


@dataclass(frozen=True)
class LoadedCalibrationRegistry:
    rules: List[CalibrationRule]
    stamp: CalibrationRegistryStamp


_registry_cache: Optional[LoadedCalibrationRegistry] = None


def _fixture_mode_enabled() -> bool:
    return os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "calibration_registry.yaml"


def _sorted_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(raw)
    rules = payload.get("calibration_rules", [])
    if isinstance(rules, list):
        payload["calibration_rules"] = sorted(
            rules,
            key=lambda r: (
                int(((r or {}).get("precedence") or {}).get("rank", 10**9)),
                str((r or {}).get("rule_id", "")),
            ),
        )
    return payload


def _list_of_strings(value: Any, field_name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    out = [str(v).strip() for v in value if str(v).strip()]
    return sorted(set(out))


def load_calibration_registry() -> LoadedCalibrationRegistry:
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _registry_path()
    if not path.exists():
        if _fixture_mode_enabled():
            stamp = CalibrationRegistryStamp(
                calibration_registry_version=CALIBRATION_LAYER_V1_VERSION,
                calibration_registry_hash="",
            )
            _registry_cache = LoadedCalibrationRegistry(rules=[], stamp=stamp)
            return _registry_cache
        raise FileNotFoundError(f"Calibration registry not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        raise ValueError("calibration_registry.yaml must parse to a top-level mapping")

    registry_version = str(raw.get("registry_version", "")).strip()
    if not registry_version:
        raise ValueError("calibration_registry.yaml must include registry_version")
    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("calibration_registry.yaml must include schema_version")

    rules_raw = raw.get("calibration_rules", [])
    if not isinstance(rules_raw, list):
        raise ValueError("calibration_registry.yaml calibration_rules must be a list")

    seen_rule_ids: Set[str] = set()
    rules: List[CalibrationRule] = []
    for idx, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise ValueError(f"calibration_rules[{idx}] must be a mapping")
        rule_id = str(item.get("rule_id", "")).strip()
        if not rule_id:
            raise ValueError(f"calibration_rules[{idx}] missing rule_id")
        if rule_id in seen_rule_ids:
            raise ValueError(f"duplicate rule_id: {rule_id}")
        seen_rule_ids.add(rule_id)

        match_raw = item.get("match", {})
        if not isinstance(match_raw, dict):
            raise ValueError(f"rule {rule_id}: match must be a mapping")
        match = {
            "required_system_ids": _list_of_strings(match_raw.get("required_system_ids"), f"{rule_id}.match.required_system_ids"),
            "required_state_codes": _list_of_strings(match_raw.get("required_state_codes"), f"{rule_id}.match.required_state_codes"),
            "required_transition_codes": _list_of_strings(match_raw.get("required_transition_codes"), f"{rule_id}.match.required_transition_codes"),
            "required_precedence_codes": _list_of_strings(match_raw.get("required_precedence_codes"), f"{rule_id}.match.required_precedence_codes"),
            "required_causal_codes": _list_of_strings(match_raw.get("required_causal_codes"), f"{rule_id}.match.required_causal_codes"),
        }

        outputs_raw = item.get("outputs", {})
        if not isinstance(outputs_raw, dict):
            raise ValueError(f"rule {rule_id}: outputs must be a mapping")
        priority_tier = str(outputs_raw.get("priority_tier", "")).strip()
        urgency_band = str(outputs_raw.get("urgency_band", "")).strip()
        action_intensity = str(outputs_raw.get("action_intensity", "")).strip()
        stability_flag = str(outputs_raw.get("stability_flag", "")).strip()
        if priority_tier not in _ALLOWED_PRIORITY_TIER:
            raise ValueError(f"rule {rule_id}: invalid priority_tier '{priority_tier}'")
        if urgency_band not in _ALLOWED_URGENCY_BAND:
            raise ValueError(f"rule {rule_id}: invalid urgency_band '{urgency_band}'")
        if action_intensity not in _ALLOWED_ACTION_INTENSITY:
            raise ValueError(f"rule {rule_id}: invalid action_intensity '{action_intensity}'")
        if stability_flag not in _ALLOWED_STABILITY_FLAG:
            raise ValueError(f"rule {rule_id}: invalid stability_flag '{stability_flag}'")
        explanation_codes = _list_of_strings(outputs_raw.get("explanation_codes"), f"{rule_id}.outputs.explanation_codes")

        precedence_raw = item.get("precedence", {})
        if not isinstance(precedence_raw, dict):
            raise ValueError(f"rule {rule_id}: precedence must be a mapping")
        rank = precedence_raw.get("rank")
        if not isinstance(rank, int):
            raise ValueError(f"rule {rule_id}: precedence.rank must be int")

        rules.append(
            CalibrationRule(
                rule_id=rule_id,
                match=match,
                outputs={
                    "priority_tier": priority_tier,
                    "urgency_band": urgency_band,
                    "action_intensity": action_intensity,
                    "stability_flag": stability_flag,
                    "explanation_codes": explanation_codes,
                },
                rank=rank,
            )
        )

    rules.sort(key=lambda r: (r.rank, r.rule_id))
    stamp = CalibrationRegistryStamp(
        calibration_registry_version=registry_version,
        calibration_registry_hash=canonical_json_sha256(_sorted_payload(raw)),
    )
    _registry_cache = LoadedCalibrationRegistry(rules=rules, stamp=stamp)
    return _registry_cache
