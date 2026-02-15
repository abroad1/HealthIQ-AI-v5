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
