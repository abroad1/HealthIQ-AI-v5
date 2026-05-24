"""
FE-R1 — Consumer-facing prose safety helpers.

Strips internal compiler tokens, bounds narrative length, and formats
runner-up / confidence copy for retail surfaces. No LLM.
"""

from __future__ import annotations

import re
from typing import Any, List, Mapping, Optional, Sequence

from core.contracts.narrative_payload_v1 import NarrativePayloadV1
from core.contracts.report_v1 import ReportTopFindingV1

# Substrings that must not appear in consumer retail prose (case-insensitive).
PROHIBITED_CONSUMER_SUBSTRINGS: tuple[str, ...] = (
    "(governed label)",
    "governed label",
    "moderate_by_default",
    "confidence weight",
    "structured ranking only",
    "ranked lead pattern",
    "lab anchor",
    " functional read —",
    "functional read —",
    "prioritised follow-up (governed assets)",
    "prioritised follow-up (governed asset",
    "clinician-structured",
    "lead ranked finding",
    "lead ranked",
    "this wording stays descriptive",
    "does not replace clinician judgement",
    "interpretation display layer (clinical-facing",
    "hypothesis —",
    "clarification paths:",
    " vs 0.",
    "0.90",
    "0.60",
)

RETAIL_LABEL_TEMPLATE_SUFFIX = ": is outside the optimal range on this panel"
RETAIL_LABEL_TEMPLATE_SUFFIX_ALT = "is outside the optimal range on this panel"

_MAX_RETAIL_SUMMARY_CHARS = 520
_MAX_LEAD_NARRATIVE_CHARS = 1200
_MAX_SECONDARY_NARRATIVE_CHARS = 600
_MAX_PARAGRAPHS_LEAD = 4
_MAX_PARAGRAPHS_SECONDARY = 3


def _humanize_signal(token: str) -> str:
    s = str(token or "").strip().replace("signal_", "").replace("_", " ")
    return s.title() if s else "this pattern"


def _humanize_metric(mid: str) -> str:
    s = str(mid or "").strip().replace("_", " ")
    return s.title() if s else "your markers"


def contains_prohibited_consumer_text(text: str) -> bool:
    low = (text or "").lower()
    return any(p in low for p in PROHIBITED_CONSUMER_SUBSTRINGS)


def sanitize_consumer_prose(text: str) -> str:
    """Remove paragraphs containing prohibited internal tokens."""
    if not text or not str(text).strip():
        return ""
    banned = [p.strip().lower() for p in PROHIBITED_CONSUMER_SUBSTRINGS if p.strip()]
    kept: List[str] = []
    for para in str(text).split("\n\n"):
        p = para.strip()
        if not p:
            continue
        low = p.lower()
        if any(b in low for b in banned):
            continue
        if RETAIL_LABEL_TEMPLATE_SUFFIX.lower() in low and ":" in p[:80]:
            continue
        kept.append(p)
    return "\n\n".join(kept)


def sanitize_retail_display_label(label: str) -> str:
    """Consumer-safe IDL / hero label without template suffix."""
    raw = str(label or "").strip()
    if not raw:
        return ""
    if RETAIL_LABEL_TEMPLATE_SUFFIX in raw:
        raw = raw.split(RETAIL_LABEL_TEMPLATE_SUFFIX, 1)[0].strip().rstrip(":")
    if raw.lower().endswith(RETAIL_LABEL_TEMPLATE_SUFFIX_ALT):
        raw = raw[: -len(RETAIL_LABEL_TEMPLATE_SUFFIX_ALT)].strip().rstrip(":")
    raw = re.sub(r"\s*:\s*$", "", raw)
    if not raw:
        return "Pattern on this panel"
    return raw[:120]


def bound_consumer_text(text: str, *, max_chars: int, max_paragraphs: int) -> str:
    cleaned = sanitize_consumer_prose(text)
    if not cleaned:
        return ""
    paras = [p.strip() for p in cleaned.split("\n\n") if p.strip()][:max_paragraphs]
    out = "\n\n".join(paras)
    if len(out) <= max_chars:
        return out
    truncated = out[: max_chars - 3].rsplit(" ", 1)[0]
    return truncated.rstrip() + "..."


def build_consumer_retail_summary(
    payload: NarrativePayloadV1,
    idl_retail_block: str = "",
) -> str:
    """Concise retail summary without compiler self-description."""
    if not payload.top_findings:
        base = (
            "This panel does not show one clear lead pattern. "
            "Use the sections below for how individual markers and domains fit together."
        )
        return bound_consumer_text(base, max_chars=_MAX_RETAIL_SUMMARY_CHARS, max_paragraphs=3)

    lead = payload.top_findings[0]
    signal_label = _humanize_signal(lead.signal_id)
    metric_label = _humanize_metric(lead.primary_metric)
    parts: List[str] = [
        (
            f"Your main result pattern centres on {signal_label.lower()}, "
            f"with {metric_label} as the primary marker on this panel."
        ),
        (
            "Other areas of the panel still matter, but this pattern is the best starting point "
            "for follow-up with your clinician."
        ),
    ]
    tail = (lead.why_it_matters or "").strip()
    if tail and not contains_prohibited_consumer_text(tail):
        parts.append(tail)
    # Do not append full idl_retail_block — duplicates pattern cards (FE-R0 dedup).
    return bound_consumer_text(
        "\n\n".join(parts),
        max_chars=_MAX_RETAIL_SUMMARY_CHARS,
        max_paragraphs=3,
    )


def build_consumer_lead_narrative(
    payload: NarrativePayloadV1,
    pathway_excerpt: str = "",
) -> str:
    """Bounded lead narrative: one pathway excerpt + top hypothesis only."""
    parts: List[str] = []
    if pathway_excerpt.strip():
        excerpt = bound_consumer_text(
            pathway_excerpt.strip(),
            max_chars=500,
            max_paragraphs=2,
        )
        if excerpt:
            parts.append(excerpt)

    finding = None
    lead = payload.top_findings[0] if payload.top_findings else None
    rc = payload.root_cause_v1
    if lead and rc:
        for f in rc.findings:
            if getattr(f, "signal_id", "") == lead.signal_id:
                finding = f
                break
    if finding and finding.hypotheses:
        top = max(
            finding.hypotheses,
            key=lambda h: float(getattr(h, "hypothesis_confidence", 0.0)),
        )
        hyp_parts = [f"{top.title.strip()}: {top.summary.strip()}"]
        ev_ok = [str(e.item).strip() for e in top.evidence_for if str(e.item).strip()]
        if ev_ok:
            hyp_parts.append(
                "Supporting context: " + "; ".join(ev_ok[:4]) + (" …" if len(ev_ok) > 4 else "")
            )
        parts.append("\n".join(hyp_parts))

    if not parts:
        return ""
    return bound_consumer_text(
        "\n\n".join(parts),
        max_chars=_MAX_LEAD_NARRATIVE_CHARS,
        max_paragraphs=_MAX_PARAGRAPHS_LEAD,
    )


def build_consumer_secondary_narratives(
    payload: NarrativePayloadV1,
    secondary_yaml_block: str = "",
) -> str:
    """Short secondary context without raw signal slug lists."""
    parts: List[str] = []
    if secondary_yaml_block.strip():
        brief = bound_consumer_text(
            secondary_yaml_block.strip(),
            max_chars=400,
            max_paragraphs=2,
        )
        if brief:
            parts.append(brief)

    rest: List[ReportTopFindingV1] = list(payload.top_findings[1:3])
    if rest:
        bullets: List[str] = []
        for tf in rest:
            label = _humanize_signal(tf.signal_id)
            why = (tf.why_it_matters or "").strip()
            if why and not contains_prohibited_consumer_text(why):
                bullets.append(f"{label}: {why[:200]}")
            else:
                bullets.append(
                    f"{label} also contributes context on this panel and is worth reviewing with your clinician."
                )
        if bullets:
            parts.append("Other patterns noted on this panel:\n\n" + "\n".join(f"• {b}" for b in bullets))

    if not parts:
        return ""
    return bound_consumer_text(
        "\n\n".join(parts),
        max_chars=_MAX_SECONDARY_NARRATIVE_CHARS,
        max_paragraphs=_MAX_PARAGRAPHS_SECONDARY,
    )


def build_consumer_next_steps(
    payload: NarrativePayloadV1,
    clarification_paths_block: str = "",
) -> str:
    bullets: List[str] = [
        "Discuss these findings with a clinician who knows your history.",
        "Monitor trends on the cadence your clinician recommends.",
        "Repeat priority markers when your clinician advises retesting.",
    ]
    finding = None
    lead = payload.top_findings[0] if payload.top_findings else None
    rc = payload.root_cause_v1
    if lead and rc:
        for f in rc.findings:
            if getattr(f, "signal_id", "") == lead.signal_id:
                finding = f
                break
    if finding:
        seen: set[str] = set()
        for hyp in finding.hypotheses[:2]:
            for t in hyp.confirmatory_tests[:2]:
                line = f"Consider discussing {t.display_name.strip()} with your clinician."
                key = line.lower()
                if key not in seen:
                    seen.add(key)
                    bullets.append(line)

    clar = sanitize_consumer_prose(clarification_paths_block.replace(
        "Prioritised follow-up (governed assets):", "Suggested follow-up themes:"
    ).replace("Prioritised follow-up (governed assets)", "Suggested follow-up themes"))
    parts = [f"• {b}" for b in bullets]
    if clar.strip():
        parts.append("")
        parts.append(clar.strip())
    return "\n".join(parts)


def format_runner_up_why_consumer(
    pri_label: str,
    sec_label: str,
    *,
    near_tie: bool,
) -> str:
    if near_tie:
        return (
            f"{pri_label} and {sec_label} were similarly important on this panel; "
            "we show one lead first so the story has a clear starting point."
        )
    return (
        f"{pri_label} was prioritised slightly ahead of {sec_label} on this panel. "
        "Both patterns are still worth discussing with your clinician."
    )


def format_runner_up_topic_consumer(sec_label: str, state: str) -> str:
    state_key = str(state or "").strip().lower()
    if state_key in ("suboptimal", "at_risk"):
        return f"{sec_label} also stood out on this panel and was close to the lead pattern."
    return f"{sec_label} was also considered when choosing the lead pattern."


def format_confidence_consumer(*, missing_markers: bool, near_tie: bool = False) -> str:
    parts: List[str] = []
    if near_tie:
        parts.append("Several findings were close in priority on this panel.")
    else:
        parts.append("The panel has enough information to identify a lead pattern.")
    if missing_markers:
        parts.append(
            "Some confirmatory markers were not included, which limits how specific the story can be."
        )
    return " ".join(parts)


def consumer_body_overview_opener(payload: NarrativePayloadV1) -> str:
    lead = payload.top_findings[0] if payload.top_findings else None
    if lead is None:
        return ""
    return (
        f"Your results highlight {_humanize_signal(lead.signal_id).lower()} as the main pattern "
        f"to discuss first, alongside the wider marker and domain context below."
    )


def collect_retail_prose_surfaces(dto: Mapping[str, Any]) -> List[str]:
    """Flatten narrative + IDL strings for regression scanning."""
    texts: List[str] = []
    nr = dto.get("narrative_report_v1")
    if isinstance(nr, dict):
        for key in (
            "retail_summary",
            "lead_narrative",
            "secondary_narratives",
            "next_steps_narrative",
            "body_overview",
        ):
            val = nr.get(key)
            if isinstance(val, str) and val.strip():
                texts.append(val)
    idl = dto.get("interpretation_display_layer_v1")
    if isinstance(idl, dict):
        for rec in idl.get("records") or []:
            if isinstance(rec, dict):
                lab = rec.get("retail_display_label")
                if isinstance(lab, str) and lab.strip():
                    texts.append(lab)
    cr = dto.get("clinician_report_v1")
    if isinstance(cr, dict):
        sec = (cr.get("sections") or {}).get("page1") or {}
        if isinstance(sec, dict):
            for key in (
                "runner_up_why_not_lead_line",
                "runner_up_topic_line",
                "confidence_and_missing_data",
            ):
                val = sec.get(key)
                if isinstance(val, str) and val.strip():
                    texts.append(val)
    cds = dto.get("consumer_domain_scores")
    if isinstance(cds, list):
        for row in cds:
            if isinstance(row, dict):
                for key in ("headline_sentence", "contributor_sentence", "evidence_anchor_sentence"):
                    val = row.get(key)
                    if isinstance(val, str) and val.strip():
                        texts.append(val)
    return texts
