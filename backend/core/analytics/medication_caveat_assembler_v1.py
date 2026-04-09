"""
MEDICATION-CAVEAT-B — deterministic, bounded interpretation caveat text from questionnaire-derived
``medical_history`` only (no scoring, no drug reasoning).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# SSOT questionnaire.json labels (long_term_medications + supplements options)
_SSOT_LONG_TERM_CLASS_LABELS = frozenset(
    {"Corticosteroids", "Atypical antipsychotics", "HIV/AIDS treatments", "None"}
)
_SSOT_SUPPLEMENT_LABELS = frozenset(
    {"Multivitamin", "Vitamin D", "Omega-3/Fish Oil", "Probiotics", "Iron", "Other", "None"}
)
_QRISK_FLAG_KEYS = (
    "atrial_fibrillation",
    "rheumatoid_arthritis",
    "systemic_lupus",
    "corticosteroids",
    "atypical_antipsychotics",
    "hiv_treatments",
    "migraines",
)


def _str_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(x).strip() for x in value if str(x).strip()]


def build_medication_supplement_interpretation_caveat(
    medical_history: Optional[Dict[str, Any]],
    *,
    max_length: int = 280,
) -> Optional[str]:
    """
    Return a single bounded caveat string, or ``None`` when no qualifying self-reported context.

    Does not echo free-text supplement ``allowOther`` values — non-catalogue tokens only elevate
    a generic supplement flag.
    """
    if not medical_history:
        return None

    parts: List[str] = []

    meds = _str_list(medical_history.get("medications"))
    if any(m == "Prefer not to say" for m in meds):
        parts.append(
            "Medication exposure was declined or not fully specified; interpretation may need contextual review."
        )
    elif any(m for m in meds if m != "None"):
        parts.append(
            "Prescription medication burden is captured only as a coarse self-reported category (not specific drugs); "
            "findings may need contextual review."
        )

    lt_raw = _str_list(medical_history.get("long_term_medication_classes"))
    lt = [x for x in lt_raw if x != "None"]
    if lt:
        known = sorted({x for x in lt if x in _SSOT_LONG_TERM_CLASS_LABELS and x != "None"})
        unknown = [x for x in lt if x not in _SSOT_LONG_TERM_CLASS_LABELS]
        if known:
            parts.append(
                "Long-term medication classes reported include "
                f"{', '.join(known)}; these can affect how cardiovascular-related findings are interpreted."
            )
        if unknown:
            parts.append(
                "Additional long-term medication context was reported outside the standard class list; "
                "keep interpretation general and clinician-guided."
            )

    supp = _str_list(medical_history.get("supplements"))
    supp = [x for x in supp if x != "None"]
    if supp:
        otherish = any(x not in _SSOT_SUPPLEMENT_LABELS for x in supp) or "Other" in supp
        if otherish:
            parts.append(
                "Supplement use is reported, including non-catalogued or free-text entries; "
                "treat only as self-reported context, not product-specific advice."
            )
        else:
            parts.append(
                "Regular supplement use is reported; findings may warrant contextual review alongside self-reported supplements."
            )

    if any(bool(medical_history.get(k)) for k in _QRISK_FLAG_KEYS):
        parts.append(
            "Questionnaire flags relevant to cardiovascular risk context are present; "
            "this summary is not a substitute for clinical medication review."
        )

    if not parts:
        return None

    text = " ".join(parts)
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"
