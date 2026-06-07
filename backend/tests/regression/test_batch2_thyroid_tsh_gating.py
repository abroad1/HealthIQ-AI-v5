"""Regression tests for BATCH2-THYROID-GATE-1 mandatory TSH pre-emission gating."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

THYROID_LAB_RANGES = {
    "free_t3": {"min": 2.0, "max": 4.4},
    "free_t4": {"min": 0.8, "max": 1.8},
    "tsh": {"min": 0.4, "max": 4.5},
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


def _evaluate_signal(signal: dict, biomarkers: dict[str, float]) -> list:
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=THYROID_LAB_RANGES,
    )


def _signal_ids(results) -> set[str]:
    return {row.signal_id for row in results}


def test_ft3_high_does_not_emit_when_tsh_absent():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
        "signal_free_t3_high",
    )
    results = _evaluate_signal(signal, {"free_t3": 5.0})
    assert _signal_ids(results) == set()


def test_ft3_high_does_not_emit_when_tsh_not_suppressed():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
        "signal_free_t3_high",
    )
    results = _evaluate_signal(signal, {"free_t3": 5.0, "tsh": 2.0})
    assert _signal_ids(results) == set()


def test_ft3_high_emits_when_ft3_high_and_tsh_suppressed():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
        "signal_free_t3_high",
    )
    results = _evaluate_signal(signal, {"free_t3": 5.0, "tsh": 0.2})
    assert _signal_ids(results) == {"signal_free_t3_high"}


def test_ft4_high_does_not_emit_when_tsh_absent():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_high_thyrotoxicosis_context",
        "signal_free_t4_high",
    )
    results = _evaluate_signal(signal, {"free_t4": 2.5})
    assert _signal_ids(results) == set()


def test_ft4_high_does_not_emit_when_tsh_not_suppressed():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_high_thyrotoxicosis_context",
        "signal_free_t4_high",
    )
    results = _evaluate_signal(signal, {"free_t4": 2.5, "tsh": 3.0})
    assert _signal_ids(results) == set()


def test_ft4_high_emits_when_ft4_high_and_tsh_suppressed():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_high_thyrotoxicosis_context",
        "signal_free_t4_high",
    )
    results = _evaluate_signal(signal, {"free_t4": 2.5, "tsh": 0.2})
    assert _signal_ids(results) == {"signal_free_t4_high"}


def test_ft4_low_does_not_emit_when_tsh_absent():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
        "signal_free_t4_low",
    )
    results = _evaluate_signal(signal, {"free_t4": 0.5})
    assert _signal_ids(results) == set()


def test_ft4_low_emits_when_ft4_low_and_tsh_present():
    signal = _load_package_signal(
        "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
        "signal_free_t4_low",
    )
    results = _evaluate_signal(signal, {"free_t4": 0.5, "tsh": 2.0})
    assert _signal_ids(results) == {"signal_free_t4_low"}


def test_ft3_low_package_not_runtime_active_in_frame_index():
    index_path = REPO_ROOT / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    text = index_path.read_text(encoding="utf-8")
    assert "frame_batch2_free_t3_low_low_t3_syndrome" in text
    assert "source_package_id: pkg_kb47_free_t3_low_low_t3_syndrome" in text
    section_start = text.index("frame_batch2_free_t3_low_low_t3_syndrome")
    section = text[section_start : section_start + 600]
    assert "promotion_state: compiled_not_promoted" in section
    assert "runtime_authority_status: inactive" in section


def test_androgen_and_egfr_packages_remain_inactive_in_frame_index():
    index_path = REPO_ROOT / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    text = index_path.read_text(encoding="utf-8")
    inactive_markers = (
        "pkg_kb47_dhea_high_androgen_excess_context",
        "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
    )
    for package_id in inactive_markers:
        pos = text.index(f"source_package_id: {package_id}")
        section = text[pos : pos + 400]
        assert "runtime_authority_status: inactive" in section
        assert "runtime_active_canonical" not in section.split("runtime_authority_status")[0]


def test_unrelated_signal_without_gates_still_emits():
    registry = SignalRegistry()
    candidates = [
        row
        for row in registry.get_all_signals()
        if not row.get("mandatory_pre_emission_gates") and row.get("primary_metric") == "creatinine"
    ]
    assert candidates
    signal = candidates[0]
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    results = evaluator.evaluate_all(
        signal_biomarkers={"creatinine": 1.8},
        signal_derived={},
        lab_ranges={"creatinine": {"min": 0.6, "max": 1.2}},
    )
    assert results
