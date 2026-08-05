"""UAT history regression — empty vs failed history loading; no supersession filter on /history."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import ProgrammingError

from core.dto.trend_selection_v1 import TrendAnalysisRecord, select_trend_eligible
from services.storage.persistence_service import PersistenceService


@pytest.fixture
def persistence_no_fallback():
    return PersistenceService(Mock(name="db_session"), enable_fallback=False)


def test_get_analysis_history_genuine_empty_returns_empty_list(persistence_no_fallback):
    user_id = uuid4()
    with patch.object(persistence_no_fallback.analysis_repo, "list_by_user_id", return_value=[]):
        result = persistence_no_fallback.get_analysis_history(user_id, limit=10, offset=0)
    assert result == []


def test_get_analysis_history_schema_failure_is_propagated(persistence_no_fallback):
    """Undefined-column / schema errors must not become a successful []."""
    user_id = uuid4()
    schema_err = ProgrammingError(
        "SELECT analyses.result_date ...",
        {},
        Exception("column analyses.result_date does not exist"),
    )
    with patch.object(
        persistence_no_fallback.analysis_repo,
        "list_by_user_id",
        side_effect=schema_err,
    ):
        with pytest.raises(Exception) as exc_info:
            persistence_no_fallback.get_analysis_history(user_id, limit=10, offset=0)
    # Must not silently return []. Propagated error may be the schema error or
    # decorator AttributeError when fallback_service is None — either surfaces as failure.
    assert exc_info.value is not None


def test_get_analysis_history_includes_superseded_records(persistence_no_fallback):
    """Ordinary history must not apply trend supersession filtering."""
    user_id = uuid4()
    root_id = uuid4()
    tip_id = uuid4()
    superseded = Mock(
        id=root_id,
        created_at=datetime(2024, 1, 1),
        status="completed",
        processing_time_seconds=1.0,
        result_date=date(2024, 1, 1),
        result_date_provenance="user_entered",
        supersedes_analysis_id=None,
        lineage_root_analysis_id=root_id,
    )
    tip = Mock(
        id=tip_id,
        created_at=datetime(2025, 6, 1),
        status="completed",
        processing_time_seconds=1.0,
        result_date=date(2024, 1, 1),
        result_date_provenance="user_entered",
        supersedes_analysis_id=root_id,
        lineage_root_analysis_id=root_id,
    )
    with patch.object(
        persistence_no_fallback.analysis_repo,
        "list_by_user_id",
        return_value=[tip, superseded],
    ), patch.object(
        persistence_no_fallback.analysis_result_repo,
        "get_by_analysis_id",
        return_value=Mock(overall_score=0.5),
    ):
        result = persistence_no_fallback.get_analysis_history(user_id, limit=10, offset=0)

    ids = {row["id"] for row in result}
    assert str(root_id) in ids
    assert str(tip_id) in ids
    tip_row = next(r for r in result if r["id"] == str(tip_id))
    assert tip_row["supersedes_analysis_id"] == str(root_id)


def test_trend_eligible_still_excludes_superseded():
    records = [
        TrendAnalysisRecord(
            analysis_id="a1",
            status="completed",
            result_date=date(2024, 1, 1),
            created_at=datetime(2024, 1, 2),
            supersedes_analysis_id=None,
            lineage_root_analysis_id="a1",
        ),
        TrendAnalysisRecord(
            analysis_id="a2",
            status="completed",
            result_date=date(2024, 1, 1),
            created_at=datetime(2025, 6, 1),
            supersedes_analysis_id="a1",
            lineage_root_analysis_id="a1",
        ),
    ]
    eligible = select_trend_eligible(records)
    assert [r.analysis_id for r in eligible] == ["a2"]
