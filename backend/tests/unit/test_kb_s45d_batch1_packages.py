"""
KB-S45d: ten individual batch-1 investigation packages (hardened schema 2.0.0).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_VALIDATE_SCRIPT = _REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
_SOURCE_SPEC = (
    _REPO_ROOT
    / "knowledge_bus"
    / "research"
    / "investigation_specs"
    / "investigation-spec-collection-batch1-10.json"
)

KB_S45D_PACKAGE_DIRS: tuple[str, ...] = (
    "pkg_kb45_active_b12_low_deficiency",
    "pkg_kb45_apoa1_low_cardio_risk",
    "pkg_kb45_apob_high_atherogenic",
    "pkg_kb45_apob_apoa1_ratio_high_imbalance",
    "pkg_kb45_basophil_pct_high_basophilia",
    "pkg_kb45_basophils_abs_high_basophilia",
    "pkg_kb45_bilirubin_high_hyperbilirubinemia",
    "pkg_kb45_chloride_high_hyperchloremia",
    "pkg_kb45_corrected_calcium_high_hypercalcemia",
    "pkg_kb45_cortisol_high_hypercortisolism",
)

# For evaluator tests: one package directory per signal_id.
SIGNAL_ID_TO_PACKAGE_DIR: dict[str, str] = {
    "signal_active_b12_deficiency": "pkg_kb45_active_b12_low_deficiency",
    "signal_apoa1_cardio_risk": "pkg_kb45_apoa1_low_cardio_risk",
    "signal_apob_atherogenic": "pkg_kb45_apob_high_atherogenic",
    "signal_lipid_imbalance": "pkg_kb45_apob_apoa1_ratio_high_imbalance",
    "signal_basophilia_pct": "pkg_kb45_basophil_pct_high_basophilia",
    "signal_basophilia_abs": "pkg_kb45_basophils_abs_high_basophilia",
    "signal_hyperbilirubinemia": "pkg_kb45_bilirubin_high_hyperbilirubinemia",
    "signal_hyperchloremia": "pkg_kb45_chloride_high_hyperchloremia",
    "signal_hypercalcemia": "pkg_kb45_corrected_calcium_high_hypercalcemia",
    "signal_hypercortisolism": "pkg_kb45_cortisol_high_hypercortisolism",
}

EXPECTED_SIGNAL_IDS = frozenset(
    {
        "signal_active_b12_deficiency",
        "signal_apoa1_cardio_risk",
        "signal_apob_atherogenic",
        "signal_lipid_imbalance",
        "signal_basophilia_pct",
        "signal_basophilia_abs",
        "signal_hyperbilirubinemia",
        "signal_hyperchloremia",
        "signal_hypercalcemia",
        "signal_hypercortisolism",
    }
)

_TRIGGER_DIRECTIONS = frozenset({"high", "low", "bidirectional", "context_dependent"})


def _pkg_path(dirname: str) -> Path:
    return _REPO_ROOT / "knowledge_bus" / "packages" / dirname


def test_kb_s45d_source_json_matches_expected_signal_ids():
    raw = json.loads(_SOURCE_SPEC.read_text(encoding="utf-8"))
    assert isinstance(raw, list) and len(raw) == 10
    ids = {entry["signal_id"] for entry in raw if isinstance(entry, dict)}
    assert ids == EXPECTED_SIGNAL_IDS


def test_kb_s45d_all_packages_validate_under_orchestrator():
    for dirname in KB_S45D_PACKAGE_DIRS:
        proc = subprocess.run(
            [
                sys.executable,
                str(_VALIDATE_SCRIPT),
                "--package-dir",
                str(_pkg_path(dirname)),
            ],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, f"{dirname}: {proc.stdout}\n{proc.stderr}"
        assert "signal_validation: PASS" in proc.stdout


def test_kb_s45d_each_package_has_exactly_one_expected_signal():
    found: set[str] = set()
    for dirname in KB_S45D_PACKAGE_DIRS:
        lib_path = _pkg_path(dirname) / "signal_library.yaml"
        payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        sigs = payload.get("signals", [])
        assert len(sigs) == 1, dirname
        sid = sigs[0].get("signal_id")
        assert isinstance(sid, str)
        found.add(sid)
    assert found == EXPECTED_SIGNAL_IDS


def test_kb_s45d_signal_libraries_use_schema_v2_and_trigger_direction():
    for dirname in KB_S45D_PACKAGE_DIRS:
        lib_path = _pkg_path(dirname) / "signal_library.yaml"
        payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        lib = payload.get("library") or {}
        assert lib.get("schema_version") == "2.0.0", dirname
        sig = (payload.get("signals") or [{}])[0]
        td = sig.get("trigger_direction")
        assert td in _TRIGGER_DIRECTIONS, f"{dirname}: {td}"


def test_kb_s45d_supporting_metrics_are_structured_objects():
    for dirname in KB_S45D_PACKAGE_DIRS:
        lib_path = _pkg_path(dirname) / "signal_library.yaml"
        payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        sig = (payload.get("signals") or [{}])[0]
        sm = sig.get("supporting_metrics")
        assert isinstance(sm, list) and sm, dirname
        for row in sm:
            assert isinstance(row, dict), dirname
            for k in ("biomarker_id", "expected_direction", "role", "availability", "rationale"):
                assert k in row, f"{dirname} missing {k}"


def test_kb_s45d_output_supporting_markers_are_flat_strings_matching_order():
    for dirname in KB_S45D_PACKAGE_DIRS:
        lib_path = _pkg_path(dirname) / "signal_library.yaml"
        payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        sig = (payload.get("signals") or [{}])[0]
        sm = sig.get("supporting_metrics") or []
        om = ((sig.get("output") or {}).get("supporting_markers")) or []
        expected = [r["biomarker_id"] for r in sm if isinstance(r, dict)]
        assert om == expected, dirname
        for x in om:
            assert isinstance(x, str), dirname


def test_kb_s45d_override_rules_include_nonempty_source_refs():
    for dirname in KB_S45D_PACKAGE_DIRS:
        lib_path = _pkg_path(dirname) / "signal_library.yaml"
        payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        sig = (payload.get("signals") or [{}])[0]
        for rule in sig.get("override_rules") or []:
            refs = rule.get("source_refs")
            assert isinstance(refs, list) and len(refs) >= 1, dirname
            assert all(isinstance(r, str) and r.strip() for r in refs), dirname


def test_kb_s45d_lipid_imbalance_keeps_apob_apoa1_ratio_on_derived_metrics():
    lib_path = _pkg_path("pkg_kb45_apob_apoa1_ratio_high_imbalance") / "signal_library.yaml"
    payload = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
    sig = (payload.get("signals") or [{}])[0]
    assert sig.get("signal_id") == "signal_lipid_imbalance"
    deps = sig.get("dependencies") or {}
    assert "apob_apoa1_ratio" in (deps.get("derived_metrics") or [])
    assert "apob_apoa1_ratio" not in (deps.get("biomarkers") or [])


def test_kb_s45d_research_briefs_reference_external_sources_with_source_ids():
    for dirname in KB_S45D_PACKAGE_DIRS:
        brief_path = _pkg_path(dirname) / "research_brief.yaml"
        brief = yaml.safe_load(brief_path.read_text(encoding="utf-8")) or {}
        sources = brief.get("sources") or []
        assert sources, dirname
        for src in sources:
            assert isinstance(src.get("source_id"), str) and src["source_id"].startswith("source_"), dirname
            j = str(src.get("journal", "")).strip().lower()
            assert j != "healthiq knowledge bus"
