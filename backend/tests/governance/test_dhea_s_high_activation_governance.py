"""Governance tests for DHEA-S-HIGH-ACTIVATION-1."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

BATCH2_REGISTER = REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
DHEA_HIGH_MANIFEST = (
    REPO_ROOT / "knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/package_manifest.yaml"
)
MEDICAL_AUTHORITY = (
    REPO_ROOT / "docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md"
)


def test_dhea_s_high_package_activated_in_batch2_register():
    payload = yaml.safe_load(BATCH2_REGISTER.read_text(encoding="utf-8")) or {}
    activated = {row["package_id"] for row in payload.get("activated_packages") or []}
    inactive = {row["package_id"] for row in payload.get("kept_inactive_packages") or []}
    assert "pkg_kb47_dhea_high_androgen_excess_context" in activated
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" in inactive
    assert payload.get("dhea_s_high_superseding_authority") == str(
        MEDICAL_AUTHORITY.relative_to(REPO_ROOT)
    ).replace("\\", "/")


def test_dhea_high_package_manifest_runtime_active():
    payload = yaml.safe_load(DHEA_HIGH_MANIFEST.read_text(encoding="utf-8")) or {}
    assert payload.get("behavioural_impact") == "SIGNAL_RUNTIME_ACTIVATION"
    assert payload.get("governance_runtime_activation_status") == "runtime_active_canonical"
    assert "DHEA-S_High_Activation_Medical_Research_Review.md" in str(
        payload.get("medical_research_authority") or ""
    )


def test_medical_authority_contains_activation_directives():
    text = MEDICAL_AUTHORITY.read_text(encoding="utf-8")
    assert "DHEA_S_HIGH_ACTIVATE_NOW" in text
    assert "standalone_signal_allowed: true" in text
    assert "corroboration_required: false" in text
