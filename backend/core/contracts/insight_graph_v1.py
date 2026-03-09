"""
Sprint 7 - InsightGraph v1 Contract.

Strict output object between Layer B (deterministic) and Layer C (narrative).
LLM receives ONLY this object. No raw biomarkers, no local computation.

PRD §4.6, §4.7; Delivery Plan Sprint 7.
Sprint 8: Added confidence field (ConfidenceModel_v1).
"""

from typing import Dict, List, Any, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, Field
from core.contracts.relationship_registry_v1 import RelationshipDetection
from core.contracts.biomarker_context_v1 import BiomarkerContextNode
from core.contracts.state_transition_v1 import BiomarkerTransitionNode
from core.contracts.state_engine_v1 import SystemStateNode
from core.contracts.precedence_engine_v1 import PrecedenceOutput
from core.contracts.calibration_layer_v1 import CalibrationItem
from core.contracts.arbitration_v1 import (
    ArbitrationNode,
    ConflictItem,
    DominanceEdge,
    CausalEdge,
)

if TYPE_CHECKING:
    from core.contracts.confidence_model_v1 import ConfidenceModelV1

# Version stamp for replay determinism
INSIGHTGRAPH_V1_VERSION = "1.0.0"


class BiomarkerNode(BaseModel):
    """
    Single biomarker node in InsightGraph.

    PRD §4.7: No raw values, units, or reference ranges. Only interpreted outputs.
    """

    biomarker_id: str
    status: str = "unknown"  # low | normal | high | elevated | critical | unknown
    score: Optional[float] = None  # 0-100, already computed by Layer B


class ClusterSummaryItem(BaseModel):
    """Per-cluster status summary."""

    cluster_id: str
    complete: bool
    required_present: List[str]
    required_missing: List[str]
    confidence: float


class MetabolicAgeFeatureV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metabolic_age: float = 0.0
    age_delta_years: float = 0.0
    homa_ir: float = 0.0
    severity: str = "normal"
    confidence: float = 0.0
    risk_flags: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class HeartFeatureV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    heart_resilience_score: float = 0.0
    severity: str = "normal"
    confidence: float = 0.0
    risk_factors: List[str] = Field(default_factory=list)
    ldl_hdl_ratio: Optional[float] = None
    tc_hdl_ratio: Optional[float] = None
    tg_hdl_ratio: Optional[float] = None
    recommendations: List[str] = Field(default_factory=list)


class InflammationFeatureV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inflammation_burden_score: float = 0.0
    severity: str = "normal"
    confidence: float = 0.0
    risk_factors: List[str] = Field(default_factory=list)
    nlr: Optional[float] = None
    recommendations: List[str] = Field(default_factory=list)


class FatigueFeatureV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    severity: str = "normal"
    confidence: float = 0.0
    root_causes: List[str] = Field(default_factory=list)
    iron_status: str = "unknown"
    thyroid_status: str = "unknown"
    vitamin_status: str = "unknown"
    inflammation_status: str = "unknown"
    cortisol_status: str = "unknown"
    recommendations: List[str] = Field(default_factory=list)


class DetoxFeatureV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detox_filtration_score: float = 0.0
    liver_score: float = 0.0
    kidney_score: float = 0.0
    severity: str = "normal"
    confidence: float = 0.0
    risk_factors: List[str] = Field(default_factory=list)
    egfr: Optional[float] = None
    egfr_source: str = "unknown"
    urea_creatinine_ratio: Optional[float] = None
    recommendations: List[str] = Field(default_factory=list)


class LayerCFeatureBundleV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metabolic_age: MetabolicAgeFeatureV1 = Field(default_factory=MetabolicAgeFeatureV1)
    heart_insight: HeartFeatureV1 = Field(default_factory=HeartFeatureV1)
    inflammation: InflammationFeatureV1 = Field(default_factory=InflammationFeatureV1)
    fatigue_root_cause: FatigueFeatureV1 = Field(default_factory=FatigueFeatureV1)
    detox_filtration: DetoxFeatureV1 = Field(default_factory=DetoxFeatureV1)


class InsightGraphV1(BaseModel):
    """
    InsightGraph v1 — sole input to LLM/narrative layer.

    Deterministic, JSON-serialisable, version-stamped.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    graph_version: str = Field(default=INSIGHTGRAPH_V1_VERSION, description="Contract version")
    analysis_id: str = Field(default="", description="Analysis identifier")

    # Lab origin (Sprint 2)
    lab_origin: Optional[Dict[str, Any]] = Field(default=None, description="Lab provider metadata")

    # Unit normalisation (Sprint 1)
    unit_normalisation_meta: Optional[Dict[str, Any]] = Field(default=None)

    # Derived markers (Sprint 5)
    derived_markers: Optional[Dict[str, Any]] = Field(
        default=None,
        description="registry_version + derived dict"
    )

    # Cluster summary (Sprint 6)
    cluster_summary: Optional[Dict[str, Any]] = Field(
        default=None,
        description="schema_version, schema_hash, clusters list"
    )

    # Criticality / confidence (Sprint 3)
    criticality: Optional[Dict[str, Any]] = Field(
        default=None,
        description="confidence_score, missing_required, system_confidence"
    )

    # Sprint 8: Formal confidence model (deterministic, Layer B only)
    confidence: Optional[Any] = Field(
        default=None,
        description="ConfidenceModel_v1; system/cluster/biomarker confidence, missing_required"
    )

    # Sprint 10: Relationship registry stamp (deterministic replay metadata)
    relationship_registry_version: Optional[str] = Field(
        default=None,
        description="RelationshipRegistry version used for relationship detections",
    )
    relationship_registry_hash: Optional[str] = Field(
        default=None,
        description="RelationshipRegistry schema hash for deterministic replay",
    )

    # Sprint 14: Signal registry stamp + evaluated signal payload
    signal_registry_version: Optional[str] = Field(default=None)
    signal_registry_hash: Optional[str] = Field(default=None)
    signal_results: List[Dict[str, Any]] = Field(default_factory=list)

    # Sprint 10: Relationship detections (safe status/score-derived, no raw values)
    relationships: List[RelationshipDetection] = Field(default_factory=list)

    # Sprint 11: BiomarkerContext_v1 stamp + nodes (code-only explanatory context)
    biomarker_context_version: Optional[str] = Field(default=None)
    biomarker_context_hash: Optional[str] = Field(default=None)
    biomarker_context: List[BiomarkerContextNode] = Field(default_factory=list)

    # v5.3 Sprint 1: StateTransition_v1 stamp + nodes (longitudinal, code-only)
    state_transition_version: Optional[str] = Field(default=None)
    state_transition_hash: Optional[str] = Field(default=None)
    state_transitions: List[BiomarkerTransitionNode] = Field(default_factory=list)

    # v5.3 Sprint 2: Multi-marker system state engine (code-only)
    state_engine_version: Optional[str] = Field(default=None)
    state_engine_hash: Optional[str] = Field(default=None)
    system_states: List[SystemStateNode] = Field(default_factory=list)

    # v5.3 Sprint 3: Interaction precedence arbitration (code-only)
    precedence_engine_version: Optional[str] = Field(default=None)
    precedence_engine_hash: Optional[str] = Field(default=None)
    precedence_output: PrecedenceOutput = Field(
        default_factory=lambda: PrecedenceOutput(
            primary_driver_system_id="",
            dominant_edges=[],
            conflicts_resolved=[],
            rationale_codes=[],
        )
    )
    causal_layer_version: Optional[str] = Field(default=None)
    causal_layer_hash: Optional[str] = Field(default=None)
    conflict_set: List[ConflictItem] = Field(default_factory=list)
    dominance_edges: List[DominanceEdge] = Field(default_factory=list)
    causal_edges: List[CausalEdge] = Field(default_factory=list)
    arbitration_result: ArbitrationNode = Field(
        default_factory=lambda: ArbitrationNode(
            supporting_system_ids=[],
            decision_trace_codes=[],
            tie_breaker_codes=[],
            rationale_codes=[],
        )
    )
    primary_driver_system_id: str = Field(default="")
    supporting_systems: List[str] = Field(default_factory=list)
    influence_order: List[str] = Field(default_factory=list)
    arbitration_version: str = Field(default="")
    arbitration_hash: str = Field(default="")
    calibration_version: str = Field(default="")
    calibration_hash: str = Field(default="")
    calibration_items: List[CalibrationItem] = Field(default_factory=list)
    bio_stats_engine_version: str = Field(default="")
    system_burden_engine_version: str = Field(default="")
    influence_propagator_version: str = Field(default="")
    capacity_scaler_version: str = Field(default="")
    validation_gate_version: str = Field(default="")
    raw_system_burden_vector: Dict[str, float] = Field(default_factory=dict)
    adjusted_system_burden_vector: Dict[str, float] = Field(default_factory=dict)
    burden_path_distances: Dict[str, float] = Field(default_factory=dict)
    system_capacity_scores: Dict[str, int] = Field(default_factory=dict)
    burden_hash: str = Field(default="")
    burden_validation_status: str = Field(default="")
    burden_validation_violations: List[str] = Field(default_factory=list)

    # Biomarker nodes (deterministic order by biomarker_id)
    biomarker_nodes: List[BiomarkerNode] = Field(default_factory=list)

    # Edges (optional; empty if not implemented)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    layer_c_features: Optional[LayerCFeatureBundleV1] = Field(default=None)
