"""
LC-S21/23/23B — Orchestrator phase decomposition, scaffold docs, SSOT metadata.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

import logging

from core.knowledge.ssot_tier1_metadata_contract_v1 import (
    PROHIBITED_PLACEHOLDER_STRINGS,
    TIER1_BIOMARKER_IDS,
    validate_tier1_metadata,
)
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.pipeline.orchestrator_phases_v1 import (
    PIPELINE_PHASE_ORDER,
    evaluate_signal_evaluation_phase,
    prepare_scoring_inputs_from_panel,
    quarantine_unmapped_biomarkers,
)
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)
_SENTINEL_PACK = _REPO_ROOT / "sentinel" / "packs" / "escaped_defects_v1.json"

_REQUIRED_DOCS = (
    "docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md",
    "docs/developer-guides/how_to_add_signal_package_v1.md",
    "docs/developer-guides/how_to_add_why_coverage_v1.md",
    "docs/developer-guides/how_to_add_lifestyle_modifier_v1.md",
    "docs/developer-guides/how_to_test_intelligence_asset_v1.md",
    "docs/developer-guides/healthiq_scaffold_guardrails_v1.md",
    "docs/developer-guides/scaffold_defect_vs_missing_content_classification_v1.md",
    "docs/audit-papers/LC-S21_orchestrator_phase_decomposition_notes.md",
    "docs/audit-papers/LC-S23_scaffold_documentation_onboarding_notes.md",
    "docs/audit-papers/LC-S23B_ssot_metadata_completion_notes.md",
    "docs/audit-papers/LC-S21_23_23B_orchestrator_docs_ssot_notes.md",
)

_REQUIRED_DOC_HEADINGS = {
    "docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md": (
        "## Ingestion",
        "## Canonicalisation",
        "## Scoring",
        "## Signals",
        "## DTO contract",
        "## Sentinel",
    ),
    "docs/developer-guides/how_to_add_signal_package_v1.md": ("## Package lifecycle", "## Validators"),
    "docs/developer-guides/how_to_add_why_coverage_v1.md": ("## Root-cause registry", "## LC-S18"),
    "docs/developer-guides/how_to_add_lifestyle_modifier_v1.md": ("## Questionnaire mapping", "## Sentinel"),
    "docs/developer-guides/how_to_test_intelligence_asset_v1.md": ("## Regression tests", "## Proving harness"),
    "docs/developer-guides/healthiq_scaffold_guardrails_v1.md": ("## Forbidden patterns", "## Standing maintenance"),
    "docs/developer-guides/scaffold_defect_vs_missing_content_classification_v1.md": (
        "## Scaffold defect",
        "## Missing knowledge asset",
    ),
}


def _prepare_ab_panel() -> Dict[str, Any]:
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
        fixed_analysis_id="lc-s21-ab",
    )


def _stable_output_fingerprint(dto: Any) -> str:
    meta = dto.meta or {}
    ig = meta.get("insight_graph") or {}
    report = ig.get("report_v1") or {}
    if hasattr(report, "model_dump"):
        report = report.model_dump()
    payload = {
        "signal_count": len(meta.get("signal_results") or []),
        "domain_score_keys": sorted((meta.get("domain_scores_v1") or {}).keys()),
        "root_cause_signal_ids": sorted(
            str(f.get("signal_id", ""))
            for f in (report.get("root_cause_v1") or {}).get("findings") or []
            if isinstance(f, dict)
        ),
        "replay_manifest_version": (meta.get("replay_manifest") or {}).get("manifest_version"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _load_sentinel_pack() -> Dict[str, Any]:
    return json.loads(_SENTINEL_PACK.read_text(encoding="utf-8"))


@pytest.mark.regression
def test_lc_s21_pipeline_phase_order_documented() -> None:
    assert "canonicalisation_quarantine" in PIPELINE_PHASE_ORDER
    assert "signal_evaluation" in PIPELINE_PHASE_ORDER
    assert PIPELINE_PHASE_ORDER.index("scoring_input_preparation") < PIPELINE_PHASE_ORDER.index("signal_evaluation")


@pytest.mark.regression
def test_lc_s21_phase_helpers_invocable() -> None:
    class _Alias:
        def resolve(self, key: str) -> str:
            return key

    quarantine = quarantine_unmapped_biomarkers({"ldl_cholesterol": 3.0}, alias_service=_Alias())
    assert "ldl_cholesterol" in quarantine.filtered_biomarkers
    prep = prepare_scoring_inputs_from_panel(
        {"ldl_cholesterol": {"value": 3.0, "reference_range": {"min": 1.0, "max": 4.0}}},
        logger=logging.getLogger("test_lc_s21"),
    )
    assert prep.simple_biomarkers["ldl_cholesterol"] == 3.0
    assert "ldl_cholesterol" in prep.input_reference_ranges


@pytest.mark.regression
def test_lc_s21_ab_baseline_output_fingerprint_stable() -> None:
    dto = _run_ab_baseline()
    fp = _stable_output_fingerprint(dto)
    assert len(fp) == 64
    fp_path = _REPO_ROOT / "docs" / "audit-papers" / "LC-S21_orchestrator_ab_baseline_fingerprint.json"
    if fp_path.is_file():
        expected = json.loads(fp_path.read_text(encoding="utf-8"))
        assert fp == expected["fingerprint"], "orchestrator phase extraction changed analytical output fingerprint"


@pytest.mark.regression
def test_lc_s21_homocysteine_why_present_on_ab_baseline() -> None:
    dto = _run_ab_baseline()
    ig = (dto.meta or {}).get("insight_graph") or {}
    report = ig.get("report_v1") or {}
    if hasattr(report, "model_dump"):
        report = report.model_dump()
    ids = {
        str(f.get("signal_id", ""))
        for f in (report.get("root_cause_v1") or {}).get("findings") or []
        if isinstance(f, dict)
    }
    assert "signal_homocysteine_elevation_context" in ids or "signal_homocysteine_high" in ids


@pytest.mark.regression
@pytest.mark.parametrize("rel_path", _REQUIRED_DOCS)
def test_lc_s23_required_docs_exist(rel_path: str) -> None:
    path = _REPO_ROOT / rel_path
    assert path.is_file(), rel_path
    text = path.read_text(encoding="utf-8")
    assert "Standing maintenance" in text or "standing-maintenance" in text.lower()


@pytest.mark.regression
@pytest.mark.parametrize("rel_path,headings", list(_REQUIRED_DOC_HEADINGS.items()))
def test_lc_s23_required_headings(rel_path: str, headings: tuple[str, ...]) -> None:
    text = (_REPO_ROOT / rel_path).read_text(encoding="utf-8")
    for heading in headings:
        assert heading in text, f"{rel_path} missing {heading}"


@pytest.mark.regression
def test_lc_s23_docs_reference_real_runtime_paths() -> None:
    arch = (_REPO_ROOT / "docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md").read_text(encoding="utf-8")
    assert "backend/core/pipeline/orchestrator.py" in arch
    assert "backend/core/analytics/signal_evaluator.py" in arch
    assert "knowledge_bus/packages" not in arch.lower() or "not runtime" in arch.lower() or "future" in arch.lower()


@pytest.mark.regression
def test_lc_s23b_tier1_metadata_complete() -> None:
    failures = validate_tier1_metadata()
    assert failures == [], failures


@pytest.mark.regression
def test_lc_s23b_no_placeholder_strings_in_tier1() -> None:
    biomarkers = yaml.safe_load((_REPO_ROOT / "backend/ssot/biomarkers.yaml").read_text(encoding="utf-8"))["biomarkers"]
    for biomarker_id in TIER1_BIOMARKER_IDS:
        row = biomarkers[biomarker_id]
        for field in ("key_risks_when_high", "key_risks_when_low", "known_modifiers"):
            for item in row.get(field) or []:
                assert str(item).strip().lower() not in PROHIBITED_PLACEHOLDER_STRINGS


@pytest.mark.regression
def test_lc_s23b_metadata_has_no_global_reference_ranges() -> None:
    biomarkers = yaml.safe_load((_REPO_ROOT / "backend/ssot/biomarkers.yaml").read_text(encoding="utf-8"))["biomarkers"]
    for biomarker_id in TIER1_BIOMARKER_IDS:
        row = biomarkers[biomarker_id]
        for key in row.keys():
            assert "reference_range" not in key.lower()
            assert "default_range" not in key.lower()


@pytest.mark.regression
@pytest.mark.parametrize(
    "defect_class",
    [
        "orchestrator_phase_output_changed",
        "pipeline_phase_regression",
        "scaffold_documentation_missing_for_new_pattern",
        "active_signal_biomarker_missing_ssot_metadata",
        "ssot_metadata_unreviewed_for_kb_wave_target",
    ],
)
def test_lc_s21_23_23b_sentinel_defect_classes_registered(defect_class: str) -> None:
    entry = (_load_sentinel_pack().get("defect_classes") or {}).get(defect_class)
    assert entry is not None, defect_class
    assert entry.get("test_file") == "backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py"
    assert entry.get("status") == "GUARDED"
