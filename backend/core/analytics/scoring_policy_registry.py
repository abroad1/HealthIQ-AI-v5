"""
Sprint 13 - Scoring policy SSOT loader/validator/stamp.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import yaml


@dataclass(frozen=True)
class ScoringPolicyStamp:
    scoring_policy_version: str
    scoring_policy_hash: str


@dataclass(frozen=True)
class LoadedScoringPolicy:
    raw: Dict[str, Any]
    stamp: ScoringPolicyStamp


_policy_cache: Optional[LoadedScoringPolicy] = None


def _policy_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "scoring_policy.yaml"


def _canonical_json_sha256(obj: object) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _validate_range_dict(name: str, value: Mapping[str, Any]) -> None:
    min_val = value.get("min")
    max_val = value.get("max")
    if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
        raise ValueError(f"{name} range must include numeric min/max")
    if float(min_val) >= float(max_val):
        raise ValueError(f"{name} range min must be < max")


def _validate_policy(raw: Dict[str, Any]) -> None:
    policy_version = str(raw.get("policy_version", "")).strip()
    if not policy_version:
        raise ValueError("scoring_policy.yaml must include policy_version")
    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("scoring_policy.yaml must include schema_version")

    systems = raw.get("systems")
    if not isinstance(systems, dict) or not systems:
        raise ValueError("scoring_policy.yaml must include systems mapping")
    biomarkers = raw.get("biomarkers")
    if not isinstance(biomarkers, dict) or not biomarkers:
        raise ValueError("scoring_policy.yaml must include biomarkers mapping")

    for biomarker_id, policy in biomarkers.items():
        if not isinstance(policy, dict):
            raise ValueError(f"Biomarker policy must be mapping: {biomarker_id}")
        if not isinstance(policy.get("weight"), (int, float)):
            raise ValueError(f"Biomarker weight must be numeric: {biomarker_id}")
        if policy.get("scoring_type") != "range_position":
            raise ValueError(f"Unsupported scoring_type for {biomarker_id}")
        bands = policy.get("bands")
        if not isinstance(bands, dict):
            raise ValueError(f"Bands must be mapping: {biomarker_id}")
        for band_name in ["optimal", "normal", "borderline", "high", "very_high", "critical"]:
            band = bands.get(band_name)
            if not isinstance(band, dict):
                raise ValueError(f"Missing band '{band_name}' for {biomarker_id}")
            _validate_range_dict(f"{biomarker_id}.{band_name}", band)

    for system_name, system in systems.items():
        if not isinstance(system, dict):
            raise ValueError(f"System policy must be mapping: {system_name}")
        if not isinstance(system.get("min_biomarkers_required"), int):
            raise ValueError(f"min_biomarkers_required must be int: {system_name}")
        if not isinstance(system.get("system_weight"), (int, float)):
            raise ValueError(f"system_weight must be numeric: {system_name}")
        biomarker_ids = system.get("biomarkers")
        if not isinstance(biomarker_ids, list):
            raise ValueError(f"biomarkers list missing for system: {system_name}")
        for biomarker_id in biomarker_ids:
            if biomarker_id not in biomarkers:
                raise ValueError(
                    f"System '{system_name}' references unknown biomarker '{biomarker_id}'"
                )

    execution_order = raw.get("system_execution_order")
    if execution_order is not None:
        if not isinstance(execution_order, list) or not execution_order:
            raise ValueError("system_execution_order must be a non-empty list when provided")
        seen = set()
        for system_name in execution_order:
            if not isinstance(system_name, str) or not system_name.strip():
                raise ValueError("system_execution_order entries must be non-empty strings")
            if system_name in seen:
                raise ValueError(f"system_execution_order contains duplicate '{system_name}'")
            if system_name not in systems:
                raise ValueError(
                    f"system_execution_order references unknown system '{system_name}'"
                )
            seen.add(system_name)
        missing = sorted(set(systems.keys()) - set(execution_order))
        if missing:
            raise ValueError(
                "system_execution_order must include all systems; missing "
                f"{missing}"
            )

    derived_ratio_policy_bounds = raw.get("derived_ratio_policy_bounds", {})
    if not isinstance(derived_ratio_policy_bounds, dict):
        raise ValueError("derived_ratio_policy_bounds must be a mapping")
    for ratio_id, bounds in derived_ratio_policy_bounds.items():
        if not isinstance(bounds, dict):
            raise ValueError(f"derived_ratio_policy_bounds['{ratio_id}'] must be mapping")
        _validate_range_dict(f"derived_ratio_policy_bounds.{ratio_id}", bounds)
        unit = str(bounds.get("unit", "")).strip()
        if not unit:
            raise ValueError(f"derived_ratio_policy_bounds['{ratio_id}'] must include unit")
        source = str(bounds.get("source", "")).strip()
        if source != "healthiq_policy":
            raise ValueError(
                f"derived_ratio_policy_bounds['{ratio_id}'] source must be 'healthiq_policy'"
            )
        notes = str(bounds.get("notes", "")).strip()
        if not notes:
            raise ValueError(f"derived_ratio_policy_bounds['{ratio_id}'] must include notes")

    if not isinstance(raw.get("status_map"), dict) or not raw.get("status_map"):
        raise ValueError("status_map must be a non-empty mapping")
    if not isinstance(raw.get("score_curve"), dict) or not raw.get("score_curve"):
        raise ValueError("score_curve must be a non-empty mapping")
    scoring_runtime = raw.get("scoring_runtime", {})
    if scoring_runtime:
        if not isinstance(scoring_runtime, dict):
            raise ValueError("scoring_runtime must be a mapping")
        reason = str(scoring_runtime.get("unscored_reason_missing_lab_reference_range", "")).strip()
        if not reason:
            raise ValueError(
                "scoring_runtime.unscored_reason_missing_lab_reference_range must be a non-empty string"
            )


def load_scoring_policy() -> LoadedScoringPolicy:
    global _policy_cache
    if _policy_cache is not None:
        return _policy_cache

    path = _policy_path()
    if not path.exists():
        raise FileNotFoundError(f"Scoring policy not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        raise ValueError("scoring_policy.yaml must parse to a top-level mapping")

    _validate_policy(raw)
    stamp = ScoringPolicyStamp(
        scoring_policy_version=str(raw.get("policy_version", "")),
        scoring_policy_hash=_canonical_json_sha256(raw),
    )
    _policy_cache = LoadedScoringPolicy(raw=raw, stamp=stamp)
    return _policy_cache
