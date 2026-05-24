"""
FE-R6A — Fresh UAT defect cleanup regression.

Sentinel defect classes (escaped_defects_v1.json):
  fresh_uat_instruction_wrapper_visible
  fresh_uat_duplicate_summary_visible
  fresh_uat_pattern_counter_contradiction
  fresh_uat_interpretation_confidence_leak
  fresh_uat_linked_to_internal_label_visible
  fresh_uat_next_steps_rendering_artifact
  fresh_uat_raw_scoring_error_visible
  fresh_uat_thin_lead_marker_expansion
  fresh_uat_finding_label_mismatch
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_BIOMARKER_DIALS = _REPO_ROOT / "frontend" / "app" / "components" / "biomarkers" / "BiomarkerDials.tsx"
_UPLOADED_FIDELITY = _REPO_ROOT / "frontend" / "app" / "components" / "biomarkers" / "UploadedPanelFidelity.tsx"
_NARRATIVE_SURFACE = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "DeterministicNarrativeSurface.tsx"
_ACTION_CARDS = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "ResultsHeroBlocks.tsx"
_FE_R6A_LIB = _REPO_ROOT / "frontend" / "app" / "lib" / "feR6aRetailCopy.ts"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


@pytest.mark.regression
def test_fe_r6a_no_how_to_read_page_wrapper_h2() -> None:
    """Sentinel: fresh_uat_instruction_wrapper_visible."""
    src = _read(_RESULTS_PAGE)
    assert "How to read this page" not in src
    assert 'id="fe-r2-body-overview-heading"' in src or "Your body overview" in src


@pytest.mark.regression
def test_fe_r6a_duplicate_summary_removed_from_journey() -> None:
    """Sentinel: fresh_uat_duplicate_summary_visible."""
    src = _read(_RESULTS_PAGE)
    assert "NarrativeRetailSummaryCard" not in src
    assert 'data-testid="narrative-retail-summary"' not in src


@pytest.mark.regression
def test_fe_r6a_pattern_buckets_gated_from_retail() -> None:
    """Sentinel: fresh_uat_pattern_counter_contradiction."""
    body = _read(_REPO_ROOT / "frontend" / "app" / "components" / "results" / "ResultsBodyOverview.tsx")
    assert "showPatternGroupBuckets" in body
    page = _read(_RESULTS_PAGE)
    assert "showPatternGroupBuckets={showDetails}" in page


@pytest.mark.regression
def test_fe_r6a_interpretation_confidence_scrubbed() -> None:
    """Sentinel: fresh_uat_interpretation_confidence_leak."""
    lib = _read(_FE_R6A_LIB)
    assert "interpretation confidence for this read" in lib
    balanced = _read(_REPO_ROOT / "frontend" / "app" / "components" / "results" / "BalancedSystemsSummary.tsx")
    assert "scrubBalancedSystemsEvidenceLine" in balanced


@pytest.mark.regression
def test_fe_r6a_no_linked_to_labels_in_upload_panel() -> None:
    """Sentinel: fresh_uat_linked_to_internal_label_visible."""
    src = _read(_UPLOADED_FIDELITY)
    assert "Linked to" not in src


@pytest.mark.regression
def test_fe_r6a_next_steps_list_markup() -> None:
    """Sentinel: fresh_uat_next_steps_rendering_artifact."""
    src = _read(_NARRATIVE_SURFACE)
    assert "narrative-next-steps-list" in src
    assert "<ul" in src


@pytest.mark.regression
def test_fe_r6a_no_packaged_fallback_in_action_cards() -> None:
    """Sentinel: fresh_uat_next_steps_rendering_artifact."""
    src = _read(_ACTION_CARDS)
    assert "No separate checklist of follow-up lines was packaged" not in src


@pytest.mark.regression
def test_fe_r6a_raw_scoring_error_sanitized() -> None:
    """Sentinel: fresh_uat_raw_scoring_error_visible."""
    lib = _read(_FE_R6A_LIB)
    assert "BIOMARKER_UNSCORED_CONSUMER_MESSAGE" in lib
    dials = _read(_BIOMARKER_DIALS)
    assert "sanitizeBiomarkerInterpretationForRetail" in dials
    assert "Not scored - result unit and lab reference range unit cannot be aligned" not in dials


@pytest.mark.regression
def test_fe_r6a_biomarker_limited_state_when_thin() -> None:
    """Sentinel: fresh_uat_thin_lead_marker_expansion."""
    dials = _read(_BIOMARKER_DIALS)
    assert "biomarker-detail-limited-state" in dials
    assert "BIOMARKER_LIMITED_STATE_MESSAGE" in dials
    assert "retailInterpretationForExpansion" in dials


@pytest.mark.regression
def test_fe_r6a_primary_finding_lead_pattern_bridge() -> None:
    """Sentinel: fresh_uat_finding_label_mismatch."""
    page = _read(_RESULTS_PAGE)
    primary = _read(_REPO_ROOT / "frontend" / "app" / "components" / "results" / "PrimaryFindingAndWhy.tsx")
    assert "leadPatternLabel" in page
    assert "primary-finding-lead-pattern-bridge" in primary


@pytest.mark.regression
def test_fe_r6a_fe_r5a_journey_preserved() -> None:
    order = _read(_REPO_ROOT / "frontend" / "app" / "lib" / "feR2ResultsJourneyOrder.ts")
    assert "fe-r5a-journey-patterns-across-body" in order
    page = _read(_RESULTS_PAGE)
    assert "FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]" in page
    assert "InterpretationPatternsSection" in page
    marker = page.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    advanced = page.index('data-testid="section-advanced"')
    assert marker < advanced
