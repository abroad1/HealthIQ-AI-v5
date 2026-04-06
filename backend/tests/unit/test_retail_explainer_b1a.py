"""FE-VISUALISATION-B1A — retail explainer registry and assembly."""

import pytest

from core.models.results import BiomarkerScore, ClusterHit
from core.analytics.retail_explainer_assembly_v1 import attach_retail_explainers_v1
from core.ssot.retail_explainer_registry_v1 import (
    cluster_schema_key_from_cluster_id,
    load_retail_explainer_registry_v1,
    cached_retail_explainer_registry_v1,
)


def test_cluster_schema_key_from_cluster_id():
    assert cluster_schema_key_from_cluster_id("metabolic_3_biomarkers") == "metabolic"
    assert cluster_schema_key_from_cluster_id("renal_2_biomarkers") == "renal"


def test_load_registry_contains_pilot_biomarker_and_system():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    assert "glucose" in reg.biomarkers
    assert "metabolic" in reg.systems
    assert "title" in reg.biomarkers["glucose"]


def test_attach_enrichment_glucose_and_metabolic_cluster():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    biomarkers = [
        BiomarkerScore(
            biomarker_name="glucose",
            value=5.0,
            unit="mmol/L",
            score=0.8,
            percentile=None,
            status="normal",
            reference_range={"min": 3.0, "max": 6.0, "unit": "mmol/L"},
            interpretation="Scored using lab reference range",
        ),
        BiomarkerScore(
            biomarker_name="creatinine",
            value=80.0,
            unit="µmol/L",
            score=0.7,
            percentile=None,
            status="normal",
            reference_range={"min": 60.0, "max": 110.0, "unit": "µmol/L"},
            interpretation="Scored using lab reference range",
        ),
    ]
    clusters = [
        ClusterHit(
            cluster_id="metabolic_2_biomarkers",
            name="Metabolic Health Pattern",
            biomarkers=["glucose", "hba1c"],
            confidence=0.85,
            severity="normal",
            description="Synthetic",
        ),
    ]
    b_out, c_out = attach_retail_explainers_v1(biomarkers, clusters, registry=reg)
    g = next(x for x in b_out if x.biomarker_name == "glucose")
    assert g.biomarker_educational_explainer is not None
    assert g.biomarker_educational_explainer.content_class == "biomarker_education"
    assert g.contribution_context is not None
    assert g.contribution_context.relationship_kind == "cluster_membership"
    cr = next(x for x in b_out if x.biomarker_name == "creatinine")
    assert cr.biomarker_educational_explainer is None
    assert cr.contribution_context is None
    assert c_out[0].system_educational_explainer is not None
    assert c_out[0].system_educational_explainer.content_class == "system_education"


def test_validate_entry_rejects_bad_payload():
    from core.ssot import retail_explainer_registry_v1 as mod

    with pytest.raises(ValueError):
        mod._validate_entry("x", "not-a-dict", kind="biomarkers")
