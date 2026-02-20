"""
Analysis orchestrator - enforces canonical-only keys and coordinates analysis.
"""

import os
from typing import Dict, Any, List, Mapping, Optional

# Reserved key for unit-normalisation invariant (Sprint 5). Set by callers after apply_unit_normalisation.
UNIT_NORMALISATION_META_KEY = "__unit_normalisation_meta__"

from core.canonical.normalize import BiomarkerNormalizer, normalize_panel
from core.canonical.resolver import resolve_to_canonical, CanonicalResolver
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
from core.clustering.cluster_engine_v2 import ClusterEngineV2
from core.insights.synthesis import InsightSynthesizer
from core.analytics.primitives import frontend_status_from_value_and_range
from core.analytics.criticality import evaluate_criticality
from core.analytics.ratio_registry import RatioRegistry, DERIVED_IDS, compute
from core.analytics.cluster_schema import get_cluster_schema_version_stamp
from core.analytics.insight_graph_builder import build_insight_graph_v1
from core.analytics.replay_manifest_builder import build_replay_manifest_v1
from core.analytics.scoring_policy_registry import load_scoring_policy
from core.analytics.evidence_registry import load_evidence_registry
from core.analytics.snapshot_linker import link_prior_snapshot_insight_graphs
from core.analytics.state_transition_engine import build_state_transition_v1
from core.analytics.state_engine import build_state_engine_v1
from core.analytics.precedence_engine import build_precedence_v1
from core.analytics.causal_layer_engine import build_causal_layer_v1
from core.analytics.calibration_engine import build_calibration_layer_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.arbitration_engine import build_dominance_edges_v1, build_arbitration_result_v1
from core.analytics.conflict_registry import load_conflict_registry
from core.analytics.arbitration_registry import load_arbitration_registry
from core.units.registry import UNIT_REGISTRY_VERSION
from core.scoring.rules import DERIVED_RATIO_BOUNDS


class AnalysisOrchestrator:
    """Orchestrates biomarker analysis with canonical enforcement."""
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None, db_session: Any = None):
        """
        Initialize the orchestrator.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
            db_session: Optional DB session for longitudinal snapshot linking
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.db_session = db_session
        self.context_factory = AnalysisContextFactory()
        self.completeness_validator = DataCompletenessValidator(self.normalizer)
        self.gap_analyzer = BiomarkerGapAnalyzer(self.normalizer)
        self.recommendation_engine = RecommendationEngine(self.normalizer)
        self.scoring_engine = ScoringEngine(self.normalizer)
        self.lifestyle_overlays = LifestyleOverlays()
        self.questionnaire_mapper = QuestionnaireMapper()
        self.questionnaire_validator = create_questionnaire_validator()
        self.clustering_engine = ClusterEngineV2()
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

        # Drop any unmapped_* entries before canonical enforcement
        filtered_biomarkers = {
            key: value for key, value in biomarker_panel.biomarkers.items()
            if not key.startswith("unmapped_")
        }
        biomarker_panel = biomarker_panel.model_copy(update={"biomarkers": filtered_biomarkers})
        
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
        lifestyle_data: Optional[Dict[str, Any]] = None,
        input_reference_ranges: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Score biomarkers across all health systems.
        
        Args:
            biomarkers: Dictionary of biomarker data with canonical keys
            age: Patient age for adjustments
            sex: Patient sex for adjustments
            lifestyle_data: Lifestyle profile data for overlays
            input_reference_ranges: Optional dict mapping biomarker names to their input reference ranges
            
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
        
        # Score biomarkers with input reference ranges
        scoring_result = self.scoring_engine.score_biomarkers(
            normalized_biomarkers, age, sex, lifestyle_profile, input_reference_ranges=input_reference_ranges
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

        # Sprint 7: Build InsightGraph as sole LLM input
        filtered_biomarkers = {}
        for bm_name, bm_val in context.biomarker_panel.biomarkers.items():
            v = bm_val.value if hasattr(bm_val, 'value') else bm_val
            filtered_biomarkers[bm_name] = v if isinstance(v, (int, float)) else (v.get('value', v) if isinstance(v, dict) else v)
        insight_graph = build_insight_graph_v1(
            analysis_id=context.analysis_id,
            scoring_result=biomarker_scores,
            clustering_result=clustering_results,
            criticality_result=evaluate_criticality(biomarker_scores, set(filtered_biomarkers.keys())) if biomarker_scores else None,
            derived_ratios_meta=None,
            input_reference_ranges=None,
            filtered_biomarkers=filtered_biomarkers,
            context=context,
            lab_origin=None,
            unit_normalisation_meta=None,
        )

        # Synthesize insights (LLM receives only InsightGraph)
        synthesis_result = self.insight_synthesizer.synthesize_insights(
            context=context,
            insight_graph=insight_graph,
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

    def _synthesize_from_insight_graph(
        self,
        context: AnalysisContext,
        insight_graph: Any,
        lifestyle_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Sprint 7: Synthesize insights using InsightGraph only. Used by run()."""
        synthesis_result = self.insight_synthesizer.synthesize_insights(
            context=context,
            insight_graph=insight_graph,
            lifestyle_profile=lifestyle_profile,
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
        """
        Run the complete analysis pipeline: scoring → clustering → insights.
        
        Args:
            biomarkers: Canonical biomarker data (must be unit-normalised; carry __unit_normalisation_meta__)
            user: User data
            assume_canonical: Whether to skip canonical validation
            
        Returns:
            AnalysisDTO with complete analysis results
            
        Raises:
            ValueError: If unit normalisation meta is missing (apply_unit_normalisation required before run).
        """
        import logging
        import uuid
        from datetime import datetime, UTC
        from core.models.results import AnalysisDTO, BiomarkerScore as BiomarkerScoreDTO, ClusterHit, InsightResult
        
        logger = logging.getLogger(__name__)
        
        # Sprint 5: Enforce unit-normalisation invariant (non-bypassable)
        biomarkers = dict(biomarkers)
        unit_meta = biomarkers.pop(UNIT_NORMALISATION_META_KEY, None)
        if not unit_meta or not unit_meta.get("unit_normalised"):
            raise ValueError(
                "Unit normalisation required before orchestrator.run (apply_unit_normalisation)."
            )
        
        analysis_id = str(uuid.uuid4())
        try:
            if not assume_canonical:
                self._assert_canonical_only(biomarkers, where="run")
            
            # Initialize canonical resolver for units and reference ranges
            resolver = CanonicalResolver()
            
            logger.info(f"Starting analysis {analysis_id} with {len(biomarkers)} biomarkers")
            
            # Trace biomarkers received by orchestrator
            print("[TRACE] Orchestrator input biomarkers:", list(biomarkers.keys()))
            
            # Quarantine unmapped biomarkers before downstream processing
            unmapped_biomarkers = []
            filtered_biomarkers = {}
            alias_service = self.normalizer.alias_service
            for key, value in biomarkers.items():
                if key.startswith("unmapped_"):
                    unmapped_biomarkers.append(key)
                    continue
                resolved = alias_service.resolve(key)
                if resolved.startswith("unmapped_"):
                    unmapped_biomarkers.append(resolved)
                    continue
                filtered_biomarkers[key] = value
            unmapped_biomarkers = sorted(set(unmapped_biomarkers))
            skipped_unmapped = len(biomarkers) - len(filtered_biomarkers)
            logger.info(
                "Biomarker quarantine: total=%s, canonical=%s, unmapped_skipped=%s",
                len(biomarkers),
                len(filtered_biomarkers),
                skipped_unmapped,
            )

            # Step 1: Convert biomarkers to simple format for scoring engine and preserve reference ranges
            logger.info("Step 1: Converting biomarkers for scoring")
            simple_biomarkers = {}
            input_reference_ranges = {}  # Preserve reference ranges from input
            for biomarker_name, biomarker_data in filtered_biomarkers.items():
                if isinstance(biomarker_data, dict):
                    simple_biomarkers[biomarker_name] = biomarker_data.get('value', biomarker_data.get('measurement', 0))
                    # Extract reference range if present and valid
                    ref_range = biomarker_data.get('reference_range') or biomarker_data.get('referenceRange')
                    if ref_range and isinstance(ref_range, dict):
                        min_val = ref_range.get('min')
                        max_val = ref_range.get('max')
                        if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
                            input_reference_ranges[biomarker_name] = {
                                'min': float(min_val),
                                'max': float(max_val),
                                'unit': ref_range.get('unit', ''),
                                'source': ref_range.get('source', 'lab')
                            }
                            logger.debug(f"[Orchestrator] Preserved input reference range for {biomarker_name}: {input_reference_ranges[biomarker_name]}")
                else:
                    simple_biomarkers[biomarker_name] = biomarker_data

            # Step 1.5: Compute derived markers (RatioRegistry; lab-supplied wins; never overwrite)
            logger.info("Step 1.5: Computing derived markers")
            derived_result = compute(simple_biomarkers)
            derived_ratios_meta = {
                "ratio_registry_version": derived_result.get("registry_version", RatioRegistry.version),
                "ratios": {},
            }

            def _ratio_unit(rid: str) -> str:
                return "mmol/L" if rid == "non_hdl_cholesterol" else "ratio"

            for ratio_id, entry in derived_result.get("derived", {}).items():
                if not isinstance(entry, dict) or "value" not in entry:
                    continue
                val = entry.get("value")
                unit = entry.get("unit") or _ratio_unit(ratio_id)
                source = entry.get("source", "computed")
                bounds_applied = entry.get("bounds_applied", False)
                inputs_used = entry.get("inputs_used") or []

                if source == "lab":
                    # Lab-supplied: value already in simple_biomarkers; never overwrite
                    ref = input_reference_ranges.get(ratio_id)
                    if ref is None and ratio_id in DERIVED_RATIO_BOUNDS:
                        bounds = DERIVED_RATIO_BOUNDS[ratio_id]
                        if isinstance(bounds.get("min"), (int, float)) and isinstance(bounds.get("max"), (int, float)):
                            input_reference_ranges[ratio_id] = {
                                "min": float(bounds["min"]),
                                "max": float(bounds["max"]),
                                "unit": unit,
                                "source": "ratio_registry",
                            }
                            ref = input_reference_ranges[ratio_id]
                    bounds_applied = ref is not None and isinstance(ref.get("min"), (int, float)) and isinstance(ref.get("max"), (int, float))
                else:
                    # Computed: merge only if key doesn't exist
                    if ratio_id not in simple_biomarkers:
                        simple_biomarkers[ratio_id] = val
                        filtered_biomarkers[ratio_id] = {
                            "value": val,
                            "unit": unit,
                            "reference_range": None,
                        }
                        bounds = DERIVED_RATIO_BOUNDS.get(ratio_id)
                        bounds_valid = bounds and isinstance(bounds.get("min"), (int, float)) and isinstance(bounds.get("max"), (int, float))
                        if bounds_valid:
                            filtered_biomarkers[ratio_id]["reference_range"] = {
                                **bounds, "unit": unit, "source": "ratio_registry",
                            }
                            if ratio_id not in input_reference_ranges:
                                input_reference_ranges[ratio_id] = {
                                    "min": float(bounds["min"]),
                                    "max": float(bounds["max"]),
                                    "unit": unit,
                                    "source": "ratio_registry",
                                }
                        bounds_applied = bool(bounds_valid)

                derived_ratios_meta["ratios"][ratio_id] = {
                    "value": val,
                    "unit": unit,
                    "source": source,
                    "bounds_applied": bounds_applied,
                    "inputs_used": inputs_used if source == "computed" else None,
                }

            # Step 2: Score biomarkers using the scoring engine with input reference ranges
            logger.info("Step 2: Scoring biomarkers")
            scoring_result = self.score_biomarkers(
                biomarkers=simple_biomarkers,
                age=user.get('age'),
                sex=user.get('gender'),
                lifestyle_data=user.get('lifestyle_factors', {}),
                input_reference_ranges=input_reference_ranges
            )
            
            # Step 3: Create analysis context for clustering and insights
            logger.info("Step 3: Creating analysis context")
            context = self.create_analysis_context(
                analysis_id=analysis_id,
                raw_biomarkers=filtered_biomarkers,
                user_data=user,
                assume_canonical=True
            )
            
            # Step 4: Cluster biomarkers
            logger.info("Step 4: Clustering biomarkers")
            clustering_result = self.cluster_biomarkers(
                context=context,
                scoring_result=scoring_result,
                lifestyle_data=user.get('lifestyle_factors', {})
            )
            
            # Step 4.5: Evaluate biomarker criticality (Sprint 3)
            logger.info("Step 4.5: Evaluating criticality")
            available_biomarkers = set(filtered_biomarkers.keys())
            criticality_result = evaluate_criticality(scoring_result, available_biomarkers)

            # Step 4.6: Build InsightGraph_v1 (Sprint 7) — sole LLM input
            logger.info("Step 4.6: Building InsightGraph")
            insight_graph = build_insight_graph_v1(
                analysis_id=analysis_id,
                scoring_result=scoring_result,
                clustering_result=clustering_result,
                criticality_result=criticality_result,
                derived_ratios_meta=derived_ratios_meta,
                input_reference_ranges=input_reference_ranges,
                filtered_biomarkers=filtered_biomarkers,
                context=context,
                lab_origin=user.get("lab_origin") if isinstance(user.get("lab_origin"), dict) else None,
                unit_normalisation_meta=unit_meta,
            )

            # Step 4.65: v5.3 Sprint 1 longitudinal state transitions (code-only)
            linked_snapshot_ids: List[str] = []
            fixture_mode = os.getenv("HEALTHIQ_MODE", "").strip().lower() in {"fixture", "fixtures"}
            user_id = user.get("user_id")
            if self.db_session is not None and user_id:
                try:
                    linked = link_prior_snapshot_insight_graphs(
                        db_session=self.db_session,
                        user_id=user_id,
                        current_analysis_id=analysis_id,
                    )
                    stamp, transitions = build_state_transition_v1(
                        current_insight_graph=insight_graph,
                        prior_insight_graphs=linked.prior_insight_graphs,
                    )
                    insight_graph.state_transition_version = stamp.state_transition_version
                    insight_graph.state_transition_hash = stamp.state_transition_hash
                    insight_graph.state_transitions = transitions
                    linked_snapshot_ids = linked.linked_snapshot_ids
                except Exception as exc:
                    if not fixture_mode:
                        raise ValueError(f"Snapshot linking failed: {exc}") from exc
                    logger.warning("Fixture mode soft-fail for snapshot linking: %s", exc)

            # Step 4.66: v5.3 Sprint 2 system-level state engine (code-only)
            try:
                system_states, state_engine_stamp = build_state_engine_v1(insight_graph)
                insight_graph.system_states = system_states
                insight_graph.state_engine_version = state_engine_stamp.state_engine_version
                insight_graph.state_engine_hash = state_engine_stamp.state_engine_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"State engine build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for state engine: %s", exc)

            # Step 4.67: v5.3 Sprint 3 interaction precedence arbitration (code-only)
            try:
                precedence_output, precedence_stamp = build_precedence_v1(insight_graph)
                insight_graph.precedence_output = precedence_output
                insight_graph.precedence_engine_version = precedence_stamp.precedence_engine_version
                insight_graph.precedence_engine_hash = precedence_stamp.precedence_engine_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"Precedence engine build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for precedence engine: %s", exc)

            # Step 4.68: v5.3 Sprint 4 causal layer ordering (code-only)
            try:
                causal_edges, causal_stamp = build_causal_layer_v1(insight_graph)
                insight_graph.causal_edges = causal_edges
                insight_graph.causal_layer_version = causal_stamp.causal_layer_version
                insight_graph.causal_layer_hash = causal_stamp.causal_layer_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"Causal layer build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for causal layer: %s", exc)

            # Step 4.70: v5.3 Sprint 7 arbitration depth (conflicts + dominance + causal + arbitration)
            try:
                conflict_set = build_conflict_set_v1(insight_graph)
                dominance_edges = build_dominance_edges_v1(insight_graph, conflict_set)
                causal_edges = build_causal_edges_v1(conflict_set, dominance_edges)
                primary_driver_system_id, arbitration_result, arbitration_stamp = build_arbitration_result_v1(
                    insight_graph=insight_graph,
                    conflicts=conflict_set,
                    dominance_edges=dominance_edges,
                    causal_edges=causal_edges,
                )
                insight_graph.conflict_set = conflict_set
                insight_graph.dominance_edges = dominance_edges
                insight_graph.causal_edges = causal_edges
                insight_graph.arbitration_result = arbitration_result
                insight_graph.primary_driver_system_id = primary_driver_system_id
                insight_graph.arbitration_version = arbitration_stamp.arbitration_version
                insight_graph.arbitration_hash = arbitration_stamp.arbitration_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"Arbitration depth build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for arbitration depth: %s", exc)

            # Step 4.71: v5.3 Sprint 8 calibration coupling from arbitration depth (code-only)
            try:
                calibration_items, calibration_stamp = build_calibration_layer_v1(
                    insight_graph,
                    apply_arbitration_coupling=True,
                )
                insight_graph.calibration_items = calibration_items
                insight_graph.calibration_version = calibration_stamp.calibration_version
                insight_graph.calibration_hash = calibration_stamp.calibration_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"Calibration layer build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for calibration layer: %s", exc)

            # Step 4.7: Build ReplayManifest_v1 (Sprint 9) — determinism lock
            logger.info("Step 4.7: Building ReplayManifest")
            cluster_stamp = {}
            try:
                cluster_stamp = get_cluster_schema_version_stamp()
            except (FileNotFoundError, ValueError):
                pass
            replay_manifest = build_replay_manifest_v1(
                unit_registry_version=unit_meta.get("unit_registry_version", UNIT_REGISTRY_VERSION),
                ratio_registry_version=derived_ratios_meta.get("ratio_registry_version", RatioRegistry.version),
                cluster_schema_version=cluster_stamp.get("cluster_schema_version", ""),
                cluster_schema_hash=cluster_stamp.get("cluster_schema_hash", ""),
                insight_graph=insight_graph,
                confidence_model=getattr(insight_graph, "confidence", None),
                derived_markers_registry_version=derived_ratios_meta.get("ratio_registry_version"),
                relationship_registry_version=getattr(insight_graph, "relationship_registry_version", ""),
                relationship_registry_hash=getattr(insight_graph, "relationship_registry_hash", ""),
                scoring_policy_version=load_scoring_policy().stamp.scoring_policy_version,
                scoring_policy_hash=load_scoring_policy().stamp.scoring_policy_hash,
                evidence_registry_version=load_evidence_registry().stamp.evidence_registry_version,
                evidence_registry_hash=load_evidence_registry().stamp.evidence_registry_hash,
                state_transition_version=getattr(insight_graph, "state_transition_version", ""),
                state_transition_hash=getattr(insight_graph, "state_transition_hash", ""),
                state_engine_version=getattr(insight_graph, "state_engine_version", ""),
                state_engine_hash=getattr(insight_graph, "state_engine_hash", ""),
                precedence_engine_version=getattr(insight_graph, "precedence_engine_version", ""),
                precedence_engine_hash=getattr(insight_graph, "precedence_engine_hash", ""),
                causal_layer_version=getattr(insight_graph, "causal_layer_version", ""),
                causal_layer_hash=getattr(insight_graph, "causal_layer_hash", ""),
                calibration_version=getattr(insight_graph, "calibration_version", ""),
                calibration_hash=getattr(insight_graph, "calibration_hash", ""),
                conflict_registry_version=load_conflict_registry().stamp.conflict_registry_version,
                conflict_registry_hash=load_conflict_registry().stamp.conflict_registry_hash,
                arbitration_registry_version=load_arbitration_registry().stamp.arbitration_registry_version,
                arbitration_registry_hash=load_arbitration_registry().stamp.arbitration_registry_hash,
                arbitration_version=getattr(insight_graph, "arbitration_version", ""),
                arbitration_hash=getattr(insight_graph, "arbitration_hash", ""),
                linked_snapshot_ids=linked_snapshot_ids,
                analysis_result_version="1.0.0",
            )

            # Step 5: Synthesize insights (LLM receives only InsightGraph_v1)
            logger.info("Step 5: Synthesizing insights")
            insights_result = self._synthesize_from_insight_graph(
                context=context,
                insight_graph=insight_graph,
                lifestyle_profile=user.get('lifestyle_factors', {}) or {},
            )
            
            # Step 6: Build biomarker DTOs from scoring results
            logger.info("Step 6: Building biomarker DTOs")
            biomarker_dtos = []
            for system_name, system_score in scoring_result.get('health_system_scores', {}).items():
                for biomarker_score in system_score.get('biomarker_scores', []):
                    biomarker_name = biomarker_score['biomarker_name']
                    value = biomarker_score['value']
                    
                    # Extract biomarker metadata from context
                    biomarker_data = context.biomarker_panel.biomarkers.get(biomarker_name, {})
                    
                    # Get unit from resolver or context
                    unit = biomarker_data.get('unit', '') if isinstance(biomarker_data, dict) else ''
                    if not unit:
                        # Try to get canonical unit from resolver
                        try:
                            canonical_data = resolver.get_biomarker_metadata(biomarker_name)
                            unit = canonical_data.get('unit', '')
                        except Exception as e:
                            logger.warning(f"Could not resolve unit for {biomarker_name}: {e}")
                            unit = ''
                    
                    # Get reference range: Priority 1 = input, Priority 2 = SSOT
                    reference_range_dict = None
                    
                    # Priority 1: Check input reference ranges
                    if input_reference_ranges and biomarker_name in input_reference_ranges:
                        input_range = input_reference_ranges[biomarker_name]
                        if isinstance(input_range, dict) and input_range.get('min') is not None and input_range.get('max') is not None:
                            reference_range_dict = {
                                'min': input_range.get('min'),
                                'max': input_range.get('max'),
                                'unit': input_range.get('unit', unit),
                                'source': input_range.get('source', 'lab')
                            }
                            logger.debug(f"[DTO Builder] Using input reference range for {biomarker_name}: {reference_range_dict}")
                    
                    # Priority 2: Fall back to SSOT if input range not available
                    if reference_range_dict is None:
                        try:
                            ref_range = resolver.get_reference_range(
                                biomarker_name,
                                age=context.user.age,
                                sex=context.user.gender
                            )
                            if ref_range and ref_range.get('min') is not None and ref_range.get('max') is not None:
                                reference_range_dict = {
                                    'min': ref_range.get('min'),
                                    'max': ref_range.get('max'),
                                    'unit': ref_range.get('unit', unit),
                                    'source': 'ssot'
                                }
                                logger.debug(f"[DTO Builder] Using SSOT reference range for {biomarker_name}: {reference_range_dict}")
                        except Exception as e:
                            logger.warning(f"Could not resolve reference range for {biomarker_name}: {e}")
                    
                    # Use HAS v1 primitive for status (single source of truth)
                    if reference_range_dict and reference_range_dict.get('min') is not None and reference_range_dict.get('max') is not None:
                        status = frontend_status_from_value_and_range(
                            float(value),
                            float(reference_range_dict['min']),
                            float(reference_range_dict['max']),
                        )
                    else:
                        status = 'unknown'
                    logger.debug(f"[DTO Builder] {biomarker_name} unit resolved as: {unit}, ref_range: {reference_range_dict}, status: {status}")
                    
                    biomarker_dtos.append(BiomarkerScoreDTO(
                        biomarker_name=biomarker_name,
                        value=value,
                        unit=unit,
                        score=biomarker_score['score'] / 100.0,  # Convert to 0-1 scale
                        percentile=None,
                        status=status,
                        reference_range=reference_range_dict,
                        interpretation=f"Scored {biomarker_score['score']:.1f}/100"
                    ))
            
            # --- Include all original biomarkers, not just scored ones ---
            logger.debug("Adding unscored biomarkers to DTO output")
            all_biomarkers = {}
            for biomarker_name, biomarker_data in filtered_biomarkers.items():
                if isinstance(biomarker_data, dict):
                    all_biomarkers[biomarker_name] = biomarker_data.get('value', biomarker_data.get('measurement', 0))
                else:
                    all_biomarkers[biomarker_name] = biomarker_data

            scored_biomarker_names = {b.biomarker_name for b in biomarker_dtos}
            for biomarker_name, value in all_biomarkers.items():
                if biomarker_name not in scored_biomarker_names:
                    # Extract biomarker metadata from context
                    biomarker_data = context.biomarker_panel.biomarkers.get(biomarker_name)
                    
                    # Get unit: Priority 1 = input_reference_ranges, Priority 2 = BiomarkerValue, Priority 3 = dict, Priority 4 = SSOT
                    unit = ''
                    
                    # Priority 1: Unit from lab reference range if available
                    if input_reference_ranges and biomarker_name in input_reference_ranges:
                        input_range = input_reference_ranges[biomarker_name]
                        if isinstance(input_range, dict) and input_range.get('unit'):
                            unit = input_range.get('unit', '')
                            logger.debug(f"[Unscored] Using unit from input_reference_ranges for {biomarker_name}: {unit}")
                    
                    # Priority 2: Unit from BiomarkerValue object
                    if not unit and biomarker_data:
                        from core.models.biomarker import BiomarkerValue
                        if isinstance(biomarker_data, BiomarkerValue):
                            unit = biomarker_data.unit or ''
                            logger.debug(f"[Unscored] Using unit from BiomarkerValue for {biomarker_name}: {unit}")
                        elif isinstance(biomarker_data, dict):
                            unit = biomarker_data.get('unit', '')
                            logger.debug(f"[Unscored] Using unit from dict for {biomarker_name}: {unit}")
                    
                    # Priority 3: Fall back to SSOT resolver only if unit still empty
                    if not unit:
                        try:
                            canonical_data = resolver.get_biomarker_metadata(biomarker_name)
                            if canonical_data:
                                unit = canonical_data.get('unit', '')
                                logger.debug(f"[Unscored] Using unit from SSOT resolver for {biomarker_name}: {unit}")
                        except Exception as e:
                            logger.warning(f"[Unscored] Could not resolve unit for {biomarker_name}: {e}")
                    
                    # Get reference range: Priority 1 = input_reference_ranges (lab), Priority 2 = SSOT
                    reference_range_dict = None
                    
                    # Priority 1: ALWAYS use input_reference_ranges if present (lab range takes precedence)
                    if input_reference_ranges and biomarker_name in input_reference_ranges:
                        input_range = input_reference_ranges[biomarker_name]
                        if isinstance(input_range, dict):
                            min_val = input_range.get('min')
                            max_val = input_range.get('max')
                            # Validate that min and max are numeric and valid
                            if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)) and min_val < max_val:
                                # Use unit from lab range if available, otherwise use extracted unit
                                range_unit = input_range.get('unit', '') or unit
                                reference_range_dict = {
                                    'min': float(min_val),
                                    'max': float(max_val),
                                    'unit': range_unit,
                                    'source': input_range.get('source', 'lab')
                                }
                                logger.debug(f"[Unscored] Using lab reference range for {biomarker_name}: {reference_range_dict}")
                            else:
                                logger.warning(f"[Unscored] Invalid min/max in input_reference_ranges for {biomarker_name}: min={min_val}, max={max_val}")
                    
                    # Priority 2: Fall back to SSOT ONLY if no lab range was found
                    if reference_range_dict is None:
                        try:
                            ref_range = resolver.get_reference_range(
                                biomarker_name,
                                age=context.user.age,
                                sex=context.user.gender
                            )
                            if ref_range and isinstance(ref_range, dict):
                                min_val = ref_range.get('min')
                                max_val = ref_range.get('max')
                                if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)) and min_val < max_val:
                                    # Use SSOT unit, or fall back to extracted unit
                                    range_unit = ref_range.get('unit', '') or unit
                                    reference_range_dict = {
                                        'min': float(min_val),
                                        'max': float(max_val),
                                        'unit': range_unit,
                                        'source': 'ssot'
                                    }
                                    logger.debug(f"[Unscored] Using SSOT reference range for {biomarker_name}: {reference_range_dict}")
                                else:
                                    logger.warning(f"[Unscored] Invalid SSOT range for {biomarker_name}: min={min_val}, max={max_val}")
                            else:
                                logger.warning(f"[Unscored] No valid SSOT reference range for {biomarker_name}")
                        except Exception as e:
                            logger.warning(f"[Unscored] Could not resolve SSOT reference range for {biomarker_name}: {e}")
                    
                    # If both failed, use fallback structure
                    if reference_range_dict is None:
                        reference_range_dict = {
                            'min': None,
                            'max': None,
                            'unit': unit,
                            'source': 'lab'
                        }
                    
                    # Update unit to match reference_range unit if we have a lab range
                    # This ensures consistency: if source is 'lab', unit should match lab range unit
                    if reference_range_dict and reference_range_dict.get('source') == 'lab' and reference_range_dict.get('unit'):
                        unit = reference_range_dict.get('unit', unit)
                        logger.debug(f"[Unscored] Updated unit to match lab range unit for {biomarker_name}: {unit}")
                    
                    # Determine status and score using HAS primitives + scoring (single source)
                    status = "unknown"
                    score = 0.0
                    if reference_range_dict and reference_range_dict.get('min') is not None and reference_range_dict.get('max') is not None:
                        try:
                            min_val = float(reference_range_dict['min'])
                            max_val = float(reference_range_dict['max'])
                            status = frontend_status_from_value_and_range(float(value), min_val, max_val)
                            score_raw, _ = self.scoring_engine.rules._calculate_score_from_range(
                                float(value), min_val, max_val
                            )
                            score = score_raw / 100.0  # Convert to 0-1 scale
                        except Exception as e:
                            logger.warning(f"Could not score unscored biomarker {biomarker_name} using reference range: {e}")
                    
                    logger.debug(f"Added unscored biomarker: {biomarker_name} value={value} unit={unit} range={reference_range_dict} status={status} score={score}")
                    
                    biomarker_dtos.append(BiomarkerScoreDTO(
                        biomarker_name=biomarker_name,
                        value=value,
                        unit=unit,
                        score=score,
                        percentile=None,
                        status=status,
                        reference_range=reference_range_dict,
                        interpretation="Scored using reference range" if status != "unknown" else "Not scored - no reference range available"
                    ))
            logger.info(f"Total biomarkers in DTO: {len(biomarker_dtos)}")
            
            # Step 7: Build cluster DTOs
            logger.info("Step 7: Building cluster DTOs")
            cluster_dtos = []
            for cluster in clustering_result.get('clusters', []):
                cluster_dtos.append(ClusterHit(
                    cluster_id=cluster['cluster_id'],
                    name=cluster['name'],
                    biomarkers=cluster['biomarkers'],
                    confidence=cluster['confidence'],
                    severity=cluster['severity'],
                    description=cluster['description']
                ))
            
            # Step 8: Build insight DTOs
            logger.info("Step 8: Building insight DTOs")
            insight_dtos = []
            for insight in insights_result.get('insights', []):
                insight_dtos.append(InsightResult(
                    insight_id=insight['id'],
                    title=insight.get('summary', ''),
                    description=insight.get('summary', ''),
                    category=insight.get('category', 'general'),
                    confidence=insight.get('confidence', 0.5),
                    severity=insight.get('severity', 'info'),
                    biomarkers=insight.get('biomarkers_involved', []),
                    recommendations=insight.get('recommendations', [])
                ))
            
            # Step 9: Create final analysis DTO
            logger.info("Step 9: Creating final analysis DTO")
            meta = dict(criticality_result) if criticality_result else {}
            meta["derived_ratios"] = derived_ratios_meta
            try:
                meta.update(get_cluster_schema_version_stamp())
            except (FileNotFoundError, ValueError):
                pass
            meta["insight_graph"] = insight_graph.model_dump() if hasattr(insight_graph, "model_dump") else {}
            derived_markers = {
                "registry_version": derived_ratios_meta.get("ratio_registry_version"),
                "derived": derived_ratios_meta.get("ratios", {}),
            }
            result = AnalysisDTO(
                analysis_id=analysis_id,
                biomarkers=biomarker_dtos,
                clusters=cluster_dtos,
                insights=insight_dtos,
                status="completed",
                created_at=datetime.now(UTC).isoformat(),
                overall_score=scoring_result.get('overall_score', 0.0) / 100.0,  # Convert to 0-1 scale
                unmapped_biomarkers=unmapped_biomarkers,
                derived_markers=derived_markers,
                meta=meta,
                replay_manifest=replay_manifest.model_dump(),
            )
            
            logger.info(f"Analysis {analysis_id} completed successfully with {len(biomarker_dtos)} biomarkers, {len(cluster_dtos)} clusters, {len(insight_dtos)} insights")
            print("[TRACE] Orchestrator output biomarkers:", len(result.biomarkers))
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            # Return error result instead of crashing
            return AnalysisDTO(
                analysis_id=analysis_id,
                biomarkers=[],
                clusters=[],
                insights=[],
                status="error",
                created_at="1970-01-01T00:00:00+00:00",
                overall_score=0.0,
                replay_manifest={
                    "manifest_version": "1.0.0",
                    "failure_code": "analysis_pipeline_failed",
                    "failure_type": type(e).__name__,
                    "stage": "orchestrator.run",
                },
            )
