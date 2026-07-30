"""ARCH-CONV-PKG3 — per-activation_key WHY authority selection and retirement."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.knowledge.compiled_hypothesis import (
    get_compiled_hypothesis_artefact_for_activation_key,
    validate_runtime_promoted_artefact,
)
from core.knowledge.compiled_hypothesis_registry_v1 import is_runtime_promoted_compiled_signal
from core.knowledge.why_authority_v1 import (
    STATE_COMPILED_ACTIVE,
    STATE_REJECTED,
    authority_state_for,
    list_compiled_active_activation_keys,
    resolve_frame_why_authority,
)

_REPO = Path(__file__).resolve().parents[3]
METABOLIC = "signal_homocysteine_high::inv_homocysteine_high_metabolic"
BVIT = (
    "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment"
)


def test_register_has_nineteen_compiled_frames_and_rejects_metabolic():
    assert authority_state_for(METABOLIC) == STATE_REJECTED
    assert len(list_compiled_active_activation_keys()) == 19
    assert not (
        _REPO / "knowledge_bus/compiled/hypotheses/inv_homocysteine_high_metabolic.yaml"
    ).is_file()


def test_runtime_promoted_signal_set_remains_vitamin_d_only():
    assert is_runtime_promoted_compiled_signal("signal_vitamin_d_low")
    assert not is_runtime_promoted_compiled_signal("signal_homocysteine_high")


def test_compiled_active_artefacts_validate():
    for key in list_compiled_active_activation_keys():
        assert authority_state_for(key) == STATE_COMPILED_ACTIVE
        artefact = get_compiled_hypothesis_artefact_for_activation_key(key)
        validate_runtime_promoted_artefact(artefact)
        assert artefact.activation_key == key


def test_rejected_metabolic_emits_no_why_and_no_fallback():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": METABOLIC,
                "source_spec_id": "inv_homocysteine_high_metabolic",
                "signal_state": "suboptimal",
                "confidence": 0.95,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": 22.0},
        input_reference_ranges={},
    )
    assert root is None


def test_hcy_b_vitamin_uses_compiled_not_legacy():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": BVIT,
                "source_spec_id": "inv_homocysteine_high_b_vitamin_related_methylation_impairment",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": 18.0, "folate": 2.0},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    assert root is not None
    finding = next(f for f in root.findings if f.activation_key == BVIT)
    assert finding.authority_scope == "frame_specific"
    ids = {h.hypothesis_id for h in finding.hypotheses}
    assert "hyp_folate_related_hyperhomocysteinemia" in ids
    assert "hcy_inflammation_context_v1" not in ids


def test_vitamin_d_legacy_not_selected_at_runtime():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_vitamin_d_low",
                "activation_key": "signal_vitamin_d_low::inv_vitamin_d_low_deficiency",
                "source_spec_id": "inv_vitamin_d_low_deficiency",
                "signal_state": "at_risk",
                "confidence": 0.75,
                "primary_metric": "vitamin_d",
            }
        ],
        biomarker_context={"vitamin_d": {"value": 32.0}},
        input_reference_ranges={"vitamin_d": {"min": 75.0, "max": 200.0}},
    )
    assert root is not None
    finding = next(f for f in root.findings if f.signal_id == "signal_vitamin_d_low")
    assert finding.authority_scope == "frame_specific"
    assert "25-hydroxyvitamin D" in finding.hypotheses[0].summary
    assert "kidneys" not in finding.hypotheses[0].summary.lower()


def test_bare_multi_frame_signal_fail_closed():
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_homocysteine_high",
        activation_key="",
    )
    assert mode == "fail_closed"
    with pytest.raises(ValueError, match="fail-closed"):
        compile_root_cause_v1(
            signal_results=[
                {
                    "signal_id": "signal_homocysteine_high",
                    "signal_state": "at_risk",
                    "confidence": 0.7,
                    "primary_metric": "homocysteine",
                }
            ],
            biomarker_context={"homocysteine": {"value": 18.0}},
            input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
        )


def test_out_of_pilot_signal_still_legacy():
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_homocysteine_elevation_context",
        activation_key="",
    )
    assert mode == "legacy"
