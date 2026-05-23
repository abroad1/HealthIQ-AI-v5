"""
LC-S23B — Tier 1 biomarker SSOT metadata contract (documentation/authoring support only).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
BIOMARKERS_PATH = REPO_ROOT / "backend" / "ssot" / "biomarkers.yaml"

TIER1_BIOMARKER_IDS: FrozenSet[str] = frozenset(
    {
        "ldl_cholesterol",
        "hdl_cholesterol",
        "apob",
        "apoa1",
        "total_cholesterol",
        "triglycerides",
        "tsh",
        "free_t4",
        "ferritin",
        "transferrin",
        "crp",
        "egfr",
        "creatinine",
        "alt",
        "ast",
        "ggt",
        "alp",
        "homocysteine",
        "vitamin_b12",
        "folate",
        "hba1c",
    }
)

TIER2_CARRY_FORWARD: FrozenSet[str] = frozenset(
    {
        "glucose",
        "insulin",
        "cortisol",
        "creatine_kinase",
    }
)

REQUIRED_METADATA_FIELDS: Tuple[str, ...] = (
    "key_risks_when_high",
    "key_risks_when_low",
    "known_modifiers",
)

PROHIBITED_PLACEHOLDER_STRINGS: FrozenSet[str] = frozenset(
    {
        "tbd",
        "todo",
        "placeholder",
        "fixme",
        "lorem",
    }
)


class SsotTier1MetadataError(ValueError):
    pass


def load_biomarkers_ssot() -> Dict[str, Any]:
    payload = yaml.safe_load(BIOMARKERS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SsotTier1MetadataError("biomarkers.yaml must be a mapping")
    biomarkers = payload.get("biomarkers")
    if not isinstance(biomarkers, dict):
        raise SsotTier1MetadataError("biomarkers key missing")
    return biomarkers


def validate_tier1_metadata(biomarkers: Dict[str, Any] | None = None) -> List[str]:
    biomarkers = biomarkers if biomarkers is not None else load_biomarkers_ssot()
    failures: List[str] = []
    for biomarker_id in sorted(TIER1_BIOMARKER_IDS):
        if biomarker_id not in biomarkers:
            failures.append(f"missing_biomarker:{biomarker_id}")
            continue
        row = biomarkers[biomarker_id]
        if not isinstance(row, dict):
            failures.append(f"invalid_row:{biomarker_id}")
            continue
        high = row.get("key_risks_when_high")
        low = row.get("key_risks_when_low")
        modifiers = row.get("known_modifiers")
        if not isinstance(high, list) or not high:
            failures.append(f"empty_key_risks_when_high:{biomarker_id}")
        if not isinstance(low, list):
            failures.append(f"missing_key_risks_when_low_list:{biomarker_id}")
        if not isinstance(modifiers, list) or not modifiers:
            failures.append(f"empty_known_modifiers:{biomarker_id}")
        for field in ("key_risks_when_high", "key_risks_when_low", "known_modifiers"):
            values = row.get(field) or []
            if not isinstance(values, list):
                continue
            for item in values:
                text = str(item).strip().lower()
                if not text:
                    failures.append(f"blank_{field}:{biomarker_id}")
                elif text in PROHIBITED_PLACEHOLDER_STRINGS:
                    failures.append(f"placeholder_{field}:{biomarker_id}:{text}")
    return failures
