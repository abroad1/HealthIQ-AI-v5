"""
Sprint 12 - Production explainability + deterministic influence ordering tests.
"""

from core.analytics.explainability_builder import compute_influence_ordering
from core.contracts.arbitration_v1 import ArbitrationNode, CausalEdge, DominanceEdge
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import apply_unit_normalisation, UNIT_REGISTRY_VERSION


def _prepare_unit_normalised(biomarkers: dict) -> dict:
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def _seed_graph() -> InsightGraphV1:
    graph = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="ordering-test",
        system_states=[
            SystemStateNode(
                system_id="alpha",
                state_codes=["system_multi_marker_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="high",
            ),
            SystemStateNode(
                system_id="beta",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
            SystemStateNode(
                system_id="gamma",
                state_codes=["system_focal_derangement"],
                rationale_codes=[],
                transition_summary_codes=[],
                confidence_bucket="moderate",
            ),
        ],
        edges=[],
    )
    graph.primary_driver_system_id = "alpha"
    graph.arbitration_result = ArbitrationNode(
        supporting_system_ids=["gamma", "beta"],
        decision_trace_codes=["arb:seed"],
        tie_breaker_codes=[],
        rationale_codes=[],
    )
    graph.dominance_edges = [
        DominanceEdge(
            from_system_id="alpha",
            to_system_id="beta",
            rule_id="r1",
            conflict_id="c1",
            conflict_type="state_direction",
            precedence_tier=1,
            rationale_codes=[],
        ),
        DominanceEdge(
            from_system_id="alpha",
            to_system_id="gamma",
            rule_id="r2",
            conflict_id="c2",
            conflict_type="state_direction",
            precedence_tier=1,
            rationale_codes=[],
        ),
        DominanceEdge(
            from_system_id="beta",
            to_system_id="gamma",
            rule_id="r3",
            conflict_id="c3",
            conflict_type="state_direction",
            precedence_tier=2,
            rationale_codes=[],
        ),
    ]
    graph.causal_edges = [
        CausalEdge(
            edge_id="e1",
            from_system_id="alpha",
            to_system_id="beta",
            edge_type="driver",
            priority=9,
            rationale_codes=[],
            source_conflict_ids=["c1"],
        ),
        CausalEdge(
            edge_id="e2",
            from_system_id="beta",
            to_system_id="gamma",
            edge_type="amplifier",
            priority=6,
            rationale_codes=[],
            source_conflict_ids=["c3"],
        ),
        CausalEdge(
            edge_id="e3",
            from_system_id="gamma",
            to_system_id="beta",
            edge_type="constraint",
            priority=3,
            rationale_codes=[],
            source_conflict_ids=["c3"],
        ),
    ]
    return graph


def test_influence_ordering_is_deterministic_and_permutation_invariant():
    graph_a = _seed_graph()
    out_a1 = compute_influence_ordering(graph_a)
    out_a2 = compute_influence_ordering(graph_a)
    assert out_a1 == out_a2

    graph_b = _seed_graph()
    graph_b.system_states = list(reversed(graph_b.system_states))
    graph_b.dominance_edges = list(reversed(graph_b.dominance_edges))
    graph_b.causal_edges = list(reversed(graph_b.causal_edges))
    graph_b.arbitration_result = graph_b.arbitration_result.model_copy(
        update={"supporting_system_ids": ["beta", "gamma"]}
    )
    out_b = compute_influence_ordering(graph_b)
    assert out_a1["primary_driver_system_id"] == out_b["primary_driver_system_id"]
    assert out_a1["supporting_systems"] == out_b["supporting_systems"]
    assert out_a1["influence_order"] == out_b["influence_order"]


def test_production_pipeline_emits_explainability_and_driver_authority():
    orchestrator = AnalysisOrchestrator()
    prepared = _prepare_unit_normalised(
        {
            "glucose": {"value": 95.0, "unit": "mg/dL"},
            "hba1c": {"value": 5.4, "unit": "%"},
            "crp": {"value": 1.2, "unit": "mg/L"},
            "hdl_cholesterol": {"value": 55.0, "unit": "mg/dL"},
            "ldl_cholesterol": {"value": 110.0, "unit": "mg/dL"},
            "triglycerides": {"value": 140.0, "unit": "mg/dL"},
        }
    )
    user = {"user_id": "unit-s12", "age": 38, "gender": "male"}
    dto = orchestrator.run(prepared, user, assume_canonical=True)
    assert dto.status == "completed"
    assert dto.meta is not None
    explainability = dto.meta.get("explainability_report", {})
    insight_graph = dto.meta.get("insight_graph", {})
    assert explainability
    assert explainability.get("replay_stamps", {}).get("explainability_hash")
    assert explainability.get("replay_stamps", {}).get("burden_hash")
    assert insight_graph.get("influence_order")
    assert insight_graph.get("supporting_systems") is not None
    assert insight_graph.get("system_capacity_scores")
    assert insight_graph.get("burden_hash")
    assert dto.system_capacity_scores
    assert dto.burden_hash
    assert (
        insight_graph.get("primary_driver_system_id")
        == explainability.get("arbitration_decisions", {}).get("primary_driver_system_id")
        == dto.primary_driver_system_id
    )
