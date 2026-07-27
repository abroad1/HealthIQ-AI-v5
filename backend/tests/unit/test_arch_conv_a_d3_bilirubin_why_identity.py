"""ARCH-CONV-A D-3 — bilirubin WHY identity merge (non-medical)."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.knowledge.root_cause_registry_v1 import ROOT_CAUSE_TARGET_SPECS, get_root_cause_targets

REPO = Path(__file__).resolve().parents[3]
ALIAS_REGISTER = REPO / "knowledge_bus/governance/arch_conv_a_why_identity_alias_register_v1.yaml"


def test_bilirubin_high_removed_from_why_registry_after_d3():
    ids = {spec.signal_id for spec in ROOT_CAUSE_TARGET_SPECS}
    assert "signal_bilirubin_high" not in ids
    assert "signal_hyperbilirubinemia" in ids
    assert len(ROOT_CAUSE_TARGET_SPECS) == 40
    assert len(get_root_cause_targets()) == 40


def test_d3_alias_register_records_merge_to_one():
    payload = yaml.safe_load(ALIAS_REGISTER.read_text(encoding="utf-8"))
    entries = payload.get("entries") or []
    row = next(e for e in entries if e.get("retired_signal_id") == "signal_bilirubin_high")
    assert row["surviving_signal_id"] == "signal_hyperbilirubinemia"
    assert row["disposition"] == "MERGE_TO_ONE"
    assert row["medical_frame_approval"] == "NONE"
    assert row["why_registry_state"] == "REMOVED_FROM_ROOT_CAUSE_TARGET_SPECS"
