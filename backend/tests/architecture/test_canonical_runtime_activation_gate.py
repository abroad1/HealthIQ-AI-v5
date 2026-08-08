"""V5-CANONICAL-ACTIVATION-GATE-1 — non-launch canonical activation grant regressions."""

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
    COHORT_LAUNCH_CRITICAL_TEMPORARY_EXCEPTION,
    COHORT_NON_LAUNCH_CRITICAL,
    RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED,
    activation_cohort_for_package,
    clear_canonical_activation_gate_cache,
    is_non_launch_critical_cohort,
    non_launch_frame_activation_exclusion_reason,
)
from core.knowledge.package_activation_register_v1 import (  # noqa: E402
    RUNTIME_STATE_NOT_ACTIVATED,
    activated_activation_keys,
    clear_activation_register_cache,
    is_activation_key_activated,
)
from core.knowledge.package_runtime_eligibility_v1 import (  # noqa: E402
    is_launch_critical_package_id,
)
from core.knowledge.runtime_medical_authority_integrity_v1 import (  # noqa: E402
    run_runtime_medical_authority_integrity_validation,
)
from core.knowledge.why_authority_v1 import (  # noqa: E402
    STATE_LEGACY_RETIRED,
    load_why_authority_register,
)


_PROHIBITED = (
    "signal_total_cholesterol_high",
    "signal_lipid_transport_dysfunction",
    "signal_apoa1_cardio_risk",
)

_REPEAT_LOADS = 5


@pytest.fixture(autouse=True)
def _clear_caches():
    clear_activation_register_cache()
    clear_canonical_activation_gate_cache()
    yield
    clear_activation_register_cache()
    clear_canonical_activation_gate_cache()


def _activation_key_set(registry: SignalRegistry) -> list[str]:
    return sorted(row["activation_key"] for row in registry.get_all_signals())


def _non_launch_key_set(registry: SignalRegistry) -> list[str]:
    return sorted(
        row["activation_key"]
        for row in registry.get_all_signals()
        if is_non_launch_critical_cohort(str(row.get("package_id") or ""))
    )


def test_cohort_classification_is_explicit():
    assert activation_cohort_for_package("pkg_kb52c_example") == COHORT_NON_LAUNCH_CRITICAL
    assert (
        activation_cohort_for_package("pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis")
        == COHORT_LAUNCH_CRITICAL_TEMPORARY_EXCEPTION
    )


def test_canonical_register_entry_loads_when_constraints_satisfied():
    registry = SignalRegistry()
    keys = set(_non_launch_key_set(registry))
    # Known authorised non-launch lipid frame retained after integrity sprint.
    assert "signal_ldl_high::inv_ldl_high_atherogenic_ldl_burden" in keys
    assert is_activation_key_activated("signal_ldl_high::inv_ldl_high_atherogenic_ldl_burden")
    assert (
        non_launch_frame_activation_exclusion_reason(
            "signal_ldl_high::inv_ldl_high_atherogenic_ldl_burden"
        )
        is None
    )


def test_missing_canonical_entry_cannot_load_via_other_mechanisms():
    missing = "signal_fixture_never_activated::inv_fixture_never_activated"
    assert not is_activation_key_activated(missing)
    assert non_launch_frame_activation_exclusion_reason(missing) == RUNTIME_STATE_NOT_ACTIVATED
    loaded = set(_activation_key_set(SignalRegistry()))
    assert missing not in loaded


def test_explicit_prohibition_blocks_even_if_register_membership_mocked():
    prohibited_key = "signal_total_cholesterol_high::inv_total_cholesterol_high_atherogenic_hypercholesterolemia"
    with patch(
        "core.knowledge.canonical_runtime_activation_gate_v1.is_activation_key_activated",
        return_value=True,
    ):
        reason = non_launch_frame_activation_exclusion_reason(prohibited_key)
    assert reason == RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED


def test_why_retired_but_canonically_activated_signal_remains_loadable():
    register = load_why_authority_register()
    rows = register.get("_by_activation_key") or {}
    candidates = [
        key
        for key, row in rows.items()
        if str(row.get("authority_state") or "") == STATE_LEGACY_RETIRED
        and str(row.get("anthony_decision") or "").startswith("SUPERSEDED")
        and is_activation_key_activated(key)
    ]
    assert candidates, "expected at least one WHY-retired but activated frame"
    registry = SignalRegistry()
    loaded = set(_activation_key_set(registry))
    assert any(key in loaded for key in candidates)


def test_launch_critical_lineage_veto_still_excludes_non_reachable_kb47():
    """Provenance/eligibility veto continues for blocked launch-critical packages."""
    registry = SignalRegistry()
    loaded_kb47 = {
        row["package_id"]
        for row in registry.get_all_signals()
        if is_launch_critical_package_id(str(row.get("package_id") or ""))
    }
    # Known blocked kb47 packages must remain absent while lineage-eligible ones load.
    assert "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis" in loaded_kb47
    excluded_ids = {row["package_id"] for row in registry.excluded_launch_critical_packages}
    assert excluded_ids, "expected some launch-critical packages excluded by lineage veto"


def test_conflicting_authority_and_prohibited_write_fail_closed():
    integrity_errors = run_runtime_medical_authority_integrity_validation(
        repo_root=_REPO,
        activation_register={
            "activated_frame_count": 1,
            "activated_frames": [
                {
                    "activation_key": "signal_total_cholesterol_high::inv_total_cholesterol_high_atherogenic_hypercholesterolemia",
                    "package_id": "pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia",
                }
            ],
        },
    )
    assert integrity_errors

    mutation = mutate_runtime_activation_register(
        add_frames=[
            {
                "activation_key": "signal_apoa1_cardio_risk::inv_apoa1_low_cardio_risk",
                "package_id": "pkg_kb45_apoa1_low_cardio_risk",
            }
        ],
        repo_root=_REPO,
        dry_run=True,
    )
    assert mutation.ok is False
    assert mutation.errors


def test_exact_activation_key_set_deterministic_across_repeated_loads():
    sets = [_activation_key_set(SignalRegistry()) for _ in range(_REPEAT_LOADS)]
    baseline = sets[0]
    assert baseline, "registry must load a non-empty activation-key set"
    for idx, observed in enumerate(sets[1:], start=2):
        assert observed == baseline, (
            f"activation-key set drift on load #{idx}: "
            f"missing={sorted(set(baseline) - set(observed))} "
            f"added={sorted(set(observed) - set(baseline))}"
        )


def test_non_launch_loaded_keys_are_exactly_register_membership():
    """No duplicate non-launch grant path: loaded NL set == register set."""
    registry = SignalRegistry()
    loaded_nl = set(_non_launch_key_set(registry))
    register_keys = set(activated_activation_keys())
    assert loaded_nl == register_keys
    for signal_id in _PROHIBITED:
        assert not any(key.startswith(f"{signal_id}::") or key == signal_id for key in loaded_nl)


def test_mutation_write_path_refuses_launch_critical_package():
    result = mutate_runtime_activation_register(
        add_frames=[
            {
                "activation_key": "signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis",
                "package_id": "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
            }
        ],
        repo_root=_REPO,
        dry_run=True,
    )
    assert result.ok is False
    assert any("launch-critical" in err for err in result.errors)


def test_prior_integrity_module_still_passes_on_estate():
    assert run_runtime_medical_authority_integrity_validation(repo_root=_REPO) == []
