"""
INTERNAL-UAT-RESULTS-TRUST-HARDENING-1 — high-trust results page coherence regressions.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.analytics.lifestyle_consumer_surface_v1 import _metabolic_modifier_paragraph
from core.analytics.report_compiler_v1 import (
    _neutralise_hypothesis_title_for_counter_evidence,
    _normalise_root_cause_finding,
)
from core.contracts.clinician_report_v1 import EvidenceItem

_REPO_ROOT = Path(__file__).resolve().parents[3]
_FIXTURE = _REPO_ROOT / "backend" / "tests" / "fixtures" / "reports" / "clinician_report_v1_ab.json"


@pytest.mark.regression
def test_iuat_001_hypothesis_title_neutralised_when_b12_counter_evidence() -> None:
    against = [
        EvidenceItem(
            item="B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone.",
            marker_refs=["vitamin_b12"],
        )
    ]
    title = _neutralise_hypothesis_title_for_counter_evidence("B12-associated pattern", against)
    assert title == "Homocysteine-related pattern"
    assert "B12-associated" not in title


@pytest.mark.regression
def test_iuat_001_ab_fixture_hypothesis_neutralises_on_compile_path() -> None:
    raw = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    hyp = raw["sections"]["root_cause"]["hypotheses"][0]
    against = [
        EvidenceItem(
            item=str(item.get("item", "")),
            marker_refs=[str(x) for x in item.get("marker_refs", [])],
        )
        for item in hyp.get("evidence_against", [])
        if isinstance(item, dict)
    ]
    title = _neutralise_hypothesis_title_for_counter_evidence(str(hyp.get("title", "")), against)
    assert title == "Homocysteine-related pattern"


@pytest.mark.regression
def test_iuat_001_compiler_normalise_root_cause_emits_neutral_title() -> None:
    raw = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    root_cause = raw["sections"]["root_cause"]
    finding = _normalise_root_cause_finding(root_cause)
    assert finding.hypotheses
    top = finding.hypotheses[0]
    assert top.title == "Homocysteine-related pattern"
    assert "B12-associated" not in top.title
    assert top.evidence_against
    assert any("B12" in (ev.item or "") for ev in top.evidence_against)


@pytest.mark.regression
def test_iuat_001_b12_title_unchanged_without_counter_evidence() -> None:
    title = _neutralise_hypothesis_title_for_counter_evidence(
        "B12-associated pattern",
        [
            EvidenceItem(
                item="Folate is within range on this panel.",
                marker_refs=["folate"],
            )
        ],
    )
    assert title == "B12-associated pattern"


@pytest.mark.regression
def test_iuat_004_lifestyle_metabolic_paragraph_avoids_analytical_model_wording() -> None:
    lifestyle_artifact = {
        "system_modifiers": {"metabolic": {"capped_total_modifier": 0.05}},
    }
    paragraph = _metabolic_modifier_paragraph(lifestyle_artifact)
    assert paragraph
    assert "analytical model" not in paragraph.lower()
    assert "interpret" in paragraph.lower() or "context" in paragraph.lower()