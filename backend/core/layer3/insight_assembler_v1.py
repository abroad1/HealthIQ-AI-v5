"""
Sprint 22 — Layer 3 Insight Assembler v1. Deterministic, rule-based.

Converts Layer 1+2 analysis output into stable user-facing insight artifact.
No LLM. No timestamps. No UUIDs. Deterministic IDs and ordering only.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple

from core.analytics.system_burden_engine import load_burden_registry
from core.contracts.layer3_insights_v1 import (
    EvidenceBlock,
    EvidenceLifestyle,
    EvidenceSystemBurden,
    InsightCard,
    Layer3InsightsV1,
)

if TYPE_CHECKING:
    from core.models.results import AnalysisDTO

SEVERITY_ORDER: Tuple[Literal["action"], Literal["watch"], Literal["info"]] = (
    "action",
    "watch",
    "info",
)

BURDEN_ACTION = 0.66
BURDEN_WATCH = 0.33


def _burden_to_severity(burden: float) -> Literal["action", "watch", "info"]:
    if burden >= BURDEN_ACTION:
        return "action"
    if burden >= BURDEN_WATCH:
        return "watch"
    return "info"


def _burden_to_band(burden: float) -> str:
    if burden >= BURDEN_ACTION:
        return "elevated"
    if burden >= BURDEN_WATCH:
        return "moderate"
    return "optimal"


def _severity_rank(s: str) -> int:
    return {"action": 0, "watch": 1, "info": 2}.get(s, 3)


def _get_adjusted_burdens(dto: "AnalysisDTO") -> Dict[str, float]:
    """Extract adjusted system burden vector. STOP if not present."""
    meta = dto.meta or {}
    burden_vector = meta.get("burden_vector") or {}
    adjusted = burden_vector.get("adjusted_system_burden_vector")
    if adjusted is None:
        raise ValueError(
            "DTO does not expose adjusted_system_burden_vector in meta.burden_vector"
        )
    return dict(adjusted)


def _confidence_from_penalty(penalty: float) -> Literal["high", "medium", "low"]:
    if penalty >= 0.15:
        return "low"
    if penalty >= 0.10:
        return "medium"
    return "high"


def _has_missing_ref_range(biomarker: Dict[str, Any]) -> bool:
    ref = biomarker.get("reference_range") or {}
    return ref.get("min") is None or ref.get("max") is None


def _build_evidence_block(
    dto: "AnalysisDTO",
    system_id: str,
    lifestyle_modifiers: Optional[Dict[str, Any]],
) -> Tuple[EvidenceBlock, bool]:
    """
    Build evidence block for a system card.
    Returns (block, has_missing_ref_in_evidence) for per-card confidence capping.
    Cap applies only if this card's evidence includes biomarkers with missing ref; otherwise False.
    Includes: system burdens (base+adjusted), lifestyle top 1-3 modifiers if present.
    """
    meta = dto.meta or {}
    burden_vector = meta.get("burden_vector") or {}
    adjusted = burden_vector.get("adjusted_system_burden_vector") or {}
    adj_burden = float(adjusted.get(system_id, 0.0))
    mod_data = (
        (lifestyle_modifiers or {})
        .get("system_modifiers", {})
        .get(system_id)
    )

    base_burden = adj_burden
    if mod_data:
        mod_val = float(mod_data.get("capped_total_modifier", 0) or 0)
        base_burden = max(0.0, adj_burden - mod_val)

    system_burdens: List[EvidenceSystemBurden] = [
        EvidenceSystemBurden(
            system_id=system_id,
            base_burden=round(base_burden, 4),
            adjusted_burden=round(adj_burden, 4),
        )
    ]

    lifestyle_entries: List[EvidenceLifestyle] = []
    if mod_data:
        contributions = mod_data.get("contributions", [])
        if contributions:
            sorted_contrib = sorted(
                contributions,
                key=lambda c: (-abs(float(c.get("capped_modifier", 0) or 0)), c.get("input", "")),
            )
            for c in sorted_contrib[:3]:
                lifestyle_entries.append(
                    EvidenceLifestyle(
                        input_name=str(c.get("input", "")),
                        modifier=round(float(c.get("modifier", 0) or 0), 4),
                        capped_modifier=round(float(c.get("capped_modifier", 0) or 0), 4),
                    )
                )

    evidence_dict: Dict[str, Any] = {"system_burdens": system_burdens}
    if lifestyle_entries:
        evidence_dict["lifestyle"] = lifestyle_entries

    block = EvidenceBlock(**evidence_dict)
    has_missing_ref = False
    biomarkers_in_evidence = block.biomarkers or []
    for b in biomarkers_in_evidence:
        ref_min = getattr(b, "reference_min", None)
        ref_max = getattr(b, "reference_max", None)
        if ref_min is None or ref_max is None:
            has_missing_ref = True
            break
    return block, has_missing_ref


def _ssot_supported_system_ids(adjusted: Dict[str, float]) -> frozenset[str]:
    """Supported = (SSOT canonical systems) ∩ (burden vector keys)."""
    registry = load_burden_registry()
    ssot_system_ids = frozenset(
        str(r.get("system", "")).strip()
        for r in registry.values()
        if isinstance(r, dict) and str(r.get("system", "")).strip()
    )
    vector_system_ids = frozenset(adjusted.keys())
    return ssot_system_ids & vector_system_ids


def assemble_layer3_insights(dto: "AnalysisDTO") -> Layer3InsightsV1:
    """
    Assemble Layer 3 insights from analysis DTO.
    Emits cards ONLY for SSOT-supported systems (system_burden_registry ∩ burden vector keys).
    No fabricated zero-burden cards for unsupported systems (e.g. autonomic, musculoskeletal).
    Deterministic: no datetime, no UUIDs, no random, no file I/O.
    """
    adjusted = _get_adjusted_burdens(dto)
    supported_system_ids = _ssot_supported_system_ids(adjusted)
    lifestyle = dto.lifestyle
    lifestyle_modifiers = lifestyle if isinstance(lifestyle, dict) else None

    cards: List[InsightCard] = []
    for system_id in sorted(supported_system_ids):
        insight_id = f"{system_id}__system_pressure"
        burden = adjusted[system_id]
        severity = _burden_to_severity(burden)
        band = _burden_to_band(burden)

        title = f"{system_id.replace('_', ' ').title()} system pressure"
        interpretation = (
            f"Your {system_id.replace('_', ' ')} signals are in the {band} range based on this panel."
        )

        mods = (lifestyle_modifiers or {}).get("system_modifiers", {}).get(system_id, {})
        lifestyle_contributed = bool(
            mods and float(mods.get("capped_total_modifier", 0) or 0) > 0
        )
        confidence_penalty = float(mods.get("confidence_penalty", 0) or 0) if mods else 0.0

        if lifestyle_contributed:
            interpretation += " Lifestyle factors contributed to this signal."

        confidence = _confidence_from_penalty(confidence_penalty)
        evidence_block, has_missing_ref = _build_evidence_block(
            dto, system_id, lifestyle_modifiers
        )
        if has_missing_ref and confidence == "high":
            confidence = "medium"

        # exclude_none removes None but not empty lists; filter empty lists and reconstruct to satisfy contract (omit empty sections)
        evidence_d = evidence_block.model_dump(exclude_none=True)
        filtered_evidence: Dict[str, Any] = {}
        for k, v in evidence_d.items():
            if v is not None and (not isinstance(v, list) or v):
                filtered_evidence[k] = v
        evidence_final = (
            EvidenceBlock(**filtered_evidence) if filtered_evidence else EvidenceBlock()
        )

        cards.append(
            InsightCard(
                insight_id=insight_id,
                system_id=system_id,
                title=title,
                severity=severity,
                confidence=confidence,
                evidence=evidence_final,
                interpretation=interpretation,
                next_steps=[],
                flags=None,
            )
        )

    cards.sort(
        key=lambda c: (
            _severity_rank(c.severity),
            c.system_id,
            c.insight_id,
        )
    )

    return Layer3InsightsV1(
        schema_version="1.0.0",
        insights=cards,
        summary=None,
    )
