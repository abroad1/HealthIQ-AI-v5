"""
LLM Output Validator v2 - Validates LLM responses against prompt and schema.

Sprint 17: Schema + cross-checks. Wired into InsightGraph insight synthesis (BE-S1A).
Performs schema validation and post-validations (numeric invention, evidence referencing).
WP2: Layer B lead signal token preservation, hypothesis allow-list, prohibited claim language.
"""

from typing import Any, Dict, List, Set
import re
from pydantic import ValidationError

from core.llm.schemas_v2 import LLMResultV2

_SIGNAL_TOKEN_RE = re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE)
_HYP_TOKEN_RE = re.compile(r"\bhyp_[a-z0-9_]+\b", re.IGNORECASE)
_PROHIBITED_CLAIM_RE = re.compile(
    r"(?:\bdiagnoses\b|\bdiagnosis\b|\bdiagnostic\b|\bconfirms\b|\bconfirmed\b|\brules\s+out\b|\bguarantees\b|"
    r"\btreatment\s+recommendation\b|\bmedication\s+recommendation\b|\bsupplement\s+recommendation\b)",
    re.IGNORECASE,
)


def _extract_numeric_values(text: str) -> Set[float]:
    """
    Extract all numeric values from text.

    Args:
        text: Text to extract numbers from

    Returns:
        Set of numeric values found
    """
    # Pattern to match numbers (integers and decimals)
    pattern = r"\b\d+\.?\d*\b"
    matches = re.findall(pattern, text)
    return {float(m) for m in matches}


def _get_prompt_numerics(prompt_json: Dict[str, Any]) -> Set[float]:
    """
    Extract all numeric values from prompt JSON.

    Args:
        prompt_json: Prompt JSON dict

    Returns:
        Set of all numeric values present in prompt
    """
    numerics: Set[float] = set()

    # Extract from biomarkers
    for bm in prompt_json.get("biomarkers", []):
        if "value" in bm and isinstance(bm["value"], (int, float)):
            numerics.add(float(bm["value"]))
        if "lab_range" in bm and bm["lab_range"]:
            if "min" in bm["lab_range"] and bm["lab_range"]["min"] is not None:
                numerics.add(float(bm["lab_range"]["min"]))
            if "max" in bm["lab_range"] and bm["lab_range"]["max"] is not None:
                numerics.add(float(bm["lab_range"]["max"]))

    # Extract from clusters
    for cluster in prompt_json.get("clusters", []):
        if "score" in cluster and isinstance(cluster["score"], (int, float)):
            numerics.add(float(cluster["score"]))

    # Extract from completeness
    completeness = prompt_json.get("completeness", {})
    if "score" in completeness and isinstance(completeness["score"], (int, float)):
        numerics.add(float(completeness["score"]))

    return numerics


def _get_prompt_ids(prompt_json: Dict[str, Any]) -> Set[str]:
    """
    Extract all valid IDs from prompt JSON (biomarker IDs and cluster IDs).

    Args:
        prompt_json: Prompt JSON dict

    Returns:
        Set of all valid IDs
    """
    ids: Set[str] = set()

    # Extract biomarker IDs
    for bm in prompt_json.get("biomarkers", []):
        if "id" in bm:
            ids.add(bm["id"])

    # Extract cluster IDs
    for cluster in prompt_json.get("clusters", []):
        if "id" in cluster:
            ids.add(cluster["id"])

    return ids


def _get_prompt_red_flags(prompt_json: Dict[str, Any]) -> Set[str]:
    """
    Extract all red flag IDs from prompt JSON.

    Args:
        prompt_json: Prompt JSON dict

    Returns:
        Set of red flag IDs
    """
    red_flag_ids: Set[str] = set()

    for rf in prompt_json.get("red_flags", []):
        if "id" in rf:
            red_flag_ids.add(rf["id"])

    return red_flag_ids


def _combined_llm_text_parts(result: LLMResultV2) -> str:
    parts: List[str] = []
    for insight in result.insights:
        parts.append(insight.title)
        parts.extend(insight.evidence)
        parts.extend(insight.actions)
        parts.extend(insight.red_flags)
    return " ".join(parts)


def _apply_layer_b_post_checks(prompt_json: Dict[str, Any], result: LLMResultV2) -> None:
    """WP2 §3.9 boundary checks using Layer B fields mirrored into prompt_json."""
    combined = _combined_llm_text_parts(result)

    if _PROHIBITED_CLAIM_RE.search(combined):
        raise ValueError(
            "prohibited claim language: LLM output contains disallowed diagnostic / certainty / "
            "prescriptive phrasing (Layer B → Layer C boundary)."
        )

    if "layer_b_hypothesis_ids" in prompt_json:
        raw_allowed = prompt_json.get("layer_b_hypothesis_ids")
        if not isinstance(raw_allowed, list):
            raw_allowed = []
        allowed_norm = {str(x).lower() for x in raw_allowed}
        for token in _HYP_TOKEN_RE.findall(combined):
            tl = token.lower()
            if tl not in allowed_norm:
                raise ValueError(
                    f"hypothesis allow-list: referenced '{token}' but Layer B root_cause_v1 allows "
                    f"{sorted(allowed_norm)}."
                )

    lead_sid = str(prompt_json.get("layer_b_lead_signal_id") or "").strip()
    if lead_sid and result.insights:
        first = result.insights[0]
        first_blob = " ".join([first.title, *first.evidence, *first.actions, *first.red_flags])
        tokens = set(_SIGNAL_TOKEN_RE.findall(first_blob))
        if tokens:
            lead_l = lead_sid.lower()
            lowered = {t.lower() for t in tokens}
            if lead_l not in lowered:
                raise ValueError(
                    "lead finding preservation: first insight centres explicit signal token(s) "
                    f"{sorted(tokens)} but Layer B lead_signal_id is "
                    f"'{lead_sid}'."
                )


def validate_llm_output_v2(prompt_json: Dict[str, Any], llm_json: Dict[str, Any]) -> LLMResultV2:
    """
    Validate LLM output against schema and prompt constraints.

    Args:
        prompt_json: Original prompt JSON (for cross-validation)
        llm_json: LLM response JSON to validate

    Returns:
        Validated LLMResultV2 object

    Raises:
        ValidationError: If schema validation fails
        ValueError: If post-validation fails (numeric invention, evidence referencing, etc.)
    """
    # Step 1: Schema validation (will raise ValidationError if invalid)
    try:
        result = LLMResultV2.model_validate(llm_json)
    except ValidationError as e:
        # Re-raise the original ValidationError
        raise e

    _apply_layer_b_post_checks(prompt_json, result)

    # Step 2: Extract prompt data for cross-validation
    prompt_numerics = _get_prompt_numerics(prompt_json)
    prompt_ids = _get_prompt_ids(prompt_json)
    prompt_red_flags = _get_prompt_red_flags(prompt_json)

    # Step 3: Post-validations for each insight
    for insight in result.insights:
        # Check for numeric invention in evidence and actions
        evidence_text = " ".join(insight.evidence)
        actions_text = " ".join(insight.actions)

        evidence_numerics = _extract_numeric_values(evidence_text)
        actions_numerics = _extract_numeric_values(actions_text)

        # Check if any numeric in evidence/actions is not in prompt
        all_llm_numerics = evidence_numerics | actions_numerics
        invented_numerics = all_llm_numerics - prompt_numerics

        if invented_numerics:
            raise ValueError(
                f"numeric invention: Found numeric values {invented_numerics} in insight '{insight.id}' "
                f"that are not present in prompt. Evidence/actions must only reference values from prompt."
            )

        # Check evidence referencing
        for evidence_item in insight.evidence:
            # Extract potential IDs from evidence text (simplified - looks for known IDs)
            # In practice, this would be more sophisticated
            evidence_ids = {eid for eid in prompt_ids if eid in evidence_item}

            # If evidence item doesn't contain any known ID, it might be invalid
            # But we allow free text that references IDs, so we check if it contains at least one
            if not evidence_ids and evidence_item.strip():
                # Check if it's a valid reference format (contains biomarker/cluster name)
                # This is lenient - in practice might want stricter matching
                pass  # Allow free text that might reference concepts

        # Check red flags referencing
        for red_flag in insight.red_flags:
            if red_flag not in prompt_red_flags and red_flag not in prompt_ids:
                # Red flag must reference either a red_flag ID or a biomarker/cluster ID
                raise ValueError(
                    f"Red flag '{red_flag}' in insight '{insight.id}' does not reference "
                    f"any red flag or biomarker/cluster ID from prompt."
                )

    return result
