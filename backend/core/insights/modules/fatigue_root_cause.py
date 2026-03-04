"""
Fatigue root cause insight module.

Clinical implementation of fatigue root cause analysis based on iron metabolism,
thyroid function, vitamin deficiencies, and inflammatory markers.
"""

from typing import List

from core.contracts.insight_graph_v1 import InsightGraphV1
from core.insights.base import BaseInsight
from core.insights.registry import register_insight
from core.insights.metadata import InsightMetadata, InsightResult
from core.models.context import AnalysisContext


@register_insight("fatigue_root_cause", "v1.0.0")
class FatigueRootCauseInsight(BaseInsight):
    """
    Fatigue root cause analysis based on comprehensive biomarker assessment.
    
    Clinical Rationale:
    - Iron deficiency is the most common cause of fatigue worldwide
    - Thyroid dysfunction (hypo/hyper) significantly impacts energy levels
    - B12 and folate deficiencies cause megaloblastic anemia and fatigue
    - Inflammatory fatigue from chronic inflammation and cytokine release
    - Cortisol dysregulation affects energy metabolism and sleep patterns
    
    Thresholds:
    - Ferritin < 30 ng/mL: Iron deficiency
    - Transferrin saturation < 20%: Iron deficiency
    - B12 < 200 pg/mL: Deficiency
    - Folate < 4 ng/mL: Deficiency
    - TSH > 4.5 mIU/L: Hypothyroidism
    - TSH < 0.4 mIU/L: Hyperthyroidism
    - FT4 < 0.8 ng/dL: Hypothyroidism
    - FT3 < 2.3 pg/mL: Hypothyroidism
    - Cortisol AM < 5 μg/dL: Adrenal insufficiency
    - Cortisol AM > 25 μg/dL: Hypercortisolism
    - CRP > 3.0 mg/L: Inflammatory fatigue
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="fatigue_root_cause",
            version="v1.0.0",
            category="metabolic",
            required_biomarkers=["ferritin"],
            optional_biomarkers=["transferrin_saturation", "b12", "folate", "tsh", "ft4", "ft3", "cortisol", "crp"],
            description="Comprehensive fatigue root cause analysis using iron, thyroid, vitamin, and inflammatory markers",
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
            feature = insight_graph.layer_c_features.fatigue_root_cause
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                drivers={
                    "root_causes": list(feature.root_causes),
                    "iron_status": feature.iron_status,
                    "thyroid_status": feature.thyroid_status,
                },
                evidence={
                    "root_causes": list(feature.root_causes),
                    "iron_status": feature.iron_status,
                    "thyroid_status": feature.thyroid_status,
                    "vitamin_status": feature.vitamin_status,
                    "inflammation_status": feature.inflammation_status,
                    "cortisol_status": feature.cortisol_status,
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
