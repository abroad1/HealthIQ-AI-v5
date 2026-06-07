"""Regression/sentinel tests for CF-AUTHORITY-RUNTIME-1 authority collision enforcement."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.signal_authority_collision_resolver import (
    AuthorityModelLoadError,
    apply_signal_authority_collision_policy,
    load_signal_authority_collision_model,
    validate_signal_authority_collision_model,
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


def _duplicate_renal_results() -> tuple[SignalResult, SignalResult]:
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
        package_id="pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
        system="renal",
        signal_state="at_risk",
        signal_value=1.8,
        primary_metric="creatinine",
    )
    return primary, supporting


def test_authority_model_loads():
    model = load_signal_authority_collision_model()
    groups = model.get("authority_groups")
    assert isinstance(groups, list)
    renal = next(g for g in groups if g.get("authority_group_id") == "renal_filtration_axis")
    assert renal.get("runtime_action") == "runtime_enforced"
    assert model.get("runtime_consumed") is True
    layer = next(
        layer
        for layer in renal.get("distinct_risk_layers", [])
        if layer.get("layer_id") == "hyperkalemia_or_electrolyte_complication"
    )
    assert layer["preserve_when"]["mechanism"] == "governed_override_rule"
    assert layer["preserve_when"]["override_rule_id"] == "or_renal_acute_imbalance"


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


def test_kb52c_still_suppressed_with_high_potassium_without_governed_override():
    egfr_signal = _egfr_low_signal_for_test()
    creatinine_signal = _load_package_signal(
        "pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
        "signal_creatinine_high",
    )
    results = _evaluate(
        [egfr_signal, creatinine_signal],
        {"egfr": 55.0, "creatinine": 1.8, "potassium": 5.5},
    )
    keys = _activation_keys(results)
    assert egfr_signal["activation_key"] in keys
    assert creatinine_signal["activation_key"] not in keys


def test_creatinine_high_preserved_for_governed_potassium_override_rule():
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


def test_missing_authority_model_raises():
    primary, supporting = _duplicate_renal_results()
    with pytest.raises(AuthorityModelLoadError, match="not found"):
        apply_signal_authority_collision_policy(
            [primary, supporting],
            signal_biomarkers={"egfr": 55.0, "creatinine": 1.8, "potassium": 1.8},
            signal_derived={},
            lab_ranges=RENAL_LAB_RANGES,
            model_path=REPO_ROOT / "nonexistent_collision_model.yaml",
        )


def test_malformed_authority_model_raises(tmp_path: Path):
    bad_model = tmp_path / "bad_collision_model.yaml"
    bad_model.write_text(
        "runtime_consumed: true\nauthority_groups: []\n",
        encoding="utf-8",
    )
    primary, supporting = _duplicate_renal_results()
    with pytest.raises(AuthorityModelLoadError, match="missing authority_groups"):
        apply_signal_authority_collision_policy(
            [primary, supporting],
            signal_biomarkers={"egfr": 55.0, "creatinine": 1.8},
            signal_derived={},
            lab_ranges=RENAL_LAB_RANGES,
            model_path=bad_model,
        )


def test_evaluate_all_raises_when_default_authority_model_missing(monkeypatch):
    egfr_signal = _egfr_low_signal_for_test()
    creatinine_signal = _load_package_signal(
        "pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
        "signal_creatinine_high",
    )
    missing = REPO_ROOT / "missing_authority_collision_model_for_test.yaml"
    monkeypatch.setattr(
        "core.analytics.signal_authority_collision_resolver.DEFAULT_MODEL_PATH",
        missing,
    )
    with pytest.raises(AuthorityModelLoadError, match="not found"):
        _evaluate(
            [egfr_signal, creatinine_signal],
            {"egfr": 55.0, "creatinine": 1.8},
        )


def test_validate_rejects_ungoverned_preserve_threshold(tmp_path: Path):
    model = load_signal_authority_collision_model()
    renal = next(
        g for g in model["authority_groups"] if g["authority_group_id"] == "renal_filtration_axis"
    )
    bad = dict(model)
    bad_groups = []
    for group in model["authority_groups"]:
        if group.get("authority_group_id") != "renal_filtration_axis":
            bad_groups.append(group)
            continue
        mutated = dict(group)
        layers = []
        for layer in group.get("distinct_risk_layers", []):
            if layer.get("layer_id") == "hyperkalemia_or_electrolyte_complication":
                layers.append(
                    {
                        **layer,
                        "preserve_when": {
                            "mechanism": "numeric_threshold",
                            "metric_id": "potassium",
                            "operator": ">",
                            "value": 5.2,
                        },
                    }
                )
            else:
                layers.append(layer)
        mutated["distinct_risk_layers"] = layers
        bad_groups.append(mutated)
    bad["authority_groups"] = bad_groups
    bad_path = tmp_path / "bad.yaml"
    bad_path.write_text(yaml.dump(bad), encoding="utf-8")
    with pytest.raises(AuthorityModelLoadError, match="governed_override_rule"):
        validate_signal_authority_collision_model(bad, model_path=bad_path)


def test_egfr_frames_runtime_active_in_frame_index():
    index_path = REPO_ROOT / "knowledge_bus" / "governance" / "medical_frame_identity_index_v1.yaml"
    payload = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    frames = []
    for family in payload.get("signal_families", []):
        if family.get("signal_family_id") != "signal_egfr_low":
            continue
        frames.extend(family.get("frames") or [])
    assert len(frames) == 2
    for frame in frames:
        assert frame.get("promotion_state") == "runtime_active_canonical"
        assert frame.get("runtime_authority_status") == "active"
        assert frame.get("clinical_adjudication_status") == "accepted_with_rationale"


def test_resolver_suppression_sentinel():
    """Sentinel: renal collision suppression must remain wired."""
    from core.analytics import signal_evaluator

    source = Path(signal_evaluator.__file__).read_text(encoding="utf-8")
    assert "apply_signal_authority_collision_policy" in source
