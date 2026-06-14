"""Governance tests for ARCH-COMPLETION-2 output authority artefacts."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

ARTIFACTS = {
    "authority_model": REPO_ROOT / "knowledge_bus/governance/compiled_output_authority_model_v1.yaml",
    "root_cause_register": REPO_ROOT / "knowledge_bus/governance/root_cause_authority_register_v1.yaml",
    "card_register": REPO_ROOT / "knowledge_bus/governance/card_authority_register_v1.yaml",
}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_all_output_authority_governance_artifacts_exist_and_runtime_consumed():
    for name, path in ARTIFACTS.items():
        assert path.is_file(), f"missing {name}"
        payload = _load(path)
        assert payload.get("runtime_consumed") is True, name


def test_authority_model_defines_required_element_types():
    model = _load(ARTIFACTS["authority_model"])
    types = {row["element_type"] for row in model.get("output_element_types") or []}
    assert "signal_card" in types
    assert "root_cause_card" in types
    assert "system_summary" in types
    forbidden = model.get("forbidden_compiler_inputs") or []
    assert "Batch_2_Pass_3.json" in forbidden


def test_root_cause_register_quarantines_why_fallback():
    reg = _load(ARTIFACTS["root_cause_register"])
    entries = reg.get("entries") or []
    fallback = next(e for e in entries if e.get("root_cause_id") == "why_engine_fallback_v1")
    assert fallback["activation_status"] == "ROOT_CAUSE_UNTRACEABLE_BLOCKED"


def test_root_cause_register_classifies_batch2_inactive_signals():
    reg = _load(ARTIFACTS["root_cause_register"])
    inactive = {row["signal_id"] for row in reg.get("batch2_inactive_signal_entries") or []}
    assert "signal_dhea_high" in inactive
    assert "signal_fai_low" in inactive


def test_card_register_quarantines_layer_c_and_layer3():
    reg = _load(ARTIFACTS["card_register"])
    statuses = {row.get("activation_status") for row in reg.get("entries") or []}
    assert "CARD_LEGACY_QUARANTINED" in statuses
    assert "CARD_GOVERNED_ACTIVE" in statuses
