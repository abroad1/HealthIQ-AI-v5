"""
Metabolic age insight module.

Clinical implementation of metabolic age calculation based on insulin resistance,
lipid metabolism, and body composition markers.
"""

from typing import List, Dict, Any, Optional
from core.insights.base import BaseInsight
from core.insights.registry import register_insight
from core.insights.metadata import InsightMetadata, InsightResult
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
    
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        try:
            # Extract biomarkers
            biomarkers = {k: v.value if hasattr(v, 'value') else v 
                         for k, v in context.biomarker_panel.biomarkers.items()}
            
            # Check for required biomarkers
            required = ["glucose", "hba1c", "insulin", "age"]
            missing = [b for b in required if b not in biomarkers or biomarkers[b] is None]
            if missing:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_BIOMARKERS",
                    error_detail=f"Missing required biomarkers: {', '.join(missing)}"
                )]
            
            # Calculate metabolic age and related metrics
            result = self._calculate_metabolic_age(biomarkers)
            
            # Determine severity based on metabolic age vs chronological age
            chronological_age = biomarkers.get('age', 0)
            delta = result['metabolic_age'] - chronological_age
            severity = self._determine_severity(delta, result['homa_ir'], result['hba1c'])
            
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
    
    def _calculate_metabolic_age(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metabolic age using HOMA-IR, HbA1c, and lipid ratios."""
        # Extract values
        glucose = float(biomarkers.get('glucose', 0))
        hba1c = float(biomarkers.get('hba1c', 0))
        insulin = float(biomarkers.get('insulin', 0))
        age = float(biomarkers.get('age', 0))
        
        # Calculate HOMA-IR
        homa_ir = (glucose * insulin) / 405.0 if glucose > 0 and insulin > 0 else 0
        
        # Get optional biomarkers
        total_chol = biomarkers.get('total_cholesterol')
        hdl_chol = biomarkers.get('hdl_cholesterol')
        triglycerides = biomarkers.get('triglycerides')
        bmi = biomarkers.get('bmi')
        waist_circ = biomarkers.get('waist_circumference')
        height = biomarkers.get('height')
        
        # Calculate lipid ratios if available
        tc_hdl_ratio = (total_chol / hdl_chol) if total_chol and hdl_chol and hdl_chol > 0 else None
        tg_hdl_ratio = (triglycerides / hdl_chol) if triglycerides and hdl_chol and hdl_chol > 0 else None
        
        # Calculate waist-to-height ratio if available
        waist_height_ratio = (waist_circ / height) if waist_circ and height and height > 0 else None
        
        # Calculate metabolic age adjustment factors
        age_adjustment = 0
        
        # HOMA-IR adjustment (primary factor)
        if homa_ir > 4.0:
            age_adjustment += 8  # Severe insulin resistance
        elif homa_ir > 2.5:
            age_adjustment += 4  # Insulin resistance
        elif homa_ir > 1.5:
            age_adjustment += 1  # Mild insulin resistance
        
        # HbA1c adjustment
        if hba1c > 6.5:
            age_adjustment += 6  # Diabetes
        elif hba1c > 5.7:
            age_adjustment += 3  # Prediabetes
        elif hba1c > 5.4:
            age_adjustment += 1  # Elevated
        
        # Lipid ratio adjustments
        if tc_hdl_ratio and tc_hdl_ratio > 4.0:
            age_adjustment += 3  # High cardiovascular risk
        elif tc_hdl_ratio and tc_hdl_ratio > 3.5:
            age_adjustment += 1  # Moderate risk
        
        if tg_hdl_ratio and tg_hdl_ratio > 2.0:
            age_adjustment += 2  # Metabolic dysfunction
        
        # BMI adjustment
        if bmi and bmi > 30:
            age_adjustment += 3  # Obesity
        elif bmi and bmi > 25:
            age_adjustment += 1  # Overweight
        
        # Waist-to-height ratio adjustment
        if waist_height_ratio and waist_height_ratio > 0.5:
            age_adjustment += 2  # Central obesity
        
        # Calculate final metabolic age
        metabolic_age = max(age + age_adjustment, age)  # Never below chronological age
        
        # Identify primary drivers
        drivers = {}
        if homa_ir > 2.5:
            drivers['homa_ir'] = round(homa_ir, 2)
        if hba1c > 5.7:
            drivers['hba1c'] = round(hba1c, 1)
        if tc_hdl_ratio and tc_hdl_ratio > 3.5:
            drivers['tc_hdl_ratio'] = round(tc_hdl_ratio, 2)
        if tg_hdl_ratio and tg_hdl_ratio > 2.0:
            drivers['tg_hdl_ratio'] = round(tg_hdl_ratio, 2)
        if bmi and bmi > 25:
            drivers['bmi'] = round(bmi, 1)
        if waist_height_ratio and waist_height_ratio > 0.5:
            drivers['waist_height_ratio'] = round(waist_height_ratio, 2)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(homa_ir, hba1c, tc_hdl_ratio, tg_hdl_ratio, bmi, waist_height_ratio)
        
        return {
            'metabolic_age': round(metabolic_age, 1),
            'homa_ir': round(homa_ir, 2),
            'hba1c': round(hba1c, 1),
            'drivers': drivers,
            'evidence': {
                'metabolic_age': round(metabolic_age, 1),
                'chronological_age': age,
                'age_delta': round(metabolic_age - age, 1),
                'homa_ir': round(homa_ir, 2),
                'hba1c': round(hba1c, 1),
                'tc_hdl_ratio': round(tc_hdl_ratio, 2) if tc_hdl_ratio else None,
                'tg_hdl_ratio': round(tg_hdl_ratio, 2) if tg_hdl_ratio else None,
                'bmi': round(bmi, 1) if bmi else None,
                'waist_height_ratio': round(waist_height_ratio, 2) if waist_height_ratio else None
            },
            'biomarkers_involved': [b for b in ['glucose', 'hba1c', 'insulin', 'age', 'total_cholesterol', 'hdl_cholesterol', 'triglycerides', 'bmi', 'waist_circumference'] if b in biomarkers],
            'recommendations': recommendations
        }
    
    def _determine_severity(self, delta: float, homa_ir: float, hba1c: float) -> str:
        """Determine severity based on metabolic age delta and key markers."""
        if delta > 10 or homa_ir > 4.0 or hba1c > 6.5:
            return "critical"
        elif delta > 5 or homa_ir > 2.5 or hba1c > 5.7:
            return "high"
        elif delta > 2 or homa_ir > 1.5 or hba1c > 5.4:
            return "moderate"
        elif delta > 0:
            return "mild"
        else:
            return "normal"
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> float:
        """Calculate confidence based on available biomarkers."""
        required_count = len([b for b in ["glucose", "hba1c", "insulin", "age"] if b in biomarkers])
        optional_count = len([b for b in ["total_cholesterol", "hdl_cholesterol", "triglycerides", "bmi", "waist_circumference"] if b in biomarkers])
        
        # Base confidence from required biomarkers
        base_confidence = 0.6 + (required_count * 0.1)
        
        # Bonus for optional biomarkers
        optional_bonus = min(optional_count * 0.05, 0.2)
        
        return min(base_confidence + optional_bonus, 0.95)
    
    def _generate_recommendations(self, homa_ir: float, hba1c: float, tc_hdl_ratio: Optional[float], 
                                 tg_hdl_ratio: Optional[float], bmi: Optional[float], 
                                 waist_height_ratio: Optional[float]) -> List[str]:
        """Generate personalized recommendations based on metabolic markers."""
        recommendations = []
        
        if homa_ir > 2.5:
            recommendations.append("Focus on insulin sensitivity through low-carb diet and regular exercise")
        if hba1c > 5.7:
            recommendations.append("Consider glucose monitoring and dietary modifications to improve HbA1c")
        if tc_hdl_ratio and tc_hdl_ratio > 4.0:
            recommendations.append("Address lipid profile through dietary changes and cardiovascular exercise")
        if tg_hdl_ratio and tg_hdl_ratio > 2.0:
            recommendations.append("Reduce refined carbohydrates and increase omega-3 fatty acids")
        if bmi and bmi > 25:
            recommendations.append("Implement sustainable weight management through caloric deficit and strength training")
        if waist_height_ratio and waist_height_ratio > 0.5:
            recommendations.append("Focus on reducing visceral fat through targeted exercise and diet")
        
        if not recommendations:
            recommendations.append("Maintain current healthy lifestyle to preserve metabolic health")
        
        return recommendations
