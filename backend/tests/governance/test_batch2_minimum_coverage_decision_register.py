"""Governance tests for batch2_minimum_coverage_decision_register_v1.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTER_PATH = REPO_ROOT / "knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml"
CLEARANCE_PATH = REPO_ROOT / "knowledge_bus/governance/batch2_context_clearance_register_v1.yaml"

ALLOWED_DECISIONS = {
    "ACTIVATE_WITH_GATES",
    "EXCLUDE_FROM_MINIMUM_COVERAGE",
    "DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY",
    "DO_NOT_ACTIVATE",
}

ANDROGEN_PACKAGE_IDS = {
    "pkg_kb47_dhea_high_androgen_excess_context",
    "pkg_kb47_dhea_low_adrenal_androgen_reduction",
    "pkg_kb47_fai_high_biochemical_hyperandrogenism",
    "pkg_kb47_fai_low_reduced_free_androgen_availability",
    "pkg_kb47_free_testosterone_high_androgen_excess_context",
    "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
    "pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction",
    "pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction",
}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_minimum_coverage_register_covers_nine_packages():
    reg = _load(REGISTER_PATH)
    packages = reg.get("packages") or []
    package_ids = {row["package_id"] for row in packages}
    assert len(packages) == 9
    assert ANDROGEN_PACKAGE_IDS.issubset(package_ids)
    assert "pkg_kb47_free_t3_low_low_t3_syndrome" in package_ids


def test_no_activation_without_approval():
    reg = _load(REGISTER_PATH)
    assert reg["runtime_activation_performed"] is False
    assert reg["activated_package_count"] == 0
    assert reg["human_stop_gate"]["approval_received"] is False
    assert reg["decision_summary"]["activate_with_gates"] == 0
    for row in reg.get("packages") or []:
        assert row.get("stop_gate_passed") is False
        assert row["minimum_coverage_decision"] != "ACTIVATE_WITH_GATES"


def test_androgen_packages_deferred_pending_external_clinical_authority():
    reg = _load(REGISTER_PATH)
    androgen_rows = [r for r in reg["packages"] if r.get("group") == "androgen"]
    assert len(androgen_rows) == 8
    for row in androgen_rows:
        assert row["minimum_coverage_decision"] == "DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY"
        assert row["clinical_authority_present"] is False


def test_ft3_low_excluded_from_minimum_coverage():
    reg = _load(REGISTER_PATH)
    ft3 = next(r for r in reg["packages"] if r["package_id"] == "pkg_kb47_free_t3_low_low_t3_syndrome")
    assert ft3["minimum_coverage_decision"] == "EXCLUDE_FROM_MINIMUM_COVERAGE"
    assert ft3["enable_lower_bound"] is False
    assert "enable_lower_bound_false" in (ft3.get("activation_layer_blockers") or [])


def test_decisions_use_allowed_enum_values():
    reg = _load(REGISTER_PATH)
    for row in reg.get("packages") or []:
        assert row["minimum_coverage_decision"] in ALLOWED_DECISIONS


def test_clearance_register_aligns_with_minimum_coverage_decisions():
    clearance = _load(CLEARANCE_PATH)
    minimum = _load(REGISTER_PATH)
    clearance_by_id = {row["package_id"]: row for row in clearance.get("packages") or []}
    for row in minimum.get("packages") or []:
        package_id = row["package_id"]
        assert clearance_by_id[package_id]["minimum_coverage_decision"] == row["minimum_coverage_decision"]


def test_cf_batch2_010_remains_unresolved():
    reg = _load(REGISTER_PATH)
    assert reg["cf_batch2_010_status"] == "Open"
    assert reg["cf_batch2_010_resolved"] is False
