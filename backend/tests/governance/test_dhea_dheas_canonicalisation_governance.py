"""Governance tests for DHEA-DHEAS-CANONICALISATION-1 artefacts."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

MODEL = REPO_ROOT / "knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml"
BATCH2_REGISTER = REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"


def test_unit_aware_canonicalisation_model_exists_and_runtime_consumed():
    assert MODEL.is_file()
    payload = yaml.safe_load(MODEL.read_text(encoding="utf-8")) or {}
    assert payload.get("runtime_consumed") is True
    assert payload.get("dhea_low_activation_policy") == "DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT"


def test_dhea_s_high_package_activated_in_batch2_register():
    payload = yaml.safe_load(BATCH2_REGISTER.read_text(encoding="utf-8")) or {}
    activated = {row["package_id"] for row in payload.get("activated_packages") or []}
    inactive = {row["package_id"] for row in payload.get("kept_inactive_packages") or []}
    assert "pkg_kb47_dhea_high_androgen_excess_context" in activated
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" in inactive
