"""
Sprint 3 - Biomarker Criticality & Missing Data Logic.

System-aware criticality: required/important/optional per health system,
confidence penalties, deterministic evaluation. No LLM, no external calls.
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class CriticalityPolicy:
    """Loaded criticality policy from criticality.yaml."""

    version: str
    systems: Dict[str, Dict[str, List[str]]]  # system -> {required, important, optional}
    penalties: Dict[str, int]


_policy_cache: Optional[CriticalityPolicy] = None


def load_criticality_policy() -> CriticalityPolicy:
    """Load criticality policy from ssot/criticality.yaml. Cached."""
    global _policy_cache
    if _policy_cache is not None:
        return _policy_cache

    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "criticality.yaml"
    if not ssot_path.exists():
        _policy_cache = CriticalityPolicy(
            version="0.0.0",
            systems={},
            penalties={
                "required_missing": 25,
                "important_missing": 10,
                "optional_missing": 3,
                "max_penalty_per_system": 70,
            },
        )
        return _policy_cache

    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    systems = data.get("systems", {})
    penalties = data.get("penalties", {})
    _policy_cache = CriticalityPolicy(
        version=str(data.get("version", "1.0.0")),
        systems=systems,
        penalties={
            "required_missing": int(penalties.get("required_missing", 25)),
            "important_missing": int(penalties.get("important_missing", 10)),
            "optional_missing": int(penalties.get("optional_missing", 3)),
            "max_penalty_per_system": int(penalties.get("max_penalty_per_system", 70)),
        },
    )
    return _policy_cache


def evaluate_criticality(
    scoring_result: Dict[str, Any],
    available_biomarkers: Set[str],
) -> Dict[str, Any]:
    """
    Evaluate biomarker criticality: missing markers, penalties, system/overall confidence.

    Args:
        scoring_result: Dict with health_system_scores (system -> {biomarker_scores, ...})
        available_biomarkers: Set of canonical biomarker IDs present in input

    Returns:
        Dict with:
        - criticality_version
        - system_confidence: {system: score 0-100}
        - overall_confidence: 0-100
        - missing_markers: {system: [biomarker, ...]}
        - confidence_downgrades: [{system, tier, biomarker, penalty, reason}, ...]
    """
    policy = load_criticality_policy()
    health_systems = scoring_result.get("health_system_scores", {})
    req_pen = policy.penalties["required_missing"]
    imp_pen = policy.penalties["important_missing"]
    opt_pen = policy.penalties["optional_missing"]
    max_pen = policy.penalties["max_penalty_per_system"]

    system_confidence: Dict[str, float] = {}
    missing_markers: Dict[str, List[str]] = {}
    confidence_downgrades: List[Dict[str, Any]] = []

    systems_in_scoring = set(health_systems.keys())

    for system_name, system_def in policy.systems.items():
        required = system_def.get("required", [])
        important = system_def.get("important", [])
        optional = system_def.get("optional", [])

        missing_req = [b for b in required if b not in available_biomarkers]
        missing_imp = [b for b in important if b not in available_biomarkers]
        missing_opt = [b for b in optional if b not in available_biomarkers]

        all_missing = missing_req + missing_imp + missing_opt
        if all_missing:
            missing_markers[system_name] = all_missing

        penalty_sum = 0
        for b in missing_req:
            penalty_sum += req_pen
            confidence_downgrades.append({
                "system": system_name,
                "tier": "required",
                "biomarker": b,
                "penalty": req_pen,
                "reason": "Missing required biomarker",
            })
        for b in missing_imp:
            penalty_sum += imp_pen
            confidence_downgrades.append({
                "system": system_name,
                "tier": "important",
                "biomarker": b,
                "penalty": imp_pen,
                "reason": "Missing important biomarker",
            })
        for b in missing_opt:
            penalty_sum += opt_pen
            confidence_downgrades.append({
                "system": system_name,
                "tier": "optional",
                "biomarker": b,
                "penalty": opt_pen,
                "reason": "Missing optional biomarker",
            })

        penalty_sum = min(penalty_sum, max_pen)
        system_confidence[system_name] = max(100 - penalty_sum, 100 - max_pen)

    # Overall confidence: weighted by systems present in scoring
    if system_confidence:
        systems_present = [s for s in system_confidence if s in systems_in_scoring]
        if systems_present:
            total = sum(system_confidence[s] for s in systems_present)
            overall_confidence = total / len(systems_present)
        else:
            overall_confidence = sum(system_confidence.values()) / len(system_confidence)
        overall_confidence = round(overall_confidence, 1)
    else:
        overall_confidence = 100.0

    return {
        "criticality_version": policy.version,
        "system_confidence": system_confidence,
        "overall_confidence": float(overall_confidence),
        "missing_markers": missing_markers,
        "confidence_downgrades": confidence_downgrades,
    }
