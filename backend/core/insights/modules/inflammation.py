"""
Silent inflammation insight module.

Clinical implementation of silent inflammation assessment based on inflammatory markers,
immune cell ratios, and iron metabolism indicators.
"""

from typing import List, Dict, Any, Optional
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
    
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        try:
            # Extract biomarkers
            biomarkers = {k: v.value if hasattr(v, 'value') else v 
                         for k, v in context.biomarker_panel.biomarkers.items()}
            
            # Check for required biomarkers
            required = ["crp"]
            missing = [b for b in required if b not in biomarkers or biomarkers[b] is None]
            if missing:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_BIOMARKERS",
                    error_detail=f"Missing required biomarkers: {', '.join(missing)}"
                )]
            
            # Calculate inflammation burden score and related metrics
            result = self._calculate_inflammation_burden(biomarkers)
            
            # Determine severity based on inflammation markers
            severity = self._determine_severity(result['inflammation_burden_score'], result['crp'], result['nlr'])
            
            # Calculate confidence based on available biomarkers
            confidence = self._calculate_confidence(biomarkers)
            
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",  # Will be set by orchestrator
                drivers=result['drivers'],
                evidence=result['evidence'],
                biomarkers_involved=result['biomarkers_involved'],
                confidence=confidence,
                severity=severity,
                recommendations=result['recommendations']
            )]
            
        except Exception as e:
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                error_code="CALCULATION_FAILED",
                error_detail=str(e)
            )]
    
    def _calculate_inflammation_burden(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate inflammation burden score using hs-CRP, NLR, and ferritin."""
        # Extract values
        crp = float(biomarkers.get('crp', 0))
        
        # Get optional biomarkers
        wbc = biomarkers.get('white_blood_cells')
        neutrophils = biomarkers.get('neutrophils')
        lymphocytes = biomarkers.get('lymphocytes')
        ferritin = biomarkers.get('ferritin')
        gender = biomarkers.get('gender', 'male')  # Default to male for ferritin thresholds
        
        # Calculate NLR if both neutrophil and lymphocyte counts are available
        nlr = None
        if neutrophils and lymphocytes and lymphocytes > 0:
            nlr = neutrophils / lymphocytes
        
        # Calculate base inflammation burden score (0-100, higher is worse)
        base_score = 0.0
        
        # hs-CRP adjustments (primary marker)
        if crp > 10.0:
            base_score += 40  # Very high inflammation
        elif crp > 3.0:
            base_score += 30  # High inflammation
        elif crp > 1.0:
            base_score += 20  # Moderate inflammation
        elif crp > 0.3:
            base_score += 10  # Mild inflammation
        else:
            base_score += 0   # Normal
        
        # NLR adjustments (immune stress)
        if nlr and nlr > 5.0:
            base_score += 25  # Very high immune stress
        elif nlr and nlr > 3.0:
            base_score += 20  # High immune stress
        elif nlr and nlr > 2.0:
            base_score += 10  # Moderate immune stress
        elif nlr and nlr > 1.5:
            base_score += 5   # Mild immune stress
        
        # Ferritin adjustments (inflammatory marker)
        if ferritin:
            # Different thresholds for men and women
            ferritin_threshold = 300 if gender.lower() == 'male' else 200
            if ferritin > ferritin_threshold * 2:
                base_score += 20  # Very high ferritin (inflammatory)
            elif ferritin > ferritin_threshold:
                base_score += 15  # High ferritin (inflammatory)
            elif ferritin > ferritin_threshold * 0.7:
                base_score += 5   # Mild elevation
        
        # WBC adjustments (general immune activation)
        if wbc and wbc > 12.0:
            base_score += 15  # High WBC (infection/inflammation)
        elif wbc and wbc > 10.0:
            base_score += 10  # Elevated WBC
        elif wbc and wbc > 8.0:
            base_score += 5   # Mild elevation
        
        # Ensure score is within bounds
        inflammation_burden_score = max(0, min(100, base_score))
        
        # Identify drivers and risk factors
        drivers = {}
        risk_factors = []
        
        if crp > 1.0:
            risk_factors.append("elevated_crp")
            drivers['crp'] = round(crp, 2)
        
        if nlr and nlr > 2.0:
            risk_factors.append("elevated_nlr")
            drivers['nlr'] = round(nlr, 2)
        
        if ferritin:
            ferritin_threshold = 300 if gender.lower() == 'male' else 200
            if ferritin > ferritin_threshold:
                risk_factors.append("elevated_ferritin")
                drivers['ferritin'] = round(ferritin, 1)
        
        if wbc and wbc > 10.0:
            risk_factors.append("elevated_wbc")
            drivers['wbc'] = round(wbc, 1)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, crp, nlr, ferritin, wbc)
        
        return {
            'inflammation_burden_score': round(inflammation_burden_score, 1),
            'crp': round(crp, 2),
            'nlr': round(nlr, 2) if nlr else None,
            'risk_factors': risk_factors,
            'drivers': drivers,
            'evidence': {
                'inflammation_burden_score': round(inflammation_burden_score, 1),
                'crp': round(crp, 2),
                'nlr': round(nlr, 2) if nlr else None,
                'ferritin': round(ferritin, 1) if ferritin else None,
                'wbc': round(wbc, 1) if wbc else None,
                'risk_factors': risk_factors
            },
            'biomarkers_involved': [b for b in ['crp', 'white_blood_cells', 'neutrophils', 'lymphocytes', 'ferritin'] if b in biomarkers],
            'recommendations': recommendations
        }
    
    def _determine_severity(self, inflammation_score: float, crp: float, nlr: Optional[float]) -> str:
        """Determine severity based on inflammation burden score and key markers."""
        if inflammation_score > 70 or crp > 10.0 or (nlr and nlr > 5.0):
            return "critical"
        elif inflammation_score > 50 or crp > 3.0 or (nlr and nlr > 3.0):
            return "high"
        elif inflammation_score > 30 or crp > 1.0 or (nlr and nlr > 2.0):
            return "moderate"
        elif inflammation_score > 10:
            return "mild"
        else:
            return "normal"
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> float:
        """Calculate confidence based on available biomarkers."""
        required_count = len([b for b in ["crp"] if b in biomarkers])
        optional_count = len([b for b in ["white_blood_cells", "neutrophils", "lymphocytes", "ferritin"] if b in biomarkers])
        
        # Base confidence from required biomarkers
        base_confidence = 0.8 + (required_count * 0.1)
        
        # Bonus for optional biomarkers
        optional_bonus = min(optional_count * 0.05, 0.15)
        
        return min(base_confidence + optional_bonus, 0.95)
    
    def _generate_recommendations(self, risk_factors: List[str], crp: float, nlr: Optional[float], 
                                 ferritin: Optional[float], wbc: Optional[float]) -> List[str]:
        """Generate personalized recommendations based on inflammation markers."""
        recommendations = []
        
        if "elevated_crp" in risk_factors:
            if crp > 3.0:
                recommendations.append("Address high inflammation through anti-inflammatory diet and stress management")
            else:
                recommendations.append("Focus on reducing mild inflammation through omega-3 supplementation and exercise")
        
        if "elevated_nlr" in risk_factors:
            recommendations.append("Support immune system through adequate sleep, stress reduction, and immune-supporting nutrients")
        
        if "elevated_ferritin" in risk_factors:
            recommendations.append("Investigate ferritin elevation - may indicate inflammation or iron overload")
        
        if "elevated_wbc" in risk_factors:
            recommendations.append("Monitor for signs of infection or chronic inflammatory conditions")
        
        if not recommendations:
            recommendations.append("Maintain current anti-inflammatory lifestyle to preserve low inflammation status")
        
        return recommendations
