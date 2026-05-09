"""
LC-S2 launch-core statin context integration — bounded proving (gate checks S-1..S-6 subset).

Full orchestrator replay belongs to golden panels; these tests stay bounded per Sprint 2 rules.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.analytics.intervention_annotation_compiler_v1 import (
    build_intervention_annotations_v1,
    format_intervention_annotation_consumer_cv_suffix_v1,
    format_intervention_annotation_narrative_appendix_v1,
)
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.pipeline.questionnaire_mapper import STATINS_LONG_TERM_MEDICATION_LABEL, QuestionnaireMapper


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


def test_s4_analysis_dto_field_contract_roundtrip():
    m = QuestionnaireMapper()
    doc = m.build_user_intervention_document_for_statin(
        {"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]},
    )
    ann = build_intervention_annotations_v1(doc)
    raw = ann.model_dump()
    again = InterventionAnnotationsV1.model_validate(raw)
    assert again.registry_id


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
    assert appendix in (on.body_overview or "")
    assert appendix not in (off.body_overview or "")
    sfx = format_intervention_annotation_consumer_cv_suffix_v1(ann)
    assert sfx.startswith("Medication context")


def test_s6_annotation_helpers_do_not_import_signal_pipeline_modules():
    import core.analytics.intervention_annotation_compiler_v1 as iac

    src = Path(iac.__file__).read_text(encoding="utf-8")
    assert "signal_evaluator" not in src
    assert "SignalEvaluator" not in src
