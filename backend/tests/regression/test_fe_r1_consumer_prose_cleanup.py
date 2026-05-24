"""
FE-R1 — Consumer prose cleanup and narrative safety regression.

Sentinel defect classes (escaped_defects_v1.json):
  consumer_prose_internal_compiler_leakage
  consumer_prose_unbounded_kb_dump
  consumer_retail_label_template_suffix
  consumer_confidence_raw_numeric_leakage
  consumer_balanced_systems_empty_when_domains_stable
  consumer_biomarker_status_direction_mismatch
  consumer_prose_raw_signal_id_visible
  consumer_summary_compiler_self_description
  retail_page_duplicate_prose_block
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest

from core.analytics.consumer_prose_safety_v1 import (
    PROHIBITED_CONSUMER_SUBSTRINGS,
    collect_retail_prose_surfaces,
    contains_prohibited_consumer_text,
)
from core.analytics.primitives import frontend_status_from_lab_reference
from core.dto.builders import build_analysis_result_dto
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"

_RAW_CONFIDENCE_RE = re.compile(r"\b0\.\d{2}\s+vs\s+0\.\d{2}\b")
_INTERNAL_SIGNAL_LABEL_RE = re.compile(
    r"\b[A-Z][a-z]+ [Hh]igh on [A-Z][a-z]+\b|\b[A-Z][a-z]+ [Ll]ow on [A-Z][a-z]+\b"
)
_RAW_SIGNAL_PHRASES: Tuple[str, ...] = (
    "Lh High",
    "Alp Low",
    "Hypercortisolism",
)
_RAW_SIGNAL_SUBOPTIMAL_ON_RE = re.compile(
    r"\b[A-Z][a-z]+ [Hh]igh \(suboptimal\) on [A-Z][a-z]+\b|"
    r"\b[A-Z][a-z]+ [Ll]ow \(suboptimal\) on [A-Z][a-z]+\b",
)
_RETAIL_SUMMARY_COMPILER_SELF_DESCRIPTION: Tuple[str, ...] = (
    "ranked lead pattern",
    "lab anchor",
    "priority thread",
    "interpretation thread",
    "this wording stays descriptive",
    "does not replace clinician judgement",
    "structured ranking only",
    "confidence weight",
    "moderate_by_default",
)
_MIN_DUPLICATE_SENTENCE_CHARS = 72


def _prepare_ab_panel() -> Dict[str, Any]:
    from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
    from core.canonical.normalize import normalize_biomarkers_with_metadata
    from core.units.registry import apply_unit_normalisation

    raw = json.loads(_AB_PANEL.read_text(encoding="utf-8"))
    biomarkers = dict(raw["biomarkers"])
    for entry in biomarkers.values():
        if isinstance(entry, dict) and entry.get("unit") == "\u03bcmol/L":
            entry["unit"] = "\u00b5mol/L"
        rr = entry.get("reference_range")
        if isinstance(rr, dict) and rr.get("unit") == "\u03bcmol/L":
            rr["unit"] = "\u00b5mol/L"
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def _run_ab_baseline() -> Any:
    return AnalysisOrchestrator().run(
        _prepare_ab_panel(),
        {"age": 45, "sex": "male"},
        assume_canonical=True,
        fixed_analysis_id="fe-r1-ab",
    )


def _stored_shape_from_dto(dto: Any) -> Dict[str, Any]:
    meta = dto.meta if isinstance(dto.meta, dict) else {}
    idl = dto.interpretation_display_layer_v1
    nr = dto.narrative_report_v1
    ia = dto.intervention_annotations_v1
    consumer_scores = dto.consumer_domain_scores
    if consumer_scores is not None and hasattr(consumer_scores, "__iter__"):
        consumer_scores = [
            row.model_dump() if hasattr(row, "model_dump") else row for row in consumer_scores
        ]
    raw = {
        "analysis_id": dto.analysis_id,
        "biomarkers": [b.model_dump() if hasattr(b, "model_dump") else b for b in (dto.biomarkers or [])],
        "clusters": [c.model_dump() if hasattr(c, "model_dump") else c for c in (dto.clusters or [])],
        "insights": [i.model_dump() if hasattr(i, "model_dump") else i for i in (dto.insights or [])],
        "status": dto.status,
        "created_at": dto.created_at,
        "overall_score": dto.overall_score,
        "primary_driver_system_id": dto.primary_driver_system_id,
        "system_capacity_scores": dto.system_capacity_scores,
        "burden_hash": dto.burden_hash,
        "risk_assessment": meta.get("risk_assessment", {}),
        "recommendations": meta.get("recommendations", []),
        "result_version": meta.get("result_version", "1.0.0"),
        "derived_markers": dto.derived_markers,
        "meta": meta,
        "replay_manifest": dto.replay_manifest,
        "interpretation_display_layer_v1": idl.model_dump() if hasattr(idl, "model_dump") else idl,
        "narrative_report_v1": nr.model_dump() if hasattr(nr, "model_dump") else nr,
        "consumer_domain_scores": consumer_scores,
        "intervention_annotations_v1": ia.model_dump() if hasattr(ia, "model_dump") else ia,
    }
    return build_analysis_result_dto(raw)


def _normalize_prose(text: str) -> str:
    return " ".join(str(text or "").lower().split())


def _sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"[.!?]\s+", str(text or "")) if s.strip()]


def _fe_r0_duplicate_prose_surfaces(api: Dict[str, Any]) -> Dict[str, str]:
    """Surfaces FE-R0 flagged for cross-section duplication on the results page."""
    surfaces: Dict[str, str] = {}

    nr = api.get("narrative_report_v1")
    if isinstance(nr, dict):
        retail_summary = str(nr.get("retail_summary") or "").strip()
        if retail_summary:
            surfaces["retail_summary"] = retail_summary

    idl = api.get("interpretation_display_layer_v1")
    if isinstance(idl, dict):
        for idx, rec in enumerate(idl.get("records") or []):
            if not isinstance(rec, dict):
                continue
            why = str(rec.get("why_it_matters") or "").strip()
            if why:
                surfaces[f"idl_why_it_matters_{idx}"] = why

    cr = api.get("clinician_report_v1")
    if isinstance(cr, dict):
        page1 = (cr.get("sections") or {}).get("page1") or {}
        if isinstance(page1, dict):
            primary = str(page1.get("primary_concern") or "").strip()
            if primary:
                surfaces["hero_primary_concern"] = primary

    for row in api.get("consumer_domain_scores") or []:
        if not isinstance(row, dict):
            continue
        domain_id = str(row.get("domain_id") or "domain").strip()
        contributor = str(row.get("contributor_sentence") or "").strip()
        if contributor:
            surfaces[f"domain_{domain_id}_contributor"] = contributor

    return surfaces


def _substantial_sentence_shared(left: str, right: str) -> str | None:
    left_norm = _normalize_prose(left)
    right_norm = _normalize_prose(right)
    if len(left_norm) >= _MIN_DUPLICATE_SENTENCE_CHARS and left_norm in right_norm:
        return left_norm
    if len(right_norm) >= _MIN_DUPLICATE_SENTENCE_CHARS and right_norm in left_norm:
        return right_norm
    for sent in _sentences(left):
        sent_norm = _normalize_prose(sent)
        if len(sent_norm) < _MIN_DUPLICATE_SENTENCE_CHARS:
            continue
        if sent_norm in right_norm:
            return sent_norm
    for sent in _sentences(right):
        sent_norm = _normalize_prose(sent)
        if len(sent_norm) < _MIN_DUPLICATE_SENTENCE_CHARS:
            continue
        if sent_norm in left_norm:
            return sent_norm
    return None


@pytest.mark.regression
def test_fe_r1_consumer_prose_raw_signal_id_visible() -> None:
    """Sentinel: consumer_prose_raw_signal_id_visible."""
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    combined = "\n".join(collect_retail_prose_surfaces(api))
    low = combined.lower()
    for phrase in _RAW_SIGNAL_PHRASES:
        assert phrase.lower() not in low, f"raw signal phrase {phrase!r} visible in consumer prose"
    assert not _RAW_SIGNAL_SUBOPTIMAL_ON_RE.search(combined), "raw (suboptimal) on signal slug visible"
    assert not _INTERNAL_SIGNAL_LABEL_RE.search(combined), "internal signal label pattern visible"


@pytest.mark.regression
def test_fe_r1_retail_summary_no_compiler_self_description() -> None:
    """Sentinel: consumer_summary_compiler_self_description."""
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    nr = api.get("narrative_report_v1") or {}
    retail_summary = str((nr or {}).get("retail_summary") or "")
    assert retail_summary.strip(), "retail_summary expected on AB baseline"
    low = retail_summary.lower()
    for token in _RETAIL_SUMMARY_COMPILER_SELF_DESCRIPTION:
        assert token not in low, f"compiler self-description {token!r} in retail_summary"
    assert " thread " not in f" {low} ", "compiler thread language in retail_summary"


@pytest.mark.regression
def test_fe_r1_no_duplicate_prose_across_retail_surfaces() -> None:
    """Sentinel: retail_page_duplicate_prose_block."""
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    surfaces = _fe_r0_duplicate_prose_surfaces(api)
    assert "retail_summary" in surfaces, "retail_summary required for duplication guard"
    keys = list(surfaces.keys())
    for i, left_key in enumerate(keys):
        for right_key in keys[i + 1 :]:
            shared = _substantial_sentence_shared(surfaces[left_key], surfaces[right_key])
            assert shared is None, (
                f"duplicate prose between {left_key!r} and {right_key!r}: {shared!r}"
            )


@pytest.mark.regression
def test_fe_r1_retail_prose_surfaces_exclude_internal_tokens() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    surfaces = collect_retail_prose_surfaces(api)
    assert surfaces, "expected retail prose surfaces on AB baseline"
    combined = "\n".join(surfaces)
    for token in PROHIBITED_CONSUMER_SUBSTRINGS:
        assert token.lower() not in combined.lower(), f"prohibited token {token!r} in retail prose"
    assert not _RAW_CONFIDENCE_RE.search(combined), "raw confidence comparison leaked"
    assert not _INTERNAL_SIGNAL_LABEL_RE.search(combined), "internal signal label pattern leaked"


@pytest.mark.regression
def test_fe_r1_lead_and_secondary_narratives_bounded() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    nr = api.get("narrative_report_v1") or {}
    assert isinstance(nr, dict)
    lead = str(nr.get("lead_narrative") or "")
    secondary = str(nr.get("secondary_narratives") or "")
    assert lead.strip(), "lead narrative should be present on AB baseline"
    assert len(lead) <= 1400, "lead narrative exceeds FE-R1 consumer bound"
    assert lead.count("\n\n") + 1 <= 5, "lead narrative has too many paragraphs"
    if secondary.strip():
        assert len(secondary) <= 700, "secondary narrative exceeds FE-R1 consumer bound"


@pytest.mark.regression
def test_fe_r1_next_steps_consumer_header() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    nr = api.get("narrative_report_v1") or {}
    next_steps = str((nr or {}).get("next_steps_narrative") or "")
    low = next_steps.lower()
    assert "prioritised follow-up (governed" not in low
    assert "functional read —" not in next_steps
    if next_steps.strip():
        assert "suggested follow-up" in low or "follow-up" in low


@pytest.mark.regression
def test_fe_r1_balanced_systems_populated_on_ab() -> None:
    """FE-R0 empty balanced_systems_v1 on AB baseline must not regress."""
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    balanced = api.get("balanced_systems_v1")
    assert balanced is not None, "balanced_systems_v1 should be present on AB baseline"
    assert isinstance(balanced, dict)
    items = balanced.get("items") or []
    assert items, "balanced systems should list at least one stable system/domain"


@pytest.mark.regression
def test_fe_r1_alp_at_range_floor_not_critical() -> None:
    status = frontend_status_from_lab_reference(46.0, 46.0, 116.0, biomarker_name="alp")
    assert status != "critical", "low ALP at lab floor must not surface as critical on retail"


@pytest.mark.regression
def test_fe_r1_results_page_heading_consumer_safe() -> None:
    src = _RESULTS_PAGE.read_text(encoding="utf-8")
    assert "clinician-structured" not in src.lower()


@pytest.mark.regression
def test_fe_r1_idl_retail_labels_no_template_suffix() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    idl = api.get("interpretation_display_layer_v1") or {}
    records = idl.get("records") if isinstance(idl, dict) else []
    for rec in records or []:
        if not isinstance(rec, dict):
            continue
        lab = str(rec.get("retail_display_label") or "")
        if not lab:
            continue
        assert "is outside the optimal range on this panel" not in lab.lower()
        assert not contains_prohibited_consumer_text(lab)
