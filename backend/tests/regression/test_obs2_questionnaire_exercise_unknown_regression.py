"""
Sentinel / bounded regression — questionnaire exercise absence must not coerce to zero minutes.

Post-LC-OBS-2 protection chore (not a sprint): promoted from
`tests/unit/test_lc_obs2_exercise_unknown_bridge.py` so Sentinel `--all` and
`-m regression` runs enforce:

  no questionnaire answer → unknown exercise, not zero exercise

Defect class key: questionnaire_exercise_unknown
Fix commit: 6c7e4c0
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.pipeline.questionnaire_mapper import STATINS_LONG_TERM_MEDICATION_LABEL
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

BACKEND_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = BACKEND_ROOT / "tests" / "fixtures" / "panels"
USER_RUNNER = {"user_id": "00000000-0000-0000-0000-0000000obs2a", "age": 58, "gender": "male"}


def _prepare_panel(fixture_name: str) -> Dict[str, Any]:
    raw = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
    biomarkers = raw["biomarkers"]
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def _domain_band_labels(dto: Any) -> List[str]:
    rows = dto.consumer_domain_scores or []
    labels: List[str] = []
    for row in rows:
        if hasattr(row, "band_label"):
            labels.append(str(row.band_label))
        elif isinstance(row, dict):
            labels.append(str(row.get("band_label", "")))
    return labels


def _meta_insight_graph(dto: Any) -> Dict[str, Any]:
    meta = dto.meta or {}
    ig = meta.get("insight_graph") or {}
    return ig if isinstance(ig, dict) else {}


def _top_finding_signal_ids(ig: Dict[str, Any]) -> List[str]:
    rv = ig.get("report_v1")
    if rv is None:
        return []
    if hasattr(rv, "model_dump"):
        rv = rv.model_dump()
    if not isinstance(rv, dict):
        return []
    tf = rv.get("top_findings") or []
    out: List[str] = []
    for row in tf:
        if isinstance(row, dict):
            sid = str(row.get("signal_id", "")).strip()
            if sid:
                out.append(sid)
    return out


def _signal_state_map(ig: Dict[str, Any]) -> Dict[str, str]:
    srs = ig.get("signal_results") or []
    out: Dict[str, str] = {}
    for row in srs:
        if isinstance(row, dict) and row.get("signal_id"):
            sid = str(row["signal_id"]).strip()
            out[sid] = str(row.get("signal_state", "")).strip()
    return out


@pytest.mark.regression
def test_obs2_ab_baseline_vs_statin_off_consumer_bands_align():
    prepared = _prepare_panel("ab_full_panel_with_ranges.json")
    orch = AnalysisOrchestrator()
    dto_base = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data=None,
        fixed_analysis_id="obs2-ab-base",
    )
    dto_off = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="obs2-ab-off",
    )
    assert dto_base.status == "completed"
    assert dto_off.status == "completed"
    assert _domain_band_labels(dto_base) == _domain_band_labels(dto_off)


@pytest.mark.regression
def test_obs2_ab_statin_off_vs_on_analytical_invariants():
    prepared = _prepare_panel("ab_full_panel_with_ranges.json")
    orch = AnalysisOrchestrator()
    dto_off = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="obs2-ab-s-off",
    )
    dto_on = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
        fixed_analysis_id="obs2-ab-s-on",
    )
    ig_off = _meta_insight_graph(dto_off)
    ig_on = _meta_insight_graph(dto_on)
    assert _top_finding_signal_ids(ig_off) == _top_finding_signal_ids(ig_on)
    assert _signal_state_map(ig_off) == _signal_state_map(ig_on)
    assert _domain_band_labels(dto_off) == _domain_band_labels(dto_on)


@pytest.mark.regression
def test_obs2_vr_baseline_vs_statin_off_consumer_bands_align():
    prepared = _prepare_panel("vr_full_panel_with_ranges.json")
    orch = AnalysisOrchestrator()
    dto_base = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data=None,
        fixed_analysis_id="obs2-vr-base",
    )
    dto_off = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="obs2-vr-off",
    )
    assert dto_base.status == "completed"
    assert dto_off.status == "completed"
    assert _domain_band_labels(dto_base) == _domain_band_labels(dto_off)


@pytest.mark.regression
def test_obs2_lifestyle_fixture_with_partial_questionnaire_completes():
    lifestyle = json.loads(
        (BACKEND_ROOT / "tests" / "fixtures" / "lifestyle_minimal.json").read_text(encoding="utf-8")
    )
    prepared = _prepare_panel("ab_full_panel_with_ranges.json")
    orch = AnalysisOrchestrator()
    dto = orch.run(
        prepared,
        USER_RUNNER,
        assume_canonical=True,
        lifestyle_inputs=lifestyle,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="obs2-ab-life-q",
    )
    assert dto.status == "completed"
    assert dto.consumer_domain_scores
