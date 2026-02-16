"""
Sprint 10 - RelationshipRegistry loader and evaluator.

Deterministic, schema-driven relationship detection (pairwise only in v1).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import yaml
from core.analytics.ratio_registry import DERIVED_IDS

from core.contracts.relationship_registry_v1 import (
    RELATIONSHIP_REGISTRY_V1_VERSION,
    RelationshipDefinition,
    RelationshipDetection,
    RelationshipRegistryStamp,
    RelationshipRuleNode,
    canonical_json_sha256,
)


@dataclass(frozen=True)
class LoadedRelationshipRegistry:
    definitions: List[RelationshipDefinition]
    stamp: RelationshipRegistryStamp


_registry_cache: Optional[LoadedRelationshipRegistry] = None


def _relationships_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "relationships.yaml"


def _load_canonical_biomarkers() -> Set[str]:
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    if not ssot_path.exists():
        return set()
    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    biomarkers = data.get("biomarkers", {})
    if not isinstance(biomarkers, dict):
        return set()
    return set(biomarkers.keys())


def _load_derived_marker_ids() -> Set[str]:
    """Derived marker IDs from the central ratio system."""
    return set(DERIVED_IDS)


def _sorted_registry_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(raw)
    relationships = payload.get("relationships", [])
    if isinstance(relationships, list):
        payload["relationships"] = sorted(
            relationships,
            key=lambda r: str((r or {}).get("relationship_id", "")),
        )
    return payload


def _iter_rule_nodes(node: RelationshipRuleNode) -> Iterable[RelationshipRuleNode]:
    yield node
    for child in (node.all or []):
        yield from _iter_rule_nodes(child)
    for child in (node.any or []):
        yield from _iter_rule_nodes(child)


def _validate_definition_ids(
    defn: RelationshipDefinition,
    canonical_ids: Set[str],
    derived_ids: Set[str],
) -> None:
    unknown = set(defn.biomarkers) - canonical_ids
    if unknown:
        raise ValueError(
            f"relationship '{defn.relationship_id}' contains unknown biomarkers: {sorted(unknown)}"
        )
    for did in defn.uses_derived_markers or []:
        if did not in derived_ids:
            raise ValueError(
                f"relationship '{defn.relationship_id}' uses unknown derived marker '{did}'"
            )

    for node in _iter_rule_nodes(defn.logic):
        if node.biomarker and node.biomarker not in canonical_ids:
            raise ValueError(
                f"relationship '{defn.relationship_id}' rule references unknown biomarker '{node.biomarker}'"
            )
        if node.derived_marker and node.derived_marker not in derived_ids:
            raise ValueError(
                f"relationship '{defn.relationship_id}' rule references unknown derived marker '{node.derived_marker}'"
            )


def load_relationship_registry() -> LoadedRelationshipRegistry:
    """
    Load and validate RelationshipRegistry from SSOT YAML.

    Validates:
    - registry_version exists
    - relationship_id uniqueness
    - biomarkers length == 2
    - all biomarker IDs exist in canonical SSOT biomarker registry
    - deterministic schema hash from canonical JSON
    """
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _relationships_path()
    if not path.exists():
        raise FileNotFoundError(f"Relationship registry not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    registry_version = str(raw.get("registry_version", "")).strip()
    if not registry_version:
        raise ValueError("relationships.yaml must include registry_version")

    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("relationships.yaml must include schema_version")

    rel_items = raw.get("relationships", [])
    if not isinstance(rel_items, list):
        raise ValueError("relationships.yaml 'relationships' must be a list")

    seen_ids: Set[str] = set()
    canonical_ids = _load_canonical_biomarkers()
    derived_ids = _load_derived_marker_ids()
    definitions: List[RelationshipDefinition] = []

    for item in rel_items:
        if not isinstance(item, dict):
            raise ValueError("each relationship entry must be a mapping")
        definition = RelationshipDefinition(**item)
        if definition.relationship_id in seen_ids:
            raise ValueError(f"duplicate relationship_id: {definition.relationship_id}")
        seen_ids.add(definition.relationship_id)
        _validate_definition_ids(definition, canonical_ids, derived_ids)
        definitions.append(definition)

    definitions.sort(key=lambda d: d.relationship_id)
    canonical_payload = _sorted_registry_payload(raw)
    schema_hash = canonical_json_sha256(canonical_payload)
    stamp = RelationshipRegistryStamp(
        relationship_registry_version=registry_version or RELATIONSHIP_REGISTRY_V1_VERSION,
        relationship_registry_hash=schema_hash,
    )

    _registry_cache = LoadedRelationshipRegistry(definitions=definitions, stamp=stamp)
    return _registry_cache


def _condition_subject(
    node: RelationshipRuleNode,
    panel_view: Dict[str, Dict[str, Any]],
    derived_markers_view: Dict[str, Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if node.biomarker:
        return panel_view.get(node.biomarker)
    if node.derived_marker:
        return derived_markers_view.get(node.derived_marker)
    return None


def _eval_node(
    node: RelationshipRuleNode,
    panel_view: Dict[str, Dict[str, Any]],
    derived_markers_view: Dict[str, Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    if node.all is not None:
        evidence: List[str] = []
        for child in node.all:
            ok, ev = _eval_node(child, panel_view, derived_markers_view)
            if not ok:
                return False, []
            evidence.extend(ev)
        return True, sorted(set(evidence))

    if node.any is not None:
        evidence: List[str] = []
        matched = False
        for child in node.any:
            ok, ev = _eval_node(child, panel_view, derived_markers_view)
            if ok:
                matched = True
                evidence.extend(ev)
        return matched, (sorted(set(evidence)) if matched else [])

    subject = _condition_subject(node, panel_view, derived_markers_view)
    present_now = subject is not None
    status = "unknown" if subject is None else str(subject.get("status", "unknown"))
    score = None if subject is None else subject.get("score")

    checks: List[bool] = []
    if node.present is not None:
        checks.append(present_now is bool(node.present))
    if node.status_in is not None:
        checks.append(status in set(node.status_in))
    if node.score_gte is not None:
        checks.append(isinstance(score, (int, float)) and float(score) >= float(node.score_gte))

    passed = all(checks) if checks else False
    if passed and node.evidence_code:
        return True, [node.evidence_code]
    return passed, []


def evaluate_relationships(
    panel_view: Dict[str, Dict[str, Any]],
    derived_markers_view: Dict[str, Dict[str, Any]],
    registry: Optional[LoadedRelationshipRegistry] = None,
) -> List[RelationshipDetection]:
    """
    Evaluate relationship definitions against safe status/score views.

    Input views must only contain safe deterministic fields (status/score/presence).
    Output contains no raw numeric biomarker values.
    """
    reg = registry or load_relationship_registry()
    out: List[RelationshipDetection] = []

    for definition in reg.definitions:
        triggered, evidence = _eval_node(definition.logic, panel_view, derived_markers_view)
        out.append(
            RelationshipDetection(
                relationship_id=definition.relationship_id,
                version=definition.version,
                biomarkers=list(definition.biomarkers),
                classification_code=definition.classification_code,
                severity=definition.severity,
                triggered=bool(triggered),
                evidence=sorted(evidence),
            )
        )

    out.sort(key=lambda d: d.relationship_id)
    return out
