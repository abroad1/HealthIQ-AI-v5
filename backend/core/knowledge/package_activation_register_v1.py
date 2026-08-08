"""
ARCH-CONV-E / V5-CANONICAL-ACTIVATION-GATE-2 — governed runtime activation boundary.

Placement of a package under ``knowledge_bus/packages/`` is a promotion act, not an
activation act. A governed frame becomes production-reachable only when its
``activation_key`` is listed in the governed activation register.

Launch-critical (``pkg_kb47_*``) frames are included in the register after Stage 2
fold-in. Provenance/lineage eligibility remains a mandatory prerequisite/veto in
``package_runtime_eligibility_v1`` and must not independently grant activation.

Fail closed: a missing or malformed register raises rather than admitting every package
on disk into the production registry.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, FrozenSet, Optional

import yaml

#: Runtime-eligibility label recorded on audit surfaces for unactivated frames.
RUNTIME_STATE_NOT_ACTIVATED = "NOT_RUNTIME_ACTIVATED"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def activation_register_path() -> Path:
    return (
        _repo_root()
        / "knowledge_bus"
        / "governance"
        / "package_runtime_activation_register_v1.yaml"
    )


@lru_cache(maxsize=1)
def load_activation_register() -> Dict[str, Any]:
    path = activation_register_path()
    if not path.is_file():
        raise FileNotFoundError(f"missing runtime activation register: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("runtime activation register root must be a mapping")
    frames = payload.get("activated_frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("runtime activation register activated_frames must be a non-empty list")

    keys: set[str] = set()
    packages: set[str] = set()
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("activated frame row must be a mapping")
        key = str(row.get("activation_key") or "").strip()
        package_id = str(row.get("package_id") or "").strip()
        if not key or not package_id:
            raise ValueError("activated frame requires activation_key and package_id")
        if key in keys:
            raise ValueError(f"duplicate activation_key in runtime activation register: {key}")
        keys.add(key)
        packages.add(package_id)

    declared = payload.get("activated_frame_count")
    if isinstance(declared, int) and declared != len(keys):
        raise ValueError(
            f"activated_frame_count {declared} does not match {len(keys)} activated frames"
        )

    resolved = dict(payload)
    resolved["_activated_activation_keys"] = frozenset(keys)
    resolved["_activated_package_ids"] = frozenset(packages)
    return resolved


def clear_activation_register_cache() -> None:
    load_activation_register.cache_clear()


def activated_activation_keys() -> FrozenSet[str]:
    return load_activation_register()["_activated_activation_keys"]


def activated_package_ids() -> FrozenSet[str]:
    return load_activation_register()["_activated_package_ids"]


def is_activation_key_activated(activation_key: str) -> bool:
    key = str(activation_key or "").strip()
    if not key:
        return False
    return key in activated_activation_keys()


def is_package_runtime_activated(package_id: str) -> bool:
    """True when the package contributes at least one explicitly activated frame."""
    pid = str(package_id or "").strip()
    if not pid:
        return False
    return pid in activated_package_ids()


def frame_activation_exclusion_reason(activation_key: str) -> Optional[str]:
    if is_activation_key_activated(activation_key):
        return None
    return RUNTIME_STATE_NOT_ACTIVATED
