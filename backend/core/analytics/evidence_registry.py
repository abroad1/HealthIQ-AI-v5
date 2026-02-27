"""
Sprint 16 - EvidenceRegistry loader and validator.

Loads evidence provenance from SSOT; produces deterministic stamp for replay.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from core.contracts.evidence_registry_v1 import (
    EVIDENCE_REGISTRY_V1_VERSION,
    EvidenceItem,
    EvidenceRegistryStamp,
    canonical_json_sha256,
)

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SOURCE_TYPES = {"guideline", "paper", "textbook", "expert_consensus", "internal_policy"}
_QUALITY_GRADES = {"high", "moderate", "low", "unknown"}


@dataclass(frozen=True)
class LoadedEvidenceRegistry:
    items: List[EvidenceItem]
    stamp: EvidenceRegistryStamp


_registry_cache: Optional[LoadedEvidenceRegistry] = None


def _evidence_registry_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "evidence_registry.yaml"


def _fixture_mode_enabled() -> bool:
    import os

    mode = os.getenv("HEALTHIQ_MODE", "").strip().lower()
    return mode in {"fixture", "fixtures"}


def _sorted_registry_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministically sort evidence_items by evidence_id."""
    payload = dict(raw)
    items = payload.get("evidence_items", [])
    if isinstance(items, list):
        payload["evidence_items"] = sorted(
            items,
            key=lambda x: str((x or {}).get("evidence_id", "")),
        )
    return payload


def _validate_date(value: str, field: str) -> None:
    if not _DATE_PATTERN.match(str(value or "")):
        raise ValueError(f"{field} must be YYYY-MM-DD format, got: {value!r}")


def _validate_item(item: Dict[str, Any], index: int) -> EvidenceItem:
    evidence_id = item.get("evidence_id")
    if not evidence_id or not str(evidence_id).strip():
        raise ValueError(f"evidence_items[{index}]: evidence_id is required")
    source_type = item.get("source_type")
    if source_type not in _SOURCE_TYPES:
        raise ValueError(
            f"evidence_items[{index}] source_type must be one of {sorted(_SOURCE_TYPES)}, got: {source_type!r}"
        )
    quality_grade = item.get("quality_grade")
    if quality_grade not in _QUALITY_GRADES:
        raise ValueError(
            f"evidence_items[{index}] quality_grade must be one of {sorted(_QUALITY_GRADES)}, got: {quality_grade!r}"
        )
    last_reviewed = item.get("last_reviewed")
    if not last_reviewed:
        raise ValueError(f"evidence_items[{index}]: last_reviewed is required")
    _validate_date(last_reviewed, f"evidence_items[{index}].last_reviewed")
    return EvidenceItem(**item)


def load_evidence_registry() -> LoadedEvidenceRegistry:
    """
    Load and validate EvidenceRegistry from SSOT YAML.

    Validates:
    - registry_version, schema_version exist
    - evidence_id uniqueness
    - required fields, enums, date format (YYYY-MM-DD)
    - deterministic sort by evidence_id
    - produces stamp with evidence_registry_version + evidence_registry_hash

    Fails loud in normal runtime; fixture-only soft-fail when HEALTHIQ_MODE=fixture|fixtures.
    """
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache

    path = _evidence_registry_path()
    if not path.exists():
        if _fixture_mode_enabled():
            stamp = EvidenceRegistryStamp(
                evidence_registry_version=EVIDENCE_REGISTRY_V1_VERSION,
                evidence_registry_hash="",
            )
            _registry_cache = LoadedEvidenceRegistry(items=[], stamp=stamp)
            return _registry_cache
        raise FileNotFoundError(f"Evidence registry not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if not isinstance(raw, dict):
        raise ValueError("evidence_registry.yaml must parse to a top-level mapping")

    registry_version = str(raw.get("registry_version", "")).strip()
    if not registry_version:
        raise ValueError("evidence_registry.yaml must include registry_version")

    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("evidence_registry.yaml must include schema_version")

    items_raw = raw.get("evidence_items", [])
    if not isinstance(items_raw, list):
        raise ValueError("evidence_registry.yaml 'evidence_items' must be a list")

    seen_ids: Set[str] = set()
    items: List[EvidenceItem] = []

    for i, item in enumerate(items_raw):
        if not isinstance(item, dict):
            raise ValueError(f"evidence_items[{i}] must be a mapping")
        parsed = _validate_item(item, i)
        if parsed.evidence_id in seen_ids:
            raise ValueError(f"duplicate evidence_id: {parsed.evidence_id}")
        seen_ids.add(parsed.evidence_id)
        items.append(parsed)

    items.sort(key=lambda x: x.evidence_id)
    canonical_payload = _sorted_registry_payload(raw)
    schema_hash = canonical_json_sha256(canonical_payload)
    stamp = EvidenceRegistryStamp(
        evidence_registry_version=registry_version or EVIDENCE_REGISTRY_V1_VERSION,
        evidence_registry_hash=schema_hash,
    )

    _registry_cache = LoadedEvidenceRegistry(items=items, stamp=stamp)
    return _registry_cache
