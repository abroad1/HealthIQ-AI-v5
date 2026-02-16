"""
Sprint 11 - BiomarkerContext v1 Builder.

Build deterministic code-only context nodes from InsightGraph_v1.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from core.contracts.biomarker_context_v1 import (
    BIOMARKER_CONTEXT_V1_VERSION,
    BiomarkerContextNode,
    BiomarkerContextStamp,
    canonical_json_sha256,
)

# Deterministic score bands for context reasoning (0-100 score scale)
_LOW_SCORE_MAX = 33.0
_MID_SCORE_MAX = 66.0


def _normalise_status(raw: Any) -> str:
    status = str(raw or "").strip().lower()
    if status in {"low"}:
        return "low"
    if status in {"high", "elevated", "critical"}:
        return "high"
    if status in {"normal", "optimal"}:
        return "normal"
    return "unknown"


def _score_band_code(score: Optional[float]) -> str:
    if score is None:
        return "score_missing"
    if score < _LOW_SCORE_MAX:
        return "score_low_band"
    if score < _MID_SCORE_MAX:
        return "score_mid_band"
    return "score_high_band"


def _build_missing_codes(
    biomarker_id: str,
    confidence: Optional[Dict[str, Any]],
    cluster_summary: Optional[Dict[str, Any]],
) -> List[str]:
    missing: List[str] = []
    confidence = confidence or {}
    cluster_summary = cluster_summary or {}

    missing_required = set(confidence.get("missing_required_biomarkers") or [])
    if biomarker_id in missing_required:
        missing.append("missing_required_for_cluster")

    incomplete_cluster_ids = set(confidence.get("missing_required_clusters") or [])
    clusters = cluster_summary.get("clusters") or []
    if incomplete_cluster_ids and isinstance(clusters, list):
        for cluster in clusters:
            if not isinstance(cluster, dict):
                continue
            cluster_id = str(cluster.get("cluster_id", ""))
            biomarkers = cluster.get("biomarkers") or []
            if cluster_id in incomplete_cluster_ids and biomarker_id in biomarkers:
                missing.append(f"in_incomplete_cluster:{cluster_id}")

    return sorted(set(missing))


def _build_relationship_codes(
    biomarker_id: str,
    relationships: List[Dict[str, Any]],
) -> List[str]:
    codes: List[str] = []
    for rel in relationships:
        if not isinstance(rel, dict):
            continue
        biomarkers = rel.get("biomarkers") or []
        if biomarker_id not in biomarkers:
            continue
        relationship_id = str(rel.get("relationship_id", ""))
        if relationship_id:
            codes.append(f"relationship:{relationship_id}")
        evidence = rel.get("evidence") or []
        for ev in evidence:
            ev_code = str(ev).strip()
            if ev_code:
                codes.append(f"evidence:{ev_code}")
    return sorted(set(codes))


def build_biomarker_context_v1(insight_graph: Any) -> Tuple[List[BiomarkerContextNode], BiomarkerContextStamp]:
    """
    Build deterministic BiomarkerContext_v1 nodes + stamp from InsightGraph.
    """
    if hasattr(insight_graph, "model_dump"):
        graph = insight_graph.model_dump()
    elif isinstance(insight_graph, dict):
        graph = insight_graph
    else:
        graph = {}

    biomarker_nodes = graph.get("biomarker_nodes") or []
    confidence = graph.get("confidence") if isinstance(graph.get("confidence"), dict) else {}
    cluster_summary = graph.get("cluster_summary") if isinstance(graph.get("cluster_summary"), dict) else {}
    relationships = graph.get("relationships") if isinstance(graph.get("relationships"), list) else []

    out: List[BiomarkerContextNode] = []
    for node in biomarker_nodes:
        if not isinstance(node, dict):
            continue
        biomarker_id = str(node.get("biomarker_id", "")).strip()
        if not biomarker_id:
            continue

        status = _normalise_status(node.get("status"))
        score = node.get("score")
        score_val: Optional[float] = None
        if isinstance(score, (int, float)):
            score_val = float(score)

        reason_codes = sorted(
            set(
                [
                    f"status_{status}",
                    _score_band_code(score_val),
                ]
            )
        )
        missing_codes = _build_missing_codes(
            biomarker_id=biomarker_id,
            confidence=confidence,
            cluster_summary=cluster_summary,
        )
        relationship_codes = _build_relationship_codes(
            biomarker_id=biomarker_id,
            relationships=relationships,
        )

        out.append(
            BiomarkerContextNode(
                biomarker_id=biomarker_id,
                status=status,
                score=score_val,
                reason_codes=reason_codes,
                missing_codes=missing_codes,
                relationship_codes=relationship_codes,
            )
        )

    out.sort(key=lambda n: n.biomarker_id)
    context_payload = {
        "biomarker_context_version": BIOMARKER_CONTEXT_V1_VERSION,
        "biomarker_context": [n.model_dump() for n in out],
    }
    context_hash = canonical_json_sha256(context_payload)
    stamp = BiomarkerContextStamp(
        biomarker_context_version=BIOMARKER_CONTEXT_V1_VERSION,
        biomarker_context_hash=context_hash,
    )
    return out, stamp
