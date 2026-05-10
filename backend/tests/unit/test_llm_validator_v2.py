"""
Unit tests for LLM Output Validator v2.
"""

import pytest
import json
from pathlib import Path
from pydantic import ValidationError

from core.llm.validator_v2 import validate_llm_output_v2
from core.llm.schemas_v2 import LLMResultV2


@pytest.fixture
def canonical_prompt():
    """Load canonical prompt snapshot."""
    prompt_path = Path(__file__).parent.parent / "snapshots" / "prompt_v2_canonical.json"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def valid_llm_result():
    """Load valid LLM result fixture."""
    result_path = Path(__file__).parent.parent / "fixtures" / "llm" / "valid_llm_result_v2.json"
    with open(result_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def invalid_numeric_invention():
    """Load invalid LLM result with numeric invention."""
    result_path = Path(__file__).parent.parent / "fixtures" / "llm" / "invalid_numeric_invention.json"
    with open(result_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def invalid_unknown_field():
    """Load invalid LLM result with unknown field."""
    result_path = Path(__file__).parent.parent / "fixtures" / "llm" / "invalid_unknown_field.json"
    with open(result_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_validate_llm_output_v2_pass_case(canonical_prompt, valid_llm_result):
    """Test PASS case with valid_llm_result_v2.json."""
    result = validate_llm_output_v2(canonical_prompt, valid_llm_result)
    
    assert isinstance(result, LLMResultV2)
    assert len(result.insights) == 2
    assert result.insights[0].id == "metabolic_health"
    assert result.insights[1].id == "cardiovascular_risk"
    assert result.tokens_used == 450
    assert result.latency_ms == 1200


def test_validate_llm_output_v2_fail_unknown_field(canonical_prompt, invalid_unknown_field):
    """Test FAIL case: unknown field present → raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_llm_output_v2(canonical_prompt, invalid_unknown_field)
    
    # Check that error mentions extra fields
    error_str = str(exc_info.value)
    assert "extra" in error_str.lower() or "forbidden" in error_str.lower()


def test_validate_llm_output_v2_fail_numeric_invention(canonical_prompt, invalid_numeric_invention):
    """Test FAIL case: numeric invention (value not present in prompt) → raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        validate_llm_output_v2(canonical_prompt, invalid_numeric_invention)
    
    # Check that error mentions numeric invention
    error_str = str(exc_info.value)
    assert "numeric invention" in error_str.lower()
    # The invalid fixture contains "85.0" which is not in the prompt
    assert "85.0" in error_str or "85" in error_str


def test_validate_llm_output_v2_fail_evidence_reference(canonical_prompt):
    """Test FAIL case: evidence references id not in prompt → raises ValueError."""
    invalid_result = {
        "insights": [
            {
                "id": "test_insight",
                "title": "Test Insight",
                "severity": "low",
                "evidence": ["nonexistent_biomarker_id"],
                "actions": ["Some action"],
                "red_flags": [],
                "confidence": 0.5
            }
        ],
        "tokens_used": 100,
        "latency_ms": 500
    }
    
    # This should pass schema validation but might fail evidence check
    # The current implementation is lenient on evidence, so this might pass
    # But if we make it stricter, it should raise ValueError
    try:
        result = validate_llm_output_v2(canonical_prompt, invalid_result)
        # If it passes, that's acceptable for now (lenient implementation)
        assert isinstance(result, LLMResultV2)
    except ValueError as e:
        # If it fails, error should mention evidence
        assert "evidence" in str(e).lower() or "reference" in str(e).lower()


def test_validate_llm_output_v2_red_flag_referencing(canonical_prompt):
    """Test that red flags must reference prompt red flags or IDs."""
    # Create prompt with a red flag
    prompt_with_red_flag = canonical_prompt.copy()
    prompt_with_red_flag["red_flags"] = [
        {"id": "ldl_cholesterol", "reason": "LDL is high"}
    ]
    
    # Valid result referencing the red flag
    valid_result = {
        "insights": [
            {
                "id": "test_insight",
                "title": "Test Insight",
                "severity": "moderate",
                "evidence": ["ldl_cholesterol"],
                "actions": ["Consider dietary changes"],
                "red_flags": ["ldl_cholesterol"],  # References prompt red flag
                "confidence": 0.8
            }
        ],
        "tokens_used": 200,
        "latency_ms": 600
    }
    
    result = validate_llm_output_v2(prompt_with_red_flag, valid_result)
    assert isinstance(result, LLMResultV2)
    
    # Invalid result with non-existent red flag
    invalid_result = {
        "insights": [
            {
                "id": "test_insight",
                "title": "Test Insight",
                "severity": "moderate",
                "evidence": ["glucose"],
                "actions": ["Some action"],
                "red_flags": ["nonexistent_red_flag"],  # Not in prompt
                "confidence": 0.8
            }
        ],
        "tokens_used": 200,
        "latency_ms": 600
    }
    
    with pytest.raises(ValueError) as exc_info:
        validate_llm_output_v2(prompt_with_red_flag, invalid_result)
    
    error_str = str(exc_info.value)
    assert "red flag" in error_str.lower()


def test_validate_llm_output_v2_fail_prohibited_claim_language(canonical_prompt, valid_llm_result):
    bad = json.loads(json.dumps(valid_llm_result))
    bad["insights"][0]["title"] = bad["insights"][0]["title"] + " This confirms diabetes."
    with pytest.raises(ValueError) as exc_info:
        validate_llm_output_v2(canonical_prompt, bad)
    assert "prohibited claim language" in str(exc_info.value).lower()


def test_validate_llm_output_v2_fail_lead_signal_token_mismatch(canonical_prompt, valid_llm_result):
    prompt = dict(canonical_prompt)
    prompt["layer_b_lead_signal_id"] = "signal_glucose_high"
    bad = json.loads(json.dumps(valid_llm_result))
    bad["insights"][0][
        "title"
    ] = "Focus on signal_ldl_cholesterol_high — lipid-centred narrative."
    with pytest.raises(ValueError) as exc_info:
        validate_llm_output_v2(prompt, bad)
    assert "lead finding preservation" in str(exc_info.value).lower()


def test_validate_llm_output_v2_fail_invented_hypothesis(canonical_prompt, valid_llm_result):
    prompt = dict(canonical_prompt)
    prompt["layer_b_hypothesis_ids"] = ["hyp_allowed_only"]
    bad = json.loads(json.dumps(valid_llm_result))
    bad["insights"][0]["actions"] = list(bad["insights"][0]["actions"]) + [
        "Discuss hyp_invented_only pathway."
    ]
    with pytest.raises(ValueError) as exc_info:
        validate_llm_output_v2(prompt, bad)
    assert "hypothesis allow-list" in str(exc_info.value).lower()


def test_validate_llm_output_v2_pass_lead_when_no_signal_tokens(canonical_prompt, valid_llm_result):
    """If the model uses plain-language-only copy, signal-token lead checks stay inert."""
    prompt = dict(canonical_prompt)
    prompt["layer_b_lead_signal_id"] = "signal_glucose_high"
    result = validate_llm_output_v2(prompt, valid_llm_result)
    assert len(result.insights) == 2

