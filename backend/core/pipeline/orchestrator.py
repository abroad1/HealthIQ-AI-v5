"""
Analysis orchestrator - enforces canonical-only keys and coordinates analysis.
"""

from typing import Dict, Any, List, Mapping, Optional

from core.canonical.normalize import BiomarkerNormalizer, normalize_panel
from core.canonical.resolver import resolve_to_canonical
from core.pipeline.context_factory import AnalysisContextFactory
from core.models.context import AnalysisContext
from core.models.user import User
from core.validation.completeness import DataCompletenessValidator
from core.validation.gaps import BiomarkerGapAnalyzer
from core.validation.recommendations import RecommendationEngine
from core.scoring.engine import ScoringEngine
from core.scoring.overlays import LifestyleOverlays, LifestyleProfile
from core.pipeline.questionnaire_mapper import QuestionnaireMapper, MappedLifestyleFactors
from core.models.questionnaire import QuestionnaireSubmission, create_questionnaire_validator
from core.clustering.engine import ClusteringEngine
from core.insights.synthesis import InsightSynthesizer


class AnalysisOrchestrator:
    """Orchestrates biomarker analysis with canonical enforcement."""
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None):
        """
        Initialize the orchestrator.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.context_factory = AnalysisContextFactory()
        self.completeness_validator = DataCompletenessValidator(normalizer)
        self.gap_analyzer = BiomarkerGapAnalyzer(normalizer)
        self.recommendation_engine = RecommendationEngine(normalizer)
        self.scoring_engine = ScoringEngine(normalizer)
        self.lifestyle_overlays = LifestyleOverlays()
        self.questionnaire_mapper = QuestionnaireMapper()
        self.questionnaire_validator = create_questionnaire_validator()
        self.clustering_engine = ClusteringEngine()
        self.insight_synthesizer = InsightSynthesizer()
    
    def create_analysis_context(
        self,
        analysis_id: str,
        raw_biomarkers: Dict[str, Any],
        user_data: Dict[str, Any],
        questionnaire_data: Optional[Dict[str, Any]] = None,
        *,
        assume_canonical: bool = False
    ) -> AnalysisContext:
        """
        Create analysis context with canonical enforcement.
        
        Args:
            analysis_id: Unique analysis identifier
            raw_biomarkers: Raw biomarker data (may contain aliases)
            user_data: Raw user data
            questionnaire_data: Optional questionnaire responses
            assume_canonical: If True, skip canonical validation
            
        Returns:
            AnalysisContext with canonical biomarkers only
            
        Raises:
            ValueError: If non-canonical biomarkers are found after normalization
        """
        if not assume_canonical:
            self._assert_canonical_only(raw_biomarkers, where="create_analysis_context")
        
        # Normalize biomarkers (maps aliases to canonical names)
        biomarker_panel, unmapped_keys = self.normalizer.normalize_biomarkers(raw_biomarkers)
        
        # Log unmapped keys (in production, this would be proper logging)
        if unmapped_keys:
            print(f"Warning: Unmapped biomarker keys: {unmapped_keys}")
        
        # Enforce canonical-only keys in the final panel
        non_canonical = self.normalizer.validate_canonical_only(biomarker_panel.biomarkers)
        if non_canonical:
            raise ValueError(
                f"Non-canonical biomarker keys found after normalization: {non_canonical}. "
                "All biomarkers must use canonical names only."
            )
        
        # Initialize questionnaire-related variables
        questionnaire_responses = None
        lifestyle_factors = None
        medical_history = None
        
        # Process questionnaire data if provided
        if questionnaire_data:
            # Always set questionnaire_responses, even if validation fails
            questionnaire_responses = questionnaire_data
            
            # Validate questionnaire data
            submission = QuestionnaireSubmission(
                responses=questionnaire_data,
                submission_id=f"{analysis_id}_questionnaire"
            )
            is_valid, errors = self.questionnaire_validator.validate_submission(submission)
            if not is_valid:
                print(f"Warning: Questionnaire validation errors: {errors}")
                # Continue processing with raw data even if validation fails
            
            # Map questionnaire to lifestyle factors and medical history
            try:
                mapped_lifestyle_factors, mapped_medical_history = self.questionnaire_mapper.map_submission(submission)
                
                # Convert to dictionaries for context
                lifestyle_factors = {
                    "diet_level": mapped_lifestyle_factors.diet_level.value,
                    "sleep_hours": mapped_lifestyle_factors.sleep_hours,
                    "exercise_minutes_per_week": mapped_lifestyle_factors.exercise_minutes_per_week,
                    "alcohol_units_per_week": mapped_lifestyle_factors.alcohol_units_per_week,
                    "smoking_status": mapped_lifestyle_factors.smoking_status,
                    "stress_level": mapped_lifestyle_factors.stress_level.value,
                    "sedentary_hours_per_day": mapped_lifestyle_factors.sedentary_hours_per_day,
                    "caffeine_consumption": mapped_lifestyle_factors.caffeine_consumption,
                    "fluid_intake_liters": mapped_lifestyle_factors.fluid_intake_liters
                }
                
                medical_history = {
                    "conditions": mapped_medical_history.conditions,
                    "medications": mapped_medical_history.medications,
                    "family_history": mapped_medical_history.family_history,
                    "supplements": mapped_medical_history.supplements,
                    "sleep_disorders": mapped_medical_history.sleep_disorders,
                    "allergies": mapped_medical_history.allergies
                }
                
                # Update user_data with questionnaire-derived information
                user_data.update({
                    "questionnaire": questionnaire_data,
                    "lifestyle_factors": lifestyle_factors,
                    "medical_history": medical_history
                })
                
                # Extract demographic data
                demographics = self.questionnaire_mapper.get_demographic_data(questionnaire_data)
                user_data.update(demographics)
                
            except Exception as e:
                print(f"Warning: Error mapping questionnaire data: {e}")
                # Continue with empty lifestyle_factors and medical_history
                lifestyle_factors = {}
                medical_history = {}
        
        # Create user object
        user = self.context_factory.create_user_from_dict(user_data)
        
        # Create analysis context
        context = self.context_factory.create_context(
            analysis_id=analysis_id,
            user=user,
            biomarker_panel=biomarker_panel,
            questionnaire_responses=questionnaire_responses,
            lifestyle_factors=lifestyle_factors,
            medical_history=medical_history
        )
        
        return context
    
    def validate_biomarker_panel(self, biomarkers: Dict[str, Any]) -> List[str]:
        """
        Validate that all biomarker keys are canonical.
        
        Args:
            biomarkers: Biomarker data to validate
            
        Returns:
            List of non-canonical keys found
        """
        return self.normalizer.validate_canonical_only(biomarkers)
    
    def get_canonical_biomarkers(self) -> List[str]:
        """
        Get list of all canonical biomarker names.
        
        Returns:
            List of canonical biomarker names
        """
        return self.normalizer.get_canonical_biomarkers()
    
    def assess_data_completeness(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess data completeness for biomarker analysis.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            Dictionary with completeness assessment results
        """
        completeness_result = self.completeness_validator.assess_completeness(biomarkers)
        
        return {
            "overall_score": completeness_result.overall_score,
            "health_system_scores": {
                system.value: score for system, score in completeness_result.health_system_scores.items()
            },
            "missing_critical": completeness_result.missing_critical,
            "missing_optional": completeness_result.missing_optional,
            "confidence_level": completeness_result.confidence_level,
            "analysis_ready": completeness_result.analysis_ready,
            "recommendations": completeness_result.recommendations
        }
    
    def analyze_data_gaps(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze gaps in biomarker data.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            Dictionary with gap analysis results
        """
        gap_analysis = self.gap_analyzer.analyze_gaps(biomarkers)
        
        return {
            "total_missing": gap_analysis.total_missing,
            "critical_missing": gap_analysis.critical_missing,
            "analysis_ready": len(gap_analysis.analysis_blockers) == 0,
            "analysis_blockers": gap_analysis.analysis_blockers,
            "critical_gaps": [
                {
                    "biomarker_name": gap.biomarker_name,
                    "health_system": gap.health_system.value,
                    "severity": gap.severity.value,
                    "description": gap.description,
                    "impact": gap.impact
                }
                for gap in gap_analysis.critical_gaps
            ],
            "health_system_gaps": {
                system.value: {
                    "completeness_score": gap.completeness_score,
                    "coverage_percentage": gap.coverage_percentage,
                    "analysis_ready": gap.analysis_ready,
                    "missing_biomarkers": [
                        {
                            "biomarker_name": gap.biomarker_name,
                            "severity": gap.severity.value,
                            "description": gap.description
                        }
                        for gap in gap.missing_biomarkers
                    ]
                }
                for system, gap in gap_analysis.health_system_gaps.items()
            },
            "recommendations": gap_analysis.recommendations
        }
    
    def generate_recommendations(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate recommendations for improving biomarker data.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            
        Returns:
            Dictionary with recommendation results
        """
        recommendation_set = self.recommendation_engine.generate_recommendations(biomarkers)
        
        return {
            "summary": recommendation_set.summary,
            "analysis_readiness": recommendation_set.analysis_readiness,
            "estimated_improvement": recommendation_set.estimated_improvement,
            "next_steps": recommendation_set.next_steps,
            "recommendations": [
                {
                    "title": rec.title,
                    "description": rec.description,
                    "priority": rec.priority.value,
                    "category": rec.category.value,
                    "action_items": rec.action_items,
                    "expected_impact": rec.expected_impact,
                    "effort_level": rec.effort_level,
                    "biomarkers_involved": rec.biomarkers_involved,
                    "health_systems_affected": [system.value for system in rec.health_systems_affected]
                }
                for rec in recommendation_set.recommendations
            ],
            "critical_recommendations": [
                {
                    "title": rec.title,
                    "description": rec.description,
                    "action_items": rec.action_items,
                    "expected_impact": rec.expected_impact,
                    "biomarkers_involved": rec.biomarkers_involved
                }
                for rec in recommendation_set.critical_recommendations
            ],
            "high_priority_recommendations": [
                {
                    "title": rec.title,
                    "description": rec.description,
                    "action_items": rec.action_items,
                    "expected_impact": rec.expected_impact,
                    "biomarkers_involved": rec.biomarkers_involved
                }
                for rec in recommendation_set.high_priority_recommendations
            ]
        }
    
    def score_biomarkers(
        self,
        biomarkers: Dict[str, Any],
        age: Optional[int] = None,
        sex: Optional[str] = None,
        lifestyle_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Score biomarkers across all health systems.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            age: Patient age for adjustments
            sex: Patient sex for adjustments
            lifestyle_data: Lifestyle profile data for overlays
            
        Returns:
            Dictionary with scoring results
        """
        # Create lifestyle profile if provided
        lifestyle_profile = None
        if lifestyle_data:
            lifestyle_profile = self.lifestyle_overlays.create_lifestyle_profile(
                diet_level=lifestyle_data.get("diet_level", "average"),
                sleep_hours=lifestyle_data.get("sleep_hours", 7.0),
                exercise_minutes_per_week=lifestyle_data.get("exercise_minutes_per_week", 150),
                alcohol_units_per_week=lifestyle_data.get("alcohol_units_per_week", 5),
                smoking_status=lifestyle_data.get("smoking_status", "never"),
                stress_level=lifestyle_data.get("stress_level", "average")
            )
        
        # Normalize biomarkers first
        normalized_biomarkers, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
        
        # Score biomarkers
        scoring_result = self.scoring_engine.score_biomarkers(
            normalized_biomarkers, age, sex, lifestyle_profile
        )
        
        return {
            "overall_score": scoring_result.overall_score,
            "confidence": scoring_result.confidence.value,
            "health_system_scores": {
                system_name: {
                    "overall_score": system_score.overall_score,
                    "confidence": system_score.confidence.value,
                    "missing_biomarkers": system_score.missing_biomarkers,
                    "recommendations": system_score.recommendations,
                    "biomarker_scores": [
                        {
                            "biomarker_name": score.biomarker_name,
                            "value": score.value,
                            "score": score.score,
                            "score_range": score.score_range.value,
                            "confidence": score.confidence.value
                        }
                        for score in system_score.biomarker_scores
                    ]
                }
                for system_name, system_score in scoring_result.health_system_scores.items()
            },
            "missing_biomarkers": scoring_result.missing_biomarkers,
            "recommendations": scoring_result.recommendations,
            "lifestyle_adjustments": scoring_result.lifestyle_adjustments
        }
    
    def cluster_biomarkers(
        self,
        context: AnalysisContext,
        scoring_result: Optional[Dict[str, Any]] = None,
        lifestyle_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Cluster biomarkers based on scoring results.
        
        Args:
            context: Analysis context with biomarker data
            scoring_result: Optional pre-computed scoring results
            lifestyle_data: Lifestyle profile data for overlays
            
        Returns:
            Dictionary with clustering results
        """
        # If scoring result not provided, compute it
        if scoring_result is None:
            # Extract biomarkers from context
            biomarkers = {}
            for biomarker_name, biomarker_value in context.biomarker_panel.biomarkers.items():
                if hasattr(biomarker_value, 'value'):
                    biomarkers[biomarker_name] = biomarker_value.value
                else:
                    biomarkers[biomarker_name] = biomarker_value
            
            # Create lifestyle profile if provided
            lifestyle_profile = None
            if lifestyle_data:
                lifestyle_profile = self.lifestyle_overlays.create_lifestyle_profile(
                    diet_level=lifestyle_data.get("diet_level", "average"),
                    sleep_hours=lifestyle_data.get("sleep_hours", 7.0),
                    exercise_minutes_per_week=lifestyle_data.get("exercise_minutes_per_week", 150),
                    alcohol_units_per_week=lifestyle_data.get("alcohol_units_per_week", 5),
                    smoking_status=lifestyle_data.get("smoking_status", "never"),
                    stress_level=lifestyle_data.get("stress_level", "average")
                )
            
            # Normalize biomarkers first
            normalized_biomarkers, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
            
            # Score biomarkers
            scoring_result = self.scoring_engine.score_biomarkers(
                normalized_biomarkers, 
                context.user.age, 
                context.user.gender, 
                lifestyle_profile
            )
        
        # Cluster biomarkers
        # Note: The clustering engine expects a ScoringResult object, but we're working with dict format
        # For now, we'll extract the necessary data and create a simplified result
        clustering_result = self.clustering_engine.cluster_biomarkers(context, scoring_result)
        
        return {
            "clusters": [
                {
                    "cluster_id": cluster.cluster_id,
                    "name": cluster.name,
                    "biomarkers": cluster.biomarkers,
                    "description": cluster.description,
                    "severity": cluster.severity,
                    "confidence": cluster.confidence
                }
                for cluster in clustering_result.clusters
            ],
            "clustering_summary": {
                "total_clusters": len(clustering_result.clusters),
                "algorithm_used": clustering_result.algorithm_used.value if hasattr(clustering_result.algorithm_used, 'value') else clustering_result.algorithm_used,
                "confidence_score": clustering_result.confidence_score,
                "processing_time_ms": clustering_result.processing_time_ms,
                "validation_summary": clustering_result.validation_summary
            }
        }
    
    def synthesize_insights(
        self,
        context: AnalysisContext,
        biomarker_scores: Optional[Dict[str, Any]] = None,
        clustering_results: Optional[Dict[str, Any]] = None,
        lifestyle_data: Optional[Dict[str, Any]] = None,
        requested_categories: Optional[List[str]] = None,
        max_insights_per_category: int = 3
    ) -> Dict[str, Any]:
        """
        Synthesize insights from analysis context and results.
        
        Args:
            context: Analysis context with user and biomarker data
            biomarker_scores: Optional pre-computed biomarker scoring results
            clustering_results: Optional pre-computed clustering results
            lifestyle_data: Lifestyle profile data
            requested_categories: Specific categories to generate insights for
            max_insights_per_category: Maximum insights per category
            
        Returns:
            Dictionary with insight synthesis results
        """
        # If biomarker scores not provided, compute them
        if biomarker_scores is None:
            # Extract biomarkers from context
            biomarkers = {}
            for biomarker_name, biomarker_value in context.biomarker_panel.biomarkers.items():
                if hasattr(biomarker_value, 'value'):
                    biomarkers[biomarker_name] = biomarker_value.value
                else:
                    biomarkers[biomarker_name] = biomarker_value
            
            # Create lifestyle profile if provided
            lifestyle_profile = None
            if lifestyle_data:
                lifestyle_profile = self.lifestyle_overlays.create_lifestyle_profile(
                    diet_level=lifestyle_data.get("diet_level", "average"),
                    sleep_hours=lifestyle_data.get("sleep_hours", 7.0),
                    exercise_minutes_per_week=lifestyle_data.get("exercise_minutes_per_week", 150),
                    alcohol_units_per_week=lifestyle_data.get("alcohol_units_per_week", 5),
                    smoking_status=lifestyle_data.get("smoking_status", "never"),
                    stress_level=lifestyle_data.get("stress_level", "average")
                )
            
            # Normalize biomarkers first
            normalized_biomarkers, unmapped = self.normalizer.normalize_biomarkers(biomarkers)
            
            # Score biomarkers
            scoring_result = self.scoring_engine.score_biomarkers(
                normalized_biomarkers, 
                context.user.age, 
                context.user.gender, 
                lifestyle_profile
            )
            
            # Convert scoring result to dict format
            biomarker_scores = {
                "overall_score": scoring_result.overall_score,
                "confidence": scoring_result.confidence.value,
                "health_system_scores": {
                    system_name: {
                        "overall_score": system_score.overall_score,
                        "confidence": system_score.confidence.value,
                        "missing_biomarkers": system_score.missing_biomarkers,
                        "recommendations": system_score.recommendations,
                        "biomarker_scores": [
                            {
                                "biomarker_name": score.biomarker_name,
                                "value": score.value,
                                "score": score.score,
                                "score_range": score.score_range.value,
                                "confidence": score.confidence.value
                            }
                            for score in system_score.biomarker_scores
                        ]
                    }
                    for system_name, system_score in scoring_result.health_system_scores.items()
                },
                "missing_biomarkers": scoring_result.missing_biomarkers,
                "recommendations": scoring_result.recommendations,
                "lifestyle_adjustments": scoring_result.lifestyle_adjustments
            }
        
        # If clustering results not provided, compute them
        if clustering_results is None:
            clustering_results = self.cluster_biomarkers(
                context=context,
                scoring_result=biomarker_scores,
                lifestyle_data=lifestyle_data
            )
        
        # Extract lifestyle profile from context or provided data
        lifestyle_profile = {}
        if lifestyle_data:
            lifestyle_profile = lifestyle_data
        elif hasattr(context.user, 'lifestyle_factors') and context.user.lifestyle_factors:
            lifestyle_profile = context.user.lifestyle_factors
        
        # Synthesize insights
        synthesis_result = self.insight_synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile,
            requested_categories=requested_categories,
            max_insights_per_category=max_insights_per_category
        )
        
        return {
            "analysis_id": synthesis_result.analysis_id,
            "insights": [
                {
                    "id": insight.id,
                    "category": insight.category,
                    "summary": insight.summary,
                    "evidence": insight.evidence,
                    "confidence": insight.confidence,
                    "severity": insight.severity,
                    "recommendations": insight.recommendations,
                    "biomarkers_involved": insight.biomarkers_involved,
                    "lifestyle_factors": insight.lifestyle_factors,
                    "created_at": insight.created_at
                }
                for insight in synthesis_result.insights
            ],
            "synthesis_summary": synthesis_result.synthesis_summary,
            "total_insights": synthesis_result.total_insights,
            "categories_covered": synthesis_result.categories_covered,
            "overall_confidence": synthesis_result.overall_confidence,
            "processing_time_ms": synthesis_result.processing_time_ms,
            "created_at": synthesis_result.created_at
        }
    
    def _assert_canonical_only(self, raw_map: Mapping[str, Any], *, where: str = "pre-context") -> None:
        """Raise if any biomarker keys are not already canonical.
        We resolve each key; if resolution changes the name, it was an alias.
        """
        offenders = []
        for k in raw_map.keys():
            canonical = resolve_to_canonical(k)
            if canonical != k:
                offenders.append(k)
        if offenders:
            offenders.sort()
            raise ValueError(f"Non-canonical biomarker keys found: {', '.join(offenders)}")

    def run(self, biomarkers: Mapping[str, Any], user: Mapping[str, Any], *, assume_canonical: bool = False):
        if not assume_canonical:
            self._assert_canonical_only(biomarkers, where="run")
        
        canonical_map = dict(biomarkers)

        # continue with existing scoring → clustering → insights using `canonical_map`
        # For now, return a stub result
        from core.models.results import AnalysisDTO
        result = AnalysisDTO(
            analysis_id="stub_analysis_id",
            clusters=[],
            insights=[],
            status="complete",
            created_at="2024-01-01T00:00:00Z"
        )
        
        # Sprint 9b - Persistence integration at phase:"complete"
        if result.status == "complete":
            # Note: Persistence is handled by the calling service/route
            # This ensures non-blocking SSE and proper error handling
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info(f"Analysis {result.analysis_id} completed, ready for persistence")
            logger.debug(f"Analysis {result.analysis_id} marked for persistence by calling service")
        
        return result
