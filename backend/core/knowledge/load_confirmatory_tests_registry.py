"""
KB-S33 confirmatory tests registry loader.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _registry_path() -> Path:
    return _repo_root() / "knowledge_bus" / "registries" / "confirmatory_tests_v1.yaml"


@lru_cache(maxsize=1)
def load_confirmatory_tests_registry_v1() -> Dict[str, Any]:
    path = _registry_path()
    if not path.exists():
        raise FileNotFoundError(f"Confirmatory tests registry not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("schema_version") != "v1":
        raise ValueError(f"Invalid schema_version in {path}: expected 'v1'")
    tests = payload.get("tests")
    if not isinstance(tests, list):
        raise ValueError(f"Invalid tests list in {path}: expected list")

    by_id: Dict[str, Dict[str, Any]] = {}
    for row in tests:
        if not isinstance(row, dict):
            raise ValueError(f"Invalid test entry in {path}: expected object")
        test_id = str(row.get("test_id", "")).strip()
        display_name = str(row.get("display_name", "")).strip()
        rationale = str(row.get("rationale_template", "")).strip()
        if not test_id or not display_name or not rationale:
            raise ValueError(f"Invalid test entry in {path}: missing required test fields for test_id={test_id!r}")
        by_id[test_id] = row

    return {"path": str(path), "payload": payload, "tests_by_id": by_id}
