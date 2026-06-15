"""Governance tests for DHEA-DHEAS-CANONICALISATION-1 artefacts."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

MODEL = REPO_ROOT / "knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml"
BATCH2_REGISTER = REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
DHEA_HIGH_MANIFEST = (
    REPO_ROOT / "knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/package_manifest.yaml"
)


def test_unit_aware_canonicalisation_model_exists_and_not_runtime_consumed():
    assert MODEL.is_file()
    payload = yaml.safe_load(MODEL.read_text(encoding="utf-8")) or {}
    assert payload.get("runtime_consumed") is False
    assert payload.get("dhea_low_activation_policy") == "DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT"
    assert payload.get("dhea_s_high_activation_policy") == "KEEP_INACTIVE_PENDING_EXTERNAL_CLINICIAN_SIGNOFF"


def test_dhea_s_high_package_remains_inactive_in_batch2_register():
    payload = yaml.safe_load(BATCH2_REGISTER.read_text(encoding="utf-8")) or {}
    activated = {row["package_id"] for row in payload.get("activated_packages") or []}
    inactive = {row["package_id"] for row in payload.get("kept_inactive_packages") or []}
    assert "pkg_kb47_dhea_high_androgen_excess_context" not in activated
    assert "pkg_kb47_dhea_high_androgen_excess_context" in inactive
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" in inactive
    dhea_high = next(
        row for row in payload.get("kept_inactive_packages") or []
        if row.get("package_id") == "pkg_kb47_dhea_high_androgen_excess_context"
    )
    assert dhea_high.get("identity_remediation_status") == "IDENTITY_RESOLVED_PRIMARY_METRIC_DHEA_S"


def test_dhea_high_package_manifest_identity_resolved_but_inactive():
    payload = yaml.safe_load(DHEA_HIGH_MANIFEST.read_text(encoding="utf-8")) or {}
    assert payload.get("behavioural_impact") == "NONE"
    assert payload.get("identity_remediation_status") == "IDENTITY_RESOLVED_PRIMARY_METRIC_DHEA_S"
    assert payload.get("governance_runtime_activation_status") == "inactive_pending_external_clinician_signoff"
