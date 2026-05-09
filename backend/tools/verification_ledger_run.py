"""
Launch-grade verification ledger driver.

Runs the production orchestrator on representative panels x lifestyle profiles
and emits a single JSON ledger file with the evidence we need to verify
runtime behaviour for the 2026-05 verification ledger.

Read-only against repo state. Writes only under docs/audit-papers/verification-2026-05-04/.
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from tools.run_golden_panel import run_golden_panel  # noqa: E402

OUT_ROOT = REPO_ROOT / "docs" / "audit-papers" / "verification-2026-05-04"
ARTIFACT_ROOT = OUT_ROOT / "artifacts"
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

PANELS: Dict[str, Path] = {
    "AB_full_panel_with_ranges": BACKEND / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json",
    "VR_full_panel_with_ranges": BACKEND / "tests" / "fixtures" / "panels" / "vr_full_panel_with_ranges.json",
    "AB_full_panel_with_profiles": BACKEND / "tests" / "fixtures" / "panels" / "ab_full_panel_with_profiles.json",
}

PROFILES: Dict[str, Optional[Path]] = {
    "P0_no_lifestyle": None,
    "P1_healthy": OUT_ROOT / "profile_healthy.json",
    "P2_minimal_existing_fixture": BACKEND / "tests" / "fixtures" / "lifestyle_minimal.json",
    "P3_stressed": OUT_ROOT / "profile_stressed.json",
}


def _safe(obj: Any, *path: str, default: Any = None) -> Any:
    cur = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def _summarise_signals(signal_results: List[dict]) -> Dict[str, Any]:
    if not isinstance(signal_results, list):
        return {"count": 0, "active": [], "by_state": {}}
    active: List[Dict[str, Any]] = []
    by_state: Dict[str, int] = {}
    for s in signal_results:
        if not isinstance(s, dict):
            continue
        state = str(s.get("activation_state") or s.get("state") or "")
        by_state[state] = by_state.get(state, 0) + 1
        if state and state not in {"normal", "no_activation", "neutral", "ok", "inactive"}:
            active.append(
                {
                    "id": s.get("signal_id") or s.get("id"),
                    "state": state,
                    "score": s.get("score") or s.get("severity_score"),
                    "drivers": s.get("driving_biomarkers") or s.get("driving_inputs") or s.get("biomarker_dependencies"),
                }
            )
    return {"count": len(signal_results), "active_count": len(active), "by_state": by_state, "active": active[:25]}


def _summarise_root_cause(insights: List[dict]) -> Dict[str, Any]:
    if not isinstance(insights, list):
        return {"present": False}
    out: Dict[str, Any] = {"present": False, "fallback_strings": [], "governed_for": [], "lengths": []}
    fallback_marker = "No hypothesis set available"
    for ins in insights:
        if not isinstance(ins, dict):
            continue
        rc = ins.get("root_cause") or ins.get("root_cause_summary") or ins.get("description") or ""
        if isinstance(rc, dict):
            text = json.dumps(rc)
        else:
            text = str(rc)
        if not text.strip():
            continue
        out["present"] = True
        out["lengths"].append(len(text))
        if fallback_marker in text:
            out["fallback_strings"].append({"insight_id": ins.get("id"), "head": text[:160]})
        else:
            out["governed_for"].append({"insight_id": ins.get("id"), "head": text[:200]})
    return out


def _extract_clinician_report(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    cr = analysis_result.get("clinician_report") or _safe(analysis_result, "meta", "clinician_report") or {}
    if not isinstance(cr, dict):
        return {}
    page1 = cr.get("page1", {}) if isinstance(cr.get("page1"), dict) else {}
    return {
        "primary_concern": page1.get("primary_concern"),
        "primary_concern_mode": page1.get("primary_concern_mode") or page1.get("mode"),
        "runner_up_topic_line": page1.get("runner_up_topic_line"),
        "runner_up_why_not_lead_line": page1.get("runner_up_why_not_lead_line"),
        "missing_data_line": page1.get("missing_data_line") or page1.get("missing_data") or cr.get("missing_data_line"),
        "confidence_line": page1.get("confidence_line") or page1.get("confidence"),
        "headline": page1.get("headline") or page1.get("title"),
        "page1_keys": sorted(list(page1.keys())) if isinstance(page1, dict) else [],
        "report_keys": sorted(list(cr.keys())),
    }


def _extract_idl(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    idl = analysis_result.get("interpretation_display_layer_v1") or analysis_result.get("idl_bundle") or {}
    if not isinstance(idl, dict):
        return {"present": False}
    records = idl.get("records") or idl.get("display_records") or []
    enabled = [r for r in records if isinstance(r, dict) and r.get("enabled_for_frontend")]
    return {
        "present": True,
        "record_count": len(records) if isinstance(records, list) else 0,
        "enabled_count": len(enabled),
        "first_enabled": enabled[:5],
        "version": idl.get("version") or idl.get("schema_version"),
    }


def _extract_lifestyle(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    lifestyle = analysis_result.get("lifestyle")
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
        "nonzero_capped_modifiers": nonzero,
        "adjusted_system_burdens_keys": sorted(list((lifestyle.get("adjusted_system_burdens") or {}).keys())),
    }


def _extract_meta_modes(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    meta = analysis_result.get("meta", {}) if isinstance(analysis_result, dict) else {}
    narrative_runtime = meta.get("narrative_runtime") or {}
    explainability = meta.get("explainability_report", {})
    return {
        "narrative_runtime_mode": narrative_runtime.get("mode") if isinstance(narrative_runtime, dict) else None,
        "narrative_runtime_keys": sorted(list(narrative_runtime.keys())) if isinstance(narrative_runtime, dict) else [],
        "explainability_present": bool(explainability),
        "meta_keys": sorted(list(meta.keys())),
    }


def run_one(panel_name: str, panel_path: Path, profile_name: str, profile_path: Optional[Path]) -> Dict[str, Any]:
    run_id = f"{panel_name}__{profile_name}"
    run_dir = ARTIFACT_ROOT / run_id
    try:
        rd, analysis_result = run_golden_panel(
            fixture_path=panel_path,
            output_root=ARTIFACT_ROOT,
            run_id=run_id,
            write_narrative=True,
            enable_llm=False,
            lifestyle_fixture_path=profile_path,
        )
        ok = True
        err: Optional[str] = None
    except Exception as exc:
        rd = run_dir
        rd.mkdir(parents=True, exist_ok=True)
        analysis_result = {}
        ok = False
        err = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
        (rd / "error.txt").write_text(err, encoding="utf-8")

    insights = analysis_result.get("insights") or []
    signal_results = (
        analysis_result.get("signal_results")
        or _safe(analysis_result, "meta", "signal_results")
        or _safe(analysis_result, "meta", "insight_graph", "signal_results")
        or []
    )

    summary = {
        "panel": panel_name,
        "profile": profile_name,
        "panel_path": str(panel_path),
        "profile_path": str(profile_path) if profile_path else None,
        "ok": ok,
        "error": err,
        "status": analysis_result.get("status"),
        "engine_version": analysis_result.get("engine_version") or _safe(analysis_result, "meta", "engine_version"),
        "schema_version": analysis_result.get("schema_version"),
        "biomarker_count": len(analysis_result.get("biomarkers") or {}),
        "insight_count": len(insights) if isinstance(insights, list) else 0,
        "insight_titles": [str(i.get("title") or i.get("id")) for i in insights[:8] if isinstance(i, dict)],
        "signal_summary": _summarise_signals(signal_results if isinstance(signal_results, list) else []),
        "root_cause_summary": _summarise_root_cause(insights if isinstance(insights, list) else []),
        "clinician_report": _extract_clinician_report(analysis_result),
        "idl": _extract_idl(analysis_result),
        "lifestyle": _extract_lifestyle(analysis_result),
        "meta_modes": _extract_meta_modes(analysis_result),
        "top_findings": analysis_result.get("top_findings"),
        "primary_concern_top": analysis_result.get("primary_concern"),
        "result_keys": sorted(list(analysis_result.keys())) if isinstance(analysis_result, dict) else [],
        "run_dir": str(rd),
    }
    return summary


def main() -> int:
    ledger: List[Dict[str, Any]] = []
    for panel_name, panel_path in PANELS.items():
        if not panel_path.exists():
            ledger.append({"panel": panel_name, "skipped": True, "reason": "fixture not found"})
            continue
        for profile_name, profile_path in PROFILES.items():
            if profile_path is not None and not profile_path.exists():
                ledger.append({"panel": panel_name, "profile": profile_name, "skipped": True, "reason": "profile not found"})
                continue
            print(f"RUN {panel_name} x {profile_name}")
            row = run_one(panel_name, panel_path, profile_name, profile_path)
            print(f"  ok={row.get('ok')} status={row.get('status')} insights={row.get('insight_count')}")
            ledger.append(row)

    out = OUT_ROOT / "ledger_runs.json"
    out.write_text(json.dumps(ledger, indent=2, default=str), encoding="utf-8")
    print(f"WROTE {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
