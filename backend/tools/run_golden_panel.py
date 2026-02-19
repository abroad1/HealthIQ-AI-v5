"""
v5.3 Sprint 6 - GoldenPanelRunner_v1 + Intelligence Snapshot Pack.

Evaluation harness only. Uses existing runtime pipeline without changing biological logic.
"""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from core.canonical.normalize import normalize_biomarkers_with_metadata
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


def run_golden_panel(
    fixture_path: Optional[Path] = None,
    output_root: Optional[Path] = None,
    run_id: Optional[str] = None,
    write_narrative: bool = True,
) -> Tuple[Path, Dict[str, Any]]:
    fixture = fixture_path or _default_fixture_path()
    out_root = output_root or _default_output_root()
    payload = _read_payload(fixture)

    biomarkers = normalize_biomarkers_with_metadata(payload["biomarkers"])
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
    replay_manifest = analysis_result.get("replay_manifest", {}) if isinstance(analysis_result, dict) else {}

    run_dir = _ensure_run_dir(out_root, run_id)
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
    print(f"Golden panel run complete: {run_dir}")
    print(f"Status: {result.get('status', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
