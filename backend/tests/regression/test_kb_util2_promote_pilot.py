"""KB-UTIL-2-PROMOTE-PILOT regression checks for single-package promotion."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import yaml
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO = Path(__file__).resolve().parents[3]
LEGACY_DIR = REPO / "knowledge_bus/packages/pkg_s24_creatinine_high_renal"
PROMOTED_DIR = REPO / "knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1"
CURRENT_STATUS = REPO / "knowledge_bus/current/latest_knowledge_status.json"
COMPILER_SCRIPT = REPO / "backend/scripts/compile_pass3_pilot_artifacts.py"


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
    subprocess.run(
        [
            sys.executable,
            str(COMPILER_SCRIPT),
            "--normalize-promoted-manifest",
            str(PROMOTED_DIR.relative_to(REPO)).replace("\\", "/"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
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
    assert compile_manifest["output_root"] == (
        "knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/"
        "pkg_creatinine_high_renal_pass3_v1"
    )
    assert compile_manifest["promotion_status"] == "compiled_not_promoted"
    assert compile_manifest["runtime_active"] is False


def test_promoted_candidate_collision_blocker_classified_real():
    compile_manifest = yaml.safe_load((PROMOTED_DIR / "compile_manifest.yaml").read_text(encoding="utf-8"))
    assert (
        compile_manifest["runtime_activation_blocker"]
        == "real_duplicate_activation_key_collision_with_pkg_kb52c_creatinine_high_reduced_glomerular_filtration"
    )


def test_promotion_validators_do_not_update_latest_knowledge_status():
    if not CURRENT_STATUS.is_file():
        return
    before = CURRENT_STATUS.read_bytes()
    subprocess.run(
        [
            sys.executable,
            str(REPO / "backend/scripts/validate_knowledge_package.py"),
            "--package-dir",
            str(PROMOTED_DIR),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(REPO / "backend/scripts/validate_promoted_signal_intelligence.py"),
            "--model",
            str(PROMOTED_DIR / "promoted_signal_intelligence.yaml"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    assert CURRENT_STATUS.read_bytes() == before


def test_wire1_creatinine_runtime_authority_preflight_activation_keys():
    package_roots = [
        REPO / "knowledge_bus/packages/pkg_s24_creatinine_high_renal/signal_library.yaml",
        REPO / "knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/signal_library.yaml",
    ]
    rows = []
    for signal_library_path in package_roots:
        activation_key, source_spec_id, package_id = resolve_activation_identity(
            signal_id="signal_creatinine_high",
            signal_library_path=signal_library_path,
        )
        rows.append((package_id, activation_key, source_spec_id))
    assert rows == [
        (
            "pkg_s24_creatinine_high_renal",
            "signal_creatinine_high::inv_creatinine_high_renal",
            "inv_creatinine_high_renal",
        ),
        (
            "pkg_kb52c_creatinine_high_reduced_glomerular_filtration",
            "signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration",
            "inv_creatinine_high_reduced_glomerular_filtration",
        ),
    ]
    assert len({row[1] for row in rows}) == len(rows)


def test_wire1_candidate_is_not_runtime_loaded_under_packages_directory():
    assert not (REPO / "knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1").exists()
    assert PROMOTED_DIR.is_dir()


def test_wire1_candidate_equivalent_to_pkg_kb52c_override_rule_signature():
    kb52c_lib = yaml.safe_load(
        (
            REPO
            / "knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/signal_library.yaml"
        ).read_text(encoding="utf-8")
    )
    candidate_lib = yaml.safe_load((PROMOTED_DIR / "signal_library.yaml").read_text(encoding="utf-8"))
    kb52c_rule = kb52c_lib["signals"][0]["override_rules"]
    candidate_rule = candidate_lib["signals"][0]["override_rules"]
    assert kb52c_rule == candidate_rule


def test_wire1_register_records_activation_refusal_and_rollback_path():
    register = yaml.safe_load(
        (REPO / "knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    decision = register["decisions"][0]
    assert decision["wire1_collision_decision"]["decision"] == "D_candidate_equivalent_to_pkg_kb52c_retain_one_canonical"
    assert decision["wire1_runtime_activation_outcome"]["activation_performed"] is False
    assert (
        decision["wire1_runtime_activation_outcome"]["rollback_path"]
        == "no_runtime_switch_performed_existing_runtime_authority_unchanged"
    )

