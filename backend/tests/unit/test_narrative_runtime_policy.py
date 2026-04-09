"""BE-S1B — governed narrative runtime policy for insights[] synthesis path."""

import pytest

from config.env import settings
from core.insights.narrative_runtime_policy import resolve_narrative_llm_allow_llm
from core.insights.synthesis import InsightSynthesizer, MockLLMClient


def _patch_settings(monkeypatch, *, mode: str, llm_enabled: bool = True):
    monkeypatch.setattr(settings, "HEALTHIQ_MODE", mode)
    monkeypatch.setattr(settings, "LLM_ENABLED", llm_enabled)


def test_api_default_production_requires_double_opt_in(monkeypatch):
    monkeypatch.delenv("HEALTHIQ_NARRATIVE_LLM", raising=False)
    monkeypatch.delenv("HEALTHIQ_ENABLE_LLM", raising=False)
    _patch_settings(monkeypatch, mode="production")
    d = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=None)
    assert d.synthesizer_allow_llm is False
    assert "NARRATIVE_LLM" in d.reason


def test_api_default_with_double_opt_in_enables_live_gate(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_NARRATIVE_LLM", "1")
    monkeypatch.setenv("HEALTHIQ_ENABLE_LLM", "1")
    _patch_settings(monkeypatch, mode="production")
    d = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=None)
    assert d.synthesizer_allow_llm is True
    assert d.reason == "api_path_double_opt_in_passed"


def test_explicit_orchestrator_true_skips_master_switch(monkeypatch):
    monkeypatch.delenv("HEALTHIQ_NARRATIVE_LLM", raising=False)
    _patch_settings(monkeypatch, mode="production")
    d = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=True)
    assert d.synthesizer_allow_llm is True
    assert d.reason == "orchestrator_explicit_true"


def test_explicit_false_overrides_env(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_NARRATIVE_LLM", "1")
    monkeypatch.setenv("HEALTHIQ_ENABLE_LLM", "1")
    _patch_settings(monkeypatch, mode="production")
    d = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=False)
    assert d.synthesizer_allow_llm is False


def test_test_mode_forces_mock_even_when_explicit_true(monkeypatch):
    _patch_settings(monkeypatch, mode="test")
    d = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=True)
    assert d.synthesizer_allow_llm is False


def test_synthesizer_includes_narrative_runtime_in_summary(monkeypatch):
    _patch_settings(monkeypatch, mode="test")
    s = InsightSynthesizer(llm_client=MockLLMClient())
    from core.models.context import AnalysisContext
    from core.models.user import User
    from core.models.biomarker import BiomarkerPanel
    from datetime import datetime, UTC

    ctx = AnalysisContext(
        analysis_id="nr1",
        user=User(user_id="u", age=30, gender="male", lifestyle_factors={}),
        biomarker_panel=BiomarkerPanel(biomarkers={}),
        created_at=datetime.now(UTC).isoformat(),
    )
    from core.contracts.insight_graph_v1 import InsightGraphV1, BiomarkerNode

    ig = InsightGraphV1(
        analysis_id="nr1",
        biomarker_nodes=[BiomarkerNode(biomarker_id="glucose", status="normal", score=70.0)],
        edges=[],
    )
    expl = {
        "run_metadata": {"report_version": "1.0.0"},
        "conflict_summary": [],
        "precedence_summary": [],
        "dominance_resolution": {
            "cycle_check": {"has_cycle": False, "status_code": "acyclic"},
            "direct_edges": [],
            "transitive_edges": [],
            "influence_ordering": {
                "primary_driver_system_id": "metabolic",
                "supporting_systems": [],
                "influence_order": ["metabolic"],
            },
        },
        "causal_edges": [],
        "arbitration_decisions": {
            "primary_driver_system_id": "metabolic",
            "supporting_systems": [],
            "decision_trace": [],
            "tie_breakers": [],
        },
        "calibration_impact": {"system_id": "metabolic", "final_calibration_tier": "p1", "reasons": []},
        "replay_stamps": {
            "conflict_registry_version": "1.0.0",
            "conflict_registry_hash": "h1",
            "arbitration_registry_version": "1.0.0",
            "arbitration_registry_hash": "h2",
            "arbitration_version": "1.0.0",
            "arbitration_hash": "h3",
            "explainability_hash": "h4",
        },
    }
    result = s.synthesize_insights(
        context=ctx,
        insight_graph=ig,
        explainability_report=expl,
        lifestyle_profile={},
        requested_categories=["metabolic"],
        max_insights_per_category=1,
    )
    nr = result.synthesis_summary.get("narrative_runtime") or {}
    assert nr.get("policy_version") == "1.0.0"
    assert nr.get("runtime_mode") == "deterministic_mock"
    assert nr.get("client_constructor_injected") is True
