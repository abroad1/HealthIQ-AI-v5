"""Tests for intervention-effects registry and alias map validation (KB-S48a)."""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_intervention_effects_registry import (
    APPROVED_CLASS_IDS,
    FORBIDDEN_KEY_FRAGMENTS,
    main,
)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "knowledge_bus" / "interventions" / "intervention_effects_registry_v1.yaml"
DEFAULT_ALIASES = ROOT / "knowledge_bus" / "interventions" / "intervention_class_alias_map_v1.yaml"


def test_default_registry_and_aliases_pass(tmp_path: Path) -> None:
    audit = tmp_path / "audit.md"
    code = main(
        [
            "--registry",
            str(DEFAULT_REGISTRY),
            "--aliases",
            str(DEFAULT_ALIASES),
            "--audit-path",
            str(audit),
        ]
    )
    assert code == 0
    assert audit.read_text(encoding="utf-8").startswith("# Intervention-Effects Registry Audit")


def test_forbidden_key_fragment_fails(tmp_path: Path) -> None:
    doc = yaml.safe_load(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
    doc["intervention_classes"][0]["notes_on_threshold_context"] = "forbidden key fragment"
    reg = tmp_path / "bad.yaml"
    reg.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    audit = tmp_path / "audit.md"
    code = main(
        [
            "--registry",
            str(reg),
            "--aliases",
            str(DEFAULT_ALIASES),
            "--audit-path",
            str(audit),
        ]
    )
    assert code == 1
    body = audit.read_text(encoding="utf-8")
    assert "threshold" in body.lower()


def test_exactly_eight_approved_ids_enforced(tmp_path: Path) -> None:
    doc = yaml.safe_load(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
    classes = doc["intervention_classes"]
    ids = {c["intervention_class_id"] for c in classes}
    assert ids == APPROVED_CLASS_IDS


def test_schema_lists_match_validator_fragments() -> None:
    schema_path = ROOT / "knowledge_bus" / "schema" / "intervention_effects_registry_schema_v1.yaml"
    sdoc = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    listed = frozenset(sdoc["forbidden_key_fragments"])
    assert listed == frozenset(FORBIDDEN_KEY_FRAGMENTS)


def test_alias_map_targets_only_approved_classes() -> None:
    adoc = yaml.safe_load(DEFAULT_ALIASES.read_text(encoding="utf-8"))
    assert set(adoc["allowed_target_class_ids"]) == APPROVED_CLASS_IDS
    for row in adoc["aliases"]:
        assert row["intervention_class_id"] in APPROVED_CLASS_IDS
