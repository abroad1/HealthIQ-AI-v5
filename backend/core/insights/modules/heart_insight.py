"""
Heart insight module.

Clinical implementation of cardiovascular health assessment based on lipid profiles,
inflammatory markers, and cardiovascular risk factors.
"""

from typing import List, Dict, Any, Optional
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
    
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        try:
            # Extract biomarkers
            biomarkers = {k: v.value if hasattr(v, 'value') else v 
                         for k, v in context.biomarker_panel.biomarkers.items()}
            
            # Check for required biomarkers
            required = ["total_cholesterol", "hdl_cholesterol", "ldl_cholesterol"]
            missing = [b for b in required if b not in biomarkers or biomarkers[b] is None]
            if missing:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_BIOMARKERS",
                    error_detail=f"Missing required biomarkers: {', '.join(missing)}"
                )]
            
            # Calculate heart resilience score and related metrics
            result = self._calculate_heart_resilience(biomarkers)
            
            # Determine severity based on risk factors
            severity = self._determine_severity(result['risk_factors'])
            
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
    
    def _calculate_heart_resilience(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate heart resilience score using lipid ratios and inflammatory markers."""
        # Extract values
        total_chol = float(biomarkers.get('total_cholesterol', 0))
        hdl_chol = float(biomarkers.get('hdl_cholesterol', 0))
        ldl_chol = float(biomarkers.get('ldl_cholesterol', 0))
        
        # Get optional biomarkers
        triglycerides = biomarkers.get('triglycerides')
        crp = biomarkers.get('crp')
        apob = biomarkers.get('apob')
        systolic_bp = biomarkers.get('systolic_bp')
        diastolic_bp = biomarkers.get('diastolic_bp')
        
        # Calculate lipid ratios
        ldl_hdl_ratio = (ldl_chol / hdl_chol) if hdl_chol > 0 else 0
        tc_hdl_ratio = (total_chol / hdl_chol) if hdl_chol > 0 else 0
        tg_hdl_ratio = (triglycerides / hdl_chol) if triglycerides and hdl_chol and hdl_chol > 0 else None
        
        # Calculate base resilience score (0-100, higher is better)
        base_score = 100.0
        
        # LDL/HDL ratio adjustments (primary risk factor)
        if ldl_hdl_ratio > 4.0:
            base_score -= 30  # Very high risk
        elif ldl_hdl_ratio > 3.5:
            base_score -= 20  # High risk
        elif ldl_hdl_ratio > 2.5:
            base_score -= 10  # Moderate risk
        elif ldl_hdl_ratio > 2.0:
            base_score -= 5   # Mild risk
        
        # TC/HDL ratio adjustments
        if tc_hdl_ratio > 5.0:
            base_score -= 25  # Very high risk
        elif tc_hdl_ratio > 4.0:
            base_score -= 15  # High risk
        elif tc_hdl_ratio > 3.5:
            base_score -= 8   # Moderate risk
        elif tc_hdl_ratio > 3.0:
            base_score -= 3   # Mild risk
        
        # TG/HDL ratio adjustments (metabolic dysfunction)
        if tg_hdl_ratio and tg_hdl_ratio > 3.0:
            base_score -= 20  # High metabolic dysfunction
        elif tg_hdl_ratio and tg_hdl_ratio > 2.0:
            base_score -= 10  # Moderate metabolic dysfunction
        elif tg_hdl_ratio and tg_hdl_ratio > 1.5:
            base_score -= 5   # Mild metabolic dysfunction
        
        # ApoB adjustments (if available)
        if apob and apob > 120:
            base_score -= 15  # High particle count
        elif apob and apob > 100:
            base_score -= 8   # Moderate particle count
        elif apob and apob > 80:
            base_score -= 3   # Mild particle count
        
        # hs-CRP adjustments (inflammation)
        if crp and crp > 3.0:
            base_score -= 20  # High inflammation
        elif crp and crp > 1.0:
            base_score -= 10  # Moderate inflammation
        elif crp and crp > 0.3:
            base_score -= 3   # Mild inflammation
        
        # Blood pressure adjustments (if available)
        if systolic_bp and diastolic_bp:
            if systolic_bp > 140 or diastolic_bp > 90:
                base_score -= 15  # Hypertension
            elif systolic_bp > 130 or diastolic_bp > 85:
                base_score -= 8   # Pre-hypertension
            elif systolic_bp > 120 or diastolic_bp > 80:
                base_score -= 3   # Elevated
        
        # Ensure score is within bounds
        heart_resilience_score = max(0, min(100, base_score))
        
        # Identify risk factors and drivers
        risk_factors = []
        drivers = {}
        
        if ldl_hdl_ratio > 3.5:
            risk_factors.append("elevated_ldl_hdl_ratio")
            drivers['ldl_hdl_ratio'] = round(ldl_hdl_ratio, 2)
        
        if tc_hdl_ratio > 4.0:
            risk_factors.append("elevated_tc_hdl_ratio")
            drivers['tc_hdl_ratio'] = round(tc_hdl_ratio, 2)
        
        if tg_hdl_ratio and tg_hdl_ratio > 2.0:
            risk_factors.append("elevated_tg_hdl_ratio")
            drivers['tg_hdl_ratio'] = round(tg_hdl_ratio, 2)
        
        if apob and apob > 100:
            risk_factors.append("elevated_apob")
            drivers['apob'] = round(apob, 1)
        
        if crp and crp > 1.0:
            risk_factors.append("elevated_crp")
            drivers['crp'] = round(crp, 2)
        
        if systolic_bp and diastolic_bp and (systolic_bp > 130 or diastolic_bp > 85):
            risk_factors.append("elevated_bp")
            drivers['blood_pressure'] = f"{systolic_bp}/{diastolic_bp}"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, ldl_hdl_ratio, tc_hdl_ratio, 
                                                       tg_hdl_ratio, crp, apob, systolic_bp, diastolic_bp)
        
        return {
            'heart_resilience_score': round(heart_resilience_score, 1),
            'risk_factors': risk_factors,
            'drivers': drivers,
            'evidence': {
                'heart_resilience_score': round(heart_resilience_score, 1),
                'ldl_hdl_ratio': round(ldl_hdl_ratio, 2),
                'tc_hdl_ratio': round(tc_hdl_ratio, 2),
                'tg_hdl_ratio': round(tg_hdl_ratio, 2) if tg_hdl_ratio else None,
                'apob': round(apob, 1) if apob else None,
                'crp': round(crp, 2) if crp else None,
                'blood_pressure': f"{systolic_bp}/{diastolic_bp}" if systolic_bp and diastolic_bp else None,
                'risk_factors': risk_factors
            },
            'biomarkers_involved': [b for b in ['total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides', 'crp', 'apob', 'systolic_bp', 'diastolic_bp'] if b in biomarkers],
            'recommendations': recommendations
        }
    
    def _determine_severity(self, risk_factors: List[str]) -> str:
        """Determine severity based on number and type of risk factors."""
        if len(risk_factors) >= 4:
            return "critical"
        elif len(risk_factors) >= 3:
            return "high"
        elif len(risk_factors) >= 2:
            return "moderate"
        elif len(risk_factors) >= 1:
            return "mild"
        else:
            return "normal"
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> float:
        """Calculate confidence based on available biomarkers."""
        required_count = len([b for b in ["total_cholesterol", "hdl_cholesterol", "ldl_cholesterol"] if b in biomarkers])
        optional_count = len([b for b in ["triglycerides", "crp", "apob", "systolic_bp", "diastolic_bp"] if b in biomarkers])
        
        # Base confidence from required biomarkers
        base_confidence = 0.7 + (required_count * 0.1)
        
        # Bonus for optional biomarkers
        optional_bonus = min(optional_count * 0.05, 0.2)
        
        return min(base_confidence + optional_bonus, 0.95)
    
    def _generate_recommendations(self, risk_factors: List[str], ldl_hdl_ratio: float, tc_hdl_ratio: float,
                                 tg_hdl_ratio: Optional[float], crp: Optional[float], apob: Optional[float],
                                 systolic_bp: Optional[float], diastolic_bp: Optional[float]) -> List[str]:
        """Generate personalized recommendations based on cardiovascular risk factors."""
        recommendations = []
        
        if "elevated_ldl_hdl_ratio" in risk_factors:
            recommendations.append("Focus on reducing LDL cholesterol through statin therapy or dietary modifications")
        if "elevated_tc_hdl_ratio" in risk_factors:
            recommendations.append("Improve lipid profile through Mediterranean diet and regular exercise")
        if "elevated_tg_hdl_ratio" in risk_factors:
            recommendations.append("Address metabolic dysfunction through low-carb diet and weight management")
        if "elevated_apob" in risk_factors:
            recommendations.append("Consider advanced lipid testing and particle therapy if available")
        if "elevated_crp" in risk_factors:
            recommendations.append("Address systemic inflammation through anti-inflammatory diet and stress management")
        if "elevated_bp" in risk_factors:
            recommendations.append("Implement lifestyle modifications for blood pressure control")
        
        if not recommendations:
            recommendations.append("Maintain current cardiovascular health through regular exercise and heart-healthy diet")
        
        return recommendations
