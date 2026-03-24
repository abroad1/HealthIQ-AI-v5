"""Load KB-S48a intervention-effects registry for runtime annotation (KB-S48e)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_intervention_effects_registry_v1() -> Tuple[Dict[str, Dict[str, Any]], str, str]:
    """
    Return (classes_by_intervention_class_id, registry_schema_version, registry_id).
    """
    path = _repo_root() / "knowledge_bus" / "interventions" / "intervention_effects_registry_v1.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    reg_ver = str(doc.get("registry_schema_version") or "")
    reg_id = str(doc.get("registry_id") or "")
    by_id: Dict[str, Dict[str, Any]] = {}
    for row in doc.get("intervention_classes") or []:
        if not isinstance(row, dict):
            continue
        cid = row.get("intervention_class_id")
        if isinstance(cid, str) and cid.strip():
            by_id[cid.strip()] = row
    return by_id, reg_ver, reg_id
