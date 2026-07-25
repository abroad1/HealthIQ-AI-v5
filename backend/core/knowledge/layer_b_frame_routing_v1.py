"""
P3-LAYERB-INTEL-1 — Canonical Layer B frame-aware prose / asset routing.

Policy (STOP Gate 1):
1. Prefer assets declaring an exact activation_key match.
2. Else prefer assets declaring an exact source_spec_id match.
3. Else allow family-level assets keyed by signal_id with fallback_authority=LEGACY_FAMILY_LEVEL.
4. Never attach another frame's activation_key-specific asset to this frame.
5. Deterministic ordering: (match_rank, asset_id).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


FALLBACK_NONE = "NONE"
FALLBACK_LEGACY_FAMILY = "LEGACY_FAMILY_LEVEL"
FALLBACK_SOURCE_SPEC = "SOURCE_SPEC_MATCH"
FALLBACK_ACTIVATION_KEY = "ACTIVATION_KEY_MATCH"

ROUTING_POLICY_VERSION = "layer_b_frame_routing_v1.0.0"


@dataclass(frozen=True)
class ProseAssetCandidate:
    asset_id: str
    signal_id: str = ""
    activation_keys: tuple[str, ...] = ()
    source_spec_ids: tuple[str, ...] = ()
    production_authority: str = "legacy_unreviewed"
    # production | approved | legacy_unreviewed | candidate | test_only | pending_medical_review


@dataclass(frozen=True)
class FrameRoutingDecision:
    selected_asset_id: Optional[str]
    match_authority: str
    fallback_authority: str
    rejected_asset_ids: tuple[str, ...]
    routing_policy_version: str = ROUTING_POLICY_VERSION
    activation_key: str = ""
    source_spec_id: str = ""
    signal_id: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "selected_asset_id": self.selected_asset_id,
            "match_authority": self.match_authority,
            "fallback_authority": self.fallback_authority,
            "rejected_asset_ids": list(self.rejected_asset_ids),
            "routing_policy_version": self.routing_policy_version,
            "activation_key": self.activation_key,
            "source_spec_id": self.source_spec_id,
            "signal_id": self.signal_id,
        }


def _norm(value: Any) -> str:
    return str(value or "").strip()


def candidate_from_mapping(row: Mapping[str, Any], *, default_signal_id: str = "") -> ProseAssetCandidate:
    asset_id = _norm(row.get("asset_id") or row.get("interpretation_entity_id") or row.get("id"))
    signal_id = _norm(row.get("signal_id") or default_signal_id)
    keys_raw = row.get("activation_keys") or row.get("activation_key") or ()
    specs_raw = row.get("source_spec_ids") or row.get("source_spec_id") or ()
    if isinstance(keys_raw, str):
        keys: tuple[str, ...] = (_norm(keys_raw),) if _norm(keys_raw) else ()
    else:
        keys = tuple(_norm(x) for x in (keys_raw or ()) if _norm(x))
    if isinstance(specs_raw, str):
        specs: tuple[str, ...] = (_norm(specs_raw),) if _norm(specs_raw) else ()
    else:
        specs = tuple(_norm(x) for x in (specs_raw or ()) if _norm(x))
    # Entity packs often scope by signal_ids list without frame keys.
    declared_signals = row.get("signal_ids")
    if not signal_id and isinstance(declared_signals, list) and len(declared_signals) == 1:
        signal_id = _norm(declared_signals[0])
    authority = _norm(row.get("production_authority") or "legacy_unreviewed") or "legacy_unreviewed"
    return ProseAssetCandidate(
        asset_id=asset_id,
        signal_id=signal_id,
        activation_keys=keys,
        source_spec_ids=specs,
        production_authority=authority,
    )


def select_frame_prose_asset(
    *,
    candidates: Sequence[ProseAssetCandidate],
    signal_id: str,
    activation_key: str = "",
    source_spec_id: str = "",
    allow_candidate_assets: bool = False,
) -> FrameRoutingDecision:
    """
    Deterministic frame-aware selection. Candidate/test_only assets are rejected unless
    allow_candidate_assets=True (test harness only).
    """
    sid = _norm(signal_id)
    akey = _norm(activation_key)
    sspec = _norm(source_spec_id)
    rejected: List[str] = []
    eligible: List[tuple[int, str, ProseAssetCandidate]] = []

    for cand in candidates:
        if not cand.asset_id:
            continue
        authority = cand.production_authority.lower()
        if authority in {"candidate", "test_only"} and not allow_candidate_assets:
            rejected.append(cand.asset_id)
            continue
        if authority == "pending_medical_review" and not allow_candidate_assets:
            rejected.append(cand.asset_id)
            continue

        # Never borrow another frame's activation-key-specific asset.
        if cand.activation_keys and akey and akey not in cand.activation_keys:
            rejected.append(cand.asset_id)
            continue
        if cand.activation_keys and not akey:
            # Frame-specific asset cannot be selected without a frame key.
            rejected.append(cand.asset_id)
            continue

        if akey and akey in cand.activation_keys:
            eligible.append((0, cand.asset_id, cand))
            continue
        if sspec and sspec in cand.source_spec_ids:
            eligible.append((1, cand.asset_id, cand))
            continue
        # Family-level: signal_id match and no conflicting activation_keys constraint.
        if sid and (cand.signal_id == sid or not cand.signal_id):
            if not cand.activation_keys:
                eligible.append((2, cand.asset_id, cand))
            else:
                rejected.append(cand.asset_id)
            continue
        rejected.append(cand.asset_id)

    eligible.sort(key=lambda t: (t[0], t[1]))
    if not eligible:
        return FrameRoutingDecision(
            selected_asset_id=None,
            match_authority="UNRESOLVED",
            fallback_authority=FALLBACK_NONE,
            rejected_asset_ids=tuple(sorted(set(rejected))),
            activation_key=akey,
            source_spec_id=sspec,
            signal_id=sid,
        )

    rank, asset_id, _cand = eligible[0]
    if rank == 0:
        match_authority, fallback = "ACTIVATION_KEY", FALLBACK_ACTIVATION_KEY
    elif rank == 1:
        match_authority, fallback = "SOURCE_SPEC", FALLBACK_SOURCE_SPEC
    else:
        match_authority, fallback = "SIGNAL_FAMILY", FALLBACK_LEGACY_FAMILY

    # Rejected includes non-winners that were eligible but not selected.
    for r, other_id, _ in eligible[1:]:
        rejected.append(other_id)

    return FrameRoutingDecision(
        selected_asset_id=asset_id,
        match_authority=match_authority,
        fallback_authority=fallback,
        rejected_asset_ids=tuple(sorted(set(rejected))),
        activation_key=akey,
        source_spec_id=sspec,
        signal_id=sid,
    )


def resolve_lead_frame_from_top_finding(top_finding: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not isinstance(top_finding, Mapping):
        return {"signal_id": "", "activation_key": "", "source_spec_id": ""}
    return {
        "signal_id": _norm(top_finding.get("signal_id")),
        "activation_key": _norm(top_finding.get("activation_key")),
        "source_spec_id": _norm(top_finding.get("source_spec_id")),
    }


def fired_frame_rows(
    signal_results: Optional[Iterable[Mapping[str, Any]]],
    *,
    valid_states: Iterable[str] = ("suboptimal", "at_risk"),
) -> List[Dict[str, str]]:
    valid = {str(s).strip() for s in valid_states}
    out: List[Dict[str, str]] = []
    for row in signal_results or []:
        if not isinstance(row, Mapping):
            continue
        state = _norm(row.get("signal_state")).lower()
        if state not in valid:
            continue
        sid = _norm(row.get("signal_id"))
        if not sid:
            continue
        out.append(
            {
                "signal_id": sid,
                "activation_key": _norm(row.get("activation_key")),
                "source_spec_id": _norm(row.get("source_spec_id")),
            }
        )
    out.sort(key=lambda r: (r["signal_id"], r["activation_key"], r["source_spec_id"]))
    return out
