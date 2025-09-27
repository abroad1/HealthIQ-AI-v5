"""
User guidance and recommendations for incomplete biomarker data.

This module provides functionality to generate actionable recommendations
for users with incomplete biomarker data, including guidance on what to add
and how to improve analysis quality.
"""

from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.validation.completeness import HealthSystem, CompletenessResult, DataCompletenessValidator
from core.validation.gaps import GapAnalysisResult, BiomarkerGapAnalyzer, GapSeverity
from core.canonical.normalize import BiomarkerNormalizer


class RecommendationPriority(Enum):
    """Priority levels for recommendations."""
    CRITICAL = "critical"    # Must address for analysis
    HIGH = "high"           # Should address for better analysis
    MEDIUM = "medium"       # Nice to have for comprehensive analysis
    LOW = "low"            # Optional enhancement


class RecommendationCategory(Enum):
    """Categories of recommendations."""
    BIOMARKER_ADDITION = "biomarker_addition"
    HEALTH_SYSTEM_IMPROVEMENT = "health_system_improvement"
    ANALYSIS_READINESS = "analysis_readiness"
    DATA_QUALITY = "data_quality"
    GENERAL_GUIDANCE = "general_guidance"


@dataclass
class Recommendation:
    """Represents a single recommendation for improving biomarker data."""
    title: str
    description: str
    priority: RecommendationPriority
    category: RecommendationCategory
    action_items: List[str]
    expected_impact: str
    effort_level: str  # "low", "medium", "high"
    biomarkers_involved: List[str]
    health_systems_affected: List[HealthSystem]


@dataclass
class RecommendationSet:
    """Complete set of recommendations for a user."""
    recommendations: List[Recommendation]
    critical_recommendations: List[Recommendation]
    high_priority_recommendations: List[Recommendation]
    medium_priority_recommendations: List[Recommendation]
    low_priority_recommendations: List[Recommendation]
    summary: str
    next_steps: List[str]
    analysis_readiness: bool
    estimated_improvement: str


class RecommendationEngine:
    """Generates actionable recommendations for improving biomarker data completeness."""
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None):
        """
        Initialize the recommendation engine.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.completeness_validator = DataCompletenessValidator(normalizer)
        self.gap_analyzer = BiomarkerGapAnalyzer(normalizer)
    
    def generate_recommendations(self, biomarkers: Dict[str, Any]) -> RecommendationSet:
        """
        Generate comprehensive recommendations for improving biomarker data.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            RecommendationSet with actionable recommendations
        """
        # Get completeness and gap analysis
        completeness_result = self.completeness_validator.assess_completeness(biomarkers)
        gap_analysis = self.gap_analyzer.analyze_gaps(biomarkers)
        
        # Generate recommendations based on analysis
        recommendations = []
        
        # Critical biomarker recommendations
        recommendations.extend(
            self._generate_critical_biomarker_recommendations(gap_analysis.critical_gaps)
        )
        
        # Health system improvement recommendations
        recommendations.extend(
            self._generate_health_system_recommendations(gap_analysis.health_system_gaps)
        )
        
        # High priority biomarker recommendations
        recommendations.extend(
            self._generate_high_priority_recommendations(gap_analysis.high_priority_gaps)
        )
        
        # Medium priority recommendations
        recommendations.extend(
            self._generate_medium_priority_recommendations(gap_analysis.medium_priority_gaps)
        )
        
        # Analysis readiness recommendations
        recommendations.extend(
            self._generate_analysis_readiness_recommendations(completeness_result, gap_analysis)
        )
        
        # General guidance recommendations
        recommendations.extend(
            self._generate_general_guidance_recommendations(completeness_result)
        )
        
        # Categorize recommendations by priority
        critical_recs = [r for r in recommendations if r.priority == RecommendationPriority.CRITICAL]
        high_recs = [r for r in recommendations if r.priority == RecommendationPriority.HIGH]
        medium_recs = [r for r in recommendations if r.priority == RecommendationPriority.MEDIUM]
        low_recs = [r for r in recommendations if r.priority == RecommendationPriority.LOW]
        
        # Generate summary and next steps
        summary = self._generate_summary(completeness_result, gap_analysis)
        next_steps = self._generate_next_steps(critical_recs, high_recs)
        analysis_readiness = completeness_result.analysis_ready
        estimated_improvement = self._estimate_improvement(completeness_result, gap_analysis)
        
        return RecommendationSet(
            recommendations=recommendations,
            critical_recommendations=critical_recs,
            high_priority_recommendations=high_recs,
            medium_priority_recommendations=medium_recs,
            low_priority_recommendations=low_recs,
            summary=summary,
            next_steps=next_steps,
            analysis_readiness=analysis_readiness,
            estimated_improvement=estimated_improvement
        )
    
    def _generate_critical_biomarker_recommendations(
        self, 
        critical_gaps: List
    ) -> List[Recommendation]:
        """Generate recommendations for critical biomarker gaps."""
        recommendations = []
        
        if not critical_gaps:
            return recommendations
        
        # Group critical gaps by health system
        gaps_by_system = {}
        for gap in critical_gaps:
            system = gap.health_system
            if system not in gaps_by_system:
                gaps_by_system[system] = []
            gaps_by_system[system].append(gap)
        
        # Create recommendations for each health system with critical gaps
        for system, gaps in gaps_by_system.items():
            biomarker_names = [gap.biomarker_name for gap in gaps]
            
            recommendation = Recommendation(
                title=f"Add Critical {system.value.title()} Biomarkers",
                description=f"Missing critical biomarkers for {system.value} health assessment: {', '.join(biomarker_names)}",
                priority=RecommendationPriority.CRITICAL,
                category=RecommendationCategory.BIOMARKER_ADDITION,
                action_items=[
                    f"Add {biomarker_names[0]} for basic {system.value} assessment",
                    f"Consider adding {', '.join(biomarker_names[1:3])} for comprehensive analysis"
                ],
                expected_impact=f"Enables {system.value} health analysis and improves overall assessment quality",
                effort_level="medium",
                biomarkers_involved=biomarker_names,
                health_systems_affected=[system]
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_health_system_recommendations(
        self, 
        health_system_gaps: Dict[HealthSystem, Any]
    ) -> List[Recommendation]:
        """Generate recommendations for improving health system coverage."""
        recommendations = []
        
        # Find health systems with low coverage
        low_coverage_systems = [
            (system, gap) for system, gap in health_system_gaps.items()
            if gap.coverage_percentage < 50 and gap.coverage_percentage > 0
        ]
        
        for system, gap in low_coverage_systems:
            if gap.missing_biomarkers:
                biomarker_names = [b.biomarker_name for b in gap.missing_biomarkers[:3]]
                
                recommendation = Recommendation(
                    title=f"Improve {system.value.title()} Coverage",
                    description=f"{system.value.title()} health system has {gap.coverage_percentage:.1f}% coverage. Adding key biomarkers would improve analysis quality.",
                    priority=RecommendationPriority.HIGH,
                    category=RecommendationCategory.HEALTH_SYSTEM_IMPROVEMENT,
                    action_items=[
                        f"Add {biomarker_names[0]} for better {system.value} assessment",
                        f"Consider adding {', '.join(biomarker_names[1:2])} for comprehensive coverage"
                    ],
                    expected_impact=f"Increases {system.value} health system coverage from {gap.coverage_percentage:.1f}% to 70%+",
                    effort_level="medium",
                    biomarkers_involved=biomarker_names,
                    health_systems_affected=[system]
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_high_priority_recommendations(
        self, 
        high_priority_gaps: List
    ) -> List[Recommendation]:
        """Generate recommendations for high priority biomarker gaps."""
        recommendations = []
        
        if not high_priority_gaps:
            return recommendations
        
        # Group by health system
        gaps_by_system = {}
        for gap in high_priority_gaps:
            system = gap.health_system
            if system not in gaps_by_system:
                gaps_by_system[system] = []
            gaps_by_system[system].append(gap)
        
        for system, gaps in gaps_by_system.items():
            biomarker_names = [gap.biomarker_name for gap in gaps[:3]]
            
            recommendation = Recommendation(
                title=f"Enhance {system.value.title()} Analysis",
                description=f"Adding important biomarkers would significantly improve {system.value} health assessment quality.",
                priority=RecommendationPriority.HIGH,
                category=RecommendationCategory.BIOMARKER_ADDITION,
                action_items=[
                    f"Add {biomarker_names[0]} for enhanced {system.value} analysis",
                    f"Consider adding {', '.join(biomarker_names[1:2])} for comprehensive assessment"
                ],
                expected_impact=f"Improves {system.value} health assessment accuracy and provides more detailed insights",
                effort_level="low",
                biomarkers_involved=biomarker_names,
                health_systems_affected=[system]
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_medium_priority_recommendations(
        self, 
        medium_priority_gaps: List
    ) -> List[Recommendation]:
        """Generate recommendations for medium priority biomarker gaps."""
        recommendations = []
        
        if not medium_priority_gaps:
            return recommendations
        
        # Create a general recommendation for optional biomarkers
        biomarker_names = [gap.biomarker_name for gap in medium_priority_gaps[:5]]
        
        recommendation = Recommendation(
            title="Add Optional Biomarkers for Comprehensive Analysis",
            description=f"Adding optional biomarkers would provide more comprehensive health insights and better analysis quality.",
            priority=RecommendationPriority.MEDIUM,
            category=RecommendationCategory.BIOMARKER_ADDITION,
            action_items=[
                f"Consider adding {', '.join(biomarker_names[:3])} for enhanced analysis",
                f"Optional: Add {', '.join(biomarker_names[3:5])} for comprehensive coverage"
            ],
            expected_impact="Provides more detailed health insights and improves analysis comprehensiveness",
            effort_level="low",
            biomarkers_involved=biomarker_names,
            health_systems_affected=list(set(gap.health_system for gap in medium_priority_gaps))
        )
        recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_analysis_readiness_recommendations(
        self, 
        completeness_result: CompletenessResult, 
        gap_analysis: GapAnalysisResult
    ) -> List[Recommendation]:
        """Generate recommendations for analysis readiness."""
        recommendations = []
        
        if completeness_result.analysis_ready:
            return recommendations
        
        # Analysis readiness recommendations
        if gap_analysis.analysis_blockers:
            blocker_text = "; ".join(gap_analysis.analysis_blockers[:2])
            
            recommendation = Recommendation(
                title="Address Analysis Blockers",
                description=f"Current data has limitations that prevent comprehensive analysis: {blocker_text}",
                priority=RecommendationPriority.CRITICAL,
                category=RecommendationCategory.ANALYSIS_READINESS,
                action_items=[
                    "Add missing critical biomarkers to enable analysis",
                    "Improve health system coverage to meet minimum requirements"
                ],
                expected_impact="Enables comprehensive biomarker analysis and provides actionable health insights",
                effort_level="high",
                biomarkers_involved=[],
                health_systems_affected=[]
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_general_guidance_recommendations(
        self, 
        completeness_result: CompletenessResult
    ) -> List[Recommendation]:
        """Generate general guidance recommendations."""
        recommendations = []
        
        # Confidence level recommendations
        if completeness_result.confidence_level == "low":
            recommendation = Recommendation(
                title="Improve Data Quality for Better Analysis",
                description="Current biomarker data has low confidence level. Adding more biomarkers would significantly improve analysis quality and reliability.",
                priority=RecommendationPriority.HIGH,
                category=RecommendationCategory.DATA_QUALITY,
                action_items=[
                    "Add critical biomarkers to improve confidence level",
                    "Ensure biomarker values are within normal ranges",
                    "Consider retesting if values seem inconsistent"
                ],
                expected_impact="Increases analysis confidence from low to medium or high",
                effort_level="medium",
                biomarkers_involved=[],
                health_systems_affected=[]
            )
            recommendations.append(recommendation)
        
        # Overall score recommendations
        if completeness_result.overall_score < 60:
            recommendation = Recommendation(
                title="Expand Biomarker Panel",
                description=f"Current completeness score is {completeness_result.overall_score:.1f}%. Adding more biomarkers would provide a more comprehensive health assessment.",
                priority=RecommendationPriority.MEDIUM,
                category=RecommendationCategory.GENERAL_GUIDANCE,
                action_items=[
                    "Add biomarkers from under-represented health systems",
                    "Focus on critical biomarkers first, then optional ones",
                    "Consider a comprehensive metabolic panel"
                ],
                expected_impact=f"Could improve completeness score from {completeness_result.overall_score:.1f}% to 80%+",
                effort_level="medium",
                biomarkers_involved=[],
                health_systems_affected=[]
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_summary(
        self, 
        completeness_result: CompletenessResult, 
        gap_analysis: GapAnalysisResult
    ) -> str:
        """Generate a summary of the current state and recommendations."""
        if completeness_result.analysis_ready:
            return f"Your biomarker data is ready for analysis with {completeness_result.overall_score:.1f}% completeness and {completeness_result.confidence_level} confidence."
        else:
            return f"Your biomarker data has {completeness_result.overall_score:.1f}% completeness with {gap_analysis.critical_missing} critical gaps. Adding key biomarkers would enable comprehensive analysis."
    
    def _generate_next_steps(
        self, 
        critical_recs: List[Recommendation], 
        high_recs: List[Recommendation]
    ) -> List[str]:
        """Generate actionable next steps."""
        next_steps = []
        
        if critical_recs:
            next_steps.append("1. Address critical biomarker gaps to enable analysis")
            if critical_recs[0].biomarkers_involved:
                next_steps.append(f"2. Add {critical_recs[0].biomarkers_involved[0]} as highest priority")
        
        if high_recs:
            next_steps.append("3. Improve health system coverage for better analysis quality")
        
        if not critical_recs and not high_recs:
            next_steps.append("1. Your data is ready for analysis")
            next_steps.append("2. Consider adding optional biomarkers for enhanced insights")
        
        return next_steps
    
    def _estimate_improvement(
        self, 
        completeness_result: CompletenessResult, 
        gap_analysis: GapAnalysisResult
    ) -> str:
        """Estimate potential improvement from following recommendations."""
        current_score = completeness_result.overall_score
        
        if gap_analysis.critical_missing > 0:
            return f"Adding critical biomarkers could improve score from {current_score:.1f}% to 70%+ and enable analysis"
        elif current_score < 80:
            return f"Following recommendations could improve score from {current_score:.1f}% to 85%+ for comprehensive analysis"
        else:
            return "Your data is already well-suited for analysis. Recommendations would provide incremental improvements"
    
    def get_recommendation_summary(self, recommendation_set: RecommendationSet) -> Dict[str, Any]:
        """
        Get a summary of recommendations.
        
        Args:
            recommendation_set: Complete recommendation set
            
        Returns:
            Dictionary with recommendation summary
        """
        return {
            "total_recommendations": len(recommendation_set.recommendations),
            "critical_count": len(recommendation_set.critical_recommendations),
            "high_priority_count": len(recommendation_set.high_priority_recommendations),
            "medium_priority_count": len(recommendation_set.medium_priority_recommendations),
            "low_priority_count": len(recommendation_set.low_priority_recommendations),
            "analysis_ready": recommendation_set.analysis_readiness,
            "next_steps_count": len(recommendation_set.next_steps),
            "estimated_improvement": recommendation_set.estimated_improvement
        }
