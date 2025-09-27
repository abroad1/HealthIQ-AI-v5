"""
Static biomarker rules and thresholds for scoring engines.

This module defines clinical thresholds and scoring rules for biomarkers
based on medical guidelines and reference ranges from SSOT data.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.canonical.resolver import CanonicalResolver


class ScoreRange(Enum):
    """Score range categories for biomarkers."""
    OPTIMAL = "optimal"
    NORMAL = "normal"
    BORDERLINE = "borderline"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"


@dataclass
class BiomarkerRule:
    """Rule definition for a single biomarker."""
    biomarker_name: str
    optimal_range: Tuple[float, float]
    normal_range: Tuple[float, float]
    borderline_range: Tuple[float, float]
    high_range: Tuple[float, float]
    very_high_range: Tuple[float, float]
    critical_range: Tuple[float, float]
    unit: str
    weight: float = 1.0
    age_adjustment: bool = False
    sex_adjustment: bool = False


@dataclass
class HealthSystemRules:
    """Rules for a complete health system."""
    system_name: str
    biomarkers: List[BiomarkerRule]
    min_biomarkers_required: int
    system_weight: float


class ScoringRules:
    """Static rules and thresholds for biomarker scoring."""
    
    def __init__(self, resolver: Optional[CanonicalResolver] = None):
        """
        Initialize scoring rules.
        
        Args:
            resolver: CanonicalResolver instance for reference ranges
        """
        self.resolver = resolver or CanonicalResolver()
        self._rules = self._load_biomarker_rules()
    
    def _load_biomarker_rules(self) -> Dict[str, HealthSystemRules]:
        """Load biomarker rules for all health systems."""
        return {
            "metabolic": self._get_metabolic_rules(),
            "cardiovascular": self._get_cardiovascular_rules(),
            "inflammatory": self._get_inflammatory_rules(),
            "hormonal": self._get_hormonal_rules(),
            "nutritional": self._get_nutritional_rules(),
            "kidney": self._get_kidney_rules(),
            "liver": self._get_liver_rules(),
            "cbc": self._get_cbc_rules()
        }
    
    def _get_metabolic_rules(self) -> HealthSystemRules:
        """Get metabolic health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="glucose",
                optimal_range=(70, 100),
                normal_range=(70, 100),
                borderline_range=(100, 125),
                high_range=(125, 200),
                very_high_range=(200, 300),
                critical_range=(300, 1000),
                unit="mg/dL",
                weight=0.4,
                age_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="hba1c",
                optimal_range=(4.0, 5.6),
                normal_range=(4.0, 5.6),
                borderline_range=(5.7, 6.4),
                high_range=(6.5, 8.0),
                very_high_range=(8.0, 10.0),
                critical_range=(10.0, 15.0),
                unit="%",
                weight=0.4,
                age_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="insulin",
                optimal_range=(2, 10),
                normal_range=(2, 25),
                borderline_range=(25, 35),
                high_range=(35, 50),
                very_high_range=(50, 100),
                critical_range=(100, 500),
                unit="μU/mL",
                weight=0.2
            )
        ]
        
        return HealthSystemRules(
            system_name="metabolic",
            biomarkers=biomarkers,
            min_biomarkers_required=2,
            system_weight=0.25
        )
    
    def _get_cardiovascular_rules(self) -> HealthSystemRules:
        """Get cardiovascular health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="total_cholesterol",
                optimal_range=(0, 200),
                normal_range=(0, 200),
                borderline_range=(200, 239),
                high_range=(240, 300),
                very_high_range=(300, 400),
                critical_range=(400, 1000),
                unit="mg/dL",
                weight=0.2
            ),
            BiomarkerRule(
                biomarker_name="ldl_cholesterol",
                optimal_range=(0, 100),
                normal_range=(0, 100),
                borderline_range=(100, 129),
                high_range=(130, 159),
                very_high_range=(160, 189),
                critical_range=(190, 500),
                unit="mg/dL",
                weight=0.3
            ),
            BiomarkerRule(
                biomarker_name="hdl_cholesterol",
                optimal_range=(60, 200),
                normal_range=(40, 200),
                borderline_range=(35, 40),
                high_range=(20, 35),
                very_high_range=(10, 20),
                critical_range=(0, 10),
                unit="mg/dL",
                weight=0.3,
                sex_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="triglycerides",
                optimal_range=(0, 150),
                normal_range=(0, 150),
                borderline_range=(150, 199),
                high_range=(200, 499),
                very_high_range=(500, 1000),
                critical_range=(1000, 5000),
                unit="mg/dL",
                weight=0.2
            )
        ]
        
        return HealthSystemRules(
            system_name="cardiovascular",
            biomarkers=biomarkers,
            min_biomarkers_required=3,
            system_weight=0.25
        )
    
    def _get_inflammatory_rules(self) -> HealthSystemRules:
        """Get inflammatory health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="crp",
                optimal_range=(0, 1.0),
                normal_range=(0, 3.0),
                borderline_range=(3.0, 10.0),
                high_range=(10.0, 50.0),
                very_high_range=(50.0, 100.0),
                critical_range=(100.0, 500.0),
                unit="mg/L",
                weight=1.0
            )
        ]
        
        return HealthSystemRules(
            system_name="inflammatory",
            biomarkers=biomarkers,
            min_biomarkers_required=1,
            system_weight=0.15
        )
    
    def _get_hormonal_rules(self) -> HealthSystemRules:
        """Get hormonal health system rules."""
        # Note: Hormonal biomarkers not yet defined in SSOT
        # Placeholder for future implementation
        biomarkers = []
        
        return HealthSystemRules(
            system_name="hormonal",
            biomarkers=biomarkers,
            min_biomarkers_required=0,
            system_weight=0.0
        )
    
    def _get_nutritional_rules(self) -> HealthSystemRules:
        """Get nutritional health system rules."""
        # Note: Nutritional biomarkers not yet defined in SSOT
        # Placeholder for future implementation
        biomarkers = []
        
        return HealthSystemRules(
            system_name="nutritional",
            biomarkers=biomarkers,
            min_biomarkers_required=0,
            system_weight=0.0
        )
    
    def _get_kidney_rules(self) -> HealthSystemRules:
        """Get kidney health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="creatinine",
                optimal_range=(0.6, 1.2),
                normal_range=(0.6, 1.2),
                borderline_range=(1.2, 1.5),
                high_range=(1.5, 2.0),
                very_high_range=(2.0, 3.0),
                critical_range=(3.0, 10.0),
                unit="mg/dL",
                weight=0.6,
                age_adjustment=True,
                sex_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="bun",
                optimal_range=(7, 20),
                normal_range=(7, 20),
                borderline_range=(20, 25),
                high_range=(25, 50),
                very_high_range=(50, 100),
                critical_range=(100, 200),
                unit="mg/dL",
                weight=0.4
            )
        ]
        
        return HealthSystemRules(
            system_name="kidney",
            biomarkers=biomarkers,
            min_biomarkers_required=1,
            system_weight=0.15
        )
    
    def _get_liver_rules(self) -> HealthSystemRules:
        """Get liver health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="alt",
                optimal_range=(7, 56),
                normal_range=(7, 56),
                borderline_range=(56, 100),
                high_range=(100, 200),
                very_high_range=(200, 500),
                critical_range=(500, 2000),
                unit="U/L",
                weight=0.5,
                sex_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="ast",
                optimal_range=(10, 40),
                normal_range=(10, 40),
                borderline_range=(40, 80),
                high_range=(80, 200),
                very_high_range=(200, 500),
                critical_range=(500, 2000),
                unit="U/L",
                weight=0.5
            )
        ]
        
        return HealthSystemRules(
            system_name="liver",
            biomarkers=biomarkers,
            min_biomarkers_required=1,
            system_weight=0.1
        )
    
    def _get_cbc_rules(self) -> HealthSystemRules:
        """Get CBC health system rules."""
        biomarkers = [
            BiomarkerRule(
                biomarker_name="hemoglobin",
                optimal_range=(12, 16),
                normal_range=(12, 16),
                borderline_range=(10, 12),
                high_range=(16, 18),
                very_high_range=(18, 20),
                critical_range=(20, 25),
                unit="g/dL",
                weight=0.4,
                sex_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="hematocrit",
                optimal_range=(36, 46),
                normal_range=(36, 46),
                borderline_range=(30, 36),
                high_range=(46, 52),
                very_high_range=(52, 60),
                critical_range=(60, 70),
                unit="%",
                weight=0.3,
                sex_adjustment=True
            ),
            BiomarkerRule(
                biomarker_name="white_blood_cells",
                optimal_range=(4.5, 11.0),
                normal_range=(4.5, 11.0),
                borderline_range=(3.5, 4.5),
                high_range=(11.0, 15.0),
                very_high_range=(15.0, 25.0),
                critical_range=(25.0, 50.0),
                unit="K/μL",
                weight=0.2
            ),
            BiomarkerRule(
                biomarker_name="platelets",
                optimal_range=(150, 450),
                normal_range=(150, 450),
                borderline_range=(100, 150),
                high_range=(450, 600),
                very_high_range=(600, 1000),
                critical_range=(1000, 2000),
                unit="K/μL",
                weight=0.1
            )
        ]
        
        return HealthSystemRules(
            system_name="cbc",
            biomarkers=biomarkers,
            min_biomarkers_required=2,
            system_weight=0.1
        )
    
    def get_biomarker_rule(self, biomarker_name: str) -> Optional[BiomarkerRule]:
        """
        Get rule for a specific biomarker.
        
        Args:
            biomarker_name: Name of the biomarker
            
        Returns:
            BiomarkerRule if found, None otherwise
        """
        for system_rules in self._rules.values():
            for rule in system_rules.biomarkers:
                if rule.biomarker_name == biomarker_name:
                    return rule
        return None
    
    def get_health_system_rules(self, system_name: str) -> Optional[HealthSystemRules]:
        """
        Get rules for a health system.
        
        Args:
            system_name: Name of the health system
            
        Returns:
            HealthSystemRules if found, None otherwise
        """
        return self._rules.get(system_name)
    
    def get_all_rules(self) -> Dict[str, HealthSystemRules]:
        """
        Get all health system rules.
        
        Returns:
            Dictionary of all health system rules
        """
        return self._rules.copy()
    
    def calculate_biomarker_score(
        self, 
        biomarker_name: str, 
        value: float, 
        age: Optional[int] = None,
        sex: Optional[str] = None
    ) -> Tuple[float, ScoreRange]:
        """
        Calculate score for a single biomarker.
        
        Args:
            biomarker_name: Name of the biomarker
            value: Biomarker value
            age: Patient age for age adjustments
            sex: Patient sex for sex adjustments
            
        Returns:
            Tuple of (score, score_range) where score is 0-100
        """
        rule = self.get_biomarker_rule(biomarker_name)
        if not rule:
            return 0.0, ScoreRange.CRITICAL
        
        # Apply age/sex adjustments if needed
        adjusted_value = self._apply_adjustments(value, rule, age, sex)
        
        # Determine score range
        score_range = self._determine_score_range(adjusted_value, rule)
        
        # Calculate score based on range
        score = self._calculate_range_score(adjusted_value, rule, score_range)
        
        return score, score_range
    
    def _apply_adjustments(
        self, 
        value: float, 
        rule: BiomarkerRule, 
        age: Optional[int], 
        sex: Optional[str]
    ) -> float:
        """Apply age and sex adjustments to biomarker value."""
        adjusted_value = value
        
        # Age adjustments (simplified - in production would use more complex formulas)
        if rule.age_adjustment and age:
            if age > 65:
                # Older adults may have different normal ranges
                if rule.biomarker_name in ["creatinine", "glucose"]:
                    adjusted_value *= 1.1  # Slightly higher normal for older adults
        
        # Sex adjustments
        if rule.sex_adjustment and sex:
            if sex.lower() == "female":
                if rule.biomarker_name in ["hemoglobin", "hematocrit"]:
                    adjusted_value *= 0.9  # Lower normal for females
                elif rule.biomarker_name in ["hdl_cholesterol"]:
                    adjusted_value *= 1.1  # Higher normal for females
        
        return adjusted_value
    
    def _determine_score_range(self, value: float, rule: BiomarkerRule) -> ScoreRange:
        """Determine which score range a value falls into."""
        if rule.optimal_range[0] <= value <= rule.optimal_range[1]:
            return ScoreRange.OPTIMAL
        elif rule.normal_range[0] <= value <= rule.normal_range[1]:
            return ScoreRange.NORMAL
        elif rule.borderline_range[0] <= value <= rule.borderline_range[1]:
            return ScoreRange.BORDERLINE
        elif rule.high_range[0] <= value <= rule.high_range[1]:
            return ScoreRange.HIGH
        elif rule.very_high_range[0] <= value <= rule.very_high_range[1]:
            return ScoreRange.VERY_HIGH
        else:
            return ScoreRange.CRITICAL
    
    def _calculate_range_score(
        self, 
        value: float, 
        rule: BiomarkerRule, 
        score_range: ScoreRange
    ) -> float:
        """Calculate score (0-100) based on score range."""
        if score_range == ScoreRange.OPTIMAL:
            return 100.0
        elif score_range == ScoreRange.NORMAL:
            return 90.0
        elif score_range == ScoreRange.BORDERLINE:
            return 70.0
        elif score_range == ScoreRange.HIGH:
            return 50.0
        elif score_range == ScoreRange.VERY_HIGH:
            return 30.0
        else:  # CRITICAL
            return 10.0
