"""
Sprint 11 - Unit tests for BiomarkerContext_v1 builder.
"""

from core.analytics.biomarker_context_builder import build_biomarker_context_v1
from core.contracts.insight_graph_v1 import InsightGraphV1, BiomarkerNode
from core.contracts.relationship_registry_v1 import RelationshipDetection


def _sample_graph() -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="ctx-1",
        biomarker_nodes=[
            BiomarkerNode(biomarker_id="glucose", status="normal", score=72.0),
            BiomarkerNode(biomarker_id="hba1c", status="high", score=20.0),
            BiomarkerNode(biomarker_id="insulin", status="low", score=55.0),
            BiomarkerNode(biomarker_id="apob", status="unknown", score=None),
        ],
        confidence={
            "missing_required_biomarkers": ["apob"],
            "missing_required_clusters": ["metabolic"],
        },
        cluster_summary={
            "clusters": [
                {"cluster_id": "metabolic", "biomarkers": ["glucose", "hba1c", "apob"]},
            ]
        },
        relationships=[
            RelationshipDetection(
                relationship_id="apob_ldl_discordance",
                version="1.0.0",
                biomarkers=["apob", "ldl_cholesterol"],
                classification_code="LIPOPROTEIN_DISCORDANCE",
                severity="moderate",
                triggered=True,
                evidence=["apob_high", "ldl_normal"],
            )
        ],
        edges=[],
    )


def test_determinism_same_input_same_output_and_hash():
    """Deterministic output/hash for identical InsightGraph input."""
    g = _sample_graph()
    c1, s1 = build_biomarker_context_v1(g)
    c2, s2 = build_biomarker_context_v1(g)
    assert [n.model_dump() for n in c1] == [n.model_dump() for n in c2]
    assert s1.biomarker_context_hash == s2.biomarker_context_hash
    assert s1.biomarker_context_version == s2.biomarker_context_version


def test_ordering_is_stable_by_biomarker_id():
    """Nodes are deterministically sorted by biomarker_id."""
    context, _ = build_biomarker_context_v1(_sample_graph())
    ids = [n.biomarker_id for n in context]
    assert ids == sorted(ids)


def test_reason_codes_cover_status_and_score_bands():
    """Reason codes include status and score-band/missing codes."""
    context, _ = build_biomarker_context_v1(_sample_graph())
    by_id = {n.biomarker_id: n for n in context}

    assert "status_normal" in by_id["glucose"].reason_codes
    assert "score_high_band" in by_id["glucose"].reason_codes

    assert "status_high" in by_id["hba1c"].reason_codes
    assert "score_low_band" in by_id["hba1c"].reason_codes

    assert "status_low" in by_id["insulin"].reason_codes
    assert "score_mid_band" in by_id["insulin"].reason_codes

    assert "status_unknown" in by_id["apob"].reason_codes
    assert "score_missing" in by_id["apob"].reason_codes


def test_relationship_codes_include_relationship_and_evidence():
    """Relationship codes include relationship_id + evidence for involved biomarkers."""
    context, _ = build_biomarker_context_v1(_sample_graph())
    by_id = {n.biomarker_id: n for n in context}
    apob_codes = by_id["apob"].relationship_codes
    assert "relationship:apob_ldl_discordance" in apob_codes
    assert "evidence:apob_high" in apob_codes
    assert "evidence:ldl_normal" in apob_codes


def test_missing_codes_come_from_confidence_and_incomplete_clusters():
    """Missing codes are code-only and derived from confidence/cluster summary."""
    context, _ = build_biomarker_context_v1(_sample_graph())
    by_id = {n.biomarker_id: n for n in context}
    missing = by_id["apob"].missing_codes
    assert "missing_required_for_cluster" in missing
    assert "in_incomplete_cluster:metabolic" in missing
