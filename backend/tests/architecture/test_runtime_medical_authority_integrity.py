"""V5-RUNTIME-AUTHORITY-INTEGRITY-1 — runtime medical-authority integrity regressions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BACKEND = _REPO / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from core.analytics.signal_evaluator import SignalRegistry  # noqa: E402
from core.knowledge.package_activation_register_v1 import (  # noqa: E402
    clear_activation_register_cache,
)
from core.knowledge.runtime_medical_authority_integrity_v1 import (  # noqa: E402
    ExplicitActivationProhibition,
    collect_explicit_activation_prohibitions,
    find_runtime_activation_violations,
    run_runtime_medical_authority_integrity_validation,
)


_PROHIBITED = (
    "signal_total_cholesterol_high",
    "signal_lipid_transport_dysfunction",
    "signal_apoa1_cardio_risk",
)

_APPROVED_LIPIDS = (
    "signal_ldl_high",
    "signal_hdl_low",
    "signal_triglycerides_high",
    "signal_apoa1_low",
    "signal_apob_atherogenic",
)


@pytest.fixture(autouse=True)
def _clear_activation_cache():
    clear_activation_register_cache()
    yield
    clear_activation_register_cache()


def test_estate_validator_passes_on_current_registers():
    errors = run_runtime_medical_authority_integrity_validation(repo_root=_REPO)
    assert errors == [], "\n".join(errors)


def test_prohibited_lipid_signals_not_runtime_loaded():
    registry = SignalRegistry()
    loaded_ids = {row["signal_id"] for row in registry.get_all_signals()}
    for signal_id in _PROHIBITED:
        assert signal_id not in loaded_ids, f"{signal_id} still runtime-loaded"


def test_approved_lipid_signals_remain_runtime_loadable():
    registry = SignalRegistry()
    loaded_ids = {row["signal_id"] for row in registry.get_all_signals()}
    for signal_id in _APPROVED_LIPIDS:
        assert signal_id in loaded_ids, f"{signal_id} unexpectedly absent"


def test_explicit_prohibition_fixture_fails_closed():
    prohibitions = [
        ExplicitActivationProhibition(
            signal_id="signal_fixture_blocked",
            activation_key="",
            status="NOT_AUTHORISED",
            source="fixture#blocked_targets",
            reason="test",
        )
    ]
    activated = [
        {
            "activation_key": "signal_fixture_blocked::inv_fixture",
            "package_id": "pkg_fixture_blocked",
        }
    ]
    errors = find_runtime_activation_violations(
        activated_frames=activated,
        prohibitions=prohibitions,
    )
    assert len(errors) == 1
    assert "signal_fixture_blocked::inv_fixture" in errors[0]
    assert "NOT_AUTHORISED" in errors[0]


def test_why_retired_without_activation_prohibition_is_not_blocked():
    """LEGACY_RETIRED / SUPERSEDED alone must not be treated as deactivation."""
    why_register = {
        "frames": [
            {
                "activation_key": "signal_fixture_legacy::inv_legacy",
                "signal_id": "signal_fixture_legacy",
                "authority_state": "LEGACY_RETIRED",
                "anthony_decision": "SUPERSEDED_BY_WAVE2",
            }
        ]
    }
    activation_register = {
        "activated_frame_count": 1,
        "activated_frames": [
            {
                "activation_key": "signal_fixture_legacy::inv_legacy",
                "package_id": "pkg_fixture_legacy",
            }
        ],
    }
    errors = run_runtime_medical_authority_integrity_validation(
        repo_root=_REPO,
        activation_register=activation_register,
        why_register=why_register,
        medical_registers=[],
    )
    assert errors == []


def test_conflicting_anthony_decisions_fail_closed():
    why_register = {
        "frames": [
            {
                "activation_key": "signal_fixture_conflict::inv_a",
                "signal_id": "signal_fixture_conflict",
                "anthony_decision": "APPROVED",
            },
            {
                "activation_key": "signal_fixture_conflict::inv_a",
                "signal_id": "signal_fixture_conflict",
                "anthony_decision": "NOT_AUTHORISED_WAVE2",
            },
        ]
    }
    errors = run_runtime_medical_authority_integrity_validation(
        repo_root=_REPO,
        activation_register={"activated_frame_count": 0, "activated_frames": []},
        why_register=why_register,
        medical_registers=[],
    )
    assert errors
    assert any("conflicting anthony_decision" in e for e in errors)


def test_validator_deterministic_for_identical_inputs():
    activation_register = {
        "activated_frame_count": 1,
        "activated_frames": [
            {
                "activation_key": "signal_fixture_blocked::inv_fixture",
                "package_id": "pkg_fixture_blocked",
            }
        ],
    }
    medical_registers = [
        (
            "fixture/medical_decision_register.yaml",
            {
                "blocked_targets": [
                    {
                        "signal_id": "signal_fixture_blocked",
                        "status": "NOT_AUTHORISED",
                        "reason": "fixture",
                    }
                ]
            },
        )
    ]
    first = run_runtime_medical_authority_integrity_validation(
        repo_root=_REPO,
        activation_register=activation_register,
        why_register={"frames": []},
        medical_registers=medical_registers,
    )
    second = run_runtime_medical_authority_integrity_validation(
        repo_root=_REPO,
        activation_register=activation_register,
        why_register={"frames": []},
        medical_registers=medical_registers,
    )
    assert first == second
    assert first  # non-empty failure on identical state


def test_wave2_blocked_targets_are_collected_as_prohibitions():
    prohibitions = collect_explicit_activation_prohibitions(repo_root=_REPO)
    blocked_ids = {p.signal_id for p in prohibitions if "wave2_medical_decision_register" in p.source}
    assert set(_PROHIBITED).issubset(blocked_ids)
