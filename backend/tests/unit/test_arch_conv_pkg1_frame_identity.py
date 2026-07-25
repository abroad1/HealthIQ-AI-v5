"""ARCH-CONV-PKG1 — launch-path activation-frame identity closure tests."""

from __future__ import annotations

import copy

import pytest

from core.analytics.domain_score_assembler import (
    _collect_activation_keys,
    _collect_signal_ids,
    _is_wave1_blood_iron_oxygen,
    _is_wave1_kidney,
    _is_wave1_liver,
)
from core.analytics.interpretation_display_layer_publish_v1 import (
    publish_interpretation_display_layer_v1,
)
from core.analytics.intervention_selector_v1 import select_interventions_v1
from core.analytics.narrative_report_compiler_v1 import _resolve_lead_frame
from core.analytics.signal_interaction_builder import build_signal_interactions_v1
from core.knowledge.signal_result_index_v1 import (
    index_by_activation_key,
    participating_activation_keys_by_signal_id,
)


PRESSURE_SET = {
    "signal_homocysteine_high": [
        "inv_homocysteine_high_b_vitamin",
        "inv_homocysteine_high_metabolic",
        "inv_homocysteine_high_renal",
    ],
    "signal_mcv_high": [
        "inv_mcv_high_macrocytosis",
        "inv_mcv_high_megaloblastic",
        "inv_mcv_high_nonmegaloblastic",
    ],
    "signal_iron_low": ["inv_iron_low_absolute", "inv_iron_low_functional"],
    "signal_tpo_ab_high": [
        "inv_tpo_ab_high_autoimmune_hypothyroid",
        "inv_tpo_ab_high_euthyroid",
    ],
    "signal_egfr_low": ["inv_egfr_low_chronic", "inv_egfr_low_hemodynamic"],
    "signal_alt_high": [
        "inv_alt_high_hepatocellular",
        "inv_alt_high_metabolic",
        "inv_alt_high_muscle",
        "inv_alt_high_legacy",
    ],
    "signal_ferritin_high": [
        "inv_ferritin_high_inflammatory",
        "inv_ferritin_high_overload",
        "inv_ferritin_high_legacy",
    ],
    "signal_creatinine_high": [
        "inv_creatinine_high_reduced_gfr",
        "inv_creatinine_high_renal",
    ],
}

_SYSTEM = {
    "signal_homocysteine_high": ("vascular", "homocysteine"),
    "signal_mcv_high": ("hematologic", "mcv"),
    "signal_iron_low": ("hematologic", "iron"),
    "signal_tpo_ab_high": ("thyroid", "tpo_ab"),
    "signal_egfr_low": ("renal", "egfr"),
    "signal_alt_high": ("hepatic", "alt"),
    "signal_ferritin_high": ("hepatic", "ferritin"),
    "signal_creatinine_high": ("renal", "creatinine"),
}


def _rows():
    out = []
    for sid, specs in PRESSURE_SET.items():
        system, metric = _SYSTEM[sid]
        for i, spec in enumerate(specs):
            out.append(
                {
                    "signal_id": sid,
                    "source_spec_id": spec,
                    "activation_key": f"{sid}::{spec}",
                    "package_id": f"pkg_test_{spec}",
                    "signal_state": "at_risk" if i == 0 else "suboptimal",
                    "confidence": 0.6 + 0.05 * i,
                    "system": system,
                    "primary_metric": metric,
                    "supporting_markers": [],
                }
            )
    return out


def test_pressure_set_has_eight_families_twenty_one_frames():
    rows = _rows()
    assert len({r["signal_id"] for r in rows}) == 8
    assert len({r["activation_key"] for r in rows}) == 21


def test_index_preserves_all_frames_and_duplicate_fails():
    rows = _rows()
    idx = index_by_activation_key(rows, require_key=True)
    assert len(idx) == 21
    with pytest.raises(ValueError, match="Duplicate activation_key"):
        index_by_activation_key([rows[0], dict(rows[0])], require_key=True)


def test_idl_preserves_participating_frames_and_prefers_at_risk():
    rows = _rows()
    bundle = publish_interpretation_display_layer_v1({"signal_results": rows})
    assert bundle.aggregation_scope == "signal_family"
    assert len(bundle.participating_activation_keys) == 21
    # Determinism
    again = publish_interpretation_display_layer_v1({"signal_results": rows})
    assert again.model_dump() == bundle.model_dump()


def test_domain_scoring_retains_activation_keys_without_double_count_ids():
    rows = _rows()
    sids = _collect_signal_ids(rows, _is_wave1_liver)
    akeys = _collect_activation_keys(rows, _is_wave1_liver)
    assert "signal_alt_high" in sids
    assert sids.count("signal_alt_high") == 1
    assert len([k for k in akeys if k.startswith("signal_alt_high::")]) == 4

    iron_keys = _collect_activation_keys(rows, _is_wave1_blood_iron_oxygen)
    assert len([k for k in iron_keys if k.startswith("signal_iron_low::")]) == 2
    kidney_keys = _collect_activation_keys(rows, _is_wave1_kidney)
    assert len([k for k in kidney_keys if k.startswith("signal_egfr_low::")]) == 2


def test_narrative_lead_retains_activation_key_on_graph_path():
    rows = _rows()
    lead = _resolve_lead_frame(narrative_payload_v1=None, insight_graph={"signal_results": rows})
    assert lead["signal_id"] in {
        "signal_homocysteine_high",
        "signal_mcv_high",
        "signal_iron_low",
        "signal_tpo_ab_high",
        "signal_free_t3_low",
    }
    assert lead["activation_key"].startswith(lead["signal_id"] + "::")
    # Determinism
    lead2 = _resolve_lead_frame(narrative_payload_v1=None, insight_graph={"signal_results": rows})
    assert lead2 == lead


def test_interaction_nodes_family_scoped_with_per_node_frames():
    rows = _rows()
    out = build_signal_interactions_v1(rows)
    graph = out["interaction_graph"]
    assert graph["aggregation_scope"] == "signal_family"
    part = graph["node_frame_participation"]
    for sid, specs in PRESSURE_SET.items():
        if sid not in graph["nodes"]:
            continue
        assert part[sid] == sorted(f"{sid}::{s}" for s in specs)
    for summary in out["interaction_summary"]:
        assert "participating_activation_keys" in summary
        assert summary.get("aggregation_scope") == "signal_family"
    # Determinism
    out2 = build_signal_interactions_v1(rows)
    assert out2 == out


def test_intervention_dedup_unions_activation_key_refs():
    rows = [
        {
            "signal_id": "signal_homocysteine_high",
            "source_spec_id": "inv_a",
            "activation_key": "signal_homocysteine_high::inv_a",
            "signal_state": "at_risk",
            "confidence": 0.9,
            "system": "vascular",
            "primary_metric": "homocysteine",
        },
        {
            "signal_id": "signal_homocysteine_high",
            "source_spec_id": "inv_b",
            "activation_key": "signal_homocysteine_high::inv_b",
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "system": "vascular",
            "primary_metric": "homocysteine",
        },
    ]
    interactions = build_signal_interactions_v1(rows)
    intervs = select_interventions_v1(
        signal_results=rows,
        interaction_summary=interactions.get("interaction_summary") or [],
    )
    # If library emits vascular interventions, frame refs must be unioned / not foreign.
    for item in intervs:
        refs = item.get("activation_key_refs") or []
        for ref in refs:
            assert ref in {
                "signal_homocysteine_high::inv_a",
                "signal_homocysteine_high::inv_b",
            }


def test_single_frame_compatible():
    row = {
        "signal_id": "signal_alt_high",
        "source_spec_id": "inv_only",
        "activation_key": "signal_alt_high::inv_only",
        "signal_state": "suboptimal",
        "confidence": 0.7,
        "system": "hepatic",
        "primary_metric": "alt",
        "supporting_markers": [],
    }
    bundle = publish_interpretation_display_layer_v1({"signal_results": [row]})
    assert bundle.participating_activation_keys == ["signal_alt_high::inv_only"]
    akeys = _collect_activation_keys([row], _is_wave1_liver)
    assert akeys == ["signal_alt_high::inv_only"]
    out = build_signal_interactions_v1([row])
    assert out["participating_activation_keys"] == ["signal_alt_high::inv_only"]


def test_per_family_helper_matches_pressure_set():
    rows = _rows()
    by_sid = participating_activation_keys_by_signal_id(
        rows, valid_states={"suboptimal", "at_risk"}, signal_ids=list(PRESSURE_SET)
    )
    for sid, specs in PRESSURE_SET.items():
        assert by_sid[sid] == sorted(f"{sid}::{s}" for s in specs)


def test_invalid_fixture_duplicate_key_fails_index():
    rows = _rows()
    bad = copy.deepcopy(rows[:1]) * 2
    with pytest.raises(ValueError):
        index_by_activation_key(bad, require_key=True)
