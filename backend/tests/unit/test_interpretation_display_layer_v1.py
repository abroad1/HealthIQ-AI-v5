"""BE-IDL-1 — IDL registry, publisher, and governance tests."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.interpretation_display_layer_governance_v1 import (
    validate_interpretation_display_layer_bundle_v1,
)
from core.analytics.interpretation_display_layer_publish_v1 import (
    load_idl_registry_document,
    load_phenotype_required_signals_by_id,
    publish_interpretation_display_layer_v1,
)


def test_idl_registry_has_nine_records_aligned_with_phenotype_map():
    schema_ver, rows = load_idl_registry_document()
    assert schema_ver
    assert len(rows) == 11
    required_map = load_phenotype_required_signals_by_id()
    ids = {str(r.get("internal_id", "")).strip() for r in rows}
    assert len(ids) == 11
    for rid in ids:
        assert rid in required_map, f"missing phenotype_map entry for {rid}"
        assert required_map[rid], f"empty required_signals for {rid}"


def test_idl_governance_passes_on_published_empty_graph():
    bundle = publish_interpretation_display_layer_v1({})
    errs = validate_interpretation_display_layer_bundle_v1(bundle)
    assert errs == [], errs


def test_idl_partial_match_emits_watch_severity():
    bundle = publish_interpretation_display_layer_v1(
        {
            "signal_results": [
                {
                    "signal_id": "signal_triglycerides_high",
                    "signal_state": "suboptimal",
                    "primary_metric": "triglycerides",
                    "supporting_markers": [],
                }
            ]
        }
    )
    # ph_metabolic_early_ir_v1 requires TG + lipid transport + HDL — partial → watch if any required fire
    metabolic = next(r for r in bundle.records if r.internal_id == "ph_metabolic_early_ir_v1")
    assert metabolic.severity_state == "watch"
    assert metabolic.enabled_for_frontend is True


def test_idl_design_lock_yaml_exists():
    path = (
        Path(__file__).resolve().parents[3]
        / "docs"
        / "strategy"
        / "Interpretation_Display_Layer_Design_Lock.md"
    )
    assert path.is_file()


def test_idl_registry_yaml_parseable():
    root = Path(__file__).resolve().parents[3]
    raw = yaml.safe_load(
        (root / "knowledge_bus" / "interpretation_display_layer_v1" / "idl_records_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert raw.get("schema_version")
    assert len(raw.get("records") or []) == 11
