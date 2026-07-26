"""
ARCH-CONV-CORRECT-1 — governed frame co-service resolution.

Decides, for an activation-frame family where a non-specific anchor and cause-specific
siblings can fire on the same primary metric, which frames may serve causal WHY and
which may serve non-causal context only.

All rules come from ``knowledge_bus/governance/frame_co_service_policy_v1.yaml``, which
records only Anthony-ratified Gate C dispositions. Fail closed: a malformed or missing
policy raises rather than allowing sibling frames to co-serve.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import yaml

WHY_ROLE_CAUSAL = "causal"
WHY_ROLE_MORPHOLOGY_CONTEXT = "morphology_context"

SERVE_CAUSAL = "SERVE_CAUSAL"
SERVE_CONTEXT = "SERVE_CONTEXT"
SUPPRESS = "SUPPRESS"


class CoServicePolicyError(RuntimeError):
    """Raised when the governed co-service policy cannot be loaded or validated."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def co_service_policy_path() -> Path:
    return _repo_root() / "knowledge_bus" / "governance" / "frame_co_service_policy_v1.yaml"


@lru_cache(maxsize=1)
def load_frame_co_service_policy() -> Dict[str, Any]:
    path = co_service_policy_path()
    if not path.is_file():
        raise CoServicePolicyError(f"missing frame co-service policy: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise CoServicePolicyError("frame co-service policy root must be a mapping")
    if payload.get("runtime_consumed") is not True:
        raise CoServicePolicyError("frame co-service policy must set runtime_consumed: true")
    families = payload.get("families")
    if not isinstance(families, list) or not families:
        raise CoServicePolicyError("frame co-service policy requires a non-empty families list")

    by_signal: Dict[str, Dict[str, Any]] = {}
    for family in families:
        if not isinstance(family, dict):
            raise CoServicePolicyError("co-service family row must be a mapping")
        signal_id = str(family.get("signal_id") or "").strip()
        anchor = family.get("anchor")
        specific = family.get("specific_frames")
        resolution = family.get("resolution")
        if not signal_id:
            raise CoServicePolicyError("co-service family requires signal_id")
        if not isinstance(anchor, dict) or not str(anchor.get("activation_key") or "").strip():
            raise CoServicePolicyError(f"co-service family {signal_id} requires an anchor activation_key")
        if not isinstance(specific, list) or not specific:
            raise CoServicePolicyError(f"co-service family {signal_id} requires specific_frames")
        if not isinstance(resolution, dict):
            raise CoServicePolicyError(f"co-service family {signal_id} requires a resolution block")
        for frame in specific:
            if not isinstance(frame, dict) or not str(frame.get("activation_key") or "").strip():
                raise CoServicePolicyError(
                    f"co-service specific frame in {signal_id} requires activation_key"
                )
            gate = frame.get("evidence_gate")
            if not isinstance(gate, dict) or not gate.get("markers_any") or not gate.get("direction"):
                raise CoServicePolicyError(
                    f"co-service specific frame {frame.get('activation_key')!r} requires an evidence_gate"
                )
        if signal_id in by_signal:
            raise CoServicePolicyError(f"duplicate co-service family for {signal_id}")
        by_signal[signal_id] = family

    payload = dict(payload)
    payload["_by_signal_id"] = by_signal
    return payload


def clear_frame_co_service_cache() -> None:
    load_frame_co_service_policy.cache_clear()


def family_policy_for_signal_id(signal_id: str) -> Optional[Dict[str, Any]]:
    sid = str(signal_id or "").strip()
    if not sid:
        return None
    return load_frame_co_service_policy()["_by_signal_id"].get(sid)


def anchor_allowed_hypothesis_ids(signal_id: str) -> Tuple[str, ...]:
    family = family_policy_for_signal_id(signal_id)
    if family is None:
        return ()
    anchor = family.get("anchor") or {}
    return tuple(
        str(x).strip() for x in (anchor.get("allowed_hypothesis_ids") or []) if str(x).strip()
    )


def anchor_forbidden_causal_terms(signal_id: str) -> Tuple[str, ...]:
    family = family_policy_for_signal_id(signal_id)
    if family is None:
        return ()
    anchor = family.get("anchor") or {}
    return tuple(
        str(x).strip().lower() for x in (anchor.get("forbidden_causal_terms") or []) if str(x).strip()
    )


def resolve_family_co_service(
    *,
    signal_id: str,
    fired_activation_keys: Sequence[str],
    evidence_gate_evaluator,
) -> Dict[str, str]:
    """
    Return ``{activation_key: SERVE_CAUSAL | SERVE_CONTEXT | SUPPRESS}`` for one family.

    ``evidence_gate_evaluator(gate)`` must return True only when the frame's governed
    evidence gate is positively satisfied on this panel. Unknown/missing evidence is not
    support, so it resolves to the anchor fallback rather than a speculative cause.

    Frames outside the governed family are not returned; callers keep their existing
    behaviour for those.
    """
    family = family_policy_for_signal_id(signal_id)
    if family is None:
        return {}

    fired = [str(k).strip() for k in fired_activation_keys if str(k).strip()]
    anchor_key = str((family.get("anchor") or {}).get("activation_key") or "").strip()
    specific_frames: List[Dict[str, Any]] = [
        frame for frame in family["specific_frames"] if isinstance(frame, dict)
    ]
    specific_keys = [str(frame.get("activation_key") or "").strip() for frame in specific_frames]

    supported: List[str] = []
    for frame in specific_frames:
        key = str(frame.get("activation_key") or "").strip()
        if key not in fired:
            continue
        if bool(evidence_gate_evaluator(frame.get("evidence_gate") or {})):
            supported.append(key)

    combined_authorised = bool(family.get("combined_pattern_authorised", False))
    serve_specific: List[str] = []
    if len(supported) == 1:
        serve_specific = list(supported)
    elif len(supported) > 1 and combined_authorised:
        serve_specific = list(supported)

    decisions: Dict[str, str] = {}
    if anchor_key in fired:
        decisions[anchor_key] = SERVE_CONTEXT
    for key in specific_keys:
        if key not in fired:
            continue
        decisions[key] = SERVE_CAUSAL if key in serve_specific else SUPPRESS
    return decisions


def why_role_for_decision(decision: str) -> str:
    return WHY_ROLE_CAUSAL if decision == SERVE_CAUSAL else WHY_ROLE_MORPHOLOGY_CONTEXT


def governed_co_service_signal_ids() -> Tuple[str, ...]:
    return tuple(sorted(load_frame_co_service_policy()["_by_signal_id"].keys()))


def evidence_gate_markers(gate: Mapping[str, Any]) -> Tuple[List[str], str]:
    markers = [str(x).strip() for x in (gate.get("markers_any") or []) if str(x).strip()]
    return markers, str(gate.get("direction") or "").strip()
