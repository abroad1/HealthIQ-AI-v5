"""FE-VISUALISATION-B1B — assembly behaviour with populated registry and failure safety."""

from core.analytics.retail_explainer_assembly_v1 import attach_retail_explainers_v1
from core.models.results import BiomarkerScore, ClusterHit
from core.ssot.retail_explainer_registry_v1 import cached_retail_explainer_registry_v1


def test_attach_graceful_when_registry_load_fails(monkeypatch):
    def boom():
        raise ValueError("simulated malformed registry")

    monkeypatch.setattr(
        "core.analytics.retail_explainer_assembly_v1.load_retail_explainer_registry_v1",
        boom,
    )
    cached_retail_explainer_registry_v1.cache_clear()
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
    ]
    clusters = [
        ClusterHit(
            cluster_id="metabolic_2_biomarkers",
            name="Metabolic Health Pattern",
            biomarkers=["glucose"],
            confidence=0.85,
            severity="normal",
            description="Synthetic",
        ),
    ]
    b_out, c_out = attach_retail_explainers_v1(biomarkers, clusters)
    assert b_out[0].biomarker_educational_explainer is None
    assert b_out[0].contribution_context is None
    assert c_out[0].system_educational_explainer is None
