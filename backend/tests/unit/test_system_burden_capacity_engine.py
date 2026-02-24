"""
Sprint 13 - deterministic burden/capacity engine tests.
"""

from core.analytics.capacity_scaler import scale_capacity_scores_v1
from core.analytics.bio_stats_engine import build_bio_stats_v1
from core.analytics.influence_propagator import propagate_influence_v1
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.analytics.system_burden_engine import (
    ALLOWED_RISK_DIRECTIONS,
    ALLOWED_BURDEN_SYSTEM_IDS,
    audit_burden_registry_system_ids,
    audit_risk_direction_registry,
    build_raw_system_burden_v1,
    load_burden_registry,
)
from core.analytics.validation_gate import compute_burden_hash, run_validation_gate_v1
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation


class _EmptySession:
    def query(self, *args, **kwargs):
        return self

    def join(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return []


def _prepare_unit_normalised(biomarkers: dict) -> dict:
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


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


def test_influence_reachability_thyroid_to_core_system_is_finite():
    raw = {"thyroid": 3.0, "metabolic": 3.0, "cardiovascular": 3.0}
    _, distances = propagate_influence_v1(
        raw_system_burden_vector=raw,
        primary_driver_system_id="thyroid",
        causal_edges=[
            {"from_system_id": "thyroid", "to_system_id": "metabolic"},
            {"from_system_id": "metabolic", "to_system_id": "cardiovascular"},
        ],
    )
    assert distances["metabolic"] == 1.0
    assert distances["cardiovascular"] == 2.0


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
    systems = audit_burden_registry_system_ids(registry_rows=registry)
    assert "thyroid" in systems
    audited = audit_risk_direction_registry(required_biomarkers=required, registry_rows=registry)
    assert sorted(audited.keys()) == required
    for biomarker_id in required:
        direction = audited[biomarker_id]["risk_direction"]
        assert direction in ALLOWED_RISK_DIRECTIONS
        assert direction != "CONTEXTUAL"


def test_burden_registry_accepts_thyroid_system_id():
    registry = load_burden_registry()
    systems = audit_burden_registry_system_ids(registry_rows=registry)
    assert "thyroid" in systems


def test_burden_registry_rejects_unknown_system_id():
    registry = load_burden_registry()
    mutated = {k: dict(v) for k, v in registry.items()}
    mutated["glucose"]["system"] = "made_up"
    try:
        audit_burden_registry_system_ids(registry_rows=mutated)
        assert False, "Expected ValueError for unknown burden registry system id"
    except ValueError as exc:
        text = str(exc)
        assert "unknown system ids in burden registry" in text
        assert "glucose:made_up" in text
        for sid in sorted(ALLOWED_BURDEN_SYSTEM_IDS):
            assert sid in text


def test_orchestrator_scores_thyroid_and_immune_abs_markers_deterministically():
    orchestrator = AnalysisOrchestrator(db_session=_EmptySession())
    prepared = _prepare_unit_normalised(
        {
            "glucose": {
                "value": 140.0,
                "unit": "mg/dL",
                "reference_range": {"min": 70.0, "max": 100.0, "unit": "mg/dL", "source": "lab"},
            },
            "tsh": {
                "value": 6.0,
                "unit": "mIU/L",
                "reference_range": {"min": 0.4, "max": 4.5, "unit": "mIU/L", "source": "lab"},
            },
            "free_t4": {
                "value": 0.7,
                "unit": "ng/dL",
                "reference_range": {"min": 0.8, "max": 1.8, "unit": "ng/dL", "source": "lab"},
            },
            "tgab": {
                "value": 80.0,
                "unit": "IU/mL",
                "reference_range": {"min": 0.0, "max": 4.0, "unit": "IU/mL", "source": "lab"},
            },
            "neutrophils_abs": {
                "value": 9.0,
                "unit": "10^9/L",
                "reference_range": {"min": 2.0, "max": 7.5, "unit": "10^9/L", "source": "lab"},
            },
            "lymphocytes_abs": {
                "value": 0.8,
                "unit": "10^9/L",
                "reference_range": {"min": 1.0, "max": 3.0, "unit": "10^9/L", "source": "lab"},
            },
        }
    )
    user = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "age": 40,
        "gender": "female",
        "lifestyle_factors": {},
    }
    dto_a = orchestrator.run(dict(prepared), user, assume_canonical=True)
    dto_b = orchestrator.run(dict(prepared), user, assume_canonical=True)
    assert dto_a.status == "completed"
    assert dto_b.status == "completed"
    meta_a = dto_a.meta or {}
    meta_b = dto_b.meta or {}
    burden_a = meta_a.get("burden_vector", {})
    burden_b = meta_b.get("burden_vector", {})
    raw_a = burden_a.get("raw_system_burden_vector", {})
    assert "thyroid" in raw_a
    assert "immune" in raw_a
    assert float(raw_a["thyroid"]) > 0.0
    assert float(raw_a["immune"]) > 0.0
    assert str(burden_a.get("burden_hash", "")) == str(burden_b.get("burden_hash", ""))


def test_orchestrator_no_ranges_completes_with_empty_burden_contract():
    orchestrator = AnalysisOrchestrator(db_session=_EmptySession())
    prepared = _prepare_unit_normalised(
        {
            "glucose": {
                "value": 95.0,
                "unit": "mg/dL",
            },
        }
    )
    user = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "age": 30,
        "gender": "male",
    }
    dto_a = orchestrator.run(dict(prepared), user, assume_canonical=True)
    dto_b = orchestrator.run(dict(prepared), user, assume_canonical=True)
    assert dto_a.status == "completed"
    assert dto_b.status == "completed"
    burden_a = (dto_a.meta or {}).get("burden_vector", {})
    burden_b = (dto_b.meta or {}).get("burden_vector", {})
    assert burden_a.get("raw_system_burden_vector", None) == {}
    assert burden_a.get("adjusted_system_burden_vector", None) == {}
    assert burden_a.get("system_capacity_scores", None) == {}
    assert "unknown" not in burden_a.get("raw_system_burden_vector", {})
    assert "unknown" not in burden_a.get("adjusted_system_burden_vector", {})
    assert str(burden_a.get("burden_hash", "")) == str(burden_b.get("burden_hash", ""))
