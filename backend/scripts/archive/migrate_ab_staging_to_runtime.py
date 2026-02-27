"""
Migrate AB staging SSOT into runtime SSOT (deterministic merge).
Sprint 18: Merge staging biomarkers, aliases, and burden into runtime.
ARCHIVED: Staging folder removed post-migration. Script kept for reference.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _normalize_aliases(aliases: list[str]) -> list[str]:
    """Dedupe and sort aliases, preserving order of first occurrence."""
    seen: set[str] = set()
    out: list[str] = []
    for a in aliases:
        if isinstance(a, str) and a.strip() and a not in seen:
            seen.add(a)
            out.append(a)
    return sorted(out)


def merge_biomarkers(runtime: dict[str, Any], staging: dict[str, Any]) -> dict[str, Any]:
    """Merge staging biomarkers into runtime. Add new; for overlap, keep runtime verbatim."""
    rt_bio = runtime.get("biomarkers") or {}
    st_bio = staging.get("biomarkers") or {}
    merged = dict(rt_bio)

    for bid, st_def in st_bio.items():
        if not isinstance(st_def, dict):
            continue
        if bid not in merged:
            merged[bid] = dict(st_def)
            continue
        # Overlap: keep runtime verbatim (validator requires prod == ab for overlap)
        pass

    return {"biomarkers": merged}


def _norm_alias(a: str) -> str:
    """Normalize alias for collision check (matches alias_registry_service)."""
    return a.strip().lower().replace(" ", "_").replace("-", "_")


def merge_alias_registry(
    runtime: dict[str, Any],
    staging_ab_list: list[dict],
    biomarkers: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge staging ab_full_panel into runtime alias registry.
    Skip staging aliases that would collide with runtime (registry + biomarkers + common_aliases).
    """
    # Build alias -> canonical from runtime registry
    alias_to_canon: dict[str, str] = {}
    canon_to_aliases: dict[str, set[str]] = {}
    for key, entry in runtime.items():
        if not isinstance(entry, dict):
            continue
        cid = entry.get("canonical_id")
        if not isinstance(cid, str):
            continue
        if cid not in canon_to_aliases:
            canon_to_aliases[cid] = set()
        for a in [key] + list(entry.get("aliases") or []):
            if isinstance(a, str) and a.strip():
                canon_to_aliases[cid].add(a)
                for norm in (_norm_alias(a), a.lower(), a.upper()):
                    if norm and norm not in alias_to_canon:
                        alias_to_canon[norm] = cid

    # Collision sources: biomarkers + common_aliases (alias_registry_service merges these at runtime)
    for cid, defn in (biomarkers or {}).items():
        if not isinstance(defn, dict):
            continue
        for a in defn.get("aliases") or []:
            if isinstance(a, str) and a.strip():
                norm = _norm_alias(a)
                if norm not in alias_to_canon:
                    alias_to_canon[norm] = cid

    COMMON_ALIASES = {"sgpt": "alt", "sgot": "ast"}
    for alias, cid in COMMON_ALIASES.items():
        norm = alias.lower()
        if norm not in alias_to_canon:
            alias_to_canon[norm] = cid

    # Add staging aliases only if they don't collide with runtime (registry + biomarkers + common)
    skipped = 0
    for item in staging_ab_list or []:
        if not isinstance(item, dict):
            continue
        cid = item.get("canonical_id")
        aliases = item.get("aliases") or []
        if not isinstance(cid, str):
            continue
        if cid not in canon_to_aliases:
            canon_to_aliases[cid] = set()
        for a in aliases:
            if not isinstance(a, str) or not a.strip():
                continue
            norm = _norm_alias(a)
            existing = alias_to_canon.get(norm)
            if existing is not None and existing != cid:
                skipped += 1
                continue
            canon_to_aliases[cid].add(a)
            alias_to_canon[norm] = cid
    if skipped:
        print(f"[NOTE] Skipped {skipped} staging aliases (collision with runtime)")

    result: dict[str, Any] = {}
    for cid in sorted(canon_to_aliases.keys()):
        aliases = _normalize_aliases(list(canon_to_aliases[cid]))
        result[cid] = {"canonical_id": cid, "aliases": aliases}
    return result


def merge_burden(runtime: dict[str, Any], staging: dict[str, Any]) -> dict[str, Any]:
    """Merge staging burden into runtime. Add new; keep runtime for overlap."""
    rt_bio = runtime.get("biomarkers") or {}
    st_bio = staging.get("biomarkers") or {}
    merged = dict(rt_bio)
    for bid, st_def in st_bio.items():
        if bid not in merged and isinstance(st_def, dict):
            merged[bid] = dict(st_def)
    return {"registry_version": runtime.get("registry_version", "1.0.0"),
            "schema_version": runtime.get("schema_version", "1.0.0"),
            "biomarkers": merged}


def main() -> int:
    print("[ARCHIVED] Staging folder removed. Run from backend/scripts/archive/ for reference only.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
