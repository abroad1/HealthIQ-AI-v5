"""
FE-R3 — Evidence depth and UX quality regression.

Sentinel defect classes (escaped_defects_v1.json):
  biomarker_contribution_context_not_surfaced
  biomarker_educational_explainer_not_surfaced
  biomarker_expansion_placeholder_visible
  biomarker_display_unit_regression
  action_rationale_missing_when_available
  next_steps_duplicate_visible
  frontend_clinical_inference_added
  fe_r2_journey_order_regressed
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_BIOMARKER_DIALS = _REPO_ROOT / "frontend" / "app" / "components" / "biomarkers" / "BiomarkerDials.tsx"
_FE_R3_NEXT_STEPS = _REPO_ROOT / "frontend" / "app" / "lib" / "feR3NextStepsLayout.ts"
_CONFIRMATORY_BLOCK = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "ConfirmatoryTestsNextSteps.tsx"
_ACTION_CARDS = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "ResultsHeroBlocks.tsx"

_PLACEHOLDER_PATTERNS = (
    re.compile(r"Lorem ipsum", re.I),
    re.compile(r"placeholder\s+text", re.I),
    re.compile(r"coming\s+soon", re.I),
    re.compile(r"education\s+unavailable", re.I),
    re.compile(r"no\s+educational\s+content\s+yet", re.I),
)

_INTERNAL_LABEL_PATTERNS = (
    re.compile(r"moderate_by_default"),
    re.compile(r"\btest_[a-z0-9_]+_v\d+\b", re.I),
    re.compile(r"Source:\s*\{a\.sourceLabel\}"),
)

_FRONTEND_CONVERSION_RE = re.compile(
    r"display_value\s*\*|/\s*display_unit|convertUnit|unitConversion|mmolToMg",
    re.I,
)


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


@pytest.mark.regression
def test_fe_r3_biomarker_dials_surfaces_contribution_context_heading() -> None:
    """Sentinel: biomarker_contribution_context_not_surfaced."""
    src = _read(_BIOMARKER_DIALS)
    assert "contribution_context" in src or "contributionContext" in src
    assert "How this fits the wider pattern" in src
    assert "biomarker-detail-contribution-context" in src


@pytest.mark.regression
def test_fe_r3_biomarker_dials_surfaces_educational_explainer_collapsed() -> None:
    """Sentinel: biomarker_educational_explainer_not_surfaced."""
    src = _read(_BIOMARKER_DIALS)
    assert "educationalExplainer" in src
    assert "General marker education" in src
    assert "biomarker-detail-educational-explainer" in src
    assert "<details" in src


@pytest.mark.regression
def test_fe_r3_biomarker_expansion_no_placeholder_copy() -> None:
    """Sentinel: biomarker_expansion_placeholder_visible."""
    src = _read(_BIOMARKER_DIALS)
    for pat in _PLACEHOLDER_PATTERNS:
        assert not pat.search(src), f"placeholder pattern {pat.pattern!r} in BiomarkerDials"


@pytest.mark.regression
def test_fe_r3_results_page_preserves_display_value_unit_mapping() -> None:
    """Sentinel: biomarker_display_unit_regression."""
    src = _read(_RESULTS_PAGE)
    assert "display_value" in src
    assert "display_unit" in src
    assert "display_label" in src
    assert not _FRONTEND_CONVERSION_RE.search(src), "frontend unit conversion suspected on results page"


@pytest.mark.regression
def test_fe_r3_confirmatory_rationale_renderable_in_next_steps() -> None:
    """Sentinel: action_rationale_missing_when_available."""
    src = _read(_CONFIRMATORY_BLOCK)
    assert "rationale" in src
    assert "display_name" in src
    assert "fe-r3-confirmatory-next-steps" in src


@pytest.mark.regression
def test_fe_r3_next_steps_dedup_helper_wired() -> None:
    """Sentinel: next_steps_duplicate_visible."""
    page = _read(_RESULTS_PAGE)
    lib = _read(_FE_R3_NEXT_STEPS)
    assert "dedupeActionCardsAgainstNarrative" in lib
    assert "dedupeActionCardsAgainstNarrative" in page
    assert "omitConfirmatoryInClarify" in page
    assert "hideConfirmatoryTests" in page


@pytest.mark.regression
def test_fe_r3_no_internal_labels_on_action_cards() -> None:
    """Sentinel: next_steps_duplicate_visible (internal label leak)."""
    src = _read(_ACTION_CARDS)
    for pat in _INTERNAL_LABEL_PATTERNS:
        assert not pat.search(src), f"internal label pattern {pat.pattern!r} in action cards"


@pytest.mark.regression
def test_fe_r3_biomarker_interpretation_separate_from_education() -> None:
    """Sentinel: frontend_clinical_inference_added (education mis-labelled as personalised)."""
    src = _read(_BIOMARKER_DIALS)
    assert "What this result means now" in src
    assert "not a personalised diagnosis" in src
    # Educational body must not be the sole content under the interpretation heading.
    assert not re.search(
        r"What this result means now[\s\S]{0,120}educationalExplainer\?\.body",
        src,
    )


@pytest.mark.regression
def test_fe_r3_fe_r2_journey_order_preserved() -> None:
    """Sentinel: fe_r2_journey_order_regressed."""
    src = _read(_RESULTS_PAGE)
    assert "FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS" in src
    patterns_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[4]")
    marker_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    next_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[6]")
    clinician_idx = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[7]")
    assert patterns_idx < marker_idx < next_idx < clinician_idx
    assert "<BiomarkerDials" in src[marker_idx:next_idx]


@pytest.mark.regression
def test_fe_r3_biomarker_evidence_in_retail_journey() -> None:
    src = _read(_RESULTS_PAGE)
    advanced = src.index('data-testid="section-advanced"')
    marker_journey = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    assert marker_journey < advanced
