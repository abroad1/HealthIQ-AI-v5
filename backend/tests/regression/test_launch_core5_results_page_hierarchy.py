"""
LAUNCH-CORE-5 — Results page narrative hierarchy regression guards.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_JOURNEY_ORDER_MODULE = _REPO_ROOT / "frontend" / "app" / "lib" / "feR2ResultsJourneyOrder.ts"
_STALE_BANNER = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "StaleResultBanner.tsx"
_FER6A = _REPO_ROOT / "frontend" / "app" / "lib" / "feR6aRetailCopy.ts"

_EXPECTED_JOURNEY_IDS = [
    "fe-r2-journey-body-overview",
    "fe-r2-journey-primary-finding",
    "fe-r2-journey-working-well",
    "fe-r2-journey-health-systems",
    "fe-r2-journey-uncertainty",
    "fe-r5a-journey-patterns-across-body",
    "fe-r2-journey-marker-evidence",
    "fe-r2-journey-next-steps",
    "fe-r2-journey-clinician-summary",
]


def _page_src() -> str:
    assert _RESULTS_PAGE.is_file(), "results page missing"
    return _RESULTS_PAGE.read_text(encoding="utf-8")


def _journey_index_positions(src: str) -> list[int]:
    positions: list[int] = []
    for i in range(len(_EXPECTED_JOURNEY_IDS)):
        needle = f"FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[{i}]"
        assert needle in src, f"{needle} missing from results page"
        positions.append(src.index(needle))
    return positions


@pytest.mark.regression
def test_lc5_journey_module_exports_canonical_order() -> None:
    mod = _JOURNEY_ORDER_MODULE.read_text(encoding="utf-8")
    for tid in _EXPECTED_JOURNEY_IDS:
        assert tid in mod


@pytest.mark.regression
def test_lc5_primary_finding_before_working_well_and_health_systems() -> None:
    src = _page_src()
    positions = _journey_index_positions(src)
    assert positions == sorted(positions), "LC-5 journey sections out of order on results page"
    assert positions[1] < positions[2] < positions[3], (
        "primary finding must precede working well and health systems cards"
    )


@pytest.mark.regression
def test_lc5_stale_banner_includes_incompatible_status() -> None:
    src = _STALE_BANNER.read_text(encoding="utf-8")
    assert "incompatible" in src
    assert "stale" in src
    assert "regenerat" not in src.lower() or "regeneration_available" in src


@pytest.mark.regression
def test_lc5_marker_numeric_score_hidden_from_default_retail_sanitize() -> None:
    src = _FER6A.read_text(encoding="utf-8")
    assert "isMarkerNumericScoreInterpretation" in src
    assert "MARKER_NUMERIC_SCORE_INTERPRETATION_RE" in src
    assert "biomarkerInterpretationForDetail" in src
