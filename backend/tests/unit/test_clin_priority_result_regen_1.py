"""CLIN-PRIORITY-RESULT-REGEN-1 — analysis-policy versioning, result_date, trend supersession."""

from __future__ import annotations

from datetime import date, datetime

from core.dto.analysis_policy_version_v1 import (
    CURRENT_ANALYSIS_POLICY_VERSION,
    RESULT_DATE_PROVENANCE_LEGACY_CREATED_AT,
    RESULT_DATE_PROVENANCE_USER_ENTERED,
    resolve_result_date_for_new_analysis,
)
from core.dto.result_versioning_policy_v1 import (
    assess_result_versioning,
    build_result_versioning_metadata,
    stamp_current_policy_meta,
)
from core.dto.trend_selection_v1 import TrendAnalysisRecord, select_trend_eligible
from tests.unit.test_launch_core3_result_versioning import _render_contract_shell


def test_current_policy_result_remains_current():
    stored = _render_contract_shell(meta=stamp_current_policy_meta({}))
    meta = build_result_versioning_metadata(stored)
    assert meta["result_status"] == "current"
    assert meta["analysis_policy_version"] == CURRENT_ANALYSIS_POLICY_VERSION
    assert meta["current_analysis_policy_version"] == CURRENT_ANALYSIS_POLICY_VERSION


def test_older_policy_renderable_result_becomes_stale():
    stored = _render_contract_shell(meta={"analysis_policy_version": "analysis_policy_v0_legacy"})
    meta = build_result_versioning_metadata(stored)
    assert meta["result_status"] == "stale"
    assert any("analysis_policy_version_mismatch" in r for r in meta["stale_reasons"])


def test_missing_policy_stamp_is_stale_and_covers_pre_clin_priority():
    """Pre-CLIN-PRIORITY / missing clinical_concern_set estate: no stamp → not current."""
    stored = _render_contract_shell(meta={})
    meta = build_result_versioning_metadata(
        stored,
        raw_biomarkers={"glucose": {"value": 5.0}},
    )
    assert meta["result_status"] == "stale"
    assert "analysis_policy_version_missing" in meta["stale_reasons"]
    assert meta["regeneration_available"] is True


def test_incompatible_still_wins_over_stale():
    stored = _render_contract_shell(meta={})
    del stored["clinician_report_v1"]
    del stored["narrative_report_v1"]
    meta = build_result_versioning_metadata(stored)
    assert meta["result_status"] == "incompatible"
    assert meta["compatible"] is False


def test_resolve_result_date_user_entered_and_legacy_fallback():
    d, prov = resolve_result_date_for_new_analysis(requested_result_date="2024-03-15")
    assert d == date(2024, 3, 15)
    assert prov == RESULT_DATE_PROVENANCE_USER_ENTERED

    d2, prov2 = resolve_result_date_for_new_analysis(
        created_at=datetime(2023, 1, 10, 12, 0, 0),
    )
    assert d2 == date(2023, 1, 10)
    assert prov2 == RESULT_DATE_PROVENANCE_LEGACY_CREATED_AT


def test_trend_excludes_superseded_keeps_tip_once():
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
        TrendAnalysisRecord(
            analysis_id="a3",
            status="completed",
            result_date=date(2024, 1, 1),
            created_at=datetime(2025, 7, 1),
            supersedes_analysis_id="a2",
            lineage_root_analysis_id="a1",
        ),
    ]
    eligible = select_trend_eligible(records)
    assert [r.analysis_id for r in eligible] == ["a3"]


def test_trend_same_date_distinct_lineages_remain_separate():
    records = [
        TrendAnalysisRecord(
            analysis_id="b1",
            status="completed",
            result_date=date(2024, 6, 1),
            created_at=datetime(2024, 6, 2),
            supersedes_analysis_id=None,
            lineage_root_analysis_id="b1",
        ),
        TrendAnalysisRecord(
            analysis_id="c1",
            status="completed",
            result_date=date(2024, 6, 1),
            created_at=datetime(2024, 6, 3),
            supersedes_analysis_id=None,
            lineage_root_analysis_id="c1",
        ),
    ]
    eligible = select_trend_eligible(records)
    ids = {r.analysis_id for r in eligible}
    assert ids == {"b1", "c1"}


def test_stamp_embeds_analysis_policy_version():
    meta = stamp_current_policy_meta({})
    assert meta["analysis_policy_version"] == CURRENT_ANALYSIS_POLICY_VERSION
    assessment = assess_result_versioning(_render_contract_shell(meta=meta))
    assert not assessment.stale or not any(
        "analysis_policy_version" in r for r in assessment.stale_reasons
    )
