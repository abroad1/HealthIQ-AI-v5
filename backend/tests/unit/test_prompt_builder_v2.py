"""
Unit tests for Prompt Builder v2.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, UTC

from core.prompt_builder.v2 import build_prompt_v2
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


@pytest.fixture
def canonical_small_panel():
    """Load canonical small panel fixture."""
    panel_path = Path(__file__).parent.parent / "fixtures" / "panels" / "canonical_small.json"
    with open(panel_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def analysis_context(canonical_small_panel):
    """Create AnalysisContext from canonical small panel."""
    user = User(
        user_id="test_user",
        age=35,
        gender="male"
    )
    
    biomarkers = {}
    for bm_data in canonical_small_panel["biomarkers"]:
        biomarkers[bm_data["name"]] = BiomarkerValue(
            name=bm_data["name"],
            value=bm_data["value"],
            unit=bm_data["unit"],
            reference_range=bm_data.get("reference_range")
        )
    
    biomarker_panel = BiomarkerPanel(
        biomarkers=biomarkers,
        source="test",
        version="1.0"
    )
    
    return AnalysisContext(
        analysis_id="test_analysis",
        user=user,
        biomarker_panel=biomarker_panel,
        created_at=datetime.now(UTC).isoformat()
    )


def test_build_prompt_v2_schema(analysis_context):
    """Test that build_prompt_v2 returns correct schema with required keys."""
    prompt = build_prompt_v2(analysis_context)
    
    # Check required top-level keys
    assert "meta" in prompt
    assert "user" in prompt
    assert "biomarkers" in prompt
    assert "completeness" in prompt
    assert "clusters" in prompt
    assert "red_flags" in prompt
    assert "insight_stubs" in prompt
    assert "policy" in prompt
    
    # Check meta structure
    assert prompt["meta"]["result_version"] == "2.0"
    assert "timestamp" in prompt["meta"]
    
    # Check user structure
    assert "age" in prompt["user"]
    assert "sex" in prompt["user"]
    assert prompt["user"]["sex"] in ["male", "female", "other"]
    
    # Check biomarkers structure
    assert isinstance(prompt["biomarkers"], list)
    for bm in prompt["biomarkers"]:
        assert "id" in bm
        assert "value" in bm
        assert "unit" in bm
        assert "lab_range" in bm  # Can be None
    
    # Check completeness structure
    assert "score" in prompt["completeness"]
    assert "missing" in prompt["completeness"]
    assert 0.0 <= prompt["completeness"]["score"] <= 1.0
    
    # Check clusters (list)
    assert isinstance(prompt["clusters"], list)
    
    # Check red_flags (list)
    assert isinstance(prompt["red_flags"], list)
    
    # Check insight_stubs (list)
    assert isinstance(prompt["insight_stubs"], list)
    
    # Check policy structure
    assert "rules" in prompt["policy"]
    assert "max_fields" in prompt["policy"]
    assert prompt["policy"]["max_fields"] == 32


def test_build_prompt_v2_stable_snapshot(analysis_context):
    """Test that prompt matches expected snapshot structure."""
    prompt = build_prompt_v2(analysis_context)
    
    # Load expected snapshot
    snapshot_path = Path(__file__).parent.parent / "snapshots" / "prompt_v2_canonical.json"
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        expected = json.load(f)
    
    # Compare structure (ignore timestamp)
    assert prompt["meta"]["result_version"] == expected["meta"]["result_version"]
    assert prompt["user"] == expected["user"]
    assert len(prompt["biomarkers"]) == len(expected["biomarkers"])
    
    # Compare biomarkers (by ID)
    prompt_bm_dict = {bm["id"]: bm for bm in prompt["biomarkers"]}
    expected_bm_dict = {bm["id"]: bm for bm in expected["biomarkers"]}
    
    for bm_id in prompt_bm_dict:
        assert bm_id in expected_bm_dict
        assert prompt_bm_dict[bm_id]["value"] == expected_bm_dict[bm_id]["value"]
        assert prompt_bm_dict[bm_id]["unit"] == expected_bm_dict[bm_id]["unit"]
    
    # Compare policy
    assert prompt["policy"] == expected["policy"]


def test_build_prompt_v2_includes_lab_ranges(analysis_context):
    """Test that prompt includes lab ranges when available."""
    prompt = build_prompt_v2(analysis_context)
    
    # All biomarkers in fixture have lab ranges
    for bm in prompt["biomarkers"]:
        assert bm["lab_range"] is not None
        assert "min" in bm["lab_range"]
        assert "max" in bm["lab_range"]
        assert "unit" in bm["lab_range"]
        assert "source" in bm["lab_range"]


def test_build_prompt_v2_clusters_when_present(analysis_context):
    """Test that prompt includes clusters when present in context."""
    # Create new context with clusters (cannot modify frozen model)
    from core.models.context import AnalysisContext
    from datetime import datetime, UTC
    
    context_with_clusters = AnalysisContext(
        analysis_id=analysis_context.analysis_id,
        user=analysis_context.user,
        biomarker_panel=analysis_context.biomarker_panel,
        questionnaire_responses=analysis_context.questionnaire_responses,
        lifestyle_factors=analysis_context.lifestyle_factors,
        medical_history=analysis_context.medical_history,
        analysis_parameters={
            "clusters_v2": [
                {"id": "metabolic", "score": 60, "band": "amber"},
                {"id": "cardiovascular", "score": 70, "band": "red"}
            ]
        },
        created_at=analysis_context.created_at,
        version=analysis_context.version
    )
    
    prompt = build_prompt_v2(context_with_clusters)
    
    assert len(prompt["clusters"]) == 2
    assert prompt["clusters"][0]["id"] == "metabolic"
    assert prompt["clusters"][0]["score"] == 60
    assert prompt["clusters"][0]["band"] == "amber"


def test_build_prompt_v2_no_clusters_when_absent(analysis_context):
    """Test that prompt has empty clusters list when not present."""
    prompt = build_prompt_v2(analysis_context)
    
    assert prompt["clusters"] == []

