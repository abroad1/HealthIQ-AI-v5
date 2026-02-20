"""
v5.3 Sprint 7 - Arbitration registry loader/validator.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.arbitration_v1 import canonical_json_sha256

_ALLOWED_DOMINANCE = {"a_over_b", "b_over_a"}
_ALLOWED_EDGE_TYPES = {"driver", "amplifier", "constraint"}
_ALLOWED_DIRECTIONS = {"winner_to_loser", "loser_to_winner", "a_to_b", "b_to_a"}


@dataclass(frozen=True)
class ArbitrationRegistryStamp:
    arbitration_registry_version: str
    arbitration_registry_hash: str


@dataclass(frozen=True)
class DominanceRule:
    rule_id: str
    conflict_type: str
    dominance: str
    precedence_tier: int
    rationale_codes: List[str]


@dataclass(frozen=True)
class CausalEdgeRule:
    edge_rule_id: str
    conflict_type: str
    edge_type: str
    direction: str
    priority: int
    rationale_codes: List[str]


@dataclass(frozen=True)
class ArbitrationScoring:
    tie_breakers: List[str]


@dataclass(frozen=True)
class LoadedArbitrationRegistry:
    dominance_rules: List[DominanceRule]
    causal_edge_rules: List[CausalEdgeRule]
    scoring: ArbitrationScoring
    stamp: ArbitrationRegistryStamp


_registry_cache: Optional[LoadedArbitrationRegistry] = None


def _fixture_mode_enabled() -> bool:
    return os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}


def _registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "arbitration_registry.yaml"


def load_arbitration_registry() -> LoadedArbitrationRegistry:
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _registry_path()
    if not path.exists():
        if _fixture_mode_enabled():
            _registry_cache = LoadedArbitrationRegistry(
                dominance_rules=[],
                causal_edge_rules=[],
                scoring=ArbitrationScoring(tie_breakers=[]),
                stamp=ArbitrationRegistryStamp(arbitration_registry_version="1.0.0", arbitration_registry_hash=""),
            )
            return _registry_cache
        raise FileNotFoundError(f"Arbitration registry not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("arbitration_registry.yaml must be a mapping")
    version = str(raw.get("registry_version", "")).strip()
    schema = str(raw.get("schema_version", "")).strip()
    if not version or not schema:
        raise ValueError("arbitration_registry.yaml requires registry_version and schema_version")

    dominance_raw = raw.get("dominance_rules", [])
    edge_raw = raw.get("causal_edge_rules", [])
    scoring_raw = raw.get("arbitration_scoring", {})
    if not isinstance(dominance_raw, list) or not isinstance(edge_raw, list) or not isinstance(scoring_raw, dict):
        raise ValueError("arbitration registry sections have invalid types")

    seen_rules: Set[str] = set()
    dominance_rules: List[DominanceRule] = []
    for idx, item in enumerate(dominance_raw):
        if not isinstance(item, dict):
            raise ValueError(f"dominance_rules[{idx}] must be mapping")
        rule_id = str(item.get("rule_id", "")).strip()
        if not rule_id:
            raise ValueError(f"dominance_rules[{idx}] missing rule_id")
        if rule_id in seen_rules:
            raise ValueError(f"duplicate dominance rule_id: {rule_id}")
        seen_rules.add(rule_id)
        conflict_type = str(item.get("conflict_type", "")).strip()
        dominance = str(item.get("dominance", "")).strip()
        tier = item.get("precedence_tier")
        rationale_codes = item.get("rationale_codes", [])
        if not conflict_type:
            raise ValueError(f"dominance rule {rule_id} missing conflict_type")
        if dominance not in _ALLOWED_DOMINANCE:
            raise ValueError(f"dominance rule {rule_id} invalid dominance")
        if not isinstance(tier, int):
            raise ValueError(f"dominance rule {rule_id} precedence_tier must be int")
        if not isinstance(rationale_codes, list) or not all(isinstance(x, str) for x in rationale_codes):
            raise ValueError(f"dominance rule {rule_id} rationale_codes must be list[str]")
        dominance_rules.append(
            DominanceRule(
                rule_id=rule_id,
                conflict_type=conflict_type,
                dominance=dominance,
                precedence_tier=tier,
                rationale_codes=sorted(set(str(x).strip() for x in rationale_codes if str(x).strip())),
            )
        )

    seen_edge_rules: Set[str] = set()
    edge_rules: List[CausalEdgeRule] = []
    for idx, item in enumerate(edge_raw):
        if not isinstance(item, dict):
            raise ValueError(f"causal_edge_rules[{idx}] must be mapping")
        edge_rule_id = str(item.get("edge_rule_id", "")).strip()
        if not edge_rule_id:
            raise ValueError(f"causal_edge_rules[{idx}] missing edge_rule_id")
        if edge_rule_id in seen_edge_rules:
            raise ValueError(f"duplicate causal edge_rule_id: {edge_rule_id}")
        seen_edge_rules.add(edge_rule_id)
        conflict_type = str(item.get("conflict_type", "")).strip()
        edge_type = str(item.get("edge_type", "")).strip()
        direction = str(item.get("direction", "")).strip()
        priority = item.get("priority")
        rationale_codes = item.get("rationale_codes", [])
        if not conflict_type:
            raise ValueError(f"edge rule {edge_rule_id} missing conflict_type")
        if edge_type not in _ALLOWED_EDGE_TYPES:
            raise ValueError(f"edge rule {edge_rule_id} invalid edge_type")
        if direction not in _ALLOWED_DIRECTIONS:
            raise ValueError(f"edge rule {edge_rule_id} invalid direction")
        if not isinstance(priority, int):
            raise ValueError(f"edge rule {edge_rule_id} priority must be int")
        if not isinstance(rationale_codes, list) or not all(isinstance(x, str) for x in rationale_codes):
            raise ValueError(f"edge rule {edge_rule_id} rationale_codes must be list[str]")
        edge_rules.append(
            CausalEdgeRule(
                edge_rule_id=edge_rule_id,
                conflict_type=conflict_type,
                edge_type=edge_type,
                direction=direction,
                priority=priority,
                rationale_codes=sorted(set(str(x).strip() for x in rationale_codes if str(x).strip())),
            )
        )

    tie_breakers = scoring_raw.get("tie_breakers", [])
    if not isinstance(tie_breakers, list) or not all(isinstance(x, str) for x in tie_breakers):
        raise ValueError("arbitration_scoring.tie_breakers must be list[str]")
    scoring = ArbitrationScoring(tie_breakers=[str(x).strip() for x in tie_breakers if str(x).strip()])

    dominance_rules.sort(key=lambda r: (r.precedence_tier, r.rule_id))
    edge_rules.sort(key=lambda r: (-r.priority, r.edge_rule_id))
    canonical_payload: Dict[str, Any] = {
        "registry_version": version,
        "schema_version": schema,
        "dominance_rules": [
            {
                "rule_id": r.rule_id,
                "conflict_type": r.conflict_type,
                "dominance": r.dominance,
                "precedence_tier": r.precedence_tier,
                "rationale_codes": r.rationale_codes,
            }
            for r in dominance_rules
        ],
        "causal_edge_rules": [
            {
                "edge_rule_id": r.edge_rule_id,
                "conflict_type": r.conflict_type,
                "edge_type": r.edge_type,
                "direction": r.direction,
                "priority": r.priority,
                "rationale_codes": r.rationale_codes,
            }
            for r in edge_rules
        ],
        "arbitration_scoring": {"tie_breakers": scoring.tie_breakers},
    }
    stamp = ArbitrationRegistryStamp(
        arbitration_registry_version=version,
        arbitration_registry_hash=canonical_json_sha256(canonical_payload),
    )
    _registry_cache = LoadedArbitrationRegistry(
        dominance_rules=dominance_rules,
        causal_edge_rules=edge_rules,
        scoring=scoring,
        stamp=stamp,
    )
    return _registry_cache
