"""
Sprint 9 - Replay Manifest v1 Contract.

Strict, versioned execution manifest for replay/debug/audit.
Deterministic: no timestamps, no random, no environment-dependent fields.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

REPLAY_MANIFEST_V1_VERSION = "1.0.0"


class ReplayManifestV1(BaseModel):
    """
    Immutable execution manifest — Layer B output only.

    For replay determinism. No timestamps, no DB IDs, no env identifiers.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    manifest_version: str = Field(
        default=REPLAY_MANIFEST_V1_VERSION,
        description="Contract version",
    )

    unit_registry_version: str = Field(default="", description="From units.yaml / UnitRegistry")
    ratio_registry_version: str = Field(default="", description="From RatioRegistry")
    cluster_schema_version: str = Field(default="", description="From cluster schema")
    cluster_schema_hash: str = Field(default="", description="From cluster schema")
    insight_graph_version: str = Field(default="", description="InsightGraphV1 graph_version")
    confidence_model_version: str = Field(default="", description="ConfidenceModelV1 model_version")
    derived_markers_registry_version: str = Field(
        default="",
        description="Same as ratio_registry_version if not distinct",
    )
    relationship_registry_version: str = Field(
        default="",
        description="From RelationshipRegistry",
    )
    relationship_registry_hash: str = Field(
        default="",
        description="Deterministic hash of relationships.yaml canonical JSON",
    )
    biomarker_context_version: str = Field(
        default="",
        description="BiomarkerContext_v1 version stamp from InsightGraph",
    )
    biomarker_context_hash: str = Field(
        default="",
        description="BiomarkerContext_v1 deterministic hash from InsightGraph",
    )
    scoring_policy_version: str = Field(
        default="",
        description="From scoring_policy.yaml deterministic policy version",
    )
    scoring_policy_hash: str = Field(
        default="",
        description="Deterministic hash of scoring_policy.yaml canonical JSON",
    )
    evidence_registry_version: str = Field(
        default="",
        description="From EvidenceRegistry SSOT",
    )
    evidence_registry_hash: str = Field(
        default="",
        description="Deterministic hash of evidence_registry.yaml canonical JSON",
    )
    state_transition_version: str = Field(
        default="",
        description="StateTransitionEngine_v1 version stamp",
    )
    state_transition_hash: str = Field(
        default="",
        description="Deterministic hash of state transition payload",
    )
    state_engine_version: str = Field(
        default="",
        description="StateEngine_v1 version stamp",
    )
    state_engine_hash: str = Field(
        default="",
        description="Deterministic hash of system state payload",
    )
    precedence_engine_version: str = Field(
        default="",
        description="InteractionPrecedenceEngine_v1 version stamp",
    )
    precedence_engine_hash: str = Field(
        default="",
        description="Deterministic hash of precedence arbitration payload",
    )
    causal_layer_version: str = Field(
        default="",
        description="CausalLayer_v1 version stamp",
    )
    causal_layer_hash: str = Field(
        default="",
        description="Deterministic hash of causal layer payload",
    )
    calibration_version: str = Field(
        default="",
        description="OutcomeCalibrationLayer_v1 version stamp",
    )
    calibration_hash: str = Field(
        default="",
        description="Deterministic hash of calibration payload",
    )
    conflict_registry_version: str = Field(
        default="",
        description="Conflict registry version used in arbitration depth",
    )
    conflict_registry_hash: str = Field(
        default="",
        description="Deterministic hash of conflict registry payload",
    )
    arbitration_registry_version: str = Field(
        default="",
        description="Arbitration registry version used in arbitration depth",
    )
    arbitration_registry_hash: str = Field(
        default="",
        description="Deterministic hash of arbitration registry payload",
    )
    arbitration_version: str = Field(
        default="",
        description="ArbitrationDepth_v1 version stamp",
    )
    arbitration_hash: str = Field(
        default="",
        description="Deterministic hash of arbitration result payload",
    )
    explainability_version: str = Field(
        default="",
        description="ExplainabilityReport_v1 version stamp",
    )
    explainability_hash: str = Field(
        default="",
        description="Deterministic hash of explainability payload",
    )
    explainability_artifact_filename: str = Field(
        default="",
        description="Artifact file name for explainability report in snapshot packs",
    )
    bio_stats_engine_version: str = Field(default="", description="BioStatsEngine_v1 version stamp")
    system_burden_engine_version: str = Field(default="", description="SystemBurdenEngine_v1 version stamp")
    influence_propagator_version: str = Field(default="", description="InfluencePropagator_v1 version stamp")
    capacity_scaler_version: str = Field(default="", description="CapacityScaler_v1 version stamp")
    validation_gate_version: str = Field(default="", description="ValidationGate_v1 version stamp")
    burden_hash: str = Field(default="", description="Deterministic hash of burden/capacity vectors")
    burden_artifact_filename: str = Field(
        default="",
        description="Artifact file name for burden vector output in snapshot packs",
    )
    linked_snapshot_ids: List[str] = Field(
        default_factory=list,
        description="Prior analysis_ids linked for longitudinal state transition compute",
    )
    lifestyle_input_hash: Optional[str] = Field(
        default=None,
        description="Sprint 20: SHA-256 of canonical JSON lifestyle_inputs when provided; omitted when not used",
    )

    schema_hashes: Dict[str, str] = Field(
        default_factory=dict,
        description="insight_graph_hash, confidence_model_hash (SHA-256 of canonical JSON)",
    )

    analysis_result_version: str = Field(
        default="1.0.0",
        description="Existing result schema version if present",
    )
