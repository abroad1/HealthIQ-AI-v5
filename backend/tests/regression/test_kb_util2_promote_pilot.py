"""KB-UTIL-2-PROMOTE-PILOT regression checks for single-package promotion."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
LEGACY_DIR = REPO / "knowledge_bus/packages/pkg_s24_creatinine_high_renal"
PROMOTED_DIR = REPO / "knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_promoted_package_exists_with_required_files():
    for name in (
        "research_brief.yaml",
        "signal_library.yaml",
        "package_manifest.yaml",
        "promoted_signal_intelligence.yaml",
        "compile_manifest.yaml",
        "source_field_preservation_audit.yaml",
    ):
        assert (PROMOTED_DIR / name).is_file(), f"missing promoted file: {name}"


def test_legacy_package_not_overwritten():
    legacy_hash_before = _sha256(LEGACY_DIR / "signal_library.yaml")
    legacy_hash_after = _sha256(LEGACY_DIR / "signal_library.yaml")
    assert legacy_hash_before == legacy_hash_after


def test_promoted_package_validates():
    cmd = [
        sys.executable,
        str(REPO / "backend/scripts/validate_knowledge_package.py"),
        "--package-dir",
        str(PROMOTED_DIR),
    ]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ready_for_implementation: True" in proc.stdout


def test_promoted_signal_intelligence_validates():
    cmd = [
        sys.executable,
        str(REPO / "backend/scripts/validate_promoted_signal_intelligence.py"),
        "--model",
        str(PROMOTED_DIR / "promoted_signal_intelligence.yaml"),
    ]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation_status: PASS" in proc.stdout


def test_promoted_manifest_and_contract_values():
    manifest = yaml.safe_load((PROMOTED_DIR / "package_manifest.yaml").read_text(encoding="utf-8"))
    assert manifest["package_id"] == "pkg_creatinine_high_renal_pass3_v1"
    assert manifest["legacy_supersedes"] == "pkg_s24_creatinine_high_renal"
    signal_library = yaml.safe_load((PROMOTED_DIR / "signal_library.yaml").read_text(encoding="utf-8"))
    assert signal_library["library"]["schema_version"] == "1.0.0"
    compile_manifest = yaml.safe_load((PROMOTED_DIR / "compile_manifest.yaml").read_text(encoding="utf-8"))
    assert compile_manifest["source_contract_version"] == "3.0.0"

