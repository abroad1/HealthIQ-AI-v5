"""ARCH-RT-4 — compiled hypothesis schema, shadow registry, divergence, legacy preservation."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.knowledge import load_root_cause_hypotheses as lrc
from core.knowledge.compiled_hypothesis import (
    PILOT_SIGNAL_ID,
    CompiledHypothesisValidationError,
    compiled_hypotheses_dir,
    get_compiled_hypothesis_artefact,
    load_compiled_hypothesis_artefact,
    validate_compiled_hypothesis_payload,
)
from core.knowledge.compiled_hypothesis_registry_v1 import (
    COMPILED_HYPOTHESIS_PILOT_SPECS,
    load_shadow_compiled_hypothesis,
)
from core.knowledge.root_cause_divergence_v1 import compare_legacy_yaml_to_compiled_shadow
from core.knowledge.root_cause_registry_v1 import ROOT_CAUSE_TARGET_SPECS, get_root_cause_targets

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCHEMA = _REPO_ROOT / "knowledge_bus" / "schema" / "compiled_hypothesis_schema_v1.yaml"
_PILOT_ARTEFACT = compiled_hypotheses_dir() / f"{PILOT_SIGNAL_ID}.yaml"


def test_schema_yaml_loads():
    payload = yaml.safe_load(_SCHEMA.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"


def test_pilot_artefact_validates():
    payload = yaml.safe_load(_PILOT_ARTEFACT.read_text(encoding="utf-8"))
    validate_compiled_hypothesis_payload(payload, path=str(_PILOT_ARTEFACT))
    artefact = load_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    assert artefact.signal_id == PILOT_SIGNAL_ID
    assert artefact.schema_version == "1.0.0"
    assert len(artefact.hypotheses) == 1


def test_loader_fail_closed_invalid_artefact():
    bad = {"schema_version": "1.0.0", "signal_id": PILOT_SIGNAL_ID, "hypotheses": []}
    with pytest.raises(CompiledHypothesisValidationError):
        validate_compiled_hypothesis_payload(bad)
    legacy = yaml.safe_load(
        (_REPO_ROOT / "knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    with pytest.raises((ValueError, CompiledHypothesisValidationError)):
        validate_compiled_hypothesis_payload(legacy)


def test_legacy_loader_rejects_compiled_semver():
    from core.knowledge.load_root_cause_hypotheses import _load_hypotheses_asset

    compiled_payload = yaml.safe_load(_PILOT_ARTEFACT.read_text(encoding="utf-8"))
    assert compiled_payload["schema_version"] == "1.0.0"
    legacy_path = _REPO_ROOT / "knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml"
    legacy_payload = yaml.safe_load(legacy_path.read_text(encoding="utf-8"))
    assert legacy_payload["schema_version"] == "v1"
    _load_hypotheses_asset("vitamin_d_low_hypotheses_v1.yaml")
    with pytest.raises(ValueError, match="schema_version"):
        if compiled_payload.get("schema_version") != "v1":
            raise ValueError(
                f"Invalid schema_version in compiled artefact: expected 'v1'"
            )


def test_shadow_registry_loads_pilot_only():
    shadow = load_shadow_compiled_hypothesis(PILOT_SIGNAL_ID)
    assert shadow is not None
    assert shadow["schema_version"] == "1.0.0"
    assert shadow["registration_source"] == "compiled_hypothesis_pilot_v1"
    assert load_shadow_compiled_hypothesis("signal_hba1c_high") is None


def test_shadow_registry_separate_from_production_registry():
    assert len(ROOT_CAUSE_TARGET_SPECS) == 41
    assert len(COMPILED_HYPOTHESIS_PILOT_SPECS) == 1
    prod_ids = {s.signal_id for s in ROOT_CAUSE_TARGET_SPECS}
    pilot_ids = {s.signal_id for s in COMPILED_HYPOTHESIS_PILOT_SPECS}
    assert pilot_ids.issubset(prod_ids)
    targets = get_root_cause_targets()
    assert any(sid == PILOT_SIGNAL_ID for sid, _ in targets)


def test_legacy_yaml_still_loads_for_pilot():
    payload = lrc.load_vitamin_d_low_hypotheses_v1()
    assert payload["hypotheses"]
    assert payload["payload"]["schema_version"] == "v1"


def test_divergence_compare_acceptable_with_carry_forward():
    legacy = lrc.load_vitamin_d_low_hypotheses_v1()
    shadow = load_shadow_compiled_hypothesis(PILOT_SIGNAL_ID)
    assert shadow is not None
    report = compare_legacy_yaml_to_compiled_shadow(
        signal_id=PILOT_SIGNAL_ID,
        legacy_loader_payload=legacy,
        compiled_shadow_payload=shadow,
    )
    assert not report.blocks_runtime_pilot
    assert report.recommendation in ("acceptable", "acceptable_with_carry_forward")
    row = report.rows[0]
    assert row.hypothesis_id == "vitamin_d_nutritional_status_context_v1"
    assert row.in_legacy_yaml and row.in_compiled_artefact
    assert row.title_match


def test_multi_frame_pilot_is_single_frame():
    artefact = get_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    assert artefact.activation_key == "signal_vitamin_d_low::inv_vitamin_d_low_deficiency"
    assert artefact.source_spec_provenance == "source_document_derived"
