"""Metabolic-age narrative module (InsightGraph-driven)."""

from typing import List

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.insights.base import BaseInsight
from core.insights.metadata import InsightMetadata, InsightResult
from core.insights.registry import register_insight
from core.models.context import AnalysisContext


@register_insight("metabolic_age", "v1.0.0")
class MetabolicAgeInsight(BaseInsight):
    """
    Calculates biological age based on metabolic markers.
    
    Clinical Rationale:
    - HOMA-IR (Homeostatic Model Assessment of Insulin Resistance) is the primary driver
    - HbA1c provides long-term glucose control assessment
    - Lipid ratios (TC/HDL, TG/HDL) indicate metabolic health
    - BMI and waist-to-height ratio assess body composition
    - Age adjustment based on metabolic dysfunction severity
    
    Thresholds:
    - HOMA-IR > 2.5: Insulin resistance
    - HOMA-IR > 4.0: Severe insulin resistance
    - HbA1c > 5.7%: Prediabetes
    - HbA1c > 6.5%: Diabetes
    - TC/HDL > 4.0: High cardiovascular risk
    - TG/HDL > 2.0: Metabolic dysfunction
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="metabolic_age",
            version="v1.0.0",
            category="metabolic",
            required_biomarkers=["glucose", "hba1c", "insulin", "age"],
            optional_biomarkers=["total_cholesterol", "hdl_cholesterol", "triglycerides", "bmi", "waist_circumference"],
            description="Calculates biological age based on metabolic markers using HOMA-IR and lipid ratios",
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
            feature = insight_graph.layer_c_features.metabolic_age
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                drivers={"risk_flags": list(feature.risk_flags), "homa_ir": feature.homa_ir},
                evidence={
                    "metabolic_age": feature.metabolic_age,
                    "age_delta_years": feature.age_delta_years,
                    "homa_ir": feature.homa_ir,
                    "risk_flags": list(feature.risk_flags),
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
