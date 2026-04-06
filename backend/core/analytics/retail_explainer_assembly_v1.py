"""
Attach governed retail explainer payloads to biomarker and cluster DTOs (B1A).
"""

from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple

from core.contracts.retail_explainer_v1 import ContributionContextV1
from core.models.results import BiomarkerScore, ClusterHit
from core.ssot.retail_explainer_registry_v1 import (
    biomarker_educational_explainer,
    cluster_schema_key_from_cluster_id,
    load_retail_explainer_registry_v1,
    system_educational_explainer,
)


def _membership_index(clusters: List[ClusterHit]) -> dict[str, list[tuple[str, str]]]:
    idx: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for c in clusters:
        for bm in c.biomarkers:
            idx[bm].append((c.cluster_id, c.name))
    return idx


def _membership_statement(biomarker_name: str, refs: list[tuple[str, str]]) -> ContributionContextV1:
    labels: list[str] = []
    seen: set[str] = set()
    for _, name in refs[:5]:
        if name not in seen:
            seen.add(name)
            labels.append(f'"{name}"')
    extra = len(refs) - len(labels)
    suffix = f" (and {extra} other pattern grouping(s))" if extra > 0 else ""
    factual = (
        f"For this analysis, the marker {biomarker_name} appears in the following "
        f"pattern grouping(s): {', '.join(labels)}{suffix}. "
        "This describes how markers were grouped for review only."
    )
    if len(factual) > 500:
        factual = factual[:497] + "..."
    return ContributionContextV1(factual_statement=factual)


def attach_retail_explainers_v1(
    biomarkers: List[BiomarkerScore],
    clusters: List[ClusterHit],
    *,
    registry=None,
) -> Tuple[List[BiomarkerScore], List[ClusterHit]]:
    """
    Return new lists with optional educational / contribution fields populated.
    Deterministic; no symptom or personalised interpretation logic.
    """
    reg = registry if registry is not None else load_retail_explainer_registry_v1()
    membership = _membership_index(clusters)

    enriched_clusters: List[ClusterHit] = []
    for c in clusters:
        skey = cluster_schema_key_from_cluster_id(c.cluster_id)
        sys_expl = system_educational_explainer(skey, reg)
        enriched_clusters.append(
            c.model_copy(update={"system_educational_explainer": sys_expl}),
        )

    enriched_biomarkers: List[BiomarkerScore] = []
    for b in biomarkers:
        bed = biomarker_educational_explainer(b.biomarker_name, reg)
        contrib: ContributionContextV1 | None = None
        if b.biomarker_name in membership:
            contrib = _membership_statement(b.biomarker_name, membership[b.biomarker_name])
        enriched_biomarkers.append(
            b.model_copy(
                update={
                    "biomarker_educational_explainer": bed,
                    "contribution_context": contrib,
                },
            ),
        )

    return enriched_biomarkers, enriched_clusters
