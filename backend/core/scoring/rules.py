"""
Scoring rules loaded from versioned SSOT scoring policy.

Lab-provided biomarkers: use ONLY lab reference ranges. No SSOT/global range lookups.
Derived ratios (v5-computed, lab did not supply): may use policy-defined derived bounds.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.analytics.primitives import position_in_range, map_position_to_status
from core.analytics.scoring_policy_registry import load_scoring_policy

_POLICY = load_scoring_policy()
DERIVED_RATIOS = frozenset(_POLICY.raw.get("derived_ratios", []))
DERIVED_RATIO_BOUNDS: Dict[str, Dict[str, float]] = {
    k: {"min": float(v["min"]), "max": float(v["max"])}
    for k, v in (_POLICY.raw.get("derived_ratio_bounds", {}) or {}).items()
    if isinstance(v, dict)
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
    """Versioned SSOT-backed rules for biomarker scoring."""

    def __init__(self):
        self._policy = load_scoring_policy()
        self._rules = self._load_biomarker_rules()
        self._has_to_score_range = self._build_has_status_map()
        self._score_curve = self._policy.raw.get("score_curve", {})
    
    def _to_tuple(self, range_map: Dict[str, Any]) -> Tuple[float, float]:
        return float(range_map["min"]), float(range_map["max"])

    def _build_has_status_map(self) -> Dict[str, ScoreRange]:
        mapping = self._policy.raw.get("status_map", {})
        out: Dict[str, ScoreRange] = {}
        for has_status, score_range in mapping.items():
            try:
                out[str(has_status)] = ScoreRange(str(score_range))
            except ValueError:
                continue
        return out

    def _build_biomarker_rule(self, biomarker_name: str, item: Dict[str, Any]) -> BiomarkerRule:
        bands = item.get("bands", {})
        return BiomarkerRule(
            biomarker_name=biomarker_name,
            optimal_range=self._to_tuple(bands["optimal"]),
            normal_range=self._to_tuple(bands["normal"]),
            borderline_range=self._to_tuple(bands["borderline"]),
            high_range=self._to_tuple(bands["high"]),
            very_high_range=self._to_tuple(bands["very_high"]),
            critical_range=self._to_tuple(bands["critical"]),
            unit=str(item.get("unit", "")),
            weight=float(item.get("weight", 1.0)),
            age_adjustment=bool(item.get("age_adjustment", False)),
            sex_adjustment=bool(item.get("sex_adjustment", False)),
        )

    def _load_biomarker_rules(self) -> Dict[str, HealthSystemRules]:
        systems = self._policy.raw.get("systems", {})
        biomarkers = self._policy.raw.get("biomarkers", {})
        out: Dict[str, HealthSystemRules] = {}
        for system_name, sys_item in systems.items():
            biomarker_rules: List[BiomarkerRule] = []
            for biomarker_name in sys_item.get("biomarkers", []):
                policy_item = biomarkers.get(biomarker_name)
                if isinstance(policy_item, dict):
                    biomarker_rules.append(self._build_biomarker_rule(str(biomarker_name), policy_item))
            out[str(system_name)] = HealthSystemRules(
                system_name=str(system_name),
                biomarkers=biomarker_rules,
                min_biomarkers_required=int(sys_item.get("min_biomarkers_required", 0)),
                system_weight=float(sys_item.get("system_weight", 0.0)),
            )
        return out
    
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

        Uses HAS v1 position_in_range and map_position_to_status for consistency.

        Args:
            value: Biomarker value
            min_val: Minimum of reference range
            max_val: Maximum of reference range

        Returns:
            Tuple of (score, score_range) where score is 0-100
        """
        position = position_in_range(value, min_val, max_val)
        if position is None:
            return 0.0, ScoreRange.CRITICAL

        has_status = map_position_to_status(position)
        score_range = self._has_to_score_range.get(has_status, ScoreRange.CRITICAL)
        curve = self._score_curve

        optimal_band = curve.get("optimal_band", {})
        normal_band = curve.get("normal_band", {})
        normal_low = curve.get("normal_low", {})
        normal_high = curve.get("normal_high", {})
        borderline_band = curve.get("borderline_band", {})
        borderline_low = curve.get("borderline_low", {})
        borderline_high = curve.get("borderline_high", {})
        low_noncritical = curve.get("low_noncritical", {})
        low_critical = curve.get("low_critical", {})
        high_noncritical = curve.get("high_noncritical", {})
        high_critical = curve.get("high_critical", {})

        if float(optimal_band.get("min", 0.2)) <= position <= float(optimal_band.get("max", 0.8)):
            score = float(optimal_band.get("score", 100.0))
        elif float(normal_band.get("min", 0.1)) <= position <= float(normal_band.get("max", 0.9)):
            if position < float(normal_low.get("end", 0.2)):
                score = float(normal_low.get("score_start", 90.0)) + (
                    (position - float(normal_low.get("start", 0.1)))
                    / (float(normal_low.get("end", 0.2)) - float(normal_low.get("start", 0.1)))
                    * (float(normal_low.get("score_end", 100.0)) - float(normal_low.get("score_start", 90.0)))
                )
            elif position > float(normal_high.get("start", 0.8)):
                score = float(normal_high.get("score_start", 100.0)) - (
                    (position - float(normal_high.get("start", 0.8)))
                    / (float(normal_high.get("end", 0.9)) - float(normal_high.get("start", 0.8)))
                    * (float(normal_high.get("score_start", 100.0)) - float(normal_high.get("score_end", 90.0)))
                )
            else:
                score = float(optimal_band.get("score", 100.0))
        elif float(borderline_band.get("min", 0.05)) <= position <= float(borderline_band.get("max", 0.95)):
            if position < float(borderline_low.get("end", 0.1)):
                score = float(borderline_low.get("score_start", 70.0)) + (
                    (position - float(borderline_low.get("start", 0.05)))
                    / (float(borderline_low.get("end", 0.1)) - float(borderline_low.get("start", 0.05)))
                    * (float(borderline_low.get("score_end", 90.0)) - float(borderline_low.get("score_start", 70.0)))
                )
            elif position > float(borderline_high.get("start", 0.9)):
                score = float(borderline_high.get("score_start", 90.0)) - (
                    (position - float(borderline_high.get("start", 0.9)))
                    / (float(borderline_high.get("end", 0.95)) - float(borderline_high.get("start", 0.9)))
                    * (float(borderline_high.get("score_start", 90.0)) - float(borderline_high.get("score_end", 70.0)))
                )
            else:
                score = float(borderline_low.get("score_end", 90.0))
        elif position < float(low_noncritical.get("end", 0.05)):
            if position < float(low_noncritical.get("start", 0.0)):
                excess_ratio = abs(position)
                score = max(
                    0.0,
                    float(low_critical.get("base_score", 10.0))
                    - excess_ratio * float(low_critical.get("excess_multiplier", 50.0)),
                )
            else:
                score = float(low_noncritical.get("score_start", 50.0)) + (
                    (position - float(low_noncritical.get("start", 0.0)))
                    / (float(low_noncritical.get("end", 0.05)) - float(low_noncritical.get("start", 0.0)))
                    * (float(low_noncritical.get("score_end", 70.0)) - float(low_noncritical.get("score_start", 50.0)))
                )
        else:
            if position > float(high_noncritical.get("end", 1.0)):
                excess_ratio = position - float(high_noncritical.get("end", 1.0))
                score = max(
                    0.0,
                    float(high_critical.get("base_score", 30.0))
                    - excess_ratio * float(high_critical.get("excess_multiplier", 50.0)),
                )
            else:
                score = float(high_noncritical.get("score_start", 70.0)) - (
                    (position - float(high_noncritical.get("start", 0.95)))
                    / (float(high_noncritical.get("end", 1.0)) - float(high_noncritical.get("start", 0.95)))
                    * (float(high_noncritical.get("score_start", 70.0)) - float(high_noncritical.get("score_end", 50.0)))
                )

        return score, score_range
    
    def _apply_adjustments(
        self,
        value: float,
        rule: BiomarkerRule,
        age: Optional[int],
        sex: Optional[str]
    ) -> float:
        # TODO: Age/sex adjustments defined but NOT applied in calculate_biomarker_score.
        # Single hook would be needed for consistency. See test_scoring_rules.py for coverage.
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
