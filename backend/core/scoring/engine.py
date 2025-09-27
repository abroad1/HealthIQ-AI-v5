"""
Master scoring engine for biomarker analysis.

This module provides the main scoring orchestration, integrating all health system
engines and producing comprehensive biomarker scores with confidence levels.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.scoring.rules import ScoringRules, ScoreRange
from core.scoring.overlays import LifestyleOverlays, LifestyleProfile
from core.canonical.normalize import BiomarkerNormalizer
from core.validation.completeness import DataCompletenessValidator


class ConfidenceLevel(Enum):
    """Confidence levels for scoring results."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class BiomarkerScore:
    """Score for a single biomarker."""
    biomarker_name: str
    value: float
    score: float  # 0-100
    score_range: ScoreRange
    confidence: ConfidenceLevel
    missing: bool = False


@dataclass
class HealthSystemScore:
    """Score for a health system."""
    system_name: str
    overall_score: float  # 0-100
    confidence: ConfidenceLevel
    biomarker_scores: List[BiomarkerScore]
    missing_biomarkers: List[str]
    recommendations: List[str]


@dataclass
class ScoringResult:
    """Complete scoring result for all health systems."""
    overall_score: float  # 0-100
    confidence: ConfidenceLevel
    health_system_scores: Dict[str, HealthSystemScore]
    missing_biomarkers: List[str]
    recommendations: List[str]
    lifestyle_adjustments: List[str]


class ScoringEngine:
    """Master scoring engine for biomarker analysis."""
    
    def __init__(
        self, 
        normalizer: Optional[BiomarkerNormalizer] = None,
        rules: Optional[ScoringRules] = None,
        overlays: Optional[LifestyleOverlays] = None
    ):
        """
        Initialize the scoring engine.
        
        Args:
            normalizer: BiomarkerNormalizer instance
            rules: ScoringRules instance
            overlays: LifestyleOverlays instance
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.rules = rules or ScoringRules()
        self.overlays = overlays or LifestyleOverlays()
        self.completeness_validator = DataCompletenessValidator(normalizer)
    
    def score_biomarkers(
        self,
        biomarkers: Dict[str, Any],
        age: Optional[int] = None,
        sex: Optional[str] = None,
        lifestyle_profile: Optional[LifestyleProfile] = None
    ) -> ScoringResult:
        """
        Score biomarkers across all health systems.
        
        Args:
            biomarkers: Dictionary of biomarker data
            age: Patient age for adjustments
            sex: Patient sex for adjustments
            lifestyle_profile: Lifestyle profile for overlays
            
        Returns:
            Complete scoring result
        """
        # Handle both raw biomarkers (dict) and normalized biomarkers (BiomarkerPanel)
        if isinstance(biomarkers, dict):
            # Raw biomarkers - normalize them
            normalized_panel, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
            canonical_biomarkers = normalized_panel.biomarkers
        else:
            # Already normalized biomarkers (BiomarkerPanel)
            canonical_biomarkers = biomarkers.biomarkers
        
        # Get completeness assessment
        if isinstance(biomarkers, dict):
            completeness_result = self.completeness_validator.assess_completeness(biomarkers)
        else:
            # For BiomarkerPanel, convert to dict format for completeness assessment
            biomarker_dict = {name: value.value for name, value in biomarkers.biomarkers.items()}
            completeness_result = self.completeness_validator.assess_completeness(biomarker_dict)
        
        # Score each health system
        health_system_scores = {}
        all_missing_biomarkers = []
        all_recommendations = []
        
        for system_name in ["metabolic", "cardiovascular", "inflammatory", "hormonal", "nutritional", "kidney", "liver", "cbc"]:
            system_score = self._score_health_system(
                system_name, 
                canonical_biomarkers, 
                age, 
                sex, 
                lifestyle_profile
            )
            health_system_scores[system_name] = system_score
            all_missing_biomarkers.extend(system_score.missing_biomarkers)
            all_recommendations.extend(system_score.recommendations)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(health_system_scores)
        
        # Determine overall confidence
        confidence = self._determine_overall_confidence(health_system_scores, completeness_result)
        
        # Apply lifestyle overlays if provided
        lifestyle_adjustments = []
        if lifestyle_profile:
            adjusted_score, adjustments = self.overlays.apply_lifestyle_overlays(overall_score, lifestyle_profile)
            overall_score = adjusted_score
            lifestyle_adjustments = adjustments
        
        return ScoringResult(
            overall_score=overall_score,
            confidence=confidence,
            health_system_scores=health_system_scores,
            missing_biomarkers=list(set(all_missing_biomarkers)),
            recommendations=list(set(all_recommendations)),
            lifestyle_adjustments=lifestyle_adjustments
        )
    
    def _score_health_system(
        self,
        system_name: str,
        biomarkers: Dict[str, float],
        age: Optional[int],
        sex: Optional[str],
        lifestyle_profile: Optional[LifestyleProfile]
    ) -> HealthSystemScore:
        """Score a specific health system."""
        system_rules = self.rules.get_health_system_rules(system_name)
        if not system_rules:
            return HealthSystemScore(
                system_name=system_name,
                overall_score=0.0,
                confidence=ConfidenceLevel.LOW,
                biomarker_scores=[],
                missing_biomarkers=[],
                recommendations=["Health system not implemented"]
            )
        
        biomarker_scores = []
        missing_biomarkers = []
        total_weighted_score = 0.0
        total_weight = 0.0
        
        # Score each biomarker in the system
        for rule in system_rules.biomarkers:
            if rule.biomarker_name in biomarkers:
                biomarker_value = biomarkers[rule.biomarker_name]
                # Extract numeric value from BiomarkerValue object
                if hasattr(biomarker_value, 'value'):
                    value = biomarker_value.value
                else:
                    value = biomarker_value
                score, score_range = self.rules.calculate_biomarker_score(
                    rule.biomarker_name, value, age, sex
                )
                
                # Apply lifestyle overlays if provided
                if lifestyle_profile:
                    adjusted_score, _ = self.overlays.apply_lifestyle_overlays(score, lifestyle_profile)
                    score = adjusted_score
                
                biomarker_score = BiomarkerScore(
                    biomarker_name=rule.biomarker_name,
                    value=value,
                    score=score,
                    score_range=score_range,
                    confidence=self._determine_biomarker_confidence(score, score_range)
                )
                biomarker_scores.append(biomarker_score)
                
                # Add to weighted total
                total_weighted_score += score * rule.weight
                total_weight += rule.weight
            else:
                missing_biomarkers.append(rule.biomarker_name)
        
        # Calculate overall system score
        if total_weight > 0:
            overall_score = total_weighted_score / total_weight
        else:
            overall_score = 0.0
        
        # Determine system confidence
        confidence = self._determine_system_confidence(
            biomarker_scores, missing_biomarkers, system_rules
        )
        
        # Generate recommendations
        recommendations = self._generate_system_recommendations(
            system_name, biomarker_scores, missing_biomarkers, overall_score
        )
        
        return HealthSystemScore(
            system_name=system_name,
            overall_score=overall_score,
            confidence=confidence,
            biomarker_scores=biomarker_scores,
            missing_biomarkers=missing_biomarkers,
            recommendations=recommendations
        )
    
    def _calculate_overall_score(self, health_system_scores: Dict[str, HealthSystemScore]) -> float:
        """Calculate overall score from health system scores."""
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for system_name, system_score in health_system_scores.items():
            system_rules = self.rules.get_health_system_rules(system_name)
            if system_rules and system_score.overall_score > 0:
                total_weighted_score += system_score.overall_score * system_rules.system_weight
                total_weight += system_rules.system_weight
        
        if total_weight > 0:
            return total_weighted_score / total_weight
        else:
            return 0.0
    
    def _determine_overall_confidence(
        self, 
        health_system_scores: Dict[str, HealthSystemScore],
        completeness_result: Any
    ) -> ConfidenceLevel:
        """Determine overall confidence level."""
        # Count systems with high confidence
        high_confidence_systems = sum(
            1 for score in health_system_scores.values() 
            if score.confidence == ConfidenceLevel.HIGH
        )
        total_systems = len(health_system_scores)
        
        # Base confidence on completeness and system confidence
        if completeness_result.analysis_ready and high_confidence_systems >= total_systems * 0.7:
            return ConfidenceLevel.HIGH
        elif completeness_result.overall_score >= 60 and high_confidence_systems >= total_systems * 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _determine_biomarker_confidence(self, score: float, score_range: ScoreRange) -> ConfidenceLevel:
        """Determine confidence level for a single biomarker."""
        if score_range in [ScoreRange.OPTIMAL, ScoreRange.NORMAL]:
            return ConfidenceLevel.HIGH
        elif score_range in [ScoreRange.BORDERLINE, ScoreRange.HIGH]:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _determine_system_confidence(
        self,
        biomarker_scores: List[BiomarkerScore],
        missing_biomarkers: List[str],
        system_rules: Any
    ) -> ConfidenceLevel:
        """Determine confidence level for a health system."""
        if not biomarker_scores:
            return ConfidenceLevel.LOW
        
        # Check if minimum biomarkers are present
        if len(biomarker_scores) < system_rules.min_biomarkers_required:
            return ConfidenceLevel.LOW
        
        # Check biomarker confidence levels
        high_confidence_count = sum(
            1 for score in biomarker_scores 
            if score.confidence == ConfidenceLevel.HIGH
        )
        
        if high_confidence_count >= len(biomarker_scores) * 0.8:
            return ConfidenceLevel.HIGH
        elif high_confidence_count >= len(biomarker_scores) * 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _generate_system_recommendations(
        self,
        system_name: str,
        biomarker_scores: List[BiomarkerScore],
        missing_biomarkers: List[str],
        overall_score: float
    ) -> List[str]:
        """Generate recommendations for a health system."""
        recommendations = []
        
        # Missing biomarker recommendations
        if missing_biomarkers:
            recommendations.append(
                f"Add missing {system_name} biomarkers: {', '.join(missing_biomarkers[:3])}"
            )
        
        # Score-based recommendations
        if overall_score < 50:
            recommendations.append(f"{system_name.title()} health needs immediate attention")
        elif overall_score < 70:
            recommendations.append(f"{system_name.title()} health could be improved")
        elif overall_score >= 90:
            recommendations.append(f"{system_name.title()} health is excellent")
        
        # Specific biomarker recommendations
        for score in biomarker_scores:
            if score.score < 50:
                recommendations.append(
                    f"Address {score.biomarker_name} levels (current: {score.value})"
                )
        
        return recommendations
    
    def get_scoring_summary(self, result: ScoringResult) -> Dict[str, Any]:
        """
        Get a summary of scoring results.
        
        Args:
            result: Scoring result
            
        Returns:
            Dictionary with scoring summary
        """
        return {
            "overall_score": result.overall_score,
            "confidence": result.confidence.value,
            "health_systems_scored": len(result.health_system_scores),
            "missing_biomarkers_count": len(result.missing_biomarkers),
            "recommendations_count": len(result.recommendations),
            "lifestyle_adjustments_applied": len(result.lifestyle_adjustments) > 0,
            "top_health_systems": [
                {
                    "name": name,
                    "score": score.overall_score,
                    "confidence": score.confidence.value
                }
                for name, score in sorted(
                    result.health_system_scores.items(),
                    key=lambda x: x[1].overall_score,
                    reverse=True
                )[:3]
            ]
        }
