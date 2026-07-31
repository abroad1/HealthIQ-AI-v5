"""ARCH-CONV-E ALT package asset promotion guards.

These tests validate package content and deferral metadata only. They do not
activate packages or assert runtime medical behaviour.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
SOURCE_REL = (
    "knowledge_bus/research/investigation_specs/multi_llm_research/"
    "ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json"
)
SOURCE = ROOT / SOURCE_REL
SOURCE_HASH = "7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267"
SUPPORTING_PROVENANCE = {
    (
        "knowledge_bus/research/investigation_specs/multi_llm_research/"
        "ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_1.json"
    ): "057F13627A29DC5ED18CB5C56E80E440A05BA41406677E5D31F05D2D07C19F9E",
    (
        "knowledge_bus/research/investigation_specs/multi_llm_research/"
        "ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_2.json"
    ): "1A2285B3B36C379DF58C0E191CB8C119F52DCB71C5C1BFD9FD9D850C8D67960C",
}
PACKAGES_ROOT = ROOT / "knowledge_bus" / "packages"

SPEC_TO_PACKAGE = {
    "inv_alt_high_r_value_hepatocellular_biochemical_pattern":
        "pkg_kb52c_alt_high_hepatocellular_injury_pattern",
    "inv_alt_high_r_value_mixed_biochemical_pattern":
        "pkg_kb52c_alt_high_mixed_biochemical_pattern",
    "inv_alt_high_r_value_cholestatic_alp_predominant_context":
        "pkg_kb52c_alt_high_cholestatic_alp_predominant_context",
    "inv_alt_high_muscle_source_or_exertional_contribution":
        "pkg_kb52c_alt_high_muscle_source_or_exertional_pattern",
    "inv_alt_high_bilirubin_hys_law_severity_context":
        "pkg_kb52c_alt_high_bilirubin_severity_context",
    "inv_alt_high_metabolic_masld_context":
        "pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern",
}
R_VALUE_SPECS = {
    "inv_alt_high_r_value_hepatocellular_biochemical_pattern",
    "inv_alt_high_r_value_mixed_biochemical_pattern",
    "inv_alt_high_r_value_cholestatic_alp_predominant_context",
}


def _yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _source_specs() -> dict[str, dict]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    return {row["spec_id"]: row for row in payload}


def test_arch_conv_e_source_hash_and_package_set_are_exact() -> None:
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper() == SOURCE_HASH
    for path, expected_hash in SUPPORTING_PROVENANCE.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest().upper() == expected_hash
    assert set(_source_specs()) == set(SPEC_TO_PACKAGE)
    for package_id in SPEC_TO_PACKAGE.values():
        package_dir = PACKAGES_ROOT / package_id
        assert package_dir.is_dir()
        assert {
            "research_brief.yaml",
            "signal_library.yaml",
            "package_manifest.yaml",
            "promoted_signal_intelligence.yaml",
        } <= {path.name for path in package_dir.iterdir() if path.is_file()}


def test_arch_conv_e_lineage_and_signal_content_match_assigned_specs() -> None:
    specs = _source_specs()
    for spec_id, package_id in SPEC_TO_PACKAGE.items():
        spec = specs[spec_id]
        package_dir = PACKAGES_ROOT / package_id
        manifest = _yaml(package_dir / "package_manifest.yaml")
        library = _yaml(package_dir / "signal_library.yaml")
        psi = _yaml(package_dir / "promoted_signal_intelligence.yaml")
        signal = psi["signals"][0]

        assert manifest["package_id"] == package_id
        assert manifest["source_spec_id"] == spec_id
        assert manifest["source_document"] == SOURCE_REL
        assert manifest["source_document_hash"] == SOURCE_HASH
        assert manifest["activation_key"] == f"signal_alt_high::{spec_id}"
        assert manifest["behavioural_impact"] == "NONE"

        assert library["signals"][0]["signal_id"] == "signal_alt_high"
        assert signal["signal_id"] == spec["signal_id"]
        assert signal["supporting_markers"] == spec["supporting_markers"]
        assert signal["override_rules"] == spec["override_rules"]
        assert signal["confirmatory_test_refs"] == spec["confirmatory_tests"]
        assert signal["missing_data"]["policies"] == [
            hypothesis["missing_data"]["policy"] for hypothesis in spec["hypotheses"]
        ]


def test_arch_conv_e_r_value_packages_are_explicitly_deferred() -> None:
    for spec_id, package_id in SPEC_TO_PACKAGE.items():
        package_dir = PACKAGES_ROOT / package_id
        manifest = _yaml(package_dir / "package_manifest.yaml")
        library = _yaml(package_dir / "signal_library.yaml")
        derived = library["signals"][0]["dependencies"]["derived_metrics"]
        description = manifest["description"]

        if spec_id in R_VALUE_SPECS:
            assert derived == ["r_value_alt_alp"]
            assert "DEFERRED_WITH_EXPLICIT_REASON" in description
            assert "not runtime-promoted" in description
        else:
            assert "r_value_alt_alp" not in derived

        # The package validator's structural-ready output is not a runtime
        # promotion decision; no unsupported readiness field is embedded.
        assert "ready_for_implementation" not in manifest

    ratio_registry = (
        ROOT / "backend" / "core" / "analytics" / "ratio_registry.py"
    ).read_text(encoding="utf-8")
    assert "r_value_alt_alp" not in ratio_registry


def test_arch_conv_e_r_value_formula_contract_is_preserved_without_activation() -> None:
    specs = _source_specs()
    expected_threshold_notes = {
        "inv_alt_high_r_value_hepatocellular_biochemical_pattern": "R >= 5",
        "inv_alt_high_r_value_mixed_biochemical_pattern": "R > 2 and R < 5",
        "inv_alt_high_r_value_cholestatic_alp_predominant_context": "R <= 2",
    }
    for spec_id, threshold_text in expected_threshold_notes.items():
        spec = specs[spec_id]
        package_id = SPEC_TO_PACKAGE[spec_id]
        brief = _yaml(PACKAGES_ROOT / package_id / "research_brief.yaml")
        assert brief["derived_metrics"] == ["r_value_alt_alp"]
        assert threshold_text in spec["evidence"]["threshold_notes"]
        summary = brief["research_summary"]
        assert "(ALT / ALT ULN) / (ALP / ALP ULN)" in summary
        assert "contemporaneous same-sample pairing" in summary
        assert "fail closed if any input is absent" in summary


def test_arch_conv_e_collision_dependency_remains_unadjudicated() -> None:
    collision_model = _yaml(
        ROOT
        / "knowledge_bus"
        / "governance"
        / "signal_authority_collision_model_v1.yaml"
    )
    liver_axis = next(
        row
        for row in collision_model["authority_groups"]
        if row["authority_group_id"] == "liver_injury_axis"
    )
    assert liver_axis["primary_signal_family"] == "signal_alp_high"
    assert liver_axis["supporting_signal_families"] == ["signal_ggt_high"]
    assert "signal_alt_high" not in {
        liver_axis["primary_signal_family"],
        *liver_axis["supporting_signal_families"],
    }
