"""
LC-S11A — Launch-core trust blocker correction regression.

Guards four forensic UAT defects: legacy insights[] placeholders, unsupported blood-sugar
narrative, ApoA1 elevated misclassified as cardio risk, low ALT liver false alarm.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pytest

from core.analytics.domain_narrative_wave1 import met_contributor_primary
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.scoring.rules import ScoringRules
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)

_LEGACY_INSIGHT_PLACEHOLDER = re.compile(
    r"summarise structured signals",
    re.IGNORECASE,
)
_EARLY_IR_COPY = re.compile(r"early impaired sugar and lipid handling", re.IGNORECASE)
_INTERNAL_SPRINT_STRING = re.compile(r"deferred_sprint|_deferred_sprint", re.IGNORECASE)
_RAW_SIGNAL_ID = re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE)


def _harmonise_test_panel_units(biomarkers: Dict[str, Any]) -> None:
    """Test harness: align Greek-mu urate units with registry base µmol/L (LC-S8F scope unchanged)."""
    for entry in biomarkers.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("unit") == "\u03bcmol/L":
            entry["unit"] = "\u00b5mol/L"
        rr = entry.get("reference_range")
        if isinstance(rr, dict) and rr.get("unit") == "\u03bcmol/L":
            rr["unit"] = "\u00b5mol/L"


def _prepare_ab_fixture_panel() -> Dict[str, Any]:
    raw = json.loads(_AB_PANEL.read_text(encoding="utf-8"))
    biomarkers = dict(raw["biomarkers"])
    _harmonise_test_panel_units(biomarkers)
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def _run_ab_baseline() -> Any:
    orchestrator = AnalysisOrchestrator()
    return orchestrator.run(
        _prepare_ab_fixture_panel(),
        {"age": 45, "sex": "male"},
        assume_canonical=True,
    )


def _blood_sugar_domain(dto: Any) -> Dict[str, Any]:
    for row in dto.consumer_domain_scores or []:
        if getattr(row, "domain_id", None) == "wave1_blood_sugar":
            return row.model_dump() if hasattr(row, "model_dump") else dict(row)
    pytest.fail("wave1_blood_sugar domain missing")


def _liver_domain(dto: Any) -> Dict[str, Any]:
    for row in dto.consumer_domain_scores or []:
        if getattr(row, "domain_id", None) == "wave1_liver":
            return row.model_dump() if hasattr(row, "model_dump") else dict(row)
    pytest.fail("wave1_liver domain missing")


def _user_facing_consumer_chunks(dto: Any) -> List[str]:
    chunks: List[str] = []
    for row in dto.consumer_domain_scores or []:
        d = row.model_dump() if hasattr(row, "model_dump") else dict(row)
        for key in (
            "headline_sentence",
            "contributor_sentence",
            "confidence_sentence",
            "consequence_sentence",
            "next_step_sentence",
            "evidence_anchor_sentence",
        ):
            chunks.append(str(d.get(key) or ""))
        refs = d.get("raw_evidence_refs") or {}
        if isinstance(refs, dict):
            chunks.append(json.dumps(refs))
    return chunks


@pytest.mark.regression
def test_lc_s11a_no_legacy_insights_placeholder_in_dto() -> None:
    dto = _run_ab_baseline()
    for insight in dto.insights or []:
        title = getattr(insight, "title", "") or ""
        desc = getattr(insight, "description", "") or ""
        assert not _LEGACY_INSIGHT_PLACEHOLDER.search(title), title
        assert not _LEGACY_INSIGHT_PLACEHOLDER.search(desc), desc
        biomarkers = getattr(insight, "biomarkers", None) or []
        assert biomarkers, "non-placeholder insights must cite biomarkers"


@pytest.mark.regression
def test_lc_s11a_blood_sugar_no_unsupported_early_ir_narrative() -> None:
    dto = _run_ab_baseline()
    met = _blood_sugar_domain(dto)
    assert met.get("active_signal_ids") == []
    contrib = str(met.get("contributor_sentence") or "")
    assert not _EARLY_IR_COPY.search(contrib), contrib
    assert "glucose and insulin were not included" in contrib.lower()


@pytest.mark.regression
def test_lc_s11a_elevated_apoa1_not_active_cardio_risk_signal() -> None:
    dto = _run_ab_baseline()
    ig = (dto.meta or {}).get("insight_graph") or {}
    states = {
        str(r.get("signal_id", "")): str(r.get("signal_state", ""))
        for r in (ig.get("signal_results") or [])
        if isinstance(r, dict)
    }
    apoa_state = states.get("signal_apoa1_cardio_risk")
    assert apoa_state in (None, "", "optimal", "unknown"), apoa_state

    drivers = ((dto.meta or {}).get("wave1_aligned_drivers") or {}).get("biomarker_keys") or []
    assert "apoa1" not in drivers


@pytest.mark.regression
def test_lc_s11a_low_alt_does_not_alarm_liver_domain() -> None:
    dto = _run_ab_baseline()
    liver = _liver_domain(dto)
    score_100 = float(liver.get("score", 0)) * 100.0
    assert score_100 >= 45.0, f"liver score too low: {score_100}"
    assert liver.get("band_label") != "review"
    headline = str(liver.get("headline_sentence") or "").lower()
    assert "deserve closer review" not in headline


@pytest.mark.regression
def test_lc_s11a_homocysteine_lead_finding_unchanged() -> None:
    dto = _run_ab_baseline()
    ig = (dto.meta or {}).get("insight_graph") or {}
    report = ig.get("report_v1") or {}
    if hasattr(report, "model_dump"):
        report = report.model_dump()
    top = report.get("top_findings") or []
    lead_sid = ""
    if top and isinstance(top[0], dict):
        lead_sid = str(top[0].get("signal_id") or "")
    nr = dto.narrative_report_v1
    retail = ""
    if nr is not None:
        retail = str(getattr(nr, "retail_summary", "") or "")
    assert "homocysteine" in lead_sid.lower() or "homocysteine" in retail.lower()


@pytest.mark.regression
def test_lc_s11a_no_internal_sprint_strings_in_consumer_domain_scores() -> None:
    dto = _run_ab_baseline()
    for text in _user_facing_consumer_chunks(dto):
        assert not _INTERNAL_SPRINT_STRING.search(text), text


@pytest.mark.regression
def test_lc_s11a_no_raw_signal_ids_in_consumer_domain_sentences() -> None:
    dto = _run_ab_baseline()
    for text in _user_facing_consumer_chunks(dto):
        assert not _RAW_SIGNAL_ID.search(text), text


def test_lc_s11a_met_contributor_primary_honest_when_no_active_signals() -> None:
    out = met_contributor_primary({}, set(), [], None)
    assert "glucose and insulin were not included" in out.lower()
    assert not _EARLY_IR_COPY.search(out)


def test_lc_s11a_apoa1_evaluator_skips_upper_bound_when_disabled() -> None:
    reg = SignalRegistry()
    ev = SignalEvaluator(reg)
    signal = {
        "activation_config": {
            "enable_upper_bound": False,
            "enable_lower_bound": True,
            "lower_bound_state": "suboptimal",
        },
    }
    lab_ranges = {"apoa1": {"min": 0.79, "max": 1.69}}
    high = ev._evaluate_lab_range_activation_state(signal, "apoa1", 1.73, lab_ranges)  # noqa: SLF001
    low = ev._evaluate_lab_range_activation_state(signal, "apoa1", 0.5, lab_ranges)  # noqa: SLF001
    assert high is None
    assert low == "suboptimal"


def test_lc_s11a_low_alt_lab_range_scores_non_critical() -> None:
    rules = ScoringRules()
    ref = {"min": 10.0, "max": 49.0, "unit": "U/L", "source": "lab"}
    score, score_range, unscored = rules.calculate_biomarker_score(
        "alt", 7.0, input_reference_range=ref
    )
    assert unscored is None
    assert float(score) >= 45.0
    from core.scoring.rules import ScoreRange

    assert score_range != ScoreRange.CRITICAL


def test_lc_s11a_high_alt_still_scores_concerning() -> None:
    rules = ScoringRules()
    ref = {"min": 10.0, "max": 49.0, "unit": "U/L", "source": "lab"}
    score, score_range, unscored = rules.calculate_biomarker_score(
        "alt", 120.0, input_reference_range=ref
    )
    assert unscored is None
    assert float(score) < 70.0
