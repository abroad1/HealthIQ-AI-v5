"""
Data completeness validation for biomarker analysis.

This module provides functionality to assess data sufficiency for biomarker analysis,
including completeness scoring, health system coverage, and confidence assessment.
"""

from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.canonical.normalize import BiomarkerNormalizer


class HealthSystem(Enum):
    """Health system categories for biomarker analysis."""
    METABOLIC = "metabolic"
    CARDIOVASCULAR = "cardiovascular"
    INFLAMMATORY = "inflammatory"
    HORMONAL = "hormone"
    NUTRITIONAL = "vitamin"
    KIDNEY = "kidney"
    LIVER = "liver"
    CBC = "cbc"


@dataclass
class CompletenessResult:
    """Result of completeness assessment."""
    overall_score: float  # 0-100
    health_system_scores: Dict[HealthSystem, float]
    missing_critical: List[str]
    missing_optional: List[str]
    confidence_level: str  # "high", "medium", "low"
    analysis_ready: bool
    recommendations: List[str]


class DataCompletenessValidator:
    """Validates data completeness for biomarker analysis."""
    
    # Minimum biomarkers required per health system for analysis
    MIN_BIOMARKERS_PER_SYSTEM = {
        HealthSystem.METABOLIC: 3,      # glucose, hba1c, insulin
        HealthSystem.CARDIOVASCULAR: 3,  # total_cholesterol, ldl_cholesterol, hdl_cholesterol
        HealthSystem.INFLAMMATORY: 1,    # crp
        HealthSystem.HORMONAL: 2,        # Basic hormone markers
        HealthSystem.NUTRITIONAL: 2,     # Basic vitamin markers
        HealthSystem.KIDNEY: 2,          # creatinine, bun
        HealthSystem.LIVER: 2,           # alt, ast
        HealthSystem.CBC: 2              # hemoglobin, hematocrit
    }
    
    # Critical biomarkers that must be present for meaningful analysis
    CRITICAL_BIOMARKERS = {
        HealthSystem.METABOLIC: ["glucose", "hba1c"],
        HealthSystem.CARDIOVASCULAR: ["total_cholesterol", "ldl_cholesterol"],
        HealthSystem.INFLAMMATORY: ["crp"],
        HealthSystem.HORMONAL: [],  # No critical biomarkers defined yet
        HealthSystem.NUTRITIONAL: [],  # No critical biomarkers defined yet
        HealthSystem.KIDNEY: ["creatinine"],
        HealthSystem.LIVER: ["alt"],
        HealthSystem.CBC: ["hemoglobin"]
    }
    
    # Optional biomarkers that enhance analysis quality
    OPTIONAL_BIOMARKERS = {
        HealthSystem.METABOLIC: ["insulin"],
        HealthSystem.CARDIOVASCULAR: ["hdl_cholesterol", "triglycerides"],
        HealthSystem.INFLAMMATORY: [],
        HealthSystem.HORMONAL: [],
        HealthSystem.NUTRITIONAL: [],
        HealthSystem.KIDNEY: ["bun"],
        HealthSystem.LIVER: ["ast"],
        HealthSystem.CBC: ["hematocrit", "white_blood_cells", "platelets"]
    }
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None):
        """
        Initialize the completeness validator.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self._biomarker_categories = self._load_biomarker_categories()
    
    def _load_biomarker_categories(self) -> Dict[str, HealthSystem]:
        """
        Load biomarker categories from SSOT data.
        
        Returns:
            Dictionary mapping biomarker names to health systems
        """
        categories = {}
        canonical_biomarkers = self.normalizer.get_canonical_biomarkers()
        
        # Map biomarker categories to health systems
        category_mapping = {
            "metabolic": HealthSystem.METABOLIC,
            "cardiovascular": HealthSystem.CARDIOVASCULAR,
            "inflammatory": HealthSystem.INFLAMMATORY,
            "hormone": HealthSystem.HORMONAL,
            "vitamin": HealthSystem.NUTRITIONAL,
            "kidney": HealthSystem.KIDNEY,
            "liver": HealthSystem.LIVER,
            "cbc": HealthSystem.CBC
        }
        
        # Load biomarker definitions to get categories
        try:
            from core.validation.ssot.validator import SSOTValidator
            validator = SSOTValidator()
            # This would need to be implemented to load from SSOT files
            # For now, we'll use the hardcoded mapping from biomarkers.yaml
            pass
        except ImportError:
            pass
        
        # Hardcoded mapping based on biomarkers.yaml structure
        # In production, this would be loaded from SSOT data
        biomarker_system_mapping = {
            # Metabolic
            "glucose": HealthSystem.METABOLIC,
            "hba1c": HealthSystem.METABOLIC,
            "insulin": HealthSystem.METABOLIC,
            
            # Cardiovascular
            "total_cholesterol": HealthSystem.CARDIOVASCULAR,
            "ldl_cholesterol": HealthSystem.CARDIOVASCULAR,
            "hdl_cholesterol": HealthSystem.CARDIOVASCULAR,
            "triglycerides": HealthSystem.CARDIOVASCULAR,
            
            # Inflammatory
            "crp": HealthSystem.INFLAMMATORY,
            
            # Kidney
            "creatinine": HealthSystem.KIDNEY,
            "bun": HealthSystem.KIDNEY,
            
            # Liver
            "alt": HealthSystem.LIVER,
            "ast": HealthSystem.LIVER,
            
            # CBC
            "hemoglobin": HealthSystem.CBC,
            "hematocrit": HealthSystem.CBC,
            "white_blood_cells": HealthSystem.CBC,
            "platelets": HealthSystem.CBC
        }
        
        return biomarker_system_mapping
    
    def assess_completeness(self, biomarkers: Dict[str, Any]) -> CompletenessResult:
        """
        Assess completeness of biomarker data for analysis.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            CompletenessResult with scoring and recommendations
        """
        # Normalize biomarkers to ensure canonical keys
        normalized_panel, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
        canonical_biomarkers = set(normalized_panel.biomarkers.keys())
        
        # Calculate health system scores
        health_system_scores = self._calculate_health_system_scores(canonical_biomarkers)
        
        # Identify missing biomarkers
        missing_critical, missing_optional = self._identify_missing_biomarkers(canonical_biomarkers)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(health_system_scores)
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(overall_score, missing_critical)
        
        # Check if analysis is ready
        analysis_ready = self._is_analysis_ready(health_system_scores, missing_critical)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            health_system_scores, missing_critical, missing_optional
        )
        
        return CompletenessResult(
            overall_score=overall_score,
            health_system_scores=health_system_scores,
            missing_critical=missing_critical,
            missing_optional=missing_optional,
            confidence_level=confidence_level,
            analysis_ready=analysis_ready,
            recommendations=recommendations
        )
    
    def _calculate_health_system_scores(self, biomarkers: Set[str]) -> Dict[HealthSystem, float]:
        """
        Calculate completeness scores for each health system.
        
        Args:
            biomarkers: Set of available biomarker names
            
        Returns:
            Dictionary mapping health systems to completeness scores (0-100)
        """
        scores = {}
        
        for system in HealthSystem:
            # Get biomarkers for this system
            system_biomarkers = {
                name for name, sys in self._biomarker_categories.items() 
                if sys == system
            }
            
            if not system_biomarkers:
                scores[system] = 0.0
                continue
            
            # Count available biomarkers
            available = len(biomarkers.intersection(system_biomarkers))
            total = len(system_biomarkers)
            
            # Calculate score (0-100)
            if total == 0:
                scores[system] = 0.0
            else:
                scores[system] = (available / total) * 100
        
        return scores
    
    def _identify_missing_biomarkers(
        self, 
        available_biomarkers: Set[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Identify missing critical and optional biomarkers.
        
        Args:
            available_biomarkers: Set of available biomarker names
            
        Returns:
            Tuple of (missing_critical, missing_optional) biomarker lists
        """
        missing_critical = []
        missing_optional = []
        
        for system in HealthSystem:
            # Check critical biomarkers
            critical = self.CRITICAL_BIOMARKERS.get(system, [])
            for biomarker in critical:
                if biomarker not in available_biomarkers:
                    missing_critical.append(biomarker)
            
            # Check optional biomarkers
            optional = self.OPTIONAL_BIOMARKERS.get(system, [])
            for biomarker in optional:
                if biomarker not in available_biomarkers:
                    missing_optional.append(biomarker)
        
        return missing_critical, missing_optional
    
    def _calculate_overall_score(self, health_system_scores: Dict[HealthSystem, float]) -> float:
        """
        Calculate overall completeness score.
        
        Args:
            health_system_scores: Health system scores
            
        Returns:
            Overall score (0-100)
        """
        if not health_system_scores:
            return 0.0
        
        # Weight health systems by clinical importance
        weights = {
            HealthSystem.METABOLIC: 0.25,
            HealthSystem.CARDIOVASCULAR: 0.25,
            HealthSystem.INFLAMMATORY: 0.15,
            HealthSystem.KIDNEY: 0.15,
            HealthSystem.LIVER: 0.10,
            HealthSystem.CBC: 0.10,
            HealthSystem.HORMONAL: 0.0,  # Not yet implemented
            HealthSystem.NUTRITIONAL: 0.0  # Not yet implemented
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for system, score in health_system_scores.items():
            weight = weights.get(system, 0.0)
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    def _determine_confidence_level(self, overall_score: float, missing_critical: List[str]) -> str:
        """
        Determine confidence level based on score and missing critical biomarkers.
        
        Args:
            overall_score: Overall completeness score
            missing_critical: List of missing critical biomarkers
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if missing_critical:
            return "low"
        elif overall_score >= 80:
            return "high"
        elif overall_score >= 60:
            return "medium"
        else:
            return "low"
    
    def _is_analysis_ready(self, health_system_scores: Dict[HealthSystem, float], missing_critical: List[str]) -> bool:
        """
        Determine if analysis is ready based on completeness.
        
        Args:
            health_system_scores: Health system scores
            missing_critical: List of missing critical biomarkers
            
        Returns:
            True if analysis is ready, False otherwise
        """
        # Analysis is not ready if critical biomarkers are missing
        if missing_critical:
            return False
        
        # Check if at least 2 health systems have minimum coverage
        systems_with_coverage = 0
        for system, score in health_system_scores.items():
            if score >= 50:  # At least 50% coverage
                systems_with_coverage += 1
        
        return systems_with_coverage >= 2
    
    def _generate_recommendations(
        self,
        health_system_scores: Dict[HealthSystem, float],
        missing_critical: List[str],
        missing_optional: List[str]
    ) -> List[str]:
        """
        Generate recommendations for improving data completeness.
        
        Args:
            health_system_scores: Health system scores
            missing_critical: List of missing critical biomarkers
            missing_optional: List of missing optional biomarkers
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Critical biomarker recommendations
        if missing_critical:
            recommendations.append(
                f"Add critical biomarkers: {', '.join(missing_critical[:3])}"
            )
        
        # Health system coverage recommendations
        low_coverage_systems = [
            system.value for system, score in health_system_scores.items()
            if score < 50
        ]
        
        if low_coverage_systems:
            recommendations.append(
                f"Improve coverage for: {', '.join(low_coverage_systems[:2])}"
            )
        
        # Optional biomarker recommendations
        if missing_optional and len(missing_optional) <= 5:
            recommendations.append(
                f"Consider adding: {', '.join(missing_optional[:3])}"
            )
        
        # General recommendations
        if not recommendations:
            recommendations.append("Data completeness is good for analysis")
        
        return recommendations
    
    def get_health_system_requirements(self) -> Dict[HealthSystem, Dict[str, Any]]:
        """
        Get requirements for each health system.
        
        Returns:
            Dictionary with health system requirements
        """
        requirements = {}
        
        for system in HealthSystem:
            requirements[system] = {
                "min_biomarkers": self.MIN_BIOMARKERS_PER_SYSTEM.get(system, 0),
                "critical_biomarkers": self.CRITICAL_BIOMARKERS.get(system, []),
                "optional_biomarkers": self.OPTIONAL_BIOMARKERS.get(system, []),
                "available_biomarkers": [
                    name for name, sys in self._biomarker_categories.items()
                    if sys == system
                ]
            }
        
        return requirements
