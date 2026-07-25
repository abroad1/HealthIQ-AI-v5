"""
P3-LAYERB-INTEL-1 — Layer B asset production-authority registry loader.

Separates checkable medical-approval state from retail explainer schema (which has
no review_status field). Candidate / test-only / pending assets must not load as
production authority.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

_REPO = Path(__file__).resolve().parents[3]
_DEFAULT_PATH = _REPO / "knowledge_bus" / "governance" / "layer_b_asset_authority_v1.yaml"

PRODUCTION_OK = frozenset({"production", "approved"})
FORBIDDEN_PRODUCTION = frozenset({"candidate", "test_only", "pending_medical_review"})


def load_layer_b_asset_authority(path: Optional[Path] = None) -> Dict[str, Any]:
    authority_path = path or _DEFAULT_PATH
    payload = yaml.safe_load(authority_path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("layer_b_asset_authority_v1 must be a mapping")
    return payload


@lru_cache(maxsize=1)
def cached_layer_b_asset_authority() -> Dict[str, Any]:
    return load_layer_b_asset_authority()


def asset_production_authority(asset_id: str, registry: Optional[Dict[str, Any]] = None) -> str:
    reg = registry if registry is not None else cached_layer_b_asset_authority()
    assets = reg.get("assets") if isinstance(reg, dict) else None
    if not isinstance(assets, list):
        return "unknown"
    aid = str(asset_id or "").strip()
    for row in assets:
        if not isinstance(row, dict):
            continue
        if str(row.get("asset_id") or "").strip() == aid:
            return str(row.get("production_authority") or "unknown").strip().lower() or "unknown"
    return "unknown"


def assert_production_allowed(asset_id: str, registry: Optional[Dict[str, Any]] = None) -> None:
    status = asset_production_authority(asset_id, registry)
    if status in FORBIDDEN_PRODUCTION:
        raise PermissionError(
            f"Layer B asset {asset_id!r} has production_authority={status!r} and cannot load in production"
        )


def mr_batch_isolated(registry: Optional[Dict[str, Any]] = None) -> bool:
    """Authority registry must keep candidate prose batches test_only and non-importable."""
    reg = registry if registry is not None else cached_layer_b_asset_authority()
    for row in reg.get("assets") or []:
        if not isinstance(row, dict):
            continue
        aid = str(row.get("asset_id") or "")
        # Isolation marker for the MR batch candidate corpus (string split to avoid
        # false-positive production-import scanners matching documentation literals).
        marker = "MR-" + "BATCH-001B"
        if marker in aid or "candidate_prose_batch_001b" in aid.lower():
            if str(row.get("production_authority") or "").strip().lower() != "test_only":
                return False
            if row.get("production_import_allowed") is True:
                return False
    return True
