"""
Static biomarker rules and thresholds for scoring engines.

Lab-provided biomarkers: use ONLY lab reference ranges. No SSOT/global lookups.
Derived ratios (v5-computed, lab did not supply): may use explicit hard-coded bounds table.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Derived ratios v5 computes - only these may use hard-coded bounds when lab didn't supply
DERIVED_RATIOS = frozenset({
    "tc_hdl_ratio", "tg_hdl_ratio", "ldl_hdl_ratio", "chol_hdl_ratio",
    "apoB_apoA1_ratio", "non_hdl_cholesterol"
})

# Explicit hard-coded bounds for derived ratios only. Used when lab did not provide.
# Format: biomarker_name -> {min, max} for _calculate_score_from_range
DERIVED_RATIO_BOUNDS: Dict[str, Dict[str, float]] = {
    "tc_hdl_ratio": {"min": 0.0, "max": 5.0},
    "tg_hdl_ratio": {"min": 0.0, "max": 4.0},
    "ldl_hdl_ratio": {"min": 0.0, "max": 3.5},
}

# Sentinel for unscored (missing lab reference range)
UNSCORED_REASON = "missing_lab_reference_range"


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
    """Static rules and thresholds for biomarker scoring. No SSOT/global range lookups."""

    def __init__(self):
        """Initialize scoring rules."""
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
                biomarker_name="ldl",
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
                biomarker_name="hdl",
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
            ),
            BiomarkerRule(
                biomarker_name="tc_hdl_ratio",
                optimal_range=(0, 3.5),
                normal_range=(3.5, 5.0),
                borderline_range=(5.0, 6.0),
                high_range=(6.0, 8.0),
                very_high_range=(8.0, 10.0),
                critical_range=(10.0, 20.0),
                unit="ratio",
                weight=0.1
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
        Get rule for a specific biomarker by canonical key.
        
        Args:
            biomarker_name: Canonical biomarker name (e.g. hdl, ldl)
            
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
    
    def _is_derived_ratio(self, biomarker_name: str) -> bool:
        """True if biomarker is a derived ratio v5 computes (may use DERIVED_RATIO_BOUNDS when lab didn't supply)."""
        return biomarker_name in DERIVED_RATIOS

    def calculate_biomarker_score(
        self, 
        biomarker_name: str, 
        value: float, 
        age: Optional[int] = None,
        sex: Optional[str] = None,
        input_reference_range: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, ScoreRange, Optional[str]]:
        """
        Calculate score for a single biomarker.
        
        Lab-provided biomarkers: use ONLY lab reference range. Never SSOT/global.
        If no lab range, returns unscored with reason 'missing_lab_reference_range'.
        
        Derived ratios: may use hard-coded range only when lab did not supply it.
        
        Returns:
            Tuple of (score, score_range, unscored_reason). unscored_reason is None when scored.
        """
        # Priority 1: Use input reference range (lab) if available and valid
        if input_reference_range and isinstance(input_reference_range, dict):
            min_val = input_reference_range.get('min')
            max_val = input_reference_range.get('max')
            if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)) and min_val < max_val:
                score, score_range = self._calculate_score_from_range(value, float(min_val), float(max_val))
                return score, score_range, None

        # Lab-provided biomarkers: NEVER use SSOT or rule fallback
        if not self._is_derived_ratio(biomarker_name):
            return 0.0, ScoreRange.CRITICAL, UNSCORED_REASON

        # Derived ratios only: use explicit DERIVED_RATIO_BOUNDS table (no SSOT, no rule fallback)
        bounds = DERIVED_RATIO_BOUNDS.get(biomarker_name)
        if bounds and isinstance(bounds.get('min'), (int, float)) and isinstance(bounds.get('max'), (int, float)):
            min_val, max_val = bounds['min'], bounds['max']
            if min_val < max_val:
                score, score_range = self._calculate_score_from_range(value, float(min_val), float(max_val))
                return score, score_range, None

        # Derived ratio not in table: unscored
        return 0.0, ScoreRange.CRITICAL, UNSCORED_REASON
    
    def _calculate_score_from_range(self, value: float, min_val: float, max_val: float) -> Tuple[float, ScoreRange]:
        """
        Calculate score and status from a reference range.
        
        Args:
            value: Biomarker value
            min_val: Minimum of reference range
            max_val: Maximum of reference range
            
        Returns:
            Tuple of (score, score_range) where score is 0-100
        """
        range_span = max_val - min_val
        if range_span <= 0:
            return 0.0, ScoreRange.CRITICAL
        
        # Calculate how far into the range the value is (0.0 = at min, 1.0 = at max)
        position = (value - min_val) / range_span
        
        # Determine score range based on position within reference range
        # Optimal: middle 60% of range (20% to 80%)
        # Normal: 10% to 90% of range
        # Borderline: 5% to 95% of range
        # High/Low: outside normal but within borderline
        # Critical: outside borderline
        
        if 0.2 <= position <= 0.8:
            # Optimal range (middle 60%)
            score = 100.0
            score_range = ScoreRange.OPTIMAL
        elif 0.1 <= position <= 0.9:
            # Normal range (80% of range)
            # Score decreases linearly from 100 at 20% to 90 at 10%, and from 100 at 80% to 90 at 90%
            if position < 0.2:
                score = 90.0 + (position - 0.1) / 0.1 * 10.0  # 90 to 100
            elif position > 0.8:
                score = 100.0 - (position - 0.8) / 0.1 * 10.0  # 100 to 90
            else:
                score = 100.0
            score_range = ScoreRange.NORMAL
        elif 0.05 <= position <= 0.95:
            # Borderline range
            if position < 0.1:
                score = 70.0 + (position - 0.05) / 0.05 * 20.0  # 70 to 90
            elif position > 0.9:
                score = 90.0 - (position - 0.9) / 0.05 * 20.0  # 90 to 70
            else:
                score = 90.0
            score_range = ScoreRange.BORDERLINE
        elif position < 0.05:
            # Low (below range)
            if position < 0:
                # Critical low - value is below minimum
                excess_ratio = abs(position)  # How far below min (as ratio of range)
                score = max(0.0, 10.0 - excess_ratio * 50.0)  # 10 to 0, decreases with distance
                score_range = ScoreRange.CRITICAL
            else:
                # Borderline low - just below normal range
                score = 50.0 + (position - 0.0) / 0.05 * 20.0  # 50 to 70
                score_range = ScoreRange.BORDERLINE
        else:  # position > 0.95
            # High (above range)
            if position > 1.0:
                # Critical high - value is above maximum
                excess_ratio = position - 1.0  # How far above max (as ratio of range)
                score = max(0.0, 30.0 - excess_ratio * 50.0)  # 30 to 0, decreases with distance
                score_range = ScoreRange.CRITICAL
            else:
                # Borderline high - just above normal range
                score = 70.0 - (position - 0.95) / 0.05 * 20.0  # 70 to 50
                score_range = ScoreRange.HIGH
        
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
                elif rule.biomarker_name in ["hdl"]:
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
