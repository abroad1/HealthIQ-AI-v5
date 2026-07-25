"""ARCH-CONV-PKG2 — launch-critical provenance reachability tests."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.package_runtime_eligibility_v1 import (
    ELIGIBILITY_NON_REACHABLE,
    ELIGIBILITY_PRODUCTION_REACHABLE,
    ELIGIBILITY_TEST_ONLY_OPT_IN,
    ELIGIBILITY_UNKNOWN_FAIL_CLOSED,
    classify_package_runtime_eligibility,
)
from core.knowledge.provenance_status_v1 import (
    classify_package_provenance_status,
    is_beta_eligible_explicit_lineage,
)

REPO = Path(__file__).resolve().parents[3]

WAVE1 = [
    "pkg_kb47_free_t3_low_low_t3_syndrome",
    "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
    "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
    "pkg_kb47_free_t4_high_thyrotoxicosis_context",
    "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
    "pkg_kb47_egfr_low_hemodynamic_filtration_drop",
]


def test_wave1_packages_have_explicit_lineage_and_inv_yaml():
    for pkg in WAVE1:
        man = yaml.safe_load(
            (REPO / "knowledge_bus/packages" / pkg / "package_manifest.yaml").read_text(encoding="utf-8")
        )
        spec = man["source_spec_id"]
        assert (REPO / "knowledge_bus/research/investigation_specs" / f"{spec}.yaml").is_file()
        status = classify_package_provenance_status(manifest=man)
        assert status == "EXPLICIT_SPEC"
        assert is_beta_eligible_explicit_lineage(status)
        elig, _ = classify_package_runtime_eligibility(package_id=pkg, manifest=man)
        assert elig == ELIGIBILITY_PRODUCTION_REACHABLE


def test_production_registry_loads_only_wave1_kb47():
    reg = SignalRegistry()
    loaded = sorted(
        {
            str(r.get("package_id"))
            for r in reg.get_all_signals()
            if str(r.get("package_id", "")).startswith("pkg_kb47_")
        }
    )
    assert loaded == sorted(WAVE1)
    assert len(reg.excluded_launch_critical_packages) == 14
    for row in reg.get_all_signals():
        if str(row.get("package_id", "")).startswith("pkg_kb47_"):
            assert row.get("provenance_status") == "EXPLICIT_SPEC"
            assert row["activation_key"] == f"{row['signal_id']}::{row['source_spec_id']}"


def test_blocked_androgen_not_in_production_registry_and_cannot_fire_via_registry():
    reg = SignalRegistry()
    ids = {r["signal_id"] for r in reg.get_all_signals()}
    assert "signal_dhea_high" not in ids
    assert "signal_creatine_kinase_high" not in ids
    assert "signal_eosinophil_pct_high" not in ids
    results = SignalEvaluator(reg).evaluate_all(
        signal_biomarkers={"dhea": 20.0, "creatine_kinase": 500.0},
        signal_derived={},
        lab_ranges={
            "dhea": {"min": 1.0, "max": 10.0},
            "creatine_kinase": {"min": 10.0, "max": 170.0},
        },
    )
    fired = {r.signal_id for r in results}
    assert "signal_dhea_high" not in fired
    assert "signal_creatine_kinase_high" not in fired


def test_test_opt_in_loads_blocked_fixtures():
    reg = SignalRegistry(allow_launch_critical_blocked=True)
    kb47 = [r for r in reg.get_all_signals() if str(r.get("package_id", "")).startswith("pkg_kb47_")]
    assert len(kb47) == 20
    elig, _ = classify_package_runtime_eligibility(
        package_id="pkg_kb47_dhea_high_androgen_excess_context",
        manifest={
            "source_document": "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json"
        },
        allow_launch_critical_blocked=True,
    )
    assert elig == ELIGIBILITY_TEST_ONLY_OPT_IN


def test_unknown_package_id_fails_closed():
    elig, status = classify_package_runtime_eligibility(package_id="")
    assert elig == ELIGIBILITY_UNKNOWN_FAIL_CLOSED
    assert status == "UNRESOLVED"


def test_non_kb47_packages_unaffected():
    reg = SignalRegistry()
    alt = [r for r in reg.get_all_signals() if r["signal_id"] == "signal_alt_high"]
    assert len(alt) == 4


def test_activation_keys_survive_lineage_attach():
    reg = SignalRegistry()
    egfr = [r for r in reg.get_all_signals() if r["signal_id"] == "signal_egfr_low"]
    assert len(egfr) == 2
    keys = {r["activation_key"] for r in egfr}
    assert keys == {
        "signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction",
        "signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop",
    }


def test_exclusions_are_auditable_and_deterministic():
    a = SignalRegistry()
    b = SignalRegistry()
    assert a.excluded_launch_critical_packages == b.excluded_launch_critical_packages
    assert all(row["eligibility"] == ELIGIBILITY_NON_REACHABLE for row in a.excluded_launch_critical_packages)
    assert [row["package_id"] for row in a.excluded_launch_critical_packages] == sorted(
        row["package_id"] for row in a.excluded_launch_critical_packages
    )


def test_deliberately_invalid_explicit_claim_without_inv_yaml_not_reachable():
    # source_spec_id present but no inv file → not EXPLICIT_SPEC → non_reachable for kb47
    man = {"source_spec_id": "inv_not_a_real_spec_zzzz_pkg2"}
    status = classify_package_provenance_status(manifest=man)
    assert status != "EXPLICIT_SPEC"
    elig, _ = classify_package_runtime_eligibility(
        package_id="pkg_kb47_dhea_high_androgen_excess_context",
        manifest=man,
    )
    assert elig == ELIGIBILITY_NON_REACHABLE


def test_reachable_wave1_result_carries_explicit_provenance_fields():
    reg = SignalRegistry()
    rows = [
        r
        for r in reg.get_all_signals()
        if r.get("package_id") == "pkg_kb47_egfr_low_chronic_kidney_function_reduction"
    ]
    assert len(rows) == 1
    row = rows[0]
    assert row["provenance_status"] == "EXPLICIT_SPEC"
    assert row["runtime_eligibility"] == ELIGIBILITY_PRODUCTION_REACHABLE
    assert row["source_spec_id"] == "inv_egfr_low_chronic_kidney_function_reduction"
    results = SignalEvaluator(reg).evaluate_all(
        signal_biomarkers={"egfr": 45.0},
        signal_derived={},
        lab_ranges={"egfr": {"min": 90.0, "max": 120.0}},
    )
    egfr = [r for r in results if r.signal_id == "signal_egfr_low"]
    assert egfr
    assert all(r.provenance_status == "EXPLICIT_SPEC" for r in egfr)
    assert all(r.source_spec_id.startswith("inv_egfr_low_") for r in egfr)
    assert all(r.activation_key == f"{r.signal_id}::{r.source_spec_id}" for r in egfr)


def test_opt_in_can_fire_excluded_ck_but_production_cannot():
    lab = {"creatine_kinase": {"min": 10.0, "max": 170.0}}
    bio = {"creatine_kinase": 500.0}
    prod = SignalEvaluator(SignalRegistry()).evaluate_all(
        signal_biomarkers=bio, signal_derived={}, lab_ranges=lab
    )
    opt = SignalEvaluator(SignalRegistry(allow_launch_critical_blocked=True)).evaluate_all(
        signal_biomarkers=bio, signal_derived={}, lab_ranges=lab
    )
    assert "signal_creatine_kinase_high" not in {r.signal_id for r in prod}
    assert "signal_creatine_kinase_high" in {r.signal_id for r in opt}
