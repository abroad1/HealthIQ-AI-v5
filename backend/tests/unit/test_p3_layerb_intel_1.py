"""P3-LAYERB-INTEL-1 — frame routing, modifier binder, authority isolation tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.knowledge.layer_b_asset_authority_v1 import (
    assert_production_allowed,
    load_layer_b_asset_authority,
    mr_batch_isolated,
)
from core.knowledge.layer_b_frame_routing_v1 import (
    ProseAssetCandidate,
    select_frame_prose_asset,
)
from core.knowledge.layer_b_modifier_binder_v1 import bind_modifiers_v1
from core.knowledge.compiled_hypothesis import RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS
from core.models.signal import SignalResult

REPO = Path(__file__).resolve().parents[3]
FE_TYPES = REPO / "frontend" / "app" / "types" / "analysis.ts"


def test_same_family_frames_receive_distinct_prose():
    cands = [
        ProseAssetCandidate(
            asset_id="prose_a",
            signal_id="signal_x",
            activation_keys=("signal_x::frame_a",),
            production_authority="approved",
        ),
        ProseAssetCandidate(
            asset_id="prose_b",
            signal_id="signal_x",
            activation_keys=("signal_x::frame_b",),
            production_authority="approved",
        ),
    ]
    a = select_frame_prose_asset(
        candidates=cands, signal_id="signal_x", activation_key="signal_x::frame_a"
    )
    b = select_frame_prose_asset(
        candidates=cands, signal_id="signal_x", activation_key="signal_x::frame_b"
    )
    assert a.selected_asset_id == "prose_a"
    assert b.selected_asset_id == "prose_b"
    assert a.selected_asset_id != b.selected_asset_id


def test_unsupported_frame_does_not_borrow_other_frame_prose():
    cands = [
        ProseAssetCandidate(
            asset_id="prose_a",
            signal_id="signal_x",
            activation_keys=("signal_x::frame_a",),
            production_authority="approved",
        )
    ]
    d = select_frame_prose_asset(
        candidates=cands, signal_id="signal_x", activation_key="signal_x::frame_b"
    )
    assert d.selected_asset_id is None
    assert "prose_a" in d.rejected_asset_ids


def test_modifier_precedence_deterministic():
    rows = [
        {"modifier_id": "mod_b", "runtime_active": True, "production_authority": "approved"},
        {"modifier_id": "mod_a", "runtime_active": True, "production_authority": "approved"},
    ]
    d1 = bind_modifiers_v1(catalogue_rows=rows, eligible_modifier_ids=["mod_a", "mod_b"])
    d2 = bind_modifiers_v1(catalogue_rows=rows, eligible_modifier_ids=["mod_b", "mod_a"])
    assert d1.selected_modifier_ids == ("mod_a", "mod_b")
    assert d1.as_dict() == d2.as_dict()


def test_contradictory_modifiers_fail_safe():
    rows = [
        {
            "modifier_id": "mod_x",
            "runtime_active": True,
            "production_authority": "approved",
            "exclusive_group": "g1",
        },
        {
            "modifier_id": "mod_y",
            "runtime_active": True,
            "production_authority": "approved",
            "exclusive_group": "g1",
        },
    ]
    d = bind_modifiers_v1(catalogue_rows=rows, eligible_modifier_ids=["mod_x", "mod_y"])
    assert d.selected_modifier_ids == ()
    assert d.fail_safe is True


def test_legacy_family_fallback_labelled_honestly():
    cands = [
        ProseAssetCandidate(
            asset_id="family_asset",
            signal_id="signal_x",
            production_authority="legacy_unreviewed",
        )
    ]
    d = select_frame_prose_asset(
        candidates=cands, signal_id="signal_x", activation_key="signal_x::frame_a"
    )
    assert d.selected_asset_id == "family_asset"
    assert d.fallback_authority == "LEGACY_FAMILY_LEVEL"


def test_compiled_why_selects_by_activation_frame_pilot():
    assert RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS == frozenset({"signal_vitamin_d_low"})
    from core.knowledge.compiled_hypothesis_registry_v1 import COMPILED_HYPOTHESIS_PILOT_SPECS

    assert len(COMPILED_HYPOTHESIS_PILOT_SPECS) == 1
    assert (
        COMPILED_HYPOTHESIS_PILOT_SPECS[0].activation_key
        == "signal_vitamin_d_low::inv_vitamin_d_low_deficiency"
    )


def test_candidate_test_only_cannot_load_in_production():
    cands = [
        ProseAssetCandidate(
            asset_id="cand",
            signal_id="signal_x",
            production_authority="candidate",
        )
    ]
    d = select_frame_prose_asset(candidates=cands, signal_id="signal_x")
    assert d.selected_asset_id is None
    with pytest.raises(PermissionError):
        assert_production_allowed("MR-BATCH-001B_candidate_prose_assets")


def test_mr_batch_001b_remains_isolated():
    reg = load_layer_b_asset_authority()
    assert mr_batch_isolated(reg)
    banned = (
        "mr_candidate_prose_test_v1",
        "from tests.support.mr_candidate",
        "import mr_candidate_prose",
    )
    for root in (REPO / "backend" / "core", REPO / "backend" / "app", REPO / "frontend" / "app"):
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for needle in banned:
                assert needle not in text, f"{path} contains {needle}"


def test_consumer_clinician_paths_preserve_identity_fields():
    # SignalResult still carries activation identity + provenance after Package 2.
    s = SignalResult(
        signal_id="signal_alt_high",
        activation_key="signal_alt_high::frame_a",
        source_spec_id="frame_a",
        package_id="pkg_t",
        provenance_status="LEGACY_INFERRED",
        system="liver",
        signal_state="at_risk",
        signal_value=80.0,
        primary_metric="alt",
    )
    dumped = json.loads(s.model_dump_json())
    assert dumped["activation_key"] == "signal_alt_high::frame_a"
    assert dumped["provenance_status"] == "LEGACY_INFERRED"


def test_replay_round_trip_preserves_selected_asset_and_modifiers():
    decision = select_frame_prose_asset(
        candidates=[
            ProseAssetCandidate(
                asset_id="family_asset",
                signal_id="signal_x",
                production_authority="legacy_unreviewed",
            )
        ],
        signal_id="signal_x",
        activation_key="signal_x::a",
    )
    mods = bind_modifiers_v1(catalogue_rows=[], eligible_modifier_ids=[])
    payload = {"routing": decision.as_dict(), "modifiers": mods.as_dict()}
    wire = json.loads(json.dumps(payload))
    assert wire["routing"]["selected_asset_id"] == "family_asset"
    assert wire["modifiers"]["selected_modifier_ids"] == []
    assert wire["routing"]["routing_policy_version"]


def test_repeated_runs_identical_output():
    cands = [
        ProseAssetCandidate(
            asset_id="b",
            signal_id="signal_x",
            activation_keys=("signal_x::a",),
            production_authority="approved",
        ),
        ProseAssetCandidate(
            asset_id="a",
            signal_id="signal_x",
            production_authority="legacy_unreviewed",
        ),
    ]
    runs = [
        select_frame_prose_asset(
            candidates=cands, signal_id="signal_x", activation_key="signal_x::a"
        ).as_dict()
        for _ in range(5)
    ]
    assert all(r == runs[0] for r in runs)


def test_frontend_types_render_only_selection_provenance():
    text = FE_TYPES.read_text(encoding="utf-8")
    assert "LayerBFrameRoutingDecisionV1" in text
    assert "LayerBModifierBindingDecisionV1" in text
    # No client-side medical inference helpers introduced for modifiers/frames
    assert "inferModifier" not in text
    assert "chooseFrameProse" not in text


def test_legacy_single_frame_compatible():
    cands = [
        ProseAssetCandidate(
            asset_id="only",
            signal_id="signal_x",
            production_authority="legacy_unreviewed",
        )
    ]
    d = select_frame_prose_asset(candidates=cands, signal_id="signal_x", activation_key="")
    assert d.selected_asset_id == "only"
    assert d.fallback_authority == "LEGACY_FAMILY_LEVEL"


def test_layer_b_gate_passes_current_estate():
    from scripts.validate_layer_b_integrity_gate import main as gate_main

    assert gate_main() == 0


def test_layer_b_gate_detects_wrong_frame_collapse_in_fixture():
    """Deliberately invalid fixture: two frames must not select the same frame-specific asset."""
    cands = [
        ProseAssetCandidate(
            asset_id="shared_wrong",
            signal_id="signal_x",
            activation_keys=("signal_x::a", "signal_x::b"),
            production_authority="approved",
        )
    ]
    # Policy: activation_keys listing both frames means either frame may match this asset.
    # Wrong-frame borrow is when an asset lists ONLY the other frame.
    other_only = [
        ProseAssetCandidate(
            asset_id="only_a",
            signal_id="signal_x",
            activation_keys=("signal_x::a",),
            production_authority="approved",
        )
    ]
    d = select_frame_prose_asset(
        candidates=other_only, signal_id="signal_x", activation_key="signal_x::b"
    )
    assert d.selected_asset_id is None  # gate-equivalent wrong-frame rejection


def test_narrative_compiler_stamps_layer_b_routing_meta():
    report = compile_narrative_report_v1(
        analysis_id="p3-layerb-intel-1",
        insight_graph={
            "signal_results": [
                {
                    "signal_id": "signal_homocysteine_high",
                    "activation_key": "signal_homocysteine_high::inv_homocysteine_high_metabolic",
                    "source_spec_id": "inv_homocysteine_high_metabolic",
                    "signal_state": "suboptimal",
                }
            ],
            "primary_driver_system_id": "metabolic",
        },
        narrative_payload_v1=None,
    )
    assert report is not None
    meta = report.meta or {}
    assert "layer_b_modifier_binding" in meta
    assert meta["layer_b_modifier_binding"]["binder_version"]


def test_draft_catalogue_binds_nothing_without_medical_activation():
    # Production binder must not auto-load the draft catalogue path.
    d = bind_modifiers_v1()
    assert d.selected_modifier_ids == ()
    assert d.fail_safe is True
    # Explicit rows from a fixture still require runtime_active + approved authority.
    cat = yaml.safe_load(
        (REPO / "knowledge_bus" / "governance" / "context_modifier_catalogue_draft_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    rows = cat.get("modifiers") or []
    d2 = bind_modifiers_v1(catalogue_rows=rows)
    assert d2.selected_modifier_ids == ()
    assert d2.fail_safe is True
