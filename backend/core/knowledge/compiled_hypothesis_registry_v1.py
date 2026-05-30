"""
ARCH-RT-4 — Shadow/pilot compiled hypothesis registry (separate from ROOT_CAUSE_TARGET_SPECS).

Must NOT be merged into root_cause_registry_v1.get_root_cause_targets() — import-time
validation of all 41 legacy YAML assets must remain unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from core.knowledge.compiled_hypothesis import (
    PILOT_SIGNAL_ID,
    RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS,
    CompiledHypothesisValidationError,
    artefact_as_shadow_dict,
    get_compiled_hypothesis_artefact,
    validate_confirmatory_test_refs,
)

ShadowLoader = Any  # returns dict payload for shadow comparison


@dataclass(frozen=True)
class CompiledHypothesisPilotSpec:
    signal_id: str
    activation_key: str
    artefact_signal_id: str
    registration_source: str = "compiled_hypothesis_pilot_v1"


# Pilot-only entries — never append to ROOT_CAUSE_TARGET_SPECS.
COMPILED_HYPOTHESIS_PILOT_SPECS: Tuple[CompiledHypothesisPilotSpec, ...] = (
    CompiledHypothesisPilotSpec(
        signal_id=PILOT_SIGNAL_ID,
        activation_key="signal_vitamin_d_low::inv_vitamin_d_low_deficiency",
        artefact_signal_id=PILOT_SIGNAL_ID,
    ),
)

_PILOT_BY_SIGNAL = {spec.signal_id: spec for spec in COMPILED_HYPOTHESIS_PILOT_SPECS}


def is_compiled_hypothesis_pilot_signal(signal_id: str) -> bool:
    return signal_id.strip() in _PILOT_BY_SIGNAL


def is_runtime_promoted_compiled_signal(signal_id: str) -> bool:
    return signal_id.strip() in RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS


def load_shadow_compiled_hypothesis(signal_id: str) -> Optional[Dict[str, Any]]:
    """
    Shadow loader for pilot signals only. Returns None for non-pilot signal_ids.
    Fail-closed on invalid artefact.
    """
    sid = signal_id.strip()
    if sid not in _PILOT_BY_SIGNAL:
        return None
    spec = _PILOT_BY_SIGNAL[sid]
    artefact = get_compiled_hypothesis_artefact(spec.artefact_signal_id)
    if artefact.activation_key != spec.activation_key:
        raise CompiledHypothesisValidationError(
            f"activation_key mismatch for {sid}: artefact={artefact.activation_key!r} "
            f"spec={spec.activation_key!r}"
        )
    validate_confirmatory_test_refs(artefact)
    payload = artefact_as_shadow_dict(artefact)
    payload["registration_source"] = spec.registration_source
    return payload


def list_compiled_hypothesis_pilot_signal_ids() -> Tuple[str, ...]:
    return tuple(spec.signal_id for spec in COMPILED_HYPOTHESIS_PILOT_SPECS)
