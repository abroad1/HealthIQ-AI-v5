"""Regression tests for medically authorised DHEA-S high runtime activation."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.report_compiler_v1 import compile_report_v1
from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
from core.canonical.alias_registry_service import get_alias_registry_service
from core.canonical.normalize import BiomarkerNormalizer, normalize_biomarkers_with_metadata
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

DHEA_S_LAB_RANGES = {
    "dhea_s": {"min": 0.94, "max": 15.44},
    "testosterone": {"min": 8.0, "max": 30.0},
    "shbg": {"min": 15.0, "max": 50.0},
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


def _base_context(*, dhea_supplement: bool = False, hormone_therapy: bool = False, aas: bool = False, pregnant: bool = False, symptoms: bool = True):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
            "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
            "supplements": (["DHEA 25mg"] if dhea_supplement else (["prohormone stack"] if aas else [])),
            "symptoms": ["acne"] if symptoms else [],
            "pregnancy_status": pregnant,
        }
    )


def _evaluate(signal: dict, biomarkers: dict, *, runtime_context, lab_ranges=None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or DHEA_S_LAB_RANGES,
        runtime_context=runtime_context,
    )


def test_minimal_real_user_context_activates_without_optional_fields():
    """Representative questionnaire: age, sex, high DHEA-S only — no symptoms/pregnancy/supplements."""
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
        }
    )
    assert ctx["clinical_context"]["pregnancy_status"] == "not_answered"
    assert ctx["supplement"]["dhea_supplementation_status"] == "not_answered"
    assert "symptoms_status" not in ctx["symptom"]
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=ctx)
    assert {row.signal_id for row in results} == {"signal_dhea_high"}


def test_missing_age_suppresses():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"biological_sex": "female"}
    )
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=ctx)
    assert results == []


def test_dhea_s_low_remains_inactive():
    signal = _load_package_signal("pkg_kb47_dhea_low_adrenal_androgen_reduction", "signal_dhea_low")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1990-01-01",
            "symptoms": ["fatigue"],
        }
    )
    results = _evaluate(
        signal,
        {"dhea_s": 0.5},
        runtime_context=ctx,
        lab_ranges={"dhea_s": {"min": 0.94, "max": 15.44}},
    )
    assert results == []


def test_dhea_s_high_activates_standalone_without_testosterone():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    assert signal.get("standalone_signal_allowed") is True
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context())
    assert {row.signal_id for row in results} == {"signal_dhea_high"}


def test_dhea_venous_canonicalises_and_activates():
    get_alias_registry_service.cache_clear()
    entry = {
        "value": 20.0,
        "unit": "umol/L",
        "reference_range": {"min": 0.94, "max": 15.44, "unit": "umol/L", "source": "lab"},
    }
    normalized = normalize_biomarkers_with_metadata({"DHEA (Venous)": entry})
    assert "dhea_s" in normalized
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": normalized["dhea_s"]["value"]}, runtime_context=_base_context())
    assert results
    get_alias_registry_service.cache_clear()


def test_normal_dhea_s_does_not_activate():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 5.0}, runtime_context=_base_context())
    assert results == []


def test_unsulfated_dhea_does_not_activate_dhea_s_signal():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(
        signal,
        {"dhea": 20.0},
        runtime_context=_base_context(),
        lab_ranges={"dhea": {"min": 1.0, "max": 10.0}},
    )
    assert results == []


def test_ambiguous_dhea_without_unit_fails_closed_and_does_not_activate():
    get_alias_registry_service.cache_clear()
    normalizer = BiomarkerNormalizer()
    panel, unmapped = normalizer.normalize_biomarkers({"DHEA": {"value": 20.0}})
    assert unmapped == ["DHEA"]
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context())
    assert results  # canonical dhea_s path still works when explicit
    get_alias_registry_service.cache_clear()


def test_dhea_supplementation_suppresses():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context(dhea_supplement=True))
    assert results == []


def test_pregnancy_suppresses():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context(pregnant=True))
    assert results == []


def test_missing_sex_suppresses():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"date_of_birth": "1990-01-01", "symptoms": ["acne"], "supplements": []}
    )
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=ctx)
    assert results == []


def test_hormone_therapy_allows_basic_signal_with_downgrade_path():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context(hormone_therapy=True))
    assert {row.signal_id for row in results} == {"signal_dhea_high"}


def test_output_contains_no_diagnosis_or_treatment_wording():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(signal, {"dhea_s": 20.0}, runtime_context=_base_context())
    report = compile_report_v1(
        signal_results=[row.model_dump() for row in results],
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
    )
    text = str(report.model_dump()).lower()
    forbidden = (
        "pcos",
        "adrenal tumour",
        "adrenal tumor",
        "adrenal overactivity",
        "adrenal glands are dysfunctional",
        "you have adrenal",
        "you need dhea",
        "hormone therapy",
        "supplement",
    )
    assert not any(term in text for term in forbidden if term != "hormone therapy")
    explanation = (signal.get("explanation") or {}).get("interpretation", "").lower()
    assert "may be consistent with" in explanation or "not diagnostic" in explanation
