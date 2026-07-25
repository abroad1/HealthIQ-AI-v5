"""
P3-LAYERB-INTEL-1 — Deterministic Layer B modifier binder.

Production binds only catalogue rows that are simultaneously:
  - runtime_active: true
  - production_authority in {approved, production}

Until medical review activates catalogue rows, the binder returns an empty
selection with fail-safe provenance (no free-form / LLM selection).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import yaml

BINDER_VERSION = "layer_b_modifier_binder_v1.0.0"
_REPO = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class ModifierBindDecision:
    selected_modifier_ids: tuple[str, ...]
    rejected: tuple[tuple[str, str], ...]  # (modifier_id, reason)
    binder_version: str = BINDER_VERSION
    fail_safe: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "selected_modifier_ids": list(self.selected_modifier_ids),
            "rejected": [{"modifier_id": m, "reason": r} for m, r in self.rejected],
            "binder_version": self.binder_version,
            "fail_safe": self.fail_safe,
        }


def _norm(value: Any) -> str:
    return str(value or "").strip()


def load_modifier_catalogue(path: Path) -> List[Dict[str, Any]]:
    """
    Load a modifier catalogue from an explicit path.

    Intentionally does not default to the draft governance catalogue path —
    day-one architecture forbids production modules referencing non-runtime
    draft artefacts. Callers (tests / future approved runtime catalogues)
    must pass an explicit path.
    """
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = payload.get("modifiers") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        return []
    return [r for r in rows if isinstance(r, dict)]


def _contradicts(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    """
    Conservative contradiction: shared exclusive_group, or explicit contradicts lists.
    """
    group_a = _norm(a.get("exclusive_group") or a.get("mutex_group"))
    group_b = _norm(b.get("exclusive_group") or b.get("mutex_group"))
    if group_a and group_a == group_b:
        return True
    id_a = _norm(a.get("modifier_id"))
    id_b = _norm(b.get("modifier_id"))
    for key in ("contradicts", "conflicts_with"):
        raw_a = a.get(key) or []
        raw_b = b.get(key) or []
        if isinstance(raw_a, list) and id_b in {_norm(x) for x in raw_a}:
            return True
        if isinstance(raw_b, list) and id_a in {_norm(x) for x in raw_b}:
            return True
    return False


def bind_modifiers_v1(
    *,
    catalogue_rows: Optional[Sequence[Mapping[str, Any]]] = None,
    eligible_modifier_ids: Optional[Iterable[str]] = None,
    signal_id: str = "",
    activation_key: str = "",
) -> ModifierBindDecision:
    """
    Deterministic binder. Unsupported / inactive combinations fail safe (omit).
    Precedence among surviving modifiers: ascending modifier_id.

    When catalogue_rows is omitted, bind nothing (fail-safe). Production must not
    auto-load the draft governance catalogue.
    """
    rows = list(catalogue_rows) if catalogue_rows is not None else []
    wanted = {_norm(x) for x in (eligible_modifier_ids or []) if _norm(x)}
    rejected: List[Tuple[str, str]] = []
    active: List[Dict[str, Any]] = []

    if catalogue_rows is None:
        return ModifierBindDecision(
            selected_modifier_ids=(),
            rejected=(("__catalogue__", "no_runtime_catalogue_bound"),),
            fail_safe=True,
        )

    for row in rows:
        mid = _norm(row.get("modifier_id"))
        if not mid:
            continue
        if wanted and mid not in wanted:
            continue
        runtime_active = bool(row.get("runtime_active"))
        authority = _norm(row.get("production_authority") or "").lower()
        # Draft catalogue historically omits production_authority — treat as not approved.
        if not runtime_active:
            rejected.append((mid, "runtime_inactive"))
            continue
        if authority not in {"approved", "production"}:
            rejected.append((mid, "missing_or_unapproved_production_authority"))
            continue
        # Optional signal scope
        scope = row.get("signal_ids") or row.get("applies_to_signal_ids") or []
        if isinstance(scope, list) and scope:
            allowed = {_norm(x) for x in scope}
            if signal_id and signal_id not in allowed:
                rejected.append((mid, "signal_scope_mismatch"))
                continue
        frame_scope = row.get("activation_keys") or []
        if isinstance(frame_scope, list) and frame_scope:
            allowed_frames = {_norm(x) for x in frame_scope}
            if activation_key and activation_key not in allowed_frames:
                rejected.append((mid, "activation_key_scope_mismatch"))
                continue
        active.append(dict(row))

    # Contradiction handling: if any pair contradicts, reject both (fail-safe).
    drop: set[str] = set()
    for i, a in enumerate(active):
        for b in active[i + 1 :]:
            if _contradicts(a, b):
                drop.add(_norm(a.get("modifier_id")))
                drop.add(_norm(b.get("modifier_id")))
    for mid in sorted(drop):
        rejected.append((mid, "contradiction_fail_safe"))
    survivors = [
        _norm(r.get("modifier_id"))
        for r in active
        if _norm(r.get("modifier_id")) not in drop
    ]
    survivors = sorted(set(survivors))
    fail_safe = not survivors
    return ModifierBindDecision(
        selected_modifier_ids=tuple(survivors),
        rejected=tuple(rejected),
        fail_safe=fail_safe,
    )
