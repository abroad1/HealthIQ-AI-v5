"""MED-FRAME-2 — medical frame identity index validator regression tests."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
INDEX = REPO / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
VALIDATOR = REPO / "backend/scripts/validate_medical_frame_identity_index.py"


def _run_validator(index_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--index", str(index_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _load_index() -> dict:
    return yaml.safe_load(INDEX.read_text(encoding="utf-8"))


def test_valid_creatinine_frame_index_passes():
    proc = _run_validator(INDEX)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation_status: PASS" in proc.stdout


def test_index_models_four_creatinine_frames():
    doc = _load_index()
    frames = doc["signal_families"][0]["frames"]
    assert len(frames) == 4
    frame_ids = {f["medical_frame_id"] for f in frames}
    assert "frame_creatinine_reduced_glomerular_filtration" in frame_ids
    assert "frame_creatinine_legacy_s24_egfr_escalation" in frame_ids
    assert "frame_creatinine_legacy_s24_potassium_escalation" in frame_ids
    assert "frame_creatinine_pass3_promoted_candidate" in frame_ids


def test_kb52c_canonical_and_candidate_collision_classified(tmp_path: Path):
    doc = _load_index()
    frames = {f["medical_frame_id"]: f for f in doc["signal_families"][0]["frames"]}
    kb52c = frames["frame_creatinine_reduced_glomerular_filtration"]
    candidate = frames["frame_creatinine_pass3_promoted_candidate"]
    assert kb52c["promotion_state"] == "runtime_active_canonical"
    assert kb52c["runtime_authority_status"] == "active"
    assert candidate["promotion_state"] == "compiled_not_promoted"
    assert candidate["collision_status"] == "allowed_non_runtime_collision"
    assert kb52c["activation_key"] == candidate["activation_key"]


def test_duplicate_active_activation_key_fails(tmp_path: Path):
    doc = _load_index()
    broken = copy.deepcopy(doc)
    frames = broken["signal_families"][0]["frames"]
    frames[3]["runtime_authority_status"] = "active"
    path = tmp_path / "broken_index.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "duplicate active activation_key" in proc.stderr


def test_duplicate_non_runtime_activation_key_allowed(tmp_path: Path):
    proc = _run_validator(INDEX)
    assert proc.returncode == 0


def test_missing_required_field_fails(tmp_path: Path):
    doc = _load_index()
    broken = copy.deepcopy(doc)
    del broken["signal_families"][0]["frames"][0]["medical_frame_id"]
    path = tmp_path / "missing_field.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "medical_frame_id" in proc.stderr


def test_unknown_promotion_state_fails(tmp_path: Path):
    doc = _load_index()
    broken = copy.deepcopy(doc)
    broken["signal_families"][0]["frames"][0]["promotion_state"] = "not_a_real_state"
    path = tmp_path / "bad_promotion.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "unknown promotion_state" in proc.stderr


def test_unknown_collision_status_fails(tmp_path: Path):
    doc = _load_index()
    broken = copy.deepcopy(doc)
    broken["signal_families"][0]["frames"][0]["collision_status"] = "mystery_collision"
    path = tmp_path / "bad_collision.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "unknown collision_status" in proc.stderr


def test_runtime_consumed_must_be_false(tmp_path: Path):
    doc = _load_index()
    broken = copy.deepcopy(doc)
    broken["runtime_consumed"] = True
    path = tmp_path / "runtime_consumed.yaml"
    path.write_text(yaml.safe_dump(broken, sort_keys=False), encoding="utf-8")
    proc = _run_validator(path)
    assert proc.returncode != 0
    assert "runtime_consumed must be false" in proc.stderr


def test_referenced_package_paths_exist():
    doc = _load_index()
    for frame in doc["signal_families"][0]["frames"]:
        rel = frame["source_package_path"]
        assert (REPO / rel).is_dir(), f"missing package path: {rel}"


def test_legacy_s24_egfr_and_potassium_preserved_not_collapsed():
    doc = _load_index()
    frames = {f["medical_frame_id"]: f for f in doc["signal_families"][0]["frames"]}
    egfr = frames["frame_creatinine_legacy_s24_egfr_escalation"]
    potassium = frames["frame_creatinine_legacy_s24_potassium_escalation"]
    assert egfr["frame_role"] == "legacy_override_rule_egfr"
    assert potassium["frame_role"] == "legacy_override_rule_potassium"
    assert egfr["clinical_adjudication_status"] == "blocked_pending_medical_review"
    assert potassium["clinical_adjudication_status"] == "blocked_pending_medical_review"
