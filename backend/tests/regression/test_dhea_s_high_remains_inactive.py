"""Regression tests proving DHEA-S high remains inactive after identity remediation."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.canonical.alias_registry_service import get_alias_registry_service
from core.canonical.normalize import normalize_biomarkers_with_metadata

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_dhea_high_and_dhea_low_packages_not_in_activated_register():
    register = yaml.safe_load(
        (
            REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
        ).read_text(encoding="utf-8")
    )
    activated = {row["package_id"] for row in register.get("activated_packages") or []}
    inactive = {row["package_id"] for row in register.get("kept_inactive_packages") or []}
    assert "pkg_kb47_dhea_high_androgen_excess_context" not in activated
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" not in activated
    assert "pkg_kb47_dhea_high_androgen_excess_context" in inactive
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" in inactive


def test_ambiguous_dhea_canonicalises_to_dhea_s_without_implying_runtime_activation():
    get_alias_registry_service.cache_clear()
    entry = {
        "value": 20.0,
        "unit": "umol/L",
        "reference_range": {"min": 0.94, "max": 15.44, "unit": "umol/L", "source": "lab"},
    }
    result = normalize_biomarkers_with_metadata({"DHEA (Venous)": entry})
    assert "dhea_s" in result
    assert result["dhea_s"]["identity_confidence"] == "HIGH_CONFIDENCE_UNIT_RANGE_MATCH"
    get_alias_registry_service.cache_clear()
