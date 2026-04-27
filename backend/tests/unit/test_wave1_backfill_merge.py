"""D-6 — backfill merge helpers (legacy preservation + version audit)."""
from core.pipeline.orchestrator import UNIT_NORMALISATION_META_KEY

from scripts.wave1_backfill_consumer_cards import (
    merge_backfill_payload,
    prepare_stored_raw_for_orchestrator,
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


def test_prepare_stored_raw_sets_unit_normalisation_meta():
    prepared = prepare_stored_raw_for_orchestrator(
        {"glucose": {"value": 95.0, "unit": "mg/dL"}}
    )
    meta = prepared.get(UNIT_NORMALISATION_META_KEY) or {}
    assert meta.get("unit_normalised") is True
    assert meta.get("unit_registry_version")
