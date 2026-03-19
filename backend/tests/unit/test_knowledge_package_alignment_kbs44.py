import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATE_MANIFEST_SCRIPT = REPO_ROOT / "backend" / "scripts" / "validate_package_manifest.py"
VALIDATE_PACKAGE_SCRIPT = REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
MANIFEST_SCHEMA_PATH = REPO_ROOT / "knowledge_bus" / "schema" / "package_manifest_schema.yaml"
RUN_KNOWLEDGE_PACKAGE_SCRIPT = REPO_ROOT / "backend" / "scripts" / "run_knowledge_package.py"


spec = importlib.util.spec_from_file_location("run_knowledge_package", RUN_KNOWLEDGE_PACKAGE_SCRIPT)
assert spec is not None and spec.loader is not None
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)


def _write_manifest_fixture(package_dir: Path, manifest_payload: dict) -> Path:
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "research_brief.yaml").write_text("summary: test\n", encoding="utf-8")
    (package_dir / "signal_library.yaml").write_text("library: {}\nsignals: []\n", encoding="utf-8")
    manifest_path = package_dir / "package_manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest_payload, sort_keys=False), encoding="utf-8")
    return manifest_path


def test_manifest_validator_fails_when_behavioural_impact_required_and_missing(tmp_path):
    manifest_path = _write_manifest_fixture(
        tmp_path / "pkg_fixture",
        {
            "package_id": "pkg_fixture",
            "package_version": "1.0.0",
            "research_brief": "research_brief.yaml",
            "signal_library": "signal_library.yaml",
        },
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_MANIFEST_SCRIPT),
            "--manifest",
            str(manifest_path),
            "--schema",
            str(MANIFEST_SCHEMA_PATH),
            "--require-behavioural-impact",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "validation_status: FAIL" in proc.stdout
    assert "errors: 1" in proc.stdout


def test_manifest_validator_fails_for_invalid_behavioural_impact_enum(tmp_path):
    manifest_path = _write_manifest_fixture(
        tmp_path / "pkg_fixture",
        {
            "package_id": "pkg_fixture",
            "package_version": "1.0.0",
            "research_brief": "research_brief.yaml",
            "signal_library": "signal_library.yaml",
            "behavioural_impact": "MEDIUM",
        },
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_MANIFEST_SCRIPT),
            "--manifest",
            str(manifest_path),
            "--schema",
            str(MANIFEST_SCHEMA_PATH),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "validation_status: FAIL" in proc.stdout
    assert "errors: 1" in proc.stdout


def test_manifest_validator_fails_when_engine_compatibility_required_and_missing(tmp_path):
    manifest_path = _write_manifest_fixture(
        tmp_path / "pkg_fixture",
        {
            "package_id": "pkg_fixture",
            "package_version": "1.0.0",
            "research_brief": "research_brief.yaml",
            "signal_library": "signal_library.yaml",
            "behavioural_impact": "LOW",
        },
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_MANIFEST_SCRIPT),
            "--manifest",
            str(manifest_path),
            "--schema",
            str(MANIFEST_SCHEMA_PATH),
            "--require-engine-compatibility",
            "--authoritative-engine-compatibility",
            "v5.x",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "validation_status: FAIL" in proc.stdout
    assert "errors: 1" in proc.stdout


def test_validate_knowledge_package_status_is_deterministic_for_identical_input():
    package_dir = REPO_ROOT / "knowledge_bus" / "packages" / "pkg_s24_hba1c_high_glycaemia"
    status_path = REPO_ROOT / "backend" / "artifacts" / "knowledge_status.json"

    cmd = [
        sys.executable,
        str(VALIDATE_PACKAGE_SCRIPT),
        "--package-dir",
        str(package_dir),
    ]
    proc_a = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    status_a = json.loads(status_path.read_text(encoding="utf-8"))
    proc_b = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    status_b = json.loads(status_path.read_text(encoding="utf-8"))

    assert proc_a.returncode == 0
    assert proc_b.returncode == 0
    assert "ready_for_implementation: True" in proc_a.stdout
    assert "ready_for_implementation: True" in proc_b.stdout
    assert status_a == status_b


def test_run_knowledge_package_resolves_pkg_and_legacy_kbp_payloads():
    assert (
        lifecycle.resolve_active_package_dir_name({"package_dir": "pkg_0042", "package_id": "KBP-0042"})
        == "pkg_0042"
    )
    assert lifecycle.resolve_active_package_dir_name({"package_id": "pkg_existing"}) == "pkg_existing"
    assert lifecycle.resolve_active_package_dir_name({"package_id": "KBP-0011"}) == "pkg_0011"


def test_run_knowledge_package_start_creates_pkg_directory(monkeypatch, tmp_path):
    kb_root = tmp_path / "knowledge_bus"
    packages_dir = kb_root / "packages"
    current_dir = kb_root / "current"

    monkeypatch.setattr(lifecycle, "KNOWLEDGE_BUS_DIR", kb_root)
    monkeypatch.setattr(lifecycle, "PACKAGES_DIR", packages_dir)
    monkeypatch.setattr(lifecycle, "CURRENT_DIR", current_dir)
    monkeypatch.setattr(lifecycle, "ACTIVE_PACKAGE_PATH", current_dir / "active_package.json")
    monkeypatch.setattr(lifecycle, "CURRENT_STATUS_PATH", current_dir / "knowledge_status.json")
    monkeypatch.setattr(lifecycle, "LATEST_STATUS_PATH", current_dir / "latest_knowledge_status.json")
    monkeypatch.setattr(lifecycle, "is_working_tree_clean", lambda: True)

    rc = lifecycle.start_command()
    assert rc == 0
    active_payload = json.loads((current_dir / "active_package.json").read_text(encoding="utf-8"))
    assert active_payload["package_dir"] == "pkg_0001"
    assert active_payload["package_id"] == "KBP-0001"
    assert (packages_dir / "pkg_0001").exists()


def test_run_knowledge_package_validate_writes_deterministic_latest_status(monkeypatch, tmp_path):
    kb_root = tmp_path / "knowledge_bus"
    packages_dir = kb_root / "packages"
    current_dir = kb_root / "current"
    artifacts_dir = tmp_path / "backend" / "artifacts"
    target_pkg_dir = packages_dir / "pkg_0007"
    target_pkg_dir.mkdir(parents=True, exist_ok=True)
    current_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    active_payload = {
        "package_dir": "pkg_0007",
        "package_id": "KBP-0007",
        "status": "IN_PROGRESS",
    }
    (current_dir / "active_package.json").write_text(
        json.dumps(active_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    fixed_status = {
        "manifest_validation": "PASS",
        "research_validation": "PASS",
        "signal_validation": "PASS",
        "ready_for_implementation": True,
    }
    (artifacts_dir / "knowledge_status.json").write_text(
        json.dumps(fixed_status, indent=2) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(lifecycle, "KNOWLEDGE_BUS_DIR", kb_root)
    monkeypatch.setattr(lifecycle, "PACKAGES_DIR", packages_dir)
    monkeypatch.setattr(lifecycle, "CURRENT_DIR", current_dir)
    monkeypatch.setattr(lifecycle, "ACTIVE_PACKAGE_PATH", current_dir / "active_package.json")
    monkeypatch.setattr(lifecycle, "CURRENT_STATUS_PATH", current_dir / "knowledge_status.json")
    monkeypatch.setattr(lifecycle, "LATEST_STATUS_PATH", current_dir / "latest_knowledge_status.json")
    monkeypatch.setattr(lifecycle, "ARTIFACT_STATUS_PATH", artifacts_dir / "knowledge_status.json")
    monkeypatch.setattr(lifecycle, "VALIDATOR_SCRIPT_PATH", tmp_path / "validate_knowledge_package.py")

    class _Proc:
        returncode = 0

    monkeypatch.setattr(lifecycle.subprocess, "run", lambda *args, **kwargs: _Proc())

    rc_a = lifecycle.validate_command()
    latest_a = (current_dir / "latest_knowledge_status.json").read_text(encoding="utf-8")
    rc_b = lifecycle.validate_command()
    latest_b = (current_dir / "latest_knowledge_status.json").read_text(encoding="utf-8")

    assert rc_a == 0
    assert rc_b == 0
    assert latest_a == latest_b

