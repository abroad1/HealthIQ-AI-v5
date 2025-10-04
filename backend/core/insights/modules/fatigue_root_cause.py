"""
Fatigue root cause insight module.

Clinical implementation of fatigue root cause analysis based on iron metabolism,
thyroid function, vitamin deficiencies, and inflammatory markers.
"""

from typing import List, Dict, Any, Optional
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
    
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        try:
            # Extract biomarkers
            biomarkers = {k: v.value if hasattr(v, 'value') else v 
                         for k, v in context.biomarker_panel.biomarkers.items()}
            
            # Check for required biomarkers
            required = ["ferritin"]
            missing = [b for b in required if b not in biomarkers or biomarkers[b] is None]
            if missing:
                return [InsightResult(
                    insight_id=self.metadata.insight_id,
                    version=self.metadata.version,
                    manifest_id="",
                    error_code="MISSING_BIOMARKERS",
                    error_detail=f"Missing required biomarkers: {', '.join(missing)}"
                )]
            
            # Analyze fatigue root causes
            result = self._analyze_fatigue_causes(biomarkers)
            
            # Determine severity based on root causes
            severity = self._determine_severity(result['root_causes'])
            
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
    
    def _analyze_fatigue_causes(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze fatigue root causes using comprehensive biomarker assessment."""
        # Extract values
        ferritin = float(biomarkers.get('ferritin', 0))
        
        # Get optional biomarkers
        transferrin_sat = biomarkers.get('transferrin_saturation')
        b12 = biomarkers.get('b12')
        folate = biomarkers.get('folate')
        tsh = biomarkers.get('tsh')
        ft4 = biomarkers.get('ft4')
        ft3 = biomarkers.get('ft3')
        cortisol = biomarkers.get('cortisol')
        crp = biomarkers.get('crp')
        gender = biomarkers.get('gender', 'female')  # Default to female for ferritin thresholds
        
        # Initialize results
        root_causes = []
        drivers = {}
        evidence = {}
        
        # Iron deficiency analysis
        iron_deficiency = self._assess_iron_deficiency(ferritin, transferrin_sat, gender)
        if iron_deficiency['deficient']:
            root_causes.append("iron_deficiency")
            drivers.update(iron_deficiency['drivers'])
            evidence.update(iron_deficiency['evidence'])
        
        # Thyroid dysfunction analysis
        thyroid_dysfunction = self._assess_thyroid_function(tsh, ft4, ft3)
        if thyroid_dysfunction['dysfunction']:
            root_causes.append(thyroid_dysfunction['type'])
            drivers.update(thyroid_dysfunction['drivers'])
            evidence.update(thyroid_dysfunction['evidence'])
        
        # Vitamin deficiency analysis
        vitamin_deficiency = self._assess_vitamin_deficiencies(b12, folate)
        if vitamin_deficiency['deficient']:
            root_causes.append("vitamin_deficiency")
            drivers.update(vitamin_deficiency['drivers'])
            evidence.update(vitamin_deficiency['evidence'])
        
        # Inflammatory fatigue analysis
        inflammatory_fatigue = self._assess_inflammatory_fatigue(crp)
        if inflammatory_fatigue['present']:
            root_causes.append("inflammatory_fatigue")
            drivers.update(inflammatory_fatigue['drivers'])
            evidence.update(inflammatory_fatigue['evidence'])
        
        # Cortisol dysregulation analysis
        cortisol_dysregulation = self._assess_cortisol_dysregulation(cortisol)
        if cortisol_dysregulation['dysregulated']:
            root_causes.append(cortisol_dysregulation['type'])
            drivers.update(cortisol_dysregulation['drivers'])
            evidence.update(cortisol_dysregulation['evidence'])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(root_causes, iron_deficiency, 
                                                       thyroid_dysfunction, vitamin_deficiency,
                                                       inflammatory_fatigue, cortisol_dysregulation)
        
        return {
            'root_causes': root_causes,
            'drivers': drivers,
            'evidence': {
                'root_causes': root_causes,
                'iron_status': iron_deficiency['status'],
                'thyroid_status': thyroid_dysfunction['status'],
                'vitamin_status': vitamin_deficiency['status'],
                'inflammation_status': inflammatory_fatigue['status'],
                'cortisol_status': cortisol_dysregulation['status'],
                **evidence
            },
            'biomarkers_involved': [b for b in ['ferritin', 'transferrin_saturation', 'b12', 'folate', 'tsh', 'ft4', 'ft3', 'cortisol', 'crp'] if b in biomarkers],
            'recommendations': recommendations
        }
    
    def _assess_iron_deficiency(self, ferritin: float, transferrin_sat: Optional[float], gender: str) -> Dict[str, Any]:
        """Assess iron deficiency based on ferritin and transferrin saturation."""
        # Gender-specific ferritin thresholds
        ferritin_threshold = 15 if gender.lower() == 'male' else 12
        
        deficient = False
        status = "normal"
        drivers = {}
        evidence = {}
        
        if ferritin < ferritin_threshold:
            deficient = True
            status = "deficient"
            drivers['ferritin'] = round(ferritin, 1)
            evidence['ferritin'] = round(ferritin, 1)
            evidence['ferritin_threshold'] = ferritin_threshold
        elif ferritin < ferritin_threshold * 2:
            status = "low_normal"
            drivers['ferritin'] = round(ferritin, 1)
            evidence['ferritin'] = round(ferritin, 1)
        
        if transferrin_sat and transferrin_sat < 20:
            deficient = True
            status = "deficient"
            drivers['transferrin_saturation'] = round(transferrin_sat, 1)
            evidence['transferrin_saturation'] = round(transferrin_sat, 1)
        
        return {
            'deficient': deficient,
            'status': status,
            'drivers': drivers,
            'evidence': evidence
        }
    
    def _assess_thyroid_function(self, tsh: Optional[float], ft4: Optional[float], ft3: Optional[float]) -> Dict[str, Any]:
        """Assess thyroid function based on TSH, FT4, and FT3."""
        dysfunction = False
        dysfunction_type = None
        status = "normal"
        drivers = {}
        evidence = {}
        
        if tsh:
            if tsh > 4.5:
                dysfunction = True
                dysfunction_type = "hypothyroidism"
                status = "hypothyroid"
                drivers['tsh'] = round(tsh, 2)
                evidence['tsh'] = round(tsh, 2)
            elif tsh < 0.4:
                dysfunction = True
                dysfunction_type = "hyperthyroidism"
                status = "hyperthyroid"
                drivers['tsh'] = round(tsh, 2)
                evidence['tsh'] = round(tsh, 2)
            else:
                evidence['tsh'] = round(tsh, 2)
        
        if ft4:
            if ft4 < 0.8:
                dysfunction = True
                dysfunction_type = "hypothyroidism"
                status = "hypothyroid"
                drivers['ft4'] = round(ft4, 2)
                evidence['ft4'] = round(ft4, 2)
            elif ft4 > 1.8:
                dysfunction = True
                dysfunction_type = "hyperthyroidism"
                status = "hyperthyroid"
                drivers['ft4'] = round(ft4, 2)
                evidence['ft4'] = round(ft4, 2)
            else:
                evidence['ft4'] = round(ft4, 2)
        
        if ft3:
            if ft3 < 2.3:
                dysfunction = True
                dysfunction_type = "hypothyroidism"
                status = "hypothyroid"
                drivers['ft3'] = round(ft3, 2)
                evidence['ft3'] = round(ft3, 2)
            elif ft3 > 4.2:
                dysfunction = True
                dysfunction_type = "hyperthyroidism"
                status = "hyperthyroid"
                drivers['ft3'] = round(ft3, 2)
                evidence['ft3'] = round(ft3, 2)
            else:
                evidence['ft3'] = round(ft3, 2)
        
        return {
            'dysfunction': dysfunction,
            'type': dysfunction_type,
            'status': status,
            'drivers': drivers,
            'evidence': evidence
        }
    
    def _assess_vitamin_deficiencies(self, b12: Optional[float], folate: Optional[float]) -> Dict[str, Any]:
        """Assess vitamin B12 and folate deficiencies."""
        deficient = False
        status = "normal"
        drivers = {}
        evidence = {}
        
        if b12:
            if b12 < 200:
                deficient = True
                status = "deficient"
                drivers['b12'] = round(b12, 1)
                evidence['b12'] = round(b12, 1)
            elif b12 < 300:
                status = "low_normal"
                drivers['b12'] = round(b12, 1)
                evidence['b12'] = round(b12, 1)
            else:
                evidence['b12'] = round(b12, 1)
        
        if folate:
            if folate < 4:
                deficient = True
                status = "deficient"
                drivers['folate'] = round(folate, 1)
                evidence['folate'] = round(folate, 1)
            elif folate < 7:
                status = "low_normal"
                drivers['folate'] = round(folate, 1)
                evidence['folate'] = round(folate, 1)
            else:
                evidence['folate'] = round(folate, 1)
        
        return {
            'deficient': deficient,
            'status': status,
            'drivers': drivers,
            'evidence': evidence
        }
    
    def _assess_inflammatory_fatigue(self, crp: Optional[float]) -> Dict[str, Any]:
        """Assess inflammatory fatigue based on CRP."""
        present = False
        status = "normal"
        drivers = {}
        evidence = {}
        
        if crp:
            if crp > 3.0:
                present = True
                status = "high_inflammation"
                drivers['crp'] = round(crp, 2)
                evidence['crp'] = round(crp, 2)
            elif crp > 1.0:
                present = True
                status = "moderate_inflammation"
                drivers['crp'] = round(crp, 2)
                evidence['crp'] = round(crp, 2)
            else:
                evidence['crp'] = round(crp, 2)
        
        return {
            'present': present,
            'status': status,
            'drivers': drivers,
            'evidence': evidence
        }
    
    def _assess_cortisol_dysregulation(self, cortisol: Optional[float]) -> Dict[str, Any]:
        """Assess cortisol dysregulation."""
        dysregulated = False
        dysregulation_type = None
        status = "normal"
        drivers = {}
        evidence = {}
        
        if cortisol:
            if cortisol < 5:
                dysregulated = True
                dysregulation_type = "adrenal_insufficiency"
                status = "low_cortisol"
                drivers['cortisol'] = round(cortisol, 1)
                evidence['cortisol'] = round(cortisol, 1)
            elif cortisol > 25:
                dysregulated = True
                dysregulation_type = "hypercortisolism"
                status = "high_cortisol"
                drivers['cortisol'] = round(cortisol, 1)
                evidence['cortisol'] = round(cortisol, 1)
            else:
                evidence['cortisol'] = round(cortisol, 1)
        
        return {
            'dysregulated': dysregulated,
            'type': dysregulation_type,
            'status': status,
            'drivers': drivers,
            'evidence': evidence
        }
    
    def _determine_severity(self, root_causes: List[str]) -> str:
        """Determine severity based on number and type of root causes."""
        if len(root_causes) >= 3:
            return "critical"
        elif len(root_causes) >= 2:
            return "high"
        elif len(root_causes) >= 1:
            return "moderate"
        else:
            return "normal"
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> float:
        """Calculate confidence based on available biomarkers."""
        required_count = len([b for b in ["ferritin"] if b in biomarkers])
        optional_count = len([b for b in ["transferrin_saturation", "b12", "folate", "tsh", "ft4", "ft3", "cortisol", "crp"] if b in biomarkers])
        
        # Base confidence from required biomarkers
        base_confidence = 0.6 + (required_count * 0.2)
        
        # Bonus for optional biomarkers
        optional_bonus = min(optional_count * 0.05, 0.3)
        
        return min(base_confidence + optional_bonus, 0.95)
    
    def _generate_recommendations(self, root_causes: List[str], iron_deficiency: Dict, 
                                 thyroid_dysfunction: Dict, vitamin_deficiency: Dict,
                                 inflammatory_fatigue: Dict, cortisol_dysregulation: Dict) -> List[str]:
        """Generate personalized recommendations based on fatigue root causes."""
        recommendations = []
        
        if "iron_deficiency" in root_causes:
            recommendations.append("Address iron deficiency through iron supplementation and dietary modifications")
        if "hypothyroidism" in root_causes:
            recommendations.append("Consult with healthcare provider for thyroid function evaluation and potential treatment")
        if "hyperthyroidism" in root_causes:
            recommendations.append("Consult with healthcare provider for thyroid function evaluation and potential treatment")
        if "vitamin_deficiency" in root_causes:
            recommendations.append("Address vitamin deficiencies through targeted supplementation")
        if "inflammatory_fatigue" in root_causes:
            recommendations.append("Address underlying inflammation through anti-inflammatory diet and lifestyle modifications")
        if "adrenal_insufficiency" in root_causes:
            recommendations.append("Support adrenal function through stress management and adaptogenic herbs")
        if "hypercortisolism" in root_causes:
            recommendations.append("Address cortisol dysregulation through stress management and lifestyle modifications")
        
        if not recommendations:
            recommendations.append("Maintain current healthy lifestyle to prevent fatigue development")
        
        return recommendations
