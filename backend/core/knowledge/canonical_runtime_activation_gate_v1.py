"""
V5-CANONICAL-ACTIVATION-GATE-2 — estate-wide canonical activation grant.

Positive activation-grant authority (estate-wide):
  ``package_runtime_activation_register_v1.yaml`` via this module.

Launch-critical ``pkg_kb47_*`` provenance/lineage eligibility
(``package_runtime_eligibility_v1``) is a **prerequisite / veto only**. It must not
independently grant runtime activation.

Supporting mechanisms (eligibility mirrors, provenance, WHY ``REJECTED``, harness
bypasses outside ``knowledge_bus/packages/``) may constrain or veto, but must not
independently grant activation for governed estate packages.
"""

from __future__ import annotations

from functools import lru_cache
from typing import FrozenSet, Optional

from core.knowledge.package_activation_register_v1 import (
    RUNTIME_STATE_NOT_ACTIVATED,
    is_activation_key_activated,
)
from core.knowledge.package_runtime_eligibility_v1 import is_launch_critical_package_id
from core.knowledge.runtime_medical_authority_integrity_v1 import (
    collect_explicit_activation_prohibitions,
)

#: Audit label when an activation_key is listed in the register but explicitly prohibited.
RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED = "EXPLICIT_ACTIVATION_PROHIBITED"

COHORT_NON_LAUNCH_CRITICAL = "non_launch_critical"
COHORT_LAUNCH_CRITICAL = "launch_critical"
# Back-compat alias from Stage 1 (exception retired in Stage 2).
COHORT_LAUNCH_CRITICAL_TEMPORARY_EXCEPTION = COHORT_LAUNCH_CRITICAL


def activation_cohort_for_package(package_id: str) -> str:
    """Classify cohort for audit/docs; both cohorts share the same positive grant."""
    if is_launch_critical_package_id(package_id):
        return COHORT_LAUNCH_CRITICAL
    return COHORT_NON_LAUNCH_CRITICAL


def is_non_launch_critical_cohort(package_id: str) -> bool:
    return activation_cohort_for_package(package_id) == COHORT_NON_LAUNCH_CRITICAL


def is_launch_critical_cohort(package_id: str) -> bool:
    return activation_cohort_for_package(package_id) == COHORT_LAUNCH_CRITICAL


@lru_cache(maxsize=1)
def _prohibited_activation_matcher() -> FrozenSet[str]:
    """
    Materialise explicit prohibition signal_ids and activation_keys for fast matching.

    Uses the same governed prohibition sources as runtime_medical_authority_integrity_v1.
    WHY retirement / LEGACY_RETIRED / SUPERSEDED alone are not included.
    """
    prohibitions = collect_explicit_activation_prohibitions()
    tokens: set[str] = set()
    for row in prohibitions:
        if row.activation_key:
            tokens.add(f"key::{row.activation_key}")
        if row.signal_id:
            tokens.add(f"sid::{row.signal_id}")
    return frozenset(tokens)


def clear_canonical_activation_gate_cache() -> None:
    _prohibited_activation_matcher.cache_clear()


def is_explicitly_activation_prohibited(activation_key: str) -> bool:
    key = str(activation_key or "").strip()
    if not key:
        return False
    tokens = _prohibited_activation_matcher()
    if f"key::{key}" in tokens:
        return True
    signal_id = key.split("::", 1)[0].strip() if "::" in key else key
    return f"sid::{signal_id}" in tokens


def canonical_frame_activation_exclusion_reason(activation_key: str) -> Optional[str]:
    """
    Sole estate-wide positive activation grant gate for governed packages.

    A governed frame loads only when:
    1. its activation_key is present in ``package_runtime_activation_register_v1.yaml``; and
    2. it is not covered by an explicit governed activation prohibition.

    Launch-critical provenance/lineage checks remain separate prerequisites/vetoes in
    ``package_runtime_eligibility_v1`` / ``SignalRegistry._load``.

    Returns None when activation is granted; otherwise an audit exclusion reason.
    """
    key = str(activation_key or "").strip()
    if not key:
        return RUNTIME_STATE_NOT_ACTIVATED
    if not is_activation_key_activated(key):
        return RUNTIME_STATE_NOT_ACTIVATED
    if is_explicitly_activation_prohibited(key):
        return RUNTIME_STATE_EXPLICIT_ACTIVATION_PROHIBITED
    return None


# Stage 1 name retained as a thin alias (same estate-wide grant semantics after Stage 2).
non_launch_frame_activation_exclusion_reason = canonical_frame_activation_exclusion_reason
