"""
FE-R2 — Results journey restructure regression.

Sentinel defect classes (escaped_defects_v1.json):
  retail_results_journey_wrong_order
  body_overview_not_first
  working_well_section_missing_or_late
  biomarker_evidence_hidden_in_advanced_only
  clinician_language_in_retail_flow
  results_page_accordion_dominated
  duplicate_what_this_means_heading
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_JOURNEY_ORDER_MODULE = _REPO_ROOT / "frontend" / "app" / "lib" / "feR2ResultsJourneyOrder.ts"

_EXPECTED_JOURNEY_IDS = [
    "fe-r2-journey-body-overview",
    "fe-r2-journey-working-well",
    "fe-r2-journey-primary-finding",
    "fe-r2-journey-uncertainty",
    "fe-r5a-journey-patterns-across-body",
    "fe-r2-journey-marker-evidence",
    "fe-r2-journey-next-steps",
    "fe-r2-journey-clinician-summary",
]

_RETAIL_BANNED_HEADINGS = (
    "clinician-structured",
    "what this means",
)

_ADVANCED_ONLY_MARKER_BLOCK_RE = re.compile(
    r'data-testid="section-advanced"[\s\S]*?'
    r'<BiomarkerDials',
    re.IGNORECASE,
)


def _page_src() -> str:
    assert _RESULTS_PAGE.is_file(), "results page missing"
    return _RESULTS_PAGE.read_text(encoding="utf-8")


def _journey_index_positions(src: str) -> list[int]:
    """Page binds journey sections via FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[i]."""
    positions: list[int] = []
    for i in range(len(_EXPECTED_JOURNEY_IDS)):
        needle = f"FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[{i}]"
        assert needle in src, f"{needle} missing from results page"
        positions.append(src.index(needle))
    return positions


@pytest.mark.regression
def test_fe_r2_journey_module_exports_canonical_order() -> None:
    mod = _JOURNEY_ORDER_MODULE.read_text(encoding="utf-8")
    for tid in _EXPECTED_JOURNEY_IDS:
        assert tid in mod


@pytest.mark.regression
def test_fe_r2_results_page_section_order() -> None:
    """Sentinel: retail_results_journey_wrong_order, body_overview_not_first."""
    src = _page_src()
    positions = _journey_index_positions(src)
    assert positions == sorted(positions), "FE-R2 journey sections out of order on results page"
    assert positions[0] == min(positions), "body overview must be first in retail journey"


@pytest.mark.regression
def test_fe_r2_working_well_before_primary_finding() -> None:
    """Sentinel: working_well_section_missing_or_late."""
    src = _page_src()
    positions = _journey_index_positions(src)
    assert positions[1] < positions[2] < positions[3] < positions[4] < positions[5]


@pytest.mark.regression
def test_fe_r2_biomarker_evidence_not_advanced_only() -> None:
    """Sentinel: biomarker_evidence_hidden_in_advanced_only."""
    src = _page_src()
    marker_journey = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    advanced = src.index('data-testid="section-advanced"')
    assert marker_journey < advanced, "marker evidence must appear before advanced disclosure"
    assert "<BiomarkerDials" in src[marker_journey:advanced]
    assert not _ADVANCED_ONLY_MARKER_BLOCK_RE.search(src), (
        "BiomarkerDials must not live only inside advanced disclosure"
    )


@pytest.mark.regression
def test_fe_r2_no_clinician_structured_retail_heading() -> None:
    """Sentinel: clinician_language_in_retail_flow."""
    src = _page_src()
    clinician_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[7]")
    retail = src[:clinician_idx]
    low = retail.lower()
    for banned in _RETAIL_BANNED_HEADINGS:
        assert banned not in low, f"{banned!r} found in retail journey headings/copy"


@pytest.mark.regression
def test_fe_r2_no_duplicate_what_this_means_accordion() -> None:
    """Sentinel: duplicate_what_this_means_heading, results_page_accordion_dominated."""
    src = _page_src()
    assert 'data-testid="section-what-this-means"' not in src
    assert src.count('title="What this means"') == 0
    assert "FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS" in src
    clinician_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[7]")
    retail = src[:clinician_idx]
    assert not re.search(r"defaultOpen(?!\s*=\s*\{false\})", retail), (
        "retail journey must not use open-by-default accordions"
    )


@pytest.mark.regression
def test_fe_r2_fe_r1_merge_precondition_on_main() -> None:
    """FE-R2 requires FE-R1 consumer prose guards on branch ancestry."""
    fe_r1_test = _REPO_ROOT / "backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py"
    fe_r1_notes = _REPO_ROOT / "docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md"
    assert fe_r1_test.is_file(), "FE-R1 regression test missing"
    assert fe_r1_notes.is_file(), "FE-R1 notes missing"
