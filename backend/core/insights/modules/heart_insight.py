"""
Heart insight module.

Clinical implementation of cardiovascular health assessment based on lipid profiles,
inflammatory markers, and cardiovascular risk factors.
"""

from typing import List

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.insights.base import BaseInsight
from core.insights.registry import register_insight
from core.insights.metadata import InsightMetadata, InsightResult
from core.models.context import AnalysisContext


@register_insight("heart_insight", "v1.0.0")
class HeartInsight(BaseInsight):
    """
    Cardiovascular health insight based on heart-related biomarkers.
    
    Clinical Rationale:
    - LDL/HDL ratio is the strongest predictor of cardiovascular risk
    - TC/HDL ratio provides additional risk stratification
    - TG/HDL ratio indicates metabolic dysfunction and insulin resistance
    - ApoB provides particle count assessment (more accurate than LDL-C)
    - hs-CRP indicates systemic inflammation and cardiovascular risk
    - Blood pressure integration when available
    
    Thresholds:
    - LDL/HDL > 3.5: High risk
    - TC/HDL > 4.0: High risk
    - TG/HDL > 2.0: Metabolic dysfunction
    - ApoB > 100 mg/dL: High risk
    - hs-CRP > 3.0 mg/L: High risk
    - hs-CRP > 1.0 mg/L: Moderate risk
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="heart_insight",
            version="v1.0.0",
            category="cardiovascular",
            required_biomarkers=["total_cholesterol", "hdl_cholesterol", "ldl_cholesterol"],
            optional_biomarkers=["triglycerides", "crp", "apob", "systolic_bp", "diastolic_bp"],
            description="Cardiovascular health assessment using lipid ratios and inflammatory markers",
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
            feature = insight_graph.layer_c_features.heart_insight
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                drivers={
                    "risk_factors": list(feature.risk_factors),
                    "ldl_hdl_ratio": feature.ldl_hdl_ratio,
                    "tc_hdl_ratio": feature.tc_hdl_ratio,
                    "tg_hdl_ratio": feature.tg_hdl_ratio,
                },
                evidence={
                    "heart_resilience_score": feature.heart_resilience_score,
                    "risk_factors": list(feature.risk_factors),
                    "ldl_hdl_ratio": feature.ldl_hdl_ratio,
                    "tc_hdl_ratio": feature.tc_hdl_ratio,
                    "tg_hdl_ratio": feature.tg_hdl_ratio,
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
