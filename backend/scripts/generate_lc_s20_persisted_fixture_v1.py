#!/usr/bin/env python3
"""Generate LC-S20 persisted replay fixture from AB launch-core baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input  # noqa: E402
from core.canonical.normalize import normalize_biomarkers_with_metadata  # noqa: E402
from core.dto.builders import build_analysis_result_dto  # noqa: E402
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY  # noqa: E402
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation  # noqa: E402


def _dump(obj: object) -> object:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [_dump(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _dump(v) for k, v in obj.items()}
    return obj


def main() -> int:
    panel_path = ROOT / "backend" / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    biomarkers = dict(panel["biomarkers"])
    for entry in biomarkers.values():
        if isinstance(entry, dict) and entry.get("unit") == "\u03bcmol/L":
            entry["unit"] = "\u00b5mol/L"
        rr = entry.get("reference_range")
        if isinstance(rr, dict) and rr.get("unit") == "\u03bcmol/L":
            rr["unit"] = "\u00b5mol/L"
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    dto = AnalysisOrchestrator().run(
        normalized,
        {"age": 45, "sex": "male"},
        assume_canonical=True,
        fixed_analysis_id="lc-s20-persisted-fixture-v1",
    )
    meta = dto.meta or {}
    raw = {
        "analysis_id": dto.analysis_id,
        "biomarkers": _dump(dto.biomarkers or []),
        "clusters": _dump(dto.clusters or []),
        "insights": _dump(dto.insights or []),
        "status": dto.status,
        "created_at": dto.created_at,
        "overall_score": dto.overall_score,
        "primary_driver_system_id": dto.primary_driver_system_id,
        "system_capacity_scores": dto.system_capacity_scores,
        "burden_hash": dto.burden_hash,
        "risk_assessment": meta.get("risk_assessment", {}),
        "recommendations": meta.get("recommendations", []),
        "result_version": "1.0.0",
        "derived_markers": _dump(dto.derived_markers),
        "meta": meta,
        "replay_manifest": _dump(dto.replay_manifest),
        "interpretation_display_layer_v1": _dump(dto.interpretation_display_layer_v1),
        "narrative_report_v1": _dump(dto.narrative_report_v1),
        "consumer_domain_scores": _dump(dto.consumer_domain_scores),
        "intervention_annotations_v1": _dump(dto.intervention_annotations_v1),
    }
    api = build_analysis_result_dto(raw)
    api = _dump(api)
    out = ROOT / "backend" / "tests" / "fixtures" / "persisted_results" / "lc_s20_ab_launch_core_v1.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(api, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "keys": len(api)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
