"""
Sentinel — LC-S4 escaped-defect regression: statin signal isolation.

Defect class: statin_signal_isolation

User-reported statin context must change consumer-facing narrative framing (e.g. body_overview)
without changing analytical outputs: top finding order, per-signal states, or Wave-1 domain band labels.

Promoted from LC-S2 unit coverage (test_s6) — helpers below mirror that test's orchestrator wiring only;
this file must not import from backend.tests.unit.
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


def _prepare_ab_fixture_panel() -> Dict[str, Any]:
    path = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    biomarkers = raw["biomarkers"]
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def _meta_insight_graph(dto: Any) -> Dict[str, Any]:
    meta = dto.meta or {}
    ig = meta.get("insight_graph") or {}
    return ig if isinstance(ig, dict) else {}


def _report_v1_dict(ig: Dict[str, Any]) -> Dict[str, Any]:
    rv = ig.get("report_v1")
    if rv is None:
        return {}
    if hasattr(rv, "model_dump"):
        return rv.model_dump()
    return rv if isinstance(rv, dict) else {}


def _top_finding_signal_ids(ig: Dict[str, Any]) -> List[str]:
    tf = _report_v1_dict(ig).get("top_findings") or []
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


def _domain_band_labels(dto: Any) -> List[str]:
    rows = dto.consumer_domain_scores or []
    labels: List[str] = []
    for row in rows:
        if hasattr(row, "band_label"):
            labels.append(str(row.band_label))
        elif isinstance(row, dict):
            labels.append(str(row.get("band_label", "")))
    return labels


@pytest.mark.regression
def test_statin_on_vs_off_preserves_scoring_body_overview_framing_only():
    prepared = _prepare_ab_fixture_panel()
    user = {"user_id": "00000000-0000-0000-0000-00000000lc4s", "age": 45, "gender": "male"}
    orch = AnalysisOrchestrator()
    dto_off = orch.run(
        prepared,
        user,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="lc-s4-sentinel-statin-off",
    )
    dto_on = orch.run(
        prepared,
        user,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
        fixed_analysis_id="lc-s4-sentinel-statin-on",
    )
    assert dto_off.status == "completed"
    assert dto_on.status == "completed"

    ig_off = _meta_insight_graph(dto_off)
    ig_on = _meta_insight_graph(dto_on)
    assert _top_finding_signal_ids(ig_off) == _top_finding_signal_ids(ig_on)
    assert _signal_state_map(ig_off) == _signal_state_map(ig_on)
    assert _domain_band_labels(dto_off) == _domain_band_labels(dto_on)

    assert dto_off.intervention_annotations_v1 is None
    assert dto_on.intervention_annotations_v1 is not None
    on_classes = [
        r.intervention_class_id
        for r in (dto_on.intervention_annotations_v1.resolved or [])
        if getattr(r, "intervention_class_id", None)
    ]
    assert "lipid_lowering_statin" in on_classes

    body_off = dto_off.narrative_report_v1.body_overview if dto_off.narrative_report_v1 else ""
    body_on = dto_on.narrative_report_v1.body_overview if dto_on.narrative_report_v1 else ""
    assert isinstance(body_off, str) and isinstance(body_on, str)
    assert body_off != body_on
