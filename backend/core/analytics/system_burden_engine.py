"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module B: direction-aware raw system burden.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import yaml

SYSTEM_BURDEN_ENGINE_VERSION = "1.0.0"
CALIBRATION_FACTOR = 1.0
# TODO (Sprint 14+): introduce tier-aware calibration multiplier

ALLOWED_RISK_DIRECTIONS = {"HIGH_IS_RISK", "LOW_IS_RISK", "BOTH_SIDES_RISK"}


def _biomarker_registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "system_burden_registry.yaml"


def load_burden_registry() -> Dict[str, Dict[str, Any]]:
    path = _biomarker_registry_path()
    if not path.exists():
        raise FileNotFoundError(f"system_burden_engine: biomarkers registry missing: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = payload.get("biomarkers", {})
    if not isinstance(rows, dict):
        raise ValueError("system_burden_engine: invalid biomarkers registry payload")
    out: Dict[str, Dict[str, Any]] = {}
    for biomarker_id in sorted(str(k) for k in rows.keys()):
        row = rows[biomarker_id]
        if not isinstance(row, dict):
            raise ValueError(f"system_burden_engine: invalid registry row for {biomarker_id}")
        out[biomarker_id] = row
    return out


def audit_risk_direction_registry(
    *,
    required_biomarkers: Sequence[str],
    registry_rows: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    missing: List[str] = []
    invalid: List[str] = []
    contextual: List[str] = []
    missing_weight: List[str] = []
    validated: Dict[str, Dict[str, Any]] = {}

    for biomarker_id in sorted(set(str(x) for x in required_biomarkers if str(x).strip())):
        row = registry_rows.get(biomarker_id)
        if not isinstance(row, Mapping):
            missing.append(biomarker_id)
            continue
        risk_direction = str(row.get("risk_direction", "")).strip()
        if not risk_direction:
            missing.append(biomarker_id)
            continue
        if risk_direction == "CONTEXTUAL":
            contextual.append(biomarker_id)
            continue
        if risk_direction not in ALLOWED_RISK_DIRECTIONS:
            invalid.append(f"{biomarker_id}:{risk_direction}")
            continue
        weight = row.get("weight")
        if not isinstance(weight, (int, float)):
            missing_weight.append(biomarker_id)
            continue
        validated[biomarker_id] = {
            "risk_direction": risk_direction,
            "weight": float(weight),
        }

    if missing or invalid or contextual or missing_weight:
        raise ValueError(
            "system_burden_engine: risk direction registry audit failed "
            f"(missing={missing}, invalid={invalid}, contextual={contextual}, missing_weight={missing_weight})"
        )
    return validated


def _component_from_direction(z_score: float, risk_direction: str) -> float:
    if risk_direction == "HIGH_IS_RISK":
        return max(0.0, float(z_score))
    if risk_direction == "LOW_IS_RISK":
        return max(0.0, -float(z_score))
    if risk_direction == "BOTH_SIDES_RISK":
        return abs(float(z_score))
    raise ValueError(f"system_burden_engine: unsupported risk_direction={risk_direction!r}")


def build_raw_system_burden_v1(
    *,
    system_to_biomarkers: Mapping[str, Sequence[str]],
    biomarker_stats: Mapping[str, Mapping[str, Any]],
    audited_registry: Mapping[str, Mapping[str, Any]],
) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for system_id in sorted(str(s) for s in system_to_biomarkers.keys()):
        burden = 0.0
        biomarker_ids = sorted(str(b) for b in system_to_biomarkers.get(system_id, []))
        for biomarker_id in biomarker_ids:
            if biomarker_id not in biomarker_stats:
                continue
            if biomarker_id not in audited_registry:
                raise ValueError(f"system_burden_engine: unaudited biomarker {biomarker_id}")
            z_score = biomarker_stats[biomarker_id].get("z_score")
            if not isinstance(z_score, (int, float)):
                raise ValueError(f"system_burden_engine: missing z_score for {biomarker_id}")
            risk_direction = str(audited_registry[biomarker_id]["risk_direction"])
            biomarker_weight = audited_registry[biomarker_id]["weight"]
            component = _component_from_direction(float(z_score), risk_direction)
            burden += component * float(biomarker_weight) * CALIBRATION_FACTOR
        out[system_id] = float(burden)
    return out
