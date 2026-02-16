"""Contracts - formal interface definitions (InsightGraph, ConfidenceModel, etc.)."""

from core.contracts.insight_graph_v1 import (
    InsightGraphV1,
    BiomarkerNode,
    INSIGHTGRAPH_V1_VERSION,
)
from core.contracts.confidence_model_v1 import (
    ConfidenceModelV1,
    CONFIDENCE_MODEL_V1_VERSION,
)
from core.contracts.replay_manifest_v1 import (
    ReplayManifestV1,
    REPLAY_MANIFEST_V1_VERSION,
)
from core.contracts.relationship_registry_v1 import (
    RelationshipDefinition,
    RelationshipDetection,
    RelationshipRegistryStamp,
    RELATIONSHIP_REGISTRY_V1_VERSION,
)

__all__ = [
    "InsightGraphV1",
    "BiomarkerNode",
    "INSIGHTGRAPH_V1_VERSION",
    "ConfidenceModelV1",
    "CONFIDENCE_MODEL_V1_VERSION",
    "ReplayManifestV1",
    "REPLAY_MANIFEST_V1_VERSION",
    "RelationshipDefinition",
    "RelationshipDetection",
    "RelationshipRegistryStamp",
    "RELATIONSHIP_REGISTRY_V1_VERSION",
]
