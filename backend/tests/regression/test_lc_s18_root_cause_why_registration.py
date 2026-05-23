"""
LC-S18 — Root-cause / WHY registration generalisation regression.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.knowledge.root_cause_registry_v1 import (
    ROOT_CAUSE_TARGET_SPECS,
    RootCauseRegistryValidationError,
    RootCauseTargetSpec,
    fingerprint_root_cause_targets,
    get_root_cause_targets,
    validate_root_cause_registry,
)
from core.knowledge import load_root_cause_hypotheses as lrc
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AB_PANEL = (
    Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
)
_BEFORE_FP = _REPO_ROOT / "docs" / "audit-papers" / "LC-S18_root_cause_why_registration_before_fingerprint.json"
_AFTER_FP = _REPO_ROOT / "docs" / "audit-papers" / "LC-S18_root_cause_why_registration_after_fingerprint.json"


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
        fixed_analysis_id="lc-s18-ab",
    )


def _minimal_fired_signal(signal_id: str) -> Dict[str, Any]:
    return {
        "signal_id": signal_id,
        "signal_state": "at_risk",
        "confidence": 0.85,
        "primary_metric": "homocysteine",
        "why_it_matters": "Test signal for root-cause compile.",
    }


@pytest.mark.regression
def test_lc_s18_registry_target_count_discovered() -> None:
    assert len(ROOT_CAUSE_TARGET_SPECS) == 41
    assert len(get_root_cause_targets()) == 41


@pytest.mark.regression
def test_lc_s18_all_targets_load_governed_assets() -> None:
    report = fingerprint_root_cause_targets()
    assert report["target_count"] == 41
    for row in report["targets"]:
        assert row["asset_loads"] is True, row
        assert row["governed"] is True, row
        assert row.get("error") is None, row
        assert row.get("hypothesis_asset_fingerprint")


@pytest.mark.regression
def test_lc_s18_before_after_fingerprints_equivalent() -> None:
    assert _BEFORE_FP.is_file() and _AFTER_FP.is_file()
    before = json.loads(_BEFORE_FP.read_text(encoding="utf-8"))
    after = json.loads(_AFTER_FP.read_text(encoding="utf-8"))
    assert before["target_count"] == after["target_count"] == 41
    for b, a in zip(before["targets"], after["targets"]):
        assert b["signal_id"] == a["signal_id"]
        assert b["hypothesis_asset_fingerprint"] == a["hypothesis_asset_fingerprint"]


@pytest.mark.regression
def test_lc_s18_duplicate_target_id_fails_loudly() -> None:
    dup = list(ROOT_CAUSE_TARGET_SPECS)
    dup = list(dup) + [dup[0]]
    with pytest.raises(RootCauseRegistryValidationError, match="duplicate"):
        validate_root_cause_registry(dup, load_assets=False)


@pytest.mark.regression
def test_lc_s18_malformed_empty_signal_id_fails_loudly() -> None:
    bad = list(ROOT_CAUSE_TARGET_SPECS) + [
        RootCauseTargetSpec("", lrc.load_hcy_hypotheses_v1, "hcy_hypotheses_v1.yaml"),
    ]
    with pytest.raises(RootCauseRegistryValidationError):
        validate_root_cause_registry(bad, load_assets=False)


@pytest.mark.regression
def test_lc_s18_registry_order_stable() -> None:
    first = [sid for sid, _ in get_root_cause_targets()]
    second = [sid for sid, _ in get_root_cause_targets()]
    assert first == second
    assert first[0] == "signal_homocysteine_elevation_context"


@pytest.mark.regression
def test_lc_s18_no_orphan_package_auto_discovery_in_registry() -> None:
    for spec in ROOT_CAUSE_TARGET_SPECS:
        assert spec.registration_source == "manual_v1"


@pytest.mark.regression
def test_lc_s18_homocysteine_governed_why_on_ab_baseline() -> None:
    dto = _run_ab_baseline()
    ig = (dto.meta or {}).get("insight_graph") or {}
    report = ig.get("report_v1") or {}
    if hasattr(report, "model_dump"):
        report = report.model_dump()
    root = report.get("root_cause_v1") or {}
    findings = root.get("findings") or []
    ids = {str(f.get("signal_id", "")) for f in findings if isinstance(f, dict)}
    assert "signal_homocysteine_elevation_context" in ids or "signal_homocysteine_high" in ids


@pytest.mark.regression
def test_lc_s18_registered_target_compiles_when_signal_fired() -> None:
    signal_id, loader = get_root_cause_targets()[0]
    root = compile_root_cause_v1(
        signal_results=[_minimal_fired_signal(signal_id)],
        biomarker_context={"homocysteine": {"value": 16.0, "unit": "umol/L"}},
        input_reference_ranges={"homocysteine": {"min": 4.0, "max": 14.0, "unit": "umol/L"}},
    )
    assert root is not None
    assert any(f.signal_id == signal_id for f in root.findings)


@pytest.mark.regression
def test_lc_s18_fallback_finding_explicit_when_unregistered_lead() -> None:
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_not_in_registry_example",
                "signal_state": "at_risk",
                "confidence": 0.9,
                "rank": 1,
                "why_it_matters": "Unregistered lead for fallback path.",
            }
        ],
        biomarker_context={},
        input_reference_ranges={},
    )
    assert root is not None
    finding = root.findings[0]
    assert finding.hypotheses[0].hypothesis_id == "why_engine_fallback_v1"


def _load_sentinel_pack() -> Dict[str, Any]:
    return json.loads((_REPO_ROOT / "sentinel" / "packs" / "escaped_defects_v1.json").read_text(encoding="utf-8"))


@pytest.mark.regression
@pytest.mark.parametrize(
    "defect_class",
    [
        "root_cause_target_not_loaded",
        "why_asset_silent_skip",
        "metadata_malformed_not_failed",
        "why_output_changed_after_registration_migration",
        "duplicate_why_target_id_not_rejected",
        "orphan_why_asset_auto_loaded",
        "new_why_asset_requires_backend_code",
    ],
)
def test_lc_s18_sentinel_defect_classes_registered(defect_class: str) -> None:
    entry = (_load_sentinel_pack().get("defect_classes") or {}).get(defect_class)
    assert entry is not None
    assert entry.get("test_file") == "backend/tests/regression/test_lc_s18_root_cause_why_registration.py"
    assert entry.get("status") == "GUARDED"
