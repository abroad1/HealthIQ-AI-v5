"""Unit tests for activation_key resolution (ARCH-RT-2)."""

from __future__ import annotations

from core.knowledge.signal_activation_identity_v1 import (
    build_activation_key,
    infer_source_spec_id,
)


def test_build_activation_key_format():
    assert build_activation_key(
        signal_id="signal_alt_high",
        source_spec_id="inv_alt_high_hepatocellular_injury",
    ) == "signal_alt_high::inv_alt_high_hepatocellular_injury"


def test_infer_source_spec_id_from_inv_yaml_path():
    spec = infer_source_spec_id(
        package_id="pkg_s24_alt_high_hepatocellular_injury",
        source_document="knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml",
    )
    assert spec == "inv_alt_high_hepatocellular_injury"


def test_infer_source_spec_id_from_kb52c_package_id():
    spec = infer_source_spec_id(
        package_id="pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern",
        source_document="knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json",
    )
    assert spec == "inv_alt_high_metabolic_steatotic_liver_pattern"
