"""
DOMAIN-UX1A — Wave 1 Health Systems Card scaffold + contract hardening.

Sentinel classes:
  health_system_card_hidden_from_main_journey
  health_system_card_frontend_calculates_evidence_completeness
  health_system_card_clinical_label_visible
  health_system_card_subsystem_placeholder_visible
  health_system_card_internal_language_visible
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.confidence_model_v1 import ConfidenceModelV1

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_WAVE1_CARDS = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "Wave1DomainCards.tsx"
_DISPLAY_LIB = _REPO_ROOT / "frontend" / "app" / "lib" / "wave1HealthSystemCardDisplay.ts"
_ASSEMBLER = _REPO_ROOT / "backend" / "core" / "analytics" / "domain_score_assembler.py"
_MODEL = _REPO_ROOT / "backend" / "core" / "models" / "results.py"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


def _minimal_rows():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 72.0,
                "missing_biomarkers": ["tc_hdl_ratio"],
                "biomarker_scores": [{"biomarker_name": "total_cholesterol"}],
            },
            "metabolic": {
                "overall_score": 68.0,
                "missing_biomarkers": ["insulin"],
                "biomarker_scores": [
                    {"biomarker_name": "glucose"},
                    {"biomarker_name": "hba1c"},
                ],
            },
            "liver": {
                "overall_score": 75.0,
                "missing_biomarkers": [],
                "biomarker_scores": [{"biomarker_name": "alt"}],
            },
        }
    }
    ig = InsightGraphV1(
        analysis_id="ux1a",
        signal_results=[],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}),
    )
    panel = {
        "total_cholesterol",
        "glucose",
        "hba1c",
        "alt",
        "ast",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    return rows


@pytest.mark.regression
def test_wave1_emits_evidence_completeness_fields() -> None:
    for row in _minimal_rows():
        assert isinstance(row.evidence_completeness_numerator, int)
        assert isinstance(row.evidence_completeness_denominator, int)
        assert row.evidence_completeness_numerator <= row.evidence_completeness_denominator
        assert row.evidence_completeness_denominator > 0


@pytest.mark.regression
def test_wave1_plain_english_descriptors() -> None:
    by_id = {r.domain_id: r for r in _minimal_rows()}
    assert by_id["wave1_cardiovascular"].plain_english_descriptor == "Heart, arteries and circulation"
    assert by_id["wave1_blood_sugar"].plain_english_descriptor == "Sugar and insulin balance"
    assert by_id["wave1_liver"].plain_english_descriptor == "Liver strain and processing load"


@pytest.mark.regression
def test_health_system_card_hidden_from_main_journey_sentinel() -> None:
    """Sentinel: health_system_card_hidden_from_main_journey."""
    page = _read(_PAGE)
    cards = _read(_WAVE1_CARDS)
    assert 'data-testid="fe-domain-ux1a-health-systems-cards"' in cards
    assert "embedInJourney" in page
    assert "<Wave1DomainCards" in page
    assert 'title="Health domains"' not in page
    assert page.index("<Wave1DomainCards") < page.index("fe-r2-next-steps-heading")


@pytest.mark.regression
def test_health_system_card_frontend_calculates_evidence_completeness_sentinel() -> None:
    """Sentinel: health_system_card_frontend_calculates_evidence_completeness."""
    cards = _read(_WAVE1_CARDS)
    display = _read(_DISPLAY_LIB)
    assert "evidence_completeness_numerator" in cards
    assert "wave1EvidenceCompletenessLine" in cards
    assert "missing_marker_ids.length" not in cards.split("wave1EvidenceCompletenessLine")[0]
    assert "denominator -" not in display.lower()
    assert "numerator -" not in display.lower()


@pytest.mark.regression
def test_health_system_card_clinical_label_visible_sentinel() -> None:
    """Sentinel: health_system_card_clinical_label_visible."""
    cards = _read(_WAVE1_CARDS)
    assert "clinical_label" not in cards


@pytest.mark.regression
def test_health_system_card_subsystem_placeholder_visible_sentinel() -> None:
    """Sentinel: health_system_card_subsystem_placeholder_visible."""
    cards = _read(_WAVE1_CARDS)
    assert "coming soon" not in cards.lower()
    assert "subsystem" not in cards.lower()


@pytest.mark.regression
def test_health_system_card_internal_language_visible_sentinel() -> None:
    """Sentinel: health_system_card_internal_language_visible."""
    cards = _read(_WAVE1_CARDS)
    for term in ("governed", "compiler", "structured ranking", "Functional read"):
        assert term not in cards
    assert "wave1ScoreReliabilityLabel" in cards


@pytest.mark.regression
def test_assembler_emits_completeness_helper() -> None:
    src = _read(_ASSEMBLER)
    assert "_evidence_completeness_for_rail" in src
    assert "evidence_completeness_numerator" in _read(_MODEL)
