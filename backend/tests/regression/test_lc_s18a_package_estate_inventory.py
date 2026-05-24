"""LC-S18A — Knowledge Bus package estate inventory refresh guards."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]

if str(_REPO_ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "backend"))

from core.knowledge.kb_lifecycle_contract_v1 import (  # noqa: E402
    ESTATE_INVENTORY_PATH,
    GOVERNED_TIER_POST_KB_S49_UNREVIEWED,
    WHY_ENABLED_PACKAGE_FILES,
    assess_package_estate,
    build_inventory_row,
    detect_orphan_packages,
    is_lipid_kb_wave1_relevant,
    load_estate_inventory_package_ids,
    package_has_required_files,
)

_INVENTORY_PATH = _REPO_ROOT / ESTATE_INVENTORY_PATH
_SENTINEL_PATH = _REPO_ROOT / "sentinel" / "packs" / "escaped_defects_v1.json"
_TEST_FILE = "backend/tests/regression/test_lc_s18a_package_estate_inventory.py"


def _load_inventory() -> dict:
    payload = yaml.safe_load(_INVENTORY_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


@pytest.mark.regression
def test_lc_s18a_inventory_parses() -> None:
    payload = _load_inventory()
    assert payload.get("inventory_refresh", {}).get("work_id") == "LC-S18A"
    packages = payload.get("packages")
    assert isinstance(packages, list)
    assert len(packages) >= 185


@pytest.mark.regression
def test_lc_s18a_no_unregistered_disk_orphans_after_refresh() -> None:
    report = detect_orphan_packages(_REPO_ROOT)
    assert report.disk_not_in_inventory == ()
    assert report.inventory_not_on_disk == ()


@pytest.mark.regression
def test_lc_s18a_review_queue_not_runtime_approved() -> None:
    payload = _load_inventory()
    review_rows = [
        row
        for row in payload.get("packages", [])
        if isinstance(row, dict) and row.get("requires_review") is True
    ]
    assert len(review_rows) == 112
    for row in review_rows:
        assert row.get("runtime_loaded") is False
        assert row.get("validator_ready_for_implementation") is False
        assert row.get("validate_knowledge_package_exit_code") is None
        assert row.get("governed_tier") == GOVERNED_TIER_POST_KB_S49_UNREVIEWED


@pytest.mark.regression
def test_lc_s18a_inventory_entries_point_to_existing_directories() -> None:
    packages_root = _REPO_ROOT / "knowledge_bus" / "packages"
    for package_id in load_estate_inventory_package_ids(_REPO_ROOT):
        if package_id == "pkg_example":
            continue
        assert (packages_root / package_id).is_dir(), package_id


@pytest.mark.regression
def test_lc_s18a_why_enabled_packages_have_required_files_or_flagged() -> None:
    payload = _load_inventory()
    for row in payload.get("packages", []):
        if not isinstance(row, dict):
            continue
        if row.get("package_type") != "WHY-enabled":
            continue
        package_id = str(row.get("package_id") or "")
        pkg_dir = _REPO_ROOT / "knowledge_bus" / "packages" / package_id
        missing = package_has_required_files(pkg_dir, WHY_ENABLED_PACKAGE_FILES)
        assert not missing or row.get("requires_review") is True, package_id


@pytest.mark.regression
def test_lc_s18a_lipid_kb_wave1_packages_identifiable() -> None:
    payload = _load_inventory()
    lipid_rows = [
        row
        for row in payload.get("packages", [])
        if isinstance(row, dict) and row.get("kb_wave_1_lipid_relevant") is True
    ]
    assert len(lipid_rows) >= 17
    for row in lipid_rows:
        package_id = str(row.get("package_id") or "")
        assert is_lipid_kb_wave1_relevant(package_id)


@pytest.mark.regression
def test_lc_s18a_orphan_reporter_output_stable() -> None:
    cmd = [sys.executable, "backend/scripts/validate_kb_package_estate_orphans_v1.py"]
    proc = subprocess.run(cmd, cwd=_REPO_ROOT, capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout)
    assert payload["has_orphans"] is False
    assert payload["review_queue_count"] == 112
    assert payload["inventory_package_count"] == 185


@pytest.mark.regression
def test_lc_s18a_estate_assessment_deterministic() -> None:
    first = assess_package_estate(_REPO_ROOT)
    second = assess_package_estate(_REPO_ROOT)
    assert first == second
    assert first.review_queue_count == 112
    assert first.draft_incomplete_count == 0


@pytest.mark.regression
def test_lc_s18a_build_inventory_row_marks_review_for_new_batch() -> None:
    sample_id = "pkg_kb52c_apob_high_atherogenic_particle_excess"
    row = build_inventory_row(_REPO_ROOT, sample_id, requires_review=True)
    assert row["requires_review"] is True
    assert row["runtime_loaded"] is False
    assert row["kb_wave_1_lipid_relevant"] is True


@pytest.mark.regression
@pytest.mark.parametrize(
    "defect_class",
    [
        "kb_package_estate_inventory_stale",
        "kb_orphan_package_unreviewed",
        "kb_inventory_entry_missing_on_disk",
        "kb_draft_package_marked_runtime_valid",
        "kb_why_enabled_package_missing_required_files",
    ],
)
def test_lc_s18a_sentinel_defect_classes_registered(defect_class: str) -> None:
    pack = json.loads(_SENTINEL_PATH.read_text(encoding="utf-8"))
    entry = (pack.get("defect_classes") or {}).get(defect_class)
    assert entry is not None, defect_class
    assert entry.get("test_file") == _TEST_FILE
    assert entry.get("guard_type") == "active_deterministic"
    assert entry.get("status") == "GUARDED"
