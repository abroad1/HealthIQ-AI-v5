"""Regression tests for CONTEXT-RUNTIME-1 reusable runtime context evaluation."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.runtime_context_evaluator import (
    RuntimeContextModelError,
    build_runtime_context_snapshot,
    evaluate_runtime_context_requirements,
    load_runtime_context_requirements_model,
    passes_runtime_context_requirements,
    validate_runtime_context_requirements_model,
)
from core.analytics.signal_evaluator import SignalEvaluator
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

THYROID_LAB_RANGES = {
    "free_t3": {"min": 2.0, "max": 4.4},
    "free_t4": {"min": 0.8, "max": 1.8},
    "tsh": {"min": 0.4, "max": 4.5},
}

ANDROGEN_LAB_RANGES = {
    "dhea": {"min": 1.0, "max": 10.0},
    "testosterone": {"min": 8.0, "max": 30.0},
    "shbg": {"min": 15.0, "max": 50.0},
    "free_testosterone": {"min": 5.0, "max": 25.0},
    "lh": {"min": 1.0, "max": 10.0},
    "fai": {"min": 20.0, "max": 70.0},
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


def _evaluate_signal(
    signal: dict,
    biomarkers: dict[str, float],
    *,
    runtime_context: dict | None = None,
    lab_ranges: dict | None = None,
) -> list:
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or ANDROGEN_LAB_RANGES,
        runtime_context=runtime_context,
    )


def _full_androgen_context() -> dict:
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1980-01-01",
            "symptoms": ["fatigue"],
            "supplements": ["vitamin_d"],
            "long_term_medications": ["Testosterone replacement"],
            "chronic_conditions": ["None"],
        },
        lifestyle_factors={"stress_level": 3},
        medical_history={
            "long_term_medication_classes": ["Testosterone hormone therapy"],
            "conditions": ["None"],
        },
    )
    ctx["medication"]["hormone_therapy"] = True
    ctx["clinical_context"]["aas_exposure"] = True
    ctx["symptom"]["symptoms_present"] = True
    ctx["supplement"]["supplements_disclosed"] = True
    return ctx


def test_runtime_context_model_loads():
    model = load_runtime_context_requirements_model()
    validate_runtime_context_requirements_model(
        model,
        model_path=REPO_ROOT / "knowledge_bus/governance/runtime_context_requirements_model_v1.yaml",
    )
    assert model["runtime_consumed"] is True


def test_missing_model_raises(tmp_path: Path):
    with pytest.raises(RuntimeContextModelError):
        load_runtime_context_requirements_model(tmp_path / "missing.yaml")


def test_demographic_context_missing_suppresses_signal():
    signal = {
        "signal_id": "signal_demo",
        "runtime_context_requirements": {
            "missing_context_behaviour": "suppress_signal",
            "required_context": [
                {"context_type": "demographic", "key": "sex", "requirement": "present"},
            ],
        },
        "primary_metric": "dhea",
        "activation_logic": "lab_range_exceeded",
        "activation_config": {"enable_upper_bound": True, "upper_bound_state": "suboptimal"},
        "output": {},
    }
    assert not passes_runtime_context_requirements(
        signal,
        runtime_context={},
        signal_biomarkers={"dhea": 20.0},
        signal_derived={},
        lab_ranges=ANDROGEN_LAB_RANGES,
    )


def test_demographic_context_present_allows_requirement_check():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {"context_type": "demographic", "key": "sex", "requirement": "present"},
        ],
    }
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context={"demographic": {"sex": "female"}},
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert result.satisfied


def test_companion_biomarker_missing_fails_closed():
    signal = _load_package_signal(
        "pkg_kb47_fai_high_biochemical_hyperandrogenism",
        "signal_fai_high",
    )
    results = _evaluate_signal(
        signal,
        {"fai": 90.0, "testosterone": 40.0},
        runtime_context=_full_androgen_context(),
    )
    assert results == []


def test_companion_biomarker_present_with_context_allows_evaluation_path():
    signal = _load_package_signal(
        "pkg_kb47_fai_high_biochemical_hyperandrogenism",
        "signal_fai_high",
    )
    ctx = _full_androgen_context()
    ctx["medication"]["hormone_therapy"] = True
    ctx["clinical_context"]["aas_exposure"] = True
    results = _evaluate_signal(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert isinstance(results, list)


def test_medication_context_missing_suppresses_androgen_signal():
    signal = _load_package_signal(
        "pkg_kb47_dhea_high_androgen_excess_context",
        "signal_dhea_high",
    )
    ctx = _full_androgen_context()
    ctx["medication"].pop("hormone_therapy_status_disclosed", None)
    results = _evaluate_signal(signal, {"dhea": 20.0}, runtime_context=ctx)
    assert results == []


def test_unrelated_signal_without_context_requirements_unaffected():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
        "signal_free_t4_low",
    )
    results = _evaluate_signal(
        signal,
        {"free_t4": 0.5, "tsh": 2.0},
        lab_ranges=THYROID_LAB_RANGES,
        runtime_context=None,
    )
    assert {row.signal_id for row in results} == {"signal_free_t4_low"}


def test_ft3_low_remains_inactive_without_full_context():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_low_low_t3_syndrome",
        "signal_free_t3_low",
    )
    results = _evaluate_signal(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        lab_ranges=THYROID_LAB_RANGES,
        runtime_context=None,
    )
    assert results == []


def test_ft3_low_suppressed_without_illness_context_even_with_tsh_ft4():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_low_low_t3_syndrome",
        "signal_free_t3_low",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"biological_sex": "female", "date_of_birth": "1980-01-01"},
    )
    results = _evaluate_signal(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        lab_ranges=THYROID_LAB_RANGES,
        runtime_context=ctx,
    )
    assert results == []


def test_snapshot_records_hormone_therapy_disclosure_separate_from_exposure():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": []},
    )
    assert ctx["medication"].get("hormone_therapy_status_disclosed") is True
    assert "hormone_therapy" not in ctx["medication"]


def test_snapshot_records_aas_disclosure_separate_from_exposure():
    ctx_no_aas = build_runtime_context_snapshot(
        questionnaire_responses={"supplements": []},
    )
    assert ctx_no_aas["clinical_context"].get("aas_exposure_status_disclosed") is True
    assert "aas_exposure" not in ctx_no_aas["clinical_context"]

    ctx_aas = build_runtime_context_snapshot(
        questionnaire_responses={"supplements": ["prohormone stack"]},
    )
    assert ctx_aas["clinical_context"].get("aas_exposure_status_disclosed") is True
    assert ctx_aas["clinical_context"].get("aas_exposure") is True


def test_disclosed_hormone_therapy_passes_when_answer_is_no():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {
                "context_type": "medication",
                "key": "hormone_therapy_status_disclosed",
                "requirement": "disclosed",
            },
        ],
    }
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": []},
    )
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=ctx,
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert result.satisfied


def test_disclosed_aas_exposure_passes_when_answer_is_no():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {
                "context_type": "clinical_context",
                "key": "aas_exposure_status_disclosed",
                "requirement": "disclosed",
            },
        ],
    }
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"supplements": []},
    )
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=ctx,
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert result.satisfied


def test_disclosed_requirement_fails_when_question_not_answered():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {
                "context_type": "medication",
                "key": "hormone_therapy_status_disclosed",
                "requirement": "disclosed",
            },
        ],
    }
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=build_runtime_context_snapshot(),
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert not result.satisfied


def test_ft3_low_enable_lower_bound_active_after_full_coverage_activation():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_low_low_t3_syndrome",
        "signal_free_t3_low",
    )
    assert signal.get("activation_config", {}).get("enable_lower_bound") is True
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1980-01-01",
            "chronic_conditions": [],
            "long_term_medications": [],
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )
    results = _evaluate_signal(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        lab_ranges=THYROID_LAB_RANGES,
        runtime_context=ctx,
    )
    assert {row.signal_id for row in results} == {"signal_free_t3_low"}


def test_androgen_packages_remain_inactive_without_runtime_context():
    packages = [
        ("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high", {"dhea": 20.0}),
        ("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high", {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0}),
    ]
    for package_dir, signal_id, biomarkers in packages:
        signal = _load_package_signal(package_dir, signal_id)
        results = _evaluate_signal(signal, biomarkers, runtime_context=None)
        assert results == [], f"{signal_id} should not emit without runtime context"


def test_evaluator_wires_runtime_context_check():
    source = (REPO_ROOT / "backend/core/analytics/signal_evaluator.py").read_text(encoding="utf-8")
    assert "passes_runtime_context_requirements" in source
    assert "runtime_context" in source


def test_no_hardcoded_thresholds_in_runtime_context_evaluator():
    source = (REPO_ROOT / "backend/core/analytics/runtime_context_evaluator.py").read_text(
        encoding="utf-8"
    )
    assert "5.2" not in source
    assert "60.0" not in source


def test_disclosure_state_answered_no_not_treated_as_missing_for_hormone_therapy():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": []},
    )
    assert ctx["medication"]["hormone_therapy_status"] == "answered_no"
    assert ctx["medication"].get("hormone_therapy_status_disclosed") is True
    assert "hormone_therapy" not in ctx["medication"]


def test_disclosure_state_answered_no_not_treated_as_missing_for_aas():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"supplements": []},
    )
    assert ctx["clinical_context"]["aas_exposure_status"] == "answered_no"
    assert ctx["clinical_context"].get("aas_exposure_status_disclosed") is True
    assert "aas_exposure" not in ctx["clinical_context"]


def test_disclosure_state_answered_no_for_thyroid_medication_when_meds_empty():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": []},
    )
    assert ctx["medication"]["thyroid_medication_status"] == "answered_no"
    assert "thyroid_medication" not in ctx["medication"]


def test_disclosure_state_not_answered_when_question_unanswered():
    ctx = build_runtime_context_snapshot()
    assert ctx["medication"].get("hormone_therapy_status") == "not_answered"
    assert ctx["clinical_context"].get("aas_exposure_status") == "not_answered"
    assert ctx["clinical_context"].get("illness_or_recovery_disclosure_status") == "not_answered"


def test_disclosure_state_requirement_accepts_answered_no():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {
                "context_type": "medication",
                "key": "hormone_therapy_status",
                "requirement": "disclosure_state",
                "allowed_values": ["answered_yes", "answered_no"],
            },
        ],
    }
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": []},
    )
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=ctx,
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert result.satisfied


def test_disclosure_state_requirement_fails_for_not_answered():
    requirements = {
        "missing_context_behaviour": "suppress_signal",
        "required_context": [
            {
                "context_type": "medication",
                "key": "hormone_therapy_status",
                "requirement": "disclosure_state",
                "allowed_values": ["answered_yes", "answered_no"],
            },
        ],
    }
    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=build_runtime_context_snapshot(),
        signal_biomarkers={},
        signal_derived={},
        lab_ranges={},
    )
    assert not result.satisfied


def test_positive_exposure_separate_from_disclosure_for_aas():
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"supplements": ["prohormone stack"]},
    )
    assert ctx["clinical_context"]["aas_exposure_status"] == "answered_yes"
    assert ctx["clinical_context"]["aas_exposure"] is True


def test_companion_biomarker_availability_primitives_from_signal_biomarkers():
    ctx = build_runtime_context_snapshot(
        signal_biomarkers={"tsh": 2.0, "free_t4": 1.2},
    )
    assert ctx["biomarker"]["tsh_available"] is True
    assert ctx["biomarker"]["free_t4_available"] is True


def test_lifestyle_disclosure_states_mapped_when_present():
    ctx = build_runtime_context_snapshot(
        lifestyle_factors={
            "calorie_restriction": False,
            "fasting": True,
            "heavy_training_load": False,
        },
    )
    assert ctx["clinical_context"]["calorie_restriction_status"] == "answered_no"
    assert ctx["clinical_context"]["fasting_status"] == "answered_yes"
    assert ctx["clinical_context"]["heavy_training_load_status"] == "answered_no"
