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

    # Biomarker nodes (deterministic order by biomarker_id)
    biomarker_nodes: List[BiomarkerNode] = Field(default_factory=list)

    # Edges (optional; empty if not implemented)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
