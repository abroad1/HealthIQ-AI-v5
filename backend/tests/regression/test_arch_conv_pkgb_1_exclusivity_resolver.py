"""ARCH-CONV-PKGB-1 — homocysteine exclusivity + bare-key resolver closure."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.knowledge.why_authority_v1 import (
    STATE_COMPILED_ACTIVE,
    STATE_LEGACY_RETIRED,
    clear_why_authority_cache,
    load_why_authority_register,
    resolve_frame_why_authority,
)

REPO = Path(__file__).resolve().parents[3]
ELEV = "signal_homocysteine_elevation_context::inv_elevation_context"
BVIT = (
    "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment"
)
RENAL = "signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction"

ZERO_COMPILED_PILOTS = (
    "signal_ldl_high",
    "signal_hdl_low",
    "signal_total_cholesterol_high",
    "signal_hgb_low",
    "signal_hepatic_alt_context",
)

LEGACY_ELEVATION_HYP_IDS = {
    "hcy_b12_pattern_v1",
    "hcy_folate_pattern_v1",
    "hcy_inflammation_context_v1",
    "hcy_renal_clearance_context_v1",
}


def _finding_by_signal(root, signal_id: str):
    if root is None:
        return None
    for finding in root.findings:
        if finding.signal_id == signal_id:
            return finding
    return None


def test_elevation_context_does_not_independently_emit_why():
    clear_why_authority_cache()
    mode, row = resolve_frame_why_authority(
        signal_id="signal_homocysteine_elevation_context",
        activation_key=ELEV,
    )
    assert mode == "skip"
    assert row is not None
    assert row["authority_state"] == STATE_LEGACY_RETIRED
    assert row.get("artefact_path") is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_elevation_context",
                "activation_key": ELEV,
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": {"value": 18.0}, "folate": {"value": 2.0}},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    assert _finding_by_signal(root, "signal_homocysteine_elevation_context") is None


def test_homocysteine_high_compiled_why_unchanged():
    clear_why_authority_cache()
    mode, row = resolve_frame_why_authority(
        signal_id="signal_homocysteine_high",
        activation_key=BVIT,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["authority_state"] == STATE_COMPILED_ACTIVE

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": BVIT,
                "source_spec_id": "inv_homocysteine_high_b_vitamin_related_methylation_impairment",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": {"value": 18.0}, "folate": {"value": 2.0}},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    finding = _finding_by_signal(root, "signal_homocysteine_high")
    assert finding is not None
    assert finding.activation_key == BVIT
    ids = {h.hypothesis_id for h in finding.hypotheses}
    assert "hyp_folate_related_hyperhomocysteinemia" in ids
    assert "hyp_b12_related_or_combined_methylation_impairment" in ids
    assert ids.isdisjoint(LEGACY_ELEVATION_HYP_IDS)


def test_dual_panel_emits_only_compiled_homocysteine_why():
    clear_why_authority_cache()
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_elevation_context",
                "activation_key": ELEV,
                "signal_state": "at_risk",
                "confidence": 0.85,
                "primary_metric": "homocysteine",
            },
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": BVIT,
                "source_spec_id": "inv_homocysteine_high_b_vitamin_related_methylation_impairment",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            },
        ],
        biomarker_context={
            "homocysteine": {"value": 18.0},
            "folate": {"value": 2.0},
            "vitamin_b12": {"value": 180.0},
        },
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    assert _finding_by_signal(root, "signal_homocysteine_elevation_context") is None
    high = _finding_by_signal(root, "signal_homocysteine_high")
    assert high is not None
    assert high.activation_key == BVIT
    all_ids = {h.hypothesis_id for f in (root.findings if root else []) for h in f.hypotheses}
    assert all_ids.isdisjoint(LEGACY_ELEVATION_HYP_IDS)


def test_no_legacy_path_restores_elevation_context_content():
    clear_why_authority_cache()
    # Bare elevation-context (no key) with only retired rows → skip, not legacy emit.
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_homocysteine_elevation_context",
        activation_key="",
    )
    assert mode == "skip"

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_elevation_context",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": {"value": 20.0}},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
    )
    assert _finding_by_signal(root, "signal_homocysteine_elevation_context") is None
    if root is not None:
        ids = {h.hypothesis_id for f in root.findings for h in f.hypotheses}
        assert ids.isdisjoint(LEGACY_ELEVATION_HYP_IDS)


@pytest.mark.parametrize("signal_id", ZERO_COMPILED_PILOTS)
def test_zero_compiled_pilot_bare_key_resolves_skip(signal_id: str):
    clear_why_authority_cache()
    mode, row = resolve_frame_why_authority(signal_id=signal_id, activation_key="")
    assert mode == "skip"
    assert row is not None
    assert row["authority_state"] == STATE_LEGACY_RETIRED

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": signal_id,
                "signal_state": "at_risk",
                "confidence": 0.7,
                "primary_metric": "probe",
            }
        ],
        biomarker_context={},
        input_reference_ranges={},
    )
    assert _finding_by_signal(root, signal_id) is None


def test_total_cholesterol_remains_non_owning_no_invented_compiled_why():
    clear_why_authority_cache()
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_total_cholesterol_high",
        activation_key="",
    )
    assert mode == "skip"
    reg = load_why_authority_register()
    compiled = [
        r
        for r in reg["_by_activation_key"].values()
        if str(r.get("signal_id")) == "signal_total_cholesterol_high"
        and str(r.get("authority_state")) == STATE_COMPILED_ACTIVE
    ]
    assert compiled == []


def test_genuine_ambiguity_still_fail_closed():
    clear_why_authority_cache()
    # Multi COMPILED_ACTIVE bare key remains fail_closed.
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_homocysteine_high",
        activation_key="",
    )
    assert mode == "fail_closed"
    with pytest.raises(ValueError, match="fail-closed"):
        compile_root_cause_v1(
            signal_results=[
                {
                    "signal_id": "signal_homocysteine_high",
                    "signal_state": "at_risk",
                    "confidence": 0.7,
                    "primary_metric": "homocysteine",
                }
            ],
            biomarker_context={"homocysteine": {"value": 18.0}},
            input_reference_ranges={"homocysteine": {"min": 5.0, "max": 15.0}},
        )


def test_missing_governance_still_fail_closed():
    clear_why_authority_cache()
    # Pilot signal with no register rows for that id — use a synthetic pilot-only path
    # by resolving a known pilot id with a bogus key (missing row).
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_vitamin_d_low",
        activation_key="signal_vitamin_d_low::inv_does_not_exist",
    )
    assert mode == "fail_closed"


def test_hba1c_and_urate_ratified_hypothesis_ids():
    clear_why_authority_cache()
    hba1c_root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hba1c_high",
                "activation_key": "signal_hba1c_high::inv_hba1c_high_glycaemia",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "hba1c",
            }
        ],
        biomarker_context={"hba1c": {"value": 48.0}},
        input_reference_ranges={"hba1c": {"min": 20.0, "max": 42.0}},
    )
    hba1c = _finding_by_signal(hba1c_root, "signal_hba1c_high")
    assert hba1c is not None
    assert "hyp_hba1c_elevated_glycaemia_context" in {
        h.hypothesis_id for h in hba1c.hypotheses
    }

    urate_root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_urate_high",
                "activation_key": "signal_urate_high::inv_uric_acid_high_metabolic",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "urate",
            }
        ],
        biomarker_context={"urate": {"value": 480.0}},
        input_reference_ranges={"urate": {"min": 200.0, "max": 420.0}},
    )
    urate = _finding_by_signal(urate_root, "signal_urate_high")
    assert urate is not None
    assert "hyp_urate_elevated_non_causal_context" in {
        h.hypothesis_id for h in urate.hypotheses
    }


def test_package_activation_and_shared_asset_unchanged():
    """Package reachability + shared YAML remain; exclusivity is WHY-only."""
    activation = yaml.safe_load(
        (REPO / "knowledge_bus/governance/package_runtime_activation_register_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    keys = {
        str(row.get("activation_key") or "").strip()
        for row in (activation.get("activated_frames") or activation.get("frames") or [])
        if isinstance(row, dict)
    }
    # Support either register shape used historically.
    if not keys:
        for row in activation.get("activated") or []:
            if isinstance(row, dict):
                keys.add(str(row.get("activation_key") or "").strip())
    # Direct scan of file text as fail-soft if structure differs.
    text = (
        REPO / "knowledge_bus/governance/package_runtime_activation_register_v1.yaml"
    ).read_text(encoding="utf-8")
    assert "signal_homocysteine_elevation_context::inv_elevation_context" in text
    assert "pkg_homocysteine_elevation_context" in text
    shared = REPO / "knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml"
    assert shared.is_file()
    payload = yaml.safe_load(shared.read_text(encoding="utf-8"))
    assert payload.get("primary_signal_id") == "signal_homocysteine_elevation_context"


def test_register_delta_adds_only_elevation_context_retirement():
    clear_why_authority_cache()
    reg = load_why_authority_register()
    row = reg["_by_activation_key"][ELEV]
    assert row["authority_state"] == STATE_LEGACY_RETIRED
    assert row.get("artefact_path") is None
    # Compiled hcy-high rows unchanged in count/state.
    assert (
        reg["_by_activation_key"][BVIT]["authority_state"] == STATE_COMPILED_ACTIVE
    )
    assert (
        reg["_by_activation_key"][RENAL]["authority_state"] == STATE_COMPILED_ACTIVE
    )
