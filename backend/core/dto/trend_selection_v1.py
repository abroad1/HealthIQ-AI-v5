"""
CLIN-PRIORITY-RESULT-REGEN-1 — canonical backend trend/history selection.

Selects active (non-superseded) completed analyses for trend and longitudinal use.
Lineage identity, not date alone, determines replacement.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable, List, Optional, Sequence
from uuid import UUID

from core.dto.analysis_policy_version_v1 import parse_result_date


@dataclass(frozen=True)
class TrendAnalysisRecord:
    """Minimal record required for trend eligibility selection."""

    analysis_id: str
    status: str
    result_date: Optional[date]
    created_at: Optional[datetime]
    supersedes_analysis_id: Optional[str]
    lineage_root_analysis_id: Optional[str]
    overall_score: Optional[float] = None
    result_date_provenance: Optional[str] = None


def _as_id(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def record_from_analysis_row(row: Any, *, overall_score: Optional[float] = None) -> TrendAnalysisRecord:
    """Build a TrendAnalysisRecord from an ORM Analysis (or duck-typed) row."""
    result_date = getattr(row, "result_date", None)
    if result_date is not None and not isinstance(result_date, date):
        result_date = parse_result_date(result_date)
    created_at = getattr(row, "created_at", None)
    supersedes = getattr(row, "supersedes_analysis_id", None)
    lineage_root = getattr(row, "lineage_root_analysis_id", None)
    return TrendAnalysisRecord(
        analysis_id=str(getattr(row, "id")),
        status=str(getattr(row, "status", "") or ""),
        result_date=result_date,
        created_at=created_at if isinstance(created_at, datetime) else None,
        supersedes_analysis_id=_as_id(supersedes),
        lineage_root_analysis_id=_as_id(lineage_root) or str(getattr(row, "id")),
        overall_score=overall_score,
        result_date_provenance=getattr(row, "result_date_provenance", None),
    )


def effective_result_date(record: TrendAnalysisRecord) -> date:
    """Placement date: result_date, else created_at date, else epoch."""
    if record.result_date is not None:
        return record.result_date
    if record.created_at is not None:
        return record.created_at.date()
    return date.min


def select_trend_eligible(
    records: Sequence[TrendAnalysisRecord],
    *,
    limit: Optional[int] = None,
) -> List[TrendAnalysisRecord]:
    """
    Return active completed analyses for trend participation.

    An analysis is superseded when another completed analysis in the estate lists it
    as `supersedes_analysis_id`. Only the tip of each lineage participates.
    Distinct lineage roots sharing the same result_date remain separate.
    """
    completed = [r for r in records if r.status == "completed"]
    superseded_ids = {
        r.supersedes_analysis_id
        for r in completed
        if r.supersedes_analysis_id
    }
    active = [r for r in completed if r.analysis_id not in superseded_ids]

    def sort_key(r: TrendAnalysisRecord) -> tuple:
        # Newest clinical chronology first; tie-break by created_at then id (deterministic).
        created_ts = r.created_at.timestamp() if r.created_at is not None else 0.0
        return (effective_result_date(r), created_ts, r.analysis_id)

    active_sorted = sorted(active, key=sort_key, reverse=True)
    if limit is not None and limit >= 0:
        return active_sorted[:limit]
    return active_sorted


def trend_history_item(record: TrendAnalysisRecord) -> dict[str, Any]:
    """API history-shaped item for a trend-eligible analysis."""
    created = (
        record.created_at.isoformat()
        if record.created_at is not None
        else None
    )
    return {
        "id": record.analysis_id,
        "analysis_id": record.analysis_id,
        "created_at": created,
        "status": record.status,
        "overall_score": record.overall_score,
        "result_date": record.result_date.isoformat() if record.result_date else None,
        "result_date_provenance": record.result_date_provenance,
        "supersedes_analysis_id": record.supersedes_analysis_id,
        "lineage_root_analysis_id": record.lineage_root_analysis_id,
        "trend_eligible": True,
    }
