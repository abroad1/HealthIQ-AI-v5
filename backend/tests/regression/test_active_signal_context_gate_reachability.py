"""Regression tests for active signal context gate reachability (BETA-READINESS-SPRINT-2)."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

THYROID_LAB_RANGES = {
    "free_t3": {"min": 2.0, "max": 4.4},
    "free_t4": {"min": 0.8, "max": 1.8},
    "tsh": {"min": 0.4, "max": 4.5},
}

ANDROGEN_LAB_RANGES = {
    "fai": {"min": 20.0, "max": 70.0},
    "testosterone": {"min": 8.0, "max": 30.0},
    "shbg": {"min": 15.0, "max": 50.0},
    "free_testosterone": {"min": 5.0, "max": 25.0},
    "dhea_s": {"min": 0.94, "max": 15.44},
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
    raise AssertionError(f"signal {signal_id} not found")


def _evaluate(signal: dict, biomarkers: dict, *, runtime_context, lab_ranges=None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or ANDROGEN_LAB_RANGES,
        runtime_context=runtime_context,
    )


def _female_minimal(*, pregnant: bool | None = None, supplements: list[str] | None = None):
    responses: dict = {
        "biological_sex": "female",
        "date_of_birth": "1990-01-01",
        "long_term_medications": [],
        "supplements": supplements if supplements is not None else [],
    }
    if pregnant is not None:
        responses["pregnancy_status"] = pregnant
    return build_runtime_context_snapshot(questionnaire_responses=responses)


def _ft3_minimal(*, pregnant: bool | None = None):
    responses: dict = {
        "long_term_medications": [],
        "chronic_conditions": [],
    }
    if pregnant is not None:
        responses["pregnancy_status"] = pregnant
    return build_runtime_context_snapshot(
        questionnaire_responses=responses,
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )


def test_fai_high_activates_without_pregnancy_field():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    ctx = _female_minimal()
    assert ctx["clinical_context"]["pregnancy_status"] == "not_answered"
    results = _evaluate(signal, {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0}, runtime_context=ctx)
    assert {row.signal_id for row in results} == {"signal_fai_high"}


def test_fai_high_suppresses_pregnancy_answered_yes():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_minimal(pregnant=True),
    )
    assert results == []


def test_free_testosterone_high_activates_without_pregnancy_field():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    ctx = _female_minimal()
    assert ctx["clinical_context"]["pregnancy_status"] == "not_answered"
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert {row.signal_id for row in results} == {"signal_free_testosterone_high"}


def test_free_testosterone_high_suppresses_pregnancy_answered_yes():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_minimal(pregnant=True),
    )
    assert results == []


def test_ft3_low_activates_without_pregnancy_field():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    ctx = _ft3_minimal()
    assert ctx["clinical_context"]["pregnancy_status"] == "not_answered"
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=ctx,
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert {row.signal_id for row in results} == {"signal_free_t3_low"}


def test_ft3_low_suppresses_pregnancy_answered_yes():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=_ft3_minimal(pregnant=True),
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert results == []


def test_pregnancy_not_answered_allows_when_answered_no_also_valid():
    ctx = _female_minimal(pregnant=False)
    assert ctx["clinical_context"]["pregnancy_status"] == "answered_no"


def test_missing_sex_suppresses_fai_high():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"date_of_birth": "1990-01-01", "long_term_medications": [], "supplements": [], "symptoms": []}
    )
    results = _evaluate(signal, {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0}, runtime_context=ctx)
    assert results == []


def test_missing_age_suppresses_free_testosterone_high():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"biological_sex": "female", "long_term_medications": [], "supplements": []}
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert results == []


def test_ordinary_supplements_do_not_suppress_fai_high():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    for supplements in (["Vitamin D"], ["Omega-3/Fish Oil"], ["Multivitamin"]):
        ctx = _female_minimal(supplements=supplements)
        assert ctx["clinical_context"]["aas_exposure_status"] == "answered_no"
        results = _evaluate(
            signal,
            {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
            runtime_context=ctx,
        )
        assert {row.signal_id for row in results} == {"signal_fai_high"}, f"suppressed for {supplements}"


def test_genuine_aas_suppresses_fai_high():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    ctx = _female_minimal(supplements=["prohormone stack"])
    assert ctx["clinical_context"]["aas_exposure_status"] == "answered_yes"
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert results == []


def test_fai_high_activates_without_symptoms_field():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    ctx = _female_minimal()
    assert "symptoms_status" not in ctx["symptom"]
    results = _evaluate(signal, {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0}, runtime_context=ctx)
    assert {row.signal_id for row in results} == {"signal_fai_high"}


def test_free_testosterone_high_activates_without_symptoms_field():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    ctx = _female_minimal()
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert {row.signal_id for row in results} == {"signal_free_testosterone_high"}


def test_free_testosterone_low_reachable_via_low_testosterone_symptoms():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        "signal_free_testosterone_low",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1985-01-01",
            "long_term_medications": [],
            "supplements": [],
            "chronic_conditions": [],
            "low_testosterone_symptoms": "Decreased energy/libido",
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )
    assert ctx["symptom"]["symptoms_status"] == "answered_yes"
    results = _evaluate(
        signal,
        {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0},
        runtime_context=ctx,
    )
    assert {row.signal_id for row in results} == {"signal_free_testosterone_low"}


def test_free_testosterone_low_suppressed_without_symptoms_answered():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        "signal_free_testosterone_low",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1985-01-01",
            "long_term_medications": [],
            "supplements": [],
            "chronic_conditions": [],
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )
    assert "symptoms_status" not in ctx["symptom"]
    results = _evaluate(
        signal,
        {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0},
        runtime_context=ctx,
    )
    assert results == []
