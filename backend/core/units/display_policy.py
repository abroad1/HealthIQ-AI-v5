"""
LC-S8D — Governed Layer C display unit policy loader.

Presentation-only: must not change Layer B scoring units or perform conversions.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

DISPLAY_POLICY_VERSION = "1.0.0"


@lru_cache(maxsize=1)
def load_display_unit_policy() -> Dict[str, Any]:
    path = Path(__file__).parent.parent.parent / "ssot" / "display_unit_policy.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Display unit policy not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_biomarker_display_policy(biomarker_id: str) -> Optional[Dict[str, Any]]:
    data = load_display_unit_policy()
    biomarkers = data.get("biomarkers") or {}
    entry = biomarkers.get(biomarker_id)
    return dict(entry) if isinstance(entry, dict) else None


def get_presentation_mode_config(
    biomarker_id: str, mode: str
) -> Optional[Dict[str, Any]]:
    entry = get_biomarker_display_policy(biomarker_id)
    if not entry:
        return None
    block = entry.get(mode)
    return dict(block) if isinstance(block, dict) else None


def build_display_policy_meta() -> Dict[str, Any]:
    data = load_display_unit_policy()
    return {
        "display_unit_policy_version": str(data.get("policy_version", DISPLAY_POLICY_VERSION)),
        "presentation_modes": data.get("presentation_modes") or {},
    }
