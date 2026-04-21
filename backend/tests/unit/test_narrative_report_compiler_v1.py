"""N-8 — deterministic narrative compiler v1 (governed asset assembly)."""

from __future__ import annotations

from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1


def test_compiler_emits_lead_when_homocysteine_signal_fires():
    ig = {
        "signal_results": [
            {"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"},
        ],
        "primary_driver_system_id": "vascular",
    }
    rep = compile_narrative_report_v1(analysis_id="a1", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.lead_narrative
    assert "homocysteine" in rep.lead_narrative.lower() or "one-carbon" in rep.lead_narrative.lower()
    assert rep.body_overview
    assert "vascular" in rep.body_overview.lower()


def test_compiler_emits_secondary_when_ldl_signal_fires():
    ig = {
        "signal_results": [
            {"signal_id": "signal_ldl_cholesterol_high", "signal_state": "suboptimal"},
        ],
    }
    rep = compile_narrative_report_v1(analysis_id="a2", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.secondary_narratives
    assert "lipid" in rep.secondary_narratives.lower() or "ldl" in rep.secondary_narratives.lower()


def test_compiler_no_raise_when_assets_missing(monkeypatch, tmp_path):
    from core.analytics import narrative_report_compiler_v1 as mod

    monkeypatch.setattr(mod, "_ENTITIES_PATH", tmp_path / "missing.yaml")
    rep = compile_narrative_report_v1(analysis_id="a3", meta={}, insight_graph={}, idl_bundle=None)
    assert rep.meta.get("skipped")


def test_lifestyle_bridges_surface_when_active():
    meta = {
        "lifestyle_interpretation_bridges_v1": {
            "alcohol_methylation_macrocytosis": {"active": True, "rationale_codes": ["test"]},
        }
    }
    rep = compile_narrative_report_v1(analysis_id="a4", meta=meta, insight_graph={}, idl_bundle=None)
    assert "Lifestyle bridge" in rep.lead_narrative
