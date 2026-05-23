"""
LC-S13 — Lifestyle propagation, coherence guard, narrative language audit regression.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from core.analytics.domain_narrative_wave1 import (
    _cv_story_conflicts_with_stable_headline,
    _idl_suggests_risk_or_review_led,
)
from core.analytics.lifestyle_consumer_surface_v1 import build_lifestyle_consumer_overview_paragraphs_v1
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)

_RAW_SIGNAL_ID = re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE)
_INTERNAL_BRIDGE_SLUG = re.compile(
    r"alcohol_intake_moderate_or_higher|renal_panel_with_volume|fasting_pattern_with_favourable|rationale_codes",
    re.IGNORECASE,
)
_FORBIDDEN_NARRATIVE = re.compile(
    r"\byour measured\b|\bai-personalised\b|\bpersonalised narrative\b|\bpersonalized narrative\b",
    re.IGNORECASE,
)
_ALL_CLEAR_HEADLINE = re.compile(r"not a simple all-clear", re.IGNORECASE)

_PROFILE_LOW: Dict[str, Any] = {
    "height_cm": 175,
    "weight_kg": 72,
    "waist_circumference_cm": 82,
    "systolic_bp": 118,
    "diastolic_bp": 75,
    "resting_heart_rate": 62,
    "smoking_status": "never",
    "alcohol_units_per_week": 0,
    "sleep_hours": 8.0,
    "fluid_intake_liters": 2.5,
}

_PROFILE_HIGH: Dict[str, Any] = {
    "height_cm": 175,
    "weight_kg": 105,
    "waist_circumference_cm": 108,
    "systolic_bp": 148,
    "diastolic_bp": 92,
    "resting_heart_rate": 82,
    "smoking_status": "current",
    "alcohol_units_per_week": 18,
    "sleep_hours": 5.0,
    "fluid_intake_liters": 0.7,
}

_QUESTIONNAIRE_HIGH: Dict[str, Any] = {
    "vigorous_exercise_days": "5+ days",
    "dietary_pattern": "Intermittent fasting",
}


def _harmonise_test_panel_units(biomarkers: Dict[str, Any]) -> None:
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


def _run_ab(
    lifestyle_inputs: Optional[Dict[str, Any]] = None,
    questionnaire_data: Optional[Dict[str, Any]] = None,
    fixed_analysis_id: str = "lc-s13-ab",
) -> Any:
    orchestrator = AnalysisOrchestrator()
    return orchestrator.run(
        _prepare_ab_fixture_panel(),
        {"age": 45, "sex": "male"},
        assume_canonical=True,
        lifestyle_inputs=lifestyle_inputs,
        questionnaire_data=questionnaire_data,
        fixed_analysis_id=fixed_analysis_id,
    )


def _domain_row(dto: Any, domain_id: str) -> Dict[str, Any]:
    for row in dto.consumer_domain_scores or []:
        did = getattr(row, "domain_id", None) or (row.get("domain_id") if isinstance(row, dict) else None)
        if did == domain_id:
            return row.model_dump() if hasattr(row, "model_dump") else dict(row)
    pytest.fail(f"{domain_id} missing from consumer_domain_scores")


def _user_facing_chunks(dto: Any) -> List[str]:
    chunks: List[str] = []
    body = (dto.narrative_report_v1.body_overview if dto.narrative_report_v1 else "") or ""
    chunks.append(body)
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
    return chunks


def _assert_domain_band_headline_polarity_coherent(row: Dict[str, Any], domain_id: str) -> None:
    band = str(row.get("band_label") or "").strip().lower()
    headline = str(row.get("headline_sentence") or "")
    confidence = str(row.get("confidence_sentence") or "")
    contributor = str(row.get("contributor_sentence") or "")
    consequence = str(row.get("consequence_sentence") or "")
    active = row.get("active_signal_ids") or []
    primary_rec = row.get("primary_recommendation")

    if band not in ("stable", "strong"):
        return
    if not _ALL_CLEAR_HEADLINE.search(headline):
        return
    if "high confidence" not in confidence.lower():
        return
    if active:
        return
    if _idl_suggests_risk_or_review_led(primary_rec):
        return
    if _cv_story_conflicts_with_stable_headline(contributor, consequence):
        return
    pytest.fail(
        f"{domain_id}: stable/high-confidence headline contradicts band without supporting "
        f"signals or contributor conflict (headline={headline[:120]!r})"
    )


@pytest.mark.regression
def test_lc_s13_lifestyle_profiles_produce_visible_body_difference() -> None:
    low = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-low")
    high = _run_ab(
        lifestyle_inputs=_PROFILE_HIGH,
        questionnaire_data=_QUESTIONNAIRE_HIGH,
        fixed_analysis_id="lc-s13-high",
    )
    body_low = (low.narrative_report_v1.body_overview if low.narrative_report_v1 else "") or ""
    body_high = (high.narrative_report_v1.body_overview if high.narrative_report_v1 else "") or ""
    assert body_low != body_high, "contrasting lifestyle profiles must change body_overview"
    assert "current smoking" in body_high.lower() or "moderate alcohol" in body_high.lower(), (
        f"high-risk profile expected governed lifestyle paragraph: {body_high[:400]!r}"
    )


@pytest.mark.regression
def test_lc_s13_lifestyle_modifiers_differ_between_profiles() -> None:
    low = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-mod-low")
    high = _run_ab(lifestyle_inputs=_PROFILE_HIGH, fixed_analysis_id="lc-s13-mod-high")
    low_life = low.lifestyle or {}
    high_life = high.lifestyle or {}
    low_mods = (low_life.get("system_modifiers") or {}) if isinstance(low_life, dict) else {}
    high_mods = (high_life.get("system_modifiers") or {}) if isinstance(high_life, dict) else {}
    assert low_mods != high_mods, "system_modifiers must differ for contrasting profiles"


@pytest.mark.regression
def test_lc_s13_no_internal_bridge_slugs_in_consumer_surfaces() -> None:
    dto = _run_ab(
        lifestyle_inputs=_PROFILE_HIGH,
        questionnaire_data=_QUESTIONNAIRE_HIGH,
        fixed_analysis_id="lc-s13-leak",
    )
    for chunk in _user_facing_chunks(dto):
        assert not _INTERNAL_BRIDGE_SLUG.search(chunk), chunk[:240]
        assert not _RAW_SIGNAL_ID.search(chunk), chunk[:240]


@pytest.mark.regression
def test_lc_s13_domain_band_headline_polarity_guard() -> None:
    dto = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-coherence")
    for row in dto.consumer_domain_scores or []:
        d = row.model_dump() if hasattr(row, "model_dump") else dict(row)
        domain_id = str(d.get("domain_id") or "")
        if domain_id.startswith("wave1_"):
            _assert_domain_band_headline_polarity_coherent(d, domain_id)


@pytest.mark.regression
def test_lc_s13_blood_sugar_no_narrative_without_active_signals() -> None:
    dto = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-bs")
    bs = _domain_row(dto, "wave1_blood_sugar")
    active = bs.get("active_signal_ids") or []
    if active:
        pytest.skip("AB panel has active blood-sugar signals; inactive-signal guard not applicable")
    contrib = str(bs.get("contributor_sentence") or "").lower()
    assert "early impaired sugar" not in contrib


@pytest.mark.regression
def test_lc_s13_no_mock_personalisation_overclaim_in_consumer_text() -> None:
    dto = _run_ab(
        lifestyle_inputs=_PROFILE_HIGH,
        questionnaire_data=_QUESTIONNAIRE_HIGH,
        fixed_analysis_id="lc-s13-lang",
    )
    for chunk in _user_facing_chunks(dto):
        assert not _FORBIDDEN_NARRATIVE.search(chunk), chunk[:240]


@pytest.mark.regression
def test_lc_s13_lifestyle_does_not_change_biomarker_values() -> None:
    low = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-bio-low")
    high = _run_ab(lifestyle_inputs=_PROFILE_HIGH, fixed_analysis_id="lc-s13-bio-high")

    def _value_map(dto: Any) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for bm in dto.biomarkers or []:
            bid = getattr(bm, "biomarker_id", None) or getattr(bm, "id", None)
            val = getattr(bm, "value", None)
            if bid is not None and val is not None:
                out[str(bid)] = float(val)
        return out

    assert _value_map(low) == _value_map(high), "lifestyle inputs must not alter measured biomarker values"


@pytest.mark.regression
def test_lc_s13_confidence_adjustments_only_when_core_inputs_missing() -> None:
    """Penalties apply per-system when missing_core_inputs is set (e.g. musculoskeletal sit/stand)."""
    dto = _run_ab(lifestyle_inputs=_PROFILE_LOW, fixed_analysis_id="lc-s13-conf")
    life = dto.lifestyle or {}
    adj = (life.get("confidence_adjustments") or {}) if isinstance(life, dict) else {}
    mods = (life.get("system_modifiers") or {}) if isinstance(life, dict) else {}
    assert isinstance(adj, dict)
    for system, penalty in adj.items():
        p = float(penalty or 0.0)
        block = mods.get(system) if isinstance(mods, dict) else None
        missing = list((block or {}).get("missing_core_inputs") or []) if isinstance(block, dict) else []
        if missing:
            assert p > 0.0, f"{system}: expected confidence penalty when core inputs missing"
        else:
            assert p == 0.0, f"{system}: unexpected confidence penalty without missing core inputs"


@pytest.mark.regression
def test_lc_s13_lifestyle_consumer_surface_unit() -> None:
    meta = {
        "lifestyle_interpretation_bridges_v1": {
            "alcohol_methylation_macrocytosis": {"active": True},
            "hydration_activity_renal": {
                "active": True,
                "hydration_context": {"fluid_intake_low": True},
                "activity_context": {"high_activity_pattern": False},
            },
        },
        "explainability_report": {
            "lifestyle": {
                "validated_inputs": {"smoking_status": "current"},
                "system_modifiers": {"metabolic": {"capped_total_modifier": 0.05}},
            }
        },
    }
    paras = build_lifestyle_consumer_overview_paragraphs_v1(meta)
    assert len(paras) >= 2
    joined = "\n".join(paras).lower()
    assert "moderate alcohol" in joined
    assert "current smoking" in joined
