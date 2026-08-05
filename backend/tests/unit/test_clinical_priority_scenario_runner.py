"""
CLIN-PRIORITY-CORE-1 — Unit tests for clinical priority scenario runner (Checkpoint 2 estate).
"""

import json
from pathlib import Path

from tools.run_clinical_priority_scenarios import run_clinical_priority_scenarios
from core.analytics.concern_constructor import construct_clinical_concern_set
from core.analytics.prioritisation_registry import load_prioritisation_package


def _fixture_path() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "clinical_priority_scenarios_v1.json"


def test_estate_scenario_runner_coverage(tmp_path):
    run_dir, manifest = run_clinical_priority_scenarios(
        fixture_path=_fixture_path(),
        output_root=tmp_path,
        run_id="unit-clin-priority-estate",
    )
    assert (run_dir / "manifest.json").exists()
    assert manifest["scenario_count"] == 110
    coverage = manifest["APPROVED_SCENARIO_ESTATE_COVERAGE"]
    assert coverage["fixture_rows"] == 110
    assert coverage["unique_clinical_scenarios"] == 109
    assert coverage["target"] == 109
    assert manifest["failed"] == 0, json.dumps(
        [r for r in manifest["scenario_results"] if not r["passed"]], indent=2
    )
    assert coverage["passed_unique"] == 109
    assert coverage["zero_skips"] is True


def test_xd_as_32_no_forced_lead(tmp_path):
    _, manifest = run_clinical_priority_scenarios(
        fixture_path=_fixture_path(),
        output_root=tmp_path,
        run_id="unit-clin-priority-xd32",
    )
    xd = manifest["XD_AS_32"]
    assert xd["passed"] is True
    assert xd["no_forced_lead"] is True
    assert set(xd["finding_types"]) == {"RE-F10", "IRIN-F3", "THY-F1"}
    assert xd["presentation_mode"] == "no_forced_lead"


def test_contract_fix_1_identical_to_hep_as_1(tmp_path):
    _, manifest = run_clinical_priority_scenarios(
        fixture_path=_fixture_path(),
        output_root=tmp_path,
        run_id="unit-clin-priority-dup",
    )
    rows = {r["scenario_id"]: r for r in manifest["scenario_results"]}
    assert rows["CONTRACT-FIX-1"]["passed"] is True
    assert rows["HEP-AS-1"]["passed"] is True
    assert rows["CONTRACT-FIX-1"]["finding_types"] == rows["HEP-AS-1"]["finding_types"]


def test_hep_as_10_does_not_use_fib_4():
    raw = json.loads(_fixture_path().read_text(encoding="utf-8"))
    scenario = next(s for s in raw["scenarios"] if s["scenario_id"] == "HEP-AS-10")
    package = load_prioritisation_package()
    concern = construct_clinical_concern_set(
        signal_results=scenario["signal_results"],
        biomarkers=scenario["biomarkers"],
        lab_ranges=raw["default_lab_ranges"],
        derived=scenario.get("derived"),
        context=scenario.get("context"),
        package=package,
    )
    assert concern.fib_4_computed is False
    assert concern.fib_4_displayed is False
    assert any(f.finding_type == "HEP-F5" for f in concern.findings)
    f5 = next(f for f in concern.findings if f.finding_type == "HEP-F5")
    assert "XD-QUAR-1" in f5.quarantine_flags
    assert f5.constituent_activation_keys
    assert "fib_4" not in " ".join(f5.constituent_activation_keys)


def test_bilirubin_isolated_not_tier0_escalation():
    raw = json.loads(_fixture_path().read_text(encoding="utf-8"))
    scenario = next(s for s in raw["scenarios"] if s["scenario_id"] == "HEP-AS-6")
    package = load_prioritisation_package()
    concern = construct_clinical_concern_set(
        signal_results=scenario["signal_results"],
        biomarkers=scenario["biomarkers"],
        lab_ranges=raw["default_lab_ranges"],
        package=package,
    )
    assert all(f.concern_tier != 0 for f in concern.findings)
    assert any(f.finding_type == "HEP-F6" and f.concern_tier == 2 for f in concern.findings)


def test_provenance_retained_after_consolidation():
    raw = json.loads(_fixture_path().read_text(encoding="utf-8"))
    scenario = next(s for s in raw["scenarios"] if s["scenario_id"] == "HEP-AS-1")
    package = load_prioritisation_package()
    concern = construct_clinical_concern_set(
        signal_results=scenario["signal_results"],
        biomarkers=scenario["biomarkers"],
        lab_ranges=raw["default_lab_ranges"],
        package=package,
    )
    assert len(concern.findings) == 1
    f = concern.findings[0]
    assert f.finding_type == "HEP-F1"
    assert scenario["signal_results"][0]["activation_key"] in f.constituent_activation_keys


def test_prioritisation_loader_single_source():
    package = load_prioritisation_package()
    assert package.stamp.contract_version == "0.6.3"
    assert package.stamp.ruleset_version == "0.5"
    assert "HEP-F1" in package.finding_types
    assert "IRIN-F3" in package.finding_types
    assert any(q.get("namespace") == "fib_4" for q in package.quarantine_namespaces)
    unset_ids = {x.get("id") for x in package.excluded_unset_thresholds}
    assert "HEP-U2" in unset_ids
