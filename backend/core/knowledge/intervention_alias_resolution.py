"""Deterministic intervention alias resolution (KB-S48c).

Exact normalized-string lookup against ``intervention_class_alias_map_v1.yaml``.
Unknown inputs are not guessed: ``resolve_intervention_class`` returns ``None`` when the
alias is absent, matching ``unknown_name_handling.resolution: unmapped`` in the map.
"""

from __future__ import annotations

from typing import Any

UNKNOWN_NAME_RESOLUTION_UNMAPPED = "unmapped"


def normalize_intervention_input(text: str) -> str:
    """Normalize free text for lookup (strip + lowercase). No fuzzy matching."""
    return text.strip().lower()


def alias_lookup_from_map_doc(alias_map_doc: dict[str, Any]) -> dict[str, str]:
    """Build ``alias_normalized`` → ``intervention_class_id`` from a map document."""
    rows = alias_map_doc.get("aliases")
    if not isinstance(rows, list):
        return {}
    out: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = row.get("alias_normalized")
        cid = row.get("intervention_class_id")
        if isinstance(key, str) and isinstance(cid, str):
            out[key.strip().lower()] = cid
    return out


def assert_unknown_handling_unmapped(alias_map_doc: dict[str, Any]) -> None:
    """Raise ``ValueError`` if the governed policy is not ``unmapped``."""
    unh = alias_map_doc.get("unknown_name_handling")
    if not isinstance(unh, dict):
        raise ValueError("alias map missing unknown_name_handling")
    if unh.get("resolution") != UNKNOWN_NAME_RESOLUTION_UNMAPPED:
        raise ValueError(
            f"unknown_name_handling.resolution must be {UNKNOWN_NAME_RESOLUTION_UNMAPPED!r}"
        )


def resolve_intervention_class(normalized_alias: str, lookup: dict[str, str]) -> str | None:
    """Return canonical class ID or ``None`` if unmapped (no guessing)."""
    if not normalized_alias:
        return None
    return lookup.get(normalized_alias)
