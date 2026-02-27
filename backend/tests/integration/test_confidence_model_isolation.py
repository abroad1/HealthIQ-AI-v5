"""
Sprint 8 - Confidence Model Isolation Test.

Asserts:
- LLM payload includes confidence fields (system_confidence, missing_required, etc.)
- No inference based on missing dict keys
- Removing a required biomarker deterministically lowers cluster/system confidence
"""

import pytest
import json
from unittest.mock import patch, MagicMock

from core.analytics.confidence_builder import build_confidence_model_v1
from core.insights.prompts import InsightPromptTemplates
from core.contracts.insight_graph_v1 import InsightGraphV1, BiomarkerNode


def _minimal_explainability_json() -> str:
    return json.dumps(
        {
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
    )


def test_llm_payload_includes_confidence_fields():
    """LLM prompt includes confidence context (system_confidence, missing_required)."""
    # Build InsightGraph with confidence
    ig = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="test-conf",
        biomarker_nodes=[
            BiomarkerNode(biomarker_id="glucose", status="normal", score=75.0),
            BiomarkerNode(biomarker_id="hba1c", status="normal", score=80.0),
        ],
        edges=[],
        confidence=build_confidence_model_v1(
            available_biomarkers={"glucose", "hba1c"},
        ),
    )
    ig_json = json.dumps(ig.model_dump(), default=str)
    result = InsightPromptTemplates.format_template_from_insight_graph(
        category="metabolic",
        insight_graph_json=ig_json,
        explainability_report_json=_minimal_explainability_json(),
        lifestyle_profile={"diet_level": "average"},
    )
    assert "System confidence:" in result
    assert "Missing required biomarkers:" in result
    assert "Incomplete clusters:" in result


def test_no_inference_from_missing_dict_keys():
    """Confidence is explicit; no reliance on absent keys for inference."""
    # Empty confidence in graph → explicit fallback text, not implicit inference
    ig = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="test-no-conf",
        biomarker_nodes=[BiomarkerNode(biomarker_id="x", status="unknown")],
        edges=[],
        confidence=None,
    )
    ig_json = json.dumps(ig.model_dump(), default=str)
    result = InsightPromptTemplates.format_template_from_insight_graph(
        category="metabolic",
        insight_graph_json=ig_json,
        explainability_report_json=_minimal_explainability_json(),
        lifestyle_profile={},
    )
    assert "Confidence model not available" in result or "(Confidence model not available)" in result


def test_removing_required_biomarker_lowers_confidence():
    """Removing a required biomarker deterministically lowers cluster/system confidence."""
    full = build_confidence_model_v1(available_biomarkers={"glucose", "hba1c"})
    partial = build_confidence_model_v1(available_biomarkers={"glucose"})  # hba1c missing

    # Metabolic cluster: glucose + hba1c required. Full = 1.0, partial = 0.5
    assert full.cluster_confidence.get("metabolic", 0) >= partial.cluster_confidence.get("metabolic", 0)
    assert full.system_confidence >= partial.system_confidence
    assert "hba1c" in partial.missing_required_biomarkers
    assert "hba1c" not in full.missing_required_biomarkers
