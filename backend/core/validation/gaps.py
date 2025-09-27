"""
Gap analysis for missing biomarkers.

This module provides functionality to identify missing biomarkers,
analyze gaps in health system coverage, and provide detailed gap analysis.
"""

from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.validation.completeness import HealthSystem, DataCompletenessValidator
from core.canonical.normalize import BiomarkerNormalizer


class GapSeverity(Enum):
    """Severity levels for biomarker gaps."""
    CRITICAL = "critical"  # Missing critical biomarkers
    HIGH = "high"         # Missing important biomarkers
    MEDIUM = "medium"     # Missing optional biomarkers
    LOW = "low"          # Missing nice-to-have biomarkers


@dataclass
class BiomarkerGap:
    """Represents a gap in biomarker data."""
    biomarker_name: str
    health_system: HealthSystem
    severity: GapSeverity
    is_critical: bool
    is_optional: bool
    description: str
    impact: str


@dataclass
class HealthSystemGap:
    """Represents gaps in a health system."""
    health_system: HealthSystem
    completeness_score: float
    missing_biomarkers: List[BiomarkerGap]
    critical_gaps: List[BiomarkerGap]
    optional_gaps: List[BiomarkerGap]
    coverage_percentage: float
    analysis_ready: bool


@dataclass
class GapAnalysisResult:
    """Result of comprehensive gap analysis."""
    overall_gaps: List[BiomarkerGap]
    health_system_gaps: Dict[HealthSystem, HealthSystemGap]
    critical_gaps: List[BiomarkerGap]
    high_priority_gaps: List[BiomarkerGap]
    medium_priority_gaps: List[BiomarkerGap]
    low_priority_gaps: List[BiomarkerGap]
    total_missing: int
    critical_missing: int
    analysis_blockers: List[str]
    recommendations: List[str]
    analysis_ready: bool


class BiomarkerGapAnalyzer:
    """Analyzes gaps in biomarker data for comprehensive health assessment."""
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None):
        """
        Initialize the gap analyzer.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.completeness_validator = DataCompletenessValidator(normalizer)
    
    def analyze_gaps(self, biomarkers: Dict[str, Any]) -> GapAnalysisResult:
        """
        Perform comprehensive gap analysis on biomarker data.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            GapAnalysisResult with detailed gap analysis
        """
        # Normalize biomarkers to ensure canonical keys
        normalized_panel, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
        available_biomarkers = set(normalized_panel.biomarkers.keys())
        
        # Get completeness assessment
        completeness_result = self.completeness_validator.assess_completeness(biomarkers)
        
        # Identify all missing biomarkers
        all_missing = self._identify_all_missing_biomarkers(available_biomarkers)
        
        # Categorize gaps by severity
        critical_gaps, high_priority_gaps, medium_priority_gaps, low_priority_gaps = \
            self._categorize_gaps_by_severity(all_missing)
        
        # Analyze health system gaps
        health_system_gaps = self._analyze_health_system_gaps(
            available_biomarkers, completeness_result.health_system_scores
        )
        
        # Identify analysis blockers
        analysis_blockers = self._identify_analysis_blockers(critical_gaps, health_system_gaps)
        
        # Generate recommendations
        recommendations = self._generate_gap_recommendations(
            critical_gaps, high_priority_gaps, health_system_gaps
        )
        
        return GapAnalysisResult(
            overall_gaps=all_missing,
            health_system_gaps=health_system_gaps,
            critical_gaps=critical_gaps,
            high_priority_gaps=high_priority_gaps,
            medium_priority_gaps=medium_priority_gaps,
            low_priority_gaps=low_priority_gaps,
            total_missing=len(all_missing),
            critical_missing=len(critical_gaps),
            analysis_blockers=analysis_blockers,
            recommendations=recommendations,
            analysis_ready=len(analysis_blockers) == 0
        )
    
    def _identify_all_missing_biomarkers(self, available_biomarkers: Set[str]) -> List[BiomarkerGap]:
        """
        Identify all missing biomarkers with detailed gap information.
        
        Args:
            available_biomarkers: Set of available biomarker names
            
        Returns:
            List of BiomarkerGap objects for all missing biomarkers
        """
        missing_gaps = []
        
        # Get all possible biomarkers from completeness validator
        requirements = self.completeness_validator.get_health_system_requirements()
        
        for system, req in requirements.items():
            # Check critical biomarkers
            for biomarker in req["critical_biomarkers"]:
                if biomarker not in available_biomarkers:
                    gap = BiomarkerGap(
                        biomarker_name=biomarker,
                        health_system=system,
                        severity=GapSeverity.CRITICAL,
                        is_critical=True,
                        is_optional=False,
                        description=self._get_biomarker_description(biomarker),
                        impact=self._get_critical_impact(biomarker, system)
                    )
                    missing_gaps.append(gap)
            
            # Check optional biomarkers
            for biomarker in req["optional_biomarkers"]:
                if biomarker not in available_biomarkers:
                    gap = BiomarkerGap(
                        biomarker_name=biomarker,
                        health_system=system,
                        severity=GapSeverity.MEDIUM,
                        is_critical=False,
                        is_optional=True,
                        description=self._get_biomarker_description(biomarker),
                        impact=self._get_optional_impact(biomarker, system)
                    )
                    missing_gaps.append(gap)
        
        return missing_gaps
    
    def _categorize_gaps_by_severity(
        self, 
        gaps: List[BiomarkerGap]
    ) -> Tuple[List[BiomarkerGap], List[BiomarkerGap], List[BiomarkerGap], List[BiomarkerGap]]:
        """
        Categorize gaps by severity level.
        
        Args:
            gaps: List of all biomarker gaps
            
        Returns:
            Tuple of (critical, high, medium, low) priority gaps
        """
        critical = [gap for gap in gaps if gap.severity == GapSeverity.CRITICAL]
        high = [gap for gap in gaps if gap.severity == GapSeverity.HIGH]
        medium = [gap for gap in gaps if gap.severity == GapSeverity.MEDIUM]
        low = [gap for gap in gaps if gap.severity == GapSeverity.LOW]
        
        return critical, high, medium, low
    
    def _analyze_health_system_gaps(
        self,
        available_biomarkers: Set[str],
        health_system_scores: Dict[HealthSystem, float]
    ) -> Dict[HealthSystem, HealthSystemGap]:
        """
        Analyze gaps for each health system.
        
        Args:
            available_biomarkers: Set of available biomarker names
            health_system_scores: Health system completeness scores
            
        Returns:
            Dictionary mapping health systems to their gap analysis
        """
        health_system_gaps = {}
        requirements = self.completeness_validator.get_health_system_requirements()
        
        for system in HealthSystem:
            req = requirements[system]
            system_biomarkers = set(req["available_biomarkers"])
            available_in_system = available_biomarkers.intersection(system_biomarkers)
            
            # Get missing biomarkers for this system
            missing_biomarkers = []
            critical_gaps = []
            optional_gaps = []
            
            # Check critical biomarkers
            for biomarker in req["critical_biomarkers"]:
                if biomarker not in available_biomarkers:
                    gap = BiomarkerGap(
                        biomarker_name=biomarker,
                        health_system=system,
                        severity=GapSeverity.CRITICAL,
                        is_critical=True,
                        is_optional=False,
                        description=self._get_biomarker_description(biomarker),
                        impact=self._get_critical_impact(biomarker, system)
                    )
                    missing_biomarkers.append(gap)
                    critical_gaps.append(gap)
            
            # Check optional biomarkers
            for biomarker in req["optional_biomarkers"]:
                if biomarker not in available_biomarkers:
                    gap = BiomarkerGap(
                        biomarker_name=biomarker,
                        health_system=system,
                        severity=GapSeverity.MEDIUM,
                        is_critical=False,
                        is_optional=True,
                        description=self._get_biomarker_description(biomarker),
                        impact=self._get_optional_impact(biomarker, system)
                    )
                    missing_biomarkers.append(gap)
                    optional_gaps.append(gap)
            
            # Calculate coverage percentage
            total_biomarkers = len(system_biomarkers)
            coverage_percentage = (len(available_in_system) / total_biomarkers * 100) if total_biomarkers > 0 else 0
            
            # Determine if analysis is ready
            analysis_ready = len(critical_gaps) == 0 and coverage_percentage >= 50
            
            health_system_gaps[system] = HealthSystemGap(
                health_system=system,
                completeness_score=health_system_scores.get(system, 0.0),
                missing_biomarkers=missing_biomarkers,
                critical_gaps=critical_gaps,
                optional_gaps=optional_gaps,
                coverage_percentage=coverage_percentage,
                analysis_ready=analysis_ready
            )
        
        return health_system_gaps
    
    def _identify_analysis_blockers(
        self,
        critical_gaps: List[BiomarkerGap],
        health_system_gaps: Dict[HealthSystem, HealthSystemGap]
    ) -> List[str]:
        """
        Identify what's blocking analysis from proceeding.
        
        Args:
            critical_gaps: List of critical biomarker gaps
            health_system_gaps: Health system gap analysis
            
        Returns:
            List of analysis blocker descriptions
        """
        blockers = []
        
        # Critical biomarker blockers
        if critical_gaps:
            critical_biomarkers = [gap.biomarker_name for gap in critical_gaps]
            blockers.append(f"Missing critical biomarkers: {', '.join(critical_biomarkers[:3])}")
        
        # Health system coverage blockers - only for systems with actual biomarkers
        systems_not_ready = [
            system.value for system, gap in health_system_gaps.items()
            if not gap.analysis_ready and gap.coverage_percentage > 0  # Only systems with some data
        ]
        
        if systems_not_ready:
            blockers.append(f"Health systems not ready: {', '.join(systems_not_ready[:2])}")
        
        # Minimum coverage blockers - only for systems with actual biomarkers
        systems_with_low_coverage = [
            system.value for system, gap in health_system_gaps.items()
            if gap.coverage_percentage < 30 and gap.coverage_percentage > 0  # Only systems with some data
        ]
        
        if systems_with_low_coverage:
            blockers.append(f"Very low coverage: {', '.join(systems_with_low_coverage[:2])}")
        
        return blockers
    
    def _generate_gap_recommendations(
        self,
        critical_gaps: List[BiomarkerGap],
        high_priority_gaps: List[BiomarkerGap],
        health_system_gaps: Dict[HealthSystem, HealthSystemGap]
    ) -> List[str]:
        """
        Generate recommendations for addressing gaps.
        
        Args:
            critical_gaps: List of critical gaps
            high_priority_gaps: List of high priority gaps
            health_system_gaps: Health system gap analysis
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Critical gap recommendations
        if critical_gaps:
            critical_biomarkers = [gap.biomarker_name for gap in critical_gaps[:3]]
            recommendations.append(
                f"Priority 1: Add critical biomarkers - {', '.join(critical_biomarkers)}"
            )
        
        # High priority gap recommendations
        if high_priority_gaps:
            high_biomarkers = [gap.biomarker_name for gap in high_priority_gaps[:3]]
            recommendations.append(
                f"Priority 2: Add important biomarkers - {', '.join(high_biomarkers)}"
            )
        
        # Health system improvement recommendations
        systems_needing_improvement = [
            (system.value, gap.coverage_percentage)
            for system, gap in health_system_gaps.items()
            if gap.coverage_percentage < 70
        ]
        
        if systems_needing_improvement:
            top_system = systems_needing_improvement[0]
            recommendations.append(
                f"Improve {top_system[0]} coverage (currently {top_system[1]:.1f}%)"
            )
        
        # General recommendations
        if not recommendations:
            recommendations.append("Biomarker coverage is good for comprehensive analysis")
        
        return recommendations
    
    def _get_biomarker_description(self, biomarker_name: str) -> str:
        """
        Get human-readable description for a biomarker.
        
        Args:
            biomarker_name: Name of the biomarker
            
        Returns:
            Description string
        """
        descriptions = {
            "glucose": "Blood glucose level - essential for metabolic health assessment",
            "hba1c": "Hemoglobin A1c - long-term blood sugar control indicator",
            "insulin": "Fasting insulin - insulin resistance marker",
            "total_cholesterol": "Total cholesterol - cardiovascular risk assessment",
            "ldl_cholesterol": "LDL cholesterol - 'bad' cholesterol level",
            "hdl_cholesterol": "HDL cholesterol - 'good' cholesterol level",
            "triglycerides": "Triglycerides - blood fat levels",
            "crp": "C-reactive protein - inflammation marker",
            "creatinine": "Serum creatinine - kidney function marker",
            "bun": "Blood urea nitrogen - kidney function marker",
            "alt": "Alanine aminotransferase - liver function marker",
            "ast": "Aspartate aminotransferase - liver function marker",
            "hemoglobin": "Hemoglobin - oxygen-carrying capacity",
            "hematocrit": "Hematocrit - blood volume percentage",
            "white_blood_cells": "White blood cell count - immune system marker",
            "platelets": "Platelet count - blood clotting marker"
        }
        
        return descriptions.get(biomarker_name, f"{biomarker_name} - biomarker for health assessment")
    
    def _get_critical_impact(self, biomarker_name: str, health_system: HealthSystem) -> str:
        """
        Get impact description for critical biomarker gaps.
        
        Args:
            biomarker_name: Name of the biomarker
            health_system: Health system the biomarker belongs to
            
        Returns:
            Impact description string
        """
        impacts = {
            "glucose": "Cannot assess metabolic health or diabetes risk",
            "hba1c": "Cannot assess long-term blood sugar control",
            "total_cholesterol": "Cannot assess cardiovascular risk",
            "ldl_cholesterol": "Cannot assess 'bad' cholesterol levels",
            "crp": "Cannot assess inflammation status",
            "creatinine": "Cannot assess kidney function",
            "alt": "Cannot assess liver function",
            "hemoglobin": "Cannot assess oxygen-carrying capacity"
        }
        
        return impacts.get(biomarker_name, f"Cannot assess {health_system.value} health")
    
    def _get_optional_impact(self, biomarker_name: str, health_system: HealthSystem) -> str:
        """
        Get impact description for optional biomarker gaps.
        
        Args:
            biomarker_name: Name of the biomarker
            health_system: Health system the biomarker belongs to
            
        Returns:
            Impact description string
        """
        impacts = {
            "insulin": "Limited insulin resistance assessment",
            "hdl_cholesterol": "Limited cardiovascular risk assessment",
            "triglycerides": "Limited blood fat assessment",
            "bun": "Limited kidney function assessment",
            "ast": "Limited liver function assessment",
            "hematocrit": "Limited blood volume assessment",
            "white_blood_cells": "Limited immune system assessment",
            "platelets": "Limited blood clotting assessment"
        }
        
        return impacts.get(biomarker_name, f"Limited {health_system.value} health assessment")
    
    def get_gap_summary(self, gap_analysis: GapAnalysisResult) -> Dict[str, Any]:
        """
        Get a summary of gap analysis results.
        
        Args:
            gap_analysis: Gap analysis result
            
        Returns:
            Dictionary with gap summary
        """
        return {
            "total_gaps": gap_analysis.total_missing,
            "critical_gaps": gap_analysis.critical_missing,
            "analysis_ready": len(gap_analysis.analysis_blockers) == 0,
            "health_systems_ready": sum(
                1 for gap in gap_analysis.health_system_gaps.values()
                if gap.analysis_ready
            ),
            "health_systems_total": len(gap_analysis.health_system_gaps),
            "top_priorities": [
                gap.biomarker_name for gap in gap_analysis.critical_gaps[:3]
            ],
            "recommendations_count": len(gap_analysis.recommendations)
        }
