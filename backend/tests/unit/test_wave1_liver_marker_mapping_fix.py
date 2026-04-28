"""Trace-driven liver marker aliases (GGT, bilirubin) + Wave 1 missing-marker coherence."""

from __future__ import annotations

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service
from core.canonical.normalize import BiomarkerNormalizer
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1


@pytest.fixture(autouse=True)
def _clear_alias_registry_cache():
    get_alias_registry_service.cache_clear()
    yield
    get_alias_registry_service.cache_clear()


@pytest.fixture(autouse=True)
def _disable_common_alias_injection(monkeypatch):
    """Stable SSOT-driven aliases for these tests."""
    monkeypatch.setattr(
        AliasRegistryService,
        "_add_common_aliases",
        lambda self, alias_mapping, insert_alias: None,
    )


def test_observed_trace_key_gamma_glutamiltransferase_ggt_venous_maps_to_ggt():
    """Live trace key must resolve to canonical ``ggt`` (no unmapped_* quarantine)."""
    normalizer = BiomarkerNormalizer()
    raw_key = "gamma-glutamiltransferase_ggt_(venous)"
    panel, unmapped_keys = normalizer.normalize_biomarkers(
        {raw_key: {"value": 45.0, "unit": "U/L"}}
    )
    assert "ggt" in panel.biomarkers
    assert raw_key not in unmapped_keys


def test_observed_trace_key_bilirubin_total_venous_maps_to_canonical_bilirubin():
    """Parser export ``bilirubin_total_(venous)`` → canonical ``bilirubin``."""
    normalizer = BiomarkerNormalizer()
    panel, unmapped_keys = normalizer.normalize_biomarkers(
        {"bilirubin_total_(venous)": {"value": 14.0, "unit": "umol/L"}}
    )
    assert "bilirubin" in panel.biomarkers
    assert not any("bilirubin_total_(venous)" == k for k in unmapped_keys)


def _minimal_graph() -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="t_liver_missing",
        signal_results=[],
        system_capacity_scores={"hepatic": 70},
        confidence=ConfidenceModelV1(cluster_confidence={}),
    )


def test_wave1_liver_missing_does_not_flag_bilirubin_when_canonical_bilirubin_present():
    """Panel carries ``bilirubin`` only — must not list ``total_bilirubin`` / bilirubin as missing."""
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
        }
    }
    panel = {
        "alt",
        "bilirubin",
        "glucose",
        "hba1c",
        "ldl_cholesterol",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    liver = rows[2]
    assert liver.domain_id == "wave1_liver"
    assert "bilirubin" not in liver.missing_marker_ids
    assert "total_bilirubin" not in liver.missing_marker_ids


def test_wave1_liver_missing_still_lists_bilirubin_when_neither_form_present():
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result={
            "health_system_scores": {
                "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
                "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
                "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            }
        },
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"alt", "glucose", "hba1c", "ldl_cholesterol"},
    )
    liver = rows[2]
    assert "bilirubin" in liver.missing_marker_ids
