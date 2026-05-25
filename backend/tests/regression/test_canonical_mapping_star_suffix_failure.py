"""
MAP-R1A — regression guard for star-suffix canonical mapping failure.

Sentinel: canonical_mapping_star_suffix_failure
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.canonical.alias_registry_service import get_alias_registry_service

_REPO_ROOT = Path(__file__).resolve().parents[3]
_ALIAS_SERVICE = _REPO_ROOT / "backend" / "core" / "canonical" / "alias_registry_service.py"
_FRONTEND_UPLOAD = _REPO_ROOT / "frontend" / "app" / "lib" / "uploadReferenceRange.ts"

# d8-style Group A keys (MAP-R1 investigation)
D8_STYLE_STAR_KEYS = [
    "Homocysteine (venous)*",
    "Creatinine (venous)*",
    "Apolipoprotein B (venous)*",
    "Apolipoprotein A1 (venous)*",
    "Lipoprotein (a) (venous)*",
    "Vitamin B12 (venous)*",
    "TSH (venous)*",
    "Corrected Calcium (venous)*",
]

D8_EXPECTED_CANONICAL = {
    "Homocysteine (venous)*": "homocysteine",
    "Creatinine (venous)*": "creatinine",
    "Apolipoprotein B (venous)*": "apob",
    "Apolipoprotein A1 (venous)*": "apoa1",
    "Lipoprotein (a) (venous)*": "lipoprotein_a",
    "Vitamin B12 (venous)*": "vitamin_b12",
    "TSH (venous)*": "tsh",
    "Corrected Calcium (venous)*": "corrected_calcium",
}


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="module", autouse=True)
def _clear_alias_singleton():
    get_alias_registry_service.cache_clear()
    yield
    get_alias_registry_service.cache_clear()


@pytest.mark.regression
def test_sentinel_canonical_mapping_star_suffix_failure_guard_present() -> None:
    """Sentinel: canonical_mapping_star_suffix_failure."""
    src = _read(_ALIAS_SERVICE)
    assert "_strip_abnormal_lab_marker_suffix" in src
    assert "cleaned = self._strip_abnormal_lab_marker_suffix(raw)" in src


@pytest.mark.regression
def test_frontend_defence_in_depth_present() -> None:
    src = _read(_FRONTEND_UPLOAD)
    assert "stripAbnormalLabMarkerSuffix" in src
    assert "stripAbnormalLabMarkerSuffix(displayName)" in src


@pytest.mark.regression
@pytest.mark.parametrize("label", D8_STYLE_STAR_KEYS)
def test_d8_style_keys_do_not_become_unmapped(label: str) -> None:
    resolver = get_alias_registry_service()
    canonical = resolver.resolve(label)
    assert canonical == D8_EXPECTED_CANONICAL[label]
    assert not canonical.startswith("unmapped_")


@pytest.mark.regression
def test_homocysteine_enters_canonical_path_not_truncated() -> None:
    resolver = get_alias_registry_service()
    assert resolver.resolve("Homocysteine (venous)*") == "homocysteine"
    assert resolver.is_canonical("homocysteine")


@pytest.mark.regression
def test_f2_clean_label_path_unchanged() -> None:
    resolver = get_alias_registry_service()
    assert resolver.resolve("Homocysteine (venous)") == "homocysteine"
    assert resolver.resolve("Transferrin (venous)") == "transferrin"
