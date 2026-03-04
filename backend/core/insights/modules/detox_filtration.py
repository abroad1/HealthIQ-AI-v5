"""Detox/filtration narrative module (InsightGraph-driven)."""

from typing import List

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.insights.base import BaseInsight
from core.insights.metadata import InsightMetadata, InsightResult
from core.insights.registry import register_insight
from core.models.context import AnalysisContext


@register_insight("detox_filtration", "v1.0.0")
class DetoxFiltrationInsight(BaseInsight):
    """
    Detox and filtration system assessment based on liver and kidney function markers.
    
    Clinical Rationale:
    - Liver enzymes (ALT, AST, GGT, ALP) indicate hepatocyte damage and bile flow
    - Bilirubin levels reflect liver conjugation and bile excretion capacity
    - Creatinine and eGFR assess kidney filtration function
    - Urea/creatinine ratio indicates kidney function and hydration status
    - Albumin levels reflect liver synthetic function and protein status
    
    Thresholds:
    - ALT > 40 U/L: Liver damage
    - AST > 40 U/L: Liver damage
    - GGT > 60 U/L: Bile duct obstruction or liver damage
    - ALP > 120 U/L: Bile duct obstruction or bone disease
    - Bilirubin > 1.2 mg/dL: Jaundice/liver dysfunction
    - eGFR < 60 mL/min/1.73m²: Kidney dysfunction
    - Creatinine > 1.2 mg/dL: Kidney dysfunction
    - Urea/Creatinine > 20: Dehydration or kidney dysfunction
    - Albumin < 3.5 g/dL: Liver dysfunction or malnutrition
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="detox_filtration",
            version="v1.0.0",
            category="metabolic",
            required_biomarkers=["creatinine"],
            optional_biomarkers=["alt", "ast", "ggt", "alp", "bilirubin", "egfr", "urea", "albumin"],
            description="Comprehensive detox and filtration system assessment using liver and kidney function markers",
            author="HealthIQ Team",
            created_at="2024-01-30T00:00:00Z",
            updated_at="2024-01-30T00:00:00Z"
        )
    
    def _extract_insight_graph(self, context: AnalysisContext) -> InsightGraphV1 | None:
        params = context.analysis_parameters or {}
        raw_graph = params.get("insight_graph")
        if isinstance(raw_graph, InsightGraphV1):
            return raw_graph
        if isinstance(raw_graph, dict):
            return InsightGraphV1.model_validate(raw_graph)
        return None

    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Render narrative output from precomputed InsightGraph features only."""
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
            feature = insight_graph.layer_c_features.detox_filtration
            drivers = {
                "risk_factors": list(feature.risk_factors),
                "egfr": feature.egfr,
                "egfr_source": feature.egfr_source,
                "urea_creatinine_ratio": feature.urea_creatinine_ratio,
            }
            evidence = {
                "detox_filtration_score": feature.detox_filtration_score,
                "liver_score": feature.liver_score,
                "kidney_score": feature.kidney_score,
                "risk_factors": list(feature.risk_factors),
                "egfr": feature.egfr,
                "egfr_source": feature.egfr_source,
                "urea_creatinine_ratio": feature.urea_creatinine_ratio,
            }
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                drivers=drivers,
                evidence=evidence,
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
