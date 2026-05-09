"""
N-8 — Deterministic narrative report compiler v1.

Consumes governed knowledge_bus assets (N-5..N-7) and orchestrator meta; no LLM.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import yaml

from core.analytics.longitudinal_numeric_v1 import comparable_lab_delta
from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.narrative_report_v1 import NARRATIVE_REPORT_V1_VERSION, NarrativeReportV1
from core.analytics.intervention_annotation_compiler_v1 import (
    format_intervention_annotation_narrative_appendix_v1,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_ENTITIES_PATH = _REPO_ROOT / "knowledge_bus" / "interpretation_entities_v1" / "benchmark_interpretation_entities_v1.yaml"
_PATHWAY_PATH = _REPO_ROOT / "knowledge_bus" / "pathway_explainers_v1" / "pathway_explainers_v1.yaml"
_FUNCTIONAL_PATH = _REPO_ROOT / "knowledge_bus" / "functional_interpretation_v1" / "functional_interpretation_v1.yaml"

_LEAD_SIGNAL_HINTS: Set[str] = {
    "signal_homocysteine_high",
    "signal_homocysteine_elevation_context",
    "signal_mcv_high",
}
_SECONDARY_SIGNAL_HINTS: Set[str] = {
    "signal_ldl_cholesterol_high",
    "signal_hdl_cholesterol_high",
    "signal_non_hdl_high",
    "signal_lipid_transport_dysfunction",
    "signal_triglycerides_high",
}


def _load_yaml(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return raw if isinstance(raw, dict) else None


def _fired_suboptimal_signal_ids(insight_graph: Optional[Mapping[str, Any]]) -> Set[str]:
    if not insight_graph or not isinstance(insight_graph, dict):
        return set()
    out: Set[str] = set()
    for row in insight_graph.get("signal_results") or []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("signal_id", "")).strip()
        state = str(row.get("signal_state", "")).strip().lower()
        if not sid:
            continue
        if state in {"suboptimal", "at_risk"}:
            out.add(sid)
    return out


def _join_blocks(parts: Sequence[str]) -> str:
    cleaned = [p.strip() for p in parts if isinstance(p, str) and p.strip()]
    return "\n\n".join(cleaned)


def _humanize_biomarker_id(biomarker_id: str) -> str:
    s = str(biomarker_id or "").strip().replace("_", " ")
    if not s:
        return "Marker"
    return s.title()


def _rec_get(rec: Any, key: str, default: str = "") -> str:
    if rec is None:
        return default
    if isinstance(rec, dict):
        v = rec.get(key, default)
    else:
        v = getattr(rec, key, default)
    if v is None:
        return default
    return str(v)


def _rec_get_bool(rec: Any, key: str, default: bool = False) -> bool:
    if rec is None:
        return default
    if isinstance(rec, dict):
        v = rec.get(key, default)
    else:
        v = getattr(rec, key, default)
    return bool(v)


def _rec_int(rec: Any, key: str, default: int = 999) -> int:
    raw = _rec_get(rec, key, str(default))
    try:
        return int(raw)
    except ValueError:
        return default


def _idl_records(idl_bundle: Any) -> List[Any]:
    if idl_bundle is None:
        return []
    if hasattr(idl_bundle, "records"):
        recs = getattr(idl_bundle, "records", None)
        return list(recs) if isinstance(recs, list) else []
    if isinstance(idl_bundle, dict):
        recs = idl_bundle.get("records")
        return list(recs) if isinstance(recs, list) else []
    return []


def _prior_lab_map(meta: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not meta or not isinstance(meta, dict):
        return {}
    snap = meta.get("prior_biomarker_lab_snapshot_v1")
    return snap if isinstance(snap, dict) else {}


def _benchmark_domain_display_titles(
    entities_doc: Optional[Dict[str, Any]],
    domains_by_id: Dict[str, Any],
    include_lead: bool,
    include_secondary: bool,
) -> List[str]:
    titles: List[str] = []
    rows = (entities_doc or {}).get("interpretation_entities")
    if not isinstance(rows, list):
        return titles
    for row in rows:
        if not isinstance(row, dict):
            continue
        role = str(row.get("compiler_role", "")).strip()
        fdid = str(row.get("functional_interpretation_domain_id", "")).strip()
        domain = domains_by_id.get(fdid, {})
        if not domain:
            continue
        title = str(domain.get("display_title", "")).strip()
        if not title:
            continue
        if role == "benchmark_lead_domain" and include_lead:
            titles.append(title)
        elif role == "benchmark_secondary_domain" and include_secondary:
            titles.append(title)
    return titles


def _build_body_overview(
    *,
    insight_graph: Optional[Mapping[str, Any]],
    primary_driver: str,
    include_lead: bool,
    include_secondary: bool,
    entities_doc: Optional[Dict[str, Any]],
    domains_by_id: Dict[str, Any],
    compiler_meta: Dict[str, Any],
) -> str:
    parts: List[str] = []
    if primary_driver:
        parts.append(f"Primary driver system (deterministic arbitration): {primary_driver}.")
    sup_list: List[str] = []
    if insight_graph and isinstance(insight_graph, dict):
        raw_sup = insight_graph.get("supporting_systems") or []
        if isinstance(raw_sup, list):
            sup_list = sorted({str(x).strip() for x in raw_sup if str(x).strip()})
    if sup_list:
        parts.append("Co-supporting systems (deterministic arbitration): " + ", ".join(sup_list) + ".")
    calm_parts: List[str] = []
    if insight_graph and isinstance(insight_graph, dict):
        caps = insight_graph.get("system_capacity_scores") or {}
        if isinstance(caps, dict):
            calm_rows = sorted(
                (str(k), int(float(v)))
                for k, v in caps.items()
                if isinstance(v, (int, float)) and float(v) >= 90.0
            )
            if calm_rows:
                calm_parts = [f"{k} ({v})" for k, v in calm_rows]
    if calm_parts:
        parts.append(
            "High capacity / comparatively calmer systems in this snapshot (governed capacity score ≥90): "
            + ", ".join(calm_parts)
            + "."
        )
        compiler_meta["assets_resolved"].append("body_overview_capacity_context")
    themes = _benchmark_domain_display_titles(entities_doc, domains_by_id, include_lead, include_secondary)
    if themes:
        parts.append(
            "Benchmark interpretation themes (governed functional titles): " + "; ".join(themes) + "."
        )
        compiler_meta["assets_resolved"].append("body_overview_benchmark_themes")
    return _join_blocks(parts)


def _build_retail_summary(idl_bundle: Any, compiler_meta: Dict[str, Any]) -> str:
    records = _idl_records(idl_bundle)
    if not records:
        compiler_meta["skipped"].append("retail_summary_no_idl_records")
        return ""
    lines: List[str] = []
    sev_phrase = {
        "watch": "pattern to watch",
        "attention": "needs attention",
        "strong_signal": "strong signal",
    }
    for rec in sorted(records, key=lambda r: _rec_int(r, "display_order_priority", 999)):
        sev = _rec_get(rec, "severity_state", "not_observed").strip().lower()
        if sev == "not_observed":
            continue
        if not _rec_get_bool(rec, "enabled_for_frontend", False):
            continue
        if _rec_get(rec, "frontend_allowed_term", "") != "phenotype_allowed":
            continue
        label = _rec_get(rec, "retail_display_label", "").strip()
        subtitle = _rec_get(rec, "subtitle", "").strip()
        why = _rec_get(rec, "why_it_matters", "").strip()
        sphr = sev_phrase.get(sev, sev.replace("_", " "))
        head = f"{label} ({sphr})" if label else sphr.title()
        body = _join_blocks([subtitle, why])
        if body:
            lines.append(f"{head}: {body}" if head else body)
        elif head:
            lines.append(head)
    if not lines:
        compiler_meta["skipped"].append("retail_summary_no_enabled_phenotype_cards")
        return ""
    compiler_meta["assets_resolved"].append("retail_summary_from_idl")
    return _join_blocks(lines)


def _transition_sentence(human_label: str, trow: Mapping[str, Any]) -> str:
    bid = str(trow.get("biomarker_id", "")).strip()
    fs = str(trow.get("from_status", "")).strip().lower()
    ts = str(trow.get("to_status", "")).strip().lower()
    tr = str(trow.get("transition", "")).strip().lower()
    label = human_label or bid or "Marker"
    if tr == "insufficient_history":
        return f"{label}: first assessment in this series — no prior snapshot to compare."
    if tr == "stable_normal":
        return f"{label}: remained in a normal range versus the prior panel."
    if tr == "stable_abnormal":
        return f"{label}: remained outside the normal range versus the prior panel."
    if tr == "improving":
        return f"{label}: improved ({fs} → {ts}) versus the prior panel."
    if tr == "worsening":
        return f"{label}: worsened ({fs} → {ts}) versus the prior panel."
    if tr == "volatile":
        return f"{label}: showed volatile movement across recent panels."
    if tr == "unknown":
        return f"{label}: longitudinal direction unclear ({fs} → {ts})."
    return f"{label}: {tr} ({fs} → {ts})."


def _format_delta_line(biomarker_id: str, delta: Mapping[str, Any]) -> str:
    label = _humanize_biomarker_id(biomarker_id)
    p = delta["prior"]
    c = delta["current"]
    d = delta["delta"]
    u = str(delta.get("unit") or "").strip()
    u_suffix = f" {u}" if u else ""
    return (
        f"{label}: lab value prior {p:g}{u_suffix} → current {c:g}{u_suffix} "
        f"(delta {d:+.4g}{u_suffix}, same-unit comparison)."
    )


def _build_longitudinal_narrative(
    insight_graph: Optional[Mapping[str, Any]],
    meta: Optional[Mapping[str, Any]],
    compiler_meta: Dict[str, Any],
) -> str:
    if not insight_graph or not isinstance(insight_graph, dict):
        compiler_meta["skipped"].append("longitudinal_no_insight_graph")
        return ""
    transitions = insight_graph.get("state_transitions") or []
    if not isinstance(transitions, list):
        transitions = []
    t_lines: List[str] = []
    for trow in sorted(
        (r for r in transitions if isinstance(r, dict)),
        key=lambda r: str(r.get("biomarker_id", "")),
    ):
        bid = str(trow.get("biomarker_id", "")).strip()
        t_lines.append(_transition_sentence(_humanize_biomarker_id(bid), trow))

    prior_map = _prior_lab_map(meta)
    delta_lines: List[str] = []
    if prior_map:
        nodes = insight_graph.get("biomarker_nodes") or []
        if isinstance(nodes, list):
            for node in sorted(
                (n for n in nodes if isinstance(n, dict)),
                key=lambda n: str(n.get("biomarker_id", "")),
            ):
                bid = str(node.get("biomarker_id", "")).strip()
                if not bid or bid not in prior_map:
                    continue
                pr = prior_map[bid]
                if not isinstance(pr, dict):
                    continue
                delta = comparable_lab_delta(
                    pr.get("lab_value"),
                    pr.get("lab_unit"),
                    node.get("lab_value"),
                    node.get("lab_unit"),
                )
                if not delta:
                    continue
                delta_lines.append(_format_delta_line(bid, delta))
    if delta_lines:
        compiler_meta["assets_resolved"].append("longitudinal_numeric_delta")
    if t_lines:
        compiler_meta["assets_resolved"].append("longitudinal_state_transitions")
    body = _join_blocks([*t_lines, *delta_lines])
    if not body:
        compiler_meta["skipped"].append("longitudinal_empty")
    elif not t_lines and delta_lines:
        compiler_meta["skipped"].append("longitudinal_no_state_transitions")
    return body


def _clarification_paths_block(domain: Mapping[str, Any]) -> str:
    clar = domain.get("clarification_paths")
    if not isinstance(clar, list) or not clar:
        return ""
    bullets = "\n".join(f"• {c.strip()}" for c in clar if isinstance(c, str) and c.strip())
    return bullets


def _collect_next_steps(
    *,
    entities_doc: Optional[Dict[str, Any]],
    domains_by_id: Dict[str, Any],
    include_lead: bool,
    include_secondary: bool,
    compiler_meta: Dict[str, Any],
) -> str:
    blocks: List[str] = []
    rows = (entities_doc or {}).get("interpretation_entities")
    if not isinstance(rows, list):
        compiler_meta["skipped"].append("next_steps_no_interpretation_entities")
        return ""
    for row in rows:
        if not isinstance(row, dict):
            continue
        role = str(row.get("compiler_role", "")).strip()
        fdid = str(row.get("functional_interpretation_domain_id", "")).strip()
        domain = domains_by_id.get(fdid, {})
        if not domain:
            continue
        if role == "benchmark_lead_domain" and not include_lead:
            continue
        if role == "benchmark_secondary_domain" and not include_secondary:
            continue
        if role not in {"benchmark_lead_domain", "benchmark_secondary_domain"}:
            continue
        title = str(domain.get("display_title", "")).strip()
        clar = _clarification_paths_block(domain)
        if not clar:
            continue
        head = f"{title}" if title else "Follow-up"
        blocks.append(f"{head}:\n{clar}")
    if not blocks:
        compiler_meta["skipped"].append("next_steps_no_clarification_paths")
        return ""
    compiler_meta["assets_resolved"].append("next_steps_from_functional_domains")
    return "Prioritised follow-up (governed assets):\n\n" + _join_blocks(blocks)


def _clinician_functional_tail(domain: Mapping[str, Any]) -> str:
    keys = (
        "confidence_limits",
        "monitoring_improvement_signals",
        "monitoring_persistence_signals",
    )
    return _join_blocks(str(domain.get(k, "")) for k in keys if domain.get(k))


def _build_clinician_synthesis(
    *,
    idl_bundle: Any,
    entities_doc: Optional[Dict[str, Any]],
    domains_by_id: Dict[str, Any],
    include_lead: bool,
    include_secondary: bool,
    body_overview: str,
    compiler_meta: Dict[str, Any],
) -> str:
    parts: List[str] = []
    if body_overview:
        parts.append(body_overview)

    records = _idl_records(idl_bundle)
    idl_lines: List[str] = []
    for rec in sorted(records, key=lambda r: _rec_int(r, "display_order_priority", 999)):
        sev = _rec_get(rec, "severity_state", "not_observed").strip().lower()
        if sev == "not_observed":
            continue
        clin = _rec_get(rec, "clinical_display_label", "").strip()
        why = _rec_get(rec, "why_it_matters", "").strip()
        supp = _rec_get(rec, "supporting_biomarkers_summary", "").strip()
        sys_s = _rec_get(rec, "supporting_systems_summary", "").strip()
        usr = _rec_get(rec, "user_safe_description", "").strip()
        cave = _rec_get(rec, "display_caveat", "").strip()
        head = f"{clin} ({sev})" if clin else sev.title()
        chunk = _join_blocks(
            [
                why,
                f"Supporting biomarkers: {supp}." if supp else "",
                f"Supporting systems: {sys_s}." if sys_s else "",
                usr,
                f"Caveat: {cave}" if cave else "",
            ]
        )
        if chunk:
            idl_lines.append(f"{head}\n{chunk}")
    if idl_lines:
        parts.append("Interpretation display layer (clinical-facing excerpts):\n\n" + _join_blocks(idl_lines))
        compiler_meta["assets_resolved"].append("clinician_synthesis_idl")

    dom_tails: List[str] = []
    rows = (entities_doc or {}).get("interpretation_entities")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            role = str(row.get("compiler_role", "")).strip()
            fdid = str(row.get("functional_interpretation_domain_id", "")).strip()
            domain = domains_by_id.get(fdid, {})
            if not domain:
                continue
            if role == "benchmark_lead_domain" and include_lead:
                pass
            elif role == "benchmark_secondary_domain" and include_secondary:
                pass
            else:
                continue
            title = str(domain.get("display_title", "")).strip()
            tail = _clinician_functional_tail(domain)
            if tail:
                dom_tails.append(f"{title}:\n{tail}" if title else tail)
    if dom_tails:
        parts.append(
            "Functional interpretation — limits and monitoring (governed):\n\n" + _join_blocks(dom_tails)
        )
        compiler_meta["assets_resolved"].append("clinician_synthesis_functional")

    out = _join_blocks(parts)
    if not out:
        compiler_meta["skipped"].append("clinician_synthesis_empty")
    return out


def _pathway_section(pathway: Mapping[str, Any]) -> str:
    keys = (
        "pathway_role",
        "system_in_action",
        "homocysteine_in_this_pathway",
        "remethylation_and_transsulfuration",
        "red_blood_cell_maturation_link",
        "lipid_particles_as_transport_architecture",
        "apob_triglycerides_hdl_ldl_together",
        "beyond_a_single_ldl_value",
    )
    return _join_blocks(str(pathway.get(k, "")) for k in keys if pathway.get(k))


def _functional_section(domain: Mapping[str, Any]) -> str:
    keys = (
        "functional_reading",
        "why_beyond_itself",
        "confidence_grade_label",
        "confidence_supports_reading",
        "confidence_limits",
        "monitoring_improvement_signals",
        "monitoring_persistence_signals",
    )
    parts: List[str] = []
    for k in keys:
        if k == "confidence_grade_label":
            label = domain.get("confidence_grade_label")
            if label:
                parts.append(f"Confidence framing (governed label): {label}")
            continue
        v = domain.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
    clar = domain.get("clarification_paths")
    if isinstance(clar, list) and clar:
        bullets = "\n".join(f"• {c}" for c in clar if isinstance(c, str) and c.strip())
        if bullets:
            parts.append("Clarification paths:\n" + bullets)
    return _join_blocks(parts)


def _bridge_lines(meta: Optional[Mapping[str, Any]]) -> List[str]:
    if not meta or not isinstance(meta, dict):
        return []
    bridges = meta.get("lifestyle_interpretation_bridges_v1")
    if not isinstance(bridges, dict):
        return []
    lines: List[str] = []
    for key, title in (
        ("alcohol_methylation_macrocytosis", "Lifestyle bridge — one-carbon / alcohol context"),
        ("hydration_activity_renal", "Lifestyle bridge — hydration / activity renal context"),
        ("fasting_dietary_glycaemic", "Lifestyle bridge — fasting / glycaemic context"),
    ):
        block = bridges.get(key)
        if not isinstance(block, dict):
            continue
        if not block.get("active"):
            continue
        codes = block.get("rationale_codes") or []
        code_str = ", ".join(str(c) for c in codes if c)
        lines.append(f"{title}: active ({code_str}).".strip())
    return lines


def compile_narrative_report_v1(
    *,
    analysis_id: str,
    meta: Optional[Mapping[str, Any]] = None,
    insight_graph: Optional[Mapping[str, Any]] = None,
    idl_bundle: Any = None,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None,
) -> NarrativeReportV1:
    """
    Compile a bounded v1 narrative report from governed assets and enriched graph/meta.

    Missing assets or failed lookups yield empty sections and recorded skips in meta (no raise).
    """
    compiler_meta: Dict[str, Any] = {
        "compiler_version": NARRATIVE_REPORT_V1_VERSION,
        "analysis_id": analysis_id,
        "assets_resolved": [],
        "skipped": [],
    }

    entities_doc = _load_yaml(_ENTITIES_PATH)
    pathway_doc = _load_yaml(_PATHWAY_PATH)
    functional_doc = _load_yaml(_FUNCTIONAL_PATH)

    if entities_doc is None:
        compiler_meta["skipped"].append("missing_benchmark_interpretation_entities")
    if pathway_doc is None:
        compiler_meta["skipped"].append("missing_pathway_explainers")
    if functional_doc is None:
        compiler_meta["skipped"].append("missing_functional_interpretation")

    pathways_by_id = {
        str(p.get("pathway_id", "")).strip(): p
        for p in (pathway_doc or {}).get("pathways", [])
        if isinstance(p, dict) and str(p.get("pathway_id", "")).strip()
    }
    domains_by_id = {
        str(d.get("domain_id", "")).strip(): d
        for d in (functional_doc or {}).get("domains", [])
        if isinstance(d, dict) and str(d.get("domain_id", "")).strip()
    }

    fired = _fired_suboptimal_signal_ids(insight_graph)
    include_lead = bool(fired & _LEAD_SIGNAL_HINTS)
    include_secondary = bool(fired & _SECONDARY_SIGNAL_HINTS)

    lead_text = ""
    secondary_text = ""

    rows = (entities_doc or {}).get("interpretation_entities")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            role = str(row.get("compiler_role", "")).strip()
            peid = str(row.get("pathway_explainer_id", "")).strip()
            fdid = str(row.get("functional_interpretation_domain_id", "")).strip()
            pathway = pathways_by_id.get(peid, {})
            domain = domains_by_id.get(fdid, {})
            block = _join_blocks(
                [
                    _pathway_section(pathway) if pathway else "",
                    _functional_section(domain) if domain else "",
                ]
            )
            if role == "benchmark_lead_domain" and include_lead:
                lead_text = block
                compiler_meta["assets_resolved"].append("lead_domain_composed")
            elif role == "benchmark_secondary_domain" and include_secondary:
                secondary_text = block
                compiler_meta["assets_resolved"].append("secondary_domain_composed")

    bridge_block = _join_blocks(_bridge_lines(meta))
    if bridge_block:
        compiler_meta["lifestyle_bridge_lines"] = bridge_block
        if lead_text:
            lead_text = _join_blocks([lead_text, bridge_block])
            compiler_meta["assets_resolved"].append("lifestyle_bridges_appended_to_lead")
        elif secondary_text:
            secondary_text = _join_blocks([secondary_text, bridge_block])
            compiler_meta["assets_resolved"].append("lifestyle_bridges_appended_to_secondary")
        else:
            lead_text = bridge_block
            compiler_meta["assets_resolved"].append("lifestyle_bridges_only")

    primary_driver = ""
    if insight_graph and isinstance(insight_graph, dict):
        primary_driver = str(insight_graph.get("primary_driver_system_id", "") or "").strip()

    body_overview = _build_body_overview(
        insight_graph=insight_graph,
        primary_driver=primary_driver,
        include_lead=include_lead,
        include_secondary=include_secondary,
        entities_doc=entities_doc,
        domains_by_id=domains_by_id,
        compiler_meta=compiler_meta,
    )
    ia_appendix = format_intervention_annotation_narrative_appendix_v1(intervention_annotations_v1)
    if ia_appendix:
        body_overview = _join_blocks([body_overview, ia_appendix])
        compiler_meta["assets_resolved"].append("intervention_annotation_appendix_lc_s2")

    if not include_lead:
        compiler_meta["skipped"].append("lead_narrative_no_matching_signals")
    if not include_secondary:
        compiler_meta["skipped"].append("secondary_narratives_no_matching_signals")

    if idl_bundle is not None:
        compiler_meta["idl_bundle_present"] = True

    retail_summary = _build_retail_summary(idl_bundle, compiler_meta)
    longitudinal_narrative = _build_longitudinal_narrative(insight_graph, meta, compiler_meta)
    next_steps_narrative = _collect_next_steps(
        entities_doc=entities_doc,
        domains_by_id=domains_by_id,
        include_lead=include_lead,
        include_secondary=include_secondary,
        compiler_meta=compiler_meta,
    )
    clinician_synthesis = _build_clinician_synthesis(
        idl_bundle=idl_bundle,
        entities_doc=entities_doc,
        domains_by_id=domains_by_id,
        include_lead=include_lead,
        include_secondary=include_secondary,
        body_overview=body_overview,
        compiler_meta=compiler_meta,
    )

    return NarrativeReportV1(
        retail_summary=retail_summary,
        lead_narrative=lead_text,
        secondary_narratives=secondary_text,
        body_overview=body_overview,
        longitudinal_narrative=longitudinal_narrative,
        next_steps_narrative=next_steps_narrative,
        clinician_synthesis=clinician_synthesis,
        meta=compiler_meta,
    )
