"""
Extracts a structured per-run verification record from each
analysis_result.json under docs/audit-papers/verification-2026-05-04/artifacts/.

Produces:
- ledger_extract.json   (one record per panel x profile)
- ledger_diff.json      (per-panel: what changes across profiles)
- ledger_summary.md     (compact human-readable matrix)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = REPO_ROOT / "docs" / "audit-papers" / "verification-2026-05-04"
ART = OUT_ROOT / "artifacts"

PANEL_ORDER = [
    "AB_full_panel_with_ranges",
    "VR_full_panel_with_ranges",
    "AB_full_panel_with_profiles",
]
PROFILE_ORDER = ["P0_no_lifestyle", "P1_healthy", "P2_minimal_existing_fixture", "P3_stressed"]


def _safe(obj: Any, *path: str, default: Any = None) -> Any:
    cur = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def _summarise_root_cause(findings: List[dict]) -> Dict[str, Any]:
    if not isinstance(findings, list):
        return {"finding_count": 0, "with_governed_hypotheses": 0, "fallback_count": 0, "items": []}
    fallback_marker = "No hypothesis set available"
    items: List[Dict[str, Any]] = []
    governed = 0
    fallback = 0
    for f in findings:
        if not isinstance(f, dict):
            continue
        signal_id = f.get("signal_id")
        hyps = f.get("hypotheses") or []
        hyp_count = len(hyps) if isinstance(hyps, list) else 0
        gov_for_this = 0
        fb_for_this = 0
        ev_for = 0
        ev_against = 0
        miss = 0
        titles: List[str] = []
        for h in hyps if isinstance(hyps, list) else []:
            if not isinstance(h, dict):
                continue
            title = str(h.get("title") or h.get("hypothesis_id") or "")
            titles.append(title)
            summ = str(h.get("summary") or "")
            if fallback_marker in summ or fallback_marker in title:
                fb_for_this += 1
            else:
                gov_for_this += 1
            ev_for += len(h.get("evidence_for") or [])
            ev_against += len(h.get("evidence_against") or [])
            miss += len(h.get("missing_data") or [])
        governed += gov_for_this
        fallback += fb_for_this
        items.append(
            {
                "signal_id": signal_id,
                "signal_state": f.get("signal_state"),
                "signal_confidence": f.get("signal_confidence"),
                "primary_metric": f.get("primary_metric"),
                "hypothesis_count": hyp_count,
                "governed_hypotheses": gov_for_this,
                "fallback_hypotheses": fb_for_this,
                "evidence_for_total": ev_for,
                "evidence_against_total": ev_against,
                "missing_data_total": miss,
                "hypothesis_titles": titles,
            }
        )
    return {
        "finding_count": len(items),
        "governed_hypothesis_count": governed,
        "fallback_hypothesis_count": fallback,
        "items": items,
    }


def _summarise_top_findings(items: List[dict]) -> Dict[str, Any]:
    if not isinstance(items, list):
        return {"count": 0, "ranked": []}
    ranked: List[Dict[str, Any]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        ranked.append(
            {
                "rank": it.get("priority_rank"),
                "signal_id": it.get("signal_id"),
                "signal_state": it.get("signal_state"),
                "system": it.get("system"),
                "primary_metric": it.get("primary_metric"),
                "confidence": it.get("confidence"),
                "supporting_markers": it.get("supporting_markers"),
                "why_it_matters": it.get("why_it_matters"),
            }
        )
    ranked.sort(key=lambda r: (r.get("rank") or 999))
    return {"count": len(ranked), "ranked": ranked}


def _summarise_idl(idl: dict) -> Dict[str, Any]:
    if not isinstance(idl, dict):
        return {"present": False, "record_count": 0, "enabled_count": 0, "enabled": []}
    records = idl.get("records") or []
    enabled = []
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("enabled_for_frontend"):
                enabled.append(
                    {
                        "internal_id": r.get("internal_id"),
                        "scientific_class": r.get("scientific_class"),
                        "retail_display_label": r.get("retail_display_label"),
                        "clinical_display_label": r.get("clinical_display_label"),
                        "severity_state": r.get("severity_state"),
                        "frontend_allowed_term": r.get("frontend_allowed_term"),
                        "supporting_biomarkers_summary": r.get("supporting_biomarkers_summary"),
                    }
                )
    return {
        "present": True,
        "record_count": len(records) if isinstance(records, list) else 0,
        "enabled_count": len(enabled),
        "enabled": enabled,
        "version": idl.get("version") or idl.get("schema_version"),
    }


def _summarise_lifestyle_v1(payload: dict) -> Dict[str, Any]:
    lifestyle = payload.get("lifestyle")
    if not isinstance(lifestyle, dict):
        return {"present": False}
    sys_mods = lifestyle.get("system_modifiers", {})
    nonzero: Dict[str, float] = {}
    if isinstance(sys_mods, dict):
        for sysname, data in sys_mods.items():
            if isinstance(data, dict):
                cap = data.get("capped_total_modifier")
                try:
                    if cap is not None and float(cap) != 0:
                        nonzero[sysname] = float(cap)
                except Exception:
                    continue
    return {
        "present": True,
        "derived_inputs": lifestyle.get("derived_inputs"),
        "input_errors": lifestyle.get("input_errors"),
        "invalid_input_plausibility": lifestyle.get("invalid_input_plausibility"),
        "nonzero_capped_system_modifiers": nonzero,
        "adjusted_system_burdens": lifestyle.get("adjusted_system_burdens"),
    }


def _summarise_narrative_runtime(meta: dict) -> Dict[str, Any]:
    nr = meta.get("narrative_runtime", {}) if isinstance(meta, dict) else {}
    if not isinstance(nr, dict):
        return {"present": False}
    return {
        "runtime_mode": nr.get("runtime_mode"),
        "client_kind": nr.get("client_kind"),
        "policy_reason": nr.get("policy_reason"),
        "policy_version": nr.get("policy_version"),
        "synthesizer_allow_llm_resolved": nr.get("synthesizer_allow_llm_resolved"),
        "master_switch_HEALTHIQ_NARRATIVE_LLM": nr.get("master_switch_HEALTHIQ_NARRATIVE_LLM"),
    }


def _summarise_narrative_report_v1(nr: dict) -> Dict[str, Any]:
    if not isinstance(nr, dict):
        return {"present": False}
    out = {"present": True, "version": nr.get("narrative_report_version"), "secondary_systems": nr.get("secondary_systems")}
    for k in ("body_overview", "lead_narrative", "retail_summary", "clinician_synthesis", "secondary_narratives", "next_steps_narrative", "longitudinal_narrative"):
        v = nr.get(k)
        if isinstance(v, str):
            out[f"{k}_len"] = len(v)
            out[f"{k}_head"] = v[:280]
        else:
            out[f"{k}_len"] = 0
            out[f"{k}_head"] = ""
    return out


def _summarise_meta_extras(meta: dict) -> Dict[str, Any]:
    if not isinstance(meta, dict):
        return {}
    confidence = meta.get("system_confidence", {}) if isinstance(meta.get("system_confidence"), dict) else {}
    missing = meta.get("missing_markers", {}) if isinstance(meta.get("missing_markers"), dict) else {}
    downgrades = meta.get("confidence_downgrades", []) or []
    bridges = meta.get("lifestyle_interpretation_bridges_v1") or {}
    bridge_summary = {}
    if isinstance(bridges, dict):
        bridge_summary = {
            "active_bridges": bridges.get("active_bridges") if "active_bridges" in bridges else None,
            "bridges_count": len(bridges.get("bridges", [])) if isinstance(bridges.get("bridges"), list) else None,
            "keys": sorted(list(bridges.keys())),
        }
    return {
        "overall_confidence": meta.get("overall_confidence"),
        "system_confidence": confidence,
        "missing_markers_by_system": {k: list(v) for k, v in missing.items() if isinstance(v, list)},
        "confidence_downgrades_count": len(downgrades) if isinstance(downgrades, list) else 0,
        "confidence_downgrades_sample": downgrades[:5] if isinstance(downgrades, list) else [],
        "lifestyle_interpretation_bridges_v1_summary": bridge_summary,
    }


def extract_one(panel: str, profile: str) -> Optional[Dict[str, Any]]:
    run_dir = ART / f"{panel}__{profile}"
    res_path = run_dir / "analysis_result.json"
    if not res_path.exists():
        return None
    try:
        payload = json.loads(res_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"panel": panel, "profile": profile, "error": str(exc)}

    meta = payload.get("meta", {}) if isinstance(payload, dict) else {}
    insight_graph = meta.get("insight_graph", {}) if isinstance(meta, dict) else {}
    report_v1 = insight_graph.get("report_v1", {}) if isinstance(insight_graph, dict) else {}
    root_cause = report_v1.get("root_cause_v1", {}) if isinstance(report_v1, dict) else {}

    insights_top = payload.get("insights") or []
    out: Dict[str, Any] = {
        "panel": panel,
        "profile": profile,
        "status": payload.get("status"),
        "analysis_id": payload.get("analysis_id"),
        "overall_score": payload.get("overall_score"),
        "primary_driver_system_id": payload.get("primary_driver_system_id"),
        "biomarker_count": len(payload.get("biomarkers", [])) if isinstance(payload.get("biomarkers"), list) else 0,
        "insights_top_level": [
            {
                "category": ins.get("category"),
                "title": ins.get("title"),
                "description": ins.get("description"),
                "confidence": ins.get("confidence"),
                "biomarker_count": len(ins.get("biomarkers") or []),
                "manifest_id": ins.get("manifest_id"),
            }
            for ins in insights_top if isinstance(ins, dict)
        ],
        "top_findings": _summarise_top_findings(report_v1.get("top_findings") or []),
        "root_cause_v1": _summarise_root_cause(root_cause.get("findings") or []),
        "narrative_runtime": _summarise_narrative_runtime(meta),
        "narrative_report_v1": _summarise_narrative_report_v1(payload.get("narrative_report_v1", {})),
        "interpretation_display_layer_v1": _summarise_idl(payload.get("interpretation_display_layer_v1", {})),
        "lifestyle": _summarise_lifestyle_v1(payload),
        "meta_extras": _summarise_meta_extras(meta),
        "report_v1_meta": report_v1.get("meta"),
        "actions_count": len((report_v1.get("actions") or {}).get("daily", []) if isinstance(report_v1.get("actions"), dict) else []),
        "consumer_domain_scores": payload.get("consumer_domain_scores"),
    }
    return out


def main() -> int:
    extracted: List[Dict[str, Any]] = []
    for panel in PANEL_ORDER:
        for profile in PROFILE_ORDER:
            row = extract_one(panel, profile)
            if row is None:
                continue
            extracted.append(row)

    out = OUT_ROOT / "ledger_extract.json"
    out.write_text(json.dumps(extracted, indent=2, default=str), encoding="utf-8")
    print(f"WROTE {out} (records={len(extracted)})")

    diffs: Dict[str, Dict[str, Any]] = {}
    for panel in PANEL_ORDER:
        rows = [r for r in extracted if r.get("panel") == panel]
        if not rows:
            continue
        baseline = next((r for r in rows if r.get("profile") == "P0_no_lifestyle"), rows[0])
        per_panel: Dict[str, Any] = {
            "panel": panel,
            "baseline_profile": baseline.get("profile"),
            "baseline_overall_score": baseline.get("overall_score"),
            "baseline_primary_driver": baseline.get("primary_driver_system_id"),
            "baseline_top_finding_signal": _safe(baseline, "top_findings", "ranked", default=[]),
            "comparisons": [],
        }
        bsig = None
        bf = baseline.get("top_findings", {}).get("ranked") or []
        if bf:
            bsig = bf[0].get("signal_id")
        for r in rows:
            prof = r.get("profile")
            if prof == baseline.get("profile"):
                continue
            other_top = r.get("top_findings", {}).get("ranked") or []
            other_sig = other_top[0].get("signal_id") if other_top else None
            cmp_row = {
                "profile": prof,
                "overall_score": r.get("overall_score"),
                "overall_score_delta": (r.get("overall_score") or 0) - (baseline.get("overall_score") or 0),
                "primary_driver_system_id": r.get("primary_driver_system_id"),
                "primary_driver_changed": r.get("primary_driver_system_id") != baseline.get("primary_driver_system_id"),
                "lead_signal": other_sig,
                "lead_signal_changed": other_sig != bsig,
                "lifestyle_present": _safe(r, "lifestyle", "present"),
                "lifestyle_nonzero_modifiers": _safe(r, "lifestyle", "nonzero_capped_system_modifiers"),
                "lifestyle_input_errors": _safe(r, "lifestyle", "input_errors"),
                "lifestyle_invalid": _safe(r, "lifestyle", "invalid_input_plausibility"),
                "narrative_runtime_mode": _safe(r, "narrative_runtime", "runtime_mode"),
                "consumer_domain_scores_changed": r.get("consumer_domain_scores") != baseline.get("consumer_domain_scores"),
                "narrative_lead_head_baseline": _safe(baseline, "narrative_report_v1", "lead_narrative_head"),
                "narrative_lead_head_other": _safe(r, "narrative_report_v1", "lead_narrative_head"),
                "narrative_lead_changed": _safe(r, "narrative_report_v1", "lead_narrative_head") != _safe(baseline, "narrative_report_v1", "lead_narrative_head"),
                "retail_summary_changed": _safe(r, "narrative_report_v1", "retail_summary_head") != _safe(baseline, "narrative_report_v1", "retail_summary_head"),
                "actions_count_baseline": baseline.get("actions_count"),
                "actions_count_other": r.get("actions_count"),
                "idl_enabled_count_baseline": _safe(baseline, "interpretation_display_layer_v1", "enabled_count"),
                "idl_enabled_count_other": _safe(r, "interpretation_display_layer_v1", "enabled_count"),
                "system_confidence_baseline": _safe(baseline, "meta_extras", "system_confidence"),
                "system_confidence_other": _safe(r, "meta_extras", "system_confidence"),
            }
            per_panel["comparisons"].append(cmp_row)
        diffs[panel] = per_panel

    out2 = OUT_ROOT / "ledger_diff.json"
    out2.write_text(json.dumps(diffs, indent=2, default=str), encoding="utf-8")
    print(f"WROTE {out2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
