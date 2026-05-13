"""
LC-S3 — deterministic Layer C assembly driven by NarrativePayloadV1 (governed Path B).

Translates typed Layer B fields into bounded prose. No LLM.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from core.contracts.narrative_payload_v1 import NarrativeClaimBoundaryV1, NarrativePayloadV1
from core.contracts.report_v1 import ReportTopFindingV1


_LEAD_SIGNAL_HINTS = frozenset(
    {
        "signal_homocysteine_high",
        "signal_homocysteine_elevation_context",
        "signal_mcv_high",
    }
)
_SECONDARY_SIGNAL_HINTS = frozenset(
    {
        "signal_ldl_cholesterol_high",
        "signal_hdl_cholesterol_high",
        "signal_non_hdl_high",
        "signal_lipid_transport_dysfunction",
        "signal_triglycerides_high",
    }
)


def infer_yaml_flags_from_payload(payload: NarrativePayloadV1) -> Tuple[bool, bool]:
    """Which benchmark YAML pathway blocks apply, derived only from Layer B ranking."""
    tfs = payload.top_findings
    lead = tfs[0] if tfs else None
    inc_lead = bool(lead and lead.signal_id in _LEAD_SIGNAL_HINTS)
    inc_secondary = any(tf.signal_id in _SECONDARY_SIGNAL_HINTS for tf in tfs[1:])
    return inc_lead, inc_secondary


def _humanize_metric(mid: str) -> str:
    s = str(mid or "").strip().replace("_", " ")
    return s.title() if s else "panel markers"


def _humanize_signal(token: str) -> str:
    s = str(token or "").strip().replace("signal_", "").replace("_", " ")
    return s.title() if s else "lead signal"


def _sanitize_prose(text: str, prohibited: Sequence[str]) -> str:
    """Drop paragraphs that contain prohibited substrings (case-insensitive)."""
    if not text or not prohibited:
        return text or ""
    banned = [p.strip().lower() for p in prohibited if isinstance(p, str) and p.strip()]
    if not banned:
        return text
    kept: List[str] = []
    for para in text.split("\n\n"):
        p = para.strip()
        if not p:
            continue
        low = p.lower()
        if any(b in low for b in banned):
            continue
        kept.append(p)
    return "\n\n".join(kept)


def _boundary_patterns(payload: NarrativePayloadV1) -> List[str]:
    return list(payload.claim_boundaries.prohibited_claim_patterns or [])


def _lead_matching_finding(payload: NarrativePayloadV1) -> Optional[Any]:
    lead = payload.top_findings[0] if payload.top_findings else None
    rc = payload.root_cause_v1
    if lead is None or rc is None:
        return None
    for f in rc.findings:
        if getattr(f, "signal_id", "") == lead.signal_id:
            return f
    return None


def _retail_from_payload(payload: NarrativePayloadV1, idl_retail_block: str) -> str:
    lead = payload.top_findings[0]
    head = (
        f"The ranked lead pattern is **{_humanize_signal(lead.signal_id)}** "
        f"({lead.signal_state}), centred on **{_humanize_metric(lead.primary_metric)}**. "
        "This is the priority focus for interpretation on this panel."
    )
    tail = (lead.why_it_matters or "").strip()
    hedge = (
        "This wording stays descriptive and **does not** replace clinician judgement "
        "or imply certainty beyond what the markers support."
    )
    parts = [head]
    if tail:
        parts.append(tail)
    parts.append(hedge)
    if idl_retail_block.strip():
        parts.append(idl_retail_block.strip())
    return "\n\n".join(parts)


def _root_cause_block(payload: NarrativePayloadV1) -> str:
    finding = _lead_matching_finding(payload)
    if finding is None:
        return ""
    blocks: List[str] = []
    hyps = sorted(
        list(finding.hypotheses),
        key=lambda h: float(getattr(h, "hypothesis_confidence", 0.0)),
        reverse=True,
    )
    for hyp in hyps:
        parts_h: List[str] = []
        parts_h.append(
            f"Hypothesis — **{hyp.title.strip()}**: "
            f"{hyp.summary.strip()} "
            f"(confidence weight **{hyp.hypothesis_confidence:.2f}** — structured ranking only)."
        )
        ev_ok = [str(e.item).strip() for e in hyp.evidence_for if str(e.item).strip()]
        if ev_ok:
            parts_h.append(
                "Evidence supporting this read: "
                + "; ".join(ev_ok[:8])
                + (" …" if len(ev_ok) > 8 else "")
            )
        ev_no = [str(e.item).strip() for e in hyp.evidence_against if str(e.item).strip()]
        if ev_no:
            parts_h.append(
                "Limiting factors or evidence against: "
                + "; ".join(ev_no[:8])
                + (" …" if len(ev_no) > 8 else "")
            )
        miss = [f"{m.marker_id}: {m.reason}" for m in hyp.missing_data if m.marker_id]
        if miss:
            parts_h.append("Missing data noted: " + "; ".join(miss[:6]))
        conf_tests = [
            f"{t.display_name} — {t.rationale}".strip(" —")
            for t in hyp.confirmatory_tests
            if t.display_name or t.rationale
        ]
        if conf_tests:
            parts_h.append(
                "Confirmatory tests listed for discussion with a clinician: "
                + "; ".join(conf_tests[:6])
            )
        blocks.append("\n".join(parts_h))
    if not blocks:
        return ""
    return "How the lead pattern may be explained (structured interpretation):\n\n" + "\n\n".join(blocks)


def _body_overview_payload_sentence(payload: NarrativePayloadV1) -> str:
    lead = payload.top_findings[0] if payload.top_findings else None
    if lead is None:
        return ""
    return (
        f"Lead ranked finding **{_humanize_signal(lead.signal_id)}** ({lead.signal_state}) "
        "is interpreted alongside the wider deterministic system snapshot below."
    )


def _next_steps_from_payload(
    payload: NarrativePayloadV1,
    clarification_paths_block: str,
) -> str:
    bullets: List[str] = [
        "Discuss these findings with a clinician who knows your history.",
        "Monitor trends on the cadence your clinician recommends.",
        "Repeat priority markers when your clinician advises retesting.",
        "Review lifestyle context already captured in your questionnaire — no new behavioural prescriptions are added here.",
    ]
    finding = _lead_matching_finding(payload)
    extra: List[str] = []
    if finding is not None:
        seen: set[str] = set()
        for hyp in finding.hypotheses:
            for t in hyp.confirmatory_tests:
                line = f"Consider clinician-guided follow-up on **{t.display_name.strip()}** ({t.rationale.strip()})."
                key = line.lower()
                if key not in seen:
                    seen.add(key)
                    extra.append(line)
    parts = []
    parts.extend(f"• {b}" for b in bullets)
    if extra:
        parts.append("")
        parts.extend(f"• {e}" for e in extra[:8])
    if clarification_paths_block.strip():
        parts.append("")
        parts.append(clarification_paths_block.strip())
    return "\n".join(parts)


def _clinician_header(payload: NarrativePayloadV1) -> str:
    lead = payload.top_findings[0] if payload.top_findings else None
    if lead is None:
        return ""
    lines = [
        "**Clinician fast-read — lead pattern**",
        f"- Pattern: **{_humanize_signal(lead.signal_id)}** ({lead.signal_state}); "
        f"primary marker **{_humanize_metric(lead.primary_metric)}**; "
        f"confidence score {lead.confidence:.2f}.",
        f"- Why it matters: {lead.why_it_matters.strip()}",
    ]
    reasons = [r.strip() for r in (lead.confidence_reasons or []) if isinstance(r, str) and r.strip()]
    if reasons:
        lines.append("- Confidence drivers: " + "; ".join(reasons[:6]))

    finding = _lead_matching_finding(payload)
    if finding and finding.hypotheses:
        top = max(finding.hypotheses, key=lambda h: float(h.hypothesis_confidence))
        lines.append(
            f"- Top ranked hypothesis: **{top.title.strip()}** — {top.summary}"
        )
        miss = [f"{m.marker_id}: {m.reason}" for m in top.missing_data if m.marker_id]
        if miss:
            lines.append("- Missing / limiting markers: " + "; ".join(miss[:8]))

    sup_markers = [str(m).strip() for m in (lead.supporting_markers or []) if str(m).strip()]
    if sup_markers:
            lines.append("- Supporting markers: " + ", ".join(sup_markers[:16]))

    return "\n".join(lines)


def _secondary_ranked(payload: NarrativePayloadV1) -> str:
    rest: List[ReportTopFindingV1] = list(payload.top_findings[1:])
    if not rest:
        return ""
    chunks: List[str] = []
    for tf in rest[:6]:
        chunks.append(
            f"**{_humanize_signal(tf.signal_id)}** ({tf.signal_state}) on "
            f"**{_humanize_metric(tf.primary_metric)}**: {tf.why_it_matters.strip()}"
        )
    return "Other patterns considered on this panel:\n\n" + "\n\n".join(chunks)


def _apply_boundary(text: str, boundaries: NarrativeClaimBoundaryV1) -> str:
    return _sanitize_prose(text, boundaries.prohibited_claim_patterns)


@dataclass(frozen=True)
class LcS3AssembledSections:
    retail_summary: str
    lead_narrative: str
    body_overview: str
    next_steps_narrative: str
    clinician_synthesis: str
    secondary_narratives: str


def assemble_lc_s3_sections(
    *,
    payload: NarrativePayloadV1,
    idl_retail_block: str,
    clarification_paths_block: str,
    lead_yaml_block: str,
    secondary_yaml_block: str,
    bridge_block: str,
    body_overview_for_consumer: str,
    clinician_base_without_consumer_lead: str,
    compiler_meta: Dict[str, Any],
) -> LcS3AssembledSections:
    """Compose governed prose when NarrativePayloadV1 is the primary Layer B input.

    ``body_overview_for_consumer`` is the consumer-safe structural overview (and optional
    consumer statin suffix), not the machine intervention appendix string.
    """
    compiler_meta["assets_resolved"].append("lc_s3_payload_primary_assembly")
    compiler_meta["lc_s3_assembly_version"] = "1"

    boundaries = payload.claim_boundaries

    retail_raw = _retail_from_payload(payload, idl_retail_block)
    retail_summary = _apply_boundary(retail_raw, boundaries)

    rc_block = _root_cause_block(payload)
    lead_narrative_raw = "\n\n".join(
        p for p in [lead_yaml_block.strip(), rc_block.strip(), bridge_block.strip()] if p
    )
    lead_narrative = _apply_boundary(lead_narrative_raw, boundaries)

    bo_raw = "\n\n".join(
        p
        for p in [_body_overview_payload_sentence(payload).strip(), body_overview_for_consumer.strip()]
        if p
    )
    body_overview = _apply_boundary(bo_raw, boundaries)

    ns_raw = _next_steps_from_payload(payload, clarification_paths_block)
    next_steps_narrative = _apply_boundary(ns_raw, boundaries)

    clin_raw = "\n\n".join(
        p for p in [_clinician_header(payload).strip(), clinician_base_without_consumer_lead.strip()] if p
    )
    clinician_synthesis = _apply_boundary(clin_raw, boundaries)

    secondary_raw = _secondary_ranked(payload)
    if secondary_yaml_block.strip():
        secondary_raw = "\n\n".join(
            p for p in [secondary_yaml_block.strip(), secondary_raw.strip()] if p
        )
    secondary_narratives = _apply_boundary(secondary_raw, boundaries)

    return LcS3AssembledSections(
        retail_summary=retail_summary,
        lead_narrative=lead_narrative,
        body_overview=body_overview,
        next_steps_narrative=next_steps_narrative,
        clinician_synthesis=clinician_synthesis,
        secondary_narratives=secondary_narratives,
    )
