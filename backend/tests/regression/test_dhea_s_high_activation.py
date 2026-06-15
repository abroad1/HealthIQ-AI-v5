"""Regression tests for gated DHEA-S high signal activation."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.report_compiler_v1 import compile_report_v1
from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
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


def _female_context(*, dhea_supplement: bool = False, hormone_therapy: bool = False, pregnant: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
            "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
            "supplements": ["DHEA 25mg"] if dhea_supplement else [],
            "symptoms": ["acne"],
            "pregnancy_status": pregnant,
        }
    )


def _evaluate(signal: dict, biomarkers: dict, *, runtime_context):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=DHEA_S_LAB_RANGES,
        runtime_context=runtime_context,
    )


def test_dhea_s_high_emits_with_full_gates():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    assert signal["primary_metric"] == "dhea_s"
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_context(),
    )
    assert {row.signal_id for row in results} == {"signal_dhea_high"}


def test_dhea_s_high_suppresses_with_dhea_supplementation():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_context(dhea_supplement=True),
    )
    assert results == []


def test_dhea_s_high_suppresses_with_hormone_therapy():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_context(hormone_therapy=True),
    )
    assert results == []


def test_dhea_s_high_suppresses_when_pregnant():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_context(pregnant=True),
    )
    assert results == []


def test_dhea_s_high_suppresses_without_sex():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={"date_of_birth": "1990-01-01", "symptoms": ["acne"], "supplements": []}
    )
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
    )
    assert results == []


def test_dhea_s_high_report_wording_is_non_diagnostic():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    results = _evaluate(
        signal,
        {"dhea_s": 20.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=_female_context(),
    )
    report = compile_report_v1(
        signal_results=[row.model_dump() for row in results],
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
    )
    text = str(report.model_dump())
    forbidden = ("adrenal tumour", "PCOS", "adrenal glands are overactive", "You have adrenal")
    assert not any(term.lower() in text.lower() for term in forbidden)
