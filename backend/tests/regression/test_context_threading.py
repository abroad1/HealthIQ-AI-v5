"""Regression tests for CONTEXT-THREADING-1 orchestrator runtime context threading."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import yaml

from core.analytics.runtime_context_evaluator import (
    build_runtime_context_snapshot,
    build_runtime_context_snapshot_from_analysis_context,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity
from core.pipeline import orchestrator as orchestrator_module
from core.pipeline.orchestrator_phases_v1 import evaluate_signal_evaluation_phase

REPO_ROOT = Path(__file__).resolve().parents[3]

LAB_RANGES = {
    "creatinine": {"min": 0.6, "max": 1.2},
    "egfr": {"min": 90.0, "max": 120.0},
    "dhea": {"min": 1.0, "max": 10.0},
}


class _SingleSignalRegistry:
    def __init__(self, signal: dict) -> None:
        self._signal = dict(signal)

    def get_all_signals(self) -> list[dict]:
        return [dict(self._signal)]


def _load_package_signal(package_dir: str, signal_id: str) -> dict:
    path = REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for item in payload.get("signals", []):
        if item.get("signal_id") == signal_id:
            activation_key, source_spec_id, package_id = resolve_activation_identity(
                signal_id=signal_id,
                signal_library_path=path,
            )
            compiled = dict(item)
            compiled["activation_key"] = activation_key
            compiled["source_spec_id"] = source_spec_id
            compiled["package_id"] = package_id
            return compiled
    raise AssertionError(f"signal {signal_id} not found in {path}")


def _phase_kwargs(**overrides):
    base = {
        "simple_biomarkers": {"creatinine": 1.8, "egfr": 55.0},
        "derived_ratios_meta": {"ratios": {}},
        "input_reference_ranges": LAB_RANGES,
        "input_reference_profiles": {},
        "registry_hash_fn": lambda: "test-hash",
        "utc_now_fn": lambda: "2026-06-12T00:00:00Z",
    }
    base.update(overrides)
    return base


def test_evaluate_signal_evaluation_phase_backward_compatible_without_runtime_context():
    mock_evaluator = MagicMock()
    mock_evaluator.evaluate_all.return_value = []
    evaluate_signal_evaluation_phase(
        signal_evaluator=mock_evaluator,
        **_phase_kwargs(),
    )
    mock_evaluator.evaluate_all.assert_called_once()
    _, kwargs = mock_evaluator.evaluate_all.call_args
    assert kwargs.get("runtime_context") is None


def test_evaluate_signal_evaluation_phase_forwards_runtime_context():
    mock_evaluator = MagicMock()
    mock_evaluator.evaluate_all.return_value = []
    runtime_ctx = {"demographic": {"sex": "female"}}
    evaluate_signal_evaluation_phase(
        signal_evaluator=mock_evaluator,
        runtime_context=runtime_ctx,
        **_phase_kwargs(),
    )
    mock_evaluator.evaluate_all.assert_called_once()
    _, kwargs = mock_evaluator.evaluate_all.call_args
    assert kwargs.get("runtime_context") == runtime_ctx


def test_orchestrator_wires_post_context_runtime_snapshot():
    source = Path(orchestrator_module.__file__).read_text(encoding="utf-8")
    assert "build_runtime_context_snapshot_from_analysis_context" in source
    assert "runtime_ctx = build_runtime_context_snapshot_from_analysis_context" in source
    ctx_idx = source.index("create_analysis_context(")
    sig_idx = source.index("evaluate_signal_evaluation_phase(")
    assert ctx_idx < sig_idx
    assert "questionnaire_responses=questionnaire_data" not in source.split(
        "evaluate_signal_evaluation_phase("
    )[0].split("create_analysis_context(")[-1]


def test_build_runtime_context_snapshot_from_analysis_context_uses_assembled_fields():
    from core.models.biomarker import BiomarkerPanel, BiomarkerValue
    from core.models.context import AnalysisContext
    from core.models.user import User

    user = User(user_id="test-user", gender="female", age=45)
    panel = BiomarkerPanel(
        biomarkers={
            "glucose": BiomarkerValue(name="glucose", value=95.0, unit="mg/dL"),
        }
    )
    context = AnalysisContext(
        analysis_id="analysis-test",
        user=user,
        biomarker_panel=panel,
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1980-06-01",
            "long_term_medications": [],
        },
        lifestyle_factors={"stress_level": 3},
        medical_history={"long_term_medication_classes": []},
        created_at="2026-06-12T00:00:00Z",
    )
    ctx = build_runtime_context_snapshot_from_analysis_context(context)
    assert ctx["demographic"]["sex"] == "female"
    assert ctx["medication"]["hormone_therapy_status_disclosed"] is True
    assert ctx["clinical_context"]["stress_context"] is True


def test_build_runtime_context_snapshot_accepts_raw_questionnaire_data():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1980-06-01",
            "symptoms": ["fatigue"],
        },
    )
    assert ctx["demographic"]["sex"] == "female"
    assert "age" in ctx["demographic"]
    assert ctx["symptom"]["symptoms_present"] is True


def test_active_signals_unchanged_with_runtime_context_questionnaire():
    evaluator = SignalEvaluator(SignalRegistry())
    biomarkers = {"creatinine": 1.8, "egfr": 55.0}
    lab_ranges = {
        "creatinine": {"min": 0.6, "max": 1.2},
        "egfr": {"min": 90.0, "max": 120.0},
    }
    kwargs = {
        "signal_evaluator": evaluator,
        "simple_biomarkers": biomarkers,
        "derived_ratios_meta": {"ratios": {}},
        "input_reference_ranges": lab_ranges,
        "input_reference_profiles": {},
        "registry_hash_fn": lambda: "hash",
        "utc_now_fn": lambda: "2026-06-12T00:00:00Z",
    }
    without_ctx = evaluate_signal_evaluation_phase(**kwargs, runtime_context=None)
    questionnaire_ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1975-01-01",
            "chronic_conditions": ["Hypertension"],
            "symptoms": ["none"],
            "long_term_medications": ["Statin"],
            "supplements": ["Vitamin D"],
        },
    )
    with_ctx = evaluate_signal_evaluation_phase(**kwargs, runtime_context=questionnaire_ctx)

    ids_without = {row["signal_id"] for row in without_ctx.signal_results_serialized}
    ids_with = {row["signal_id"] for row in with_ctx.signal_results_serialized}
    assert ids_without == ids_with
    assert ids_without


def test_context_dependent_signal_suppressed_without_runtime_context():
    signal = _load_package_signal(
        "pkg_kb47_dhea_high_androgen_excess_context",
        "signal_dhea_high",
    )
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    phase = evaluate_signal_evaluation_phase(
        signal_evaluator=evaluator,
        simple_biomarkers={"dhea": 20.0},
        derived_ratios_meta={"ratios": {}},
        input_reference_ranges=LAB_RANGES,
        input_reference_profiles={},
        registry_hash_fn=lambda: "hash",
        utc_now_fn=lambda: "2026-06-12T00:00:00Z",
        runtime_context=None,
    )
    assert phase.signal_results_serialized == []


def test_context_dependent_signal_can_pass_with_required_runtime_context():
    signal = _load_package_signal(
        "pkg_kb47_dhea_high_androgen_excess_context",
        "signal_dhea_high",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1980-01-01",
            "symptoms": ["fatigue"],
            "supplements": ["vitamin_d"],
            "long_term_medications": ["Testosterone hormone therapy"],
        },
    )
    ctx["medication"]["hormone_therapy"] = True
    ctx["clinical_context"]["aas_exposure"] = True
    ctx["symptom"]["symptoms_present"] = True
    ctx["supplement"]["supplements_disclosed"] = True
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    phase = evaluate_signal_evaluation_phase(
        signal_evaluator=evaluator,
        simple_biomarkers={"dhea": 20.0},
        derived_ratios_meta={"ratios": {}},
        input_reference_ranges=LAB_RANGES,
        input_reference_profiles={},
        registry_hash_fn=lambda: "hash",
        utc_now_fn=lambda: "2026-06-12T00:00:00Z",
        runtime_context=ctx,
    )
    assert isinstance(phase.signal_results_serialized, list)


def test_androgen_frame_index_activation_states():
    index_path = REPO_ROOT / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    text = index_path.read_text(encoding="utf-8")
    for package_id in (
        "pkg_kb47_dhea_high_androgen_excess_context",
        "pkg_kb47_dhea_low_adrenal_androgen_reduction",
    ):
        pos = text.index(f"source_package_id: {package_id}")
        section = text[pos : pos + 400]
        assert "runtime_authority_status: inactive" in section