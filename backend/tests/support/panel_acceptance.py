"""
Single import surface for governed AB/VR acceptance fixture paths (KB-S53-ABVR-HARNESS).

Authority file: tests/fixtures/panels/panel_acceptance_profiles_v1.yaml
Acceptance criteria: docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_TESTS_ROOT = Path(__file__).resolve().parent.parent
_FIXTURES_ROOT = _TESTS_ROOT / "fixtures"
_MANIFEST_PATH = _FIXTURES_ROOT / "panels" / "panel_acceptance_profiles_v1.yaml"


@lru_cache(maxsize=1)
def _manifest() -> dict[str, Any]:
    raw = yaml.safe_load(_MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("panel_acceptance_profiles_v1.yaml must parse to a mapping")
    return raw


def manifest_path() -> Path:
    return _MANIFEST_PATH


def fixture_root() -> Path:
    return _FIXTURES_ROOT


def path_for_profile(profile_id: str) -> Path:
    data = _manifest()
    profiles = data.get("profiles") or {}
    entry = profiles.get(profile_id)
    if not isinstance(entry, dict):
        raise KeyError(f"Unknown profile_id: {profile_id!r}")
    rel = str(entry.get("fixture_path", "")).strip()
    if not rel:
        raise KeyError(f"profile {profile_id!r} missing fixture_path")
    path = (_FIXTURES_ROOT / rel).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Fixture missing for {profile_id}: {path}")
    return path


def _ab_path() -> Path:
    return path_for_profile("ab_acceptance")


def _vr_path() -> Path:
    return path_for_profile("vr_acceptance")


# Module-level paths for test imports (evaluated at first use via functions for lazy load)
def ab_acceptance_fixture_path() -> Path:
    return _ab_path()


def vr_acceptance_fixture_path() -> Path:
    return _vr_path()


def golden_panel_160_path() -> Path:
    return path_for_profile("golden_panel_160")


def ab_lab_reference_profile_fixture_path() -> Path:
    return path_for_profile("ab_lab_reference_profile_variant")


def acceptance_harness_fixture_paths() -> tuple[Path, Path]:
    """(AB acceptance, VR acceptance) in stable manifest order."""
    return (_ab_path(), _vr_path())


