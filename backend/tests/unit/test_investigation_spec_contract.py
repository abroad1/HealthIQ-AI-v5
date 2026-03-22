"""Investigation spec contract validation (v2 legacy / v3 intelligence-aligned)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATE_INV = REPO_ROOT / "backend" / "scripts" / "validate_investigation_spec.py"
V3_FIXTURE = REPO_ROOT / "backend" / "tests" / "fixtures" / "investigation_spec_v3_valid.yaml"
V2_FIXTURE = REPO_ROOT / "knowledge_bus" / "research" / "investigation_specs" / "inv_plt_high_thrombocytosis.yaml"


def _run(spec: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATE_INV),
            "--spec",
            str(spec),
            "--audit-path",
            str(REPO_ROOT / "backend" / "artifacts" / "investigation_spec_audit.md"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_v3_fixture_passes():
    proc = _run(V3_FIXTURE)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "contract_mode: v3" in proc.stdout


def test_v2_legacy_passes_without_contract_version():
    proc = _run(V2_FIXTURE)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "contract_mode: v2" in proc.stdout


def test_v3_fails_without_differential_relationship_kind(tmp_path):
    doc = yaml.safe_load(V3_FIXTURE.read_text(encoding="utf-8"))
    for row in doc["supporting_markers"]:
        if row["biomarker_id"] == "ggt":
            row["relationship_kind"] = "mechanism"
            row["role"] = "mechanism_marker"
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    proc = _run(p)
    assert proc.returncode == 1
    assert "differential" in proc.stderr


def test_v3_fails_single_hypothesis(tmp_path):
    doc = yaml.safe_load(V3_FIXTURE.read_text(encoding="utf-8"))
    doc["hypotheses"] = [doc["hypotheses"][0]]
    doc["hypothesis_ranking"] = {"ordered_hypothesis_ids": [doc["hypotheses"][0]["hypothesis_id"]]}
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    proc = _run(p)
    assert proc.returncode == 1
    assert "at least 2" in proc.stderr
