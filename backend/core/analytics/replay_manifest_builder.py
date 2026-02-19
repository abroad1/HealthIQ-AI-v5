"""
Sprint 9 - Replay Manifest Builder (Layer B only).

Builds ReplayManifestV1 from already-built objects. No clinical computation.
Deterministic hashing via canonical JSON + SHA-256.
"""

import hashlib
import json
import os
from typing import Dict, Any, Optional

from core.contracts.replay_manifest_v1 import ReplayManifestV1, REPLAY_MANIFEST_V1_VERSION


def _canonical_json_hash(obj: Any) -> str:
    """Stable SHA-256 hash of canonical JSON (sorted keys, stable ordering)."""
    if obj is None:
        return ""
    try:
        # Canonical: sort_keys, no whitespace
        payload = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
    except (TypeError, ValueError):
        return ""


def _fixture_mode_enabled() -> bool:
    mode = os.getenv("HEALTHIQ_MODE", "").strip().lower()
    return mode in {"fixture", "fixtures"}


def build_replay_manifest_v1(
    unit_registry_version: str,
    ratio_registry_version: str,
    cluster_schema_version: str,
    cluster_schema_hash: str,
    insight_graph: Optional[Any] = None,
    confidence_model: Optional[Any] = None,
    derived_markers_registry_version: Optional[str] = None,
    relationship_registry_version: Optional[str] = None,
    relationship_registry_hash: Optional[str] = None,
    biomarker_context_version: Optional[str] = None,
    biomarker_context_hash: Optional[str] = None,
    scoring_policy_version: Optional[str] = None,
    scoring_policy_hash: Optional[str] = None,
    evidence_registry_version: Optional[str] = None,
    evidence_registry_hash: Optional[str] = None,
    state_transition_version: Optional[str] = None,
    state_transition_hash: Optional[str] = None,
    state_engine_version: Optional[str] = None,
    state_engine_hash: Optional[str] = None,
    precedence_engine_version: Optional[str] = None,
    precedence_engine_hash: Optional[str] = None,
    linked_snapshot_ids: Optional[list[str]] = None,
    analysis_result_version: str = "1.0.0",
) -> ReplayManifestV1:
    """
    Build ReplayManifestV1 from Layer B outputs.

    Args:
        unit_registry_version: From UNIT_REGISTRY_VERSION or units.yaml
        ratio_registry_version: From RatioRegistry.version / derived output
        cluster_schema_version: From get_cluster_schema_version_stamp
        cluster_schema_hash: From get_cluster_schema_version_stamp
        insight_graph: InsightGraphV1 instance (already built)
        confidence_model: ConfidenceModelV1 instance (already built)
        derived_markers_registry_version: If distinct; else use ratio_registry_version
        relationship_registry_version: Relationship registry version stamp
        relationship_registry_hash: Relationship registry hash stamp
        biomarker_context_version: BiomarkerContext version stamp
        biomarker_context_hash: BiomarkerContext hash stamp
        scoring_policy_version: Scoring policy version stamp
        scoring_policy_hash: Scoring policy hash stamp
        evidence_registry_version: Evidence registry version stamp
        evidence_registry_hash: Evidence registry hash stamp
        state_transition_version: State transition version stamp
        state_transition_hash: State transition hash stamp
        state_engine_version: State engine version stamp
        state_engine_hash: State engine hash stamp
        precedence_engine_version: Precedence engine version stamp
        precedence_engine_hash: Precedence engine hash stamp
        linked_snapshot_ids: Prior snapshot IDs linked for longitudinal compute
        analysis_result_version: Existing result_version if present

    Returns:
        ReplayManifestV1 instance
    """
    derived_ver = derived_markers_registry_version or ratio_registry_version

    ig_version = ""
    ig_hash = ""
    if insight_graph is not None:
        try:
            dump = insight_graph.model_dump() if hasattr(insight_graph, "model_dump") else insight_graph
            ig_version = str(dump.get("graph_version", ""))
            ig_hash = _canonical_json_hash(dump)
            if not relationship_registry_version:
                relationship_registry_version = str(dump.get("relationship_registry_version", ""))
            if not relationship_registry_hash:
                relationship_registry_hash = str(dump.get("relationship_registry_hash", ""))
            if not biomarker_context_version:
                biomarker_context_version = str(dump.get("biomarker_context_version", ""))
            if not biomarker_context_hash:
                biomarker_context_hash = str(dump.get("biomarker_context_hash", ""))
            if not state_transition_version:
                state_transition_version = str(dump.get("state_transition_version", ""))
            if not state_transition_hash:
                state_transition_hash = str(dump.get("state_transition_hash", ""))
            if not state_engine_version:
                state_engine_version = str(dump.get("state_engine_version", ""))
            if not state_engine_hash:
                state_engine_hash = str(dump.get("state_engine_hash", ""))
            if not precedence_engine_version:
                precedence_engine_version = str(dump.get("precedence_engine_version", ""))
            if not precedence_engine_hash:
                precedence_engine_hash = str(dump.get("precedence_engine_hash", ""))
            if linked_snapshot_ids is None and isinstance(dump.get("linked_snapshot_ids"), list):
                linked_snapshot_ids = [str(x) for x in dump.get("linked_snapshot_ids", [])]
        except Exception as exc:
            if not _fixture_mode_enabled():
                raise ValueError(f"Replay manifest build failed for insight_graph: {exc}") from exc

    conf_version = ""
    conf_hash = ""
    if confidence_model is not None:
        try:
            dump = confidence_model.model_dump() if hasattr(confidence_model, "model_dump") else confidence_model
            conf_version = str(dump.get("model_version", ""))
            conf_hash = _canonical_json_hash(dump)
        except Exception as exc:
            if not _fixture_mode_enabled():
                raise ValueError(f"Replay manifest build failed for confidence_model: {exc}") from exc

    schema_hashes: Dict[str, str] = {}
    if ig_hash:
        schema_hashes["insight_graph_hash"] = ig_hash
    if conf_hash:
        schema_hashes["confidence_model_hash"] = conf_hash

    return ReplayManifestV1(
        manifest_version=REPLAY_MANIFEST_V1_VERSION,
        unit_registry_version=unit_registry_version,
        ratio_registry_version=ratio_registry_version,
        cluster_schema_version=cluster_schema_version,
        cluster_schema_hash=cluster_schema_hash,
        insight_graph_version=ig_version,
        confidence_model_version=conf_version,
        derived_markers_registry_version=derived_ver,
        relationship_registry_version=relationship_registry_version or "",
        relationship_registry_hash=relationship_registry_hash or "",
        biomarker_context_version=biomarker_context_version or "",
        biomarker_context_hash=biomarker_context_hash or "",
        scoring_policy_version=scoring_policy_version or "",
        scoring_policy_hash=scoring_policy_hash or "",
        evidence_registry_version=evidence_registry_version or "",
        evidence_registry_hash=evidence_registry_hash or "",
        state_transition_version=state_transition_version or "",
        state_transition_hash=state_transition_hash or "",
        state_engine_version=state_engine_version or "",
        state_engine_hash=state_engine_hash or "",
        precedence_engine_version=precedence_engine_version or "",
        precedence_engine_hash=precedence_engine_hash or "",
        linked_snapshot_ids=list(linked_snapshot_ids or []),
        schema_hashes=schema_hashes,
        analysis_result_version=analysis_result_version,
    )
