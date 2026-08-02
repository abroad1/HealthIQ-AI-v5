"""ARCH-CONV-PKGC-1 — waist-unit stale detection + MARK_STALE_NO_REWRITE remediation."""

from __future__ import annotations

import copy

from core.dto.arch_conv_pkgc_1_waist_remediation_v1 import (
    APPROVED_ANALYSIS_IDS,
    APPROVED_ANALYSIS_ID_SET,
    AUDIT_ORIGINAL_VALUES,
    CLIENT_RESULT_SHAPE_V1,
    DISPOSITION,
    REMEDIATION_META_KEY,
    STALE_REASON,
    apply_mark_stale_no_rewrite,
    apply_planned_remediation,
    plan_remediation,
)
from core.dto.result_versioning_policy_v1 import (
    CURRENT_COMPLETENESS_POLICY_ID,
    detect_launch_core_stale_reasons,
)


def _shell(**overrides):
    base = {
        "analysis_id": "unrelated-id",
        "meta": {"completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID},
        "consumer_domain_scores": [],
        "result_version": "1.0.0",
        "replay_manifest": {"manifest_version": "1.0.0"},
    }
    base.update(overrides)
    return base


def test_governed_ids_receive_waist_stale_reason():
    for aid in APPROVED_ANALYSIS_IDS:
        reasons = detect_launch_core_stale_reasons(_shell(analysis_id=aid))
        assert STALE_REASON in reasons


def test_valid_cm_record_not_marked_stale_by_waist_rule():
    reasons = detect_launch_core_stale_reasons(
        _shell(
            analysis_id="not-in-allowlist",
            meta={
                "completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID,
                "waist": {"unit": "cm", "value": 90},
            },
        )
    )
    assert STALE_REASON not in reasons


def test_valid_inches_provenance_not_marked_stale_by_waist_rule():
    reasons = detect_launch_core_stale_reasons(
        _shell(
            analysis_id="fresh-inches-record",
            meta={
                "completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID,
                "waist": {"unit": "inches", "value": 34, "provenance": "explicit_dict"},
            },
        )
    )
    assert STALE_REASON not in reasons


def test_surprising_waist_magnitude_alone_does_not_mark_stale():
    reasons = detect_launch_core_stale_reasons(
        _shell(
            analysis_id="random-id",
            meta={"completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID, "waist_cm": 22},
        )
    )
    assert STALE_REASON not in reasons


def test_existing_completeness_rules_unchanged_and_compose_with_waist():
    aid = APPROVED_ANALYSIS_IDS[0]
    reasons = detect_launch_core_stale_reasons(
        {
            "analysis_id": aid,
            "meta": {},  # completeness_policy_missing
            "consumer_domain_scores": [],
        }
    )
    assert "completeness_policy_missing" in reasons
    assert STALE_REASON in reasons


def test_detection_deterministic():
    stored = _shell(analysis_id=APPROVED_ANALYSIS_IDS[0])
    assert detect_launch_core_stale_reasons(stored) == detect_launch_core_stale_reasons(
        copy.deepcopy(stored)
    )


def test_remediation_stamp_also_triggers_stale_reason():
    stamped = apply_mark_stale_no_rewrite(
        {CLIENT_RESULT_SHAPE_V1: {"analysis_id": "other", "meta": {}}},
        analysis_id="other",
        timestamp_utc="2026-08-02T00:00:00Z",
    )
    client = stamped[CLIENT_RESULT_SHAPE_V1]
    reasons = detect_launch_core_stale_reasons(client)
    assert STALE_REASON in reasons
    assert stamped[REMEDIATION_META_KEY]["disposition"] == DISPOSITION
    assert stamped[REMEDIATION_META_KEY]["value_rewritten"] is False


def _fixture_rows():
    rows = []
    for aid in APPROVED_ANALYSIS_IDS:
        rows.append(
            {
                "analysis_id": aid,
                "exists": True,
                "questionnaire_data": {
                    "waist_circumference": AUDIT_ORIGINAL_VALUES[aid],
                },
                "processing_metadata": {
                    CLIENT_RESULT_SHAPE_V1: {
                        "analysis_id": aid,
                        "meta": {"completeness_policy_id": CURRENT_COMPLETENESS_POLICY_ID},
                        "consumer_domain_scores": [],
                    }
                },
                "already_superseded": False,
            }
        )
    return rows


def test_dry_run_identifies_exact_approved_rows():
    plan = plan_remediation(_fixture_rows(), timestamp_utc="2026-08-02T12:00:00Z")
    assert plan["fail_closed"] is False
    assert plan["summary"]["pass_ready"] == 12
    assert [r["analysis_id"] for r in plan["results"]] == list(APPROVED_ANALYSIS_IDS)
    for r in plan["results"]:
        assert r["action"] == DISPOSITION
        assert r["after"]["value_rewritten"] is False
        assert r["after"]["unit_rewritten"] is False


def test_no_unapproved_row_mutated_and_fail_closed_on_extra():
    rows = _fixture_rows()
    rows.append(
        {
            "analysis_id": "00000000-0000-0000-0000-000000000099",
            "exists": True,
            "questionnaire_data": {"waist_circumference": 80},
            "processing_metadata": {},
        }
    )
    plan = plan_remediation(rows)
    assert plan["fail_closed"] is True
    assert "00000000-0000-0000-0000-000000000099" in plan["unexpected_ids"]
    applied = apply_planned_remediation(plan, write=True)
    assert applied["write_executed"] is False
    assert applied["mode"] == "write_refused"


def test_idempotent_re_run_no_additional_mutation():
    rows = _fixture_rows()
    plan1 = plan_remediation(rows, timestamp_utc="2026-08-02T12:00:00Z")
    # Simulate first write into fixtures.
    for r, planned in zip(rows, plan1["results"]):
        r["processing_metadata"] = planned["planned_processing_metadata"]
    plan2 = plan_remediation(rows, timestamp_utc="2026-08-02T13:00:00Z")
    assert plan2["fail_closed"] is False
    assert plan2["summary"]["already_remediated"] == 12
    assert plan2["summary"]["pass_ready"] == 0


def test_changed_precondition_fail_closed():
    rows = _fixture_rows()
    rows[0]["questionnaire_data"] = {"waist_circumference": 999}
    plan = plan_remediation(rows)
    assert plan["fail_closed"] is True
    assert plan["results"][0]["precondition"] == "FAIL_PRECONDITION_VALUE_MISMATCH"
    applied = apply_planned_remediation(plan, write=True)
    assert applied["complete_success"] is False
    assert applied["write_executed"] is False


def test_missing_row_fail_closed_reported_without_mutation():
    rows = _fixture_rows()
    rows[0]["exists"] = False
    plan = plan_remediation(rows)
    assert plan["fail_closed"] is True
    assert plan["results"][0]["precondition"] == "FAIL_MISSING"
    assert apply_planned_remediation(plan, write=True)["write_executed"] is False


def test_partial_failure_not_complete_success():
    rows = _fixture_rows()[:11]  # missing one approved id
    plan = plan_remediation(rows)
    assert plan["fail_closed"] is True
    assert plan["missing_approved_ids"]
    applied = apply_planned_remediation(plan, write=True)
    assert applied["complete_success"] is False


def test_mark_stale_preserves_questionnaire_values():
    aid = APPROVED_ANALYSIS_IDS[0]
    q = {"waist_circumference": AUDIT_ORIGINAL_VALUES[aid]}
    pm = {
        CLIENT_RESULT_SHAPE_V1: {
            "analysis_id": aid,
            "meta": {},
            "consumer_domain_scores": [],
        }
    }
    new_pm = apply_mark_stale_no_rewrite(pm, analysis_id=aid, timestamp_utc="2026-08-02T12:00:00Z")
    assert q["waist_circumference"] == AUDIT_ORIGINAL_VALUES[aid]
    assert new_pm[CLIENT_RESULT_SHAPE_V1]["meta"][REMEDIATION_META_KEY]["value_rewritten"] is False
    assert REMEDIATION_META_KEY in new_pm


def test_approved_set_size_is_twelve():
    assert len(APPROVED_ANALYSIS_IDS) == 12
    assert len(APPROVED_ANALYSIS_ID_SET) == 12
    assert set(AUDIT_ORIGINAL_VALUES) == APPROVED_ANALYSIS_ID_SET
