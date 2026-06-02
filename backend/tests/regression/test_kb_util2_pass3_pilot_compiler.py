"""KB-UTIL-2-PILOT — deterministic Pass 3 pilot compiler regression tests."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
COMPILER_SCRIPT = REPO / "backend/scripts/compile_pass3_pilot_artifacts.py"
OUTPUT_ROOT = REPO / "knowledge_bus/generated_pilot/kb_util_2_pilot"
RUNTIME_PKG = REPO / "knowledge_bus/packages/pkg_s24_creatinine_high_renal"
CURRENT_STATUS = REPO / "knowledge_bus/current/latest_knowledge_status.json"
PASS3_TOP_LEVEL = (
    "investigation_spec_contract_version",
    "spec_id",
    "signal_id",
    "research_domain",
    "primary_marker",
    "trigger_direction",
    "activation",
    "states",
    "supporting_markers",
    "hypotheses",
    "hypothesis_ranking",
    "confirmatory_tests",
    "override_rules",
    "evidence",
    "narrative",
)


def _load_compiler_module():
    spec = importlib.util.spec_from_file_location("compile_pass3_pilot", COMPILER_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_pilot_output_directories_exist():
    for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency"):
        root = OUTPUT_ROOT / pkg
        for name in (
            "research_brief.yaml",
            "signal_library.yaml",
            "package_manifest.yaml",
            "promoted_signal_intelligence.yaml",
            "compile_manifest.yaml",
            "source_field_preservation_audit.yaml",
        ):
            assert (root / name).is_file(), f"missing {pkg}/{name}"


def test_compiler_deterministic_hashes():
    mod = _load_compiler_module()
    before = {
        pkg: _sha256_file(OUTPUT_ROOT / pkg / "compile_manifest.yaml")
        for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency")
    }
    mod.compile_all()
    after = {
        pkg: _sha256_file(OUTPUT_ROOT / pkg / "compile_manifest.yaml")
        for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency")
    }
    assert before == after


def test_preservation_audit_covers_pass3_top_level_fields():
    audit_path = OUTPUT_ROOT / "pkg_s24_creatinine_high_renal/source_field_preservation_audit.yaml"
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    fields = audit.get("fields") or {}
    for name in PASS3_TOP_LEVEL:
        assert name in fields, f"missing audit field {name}"


def test_advisory1_compile_manifest_has_source_contract_version():
    for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency"):
        manifest = yaml.safe_load((OUTPUT_ROOT / pkg / "compile_manifest.yaml").read_text(encoding="utf-8"))
        assert manifest.get("source_contract_version") == "3.0.0"


def test_advisory2_signal_library_schema_version_is_governed_v1():
    for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency"):
        signal_lib = yaml.safe_load((OUTPUT_ROOT / pkg / "signal_library.yaml").read_text(encoding="utf-8"))
        assert (signal_lib.get("library") or {}).get("schema_version") == "1.0.0"


def test_generated_manifest_marked_non_runtime():
    for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency"):
        manifest = yaml.safe_load((OUTPUT_ROOT / pkg / "package_manifest.yaml").read_text(encoding="utf-8"))
        assert manifest.get("pilot_status") == "generated_non_runtime"
        assert manifest.get("behavioural_impact") == "NONE"
        compile_manifest = yaml.safe_load((OUTPUT_ROOT / pkg / "compile_manifest.yaml").read_text(encoding="utf-8"))
        assert compile_manifest.get("runtime_active") is False


def test_runtime_packages_not_overwritten():
    legacy_hash = _sha256_file(RUNTIME_PKG / "signal_library.yaml")
    mod = _load_compiler_module()
    mod.compile_all()
    assert _sha256_file(RUNTIME_PKG / "signal_library.yaml") == legacy_hash


def test_knowledge_package_validators_pass_on_pilots():
    for pkg in ("pkg_s24_creatinine_high_renal", "pkg_s24_ferritin_low_iron_deficiency"):
        result = subprocess.run(
            [
                sys.executable,
                str(REPO / "backend/scripts/validate_knowledge_package.py"),
                "--package-dir",
                str(OUTPUT_ROOT / pkg),
            ],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert "ready_for_implementation: True" in result.stdout


def test_current_knowledge_status_not_updated_by_compiler():
    if not CURRENT_STATUS.is_file():
        return
    before = CURRENT_STATUS.read_bytes()
    mod = _load_compiler_module()
    mod.compile_all()
    assert CURRENT_STATUS.read_bytes() == before


def test_exact_signal_id_match_for_creatinine_pilot():
    psi = yaml.safe_load(
        (OUTPUT_ROOT / "pkg_s24_creatinine_high_renal/promoted_signal_intelligence.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert psi["translation"]["investigation_spec_id"] == "inv_creatinine_high_reduced_glomerular_filtration"
    assert psi["signals"][0]["signal_id"] == "signal_creatinine_high"
