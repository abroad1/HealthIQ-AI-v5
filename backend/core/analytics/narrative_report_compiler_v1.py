"""
N-8 — Deterministic narrative report compiler v1.

Consumes governed knowledge_bus assets (N-5..N-7) and orchestrator meta; no LLM.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import yaml

from core.contracts.narrative_report_v1 import NARRATIVE_REPORT_V1_VERSION, NarrativeReportV1

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

    body_overview = ""
    if primary_driver:
        body_overview = f"Primary driver system (deterministic arbitration): {primary_driver}."

    if not include_lead:
        compiler_meta["skipped"].append("lead_narrative_no_matching_signals")
    if not include_secondary:
        compiler_meta["skipped"].append("secondary_narratives_no_matching_signals")

    if idl_bundle is not None:
        compiler_meta["idl_bundle_present"] = True

    return NarrativeReportV1(
        lead_narrative=lead_text,
        secondary_narratives=secondary_text,
        body_overview=body_overview,
        meta=compiler_meta,
    )
