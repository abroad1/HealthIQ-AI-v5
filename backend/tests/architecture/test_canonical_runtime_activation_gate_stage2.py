"""V5-CANONICAL-ACTIVATION-GATE-2 — estate-wide canonical activation fold-in."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BACKEND = _REPO / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from core.analytics.signal_evaluator import SignalRegistry  # noqa: E402
from core.knowledge.activation_register_mutation_v1 import (  # noqa: E402
    mutate_runtime_activation_register,
)
from core.knowledge.canonical_runtime_activation_gate_v1 import (  # noqa: E402
    RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED,
    clear_canonical_activation_gate_cache,
    canonical_frame_activation_exclusion_reason,
)
from core.knowledge.package_activation_register_v1 import (  # noqa: E402
    RUNTIME_STATE_NOT_ACTIVATED,
    activated_activation_keys,
    clear_activation_register_cache,
    is_activation_key_activated,
)
from core.knowledge.package_runtime_eligibility_v1 import (  # noqa: E402
    ELIGIBILITY_NON_REACHABLE,
    ELIGIBILITY_OUT_OF_COHORT,
    ELIGIBILITY_PRODUCTION_REACHABLE,
    classify_package_runtime_eligibility,
    is_launch_critical_package_id,
    load_package_manifest,
)
from core.knowledge.runtime_medical_authority_integrity_v1 import (  # noqa: E402
    run_runtime_medical_authority_integrity_validation,
)
from core.knowledge.why_authority_v1 import (  # noqa: E402
    STATE_LEGACY_RETIRED,
    load_why_authority_register,
)


_LC_KEYS = (
    "signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction",
    "signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop",
    "signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis",
    "signal_free_t3_low::inv_free_t3_low_low_t3_syndrome",
    "signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context",
    "signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency",
)

_BLOCKED_LC = "pkg_kb47_dhea_high_androgen_excess_context"
_REPEAT = 5


@pytest.fixture(autouse=True)
def _clear_caches():
    clear_activation_register_cache()
    clear_canonical_activation_gate_cache()
    yield
    clear_activation_register_cache()
    clear_canonical_activation_gate_cache()


def _key_set(registry: SignalRegistry) -> list[str]:
    return sorted(row["activation_key"] for row in registry.get_all_signals())


def test_every_non_launch_loaded_key_is_in_register():
    registry = SignalRegistry()
    reg = activated_activation_keys()
    for row in registry.get_all_signals():
        if is_launch_critical_package_id(str(row.get("package_id") or "")):
            continue
        assert row["activation_key"] in reg


def test_every_launch_critical_loaded_key_is_in_register():
    registry = SignalRegistry()
    reg = activated_activation_keys()
    loaded_lc = [
        row for row in registry.get_all_signals() if is_launch_critical_package_id(row["package_id"])
    ]
    assert len(loaded_lc) == 6
    for row in loaded_lc:
        assert row["activation_key"] in reg
        assert row["activation_key"] in _LC_KEYS


def test_launch_critical_register_membership_insufficient_without_lineage():
    """Canonical membership alone must not load when lineage eligibility fails."""
    man = load_package_manifest(
        _REPO / "knowledge_bus" / "packages" / _BLOCKED_LC
    )
    # Even if we hypothetically treated register membership as true at package level,
    # lineage-failed packages remain NON_REACHABLE without opt-in.
    elig, status = classify_package_runtime_eligibility(
        package_id=_BLOCKED_LC,
        manifest=man,
        enforce_activation_register=False,  # isolate lineage veto
    )
    assert elig == ELIGIBILITY_NON_REACHABLE
    assert status == "BLOCKED"
    registry = SignalRegistry()
    assert all(row["package_id"] != _BLOCKED_LC for row in registry.get_all_signals())


def test_launch_critical_eligibility_insufficient_without_register_membership():
    missing = "signal_fixture_kb47_missing::inv_fixture"
    assert not is_activation_key_activated(missing)
    assert canonical_frame_activation_exclusion_reason(missing) == RUNTIME_STATE_NOT_ACTIVATED
    # Lineage-eligible packages without register membership are OUT_OF_COHORT.
    # Use a real EXPLICIT_SPEC package temporarily unchecked via enforce=False vs True.
    pid = "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis"
    man = load_package_manifest(_REPO / "knowledge_bus" / "packages" / pid)
    with patch(
        "core.knowledge.package_runtime_eligibility_v1.is_package_runtime_activated",
        return_value=False,
    ):
        elig, _status = classify_package_runtime_eligibility(
            package_id=pid,
            manifest=man,
            enforce_activation_register=True,
        )
    assert elig == ELIGIBILITY_OUT_OF_COHORT


def test_explicit_prohibition_overrides_canonical_membership():
    prohibited = (
        "signal_total_cholesterol_high::inv_total_cholesterol_high_atherogenic_hypercholesterolemia"
    )
    with patch(
        "core.knowledge.canonical_runtime_activation_gate_v1.is_activation_key_activated",
        return_value=True,
    ):
        reason = canonical_frame_activation_exclusion_reason(prohibited)
    assert reason == RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED


def test_why_retired_but_canonically_activated_unaffected():
    register = load_why_authority_register()
    rows = register.get("_by_activation_key") or {}
    candidates = [
        key
        for key, row in rows.items()
        if str(row.get("authority_state") or "") == STATE_LEGACY_RETIRED
        and str(row.get("anthony_decision") or "").startswith("SUPERSEDED")
        and is_activation_key_activated(key)
    ]
    assert candidates
    loaded = set(_key_set(SignalRegistry()))
    assert any(key in loaded for key in candidates)


def test_blocked_launch_critical_packages_remain_blocked():
    registry = SignalRegistry()
    excluded = {row["package_id"] for row in registry.excluded_launch_critical_packages}
    assert len(excluded) == 14
    assert _BLOCKED_LC in excluded
    assert all(
        row["package_id"] != _BLOCKED_LC for row in registry.get_all_signals()
    )


def test_authorised_launch_critical_signals_continue_to_load():
    loaded = set(_key_set(SignalRegistry()))
    for key in _LC_KEYS:
        assert key in loaded


def test_full_estate_activation_key_set_deterministic():
    sets = [_key_set(SignalRegistry()) for _ in range(_REPEAT)]
    baseline = sets[0]
    assert set(baseline) == set(activated_activation_keys())
    for idx, observed in enumerate(sets[1:], start=2):
        assert observed == baseline, (
            f"estate activation-key set drift on load #{idx}: "
            f"missing={sorted(set(baseline) - set(observed))} "
            f"added={sorted(set(observed) - set(baseline))}"
        )


def test_no_runtime_loaded_key_outside_canonical_register():
    registry = SignalRegistry()
    reg = activated_activation_keys()
    loaded = {row["activation_key"] for row in registry.get_all_signals()}
    assert loaded == set(reg)


def test_mutation_accepts_lineage_eligible_launch_critical_dry_run():
    # Already present → dry-run ok with no new adds (idempotent skip of duplicates).
    result = mutate_runtime_activation_register(
        add_frames=[
            {
                "activation_key": _LC_KEYS[0],
                "package_id": "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
            }
        ],
        repo_root=_REPO,
        dry_run=True,
    )
    assert result.ok is True
    assert result.errors == []


def test_mutation_refuses_blocked_launch_critical():
    result = mutate_runtime_activation_register(
        add_frames=[
            {
                "activation_key": "signal_dhea_high::inv_dhea_high_androgen_excess_context",
                "package_id": _BLOCKED_LC,
            }
        ],
        repo_root=_REPO,
        dry_run=True,
    )
    assert result.ok is False


def test_integrity_still_passes():
    assert run_runtime_medical_authority_integrity_validation(repo_root=_REPO) == []


def test_authorised_lc_package_is_production_reachable_with_register():
    pid = "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis"
    man = load_package_manifest(_REPO / "knowledge_bus" / "packages" / pid)
    elig, status = classify_package_runtime_eligibility(package_id=pid, manifest=man)
    assert elig == ELIGIBILITY_PRODUCTION_REACHABLE
    assert status == "EXPLICIT_SPEC"
