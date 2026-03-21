"""
KB-S45 batch-1 ingestion: evaluator smoke tests against KB-S45d individual packages.

Validation of all ten hardened packages lives in test_kb_s45d_batch1_packages.py.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

from core.analytics.signal_evaluator import SignalEvaluator

_REPO_ROOT = Path(__file__).resolve().parents[3]
_VALIDATE_SCRIPT = _REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
_SOURCE_SPEC = (
    _REPO_ROOT
    / "knowledge_bus"
    / "research"
    / "investigation_specs"
    / "investigation-spec-collection-batch1-10.json"
)
_STATUS_PATH = _REPO_ROOT / "backend" / "artifacts" / "knowledge_status.json"

_KB_S45D_PATH = Path(__file__).resolve().parent / "test_kb_s45d_batch1_packages.py"
_spec = importlib.util.spec_from_file_location("test_kb_s45d_batch1_packages", _KB_S45D_PATH)
assert _spec and _spec.loader
_kb_s45d = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_kb_s45d)

KB_S45D_PACKAGE_DIRS = _kb_s45d.KB_S45D_PACKAGE_DIRS
SIGNAL_ID_TO_PACKAGE_DIR = _kb_s45d.SIGNAL_ID_TO_PACKAGE_DIR
_EXPECTED_SIGNAL_IDS = _kb_s45d.EXPECTED_SIGNAL_IDS


def test_kb_s45_batch1_source_json_is_valid_and_matches_expected_ids():
    raw = json.loads(_SOURCE_SPEC.read_text(encoding="utf-8"))
    assert isinstance(raw, list) and len(raw) == 10
    ids = {entry["signal_id"] for entry in raw if isinstance(entry, dict)}
    assert ids == _EXPECTED_SIGNAL_IDS


def test_kb_s45_batch1_representative_package_validates_cleanly():
    proc = subprocess.run(
        [
            sys.executable,
            str(_VALIDATE_SCRIPT),
            "--package-dir",
            str(_REPO_ROOT / "knowledge_bus" / "packages" / KB_S45D_PACKAGE_DIRS[0]),
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "signal_validation: PASS" in proc.stdout


def test_kb_s45_validate_knowledge_package_status_is_deterministic():
    cmd = [
        sys.executable,
        str(_VALIDATE_SCRIPT),
        "--package-dir",
        str(_REPO_ROOT / "knowledge_bus" / "packages" / KB_S45D_PACKAGE_DIRS[0]),
    ]
    subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True, check=True)
    a = json.loads(_STATUS_PATH.read_text(encoding="utf-8"))
    subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True, check=True)
    b = json.loads(_STATUS_PATH.read_text(encoding="utf-8"))
    assert a == b


def _load_one_signal(signal_id: str) -> dict:
    dirname = SIGNAL_ID_TO_PACKAGE_DIR[signal_id]
    lib_path = _REPO_ROOT / "knowledge_bus" / "packages" / dirname / "signal_library.yaml"
    payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
    for s in payload.get("signals", []):
        if isinstance(s, dict) and s.get("signal_id") == signal_id:
            return dict(s)
    raise AssertionError(f"Missing signal {signal_id}")


def _evaluator_for(signal_id: str) -> SignalEvaluator:
    signal = _load_one_signal(signal_id)

    class _Reg:
        @staticmethod
        def get_all_signals():
            return [signal]

    return SignalEvaluator(_Reg())


def test_kb_s45_lab_range_activation_suboptimal_for_high_primary():
    ev = _evaluator_for("signal_apob_atherogenic")
    out = ev.evaluate_all(
        signal_biomarkers={"apob": 1.5, "ldl_cholesterol": 2.5},
        signal_derived={},
        lab_ranges={"apob": {"min": 0.4, "max": 1.2}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "suboptimal"


def test_kb_s45_lab_range_boundary_override_escalates_apob_when_ldl_high():
    ev = _evaluator_for("signal_apob_atherogenic")
    out = ev.evaluate_all(
        signal_biomarkers={"apob": 1.5, "ldl_cholesterol": 5.0},
        signal_derived={},
        lab_ranges={
            "apob": {"min": 0.4, "max": 1.2},
            "ldl_cholesterol": {"min": 0.0, "max": 3.0},
        },
    )
    assert len(out) == 1
    assert out[0].signal_state == "at_risk"


def test_kb_s45_lab_range_activation_suboptimal_for_low_primary():
    ev = _evaluator_for("signal_active_b12_deficiency")
    out = ev.evaluate_all(
        signal_biomarkers={"active_b12": 20.0, "homocysteine": 10.0, "mcv": 88.0},
        signal_derived={},
        lab_ranges={"active_b12": {"min": 25.0, "max": 165.0}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "suboptimal"


def test_kb_s45_homocysteine_lab_boundary_override_escalates_active_b12():
    ev = _evaluator_for("signal_active_b12_deficiency")
    out = ev.evaluate_all(
        signal_biomarkers={"active_b12": 20.0, "homocysteine": 18.0, "mcv": 88.0},
        signal_derived={},
        lab_ranges={
            "active_b12": {"min": 25.0, "max": 165.0},
            "homocysteine": {"min": 5.0, "max": 15.0},
        },
    )
    assert len(out) == 1
    assert out[0].signal_state == "at_risk"
