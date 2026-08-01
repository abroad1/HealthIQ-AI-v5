"""
ARCH-CONV-E / E2 / E3 — governed runtime activation boundary.

Gate 1 E3 (2026-08-01): hepatocellular + mixed + cholestatic + muscle + metabolic
activated; bilirubin severity remains override-escalation only (withheld); S24
superseded.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from core.analytics.signal_evaluator import SignalRegistry
from core.knowledge.package_activation_register_v1 import (
    RUNTIME_STATE_NOT_ACTIVATED,
    activated_activation_keys,
    clear_activation_register_cache,
    is_activation_key_activated,
    is_package_runtime_activated,
    load_activation_register,
)
from core.knowledge.package_runtime_eligibility_v1 import (
    ELIGIBILITY_OUT_OF_COHORT,
    ELIGIBILITY_PRODUCTION_REACHABLE,
    ELIGIBILITY_TEST_ONLY_OPT_IN,
    classify_package_runtime_eligibility,
    is_production_reachable,
    load_package_manifest,
)

REPO = Path(__file__).resolve().parents[3]
PACKAGES_ROOT = REPO / "knowledge_bus" / "packages"

ARCH_CONV_E_PACKAGES = (
    "pkg_kb52c_alt_high_bilirubin_severity_context",
    "pkg_kb52c_alt_high_cholestatic_alp_predominant_context",
    "pkg_kb52c_alt_high_hepatocellular_injury_pattern",
    "pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern",
    "pkg_kb52c_alt_high_mixed_biochemical_pattern",
    "pkg_kb52c_alt_high_muscle_source_or_exertional_pattern",
)

ACTIVATED_ALT_KEYS = (
    "signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern",
    "signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern",
    "signal_alt_high::inv_alt_high_r_value_cholestatic_alp_predominant_context",
    "signal_alt_high::inv_alt_high_muscle_source_or_exertional_contribution",
    "signal_alt_high::inv_alt_high_metabolic_masld_context",
)

WITHHELD_ALT_KEYS = (
    "signal_alt_high::inv_alt_high_bilirubin_hys_law_severity_context",
)

ACTIVATED_ALT_PACKAGES = (
    "pkg_kb52c_alt_high_hepatocellular_injury_pattern",
    "pkg_kb52c_alt_high_mixed_biochemical_pattern",
    "pkg_kb52c_alt_high_cholestatic_alp_predominant_context",
    "pkg_kb52c_alt_high_muscle_source_or_exertional_pattern",
    "pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern",
)

WITHHELD_ALT_PACKAGES = (
    "pkg_kb52c_alt_high_bilirubin_severity_context",
)

SUPERSEDED_S24_ALT_KEY = "signal_alt_high::inv_alt_high_hepatocellular_injury"

FORMER_BATCH5_KEYS = (
    "signal_alt_high::inv_alt_high_hepatocellular_injury_pattern",
    "signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern",
    "signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern",
)

WAVE1_KB47 = (
    "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
    "pkg_kb47_egfr_low_hemodynamic_filtration_drop",
    "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
    "pkg_kb47_free_t3_low_low_t3_syndrome",
    "pkg_kb47_free_t4_high_thyrotoxicosis_context",
    "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
)

BLOCKED_KB47 = "pkg_kb47_dhea_high_androgen_excess_context"

MANDATORY_ASSETS = ("research_brief.yaml", "signal_library.yaml", "package_manifest.yaml")


@pytest.fixture(autouse=True)
def _clear_activation_cache():
    clear_activation_register_cache()
    yield
    clear_activation_register_cache()


def test_six_alt_packages_remain_present_with_mandatory_assets():
    for package_id in ARCH_CONV_E_PACKAGES:
        package_dir = PACKAGES_ROOT / package_id
        assert package_dir.is_dir()
        for asset in MANDATORY_ASSETS:
            assert (package_dir / asset).is_file()


@pytest.mark.parametrize("package_id", ARCH_CONV_E_PACKAGES)
def test_six_alt_packages_still_validate(package_id: str):
    result = subprocess.run(
        [
            sys.executable,
            str(REPO / "backend" / "scripts" / "validate_knowledge_package.py"),
            "--package-dir",
            str(PACKAGES_ROOT / package_id),
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"{package_id} failed validation:\n{result.stdout}\n{result.stderr}"


def test_activated_and_withheld_alt_frames():
    registry = SignalRegistry()
    loaded_keys = {row["activation_key"] for row in registry.get_all_signals()}
    for key in ACTIVATED_ALT_KEYS:
        assert key in loaded_keys
    for key in WITHHELD_ALT_KEYS:
        assert key not in loaded_keys
    assert SUPERSEDED_S24_ALT_KEY not in loaded_keys
    alt = [row for row in registry.get_all_signals() if row["signal_id"] == "signal_alt_high"]
    assert sorted(row["activation_key"] for row in alt) == sorted(ACTIVATED_ALT_KEYS)


def test_withheld_packages_and_frames_are_auditable():
    registry = SignalRegistry()
    withheld_packages = {row["package_id"] for row in registry.excluded_unactivated_packages}
    assert set(WITHHELD_ALT_PACKAGES).issubset(withheld_packages)
    assert not (set(ACTIVATED_ALT_PACKAGES) & withheld_packages)
    withheld_frames = {
        row["activation_key"]: row["runtime_state"] for row in registry.excluded_unactivated_frames
    }
    for key in WITHHELD_ALT_KEYS:
        assert withheld_frames[key] == RUNTIME_STATE_NOT_ACTIVATED
    assert len(registry.excluded_launch_critical_packages) == 14


def test_rejected_frame_authority_keeps_precedence_over_activation():
    registry = SignalRegistry()
    rejected = {row["activation_key"] for row in registry.excluded_rejected_frames}
    assert "signal_homocysteine_high::inv_homocysteine_high_metabolic" in rejected
    unactivated = {row["activation_key"] for row in registry.excluded_unactivated_frames}
    assert not (rejected & unactivated)


def test_former_batch5_keys_remain_unreachable():
    registry = SignalRegistry()
    loaded_keys = {row["activation_key"] for row in registry.get_all_signals()}
    for key in FORMER_BATCH5_KEYS:
        assert key not in loaded_keys
        assert not is_activation_key_activated(key)


def test_production_reachable_packages_still_load():
    registry = SignalRegistry()
    rows = registry.get_all_signals()
    loaded_kb47 = sorted(
        {row["package_id"] for row in rows if str(row["package_id"]).startswith("pkg_kb47_")}
    )
    assert loaded_kb47 == sorted(WAVE1_KB47)
    activated_non_kb47 = {
        row["package_id"] for row in rows if not str(row["package_id"]).startswith("pkg_kb47_")
    }
    assert len(activated_non_kb47) == 171
    assert all(is_package_runtime_activated(pid) for pid in activated_non_kb47)
    assert all(row["runtime_eligibility"] == ELIGIBILITY_PRODUCTION_REACHABLE for row in rows)


def test_every_loaded_frame_is_explicitly_activated_or_launch_critical():
    registry = SignalRegistry()
    for row in registry.get_all_signals():
        if str(row["package_id"]).startswith("pkg_kb47_"):
            continue
        assert is_activation_key_activated(row["activation_key"])


def test_launch_critical_test_opt_in_still_loads_blocked_fixtures():
    opted_in = SignalRegistry(allow_launch_critical_blocked=True)
    kb47 = [
        row
        for row in opted_in.get_all_signals()
        if str(row["package_id"]).startswith("pkg_kb47_")
    ]
    assert len(kb47) == 20
    eligibility, _status = classify_package_runtime_eligibility(
        package_id=BLOCKED_KB47,
        manifest=load_package_manifest(PACKAGES_ROOT / BLOCKED_KB47),
        allow_launch_critical_blocked=True,
    )
    assert eligibility == ELIGIBILITY_TEST_ONLY_OPT_IN


def test_launch_critical_opt_in_does_not_activate_withheld_packages():
    opted_in = SignalRegistry(allow_launch_critical_blocked=True)
    loaded_packages = {row["package_id"] for row in opted_in.get_all_signals()}
    assert not (loaded_packages & set(WITHHELD_ALT_PACKAGES))


def test_withheld_packages_remain_out_of_cohort():
    for package_id in WITHHELD_ALT_PACKAGES:
        manifest = load_package_manifest(PACKAGES_ROOT / package_id)
        eligibility, _status = classify_package_runtime_eligibility(
            package_id=package_id, manifest=manifest
        )
        assert eligibility == ELIGIBILITY_OUT_OF_COHORT


def test_activated_alt_packages_are_production_reachable():
    for package_id in ACTIVATED_ALT_PACKAGES:
        manifest = load_package_manifest(PACKAGES_ROOT / package_id)
        eligibility, _status = classify_package_runtime_eligibility(
            package_id=package_id, manifest=manifest
        )
        assert eligibility == ELIGIBILITY_PRODUCTION_REACHABLE


def test_register_counts_and_gate_refs():
    register = load_activation_register()
    activated = activated_activation_keys()
    assert set(ACTIVATED_ALT_KEYS).issubset(activated)
    assert not (set(WITHHELD_ALT_KEYS) & activated)
    assert SUPERSEDED_S24_ALT_KEY not in activated
    assert register["activated_frame_count"] == len(activated) == 177
    withheld = {
        str(row["activation_key"]) for row in register["withheld_frames_arch_conv_e"]
    }
    assert withheld == set(WITHHELD_ALT_KEYS)
    assert register["gate1_reference"] == "ARCH-CONV-E3-GATE1-HMR-2026-08-01"
    assert register["gate2_reference"] == "ARCH-CONV-E3-GATE2-ANTHONY-PENDING"


def test_missing_register_fails_closed(monkeypatch, tmp_path):
    import core.knowledge.package_activation_register_v1 as register_module

    clear_activation_register_cache()
    monkeypatch.setattr(
        register_module, "activation_register_path", lambda: tmp_path / "absent.yaml"
    )
    try:
        with pytest.raises(FileNotFoundError):
            register_module.load_activation_register()
    finally:
        monkeypatch.undo()
        clear_activation_register_cache()


def test_malformed_register_fails_closed(monkeypatch, tmp_path):
    import core.knowledge.package_activation_register_v1 as register_module

    broken = tmp_path / "broken.yaml"
    broken.write_text("register_id: x\nactivated_frames: []\n", encoding="utf-8")
    clear_activation_register_cache()
    monkeypatch.setattr(register_module, "activation_register_path", lambda: broken)
    try:
        with pytest.raises(ValueError):
            register_module.load_activation_register()
    finally:
        monkeypatch.undo()
        clear_activation_register_cache()
