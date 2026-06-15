"""Governance tests for DHEA-DHEAS-CANONICALISATION-1 artefacts (identity layer)."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

MODEL = REPO_ROOT / "knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml"


def test_unit_aware_canonicalisation_model_exists_and_not_runtime_consumed():
    assert MODEL.is_file()
    payload = yaml.safe_load(MODEL.read_text(encoding="utf-8")) or {}
    assert payload.get("runtime_consumed") is False
    assert payload.get("dhea_low_activation_policy") == "DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT"
