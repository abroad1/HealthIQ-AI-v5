"""Regression tests for BATCH2-FULL-COVERAGE-ACTIVATION-1 gated thyroid/androgen activation."""

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


def _evaluate(signal: dict, biomarkers: dict[str, float], *, runtime_context=None, lab_ranges=None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or ANDROGEN_LAB_RANGES,
        runtime_context=runtime_context,
    )


def _ft3_full_context(*, pregnant: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "long_term_medications": [],
            "chronic_conditions": [],
            "pregnancy_status": pregnant,
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )


def _female_androgen_context(*, hormone_therapy: bool = False, aas: bool = False, dhea: bool = False, pregnant: bool = False):
    responses = {
        "biological_sex": "female",
        "date_of_birth": "1990-01-01",
        "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
        "supplements": (
            ["prohormone stack"]
            if aas
            else (["DHEA 25mg"] if dhea else [])
        ),
        "symptoms": ["acne"],
        "pregnancy_status": pregnant,
    }
    return build_runtime_context_snapshot(questionnaire_responses=responses)


def _adult_male_low_context(*, hormone_therapy: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1985-01-01",
            "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
            "supplements": [],
            "symptoms": ["fatigue"],
            "chronic_conditions": [],
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )


def test_ft3_low_emits_with_full_gates():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    assert signal["activation_config"]["enable_lower_bound"] is True
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=_ft3_full_context(),
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert {row.signal_id for row in results} == {"signal_free_t3_low"}


def test_ft3_low_fails_closed_without_tsh():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "free_t4": 1.2},
        runtime_context=_ft3_full_context(),
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert results == []


def test_ft3_low_fails_closed_without_energy_context():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"long_term_medications": [], "chronic_conditions": []},
    )
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=ctx,
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert results == []


def test_ft3_low_suppresses_when_pregnant():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=_ft3_full_context(pregnant=True),
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert results == []


def test_fai_high_suppresses_when_pregnant():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(pregnant=True),
    )
    assert results == []


def test_fai_high_suppresses_with_dhea_supplementation():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(dhea=True),
    )
    assert results == []


def test_free_testosterone_high_suppresses_when_pregnant():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(pregnant=True),
    )
    assert results == []


def test_free_testosterone_high_suppresses_with_dhea_supplementation():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(dhea=True),
    )
    assert results == []


def test_fai_high_emits_for_female_with_companions():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(),
    )
    assert {row.signal_id for row in results} == {"signal_fai_high"}


def test_fai_high_fails_closed_for_male():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    ctx = _female_androgen_context()
    ctx["demographic"]["sex"] = "male"
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert results == []


def test_fai_high_suppresses_with_hormone_therapy():
    signal = _load_package_signal("pkg_kb47_fai_high_biochemical_hyperandrogenism", "signal_fai_high")
    results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(hormone_therapy=True),
    )
    assert results == []


def test_free_testosterone_high_emits_with_gates():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(),
    )
    assert {row.signal_id for row in results} == {"signal_free_testosterone_high"}


def test_free_testosterone_high_suppresses_with_aas():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        "signal_free_testosterone_high",
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_androgen_context(aas=True),
    )
    assert results == []


def test_free_testosterone_low_emits_adult_male_only():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        "signal_free_testosterone_low",
    )
    assert signal["activation_config"]["enable_lower_bound"] is True
    results = _evaluate(
        signal,
        {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0},
        runtime_context=_adult_male_low_context(),
    )
    assert {row.signal_id for row in results} == {"signal_free_testosterone_low"}


def test_free_testosterone_low_fails_closed_for_female():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        "signal_free_testosterone_low",
    )
    ctx = _adult_male_low_context()
    ctx["demographic"]["sex"] = "female"
    results = _evaluate(
        signal,
        {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0},
        runtime_context=ctx,
    )
    assert results == []


def test_free_testosterone_low_fails_closed_for_non_adult():
    signal = _load_package_signal(
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        "signal_free_testosterone_low",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "2015-01-01",
            "symptoms": ["fatigue"],
            "long_term_medications": [],
            "chronic_conditions": [],
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )
    results = _evaluate(
        signal,
        {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0},
        runtime_context=ctx,
    )
    assert results == []


def test_dhea_high_remains_inactive():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea": 20.0}, runtime_context=_female_androgen_context())
    assert results == []


def test_dhea_low_remains_inactive():
    signal = _load_package_signal("pkg_kb47_dhea_low_adrenal_androgen_reduction", "signal_dhea_low")
    results = _evaluate(signal, {"dhea": 0.5}, runtime_context=_adult_male_low_context())
    assert results == []


def test_fai_low_remains_inactive_primary():
    signal = _load_package_signal("pkg_kb47_fai_low_reduced_free_androgen_availability", "signal_fai_low")
    results = _evaluate(
        signal,
        {"fai": 10.0, "testosterone": 5.0, "shbg": 40.0, "free_testosterone": 3.0, "lh": 2.0},
        runtime_context=_adult_male_low_context(),
    )
    assert results == []


def test_free_testosterone_pct_packages_remain_inactive():
    for package_dir, signal_id, biomarkers in (
        (
            "pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction",
            "signal_free_testosterone_pct_high",
            {"free_testosterone_pct": 5.0, "testosterone": 40.0, "shbg": 20.0, "free_testosterone": 30.0},
        ),
        (
            "pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction",
            "signal_free_testosterone_pct_low",
            {"free_testosterone_pct": 0.5, "testosterone": 5.0, "shbg": 40.0, "free_testosterone": 3.0},
        ),
    ):
        signal = _load_package_signal(package_dir, signal_id)
        results = _evaluate(signal, biomarkers, runtime_context=_female_androgen_context())
        assert results == []
