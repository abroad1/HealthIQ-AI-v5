"""N-8 — deterministic narrative compiler v1 (governed asset assembly)."""

from __future__ import annotations

from core.analytics.interpretation_display_layer_publish_v1 import publish_interpretation_display_layer_v1
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.interpretation_display_layer_v1 import (
    InterpretationDisplayLayerBundleV1,
    InterpretationDisplayRecordV1,
)


def test_compiler_no_raise_when_assets_missing(monkeypatch, tmp_path):
    from core.analytics import narrative_report_compiler_v1 as mod

    monkeypatch.setattr(mod, "_ENTITIES_PATH", tmp_path / "missing.yaml")
    rep = compile_narrative_report_v1(analysis_id="a3", meta={}, insight_graph={}, idl_bundle=None)
    assert rep.meta.get("skipped")


def test_lifestyle_bridges_surface_when_active():
    from core.analytics.narrative_report_compiler_v1 import ALCOHOL_ONE_CARBON_LIFESTYLE_BODY_OVERVIEW_V1

    meta = {
        "lifestyle_interpretation_bridges_v1": {
            "alcohol_methylation_macrocytosis": {"active": True, "rationale_codes": ["test"]},
        }
    }
    rep = compile_narrative_report_v1(analysis_id="a4", meta=meta, insight_graph={}, idl_bundle=None)
    assert ALCOHOL_ONE_CARBON_LIFESTYLE_BODY_OVERVIEW_V1 in rep.body_overview
    assert "Lifestyle bridge" not in rep.lead_narrative
    assert "alcohol_intake_moderate" not in rep.body_overview


def _sample_idl_bundle() -> InterpretationDisplayLayerBundleV1:
    return InterpretationDisplayLayerBundleV1(
        schema_version="1.0.0",
        records=[
            InterpretationDisplayRecordV1(
                internal_id="ph_demo_retail_v1",
                scientific_class="phenotype",
                clinical_display_label="Demo clinical pattern",
                retail_display_label="Demo retail pattern",
                subtitle="A concise subtitle for members.",
                why_it_matters="This matters for long-term monitoring.",
                severity_state="attention",
                supporting_biomarkers_summary="Homocysteine, MCV",
                frontend_allowed_term="phenotype_allowed",
                display_order_priority=2,
                enabled_for_frontend=True,
                supporting_systems_summary="Methylation and erythroid dynamics.",
                user_safe_description="Plain-language pattern note.",
                display_caveat="Not a standalone diagnosis.",
            ),
        ],
    )


def test_retail_and_clinician_sections_use_idl_when_bundle_present():
    ig = {
        "signal_results": [
            {"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"},
        ],
        "primary_driver_system_id": "vascular",
    }
    bundle = _sample_idl_bundle()
    rep = compile_narrative_report_v1(analysis_id="a5", meta={}, insight_graph=ig, idl_bundle=bundle)
    assert rep.retail_summary
    assert "Demo retail pattern" in rep.retail_summary
    assert rep.clinician_synthesis
    assert "Demo clinical pattern" in rep.clinician_synthesis
    assert "Interpretation display layer" in rep.clinician_synthesis


def test_longitudinal_narrative_uses_transitions_and_comparable_lab_delta():
    ig = {
        "signal_results": [],
        "state_transitions": [
            {
                "biomarker_id": "homocysteine",
                "from_status": "high",
                "to_status": "normal",
                "transition": "improving",
                "evidence_codes": ["status_change"],
            },
        ],
        "biomarker_nodes": [
            {
                "biomarker_id": "homocysteine",
                "status": "normal",
                "lab_value": 10.0,
                "lab_unit": "µmol/L",
            },
        ],
    }
    meta = {
        "prior_biomarker_lab_snapshot_v1": {
            "homocysteine": {"lab_value": 15.0, "lab_unit": "µmol/L"},
        },
    }
    rep = compile_narrative_report_v1(analysis_id="a6", meta=meta, insight_graph=ig, idl_bundle=None)
    assert rep.longitudinal_narrative
    assert "Homocysteine" in rep.longitudinal_narrative
    assert "improved" in rep.longitudinal_narrative.lower()
    assert "delta" in rep.longitudinal_narrative.lower()
    assert "10" in rep.longitudinal_narrative and "15" in rep.longitudinal_narrative


def test_next_steps_narrative_from_functional_when_lead_signal_fires():
    ig = {
        "signal_results": [
            {"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"},
        ],
    }
    rep = compile_narrative_report_v1(analysis_id="a7", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.next_steps_narrative
    assert "Suggested follow-up" in rep.next_steps_narrative
    assert "• " in rep.next_steps_narrative


def test_n9b_longitudinal_path_proof_direct_compiler_call():
    """N-9B: longitudinal path exercised via compile_narrative_report_v1 only (state_transitions + prior lab snapshot in meta)."""
    ig = {
        "state_transitions": [
            {
                "biomarker_id": "creatinine",
                "from_status": "high",
                "to_status": "normal",
                "transition": "improving",
                "evidence_codes": ["status_change"],
            },
        ],
        "biomarker_nodes": [
            {
                "biomarker_id": "homocysteine",
                "status": "high",
                "lab_value": 16.23,
                "lab_unit": "µmol/L",
            },
        ],
    }
    meta = {
        "prior_biomarker_lab_snapshot_v1": {
            "homocysteine": {"lab_value": 18.5, "lab_unit": "µmol/L"},
        },
    }
    rep = compile_narrative_report_v1(
        analysis_id="n9b-longitudinal-proof",
        meta=meta,
        insight_graph=ig,
        idl_bundle=None,
    )
    assert rep.longitudinal_narrative.strip()
    assert "creatinine" in rep.longitudinal_narrative.lower()
    assert "homocysteine" in rep.longitudinal_narrative.lower()
    assert "improved" in rep.longitudinal_narrative.lower()
    assert "delta" in rep.longitudinal_narrative.lower()
    assert "longitudinal_state_transitions" in rep.meta.get("assets_resolved", [])
    assert "longitudinal_numeric_delta" in rep.meta.get("assets_resolved", [])


def test_longitudinal_lab_delta_without_state_transitions():
    ig = {
        "signal_results": [],
        "state_transitions": [],
        "biomarker_nodes": [
            {
                "biomarker_id": "homocysteine",
                "status": "normal",
                "lab_value": 10.0,
                "lab_unit": "µmol/L",
            },
        ],
    }
    meta = {
        "prior_biomarker_lab_snapshot_v1": {
            "homocysteine": {"lab_value": 15.0, "lab_unit": "µmol/L"},
        },
    }
    rep = compile_narrative_report_v1(analysis_id="a8", meta=meta, insight_graph=ig, idl_bundle=None)
    assert rep.longitudinal_narrative
    assert "delta" in rep.longitudinal_narrative.lower()
    assert "longitudinal_no_state_transitions" in rep.meta.get("skipped", [])


def test_n9b_retail_summary_and_body_overview_with_published_idl():
    """N-9B: benchmark phenotypes are phenotype_allowed; IDL publisher + AB-like signals yield retail + richer overview."""
    ig = {
        "signal_results": [
            {"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"},
            {"signal_id": "signal_homocysteine_elevation_context", "signal_state": "at_risk"},
            {"signal_id": "signal_mcv_high", "signal_state": "at_risk"},
            {"signal_id": "signal_ldl_cholesterol_high", "signal_state": "suboptimal"},
            {"signal_id": "signal_hdl_cholesterol_high", "signal_state": "suboptimal"},
        ],
        "primary_driver_system_id": "cardiovascular_4_biomarkers",
        "supporting_systems": ["hematological_4_biomarkers", "renal_2_biomarkers"],
        "system_capacity_scores": {
            "cardiovascular": 73,
            "metabolic": 100,
            "renal": 100,
            "hepatic": 100,
        },
    }
    bundle = publish_interpretation_display_layer_v1(ig)
    rep = compile_narrative_report_v1(analysis_id="n9b1", meta={}, insight_graph=ig, idl_bundle=bundle)
    assert rep.retail_summary
    assert "Methylation pathway pattern" in rep.retail_summary or "methylation" in rep.retail_summary.lower()
    assert "LDL in context" in rep.retail_summary or "ldl" in rep.retail_summary.lower()
    assert "High capacity" in rep.body_overview or "steady" in rep.body_overview.lower()
    assert "Related systems also noted" in rep.body_overview or "related systems" in rep.body_overview.lower()
    assert "retail_summary_from_idl" in rep.meta.get("assets_resolved", [])
