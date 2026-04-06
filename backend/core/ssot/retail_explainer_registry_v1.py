"""
Load and validate `backend/ssot/retail_explainer_v1/registry.yaml`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml

from core.contracts.retail_explainer_v1 import (
    BiomarkerEducationalExplainerV1,
    RetailExplainerRegistryV1,
    SystemEducationalExplainerV1,
)


def _registry_path() -> Path:
    return Path(__file__).resolve().parents[2] / "ssot" / "retail_explainer_v1" / "registry.yaml"


def _validate_entry(marker: str, payload: dict, *, kind: str) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError(f"{kind} {marker!r}: must be a mapping")
    title = payload.get("title")
    body = payload.get("body")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{kind} {marker!r}: title must be non-empty string")
    if not isinstance(body, str) or not body.strip():
        raise ValueError(f"{kind} {marker!r}: body must be non-empty string")
    return {"title": title.strip(), "body": body.strip()}


def load_retail_explainer_registry_v1() -> RetailExplainerRegistryV1:
    path = _registry_path()
    if not path.exists():
        return RetailExplainerRegistryV1()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("retail explainer registry root must be a mapping")
    version = str(raw.get("registry_version", "1.0.0")).strip() or "1.0.0"
    biomarkers: dict[str, dict[str, str]] = {}
    systems: dict[str, dict[str, str]] = {}
    raw_biomarkers = raw.get("biomarkers") or {}
    if isinstance(raw_biomarkers, dict):
        for bid, entry in raw_biomarkers.items():
            key = str(bid).strip()
            if not key:
                continue
            biomarkers[key] = _validate_entry(key, entry, kind="biomarkers")
    raw_systems = raw.get("systems") or {}
    if isinstance(raw_systems, dict):
        for sid, entry in raw_systems.items():
            key = str(sid).strip()
            if not key:
                continue
            systems[key] = _validate_entry(key, entry, kind="systems")
    return RetailExplainerRegistryV1(registry_version=version, biomarkers=biomarkers, systems=systems)


@lru_cache
def cached_retail_explainer_registry_v1() -> RetailExplainerRegistryV1:
    return load_retail_explainer_registry_v1()


def biomarker_educational_explainer(
    biomarker_id: str, registry: Optional[RetailExplainerRegistryV1] = None
) -> Optional[BiomarkerEducationalExplainerV1]:
    reg = registry or cached_retail_explainer_registry_v1()
    row = reg.biomarkers.get(biomarker_id)
    if not row:
        return None
    return BiomarkerEducationalExplainerV1(
        biomarker_id=biomarker_id,
        title=row["title"],
        body=row["body"],
    )


def system_educational_explainer(
    system_key: str, registry: Optional[RetailExplainerRegistryV1] = None
) -> Optional[SystemEducationalExplainerV1]:
    reg = registry or cached_retail_explainer_registry_v1()
    row = reg.systems.get(system_key)
    if not row:
        return None
    return SystemEducationalExplainerV1(
        system_key=system_key,
        title=row["title"],
        body=row["body"],
    )


def cluster_schema_key_from_cluster_id(cluster_id: str) -> str:
    """Derive cluster SSOT system key from engine cluster_id `{system}_{n}_biomarkers`."""
    parts = cluster_id.split("_")
    if len(parts) >= 3 and parts[-1] == "biomarkers" and parts[-2].isdigit():
        return parts[0]
    return parts[0] if parts else cluster_id
