"""
Analysis orchestrator - enforces canonical-only keys and coordinates analysis.
"""

from typing import Dict, Any, List, Mapping, Optional
import time

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
from core.llm.client import GeminiClient
from core.llm.prompts import PromptTemplates, PromptType
from core.llm.parsing import ResponseParser


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
        self.llm_client = GeminiClient()
        self.response_parser = ResponseParser()
    
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
        
        # Process questionnaire data if provided
        if questionnaire_data:
            # Validate questionnaire data
            submission = QuestionnaireSubmission(
                responses=questionnaire_data,
                submission_id=f"{analysis_id}_questionnaire"
            )
            is_valid, errors = self.questionnaire_validator.validate_submission(submission)
            if not is_valid:
                print(f"Warning: Questionnaire validation errors: {errors}")
            
            # Map questionnaire to lifestyle factors and medical history
            lifestyle_factors, medical_history = self.questionnaire_mapper.map_submission(submission)
            
            # Extract demographic data
            demographics = self.questionnaire_mapper.get_demographic_data(questionnaire_data)
            
            # Update user_data with questionnaire-derived information
            user_data.update({
                "questionnaire": questionnaire_data,
                "lifestyle_factors": {
                    "diet_level": lifestyle_factors.diet_level.value,
                    "sleep_hours": lifestyle_factors.sleep_hours,
                    "exercise_minutes_per_week": lifestyle_factors.exercise_minutes_per_week,
                    "alcohol_units_per_week": lifestyle_factors.alcohol_units_per_week,
                    "smoking_status": lifestyle_factors.smoking_status,
                    "stress_level": lifestyle_factors.stress_level.value,
                    "sedentary_hours_per_day": lifestyle_factors.sedentary_hours_per_day,
                    "caffeine_consumption": lifestyle_factors.caffeine_consumption,
                    "fluid_intake_liters": lifestyle_factors.fluid_intake_liters
                },
                "medical_history": {
                    "conditions": medical_history.conditions,
                    "medications": medical_history.medications,
                    "family_history": medical_history.family_history,
                    "supplements": medical_history.supplements,
                    "sleep_disorders": medical_history.sleep_disorders,
                    "allergies": medical_history.allergies
                }
            })
            
            # Update demographics if available
            user_data.update(demographics)
        
        # Create user object
        user = self.context_factory.create_user_from_dict(user_data)
        
        # Extract questionnaire data for AnalysisContext
        questionnaire_responses = user_data.get("questionnaire")
        lifestyle_factors = user_data.get("lifestyle_factors")
        medical_history = user_data.get("medical_history")
        
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
    
    def _generate_insights(self, context: AnalysisContext, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights using LLM integration.
        
        Args:
            context: Analysis context with user and biomarker data
            analysis_result: Results from scoring and clustering
            
        Returns:
            List of generated insights
        """
        try:
            # Prepare data for LLM
            biomarker_data = {
                biomarker.name: {
                    "value": biomarker.value,
                    "unit": biomarker.unit
                }
                for biomarker in context.biomarker_panel.biomarkers.values()
            }
            
            scoring_results = analysis_result.get("scoring_summary", {})
            clustering_results = analysis_result.get("clustering_summary", {})
            
            user_profile = {
                "age": context.user.age,
                "gender": context.user.gender,
                "height": getattr(context.user, 'height', None),
                "weight": getattr(context.user, 'weight', None)
            }
            
            # Format prompt for insight synthesis
            prompt = PromptTemplates.format_prompt(
                PromptType.INSIGHT_SYNTHESIS,
                biomarker_data=str(biomarker_data),
                scoring_results=str(scoring_results),
                clustering_results=str(clustering_results),
                user_profile=str(user_profile)
            )
            
            # Get schema for structured output
            template = PromptTemplates.get_template(PromptType.INSIGHT_SYNTHESIS)
            
            # Generate insights using LLM
            response = self.llm_client.generate_structured_output(prompt, template.output_schema)
            
            # Parse and validate response
            parsed = self.response_parser.parse_and_validate(response, "insight_synthesis")
            
            if parsed.success:
                return parsed.data.get("insights", [])
            else:
                # Fallback to basic insights if LLM fails
                return self._generate_fallback_insights(context, analysis_result)
                
        except Exception as e:
            # Log error and return fallback insights
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"LLM insight generation failed: {str(e)}")
            return self._generate_fallback_insights(context, analysis_result)
    
    def _generate_fallback_insights(self, context: AnalysisContext, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate fallback insights when LLM is unavailable.
        
        Args:
            context: Analysis context
            analysis_result: Analysis results
            
        Returns:
            List of basic insights
        """
        insights = []
        
        # Basic insights based on clusters
        clusters = analysis_result.get("clusters", [])
        for cluster in clusters:
            insight = {
                "category": cluster.get("name", "general"),
                "title": f"{cluster.get('name', 'Health')} Analysis",
                "description": cluster.get("description", "Health pattern identified"),
                "severity": cluster.get("severity", "moderate"),
                "confidence": cluster.get("confidence", 0.7),
                "evidence": [f"Biomarker pattern: {cluster.get('biomarkers', [])}"],
                "recommendations": ["Consult with healthcare provider for personalized recommendations"]
            }
            insights.append(insight)
        
        return insights
    
    def _run_analysis_pipeline(self, context: AnalysisContext) -> Dict[str, Any]:
        """
        Run the full analysis pipeline (scoring, clustering, etc.).
        
        Args:
            context: Analysis context
            
        Returns:
            Analysis results dictionary
        """
        try:
            # For now, return a basic structure that matches what the LLM integration expects
            # This will be expanded when the full pipeline is implemented
            return {
                "clusters": [],
                "scoring_summary": {"overall_score": 85},
                "clustering_summary": {"total_clusters": 0}
            }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Analysis pipeline failed: {str(e)}")
            return {
                "clusters": [],
                "scoring_summary": {"overall_score": 0},
                "clustering_summary": {"total_clusters": 0}
            }

    def run(self, biomarkers: Mapping[str, Any], user: Mapping[str, Any], *, assume_canonical: bool = False):
        if not assume_canonical:
            self._assert_canonical_only(biomarkers, where="run")
        
        canonical_map = dict(biomarkers)

        # continue with existing scoring → clustering → insights using `canonical_map`
        # Create analysis context
        context = self.create_analysis_context(
            analysis_id="analysis_" + str(int(time.time())),
            raw_biomarkers=canonical_map,
            user_data=user,
            assume_canonical=True
        )
        
        # Run full analysis pipeline
        analysis_result = self._run_analysis_pipeline(context)
        
        # Generate insights using LLM
        insights = self._generate_insights(context, analysis_result)
        
        # Build final result
        from core.models.results import AnalysisDTO, InsightResult, ClusterHit
        from datetime import datetime
        
        # Convert insights to InsightResult objects
        insight_results = []
        for i, insight in enumerate(insights):
            insight_result = InsightResult(
                insight_id=f"insight_{i}",
                title=insight.get("title", "Health Insight"),
                description=insight.get("description", ""),
                category=insight.get("category", "general"),
                confidence=insight.get("confidence", 0.5),
                severity=insight.get("severity", "moderate"),
                biomarkers=insight.get("biomarkers", []),
                recommendations=insight.get("recommendations", [])
            )
            insight_results.append(insight_result)
        
        # Convert clusters to ClusterHit objects
        cluster_hits = []
        for i, cluster in enumerate(analysis_result.get("clusters", [])):
            cluster_hit = ClusterHit(
                cluster_id=f"cluster_{i}",
                name=cluster.get("name", "Health Cluster"),
                biomarkers=cluster.get("biomarkers", []),
                confidence=cluster.get("confidence", 0.5),
                severity=cluster.get("severity", "moderate"),
                description=cluster.get("description", "")
            )
            cluster_hits.append(cluster_hit)
        
        return AnalysisDTO(
            analysis_id=context.analysis_id,
            clusters=cluster_hits,
            insights=insight_results,
            status="complete",
            created_at=context.created_at
        )
