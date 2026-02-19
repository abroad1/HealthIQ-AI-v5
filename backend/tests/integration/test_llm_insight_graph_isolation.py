"""
Sprint 7 - LLM isolation enforcement test.

Asserts: payload going into LLM adapter equals InsightGraph_v1 derived content only;
does NOT contain raw biomarker map or computation inputs.
PRD §4.7: No raw values, units, reference ranges, or lab bounds.
"""

import pytest
import json
import re
from typing import List, Tuple
from unittest.mock import patch, MagicMock
from core.insights.synthesis import InsightSynthesizer
from core.insights.prompts import InsightPromptTemplates
from core.contracts.insight_graph_v1 import InsightGraphV1, BiomarkerNode
from core.contracts.biomarker_context_v1 import BiomarkerContextNode
from core.contracts.state_transition_v1 import BiomarkerTransitionNode

# PRD §4.7: Forbidden keys in LLM payload (raw biomarker data)
_FORBIDDEN_KEYS = {"value", "unit", "range", "reference_range", "lab_range", "lower", "upper"}


def _payload_contains_forbidden_keys(payload: str) -> Tuple[bool, List[str]]:
    """
    Recursively check if payload contains forbidden keys (raw biomarker data).
    Returns (has_forbidden, list of found forbidden keys).
    """
    found = []
    # Scan for JSON key patterns: "value":, "unit":, etc.
    for key in _FORBIDDEN_KEYS:
        if re.search(rf'["\']{key}["\']\s*:', payload):
            found.append(key)
    return (len(found) > 0, found)


@pytest.fixture
def mock_context():
    ctx = MagicMock()
    ctx.analysis_id = "test-iso"
    return ctx


@pytest.fixture
def minimal_insight_graph():
    """PRD §4.7: BiomarkerNode has only biomarker_id, status, score; no value/unit/range."""
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="test-iso",
        biomarker_nodes=[
            BiomarkerNode(biomarker_id="glucose", status="normal", score=75.0),
            BiomarkerNode(biomarker_id="hba1c", status="normal", score=80.0),
        ],
        biomarker_context_version="1.0.0",
        biomarker_context_hash="testhash",
        biomarker_context=[
            BiomarkerContextNode(
                biomarker_id="glucose",
                status="normal",
                score=75.0,
                reason_codes=["status_normal", "score_high_band"],
                missing_codes=[],
                relationship_codes=[],
            )
        ],
        state_transition_version="1.0.0",
        state_transition_hash="statehash",
        state_transitions=[
            BiomarkerTransitionNode(
                biomarker_id="glucose",
                from_status="normal",
                to_status="normal",
                transition="stable_normal",
                evidence_codes=["status_change"],
            )
        ],
        edges=[],
    )


def test_payload_from_insight_graph_contains_no_raw_biomarker_dict(mock_context, minimal_insight_graph):
    """
    When insight_graph is provided, the prepared payload uses only derived data from InsightGraph.
    No raw biomarker map (e.g. context.biomarker_panel) is passed to the LLM.
    PRD §4.7: No numeric biomarker values, units, reference_range, or lab bounds.
    """
    captured_prompt = None

    def capture_generate(system_prompt, user_prompt, category):
        nonlocal captured_prompt
        captured_prompt = user_prompt
        return {"insights": [{"id": "x", "category": category, "summary": "ok", "evidence": {}, "confidence": 0.8, "severity": "info", "recommendations": [], "biomarkers_involved": [], "lifestyle_factors": []}]}

    with patch.object(InsightSynthesizer, '_create_llm_client') as mock_client:
        mock_llm = MagicMock()
        mock_llm.generate_insights = capture_generate
        mock_client.return_value = mock_llm

        synthesizer = InsightSynthesizer(llm_client=mock_llm)
        synthesizer.synthesize_insights(
            context=mock_context,
            insight_graph=minimal_insight_graph,
            lifestyle_profile={"diet_level": "average"},
        )

    assert captured_prompt is not None
    # Prepared payload must contain biomarker data derived from InsightGraph (biomarker nodes)
    assert "glucose" in captured_prompt
    assert "hba1c" in captured_prompt
    assert "Biomarker Context" in captured_prompt
    if "state_transitions" in captured_prompt:
        assert "from_status" in captured_prompt
        assert "to_status" in captured_prompt
        assert "transition" in captured_prompt
    # Must NOT contain raw structure that would indicate raw biomarker dict
    assert "biomarker_panel" not in captured_prompt
    assert "raw_biomarkers" not in captured_prompt.lower()
    assert "prior_snapshots" not in captured_prompt.lower()
    # PRD §4.7: No forbidden keys (value, unit, range, lower, upper, etc.)
    has_forbidden, found = _payload_contains_forbidden_keys(captured_prompt)
    assert not has_forbidden, f"Payload contains forbidden keys: {found}"


def test_format_template_from_insight_graph_produces_structured_only(minimal_insight_graph):
    """
    format_template_from_insight_graph produces prompt with only InsightGraph-derived data.
    PRD §4.7: No value, unit, reference_range, lower, upper in payload.
    """
    ig_json = json.dumps(minimal_insight_graph.model_dump(), default=str)
    result = InsightPromptTemplates.format_template_from_insight_graph(
        category="metabolic",
        insight_graph_json=ig_json,
        lifestyle_profile={"diet_level": "average"},
    )
    assert "glucose" in result
    assert "hba1c" in result
    assert "metabolic" in result.lower()
    assert "Biomarker Context" in result
    if "state_transitions" in result:
        assert "from_status" in result
        assert "to_status" in result
        assert "transition" in result
    assert "prior_snapshots" not in result.lower()
    has_forbidden, found = _payload_contains_forbidden_keys(result)
    assert not has_forbidden, f"Formatted prompt contains forbidden keys: {found}"
