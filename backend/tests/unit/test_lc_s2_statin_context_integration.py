"""
LC-S2 launch-core statin context integration — bounded proving (gate checks S-1..S-6 subset).

Full orchestrator replay belongs to golden panels; these tests stay bounded per Sprint 2 rules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from core.analytics.intervention_annotation_compiler_v1 import build_intervention_annotations_v1
from core.analytics.intervention_annotation_formatter_v1 import (
    format_intervention_annotation_consumer_cv_suffix_v1,
    format_intervention_annotation_narrative_appendix_v1,
)
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.pipeline.questionnaire_mapper import STATINS_LONG_TERM_MEDICATION_LABEL, QuestionnaireMapper
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation


def _prepare_lc_s2_fixture_panel() -> Dict[str, Any]:
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


def test_s1_questionnaire_ssot_includes_statin_option():
    repo_backend = Path(__file__).resolve().parents[2]
    payload = json.loads((repo_backend / "ssot" / "questionnaire.json").read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("questions", [])
    q = next(x for x in rows if x.get("id") == "long_term_medications")
    assert STATINS_LONG_TERM_MEDICATION_LABEL in (q.get("options") or [])


def test_s2_mapper_emits_valid_user_intervention_document():
    m = QuestionnaireMapper()
    assert m.build_user_intervention_document_for_statin({"long_term_medications": ["None"]}) is None
    doc = m.build_user_intervention_document_for_statin(
        {"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
    )
    assert doc is not None
    assert doc["schema_version"] == "1.0.0"
    rec = doc["intervention_records"][0]
    assert rec["canonical_class"]["link_status"] == "mapped"
    assert rec["canonical_class"]["intervention_class_id"] == "lipid_lowering_statin"


def test_s3_annotation_compiler_resolves_statin():
    m = QuestionnaireMapper()
    doc = m.build_user_intervention_document_for_statin(
        {"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
    )
    ann = build_intervention_annotations_v1(doc)
    assert ann is not None
    assert any(r.intervention_class_id == "lipid_lowering_statin" for r in ann.resolved)


def test_s4_orchestrator_carries_intervention_annotations_for_statin_on():
    prepared = _prepare_lc_s2_fixture_panel()
    user = {"user_id": "00000000-0000-0000-0000-00000000lc24", "age": 45, "gender": "male"}
    orch = AnalysisOrchestrator()
    dto = orch.run(
        prepared,
        user,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
        fixed_analysis_id="lc-s2-s4-carriage",
    )
    assert dto.status == "completed"
    assert dto.intervention_annotations_v1 is not None
    assert any(
        r.intervention_class_id == "lipid_lowering_statin"
        for r in dto.intervention_annotations_v1.resolved
    )


def test_s5_visible_narrative_and_consumer_suffix_difference_when_annotation_present():
    m = QuestionnaireMapper()
    doc = m.build_user_intervention_document_for_statin(
        {"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
    )
    ann = build_intervention_annotations_v1(doc)
    off = compile_narrative_report_v1(analysis_id="lc_s2_off", meta={}, insight_graph={}, idl_bundle=None)
    on = compile_narrative_report_v1(
        analysis_id="lc_s2_on",
        meta={},
        insight_graph={},
        idl_bundle=None,
        intervention_annotations_v1=ann,
    )
    appendix = format_intervention_annotation_narrative_appendix_v1(ann)
    assert appendix
    assert appendix not in (on.body_overview or "")
    assert appendix not in (off.body_overview or "")
    sfx = format_intervention_annotation_consumer_cv_suffix_v1(ann)
    assert sfx
    assert sfx in (on.body_overview or "")
    assert "Statin medication noted" in (on.body_overview or "")
    assert "Layer B intervention annotation" not in sfx
    assert "direction=" not in sfx


def test_s6_statin_on_vs_off_preserves_top_findings_order_bands_and_signal_states():
    prepared = _prepare_lc_s2_fixture_panel()
    user = {"user_id": "00000000-0000-0000-0000-00000000lc26", "age": 45, "gender": "male"}
    orch = AnalysisOrchestrator()
    dto_off = orch.run(
        prepared,
        user,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": ["None"]},
        fixed_analysis_id="lc-s2-s6-off",
    )
    dto_on = orch.run(
        prepared,
        user,
        assume_canonical=True,
        questionnaire_data={"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
        fixed_analysis_id="lc-s2-s6-on",
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

    body_off = dto_off.narrative_report_v1.body_overview if dto_off.narrative_report_v1 else ""
    body_on = dto_on.narrative_report_v1.body_overview if dto_on.narrative_report_v1 else ""
    assert body_off != body_on
