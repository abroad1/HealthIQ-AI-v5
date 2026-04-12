"""
BE-W2-RQ3 — Bounded balanced-systems narrative from existing deterministic contracts only.

Derives user-facing copy from:
- meta.insight_graph.system_states (system_stable_normal)
- meta.burden_vector.system_capacity_scores and/or explainability_report.system_burden.system_capacity_scores
- meta.explainability_report.dominance_resolution.influence_ordering.supporting_systems (humanized ids only)

Does not read arbitration traces, tie-breakers, replay stamps, or raw debug payloads.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


def _canonical_system_id(raw: str) -> str:
    """Align with cluster_id → burden system id (orchestrator-style), for primary-driver comparison."""
    cid = str(raw or "").strip()
    m = re.fullmatch(r"(.+)_(\d+)_biomarkers", cid)
    if m:
        return str(m.group(1)).strip()
    return cid


def _humanize_system_label(system_id: str) -> str:
    s = str(system_id or "").strip()
    m = re.fullmatch(r"(.+)_(\d+)_biomarkers", s)
    if m:
        s = m.group(1)
    s = s.replace("-", "_")
    parts = [p for p in s.split("_") if p]
    if not parts:
        return "This system"
    return " ".join((w[:1].upper() + w[1:].lower()) if w else "" for w in parts)


def _capacity_scores_map(meta: Dict[str, Any]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    bv = meta.get("burden_vector")
    if isinstance(bv, dict):
        raw = bv.get("system_capacity_scores")
        if isinstance(raw, dict):
            for k, v in raw.items():
                sid = str(k).strip()
                if not sid:
                    continue
                try:
                    out[sid] = int(v)
                except (TypeError, ValueError):
                    continue
    if out:
        return out
    exp = meta.get("explainability_report")
    if isinstance(exp, dict):
        sb = exp.get("system_burden")
        if isinstance(sb, dict):
            raw = sb.get("system_capacity_scores")
            if isinstance(raw, dict):
                for k, v in raw.items():
                    sid = str(k).strip()
                    if not sid:
                        continue
                    try:
                        out[sid] = int(v)
                    except (TypeError, ValueError):
                        continue
    return out


def _supporting_systems_list(meta: Dict[str, Any]) -> List[str]:
    exp = meta.get("explainability_report")
    if not isinstance(exp, dict):
        return []
    dom = exp.get("dominance_resolution")
    if not isinstance(dom, dict):
        return []
    inf = dom.get("influence_ordering")
    if not isinstance(inf, dict):
        return []
    sup = inf.get("supporting_systems")
    if not isinstance(sup, list):
        return []
    return sorted({str(x).strip() for x in sup if str(x).strip()})


def compile_balanced_systems_v1(
    *,
    meta: Dict[str, Any],
    primary_driver_system_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Returns a bounded dict for API/FE, or None when no stable systems to surface.
    """
    ig = meta.get("insight_graph")
    if not isinstance(ig, dict):
        return None
    states = ig.get("system_states")
    if not isinstance(states, list):
        return None

    stable_rows: List[Dict[str, Any]] = []
    for node in states:
        if not isinstance(node, dict):
            continue
        sid = str(node.get("system_id", "")).strip()
        if not sid:
            continue
        codes = node.get("state_codes")
        if not isinstance(codes, list):
            continue
        if "system_stable_normal" not in codes:
            continue
        if primary_driver_system_id and _canonical_system_id(sid) == _canonical_system_id(
            primary_driver_system_id
        ):
            # Avoid suggesting the primary-driver system is "reassuring" in this block when it is the headline driver.
            continue
        bucket = str(node.get("confidence_bucket", "moderate") or "moderate").strip().lower()
        if bucket not in ("high", "moderate", "low", "insufficient"):
            bucket = "moderate"
        stable_rows.append(
            {
                "system_id": sid,
                "confidence_bucket": bucket,
            }
        )

    stable_rows = sorted(stable_rows, key=lambda r: r["system_id"])
    if not stable_rows:
        return None

    capacities = _capacity_scores_map(meta)
    supporting = set(_supporting_systems_list(meta))
    primary = str(primary_driver_system_id or "").strip()

    items: List[Dict[str, str]] = []
    for row in stable_rows[:4]:
        sid = row["system_id"]
        topic = _humanize_system_label(sid)
        bucket = row["confidence_bucket"]
        evidence_line = (
            f"On this panel, markers grouped under this system look broadly within expected ranges "
            f"(interpretation confidence for this read: {bucket})."
        )
        cap_note = ""
        if sid in capacities:
            cap = capacities[sid]
            cap_clamped = max(0, min(100, cap))
            cap_note = f"Modelled system capacity headroom for this group: {cap_clamped} (0–100 scale)."
        extra = ""
        if sid in supporting:
            extra = " This system also appears among the supporting systems in the cross-system model."
        items.append(
            {
                "system_topic": topic[:160],
                "evidence_line": (evidence_line + extra)[:420],
                "capacity_note": cap_note[:220],
            }
        )

    intro = (
        "Not every system group shows strain on this panel. The patterns below look broadly stable or "
        "well-regulated, based on the same structured engine that flags concerns."
    )

    stable_topics = [it["system_topic"] for it in items]
    context_parts: List[str] = []
    if primary:
        context_parts.append(
            f"The headline interpretation above focuses on {_humanize_system_label(primary)}. "
            f"Several other groups still look broadly in-range—this helps place concerns in context rather than "
            f"suggesting the whole panel is off track."
        )
    else:
        context_parts.append(
            "Several system groups look broadly in-range on this test, which helps balance the overall story."
        )
    if len(stable_topics) >= 2:
        joined = ", ".join(stable_topics[:3])
        if len(stable_topics) > 3:
            joined += ", and others"
        context_parts.append(f"Groups with reassuring patterns here include: {joined}.")

    context_line = " ".join(context_parts)[:520]

    return {
        "intro_line": intro[:360],
        "items": items,
        "context_line": context_line,
    }
