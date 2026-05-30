"""ARCH-RT-5 — launch estate index, compile manifests, carry-forward protections."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.knowledge.compiled_hypothesis import (
    load_compiled_hypothesis_artefact,
    runtime_summary_for_hypothesis,
)
from core.knowledge.health_system_card_evidence import load_card_evidence_artefact
from core.knowledge.launch_estate_v1 import (
    estate_index_path,
    manifests_dir,
    resolve_compile_manifest_ref,
    scan_package_provenance,
    wave1_subsystem_authority_rows,
)

_REPO = Path(__file__).resolve().parents[3]


def test_estate_index_loads():
    payload = yaml.safe_load(estate_index_path().read_text(encoding="utf-8"))
    assert payload["estate_id"] == "healthiq_launch_estate_v1"
    assert len(payload["card_evidence_artefacts"]) == 1
    assert len(payload["compiled_hypothesis_artefacts"]) == 1
    assert len(payload["wave1_subsystems_legacy_hard_coded"]["subsystem_ids"]) == 6


def test_compile_manifest_refs_resolve():
    card = load_card_evidence_artefact("wave1_met_glycaemic_control")
    hyp = load_compiled_hypothesis_artefact("signal_vitamin_d_low")
    assert resolve_compile_manifest_ref(card.compile_manifest_ref) is not None
    assert resolve_compile_manifest_ref(hyp.compile_manifest_ref) is not None


def test_manifest_files_validate_via_script():
    import subprocess
    import sys

    for name in ("arch_rt3_glycaemic_card_evidence.yaml", "arch_rt4_vitamin_d_hypothesis.yaml"):
        path = manifests_dir() / name
        proc = subprocess.run(
            [sys.executable, str(_REPO / "backend/scripts/validate_compile_manifest.py"), "--manifest", str(path)],
            cwd=_REPO,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr


def test_wave1_subsystems_classified():
    rows = wave1_subsystem_authority_rows()
    assert len(rows) == 7
    compiled = [r for r in rows if r["active_authority"] == "compiled_card_evidence"]
    legacy = [r for r in rows if r["active_authority"] == "hard_coded_python"]
    assert len(compiled) == 1
    assert len(legacy) == 6


def test_package_scan_returns_rows():
    rows = scan_package_provenance()
    assert len(rows) >= 180
    classes = {r.classification for r in rows}
    assert "blocked_pending_spec_extraction" in classes


def test_presentation_mapping_uses_summary_template():
    artefact = load_compiled_hypothesis_artefact("signal_vitamin_d_low")
    row = artefact.hypotheses[0]
    summary = runtime_summary_for_hypothesis(row)
    assert "25-hydroxyvitamin D" in summary
    assert row.summary_template
    assert row.summary_template.strip() in summary


def test_compiled_hypothesis_still_validates_after_rt5_fields():
    load_compiled_hypothesis_artefact("signal_vitamin_d_low")
