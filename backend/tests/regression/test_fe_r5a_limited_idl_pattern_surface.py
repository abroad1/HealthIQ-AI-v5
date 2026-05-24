"""
FE-R5A — Limited IDL pattern surface regression.

Sentinel defect classes (escaped_defects_v1.json):
  patterns_section_missing_when_idl_safe
  patterns_section_wrong_journey_position
  raw_cluster_name_used_as_pattern_label
  unsafe_pattern_taxonomy_visible
  patterns_section_placeholder_visible
  fe_r3_marker_evidence_regressed
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_PATTERNS_COMPONENT = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "InterpretationPatternsSection.tsx"
_GUARDS_MODULE = _REPO_ROOT / "frontend" / "app" / "lib" / "feR5aIdlPatternGuards.ts"
_JOURNEY_ORDER = _REPO_ROOT / "frontend" / "app" / "lib" / "feR2ResultsJourneyOrder.ts"

_PLACEHOLDER_PATTERNS = (
    re.compile(r"no patterns found", re.I),
    re.compile(r"patterns unavailable", re.I),
    re.compile(r"coming soon", re.I),
)

_UNSAFE_TAXONOMY_IN_UI = (
    re.compile(r"risk_construct"),
    re.compile(r"syndrome_state"),
    re.compile(r"organ_pattern"),
    re.compile(r"\bIDL\b"),
    re.compile(r"\bcluster\b", re.I),
)


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


@pytest.mark.regression
def test_fe_r5a_journey_order_includes_patterns_slot() -> None:
    """Sentinel: patterns_section_wrong_journey_position."""
    mod = _read(_JOURNEY_ORDER)
    assert "fe-r5a-journey-patterns-across-body" in mod
    ids = mod[mod.index("[") : mod.index("]") + 1] if "[" in mod else ""
    assert "fe-r5a-journey-patterns-across-body" in _read(_JOURNEY_ORDER)


@pytest.mark.regression
def test_fe_r5a_patterns_after_uncertainty_before_markers() -> None:
    """Sentinel: patterns_section_wrong_journey_position."""
    src = _read(_RESULTS_PAGE)
    uncertainty = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[3]")
    patterns = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[4]")
    markers = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    assert uncertainty < patterns < markers
    assert "showRetailIdlPatterns" in src
    assert "selectSafeIdlPatternRecords" in src


@pytest.mark.regression
def test_fe_r5a_renders_from_idl_only_not_clusters() -> None:
    """Sentinel: raw_cluster_name_used_as_pattern_label."""
    page = _read(_RESULTS_PAGE)
    comp = _read(_PATTERNS_COMPONENT)
    assert "InterpretationPatternsSection" in page
    assert "interpretation_display_layer_v1" in page
    assert "clusters[" not in comp
    assert "cluster.name" not in comp
    assert "selectSafeIdlPatternRecords" in page


@pytest.mark.regression
def test_fe_r5a_no_placeholder_when_empty() -> None:
    """Sentinel: patterns_section_placeholder_visible."""
    comp = _read(_PATTERNS_COMPONENT)
    page = _read(_RESULTS_PAGE)
    for pat in _PLACEHOLDER_PATTERNS:
        assert not pat.search(comp), pat.pattern
        assert not pat.search(page), pat.pattern
    assert "return null" in comp


@pytest.mark.regression
def test_fe_r5a_scientific_class_consumer_chip_not_raw_enum() -> None:
    """Sentinel: unsafe_pattern_taxonomy_visible."""
    comp = _read(_PATTERNS_COMPONENT)
    guards = _read(_GUARDS_MODULE)
    assert "idl-scientific-class-chip" in comp
    assert "formatScientificClassChipLabel" in guards
    ui_slice = comp[comp.index("return (") :]
    for pat in _UNSAFE_TAXONOMY_IN_UI:
        assert not pat.search(ui_slice), pat.pattern


@pytest.mark.regression
def test_fe_r5a_idl_not_duplicated_in_secondary_disclosure() -> None:
    src = _read(_RESULTS_PAGE)
    secondary = src[src.index('data-testid="section-patterns-secondary"'): src.index('data-testid="section-interpretation-context"')]
    assert "InterpretationPatternsSection" not in secondary


@pytest.mark.regression
def test_fe_r5a_unsafe_label_guard_module() -> None:
    """Sentinel: raw_cluster_name_used_as_pattern_label."""
    guards = _read(_GUARDS_MODULE)
    assert "Cardiovascular" in guards or "cardiovascular" in guards.lower()
    assert "isUnsafePatternRetailLabel" in guards


@pytest.mark.regression
def test_fe_r5a_marker_evidence_still_in_journey() -> None:
    """Sentinel: fe_r3_marker_evidence_regressed."""
    src = _read(_RESULTS_PAGE)
    marker = src.index("FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]")
    advanced = src.index('data-testid="section-advanced"')
    assert marker < advanced
    assert "<BiomarkerDials" in src[marker:advanced]


@pytest.mark.regression
def test_fe_r5a_fe_r4_gate_doc_on_main() -> None:
    gate = _REPO_ROOT / "docs/audit-papers/FE-R4_patterns_layer_gate_and_implementation_decision.md"
    assert gate.is_file()
