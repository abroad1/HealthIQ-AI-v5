"""Regression/sentinel tests for CF-AUTHORITY-RUNTIME-1 authority collision enforcement."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.signal_authority_collision_resolver import (
    apply_signal_authority_collision_policy,
    load_signal_authority_collision_model,
)
from core.analytics.signal_evaluator import SignalEvaluator
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity
from core.models.signal import SignalResult

REPO_ROOT = Path(__file__).resolve().parents[3]

RENAL_LAB_RANGES = {
    "egfr": {"min": 90.0, "max": 120.0},
    "creatinine": {"min": 0.6, "max": 1.2},
    "potassium": {"min": 3.5, "max": 5.0},
}


class _MultiSignalRegistry:
    def __init__(self, signals: list[dict]) -> None:
        self._signals = [dict(s) for s in signals]

    def get_all_signals(self) -> list[dict]:
        return [dict(s) for s in self._signals]


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


def _egfr_low_signal_for_test() -> dict:
    signal = _load_package_signal(
        "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
        "signal_egfr_low",
    )
    cfg = dict(signal.get("activation_config") or {})
    cfg["enable_lower_bound"] = True
    cfg["enable_upper_bound"] = False
    signal["activation_config"] = cfg
    return signal


def _evaluate(signals: list[dict], biomarkers: dict[str, float]) -> list:
    evaluator = SignalEvaluator(_MultiSignalRegistry(signals))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=RENAL_LAB_RANGES,
    )


def _activation_keys(results) -> set[str]:
    return {row.activation_key for row in results}


def test_authority_model_loads():
    model = load_signal_authority_collision_model()
    groups = model.get("authority_groups")
    assert isinstance(groups, list)
    renal = next(g for g in groups if g.get("authority_group_id") == "renal_filtration_axis")
    assert renal.get("runtime_action") == "runtime_enforced"
    assert model.get("runtime_consumed") is True


def test_egfr_low_emits_when_lower_bound_enabled_and_criteria_met():
    signal = _egfr_low_signal_for_test()
    results = _evaluate([signal], {"egfr": 55.0})
    assert _activation_keys(results) == {signal["activation_key"]}


def test_creatinine_high_suppressed_when_egfr_low_primary_present():
    egfr_signal = _egfr_low_signal_for_test()
    creatinine_signal = _load_package_signal(
        "pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
        "signal_creatinine_high",
    )
    results = _evaluate(
        [egfr_signal, creatinine_signal],
        {"egfr": 55.0, "creatinine": 1.8},
    )
    assert egfr_signal["activation_key"] in _activation_keys(results)
    assert creatinine_signal["activation_key"] not in _activation_keys(results)


def test_creatinine_high_preserved_for_distinct_potassium_risk_layer():
    egfr_signal = _egfr_low_signal_for_test()
    creatinine_signal = _load_package_signal(
        "pkg_s24_creatinine_high_renal",
        "signal_creatinine_high",
    )
    results = _evaluate(
        [egfr_signal, creatinine_signal],
        {"egfr": 55.0, "creatinine": 1.8, "potassium": 5.5},
    )
    keys = _activation_keys(results)
    assert egfr_signal["activation_key"] in keys
    assert creatinine_signal["activation_key"] in keys


def test_creatinine_high_emits_when_egfr_low_absent():
    creatinine_signal = _load_package_signal(
        "pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
        "signal_creatinine_high",
    )
    results = _evaluate([creatinine_signal], {"creatinine": 1.8})
    assert creatinine_signal["activation_key"] in _activation_keys(results)


def test_unrelated_signal_unaffected_by_renal_collision_policy():
    unrelated = {
        "signal_id": "signal_glucose_high",
        "activation_key": "signal_glucose_high::inv_test",
        "source_spec_id": "inv_test",
        "package_id": "pkg_test",
        "system": "metabolic",
        "primary_metric": "glucose",
        "activation_logic": "lab_range_exceeded",
        "activation_config": {"enable_upper_bound": True, "enable_lower_bound": False},
        "override_rules": [],
        "output": {"supporting_markers": []},
    }
    egfr_signal = _egfr_low_signal_for_test()
    lab_ranges = {
        **RENAL_LAB_RANGES,
        "glucose": {"min": 70.0, "max": 100.0},
    }
    evaluator = SignalEvaluator(_MultiSignalRegistry([egfr_signal, unrelated]))
    results = evaluator.evaluate_all(
        signal_biomarkers={"egfr": 55.0, "glucose": 140.0},
        signal_derived={},
        lab_ranges=lab_ranges,
    )
    keys = _activation_keys(results)
    assert egfr_signal["activation_key"] in keys
    assert unrelated["activation_key"] in keys


def test_missing_authority_model_is_fail_safe_pass_through():
    primary = SignalResult(
        signal_id="signal_egfr_low",
        activation_key="signal_egfr_low::inv_test",
        source_spec_id="inv_test",
        package_id="pkg_test",
        system="renal",
        signal_state="at_risk",
        signal_value=55.0,
        primary_metric="egfr",
    )
    supporting = SignalResult(
        signal_id="signal_creatinine_high",
        activation_key="signal_creatinine_high::inv_test2",
        source_spec_id="inv_test2",
        package_id="pkg_test2",
        system="renal",
        signal_state="at_risk",
        signal_value=1.8,
        primary_metric="creatinine",
    )
    results = apply_signal_authority_collision_policy(
        [primary, supporting],
        signal_biomarkers={"egfr": 55.0, "creatinine": 1.8},
        signal_derived={},
        model_path=REPO_ROOT / "nonexistent_collision_model.yaml",
    )
    assert len(results) == 2


def test_egfr_frames_remain_inactive_in_frame_index():
    index_path = REPO_ROOT / "knowledge_bus" / "governance" / "medical_frame_identity_index_v1.yaml"
    payload = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    frames = []
    for family in payload.get("signal_families", []):
        if family.get("signal_family_id") != "signal_egfr_low":
            continue
        frames.extend(family.get("frames") or [])
    assert len(frames) == 2
    for frame in frames:
        assert frame.get("promotion_state") == "compiled_not_promoted"
        assert frame.get("runtime_authority_status") == "inactive"


def test_resolver_suppression_sentinel():
    """Sentinel: renal collision suppression must remain wired."""
    from core.analytics import signal_evaluator

    source = Path(signal_evaluator.__file__).read_text(encoding="utf-8")
    assert "apply_signal_authority_collision_policy" in source
