"""
ARCH-CONV-E2 — governed ALT R-value hypothesis selection (no raw Pass 3 runtime read).

Selects among the two ranked hypotheses of
``inv_alt_high_r_value_hepatocellular_biochemical_pattern``:

- rank 1: ``hyp_alt_predominant_biochemical_pattern`` when R >= 5
- rank 2: ``hyp_alt_high_general_liver_test_abnormality_context`` when ALT is high
  but R-value classification is unavailable/ineligible, or when R <= 2 while the
  cholestatic R-value package remains withheld

When ``2 < R < 5``, returns None so the mixed package owns the pattern and the
hepatocellular general fallback is not duplicated.
"""

from __future__ import annotations

from typing import Optional

from core.analytics.ratio_registry import (
    R_VALUE_CHOLESTATIC_MAX,
    R_VALUE_HEPATOCELLULAR_MIN,
    R_VALUE_MIXED_EXCLUSIVE_LOWER,
    R_VALUE_MIXED_EXCLUSIVE_UPPER,
)

HEPATOCELLULAR_ACTIVATION_KEY = (
    "signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern"
)
MIXED_ACTIVATION_KEY = (
    "signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern"
)

HYP_ALT_PREDOMINANT_BIOCHEMICAL_PATTERN = "hyp_alt_predominant_biochemical_pattern"
HYP_ALT_HIGH_GENERAL_LIVER_TEST_ABNORMALITY_CONTEXT = (
    "hyp_alt_high_general_liver_test_abnormality_context"
)


def select_hepatocellular_hypothesis_id(r_value: Optional[float]) -> Optional[str]:
    """
    Return the hypothesis id for the canonical hepatocellular package, or None to
    suppress emission when the mixed R-value band owns the pattern.
    """
    if r_value is None:
        return HYP_ALT_HIGH_GENERAL_LIVER_TEST_ABNORMALITY_CONTEXT
    value = float(r_value)
    if value >= R_VALUE_HEPATOCELLULAR_MIN:
        return HYP_ALT_PREDOMINANT_BIOCHEMICAL_PATTERN
    if (
        value > R_VALUE_MIXED_EXCLUSIVE_LOWER
        and value < R_VALUE_MIXED_EXCLUSIVE_UPPER
    ):
        return None
    if value <= R_VALUE_CHOLESTATIC_MAX:
        return HYP_ALT_HIGH_GENERAL_LIVER_TEST_ABNORMALITY_CONTEXT
    return HYP_ALT_HIGH_GENERAL_LIVER_TEST_ABNORMALITY_CONTEXT
