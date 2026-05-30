"""ARCH-RT-5D — package provenance classification, compile manifest validator, estate linkage."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from core.knowledge.compiled_hypothesis import get_compiled_hypothesis_artefact
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact
from core.knowledge.launch_estate_v1 import estate_index_path, manifests_dir, resolve_compile_manifest_ref
from core.knowledge.package_provenance_scan_v1 import (
    ARCH_RT5D_CLASSIFICATIONS,
    INFERRED_CARD_MARKERS,
    classification_counts,
    refresh_compile_manifest_hashes,
    scan_all_package_provenance,
)

_REPO = Path(__file__).resolve().parents[3]
_SCHEMA = _REPO / "knowledge_bus" / "schema" / "compile_manifest_schema_v1.yaml"
_VALIDATOR = _REPO / "backend" / "scripts" / "validate_compile_manifest.py"
_LAUNCH_MANIFESTS = (
    "arch_rt3_glycaemic_card_evidence.yaml",
    "arch_rt4_vitamin_d_hypothesis.yaml",
    "arch_rt5b_lipid_transport_card_evidence.yaml",
    "arch_rt5b_homocysteine_pathway_card_evidence.yaml",
    "arch_rt5b_vascular_strain_card_evidence.yaml",
    "arch_rt5b_insulin_metabolic_card_evidence.yaml",
    "arch_rt5b_enzyme_pattern_card_evidence.yaml",
    "arch_rt5b_processing_context_card_evidence.yaml",
)

import importlib.util

_validate_spec = importlib.util.spec_from_file_location("validate_compile_manifest", _VALIDATOR)
_validate_mod = importlib.util.module_from_spec(_validate_spec)
assert _validate_spec.loader is not None
_validate_spec.loader.exec_module(_validate_mod)
validate_compile_manifest = _validate_mod.validate_compile_manifest


def test_all_packages_classified():
    rows = scan_all_package_provenance()
    assert len(rows) == 186
    for row in rows:
        assert row.classification in ARCH_RT5D_CLASSIFICATIONS


def test_classification_counts_match_inventory():
    rows = scan_all_package_provenance()
    counts = classification_counts(rows)
    assert counts["source_document_derived"] == 31
    assert counts["batch_json_blocked_pending_spec_extraction"] == 142
    assert counts["architecture_doc_source_blocked"] == 11
    assert counts["provenance_gap"] == 1
    assert counts["retire_candidate"] == 1
    assert sum(counts.values()) == 186


def test_inferred_not_treated_as_explicit_on_manifests():
    rows = scan_all_package_provenance()
    assert all(r.source_spec_id_on_manifest is None for r in rows)


def test_kb52c_packages_classified_batch_blocked():
    rows = scan_all_package_provenance()
    kb52c = [r for r in rows if r.package_id.startswith("pkg_kb52c_")]
    assert len(kb52c) == 67
    assert all(r.classification == "batch_json_blocked_pending_spec_extraction" for r in kb52c)


def test_five_inferred_card_markers_registered():
    assert len(INFERRED_CARD_MARKERS) == 5
    markers = {m for m, _ in INFERRED_CARD_MARKERS}
    assert markers == {"total_cholesterol", "tc_hdl_ratio", "insulin", "ast", "bilirubin"}
    assert all(cls == "package_manifest_inferred" for _, cls in INFERRED_CARD_MARKERS)


def test_compile_run_id_must_equal_compile_id():
    schema = yaml.safe_load(_SCHEMA.read_text(encoding="utf-8"))
    bad = {
        "compile_id": "a",
        "compile_run_id": "b",
        "compiler_name": "x",
        "compiler_version": "1.0.0",
        "compile_mode": "card_evidence",
        "source_contract_version": "1.0.0",
        "source_specs": [
            {
                "source_spec_id": "inv_test",
                "source_path": "knowledge_bus/research/investigation_specs/inv_hba1c_high_glycaemia_v1.yaml",
                "source_hash": "abc",
                "source_hash_algorithm": "sha256",
            }
        ],
        "outputs": [
            {
                "output_type": "health_system_card_evidence",
                "output_path": "knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml",
                "output_hash": "def",
                "output_hash_algorithm": "sha256",
            }
        ],
        "translation_rules_version": "1.0.0",
        "compiled_at_utc": "2026-05-30T00:00:00Z",
        "compiled_by": "test",
        "provenance_status": "pilot_evidence_only",
    }
    errors = validate_compile_manifest(bad, schema)
    assert any("compile_run_id must equal compile_id" in e for e in errors)


@pytest.mark.parametrize("name", _LAUNCH_MANIFESTS)
def test_launch_manifests_validate(name: str):
    path = manifests_dir() / name
    schema = yaml.safe_load(_SCHEMA.read_text(encoding="utf-8"))
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = validate_compile_manifest(manifest, schema)
    assert errors == [], errors
    proc = subprocess.run(
        [sys.executable, str(_VALIDATOR), "--manifest", str(path)],
        cwd=_REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_launch_manifest_hashes_not_pending():
    for name in _LAUNCH_MANIFESTS:
        manifest = yaml.safe_load((manifests_dir() / name).read_text(encoding="utf-8"))
        for spec in manifest.get("source_specs") or []:
            assert spec.get("source_hash") != "pending_inventory_refresh", name
        for out in manifest.get("outputs") or []:
            assert out.get("output_hash") != "pending_inventory_refresh", name


def test_manifest_refs_resolve_from_compiled_artefacts():
    card = get_card_evidence_artefact("wave1_met_glycaemic_control")
    hyp = get_compiled_hypothesis_artefact("signal_vitamin_d_low")
    assert resolve_compile_manifest_ref(card.compile_manifest_ref) is not None
    assert resolve_compile_manifest_ref(hyp.compile_manifest_ref) is not None


def test_estate_index_covers_launch_artefacts():
    payload = yaml.safe_load(estate_index_path().read_text(encoding="utf-8"))
    assert len(payload["card_evidence_artefacts"]) == 7
    assert payload["compiled_hypothesis_artefacts"][0]["runtime_authority"] == "runtime_promoted_compiled"


def test_refresh_hashes_is_deterministic():
    path = manifests_dir() / "arch_rt3_glycaemic_card_evidence.yaml"
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    a, _ = refresh_compile_manifest_hashes(manifest, repo=_REPO)
    b, _ = refresh_compile_manifest_hashes(manifest, repo=_REPO)
    assert a["source_specs"][0]["source_hash"] == b["source_specs"][0]["source_hash"]
