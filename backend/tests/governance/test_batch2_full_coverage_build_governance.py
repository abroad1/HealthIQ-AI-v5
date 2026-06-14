"""Governance tests for BATCH2-FULL-COVERAGE-BUILD-1 new governance artefacts."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

ARTIFACTS = {
    "primitive_model": REPO_ROOT
    / "knowledge_bus/governance/reusable_runtime_context_primitive_model_v1.yaml",
    "questionnaire_contract": REPO_ROOT
    / "knowledge_bus/governance/context_questionnaire_contract_v1.yaml",
    "readiness_register": REPO_ROOT
    / "knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml",
    "research_intake": REPO_ROOT
    / "knowledge_bus/governance/batch2_medical_research_intake_contract_v1.yaml",
}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_all_new_governance_artifacts_exist_and_are_not_runtime_consumed():
    for name, path in ARTIFACTS.items():
        assert path.is_file(), f"missing {name}: {path}"
        payload = _load(path)
        assert payload.get("runtime_consumed") is False, name


def test_primitive_model_defines_disclosure_states():
    model = _load(ARTIFACTS["primitive_model"])
    states = set(model.get("supported_disclosure_states") or [])
    assert {"answered_yes", "answered_no", "not_answered"}.issubset(states)
    primitives = model.get("primitives") or []
    assert len(primitives) >= 10


def test_questionnaire_contract_maps_ft3_and_androgen_fields():
    contract = _load(ARTIFACTS["questionnaire_contract"])
    assert contract.get("ft3_low_required_fields")
    assert contract.get("androgen_required_fields")
    field_names = {row["field_name"] for row in contract.get("fields") or []}
    assert "long_term_medications" in field_names
    assert "supplements" in field_names
    assert "chronic_conditions" in field_names


def test_readiness_register_covers_nine_packages_without_unauthorised_activation():
    reg = _load(ARTIFACTS["readiness_register"])
    exec_reg_path = REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
    exec_reg = _load(exec_reg_path)
    packages = reg.get("packages") or []
    assert len(packages) == 9
    assert exec_reg["runtime_activation_performed"] is True
    assert exec_reg["activated_package_count"] == 4
    activated_ids = {row["package_id"] for row in exec_reg.get("activated_packages") or []}
    for row in packages:
        if row["package_id"] in activated_ids:
            assert row.get("current_activation_state") == "runtime_active_canonical"
        else:
            assert row["activation_blocker_status"] != "ACTIVATION_READY_PENDING_APPROVAL"


def test_research_intake_contract_covers_ft3_and_androgen_patterns():
    intake = _load(ARTIFACTS["research_intake"])
    patterns = intake.get("patterns") or []
    pattern_ids = {row["pattern_id"] for row in patterns}
    assert "ft3_low_low_t3_syndrome" in pattern_ids
    androgen_rows = [row for row in patterns if row.get("group") == "androgen"]
    assert len(androgen_rows) == 8
    assert intake.get("androgen_shared_research_requirements", {}).get(
        "external_clinician_review_required"
    ) is True
