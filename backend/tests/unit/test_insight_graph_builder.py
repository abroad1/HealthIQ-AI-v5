"""
Sprint 7 - Unit tests for InsightGraph builder and contract.
"""

import pytest
from core.contracts.insight_graph_v1 import InsightGraphV1, INSIGHTGRAPH_V1_VERSION
from core.analytics.insight_graph_builder import build_insight_graph_v1


def test_builder_produces_valid_insight_graph():
    """Builder produces valid InsightGraph_v1."""
    scoring = {
        "health_system_scores": {
            "metabolic": {
                "biomarker_scores": [
                    {"biomarker_name": "glucose", "value": 95.0, "score": 75},
                    {"biomarker_name": "hba1c", "value": 5.2, "score": 80},
                ]
            }
        }
    }
    clustering = {"clusters": [{"cluster_id": "metabolic", "name": "Metabolic", "biomarkers": ["glucose", "hba1c"], "confidence": 0.9, "severity": "normal"}]}
    graph = build_insight_graph_v1(
        analysis_id="test-123",
        scoring_result=scoring,
        clustering_result=clustering,
    )
    assert graph is not None
    assert isinstance(graph, InsightGraphV1)
    assert graph.graph_version == INSIGHTGRAPH_V1_VERSION
    assert graph.analysis_id == "test-123"


def test_version_stamp_present_and_stable():
    """Version stamp present and stable."""
    graph = build_insight_graph_v1(
        analysis_id="v",
        scoring_result={},
        clustering_result={},
    )
    assert graph.graph_version == INSIGHTGRAPH_V1_VERSION
    assert len(graph.graph_version) > 0


def test_ordering_deterministic():
    """Biomarker nodes sorted by biomarker_id."""
    scoring = {
        "health_system_scores": {
            "x": {
                "biomarker_scores": [
                    {"biomarker_name": "z_marker", "value": 1.0, "score": 50},
                    {"biomarker_name": "a_marker", "value": 2.0, "score": 50},
                ]
            }
        }
    }
    graph = build_insight_graph_v1(
        analysis_id="o",
        scoring_result=scoring,
        clustering_result={},
    )
    ids = [n.biomarker_id for n in graph.biomarker_nodes]
    assert ids == sorted(ids)
    assert ids == ["a_marker", "z_marker"]


def test_relationship_registry_load_error_raises_in_normal_mode(monkeypatch):
    """Registry errors must fail loudly in normal runtime mode."""
    monkeypatch.setenv("HEALTHIQ_MODE", "")

    def _boom():
        raise ValueError("invalid relationships registry")

    monkeypatch.setattr("core.analytics.insight_graph_builder.load_relationship_registry", _boom)

    with pytest.raises(ValueError, match="invalid relationships registry"):
        build_insight_graph_v1(
            analysis_id="bad-registry",
            scoring_result={},
            clustering_result={},
        )


def test_relationship_registry_load_error_soft_fails_in_fixture_mode(monkeypatch):
    """Fixture mode may soft-fail and emit empty relationship outputs."""
    monkeypatch.setenv("HEALTHIQ_MODE", "fixture")

    def _boom():
        raise ValueError("invalid relationships registry")

    monkeypatch.setattr("core.analytics.insight_graph_builder.load_relationship_registry", _boom)

    graph = build_insight_graph_v1(
        analysis_id="fixture-registry",
        scoring_result={},
        clustering_result={},
    )
    assert graph.relationships == []
    assert graph.relationship_registry_version is None
    assert graph.relationship_registry_hash is None


def test_builder_carries_signal_registry_and_results_fields():
    sha = "a" * 64
    graph = build_insight_graph_v1(
        analysis_id="sig-1",
        scoring_result={},
        clustering_result={},
        signal_registry_version="abc123def456",
        signal_registry_hash="abc123def456",
        signal_registry_hash_sha256=sha,
        signal_results=[{"signal_id": "signal_alpha", "signal_state": "suboptimal"}],
    )
    assert graph.signal_registry_version == "abc123def456"
    assert graph.signal_registry_hash == "abc123def456"
    assert graph.signal_results == [{"signal_id": "signal_alpha", "signal_state": "suboptimal"}]
    assert graph.report_v1 is not None
    assert graph.report_v1.meta.signal_registry_hash_sha256 == sha


def test_builder_defaults_signal_results_to_empty_list():
    graph = build_insight_graph_v1(
        analysis_id="sig-2",
        scoring_result={},
        clustering_result={},
        signal_registry_version=None,
        signal_registry_hash=None,
        signal_registry_hash_sha256=None,
        signal_results=None,
    )
    assert graph.signal_registry_version is None
    assert graph.signal_registry_hash is None
    assert graph.signal_results == []


def test_builder_preserves_signal_results_with_additive_interaction_outputs():
    payload = [
        {"signal_id": "signal_hba1c_high", "signal_state": "suboptimal"},
        {"signal_id": "signal_ggt_high", "signal_state": "at_risk"},
        {"signal_id": "signal_crp_high", "signal_state": "suboptimal"},
    ]
    graph = build_insight_graph_v1(
        analysis_id="sig-3",
        scoring_result={},
        clustering_result={},
        signal_registry_version="reg-v1",
        signal_registry_hash="hash-v1",
        signal_results=payload,
    )
    assert graph.signal_results == payload
    assert isinstance(graph.interaction_graph, dict)
    assert isinstance(graph.interaction_chains, list)
    assert isinstance(graph.interaction_summary, list)
    assert graph.report_v1 is not None
    assert graph.report_v1.report_version == "v1"


def test_builder_interaction_outputs_match_deterministic_snapshot():
    payload = [
        {"signal_id": "signal_tsh_high", "signal_state": "at_risk", "confidence": 0.78},
        {"signal_id": "signal_ldl_cholesterol_high", "signal_state": "suboptimal", "confidence": 0.81},
        {"signal_id": "signal_hba1c_high", "signal_state": "suboptimal", "confidence": 0.66},
    ]
    graph_one = build_insight_graph_v1(
        analysis_id="sig-snapshot-1",
        scoring_result={},
        clustering_result={},
        signal_registry_version="reg-snap",
        signal_registry_hash="hash-snap",
        signal_results=payload,
    )
    graph_two = build_insight_graph_v1(
        analysis_id="sig-snapshot-2",
        scoring_result={},
        clustering_result={},
        signal_registry_version="reg-snap",
        signal_registry_hash="hash-snap",
        signal_results=payload,
    )

    expected_chains = [["signal_tsh_high", "signal_ldl_cholesterol_high", "signal_hba1c_high"]]
    expected_summary = [
        {
            "chain_id": "chain_001",
            "priority_rank": 1,
            "signals_involved": ["signal_tsh_high", "signal_ldl_cholesterol_high", "signal_hba1c_high"],
            "chain_summary_text": "signal_tsh_high -> signal_ldl_cholesterol_high -> signal_hba1c_high (edge evidence: strong, moderate)",
            "confidence": 0.66,
        }
    ]

    assert graph_one.signal_results == payload
    assert graph_two.signal_results == payload
    assert graph_one.interaction_chains == expected_chains
    assert graph_two.interaction_chains == expected_chains
    assert graph_one.interaction_summary == expected_summary
    assert graph_two.interaction_summary == expected_summary
