"""
Sprint 11 - Enforcement: no raw biomarker fields leak into InsightGraph/prompt.
"""

import json
import re

from core.contracts.biomarker_context_v1 import BiomarkerContextNode
from core.contracts.insight_graph_v1 import BiomarkerNode, InsightGraphV1
from core.insights.prompts import InsightPromptTemplates

_FORBIDDEN_KEYS = {"value", "unit", "range", "reference_range", "lab_range", "lower", "upper"}


def _contains_forbidden_key(payload: str) -> bool:
    for key in _FORBIDDEN_KEYS:
        if re.search(rf'["\']{key}["\']\s*:', payload):
            return True
    return False


def test_insight_graph_serialized_contains_no_raw_fields():
    """InsightGraph JSON boundary excludes raw biomarker fields."""
    graph = InsightGraphV1(
        analysis_id="enforcement-1",
        biomarker_nodes=[
            BiomarkerNode(biomarker_id="glucose", status="normal", score=77.0),
        ],
        biomarker_context_version="1.0.0",
        biomarker_context_hash="abc123",
        biomarker_context=[
            BiomarkerContextNode(
                biomarker_id="glucose",
                status="normal",
                score=77.0,
                reason_codes=["status_normal", "score_high_band"],
                missing_codes=[],
                relationship_codes=[],
            )
        ],
        edges=[],
    )
    payload = json.dumps(graph.model_dump(), sort_keys=True)
    assert not _contains_forbidden_key(payload)


def test_prompt_from_insight_graph_contains_no_units_or_raw_field_keys():
    """Prompt derived from InsightGraph must not contain unit leakage patterns."""
    graph = InsightGraphV1(
        analysis_id="enforcement-2",
        biomarker_nodes=[
            BiomarkerNode(biomarker_id="hba1c", status="high", score=22.0),
        ],
        biomarker_context_version="1.0.0",
        biomarker_context_hash="abc123",
        biomarker_context=[
            BiomarkerContextNode(
                biomarker_id="hba1c",
                status="high",
                score=22.0,
                reason_codes=["status_high", "score_low_band"],
                missing_codes=[],
                relationship_codes=[],
            )
        ],
        edges=[],
    )
    prompt = InsightPromptTemplates.format_template_from_insight_graph(
        category="metabolic",
        insight_graph_json=json.dumps(graph.model_dump()),
        lifestyle_profile={"diet_level": "average"},
    )
    lowered = prompt.lower()
    assert not _contains_forbidden_key(prompt)
    assert "mg/dl" not in lowered
    assert "mmol" not in lowered
