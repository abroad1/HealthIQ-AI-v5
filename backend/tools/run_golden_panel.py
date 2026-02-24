"""
v5.3 Sprint 6 - GoldenPanelRunner_v1 + Intelligence Snapshot Pack.

Evaluation harness only. Uses existing runtime pipeline without changing biological logic.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.canonical.alias_registry_service import get_alias_registry_service
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.analytics.calibration_engine import build_calibration_layer_v1
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, UnitRegistry, apply_unit_normalisation


VOLATILE_FIELD_ALLOWLIST = {
    "created_at",
    "elapsed_ms",
    "latency_ms",
    "processing_time_seconds",
}


class _EmptySession:
    """Minimal query-chain stub to force deterministic empty prior snapshots."""

    def query(self, *args: Any, **kwargs: Any) -> "_EmptySession":
        return self

    def join(self, *args: Any, **kwargs: Any) -> "_EmptySession":
        return self

    def filter(self, *args: Any, **kwargs: Any) -> "_EmptySession":
        return self

    def all(self) -> list[Any]:
        return []


def _default_fixture_path() -> Path:
    return Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "golden_panel_160.json"


def _default_output_root() -> Path:
    return Path(__file__).resolve().parent.parent / "artifacts" / "golden_runs"


def _read_payload(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Golden panel fixture must be a JSON object")
    if "biomarkers" not in payload or "user" not in payload:
        raise ValueError("Golden panel fixture must include biomarkers and user")
    return payload


def _strip_volatile_fields(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for key, value in obj.items():
            if key in VOLATILE_FIELD_ALLOWLIST:
                continue
            out[key] = _strip_volatile_fields(value)
        return out
    if isinstance(obj, list):
        return [_strip_volatile_fields(item) for item in obj]
    return obj


def _normalise_for_artifact_write(obj: Any) -> Any:
    return _strip_volatile_fields(copy.deepcopy(obj))


def _ensure_run_dir(output_root: Path, run_id: Optional[str]) -> Path:
    resolved_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_root / resolved_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _current_git_short_sha() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
        return out.strip()
    except Exception:
        return ""


def _sorted_dict_list(items: list[dict[str, Any]], sort_keys: tuple[str, ...]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: tuple(str(item.get(k, "")) for k in sort_keys))


def _calibration_tier_by_system(calibration_items: list[dict[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in calibration_items:
        if not isinstance(item, dict):
            continue
        system_id = str(item.get("system_id", "")).strip()
        if not system_id:
            continue
        out[system_id] = str(item.get("priority_tier", "")).strip()
    return out


def build_arbitration_report(
    insight_graph: dict[str, Any],
    replay_manifest: dict[str, Any],
    run_id: str,
) -> dict[str, Any]:
    conflict_set = insight_graph.get("conflict_set", []) if isinstance(insight_graph, dict) else []
    dominance_edges = insight_graph.get("dominance_edges", []) if isinstance(insight_graph, dict) else []
    causal_edges = insight_graph.get("causal_edges", []) if isinstance(insight_graph, dict) else []
    arbitration_result = insight_graph.get("arbitration_result", {}) if isinstance(insight_graph, dict) else {}
    primary_driver_system_id = str(insight_graph.get("primary_driver_system_id", "")) if isinstance(insight_graph, dict) else ""

    conflict_summary = _sorted_dict_list(
        [
            {
                "conflict_id": str(c.get("conflict_id", "")),
                "conflict_type": str(c.get("conflict_type", "")),
                "severity": str(c.get("conflict_severity", "")),
                "system_ids": sorted([str(c.get("system_a", "")), str(c.get("system_b", ""))]),
                "rationale_codes": sorted(set(c.get("rationale_codes", []))),
            }
            for c in conflict_set
            if isinstance(c, dict)
        ],
        ("conflict_id", "conflict_type", "system_ids"),
    )

    precedence_summary = _sorted_dict_list(
        [
            {
                "rule_id": str(e.get("rule_id", "")),
                "conflict_id": str(e.get("conflict_id", "")),
                "from_system_id": str(e.get("from_system_id", "")),
                "to_system_id": str(e.get("to_system_id", "")),
                "precedence_tier": int(e.get("precedence_tier", 0)),
                "rationale_codes": sorted(set(e.get("rationale_codes", []))),
            }
            for e in dominance_edges
            if isinstance(e, dict)
        ],
        ("from_system_id", "to_system_id", "precedence_tier", "rule_id", "conflict_id"),
    )

    causal_used = _sorted_dict_list(
        [
            {
                "edge_id": str(e.get("edge_id", "")),
                "from_system_id": str(e.get("from_system_id", "")),
                "to_system_id": str(e.get("to_system_id", "")),
                "edge_code": str(e.get("edge_type", "")),
                "priority": int(e.get("priority", 0)),
                "source_conflict_ids": sorted(set(e.get("source_conflict_ids", []))),
            }
            for e in causal_edges
            if isinstance(e, dict)
        ],
        ("from_system_id", "to_system_id", "edge_code", "edge_id"),
    )

    supporting = sorted(
        set(str(x).strip() for x in arbitration_result.get("supporting_system_ids", []) if str(x).strip())
    ) if isinstance(arbitration_result, dict) else []
    decision_trace = sorted(
        set(str(x).strip() for x in arbitration_result.get("decision_trace_codes", []) if str(x).strip())
    ) if isinstance(arbitration_result, dict) else []

    # Compute pre-coupling calibration baseline from same graph (artifact-only analysis).
    previous_tier = ""
    final_tier = ""
    reasons: list[str] = []
    if isinstance(insight_graph, dict):
        ig_model = InsightGraphV1(**insight_graph)
        baseline_items, _ = build_calibration_layer_v1(ig_model, apply_arbitration_coupling=False)
        baseline_map = _calibration_tier_by_system([x.model_dump() for x in baseline_items])
        final_map = _calibration_tier_by_system(
            [x for x in (insight_graph.get("calibration_items", []) or []) if isinstance(x, dict)]
        )
        previous_tier = baseline_map.get(primary_driver_system_id, "")
        final_tier = final_map.get(primary_driver_system_id, "")
        for item in insight_graph.get("calibration_items", []) or []:
            if isinstance(item, dict) and str(item.get("system_id", "")) == primary_driver_system_id:
                reasons = sorted(set(str(x) for x in item.get("explanation_codes", []) if str(x)))
                break

    report = {
        "run_metadata": {
            "run_id": run_id,
            "git_commit_short": _current_git_short_sha(),
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "arbitration_version": str(insight_graph.get("arbitration_version", "")) if isinstance(insight_graph, dict) else "",
            "arbitration_hash": str(insight_graph.get("arbitration_hash", "")) if isinstance(insight_graph, dict) else "",
        },
        "conflict_summary": conflict_summary,
        "precedence_summary": precedence_summary,
        "causal_edges": causal_used,
        "arbitration_decisions": {
            "primary_driver_system_id": primary_driver_system_id,
            "supporting_systems": supporting,
            "decision_trace": decision_trace,
        },
        "calibration_impact": {
            "system_id": primary_driver_system_id,
            "previous_calibration_tier": previous_tier,
            "final_calibration_tier": final_tier,
            "reasons": reasons,
        },
        "replay_stamps": {
            "conflict_registry_version": replay_manifest.get("conflict_registry_version", ""),
            "conflict_registry_hash": replay_manifest.get("conflict_registry_hash", ""),
            "arbitration_registry_version": replay_manifest.get("arbitration_registry_version", ""),
            "arbitration_registry_hash": replay_manifest.get("arbitration_registry_hash", ""),
            "arbitration_version": replay_manifest.get("arbitration_version", ""),
            "arbitration_hash": replay_manifest.get("arbitration_hash", ""),
        },
    }
    return report


def _filter_unit_registry_supported(normalized: Mapping[str, Any]) -> Dict[str, Any]:
    """Keep only biomarkers that unit registry can deterministically convert."""
    base_units = UnitRegistry()._load_biomarker_base_units()
    return {k: v for k, v in normalized.items() if k in base_units}


def _coerce_to_ssot_units(normalized: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Align fixture units with SSOT canonical units before conversion.
    This is artifact-harness prep only; runtime contracts remain unchanged.
    """
    reg = UnitRegistry()
    out: Dict[str, Any] = {}
    for key, value in normalized.items():
        row = dict(value) if isinstance(value, dict) else {"value": value}
        target_unit = reg._get_ssot_unit(key) or reg.get_base_unit(key)
        row["unit"] = target_unit
        ref = row.get("reference_range")
        if isinstance(ref, dict):
            ref_copy = dict(ref)
            ref_copy["unit"] = target_unit
            row["reference_range"] = ref_copy
        out[key] = row
    return out


def _detect_canonical_collisions(raw_biomarkers: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Deterministically detect duplicate canonical targets from raw input labels."""
    alias_service = get_alias_registry_service()
    canonical_to_raw: dict[str, set[str]] = {}
    for raw_key in sorted(str(k) for k in raw_biomarkers.keys()):
        canonical_id = str(alias_service.resolve(raw_key)).strip()
        if not canonical_id or canonical_id.startswith("unmapped_"):
            continue
        canonical_to_raw.setdefault(canonical_id, set()).add(raw_key)
    collisions: list[dict[str, Any]] = []
    for canonical_id in sorted(canonical_to_raw.keys()):
        raw_markers = sorted(canonical_to_raw[canonical_id])
        if len(raw_markers) > 1:
            collisions.append(
                {
                    "canonical_id": canonical_id,
                    "raw_markers": raw_markers,
                    "reason": "multiple_raw_inputs_resolve_to_same_canonical_id",
                }
            )
    return collisions


def _write_collision_error_artifacts(
    *,
    run_dir: Path,
    fixture: Path,
    collisions: list[dict[str, Any]],
) -> Dict[str, Any]:
    now = datetime.now(UTC).isoformat()
    analysis_result: Dict[str, Any] = {
        "status": "error",
        "error_type": "canonical_collision",
        "error_payload": {"collisions": collisions},
        "created_at": now,
        "run_id": run_dir.name,
        "fixture": str(fixture),
    }
    (run_dir / "analysis_result.json").write_text(
        json.dumps(_normalise_for_artifact_write(analysis_result), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    error_payload = {
        "status": "error",
        "error_type": "canonical_collision",
        "error_payload": {"collisions": collisions},
    }
    (run_dir / "error.json").write_text(
        json.dumps(_normalise_for_artifact_write(error_payload), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return analysis_result


def run_golden_panel(
    fixture_path: Optional[Path] = None,
    output_root: Optional[Path] = None,
    run_id: Optional[str] = None,
    write_narrative: bool = True,
) -> Tuple[Path, Dict[str, Any]]:
    fixture = fixture_path or _default_fixture_path()
    out_root = output_root or _default_output_root()
    run_dir = _ensure_run_dir(out_root, run_id)
    payload = _read_payload(fixture)
    collisions = _detect_canonical_collisions(payload["biomarkers"])
    if collisions:
        return run_dir, _write_collision_error_artifacts(
            run_dir=run_dir,
            fixture=fixture,
            collisions=collisions,
        )

    try:
        biomarkers = normalize_biomarkers_with_metadata(payload["biomarkers"])
    except Exception as err:
        if type(err).__name__ != "CanonicalCollisionError":
            raise
        fallback_collisions = _detect_canonical_collisions(payload["biomarkers"])
        return run_dir, _write_collision_error_artifacts(
            run_dir=run_dir,
            fixture=fixture,
            collisions=fallback_collisions,
        )

    biomarkers = _filter_unit_registry_supported(biomarkers)
    biomarkers = _coerce_to_ssot_units(biomarkers)
    biomarkers = apply_unit_normalisation(biomarkers)
    biomarkers[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }

    orchestrator = AnalysisOrchestrator(db_session=_EmptySession())
    dto = orchestrator.run(biomarkers, payload["user"], assume_canonical=True)
    dto_dump = dto.model_dump() if hasattr(dto, "model_dump") else dict(dto)

    analysis_result = dto_dump
    meta = analysis_result.get("meta", {}) if isinstance(analysis_result, dict) else {}
    insight_graph = meta.get("insight_graph", {}) if isinstance(meta, dict) else {}
    explainability_report = meta.get("explainability_report", {}) if isinstance(meta, dict) else {}
    burden_vector = meta.get("burden_vector", {}) if isinstance(meta, dict) else {}
    replay_manifest = analysis_result.get("replay_manifest", {}) if isinstance(analysis_result, dict) else {}
    if not isinstance(explainability_report, dict) or not explainability_report:
        raise ValueError("Golden panel runner requires stamped explainability_report in production artifacts")

    (run_dir / "analysis_result.json").write_text(
        json.dumps(_normalise_for_artifact_write(analysis_result), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (run_dir / "insight_graph.json").write_text(
        json.dumps(_normalise_for_artifact_write(insight_graph), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (run_dir / "replay_manifest.json").write_text(
        json.dumps(_normalise_for_artifact_write(replay_manifest), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (run_dir / "explainability_report.json").write_text(
        json.dumps(_normalise_for_artifact_write(explainability_report), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (run_dir / "burden_vector.json").write_text(
        json.dumps(_normalise_for_artifact_write(burden_vector), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report = build_arbitration_report(
        insight_graph=insight_graph if isinstance(insight_graph, dict) else {},
        replay_manifest=replay_manifest if isinstance(replay_manifest, dict) else {},
        run_id=run_dir.name,
    )
    (run_dir / "arbitration_report.json").write_text(
        json.dumps(_normalise_for_artifact_write(report), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    if write_narrative:
        insights = analysis_result.get("insights", []) if isinstance(analysis_result, dict) else []
        lines = []
        for item in insights:
            if not isinstance(item, dict):
                continue
            summary = str(item.get("description") or item.get("title") or "").strip()
            if summary:
                lines.append(summary)
        (run_dir / "narrative.txt").write_text("\n\n".join(lines), encoding="utf-8")

    return run_dir, analysis_result


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic golden panel and write snapshot pack artifacts.")
    parser.add_argument("--fixture", default=str(_default_fixture_path()), help="Path to golden panel fixture JSON")
    parser.add_argument("--output-root", default=str(_default_output_root()), help="Root directory for golden run artifacts")
    parser.add_argument("--run-id", default=None, help="Output folder name (defaults to UTC timestamp)")
    parser.add_argument("--no-narrative", action="store_true", help="Skip writing narrative.txt")
    args = parser.parse_args()

    run_dir, result = run_golden_panel(
        fixture_path=Path(args.fixture),
        output_root=Path(args.output_root),
        run_id=args.run_id,
        write_narrative=not args.no_narrative,
    )
    status = str(result.get("status", "unknown"))
    error_type = str(result.get("error_type", "")).strip()
    if status == "error" and error_type == "canonical_collision":
        print(f"Golden panel run complete: {run_dir}")
        print("Status: error (canonical_collision)")
        return 2
    print(f"Golden panel run complete: {run_dir}")
    print(f"Status: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
