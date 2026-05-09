"""
Launch-core proving harness — bounded AB × VR × scenario matrix via real golden-panel pipeline.

Read-only consumer of run_golden_panel / orchestrator. Does not modify run_golden_panel.py.

Outputs human-readable markdown plus JSON fingerprints under docs/audit-papers/launch-core-proving/.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
DEFAULT_MATRIX = BACKEND / "tests" / "fixtures" / "proving" / "launch_core_matrix.json"
DEFAULT_OUT_ROOT = REPO_ROOT / "docs" / "audit-papers" / "launch-core-proving"

sys.path.insert(0, str(BACKEND))

from tools.run_golden_panel import run_golden_panel  # noqa: E402


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _report_v1_dict(ig: Dict[str, Any]) -> Dict[str, Any]:
    rv = ig.get("report_v1")
    if rv is None:
        return {}
    if hasattr(rv, "model_dump"):
        return rv.model_dump()
    return rv if isinstance(rv, dict) else {}


def _top_finding_signal_ids(ig: Dict[str, Any]) -> List[str]:
    tf = _report_v1_dict(ig).get("top_findings") or []
    out: List[str] = []
    for row in tf:
        if isinstance(row, dict):
            sid = str(row.get("signal_id", "")).strip()
            if sid:
                out.append(sid)
    return out


def _signal_state_map(ig: Dict[str, Any]) -> Dict[str, str]:
    srs = ig.get("signal_results") or []
    out: Dict[str, str] = {}
    for row in srs:
        if isinstance(row, dict) and row.get("signal_id"):
            sid = str(row["signal_id"]).strip()
            out[sid] = str(row.get("signal_state", "")).strip()
    return out


def _domain_rows(analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = analysis_result.get("consumer_domain_scores") or []
    if not isinstance(rows, list):
        return []
    norm: List[Dict[str, Any]] = []
    for row in rows:
        if hasattr(row, "model_dump"):
            row = row.model_dump()
        if not isinstance(row, dict):
            continue
        did = str(row.get("domain_id", "") or row.get("domain", "") or "")
        norm.append(
            {
                "domain_id": did,
                "band_label": str(row.get("band_label", "")),
                "consequence_sentence_head": (str(row.get("consequence_sentence", "") or ""))[:220],
            }
        )
    norm.sort(key=lambda x: x["domain_id"])
    return norm


def _domain_band_labels(rows: List[Dict[str, Any]]) -> List[str]:
    return [r["band_label"] for r in rows]


def _narrative_heads(nr: Any) -> Dict[str, Any]:
    if nr is None:
        return {}
    if hasattr(nr, "model_dump"):
        nr = nr.model_dump()
    if not isinstance(nr, dict):
        return {}
    return {
        "retail_summary_head": (nr.get("retail_summary") or "")[:320],
        "body_overview_head": (nr.get("body_overview") or "")[:480],
        "lead_narrative_head": (nr.get("lead_narrative") or "")[:320],
    }


def _clinician_heads(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    cr = analysis_result.get("clinician_report_v1") or {}
    if not isinstance(cr, dict):
        return {}
    sections = cr.get("sections") or {}
    if not isinstance(sections, dict):
        return {}
    p1 = sections.get("page1") or {}
    if not isinstance(p1, dict):
        return {}
    kf = p1.get("key_findings")
    kf_head = ""
    if isinstance(kf, list) and kf:
        kf_head = str(kf[0])[:200]
    elif isinstance(kf, str):
        kf_head = kf[:200]
    return {
        "primary_concern_head": str(p1.get("primary_concern") or "")[:280],
        "key_findings_head": kf_head,
        "top_hypothesis_line_head": str(p1.get("top_hypothesis_line") or "")[:280],
    }


def _idl_summary(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    idl = analysis_result.get("interpretation_display_layer_v1") or analysis_result.get("idl_bundle") or {}
    if not isinstance(idl, dict):
        return {"present": False}
    recs = idl.get("records") or idl.get("display_records") or []
    enabled = [r for r in recs if isinstance(r, dict) and r.get("enabled_for_frontend")]
    first_titles: List[str] = []
    for r in enabled[:5]:
        title = r.get("pattern_title") or r.get("title") or r.get("headline") or ""
        first_titles.append(str(title)[:120])
    return {
        "present": True,
        "enabled_count": len(enabled),
        "first_enabled_titles": first_titles,
        "version": idl.get("version") or idl.get("schema_version"),
    }


def _intervention_summary(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    ia = analysis_result.get("intervention_annotations_v1")
    if ia is None:
        return {"present": False, "resolved_class_ids": []}
    if hasattr(ia, "model_dump"):
        ia = ia.model_dump()
    if not isinstance(ia, dict):
        return {"present": False, "resolved_class_ids": []}
    resolved = ia.get("resolved") or []
    ids: List[str] = []
    for row in resolved:
        if isinstance(row, dict) and row.get("intervention_class_id"):
            ids.append(str(row["intervention_class_id"]))
    return {"present": True, "resolved_class_ids": sorted(ids)}


def _consumer_domain_row_matching(rows: Any, substr: str) -> Optional[Dict[str, Any]]:
    for r in rows or []:
        if isinstance(r, dict) and substr in str(r.get("domain_id", "")):
            return r
    return None


def fingerprint_analysis_result(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    meta = analysis_result.get("meta") or {}
    ig = meta.get("insight_graph") or {}
    if not isinstance(ig, dict):
        ig = {}
    domain_rows = _domain_rows(analysis_result)
    return {
        "status": analysis_result.get("status"),
        "top_finding_signal_ids": _top_finding_signal_ids(ig),
        "signal_state_by_id": dict(sorted(_signal_state_map(ig).items())),
        "consumer_domain_rows": domain_rows,
        "consumer_band_labels": _domain_band_labels(domain_rows),
        "narrative": _narrative_heads(analysis_result.get("narrative_report_v1")),
        "clinician_page1": _clinician_heads(analysis_result),
        "idl": _idl_summary(analysis_result),
        "intervention": _intervention_summary(analysis_result),
    }


def _short_git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return ""


def load_matrix(path: Path) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    panels = raw.get("panels") or {}
    scenarios = raw.get("scenarios") or []
    if not isinstance(panels, dict) or not isinstance(scenarios, list):
        raise ValueError("launch_core_matrix.json: invalid panels/scenarios shape")
    panel_paths: Dict[str, str] = {str(k): str(v) for k, v in panels.items()}
    scen_list: List[Dict[str, Any]] = [s for s in scenarios if isinstance(s, dict)]
    return panel_paths, scen_list


def build_merged_fixture(
    panel_path: Path,
    scenario: Dict[str, Any],
    write_path: Path,
) -> None:
    payload = json.loads(panel_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("panel fixture must be a JSON object")
    merged = copy.deepcopy(payload)
    qd = scenario.get("questionnaire_data", "__OMIT__")
    if qd == "__OMIT__":
        raise ValueError("scenario missing questionnaire_data key (use null to omit)")
    if qd is None:
        merged.pop("questionnaire_data", None)
    else:
        merged["questionnaire_data"] = qd
    write_path.parent.mkdir(parents=True, exist_ok=True)
    write_path.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")


def resolve_lifestyle_path(rel: Optional[str]) -> Optional[Path]:
    if not rel:
        return None
    p = (BACKEND / rel).resolve()
    if not p.exists():
        raise FileNotFoundError(f"lifestyle fixture not found: {p}")
    return p


def resolve_panel_path(rel: str) -> Path:
    p = (BACKEND / rel).resolve()
    if not p.exists():
        raise FileNotFoundError(f"panel fixture not found: {p}")
    return p


def run_matrix(
    matrix_path: Path,
    out_root: Path,
    stamp: Optional[str] = None,
) -> Tuple[Path, Dict[str, Any]]:
    stamp = stamp or _utc_stamp()
    panel_map, scenarios = load_matrix(matrix_path)
    artifacts_root = out_root / "artifacts" / stamp
    fixtures_dir = artifacts_root / "_merged_fixtures"
    artifacts_root.mkdir(parents=True, exist_ok=True)

    fingerprints: Dict[str, Any] = {
        "stamp": stamp,
        "matrix_path": str(matrix_path.relative_to(REPO_ROOT)),
        "git_short_sha": _short_git_sha(),
        "runs": {},
    }

    for panel_key, rel_panel in panel_map.items():
        panel_path = resolve_panel_path(rel_panel)
        for sc in scenarios:
            sid = str(sc.get("id", "")).strip()
            if not sid:
                continue
            run_id = f"{panel_key}__{sid}"
            merged_path = fixtures_dir / f"{run_id}.json"
            build_merged_fixture(panel_path, sc, merged_path)
            lifestyle = resolve_lifestyle_path(sc.get("lifestyle_fixture"))

            _run_dir, analysis_result = run_golden_panel(
                fixture_path=merged_path,
                output_root=artifacts_root,
                run_id=run_id,
                write_narrative=True,
                enable_llm=False,
                lifestyle_fixture_path=lifestyle,
            )
            fp = fingerprint_analysis_result(analysis_result if isinstance(analysis_result, dict) else {})
            fp["scenario_description"] = sc.get("description")
            fp["lifestyle_fixture"] = sc.get("lifestyle_fixture")
            fp["questionnaire_data"] = sc.get("questionnaire_data")
            fingerprints["runs"][run_id] = fp

    report_path = write_markdown_report(out_root, fingerprints, scenarios, panel_map)
    fp_path = out_root / "latest_fingerprints.json"
    fp_path.write_text(json.dumps(fingerprints, indent=2, sort_keys=True), encoding="utf-8")
    return report_path, fingerprints


def _fp_equal(a: Dict[str, Any], b: Dict[str, Any], keys: Tuple[str, ...]) -> bool:
    for k in keys:
        if a.get(k) != b.get(k):
            return False
    return True


def write_markdown_report(
    out_root: Path,
    fingerprints: Dict[str, Any],
    scenarios: List[Dict[str, Any]],
    panel_map: Dict[str, str],
) -> Path:
    runs: Dict[str, Any] = fingerprints.get("runs") or {}
    lines: List[str] = []
    lines.append("# Launch-core proving harness — comparison report")
    lines.append("")
    lines.append(f"- **Stamp:** `{fingerprints.get('stamp')}`")
    lines.append(f"- **Git (short):** `{fingerprints.get('git_short_sha')}`")
    lines.append(f"- **Matrix:** `{fingerprints.get('matrix_path')}`")
    lines.append("")
    lines.append("## Scenario matrix (panels × scenarios)")
    lines.append("")
    lines.append("| Panel | Scenario | Description |")
    lines.append("|-------|----------|-------------|")
    for pk in sorted(panel_map.keys()):
        for sc in scenarios:
            sid = sc.get("id", "")
            lines.append(f"| {pk} | `{sid}` | {sc.get('description', '')} |")
    lines.append("")
    lines.append("## Per-run fingerprints (compact)")
    lines.append("")
    for run_id in sorted(runs.keys()):
        fp = runs[run_id]
        lines.append(f"### `{run_id}`")
        lines.append("")
        lines.append(f"- **status:** {fp.get('status')}")
        lines.append(f"- **top findings (order):** `{', '.join(fp.get('top_finding_signal_ids') or [])}`")
        lines.append(f"- **consumer band labels:** `{fp.get('consumer_band_labels')}`")
        lines.append(f"- **intervention present:** {fp.get('intervention', {}).get('present')} "
                     f"classes={fp.get('intervention', {}).get('resolved_class_ids')}")
        nar = fp.get("narrative") or {}
        lines.append(f"- **retail summary (head):** {nar.get('retail_summary_head', '')[:160]}...")
        lines.append(f"- **body overview (head):** {nar.get('body_overview_head', '')[:160]}...")
        clin = fp.get("clinician_page1") or {}
        lines.append(f"- **clinician primary_concern (head):** {clin.get('primary_concern_head', '')[:160]}...")
        idl = fp.get("idl") or {}
        lines.append(f"- **IDL enabled patterns:** {idl.get('enabled_count')} "
                     f"titles={idl.get('first_enabled_titles')}")
        lines.append("")

    lines.append("## Analytical invariants — statin-off vs statin-on (same panel, no lifestyle)")
    lines.append("")
    lines.append(
        "Expect: identical **top-finding order**, **signal_state** map, and **consumer band labels**; "
        "intervention/statin wording differs only on statin-on."
    )
    lines.append("")
    for panel_key in sorted(panel_map.keys()):
        a = f"{panel_key}__statin_off"
        b = f"{panel_key}__statin_on"
        if a not in runs or b not in runs:
            lines.append(f"- **{panel_key}:** missing runs — skip.")
            continue
        fa, fb = runs[a], runs[b]
        ok = _fp_equal(fa, fb, ("top_finding_signal_ids", "signal_state_by_id", "consumer_band_labels"))
        lines.append(f"- **{panel_key}:** invariants match — **{'PASS' if ok else 'FAIL'}**")
        if not ok:
            lines.append(f"  - top ids off==on: {fa.get('top_finding_signal_ids') == fb.get('top_finding_signal_ids')}")
            lines.append(f"  - signal states: {fa.get('signal_state_by_id') == fb.get('signal_state_by_id')}")
            lines.append(f"  - bands: {fa.get('consumer_band_labels') == fb.get('consumer_band_labels')}")
        absent_off = not (fa.get("intervention") or {}).get("present")
        present_on = bool((fb.get("intervention") or {}).get("present"))
        cv_off = _consumer_domain_row_matching(fa.get("consumer_domain_rows"), "cardiovascular")
        cv_on = _consumer_domain_row_matching(fb.get("consumer_domain_rows"), "cardiovascular")
        cv_sentence_changed = (cv_off or {}).get("consequence_sentence_head") != (cv_on or {}).get("consequence_sentence_head")
        lines.append(
            f"  - statin intervention absent→present: **{'PASS' if absent_off and present_on else 'CHECK'}** "
            f"(absent_when_off={absent_off}, present_when_on={present_on})"
        )
        lines.append(
            f"  - narrative body differs (expected): **{fa.get('narrative', {}).get('body_overview_head') != fb.get('narrative', {}).get('body_overview_head')}**"
        )
        lines.append(
            f"  - CV consequence_sentence head differs (expected on statin-on): **{cv_sentence_changed}**"
        )
        lines.append("")

    lines.append("## Lifestyle/context payoff — baseline vs lifestyle_context")
    lines.append("")
    lines.append("Expect: lifestyle-derived fields present under lifestyle_context; narrative heads may diverge.")
    lines.append("")
    for panel_key in sorted(panel_map.keys()):
        base = f"{panel_key}__baseline"
        life = f"{panel_key}__lifestyle_context"
        if base not in runs or life not in runs:
            lines.append(f"- **{panel_key}:** missing runs — skip.")
            continue
        f0, f1 = runs[base], runs[life]
        bands_stable = f0.get("consumer_band_labels") == f1.get("consumer_band_labels")
        top_stable = f0.get("top_finding_signal_ids") == f1.get("top_finding_signal_ids")
        narrative_diff = (f0.get("narrative") or {}) != (f1.get("narrative") or {})
        lines.append(
            f"- **{panel_key}:** top_findings unchanged={top_stable}; bands unchanged={bands_stable}; "
            f"narrative block differs={narrative_diff}"
        )
        lines.append("")

    lines.append("## Artifact paths")
    lines.append("")
    stamp = fingerprints.get("stamp")
    rel_art = artifacts_root_rel(out_root, stamp).replace("\\", "/")
    try:
        rel_fp = str((out_root / "latest_fingerprints.json").resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        rel_fp = str(out_root / "latest_fingerprints.json")
    lines.append(
        f"- Golden outputs (per run): `{rel_art}/` — written by `run_golden_panel`; omit bulk artefacts from git if desired."
    )
    lines.append(f"- Latest fingerprints JSON: `{rel_fp}`")
    lines.append("")
    report_path = out_root / "PROVING_REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def artifacts_root_rel(out_root: Path, stamp: Optional[str]) -> str:
    if not stamp:
        return str(out_root / "artifacts")
    try:
        return str((out_root / "artifacts" / stamp).relative_to(REPO_ROOT))
    except ValueError:
        return str(out_root / "artifacts" / stamp)


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch-core proving harness (AB × VR × scenarios).")
    parser.add_argument(
        "--matrix",
        type=Path,
        default=DEFAULT_MATRIX,
        help="Path to launch_core_matrix.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_ROOT,
        help="Output directory for PROVING_REPORT.md and artifacts/",
    )
    parser.add_argument("--stamp", type=str, default=None, help="Optional run stamp (default UTC timestamp).")
    args = parser.parse_args()
    matrix_path = args.matrix.resolve()
    out_root = args.out.resolve()
    if not matrix_path.exists():
        print(f"Matrix not found: {matrix_path}", file=sys.stderr)
        return 2
    out_root.mkdir(parents=True, exist_ok=True)
    report_path, _ = run_matrix(matrix_path, out_root, stamp=args.stamp)
    print(f"WROTE {report_path}")
    print(f"WROTE {out_root / 'latest_fingerprints.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
