"""
KB-S33 root-cause hypothesis asset loader.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import yaml

from core.knowledge.load_confirmatory_tests_registry import load_confirmatory_tests_registry_v1


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _hypothesis_path() -> Path:
    return _repo_root() / "knowledge_bus" / "root_cause" / "hypotheses" / "hcy_hypotheses_v1.yaml"


@lru_cache(maxsize=1)
def load_hcy_hypotheses_v1() -> Dict[str, Any]:
    path = _hypothesis_path()
    if not path.exists():
        raise FileNotFoundError(f"Root-cause hypotheses asset not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("schema_version") != "v1":
        raise ValueError(f"Invalid schema_version in {path}: expected 'v1'")

    hypotheses = payload.get("hypotheses")
    if not isinstance(hypotheses, list):
        raise ValueError(f"Invalid hypotheses list in {path}: expected list")

    registry = load_confirmatory_tests_registry_v1()
    test_ids = set(registry["tests_by_id"].keys())

    validated: List[Dict[str, Any]] = []
    for row in hypotheses:
        if not isinstance(row, dict):
            raise ValueError(f"Invalid hypothesis entry in {path}: expected object")
        hypothesis_id = str(row.get("hypothesis_id", "")).strip()
        title = str(row.get("title", "")).strip()
        summary_template = str(row.get("summary_template", "")).strip()
        if not hypothesis_id or not title or not summary_template:
            raise ValueError(f"Invalid hypothesis entry in {path}: missing required fields for hypothesis_id={hypothesis_id!r}")
        confirmatory_tests = row.get("confirmatory_tests")
        if not isinstance(confirmatory_tests, list):
            raise ValueError(f"Invalid hypothesis entry in {path}: confirmatory_tests must be list for hypothesis_id={hypothesis_id!r}")
        missing_refs = [tid for tid in confirmatory_tests if str(tid) not in test_ids]
        if missing_refs:
            raise ValueError(
                f"Invalid confirmatory_tests refs in {path} for hypothesis_id={hypothesis_id!r}: "
                f"unknown test_id(s): {', '.join(str(x) for x in missing_refs)}"
            )
        validated.append(row)

    return {"path": str(path), "payload": payload, "hypotheses": validated}
