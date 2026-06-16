"""
LC-S13 — Governed consumer-facing lifestyle context paragraphs (Layer C).

Plain-English only. No rationale_codes or internal bridge slugs in output.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

ALCOHOL_ONE_CARBON_LIFESTYLE_BODY_OVERVIEW_V1 = (
    "Your questionnaire suggests moderate alcohol intake, which can be relevant when "
    "interpreting homocysteine because alcohol intake may increase demand on one-carbon "
    "nutrients such as folate and B vitamins. This does not change your biomarker score, "
    "but it helps explain why this pathway is worth reviewing."
)

_FORBIDDEN_SUBSTRINGS = (
    "alcohol_intake_moderate_or_higher",
    "renal_panel_with_volume",
    "fasting_pattern_with_favourable",
    "rationale_codes",
)


def _lifestyle_artifact_from_meta(meta: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not meta or not isinstance(meta, dict):
        return {}
    exp = meta.get("explainability_report")
    if isinstance(exp, dict):
        life = exp.get("lifestyle")
        if isinstance(life, dict):
            return life
    return {}


def _smoking_paragraph(lifestyle_artifact: Mapping[str, Any]) -> str:
    validated = lifestyle_artifact.get("validated_inputs") or {}
    if not isinstance(validated, dict):
        return ""
    status = str(validated.get("smoking_status", "")).strip().lower()
    if status == "current":
        return (
            "Your questionnaire indicates current smoking, which is noted as additional "
            "context when interpreting cardiovascular and immune-related markers on this panel. "
            "This does not change your biomarker values."
        )
    if status == "former":
        return (
            "Your questionnaire indicates former smoking, which is noted as light additional "
            "context on this panel where relevant."
        )
    return ""


def _renal_paragraph(bridges: Mapping[str, Any]) -> str:
    block = bridges.get("hydration_activity_renal")
    if not isinstance(block, dict) or not block.get("active"):
        return ""
    hydration = block.get("hydration_context") or {}
    activity = block.get("activity_context") or {}
    parts: List[str] = []
    if isinstance(hydration, dict) and hydration.get("fluid_intake_low"):
        parts.append("lower reported fluid intake")
    if isinstance(activity, dict) and activity.get("high_activity_pattern"):
        parts.append("higher reported exercise frequency")
    if not parts:
        return ""
    joined = " and ".join(parts)
    return (
        f"Your questionnaire suggests {joined}, which provides context when reading "
        "kidney-related markers on this panel. This does not change your biomarker values."
    )


def _fasting_paragraph(bridges: Mapping[str, Any]) -> str:
    block = bridges.get("fasting_dietary_glycaemic")
    if not isinstance(block, dict) or not block.get("active"):
        return ""
    return (
        "Your questionnaire indicates intermittent fasting or extended overnight fasting, "
        "which is noted alongside the glycaemic markers available on this panel for context. "
        "This does not change your biomarker values."
    )


def _metabolic_modifier_paragraph(lifestyle_artifact: Mapping[str, Any]) -> str:
    mods = lifestyle_artifact.get("system_modifiers") or {}
    if not isinstance(mods, dict):
        return ""
    met = mods.get("metabolic")
    if not isinstance(met, dict):
        return ""
    capped = float(met.get("capped_total_modifier") or 0.0)
    if capped <= 0.0:
        return ""
    return (
        "Your lifestyle inputs suggest additional metabolic context on this panel "
        "(for example weight, sleep, alcohol, or smoking patterns). This helps add "
        "context when we interpret how different areas of health relate on this panel."
    )


def build_lifestyle_consumer_overview_paragraphs_v1(
    meta: Optional[Mapping[str, Any]],
) -> List[str]:
    """
    Return ordered governed paragraphs to append to consumer body_overview when active.
    """
    if not meta or not isinstance(meta, dict):
        return []
    bridges = meta.get("lifestyle_interpretation_bridges_v1")
    if not isinstance(bridges, dict):
        bridges = {}
    lifestyle_artifact = _lifestyle_artifact_from_meta(meta)

    out: List[str] = []
    if bridges.get("alcohol_methylation_macrocytosis", {}).get("active"):
        out.append(ALCOHOL_ONE_CARBON_LIFESTYLE_BODY_OVERVIEW_V1)

    renal = _renal_paragraph(bridges)
    if renal:
        out.append(renal)

    fasting = _fasting_paragraph(bridges)
    if fasting:
        out.append(fasting)

    smoking = _smoking_paragraph(lifestyle_artifact)
    if smoking:
        out.append(smoking)

    metabolic = _metabolic_modifier_paragraph(lifestyle_artifact)
    if metabolic:
        out.append(metabolic)

    for para in out:
        low = para.lower()
        for bad in _FORBIDDEN_SUBSTRINGS:
            if bad in low:
                raise ValueError(f"lifestyle consumer paragraph leaked internal token: {bad!r}")
    return out


def join_lifestyle_consumer_overview_supplement(paragraphs: List[str]) -> str:
    return "\n\n".join(p.strip() for p in paragraphs if p and p.strip())
