"""
Silent inflammation insight module.

Clinical implementation of silent inflammation assessment based on inflammatory markers,
immune cell ratios, and iron metabolism indicators.
"""

from typing import List

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.insights.base import BaseInsight
from core.insights.registry import register_insight
from core.insights.metadata import InsightMetadata, InsightResult
from core.models.context import AnalysisContext


@register_insight("inflammation", "v1.0.0")
class InflammationInsight(BaseInsight):
    """
    Silent inflammation assessment based on inflammatory markers and immune cell ratios.
    
    Clinical Rationale:
    - hs-CRP is the gold standard for systemic inflammation assessment
    - NLR (neutrophil/lymphocyte ratio) indicates immune system stress
    - Ferritin can be elevated in inflammatory conditions (acute phase reactant)
    - Combined markers provide comprehensive inflammation burden assessment
    
    Thresholds:
    - hs-CRP > 3.0 mg/L: High risk
    - hs-CRP > 1.0 mg/L: Moderate risk
    - NLR > 3.0: High immune stress
    - NLR > 2.0: Moderate immune stress
    - Ferritin > 300 ng/mL (men) or > 200 ng/mL (women): Elevated (inflammatory)
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="inflammation",
            version="v1.0.0",
            category="inflammatory",
            required_biomarkers=["crp"],
            optional_biomarkers=["white_blood_cells", "neutrophils", "lymphocytes", "ferritin"],
            description="Silent inflammation assessment using hs-CRP, NLR, and ferritin markers",
            author="HealthIQ Team",
            created_at="2024-01-30T00:00:00Z",
            updated_at="2024-01-30T00:00:00Z"
        )
    
    def _extract_insight_graph(self, context: AnalysisContext) -> InsightGraphV1 | None:
        raw_graph = (context.analysis_parameters or {}).get("insight_graph")
        if isinstance(raw_graph, InsightGraphV1):
            return raw_graph
        if isinstance(raw_graph, dict):
            return InsightGraphV1.model_validate(raw_graph)
        return None

    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        try:
            insight_graph = self._extract_insight_graph(context)
            if insight_graph is None or insight_graph.layer_c_features is None:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_INSIGHT_GRAPH",
                    error_detail="InsightGraph layer_c_features missing from analysis context",
                )]
            feature = insight_graph.layer_c_features.inflammation
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                drivers={"risk_factors": list(feature.risk_factors), "nlr": feature.nlr},
                evidence={
                    "inflammation_burden_score": feature.inflammation_burden_score,
                    "risk_factors": list(feature.risk_factors),
                    "nlr": feature.nlr,
                },
                biomarkers_involved=list(self.metadata.required_biomarkers) + list(self.metadata.optional_biomarkers or []),
                confidence=feature.confidence,
                severity=feature.severity,
                recommendations=list(feature.recommendations),
            )]
        except Exception as e:
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                error_code="CALCULATION_FAILED",
                error_detail=str(e),
            )]
