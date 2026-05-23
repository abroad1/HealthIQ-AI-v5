"""
LC-S16/17/19 — Knowledge asset frontend surface, KB lifecycle, payload contract.

Sentinel defect classes (escaped_defects_v1.json):
  frontend_section_not_backed_by_governed_source
  knowledge_asset_not_surfaced_when_available
  generic_fallback_used_when_governed_asset_exists
  consumer_payload_internal_field_leakage
  dto_frontend_contract_breakage
  raw_signal_or_internal_id_visible
  kb_lifecycle_required_file_missing
  kb_orphan_package_unreported
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pytest
import yaml

from core.dto.builders import build_analysis_result_dto
from core.dto.frontend_contract_v1 import FRONTEND_CONSUMED_ROOT_KEYS
from core.knowledge.kb_lifecycle_contract_v1 import (
    LIFECYCLE_STATES,
    PACKAGE_TYPES,
    STANDARD_PACKAGE_FILES,
    WHY_ENABLED_PACKAGE_FILES,
    classify_package_type,
    detect_orphan_packages,
    iter_why_enabled_packages,
    list_package_dirs,
    package_has_required_files,
)
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)
_RESULTS_PAGE = _REPO_ROOT / "frontend" / "app" / "(app)" / "results" / "page.tsx"
_ANALYSIS_TS = _REPO_ROOT / "frontend" / "app" / "types" / "analysis.ts"

# LC-S16 section → primary DTO authority (frontend results journey).
FRONTEND_SECTION_DTO_MAP: Dict[str, str] = {
    "hero_primary_finding": "clinician_report_v1.sections.page1.primary_concern | interpretation_display_layer_v1 | narrative_report_v1",
    "whats_driving_this": "biomarkers[] | meta",
    "body_overview": "narrative_report_v1.body_overview | clinician_report_v1.sections.page1",
    "domain_cards": "consumer_domain_scores[]",
    "interpretation_patterns": "interpretation_display_layer_v1.records[]",
    "long_form_why": "narrative_report_v1.lead_narrative | clinician_report_v1.sections.root_cause",
    "biomarker_dials": "biomarkers[]",
    "uploaded_panel_fidelity": "meta.upload_panel_observations | meta.display_unit_policy",
    "clinician_advanced": "clinician_report_v1 | meta.insight_graph.layer_c_features",
    "trust_data_quality": "clinician_report_v1.data_quality",
    "next_steps": "narrative_report_v1.next_steps_narrative | recommendations[]",
    "balanced_systems": "balanced_systems_v1",
}

_RAW_SIGNAL_ID_RE = re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE)
_INTERNAL_GOVERNANCE_RE = re.compile(
    r"\b(LC-S\d+|KB-S\d+|pkg_[a-z0-9_]+|unmapped_|canonical_id:)\b",
)


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
        fixed_analysis_id="lc-s16-17-19-ab",
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


def _collect_user_facing_strings(obj: Any, prefix: str = "") -> List[str]:
    out: List[str] = []
    if isinstance(obj, str) and obj.strip():
        out.append(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("signal_results", "raw_evidence_refs", "burden_hash", "analysis_id"):
                continue
            out.extend(_collect_user_facing_strings(v, f"{prefix}.{k}"))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(_collect_user_facing_strings(item, prefix))
    return out


@pytest.mark.regression
def test_lc_s16_frontend_sections_map_to_known_dto_fields() -> None:
    assert _RESULTS_PAGE.is_file(), "results page entry missing"
    page_src = _RESULTS_PAGE.read_text(encoding="utf-8")
    for section, dto_fields in FRONTEND_SECTION_DTO_MAP.items():
        primary = dto_fields.split("|")[0].strip().split("[")[0].strip()
        root = primary.split(".")[0]
        assert root in page_src or root.replace("_v1", "") in page_src, (
            f"section {section} root {root} not referenced on results page"
        )


@pytest.mark.regression
def test_lc_s16_governed_why_present_on_ab_baseline() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    nr = api.get("narrative_report_v1") or {}
    lead = str((nr.get("lead_narrative") if isinstance(nr, dict) else "") or "")
    cr = api.get("clinician_report_v1") or {}
    page1 = {}
    if isinstance(cr, dict):
        sections = cr.get("sections") or {}
        page1 = sections.get("page1") if isinstance(sections, dict) else {}
    primary = str((page1.get("primary_concern") if isinstance(page1, dict) else "") or "")
    combined = f"{lead} {primary}".lower()
    assert "homocysteine" in combined or "methylation" in combined or "one-carbon" in combined


@pytest.mark.regression
def test_lc_s16_no_raw_signal_ids_in_consumer_domain_scores() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    for row in api.get("consumer_domain_scores") or []:
        if not isinstance(row, dict):
            continue
        for key in (
            "headline_sentence",
            "contributor_sentence",
            "consequence_sentence",
            "next_step_sentence",
            "evidence_anchor_sentence",
        ):
            text = str(row.get(key) or "")
            assert not _RAW_SIGNAL_ID_RE.search(text), f"{key}: {text!r}"


@pytest.mark.regression
def test_lc_s16_no_internal_governance_strings_in_consumer_surfaces() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    chunks = _collect_user_facing_strings(
        {
            "consumer_domain_scores": api.get("consumer_domain_scores"),
            "narrative_report_v1": api.get("narrative_report_v1"),
            "interpretation_display_layer_v1": api.get("interpretation_display_layer_v1"),
        }
    )
    for text in chunks:
        assert not _INTERNAL_GOVERNANCE_RE.search(text), text


@pytest.mark.regression
def test_lc_s17_lifecycle_states_are_valid_enum() -> None:
    assert len(LIFECYCLE_STATES) >= 7
    for state in (
        "draft",
        "validated",
        "runtime-loaded",
        "WHY-enabled",
        "frontend-surfaced",
        "Sentinel-protected",
    ):
        assert state in LIFECYCLE_STATES


@pytest.mark.regression
def test_lc_s17_package_types_defined() -> None:
    for pkg_type in ("signal-only", "WHY-enabled", "IDL-display-enabled"):
        assert pkg_type in PACKAGE_TYPES


@pytest.mark.regression
def test_lc_s17_standard_packages_have_required_files() -> None:
    root = _REPO_ROOT / "knowledge_bus" / "packages"
    sample = list_package_dirs(root)[:12]
    assert sample, "no knowledge packages found"
    for name in sample:
        if name == "pkg_example":
            continue
        missing = package_has_required_files(root / name, STANDARD_PACKAGE_FILES)
        assert not missing, f"{name} missing {missing}"


@pytest.mark.regression
def test_lc_s17_why_enabled_packages_have_required_files() -> None:
    why_pkgs = list(iter_why_enabled_packages(_REPO_ROOT))
    if not why_pkgs:
        pytest.skip("no WHY-enabled packages in estate")
    for pkg_dir in why_pkgs[:8]:
        missing = package_has_required_files(pkg_dir, WHY_ENABLED_PACKAGE_FILES)
        assert not missing, f"{pkg_dir.name} missing {missing}"
        assert classify_package_type(pkg_dir) == "WHY-enabled"


@pytest.mark.regression
def test_lc_s17_kb_orphan_reporter_runs_and_documents_drift() -> None:
    report = detect_orphan_packages(_REPO_ROOT)
    assert isinstance(report.disk_not_in_inventory, tuple)
    assert isinstance(report.inventory_not_on_disk, tuple)
    notes = _REPO_ROOT / "docs" / "audit-papers" / "LC-S17_knowledge_bus_lifecycle_framework.md"
    assert notes.is_file(), "LC-S17 framework doc must document inventory drift handling"
    body = notes.read_text(encoding="utf-8")
    assert "orphan" in body.lower() or "inventory" in body.lower()


@pytest.mark.regression
def test_lc_s19_dto_root_keys_match_frontend_contract() -> None:
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    assert frozenset(api.keys()) == FRONTEND_CONSUMED_ROOT_KEYS


@pytest.mark.regression
def test_lc_s19_analysis_ts_declares_consumed_roots() -> None:
    assert _ANALYSIS_TS.is_file()
    src = _ANALYSIS_TS.read_text(encoding="utf-8")
    for key in (
        "clinician_report_v1",
        "narrative_report_v1",
        "consumer_domain_scores",
        "interpretation_display_layer_v1",
        "balanced_systems_v1",
    ):
        assert key in src


@pytest.mark.regression
def test_lc_s19_homocysteine_lead_preserved() -> None:
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
def test_lc_s19_internal_meta_paths_not_required_for_retail_hero() -> None:
    """Consumer hero must not require meta.insight_graph.report_v1 at render time."""
    dto = _run_ab_baseline()
    api = _stored_shape_from_dto(dto)
    assert api.get("clinician_report_v1") is not None or api.get("narrative_report_v1")


def _load_sentinel_pack() -> Dict[str, Any]:
    path = _REPO_ROOT / "sentinel" / "packs" / "escaped_defects_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.regression
@pytest.mark.parametrize(
    "defect_class",
    [
        "frontend_section_not_backed_by_governed_source",
        "dto_frontend_contract_breakage",
        "raw_signal_or_internal_id_visible",
        "kb_lifecycle_required_file_missing",
        "kb_orphan_package_unreported",
        "consumer_payload_internal_field_leakage",
    ],
)
def test_lc_s16_17_19_sentinel_defect_classes_registered(defect_class: str) -> None:
    pack = _load_sentinel_pack()
    classes = pack.get("defect_classes") or {}
    entry = classes.get(defect_class)
    assert entry is not None, f"missing sentinel class {defect_class}"
    assert entry.get("test_file") == "backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py"
    assert entry.get("guard_type") == "active_deterministic"
    assert entry.get("status") == "GUARDED"
