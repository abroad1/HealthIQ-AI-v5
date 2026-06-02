"""CONTEXT-MOD-1 — context modifier catalogue validator regression tests."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
CATALOGUE = REPO / "knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml"
VALIDATOR = REPO / "backend/scripts/validate_context_modifier_catalogue.py"


def _run_validator(catalogue_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--catalogue", str(catalogue_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _load_catalogue() -> dict:
    return yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))


def test_valid_catalogue_passes():
    proc = _run_validator(CATALOGUE)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation_status: PASS" in proc.stdout


def test_duplicate_modifier_id_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"].append(copy.deepcopy(broken["modifiers"][0]))
    path = tmp_path / "dup_id.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "duplicate modifier_id" in proc.stderr


def test_unknown_modifier_type_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"][0]["modifier_type"] = "not_a_real_type"
    path = tmp_path / "bad_type.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "unknown modifier_type" in proc.stderr


def test_unknown_modifier_effect_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"][0]["modifier_effect"] = "mystery_effect"
    path = tmp_path / "bad_effect.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "unknown modifier_effect" in proc.stderr


def test_unknown_allowed_layer_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"][0]["allowed_layer"] = "Layer_Z"
    path = tmp_path / "bad_layer.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "unknown allowed_layer" in proc.stderr


def test_runtime_consumed_true_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["runtime_consumed"] = True
    path = tmp_path / "runtime_consumed.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "runtime_consumed must be false" in proc.stderr


def test_referenced_frame_ids_must_exist(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"][0]["applies_to"]["medical_frame_ids"] = ["frame_does_not_exist"]
    path = tmp_path / "bad_frame.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "not in identity index" in proc.stderr


def test_empty_medical_frame_ids_allowed(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    for mod in broken["modifiers"]:
        mod["applies_to"]["medical_frame_ids"] = []
    path = tmp_path / "empty_frames.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode == 0, proc.stderr


def test_runtime_active_true_fails(tmp_path: Path):
    doc = _load_catalogue()
    broken = copy.deepcopy(doc)
    broken["modifiers"][0]["runtime_active"] = True
    path = tmp_path / "runtime_active.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "runtime_active must be false" in proc.stderr


def test_catalogue_marked_non_runtime():
    doc = _load_catalogue()
    assert doc["runtime_consumed"] is False
    assert doc["status"] == "draft_governance_non_runtime"
    assert all(m.get("runtime_active") is False for m in doc["modifiers"])
