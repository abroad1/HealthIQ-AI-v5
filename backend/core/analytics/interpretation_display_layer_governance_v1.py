"""
BE-IDL-1 — IDL governance checks (deterministic validation for tests and CI).
"""

from __future__ import annotations

import re
from typing import List, Set

from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayLayerBundleV1

SCIENTIFIC_CLASSES: Set[str] = {"phenotype", "risk_construct", "organ_pattern", "syndrome_state"}
FRONTEND_TERM_ALLOWED: Set[str] = {"phenotype_allowed", "clinical_only"}
SEVERITY_STATES: Set[str] = {"not_observed", "watch", "attention", "strong_signal"}

# Banned generic product buckets (Section 5 must not collapse to undifferentiated labels).
BANNED_RETAIL_LABELS = frozenset(
    {
        "Metabolic Health",
        "General Health",
        "General Wellness",
        "Your Health",
        "Overall Health",
        "Health Summary",
    }
)


def validate_interpretation_display_layer_bundle_v1(
    bundle: InterpretationDisplayLayerBundleV1,
) -> List[str]:
    """
    Return a list of governance violation messages (empty if valid).
    """
    errors: List[str] = []
    priorities: List[int] = []
    seen_ids: Set[str] = set()

    for rec in bundle.records:
        if rec.internal_id in seen_ids:
            errors.append(f"duplicate internal_id: {rec.internal_id}")
        seen_ids.add(rec.internal_id)

        if not rec.internal_id.startswith("ph_"):
            errors.append(f"internal_id must use ph_ prefix: {rec.internal_id}")

        if rec.scientific_class not in SCIENTIFIC_CLASSES:
            errors.append(f"invalid scientific_class for {rec.internal_id}: {rec.scientific_class}")

        if rec.frontend_allowed_term not in FRONTEND_TERM_ALLOWED:
            errors.append(f"invalid frontend_allowed_term for {rec.internal_id}")

        if rec.severity_state not in SEVERITY_STATES:
            errors.append(f"invalid severity_state for {rec.internal_id}: {rec.severity_state}")

        for field_name in (
            "clinical_display_label",
            "retail_display_label",
            "subtitle",
            "why_it_matters",
            "supporting_biomarkers_summary",
        ):
            val = getattr(rec, field_name, "") or ""
            if not str(val).strip():
                errors.append(f"empty {field_name} for {rec.internal_id}")

        retail = (rec.retail_display_label or "").strip()
        if retail in BANNED_RETAIL_LABELS:
            errors.append(f"banned generic retail_display_label for {rec.internal_id}: {retail!r}")

        if rec.frontend_allowed_term == "clinical_only":
            if re.search(r"phenotype", rec.retail_display_label or "", flags=re.IGNORECASE):
                errors.append(
                    f"retail label must not contain 'phenotype' when clinical_only: {rec.internal_id}"
                )

        priorities.append(rec.display_order_priority)

    if len(priorities) != len(set(priorities)):
        errors.append("display_order_priority values must be unique across records")

    if priorities and (min(priorities) < 1 or max(priorities) > 999):
        errors.append("display_order_priority out of allowed range 1–999")

    return errors
