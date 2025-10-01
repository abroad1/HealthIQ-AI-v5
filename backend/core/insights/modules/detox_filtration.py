"""
Detox filtration insight module.

Clinical implementation of detoxification and filtration system assessment based on
liver function markers, kidney function markers, and filtration efficiency indicators.
"""

from typing import List, Dict, Any, Optional
from core.insights.base import BaseInsight
from core.insights.registry import register_insight
from core.insights.metadata import InsightMetadata, InsightResult
from core.models.context import AnalysisContext


@register_insight("detox_filtration", "v1.0.0")
class DetoxFiltrationInsight(BaseInsight):
    """
    Detox and filtration system assessment based on liver and kidney function markers.
    
    Clinical Rationale:
    - Liver enzymes (ALT, AST, GGT, ALP) indicate hepatocyte damage and bile flow
    - Bilirubin levels reflect liver conjugation and bile excretion capacity
    - Creatinine and eGFR assess kidney filtration function
    - BUN/creatinine ratio indicates kidney function and hydration status
    - Albumin levels reflect liver synthetic function and protein status
    
    Thresholds:
    - ALT > 40 U/L: Liver damage
    - AST > 40 U/L: Liver damage
    - GGT > 60 U/L: Bile duct obstruction or liver damage
    - ALP > 120 U/L: Bile duct obstruction or bone disease
    - Bilirubin > 1.2 mg/dL: Jaundice/liver dysfunction
    - eGFR < 60 mL/min/1.73m²: Kidney dysfunction
    - Creatinine > 1.2 mg/dL: Kidney dysfunction
    - BUN/Creatinine > 20: Dehydration or kidney dysfunction
    - Albumin < 3.5 g/dL: Liver dysfunction or malnutrition
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="detox_filtration",
            version="v1.0.0",
            category="metabolic",
            required_biomarkers=["creatinine"],
            optional_biomarkers=["alt", "ast", "ggt", "alp", "bilirubin", "egfr", "bun", "albumin"],
            description="Comprehensive detox and filtration system assessment using liver and kidney function markers",
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
            required = ["creatinine"]
            missing = [b for b in required if b not in biomarkers or biomarkers[b] is None]
            if missing:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_BIOMARKERS",
                    error_detail=f"Missing required biomarkers: {', '.join(missing)}"
                )]
            
            # Calculate detox filtration score and related metrics
            result = self._calculate_detox_filtration_score(biomarkers)
            
            # Determine severity based on liver and kidney function
            severity = self._determine_severity(result['liver_score'], result['kidney_score'], result['overall_score'])
            
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
    
    def _calculate_detox_filtration_score(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detox filtration score using liver and kidney function markers."""
        # Extract values
        creatinine = float(biomarkers.get('creatinine', 0))
        
        # Get optional biomarkers
        alt = biomarkers.get('alt')
        ast = biomarkers.get('ast')
        ggt = biomarkers.get('ggt')
        alp = biomarkers.get('alp')
        bilirubin = biomarkers.get('bilirubin')
        egfr = biomarkers.get('egfr')
        bun = biomarkers.get('bun')
        albumin = biomarkers.get('albumin')
        age = biomarkers.get('age', 50)  # Default age for eGFR calculation
        gender = biomarkers.get('gender', 'male')  # Default gender for eGFR calculation
        
        # Calculate liver score
        liver_score = self._calculate_liver_score(alt, ast, ggt, alp, bilirubin, albumin)
        
        # Calculate kidney score
        kidney_score = self._calculate_kidney_score(creatinine, egfr, bun, age, gender)
        
        # Calculate overall detox filtration score
        overall_score = (liver_score + kidney_score) / 2
        
        # Identify drivers and risk factors
        drivers = {}
        risk_factors = []
        
        # Liver risk factors
        if alt and alt > 40:
            risk_factors.append("elevated_alt")
            drivers['alt'] = round(alt, 1)
        if ast and ast > 40:
            risk_factors.append("elevated_ast")
            drivers['ast'] = round(ast, 1)
        if ggt and ggt > 60:
            risk_factors.append("elevated_ggt")
            drivers['ggt'] = round(ggt, 1)
        if alp and alp > 120:
            risk_factors.append("elevated_alp")
            drivers['alp'] = round(alp, 1)
        if bilirubin and bilirubin > 1.2:
            risk_factors.append("elevated_bilirubin")
            drivers['bilirubin'] = round(bilirubin, 2)
        if albumin and albumin < 3.5:
            risk_factors.append("low_albumin")
            drivers['albumin'] = round(albumin, 1)
        
        # Kidney risk factors
        if egfr and egfr < 60:
            risk_factors.append("reduced_egfr")
            drivers['egfr'] = round(egfr, 1)
        if creatinine > 1.2:
            risk_factors.append("elevated_creatinine")
            drivers['creatinine'] = round(creatinine, 2)
        if bun and creatinine > 0:
            bun_creatinine_ratio = bun / creatinine
            if bun_creatinine_ratio > 20:
                risk_factors.append("elevated_bun_creatinine_ratio")
                drivers['bun_creatinine_ratio'] = round(bun_creatinine_ratio, 1)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, liver_score, kidney_score)
        
        return {
            'detox_filtration_score': round(overall_score, 1),
            'liver_score': round(liver_score, 1),
            'kidney_score': round(kidney_score, 1),
            'overall_score': round(overall_score, 1),
            'risk_factors': risk_factors,
            'drivers': drivers,
            'evidence': {
                'detox_filtration_score': round(overall_score, 1),
                'liver_score': round(liver_score, 1),
                'kidney_score': round(kidney_score, 1),
                'alt': round(alt, 1) if alt else None,
                'ast': round(ast, 1) if ast else None,
                'ggt': round(ggt, 1) if ggt else None,
                'alp': round(alp, 1) if alp else None,
                'bilirubin': round(bilirubin, 2) if bilirubin else None,
                'egfr': round(egfr, 1) if egfr else None,
                'creatinine': round(creatinine, 2),
                'bun': round(bun, 1) if bun else None,
                'albumin': round(albumin, 1) if albumin else None,
                'risk_factors': risk_factors
            },
            'biomarkers_involved': [b for b in ['creatinine', 'alt', 'ast', 'ggt', 'alp', 'bilirubin', 'egfr', 'bun', 'albumin'] if b in biomarkers],
            'recommendations': recommendations
        }
    
    def _calculate_liver_score(self, alt: Optional[float], ast: Optional[float], ggt: Optional[float], 
                              alp: Optional[float], bilirubin: Optional[float], albumin: Optional[float]) -> float:
        """Calculate liver function score (0-100, higher is better)."""
        base_score = 100.0
        
        # ALT adjustments
        if alt:
            if alt > 100:
                base_score -= 30  # Severe liver damage
            elif alt > 60:
                base_score -= 20  # Moderate liver damage
            elif alt > 40:
                base_score -= 10  # Mild liver damage
        
        # AST adjustments
        if ast:
            if ast > 100:
                base_score -= 30  # Severe liver damage
            elif ast > 60:
                base_score -= 20  # Moderate liver damage
            elif ast > 40:
                base_score -= 10  # Mild liver damage
        
        # GGT adjustments (bile duct function)
        if ggt:
            if ggt > 120:
                base_score -= 25  # Severe bile duct obstruction
            elif ggt > 80:
                base_score -= 15  # Moderate bile duct obstruction
            elif ggt > 60:
                base_score -= 8   # Mild bile duct obstruction
        
        # ALP adjustments (bile duct and bone)
        if alp:
            if alp > 200:
                base_score -= 20  # Severe elevation
            elif alp > 150:
                base_score -= 12  # Moderate elevation
            elif alp > 120:
                base_score -= 6   # Mild elevation
        
        # Bilirubin adjustments (conjugation and excretion)
        if bilirubin:
            if bilirubin > 3.0:
                base_score -= 25  # Severe jaundice
            elif bilirubin > 2.0:
                base_score -= 15  # Moderate jaundice
            elif bilirubin > 1.2:
                base_score -= 8   # Mild jaundice
        
        # Albumin adjustments (synthetic function)
        if albumin:
            if albumin < 2.5:
                base_score -= 20  # Severe hypoalbuminemia
            elif albumin < 3.0:
                base_score -= 12  # Moderate hypoalbuminemia
            elif albumin < 3.5:
                base_score -= 6   # Mild hypoalbuminemia
        
        return max(0, min(100, base_score))
    
    def _calculate_kidney_score(self, creatinine: float, egfr: Optional[float], bun: Optional[float], 
                               age: float, gender: str) -> float:
        """Calculate kidney function score (0-100, higher is better)."""
        base_score = 100.0
        
        # Creatinine adjustments
        if creatinine > 2.0:
            base_score -= 40  # Severe kidney dysfunction
        elif creatinine > 1.5:
            base_score -= 25  # Moderate kidney dysfunction
        elif creatinine > 1.2:
            base_score -= 12  # Mild kidney dysfunction
        
        # eGFR adjustments (if available)
        if egfr:
            if egfr < 30:
                base_score -= 40  # Severe kidney dysfunction
            elif egfr < 45:
                base_score -= 25  # Moderate kidney dysfunction
            elif egfr < 60:
                base_score -= 12  # Mild kidney dysfunction
        else:
            # Estimate eGFR if not provided
            estimated_egfr = self._estimate_egfr(creatinine, age, gender)
            if estimated_egfr < 30:
                base_score -= 40
            elif estimated_egfr < 45:
                base_score -= 25
            elif estimated_egfr < 60:
                base_score -= 12
        
        # BUN/Creatinine ratio adjustments
        if bun and creatinine > 0:
            bun_creatinine_ratio = bun / creatinine
            if bun_creatinine_ratio > 30:
                base_score -= 15  # Severe dehydration or kidney dysfunction
            elif bun_creatinine_ratio > 20:
                base_score -= 8   # Moderate dehydration or kidney dysfunction
        
        return max(0, min(100, base_score))
    
    def _estimate_egfr(self, creatinine: float, age: float, gender: str) -> float:
        """Estimate eGFR using simplified MDRD formula."""
        # Simplified MDRD formula: eGFR = 175 * (creatinine^-1.154) * (age^-0.203) * (0.742 if female)
        gender_factor = 0.742 if gender.lower() == 'female' else 1.0
        egfr = 175 * (creatinine ** -1.154) * (age ** -0.203) * gender_factor
        return max(0, min(200, egfr))  # Clamp between 0 and 200
    
    def _determine_severity(self, liver_score: float, kidney_score: float, overall_score: float) -> str:
        """Determine severity based on liver and kidney scores."""
        if overall_score < 30 or liver_score < 30 or kidney_score < 30:
            return "critical"
        elif overall_score < 50 or liver_score < 50 or kidney_score < 50:
            return "high"
        elif overall_score < 70 or liver_score < 70 or kidney_score < 70:
            return "moderate"
        elif overall_score < 85:
            return "mild"
        else:
            return "normal"
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> float:
        """Calculate confidence based on available biomarkers."""
        required_count = len([b for b in ["creatinine"] if b in biomarkers])
        optional_count = len([b for b in ["alt", "ast", "ggt", "alp", "bilirubin", "egfr", "bun", "albumin"] if b in biomarkers])
        
        # Base confidence from required biomarkers
        base_confidence = 0.7 + (required_count * 0.2)
        
        # Bonus for optional biomarkers
        optional_bonus = min(optional_count * 0.05, 0.2)
        
        return min(base_confidence + optional_bonus, 0.95)
    
    def _generate_recommendations(self, risk_factors: List[str], liver_score: float, kidney_score: float) -> List[str]:
        """Generate personalized recommendations based on detox filtration markers."""
        recommendations = []
        
        if "elevated_alt" in risk_factors or "elevated_ast" in risk_factors:
            recommendations.append("Support liver function through milk thistle, NAC, and reduced alcohol consumption")
        if "elevated_ggt" in risk_factors or "elevated_alp" in risk_factors:
            recommendations.append("Address bile duct function through choleretic herbs and digestive support")
        if "elevated_bilirubin" in risk_factors:
            recommendations.append("Support liver conjugation and bile excretion through targeted liver support")
        if "low_albumin" in risk_factors:
            recommendations.append("Improve protein synthesis through adequate protein intake and liver support")
        if "reduced_egfr" in risk_factors or "elevated_creatinine" in risk_factors:
            recommendations.append("Support kidney function through adequate hydration and kidney-supporting nutrients")
        if "elevated_bun_creatinine_ratio" in risk_factors:
            recommendations.append("Address dehydration and kidney function through proper hydration")
        
        if not recommendations:
            recommendations.append("Maintain current healthy lifestyle to preserve detox and filtration function")
        
        return recommendations
