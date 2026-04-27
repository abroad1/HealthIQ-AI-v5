"""D-6 — backfill merge helpers (legacy preservation + version audit)."""

import pytest
from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service
from core.pipeline.orchestrator import UNIT_NORMALISATION_META_KEY

from scripts.wave1_backfill_consumer_cards import (
    merge_backfill_payload,
    prepare_stored_raw_for_orchestrator,
    rerun_orchestrator_for_wave1_backfill,
    run_backfill_dry_run,
)


def test_merge_preserves_legacy_and_sets_new_rows():
    stored = {
        "consumer_domain_scores": [
            {"domain_id": "c", "card_schema_version": "1.0"},
        ],
        "meta": {"foo": 1},
    }
    new_rows = [{"domain_id": "c", "card_schema_version": "1.1"}]
    out = merge_backfill_payload(
        stored,
        new_rows,
        new_meta_fragment={"bar": 2, "wave1_backfill_audit": {"ok": True}},
    )
    assert out["consumer_domain_scores_legacy_1_0"] == stored["consumer_domain_scores"]
    assert out["consumer_domain_scores"] == new_rows
    assert out["meta"]["foo"] == 1
    assert out["meta"]["bar"] == 2


def test_dry_run_returns_audit():
    r = run_backfill_dry_run(
        {"consumer_domain_scores": [{"x": 1, "card_schema_version": "1.0"}]},
        [{"x": 2, "card_schema_version": "1.1"}],
        "00000000-0000-0000-0000-000000000001",
    )
    assert r["old_card_version"] == "1.0"
    assert r["new_card_version"] == "1.1"
    assert r["legacy_preserved"] is True
    assert "merged" in r


@pytest.fixture(autouse=True)
def _disable_common_alias_injection_for_orchestrator_backfill(monkeypatch):
    """Same as orchestrator unit tests — stable canonical keys for rerun."""
    get_alias_registry_service.cache_clear()
    monkeypatch.setattr(
        AliasRegistryService,
        "_add_common_aliases",
        lambda self, alias_mapping, insert_alias: None,
    )
    yield
    get_alias_registry_service.cache_clear()


def test_rerun_preserves_fixed_analysis_id():
    fixed = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    raw_biomarkers = {
        "total_cholesterol": {"value": 200.0, "unit": "mg/dL"},
        "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL"},
    }
    user = {"user_id": "test-wave1-backfill", "age": 35, "gender": "male"}
    dto, audit = rerun_orchestrator_for_wave1_backfill(
        raw_biomarkers=raw_biomarkers,
        user=user,
        questionnaire_data=None,
        fixed_analysis_id=fixed,
        assume_canonical=True,
    )
    assert dto.analysis_id == fixed
    assert audit["analysis_id"] == fixed


def test_prepare_stored_raw_sets_unit_normalisation_meta():
    prepared = prepare_stored_raw_for_orchestrator(
        {"glucose": {"value": 95.0, "unit": "mg/dL"}}
    )
    meta = prepared.get(UNIT_NORMALISATION_META_KEY) or {}
    assert meta.get("unit_normalised") is True
    assert meta.get("unit_registry_version")
