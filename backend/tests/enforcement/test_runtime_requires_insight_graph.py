"""
Sprint 15 - Enforcement: production runtime requires InsightGraph path.
"""

from types import SimpleNamespace

import pytest

from core.insights.synthesis import InsightSynthesizer, MockLLMClient


def test_production_synthesis_rejects_missing_insight_graph(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_MODE", "production")
    synthesizer = InsightSynthesizer(llm_client=MockLLMClient())
    context = SimpleNamespace(analysis_id="a-1")
    with pytest.raises(ValueError, match="insight_graph is required"):
        synthesizer.synthesize_insights(
            context=context,
            insight_graph=None,
            biomarker_scores={"health_system_scores": {}},
            clustering_results={"clusters": []},
            lifestyle_profile={},
            requested_categories=["metabolic"],
            max_insights_per_category=1,
        )


def test_production_synthesis_does_not_use_legacy_formatter(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_MODE", "production")
    synthesizer = InsightSynthesizer(llm_client=MockLLMClient())
    context = SimpleNamespace(analysis_id="a-2")

    def _legacy_forbidden(*args, **kwargs):
        raise AssertionError("Legacy formatter path must not be called in production")

    synthesizer._generate_category_insights = _legacy_forbidden  # type: ignore[method-assign]
    result = synthesizer.synthesize_insights(
        context=context,
        insight_graph={"graph_version": "1.0.0", "analysis_id": "a-2", "biomarker_nodes": [], "edges": []},
        explainability_report={
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
        },
        lifestyle_profile={},
        requested_categories=["metabolic"],
        max_insights_per_category=1,
    )
    assert result is not None
