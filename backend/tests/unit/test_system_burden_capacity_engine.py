"""
Sprint 13 - deterministic burden/capacity engine tests.
"""

from core.analytics.capacity_scaler import scale_capacity_scores_v1
from core.analytics.bio_stats_engine import build_bio_stats_v1
from core.analytics.influence_propagator import propagate_influence_v1
from core.analytics.system_burden_engine import (
    ALLOWED_RISK_DIRECTIONS,
    audit_risk_direction_registry,
    build_raw_system_burden_v1,
    load_burden_registry,
)
from core.analytics.validation_gate import compute_burden_hash, run_validation_gate_v1


def test_direction_aware_components_hdl_and_crp():
    audited = {
        "hdl_cholesterol": {"risk_direction": "LOW_IS_RISK", "weight": 1.0},
        "crp": {"risk_direction": "HIGH_IS_RISK", "weight": 1.0},
    }
    stats = {
        "hdl_cholesterol": {"z_score": -1.5, "clamped": False},
        "crp": {"z_score": 2.0, "clamped": False},
    }
    raw = build_raw_system_burden_v1(
        system_to_biomarkers={"sys_a": ["crp", "hdl_cholesterol"]},
        biomarker_stats=stats,
        audited_registry=audited,
    )
    assert raw["sys_a"] == 3.5


def test_bio_stats_formula_and_clamp():
    stats = build_bio_stats_v1(
        biomarker_values={"x": {"value": 200.0}},
        lab_reference_ranges={"x": {"min": 0.0, "max": 100.0}},
    )
    assert stats["x"]["z_score"] == 3.0
    assert stats["x"]["clamped"] is False
    clamped = build_bio_stats_v1(
        biomarker_values={"x": {"value": 999.0}},
        lab_reference_ranges={"x": {"min": 0.0, "max": 100.0}},
    )
    assert clamped["x"]["z_score"] == 4.0
    assert clamped["x"]["clamped"] is True


def test_permutation_invariance_of_raw_burden():
    audited = {
        "a": {"risk_direction": "HIGH_IS_RISK", "weight": 0.5},
        "b": {"risk_direction": "LOW_IS_RISK", "weight": 0.5},
        "c": {"risk_direction": "BOTH_SIDES_RISK", "weight": 0.5},
    }
    stats = {
        "a": {"z_score": 2.0, "clamped": False},
        "b": {"z_score": -2.0, "clamped": False},
        "c": {"z_score": -1.0, "clamped": False},
    }
    one = build_raw_system_burden_v1(
        system_to_biomarkers={"sys": ["a", "b", "c"]},
        biomarker_stats=stats,
        audited_registry=audited,
    )
    two = build_raw_system_burden_v1(
        system_to_biomarkers={"sys": ["c", "b", "a"]},
        biomarker_stats=stats,
        audited_registry=audited,
    )
    assert one == two


def test_capacity_scaler_perfect_and_extreme_panels():
    perfect = scale_capacity_scores_v1(adjusted_system_burden_vector={"sys": 0.0})
    extreme = scale_capacity_scores_v1(adjusted_system_burden_vector={"sys": 100.0})
    assert perfect["sys"] == 100
    assert extreme["sys"] == 0


def test_influence_damping_changes_when_edge_removed():
    raw = {"driver": 4.0, "support": 4.0}
    adjusted_with_edge, _ = propagate_influence_v1(
        raw_system_burden_vector=raw,
        primary_driver_system_id="driver",
        causal_edges=[{"from_system_id": "driver", "to_system_id": "support"}],
    )
    adjusted_without_edge, _ = propagate_influence_v1(
        raw_system_burden_vector=raw,
        primary_driver_system_id="driver",
        causal_edges=[],
    )
    assert adjusted_with_edge["support"] == 2.0
    assert adjusted_without_edge["support"] == 0.0


def test_zero_path_damping_yields_zero_adjusted_and_capacity_100():
    raw = {"driver": 3.0, "isolated": 3.0}
    adjusted, distances = propagate_influence_v1(
        raw_system_burden_vector=raw,
        primary_driver_system_id="driver",
        causal_edges=[],
    )
    capacity = scale_capacity_scores_v1(adjusted_system_burden_vector=adjusted)
    assert distances["isolated"] == float("inf")
    assert adjusted["isolated"] == 0.0
    assert capacity["isolated"] == 100


def test_validation_gate_failure_injection_detects_hash_mismatch():
    adjusted = {"driver": 2.0, "support": 1.0}
    capacity = {"driver": 75, "support": 88}
    result = run_validation_gate_v1(
        insight_graph_system_ids=["driver", "support"],
        primary_driver_system_id="driver",
        supporting_systems=["support"],
        influence_order=["driver", "support"],
        path_distances={"driver": 0.0, "support": 1.0},
        adjusted_system_burden_vector=adjusted,
        system_capacity_scores=capacity,
        burden_hash="intentionally_wrong_hash",
    )
    assert result.status == "FAIL"
    assert "burden_hash_mismatch" in result.violations


def test_registry_integrity_no_contextual_and_no_missing_direction():
    registry = load_burden_registry()
    required = sorted(registry.keys())
    audited = audit_risk_direction_registry(required_biomarkers=required, registry_rows=registry)
    assert sorted(audited.keys()) == required
    for biomarker_id in required:
        direction = audited[biomarker_id]["risk_direction"]
        assert direction in ALLOWED_RISK_DIRECTIONS
        assert direction != "CONTEXTUAL"
