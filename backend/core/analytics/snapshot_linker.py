"""
v5.3 Sprint 1 - Snapshot linker.

Builds deterministic prior InsightGraph snapshots from persisted analysis rows.
Only safe InsightGraph-derived fields are returned (status/score/code metadata).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from core.contracts.insight_graph_v1 import BiomarkerNode, InsightGraphV1
from core.models.database import Analysis, AnalysisResult

DEFAULT_LINKED_PRIOR_SNAPSHOTS = 3


@dataclass(frozen=True)
class LinkedSnapshots:
    prior_insight_graphs: List[InsightGraphV1]
    linked_snapshot_ids: List[str]


def _to_uuid(value: Any, field_name: str) -> UUID:
    try:
        return value if isinstance(value, UUID) else UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field_name}: {value!r}") from exc


def _normalise_status(status: Any) -> str:
    s = str(status or "").strip().lower()
    if s in {"low", "normal", "high", "unknown"}:
        return s
    if s in {"optimal"}:
        return "normal"
    if s in {"elevated", "critical"}:
        return "high"
    return "unknown"


def _normalise_score(score: Any) -> Optional[float]:
    if score is None:
        return None
    try:
        val = float(score)
    except (TypeError, ValueError):
        return None
    # Persisted DTO scores may be 0-1; transition engine uses 0-100 bands.
    if 0.0 <= val <= 1.0:
        return val * 100.0
    return val


def _nodes_from_biomarkers_payload(payload: Any) -> List[BiomarkerNode]:
    if not isinstance(payload, list):
        return []
    out: List[BiomarkerNode] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        biomarker_id = str(item.get("biomarker_name", "")).strip()
        if not biomarker_id:
            continue
        out.append(
            BiomarkerNode(
                biomarker_id=biomarker_id,
                status=_normalise_status(item.get("status")),
                score=_normalise_score(item.get("score")),
            )
        )
    out.sort(key=lambda n: n.biomarker_id)
    return out


def _safe_insight_graph_from_result(
    analysis_id: str,
    result: AnalysisResult,
) -> Optional[InsightGraphV1]:
    processing = result.processing_metadata if isinstance(result.processing_metadata, dict) else {}
    embedded = processing.get("insight_graph")
    if not isinstance(embedded, dict):
        meta = processing.get("meta")
        if isinstance(meta, dict):
            embedded = meta.get("insight_graph")

    if isinstance(embedded, dict):
        try:
            graph_payload = {
                "graph_version": str(embedded.get("graph_version", "1.0.0")),
                "analysis_id": str(embedded.get("analysis_id", analysis_id)),
                "biomarker_nodes": embedded.get("biomarker_nodes", []),
                "biomarker_context_version": embedded.get("biomarker_context_version"),
                "biomarker_context_hash": embedded.get("biomarker_context_hash"),
                "biomarker_context": embedded.get("biomarker_context", []),
                "state_transition_version": embedded.get("state_transition_version"),
                "state_transition_hash": embedded.get("state_transition_hash"),
                "state_transitions": embedded.get("state_transitions", []),
                "edges": embedded.get("edges", []),
            }
            return InsightGraphV1(**graph_payload)
        except Exception:
            pass

    # Fallback to persisted biomarker summary rows (still safe: status/score only).
    nodes = _nodes_from_biomarkers_payload(result.biomarkers)
    if not nodes:
        return None
    return InsightGraphV1(
        graph_version="1.0.0",
        analysis_id=analysis_id,
        biomarker_nodes=nodes,
        edges=[],
    )


def link_prior_snapshot_insight_graphs(
    db_session: Session,
    user_id: Any,
    current_analysis_id: Any,
    max_snapshots: int = DEFAULT_LINKED_PRIOR_SNAPSHOTS,
) -> LinkedSnapshots:
    """
    Load prior snapshots for a user and return safe InsightGraph-only history.

    Ordering is deterministic: newest->oldest by created_at, then analysis_id.
    """
    if max_snapshots <= 0:
        return LinkedSnapshots(prior_insight_graphs=[], linked_snapshot_ids=[])

    uid = _to_uuid(user_id, "user_id")
    current_id = _to_uuid(current_analysis_id, "current_analysis_id")

    rows: List[Tuple[Analysis, AnalysisResult]] = (
        db_session.query(Analysis, AnalysisResult)
        .join(AnalysisResult, AnalysisResult.analysis_id == Analysis.id)
        .filter(Analysis.user_id == uid)
        .filter(Analysis.id != current_id)
        .all()
    )

    candidates: List[Tuple[datetime, str, InsightGraphV1]] = []
    for analysis, result in rows:
        analysis_id = str(analysis.id)
        graph = _safe_insight_graph_from_result(analysis_id=analysis_id, result=result)
        if graph is None:
            continue
        created = analysis.created_at or result.created_at
        if created is None:
            continue
        candidates.append((created, analysis_id, graph))

    candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)
    selected = candidates[:max_snapshots]

    return LinkedSnapshots(
        prior_insight_graphs=[row[2] for row in selected],
        linked_snapshot_ids=[row[1] for row in selected],
    )
