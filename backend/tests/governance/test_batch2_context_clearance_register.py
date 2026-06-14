"""Governance tests for batch2_context_clearance_register_v1.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTER_PATH = REPO_ROOT / "knowledge_bus/governance/batch2_context_clearance_register_v1.yaml"
SEMANTICS_PATH = REPO_ROOT / "knowledge_bus/governance/runtime_context_semantics_model_v1.yaml"
FRAME_INDEX_PATH = REPO_ROOT / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"

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


def test_clearance_register_covers_all_nine_context_dependent_packages():
    reg = _load(REGISTER_PATH)
    packages = reg.get("packages") or []
    package_ids = {row["package_id"] for row in packages}
    assert len(packages) == 9
    assert ANDROGEN_PACKAGE_IDS.issubset(package_ids)
    assert "pkg_kb47_free_t3_low_low_t3_syndrome" in package_ids


def test_no_package_marked_activated():
    reg = _load(REGISTER_PATH)
    assert reg["runtime_activation_performed"] is False
    assert reg["activated_package_count"] == 0
    assert reg["activation_eligibility_summary"]["eligible_for_stop_gated_activation"] == 0
    for row in reg.get("packages") or []:
        assert row.get("activation_eligibility") is False
        assert row.get("current_runtime_authority_status") == "inactive"


def test_clearance_decisions_are_governed_enum_values():
    semantics = _load(SEMANTICS_PATH)
    allowed = set(semantics["supported_clearance_decisions"])
    reg = _load(REGISTER_PATH)
    for row in reg.get("packages") or []:
        assert row["clearance_decision"] in allowed


def test_androgen_packages_blocked_pending_clinical_signoff():
    reg = _load(REGISTER_PATH)
    androgen_rows = [r for r in reg["packages"] if r.get("group") == "androgen"]
    assert len(androgen_rows) == 8
    for row in androgen_rows:
        assert row["clearance_decision"] == "BLOCKED_PENDING_CLINICAL_SIGNOFF"
        assert row["clinical_signoff_status"] == "not_in_repo"


def test_ft3_low_deferred_after_disclosed_semantics_implementation():
    reg = _load(REGISTER_PATH)
    ft3 = next(r for r in reg["packages"] if r["package_id"] == "pkg_kb47_free_t3_low_low_t3_syndrome")
    assert ft3["clearance_decision"] == "DEFERRED_NON_LAUNCH_CRITICAL"
    assert ft3.get("metadata_remediation_status") == "disclosed_semantics_aligned"
    assert "enable_lower_bound_false" in (ft3.get("activation_layer_blockers") or [])


def test_frame_index_confirms_inactive_runtime_authority():
    index_text = FRAME_INDEX_PATH.read_text(encoding="utf-8")
    for package_id in ANDROGEN_PACKAGE_IDS | {"pkg_kb47_free_t3_low_low_t3_syndrome"}:
        pos = index_text.index(f"source_package_id: {package_id}")
        section = index_text[pos : pos + 550]
        assert "runtime_authority_status: inactive" in section


def test_minimum_coverage_decisions_recorded_on_clearance_register():
    reg = _load(REGISTER_PATH)
    androgen_rows = [r for r in reg["packages"] if r.get("group") == "androgen"]
    assert len(androgen_rows) == 8
    for row in androgen_rows:
        assert row["minimum_coverage_decision"] == "DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY"
    ft3 = next(r for r in reg["packages"] if r["package_id"] == "pkg_kb47_free_t3_low_low_t3_syndrome")
    assert ft3["minimum_coverage_decision"] == "EXCLUDE_FROM_MINIMUM_COVERAGE"
    summary = reg.get("minimum_coverage_summary") or {}
    assert summary.get("defer_pending_external_clinical_authority") == 8
    assert summary.get("exclude_from_minimum_coverage") == 1
