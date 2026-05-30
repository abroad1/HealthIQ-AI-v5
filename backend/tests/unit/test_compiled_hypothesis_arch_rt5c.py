"""ARCH-RT-5C — hypothesis runtime promotion, summary_template enforcement, legacy preservation."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.knowledge import load_root_cause_hypotheses as lrc
from core.knowledge.compiled_hypothesis import (
    PILOT_SIGNAL_ID,
    CompiledHypothesisRow,
    CompiledHypothesisValidationError,
    get_compiled_hypothesis_artefact,
    load_compiled_hypothesis_artefact,
    runtime_summary_for_hypothesis,
    validate_runtime_promoted_artefact,
)
from core.knowledge.compiled_hypothesis_registry_v1 import (
    is_runtime_promoted_compiled_signal,
    load_shadow_compiled_hypothesis,
)
from core.knowledge.launch_estate_v1 import resolve_compile_manifest_ref

_REPO = Path(__file__).resolve().parents[3]


def test_runtime_promoted_signal_gate():
    assert is_runtime_promoted_compiled_signal(PILOT_SIGNAL_ID)
    assert not is_runtime_promoted_compiled_signal("signal_homocysteine_high")


def test_manifest_resolves_for_pilot():
    artefact = get_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    assert resolve_compile_manifest_ref(artefact.compile_manifest_ref) is not None


def test_summary_template_required_fail_closed_when_promoted():
    row = CompiledHypothesisRow(
        hypothesis_id="test_hyp",
        rank=1,
        title="T",
        physiological_claim="Kidney conversion claim must not be runtime summary.",
        evidence_strength="strong",
        missing_data_policy="policy",
        evidence_for=(),
        evidence_against=(),
        contradiction_markers=(),
        caveats=(),
        confirmatory_tests=(),
        summary_template=None,
    )
    with pytest.raises(CompiledHypothesisValidationError):
        runtime_summary_for_hypothesis(row, promoted=True)


def test_shadow_path_may_use_physiological_claim_fallback():
    row = CompiledHypothesisRow(
        hypothesis_id="test_hyp",
        rank=1,
        title="T",
        physiological_claim="Shadow fallback claim text.",
        evidence_strength="strong",
        missing_data_policy="policy",
        evidence_for=(),
        evidence_against=(),
        contradiction_markers=(),
        caveats=(),
        confirmatory_tests=(),
        summary_template=None,
    )
    assert "Shadow fallback" in runtime_summary_for_hypothesis(row, promoted=False)


def test_pilot_artefact_passes_runtime_promotion_gate():
    artefact = get_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    validate_runtime_promoted_artefact(artefact)


def test_compile_root_cause_vitamin_d_uses_summary_template_not_physiological_claim():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": PILOT_SIGNAL_ID,
                "signal_state": "at_risk",
                "confidence": 0.75,
                "primary_metric": "vitamin_d",
            },
        ],
        biomarker_context={"vitamin_d": {"value": 32.0}},
        input_reference_ranges={"vitamin_d": {"min": 75.0, "max": 200.0}},
    )
    assert root is not None
    finding = next(f for f in root.findings if f.signal_id == PILOT_SIGNAL_ID)
    hyp = finding.hypotheses[0]
    assert "25-hydroxyvitamin D" in hyp.summary
    assert "kidneys" not in hyp.summary.lower()
    assert hyp.summary != hyp.title
    artefact = get_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    assert hyp.summary == runtime_summary_for_hypothesis(artefact.hypotheses[0], promoted=True)
    assert hyp.evidence_for
    assert all(item.item for item in hyp.evidence_for)


def test_non_pilot_homocysteine_path_unchanged():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "signal_state": "at_risk",
                "confidence": 0.7,
                "primary_metric": "homocysteine",
            },
        ],
        biomarker_context={"homocysteine": {"value": 18.0}},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    assert root is not None
    finding = next(f for f in root.findings if f.signal_id == "signal_homocysteine_high")
    assert finding.hypotheses


def test_legacy_yaml_still_loads_for_pilot():
    payload = lrc.load_vitamin_d_low_hypotheses_v1()
    assert payload["hypotheses"]
    assert payload["payload"]["schema_version"] == "v1"


def test_compiled_loader_rejects_legacy_semver():
    legacy_path = _REPO / "knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml"
    legacy = yaml.safe_load(legacy_path.read_text(encoding="utf-8"))
    with pytest.raises(CompiledHypothesisValidationError):
        from core.knowledge.compiled_hypothesis import validate_compiled_hypothesis_payload

        validate_compiled_hypothesis_payload(legacy, path=str(legacy_path))


def test_shadow_registry_still_available():
    shadow = load_shadow_compiled_hypothesis(PILOT_SIGNAL_ID)
    assert shadow is not None
    assert shadow["hypotheses"][0]["runtime_summary"]
    assert "25-hydroxyvitamin D" in shadow["hypotheses"][0]["runtime_summary"]
    load_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)


def test_multi_frame_promotion_blocked():
    artefact = get_compiled_hypothesis_artefact(PILOT_SIGNAL_ID)
    assert len(artefact.hypotheses) == 1
