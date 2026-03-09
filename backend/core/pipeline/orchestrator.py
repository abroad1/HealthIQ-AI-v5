"""
Analysis orchestrator - enforces canonical-only keys and coordinates analysis.
"""

import hashlib
import json
import os
import subprocess
from datetime import date
from typing import Dict, Any, List, Mapping, Optional, Tuple

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
from core.clustering.cluster_schema_loader import get_cluster_schema_version_stamp
from core.analytics.insight_graph_builder import build_insight_graph_v1
from core.analytics.replay_manifest_builder import build_replay_manifest_v1
from core.analytics.explainability_builder import (
    build_explainability_report_v1,
    assert_single_authority_driver,
)
from core.analytics.bio_stats_engine import build_bio_stats_v1, BIO_STATS_ENGINE_VERSION
from core.analytics.system_burden_engine import (
    SYSTEM_BURDEN_ENGINE_VERSION,
    load_burden_registry,
    audit_burden_registry_system_ids,
    audit_risk_direction_registry,
    build_raw_system_burden_v1,
)
from core.analytics.influence_propagator import propagate_influence_v1, INFLUENCE_PROPAGATOR_VERSION
from core.analytics.capacity_scaler import scale_capacity_scores_v1, CAPACITY_SCALER_VERSION
from core.analytics.validation_gate import (
    run_validation_gate_v1,
    compute_burden_hash,
    VALIDATION_GATE_VERSION,
)
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
from core.scoring.rules import DERIVED_RATIO_POLICY_BOUNDS


class AnalysisOrchestrator:
    """Orchestrates biomarker analysis with canonical enforcement."""
    
    def __init__(
        self,
        normalizer: Optional[BiomarkerNormalizer] = None,
        db_session: Any = None,
        allow_llm: Optional[bool] = None,
    ):
        """
        Initialize the orchestrator.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
            db_session: Optional DB session for longitudinal snapshot linking
            allow_llm: Explicit runtime gate for LLM usage in insight synthesis.
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
        self.insight_synthesizer = InsightSynthesizer(allow_llm=allow_llm)
    
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
        mode = os.getenv("HEALTHIQ_MODE", "").strip().lower()
        if mode not in {"fixture", "fixtures", "test"}:
            raise RuntimeError(
                "orchestrator.synthesize_insights() is fixture/test mode only in production use orchestrator.run()"
            )

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
        explainability_report: Any,
        lifestyle_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Sprint 7: Synthesize insights using InsightGraph only. Used by run()."""
        synthesis_result = self.insight_synthesizer.synthesize_insights(
            context=context,
            insight_graph=insight_graph,
            explainability_report=explainability_report,
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

    def _git_short_sha(self) -> str:
        try:
            out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
            return out.strip()
        except Exception:
            return ""

    def _system_biomarker_map(self, insight_graph: Any) -> Dict[str, List[str]]:
        cluster_summary = insight_graph.cluster_summary if isinstance(insight_graph.cluster_summary, dict) else {}
        clusters = cluster_summary.get("clusters", []) if isinstance(cluster_summary, dict) else []
        out: Dict[str, List[str]] = {}
        if not isinstance(clusters, list):
            return out
        for cluster in sorted(clusters, key=lambda c: str((c or {}).get("cluster_id", ""))):
            if not isinstance(cluster, dict):
                continue
            system_id = str(cluster.get("cluster_id", "")).strip()
            if not system_id:
                continue
            biomarkers = cluster.get("biomarkers", [])
            if not isinstance(biomarkers, list):
                biomarkers = []
            out[system_id] = sorted({str(b).strip() for b in biomarkers if str(b).strip()})
        return out

    def _extract_biomarker_value(self, row: Any) -> Optional[float]:
        if isinstance(row, dict):
            raw = row.get("value", row.get("measurement"))
        else:
            raw = row
        if isinstance(raw, (int, float)):
            return float(raw)
        return None

    def run(
        self,
        biomarkers: Mapping[str, Any],
        user: Mapping[str, Any],
        *,
        assume_canonical: bool = False,
        lifestyle_inputs: Optional[Dict[str, Any]] = None,
        questionnaire_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Run the complete analysis pipeline: scoring → clustering → insights.

        Args:
            biomarkers: Canonical biomarker data (must be unit-normalised; carry __unit_normalisation_meta__)
            user: User data
            lifestyle_inputs: Optional Layer 2 lifestyle inputs (UK canonical). When provided, applies
                LifestyleModifierEngine to system burdens and attaches lifestyle artifact.
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
            # KB-S11: inject age from questionnaire date_of_birth for fib_4 computation
            dob = (questionnaire_data or {}).get("date_of_birth")
            try:
                age = int((date.today() - date.fromisoformat(dob)).days / 365.25) if dob else None
            except (ValueError, TypeError):
                age = None
            simple_biomarkers["age"] = age
            derived_result = compute(simple_biomarkers)
            derived_ratios_meta = {
                "ratio_registry_version": derived_result.get("registry_version", RatioRegistry.version),
                "ratios": {},
            }
            policy_bounds_rejected_reason: Dict[str, str] = {}

            def _ratio_unit(rid: str) -> str:
                return "mmol/L" if rid == "non_hdl_cholesterol" else "ratio"

            def _has_valid_numeric_bounds(ref: Any) -> bool:
                if not isinstance(ref, dict):
                    return False
                min_val = ref.get("min")
                max_val = ref.get("max")
                return (
                    isinstance(min_val, (int, float))
                    and isinstance(max_val, (int, float))
                    and float(min_val) < float(max_val)
                )

            def _is_valid_lab_range(ref: Any) -> bool:
                if not _has_valid_numeric_bounds(ref):
                    return False
                return str(ref.get("source", "")).strip().lower() == "lab"

            def _policy_bounds_for_ratio(rid: str, expected_unit: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
                bounds = DERIVED_RATIO_POLICY_BOUNDS.get(rid)
                if not isinstance(bounds, dict):
                    return None, "policy_bounds_missing"
                min_val = bounds.get("min")
                max_val = bounds.get("max")
                policy_unit = str(bounds.get("unit", "")).strip()
                if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)) or float(min_val) >= float(max_val):
                    return None, "policy_bounds_invalid"
                if not policy_unit:
                    return None, "policy_unit_missing"
                expected = str(expected_unit or "").strip()
                unit_compatible = (
                    (policy_unit == expected)
                    or (policy_unit == "ratio" and expected == "ratio")
                )
                if not unit_compatible:
                    return None, f"policy_unit_mismatch:{policy_unit}!={expected}"
                return {
                    "min": float(min_val),
                    "max": float(max_val),
                    "unit": policy_unit,
                    "source": "ratio_registry",
                }, None

            for ratio_id, entry in derived_result.get("derived", {}).items():
                if not isinstance(entry, dict) or "value" not in entry:
                    continue
                val = entry.get("value")
                unit = entry.get("unit") or _ratio_unit(ratio_id)
                source = entry.get("source", "computed")
                bounds_applied = entry.get("bounds_applied", False)
                inputs_used = entry.get("inputs_used") or []

                if source == "lab":
                    # Lab-supplied: value already in simple_biomarkers; never overwrite.
                    # Only inject policy bounds when no valid lab range exists.
                    ref = input_reference_ranges.get(ratio_id)
                    if not _is_valid_lab_range(ref):
                        policy_ref, policy_reason = _policy_bounds_for_ratio(ratio_id, unit)
                        if policy_ref is not None:
                            input_reference_ranges[ratio_id] = policy_ref
                            ref = policy_ref
                        elif policy_reason:
                            policy_bounds_rejected_reason[ratio_id] = policy_reason
                    bounds_applied = _has_valid_numeric_bounds(ref)
                else:
                    # Computed: merge only if key doesn't exist
                    if ratio_id not in simple_biomarkers:
                        simple_biomarkers[ratio_id] = val
                        filtered_biomarkers[ratio_id] = {
                            "value": val,
                            "unit": unit,
                            "reference_range": None,
                        }
                        existing_range = input_reference_ranges.get(ratio_id)
                        if not _is_valid_lab_range(existing_range):
                            policy_ref, policy_reason = _policy_bounds_for_ratio(ratio_id, unit)
                            if policy_ref is not None:
                                filtered_biomarkers[ratio_id]["reference_range"] = {
                                    "min": policy_ref["min"],
                                    "max": policy_ref["max"],
                                    "unit": policy_ref["unit"],
                                    "source": "ratio_registry",
                                }
                                input_reference_ranges[ratio_id] = policy_ref
                            elif policy_reason:
                                policy_bounds_rejected_reason[ratio_id] = policy_reason
                        bounds_applied = _has_valid_numeric_bounds(input_reference_ranges.get(ratio_id))

                derived_ratios_meta["ratios"][ratio_id] = {
                    "value": val,
                    "unit": unit,
                    "source": source,
                    "bounds_applied": bounds_applied,
                    "bounds_source": (
                        str((input_reference_ranges.get(ratio_id) or {}).get("source", "")).strip()
                        if _has_valid_numeric_bounds(input_reference_ranges.get(ratio_id))
                        else None
                    ),
                    "bounds_rejected_reason": policy_bounds_rejected_reason.get(ratio_id),
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
                questionnaire_data=questionnaire_data,
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
            runtime_mode = os.getenv("HEALTHIQ_MODE", "").strip().lower()
            fixture_mode = runtime_mode in {"fixture", "fixtures"}
            soft_mode = fixture_mode or runtime_mode == "test"
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

            # Step 4.69: baseline calibration prior to arbitration weighting (code-only)
            try:
                calibration_items, calibration_stamp = build_calibration_layer_v1(
                    insight_graph,
                    apply_arbitration_coupling=False,
                )
                insight_graph.calibration_items = calibration_items
                insight_graph.calibration_version = calibration_stamp.calibration_version
                insight_graph.calibration_hash = calibration_stamp.calibration_hash
            except Exception as exc:
                if not fixture_mode:
                    raise ValueError(f"Calibration baseline build failed: {exc}") from exc
                logger.warning("Fixture mode soft-fail for calibration baseline: %s", exc)

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

            # Step 4.72: Build ExplainabilityReport_v1 from final mutated InsightGraph.
            run_id = analysis_id
            generated_at_utc = datetime.now(UTC).isoformat()
            git_commit_short = self._git_short_sha()
            conflict_stamp = load_conflict_registry().stamp
            arbitration_registry_stamp = load_arbitration_registry().stamp
            if not str(getattr(insight_graph, "primary_driver_system_id", "")).strip() and soft_mode:
                system_ids = sorted(
                    {
                        str(node.system_id).strip()
                        for node in (getattr(insight_graph, "system_states", []) or [])
                        if str(getattr(node, "system_id", "")).strip()
                    }
                )
                if system_ids:
                    insight_graph.primary_driver_system_id = system_ids[0]
                    if not getattr(insight_graph.arbitration_result, "supporting_system_ids", None):
                        insight_graph.arbitration_result.supporting_system_ids = system_ids[1:]
            explainability_report = build_explainability_report_v1(
                insight_graph,
                run_id=run_id,
                git_commit_short=git_commit_short,
                generated_at_utc=generated_at_utc,
                conflict_registry_version=conflict_stamp.conflict_registry_version,
                conflict_registry_hash=conflict_stamp.conflict_registry_hash,
                arbitration_registry_version=arbitration_registry_stamp.arbitration_registry_version,
                arbitration_registry_hash=arbitration_registry_stamp.arbitration_registry_hash,
                arbitration_version=getattr(insight_graph, "arbitration_version", ""),
                arbitration_hash=getattr(insight_graph, "arbitration_hash", ""),
            )
            insight_graph_driver = str(getattr(insight_graph, "primary_driver_system_id", "") or "")
            explainability_driver = str(explainability_report.arbitration_decisions.primary_driver_system_id or "")
            if insight_graph_driver != explainability_driver:
                raise ValueError(
                    "Single-authority primary driver mismatch between insight graph and explainability report"
                )

            # Step 4.73: Sprint 13 deterministic burden/capacity engines (direction-aware, calibration-neutral)
            system_to_biomarkers_full = self._system_biomarker_map(insight_graph)
            burden_registry_rows = load_burden_registry()
            audit_burden_registry_system_ids(registry_rows=burden_registry_rows)
            measured_biomarkers: Dict[str, Any] = {}
            measured_ranges: Dict[str, Dict[str, Any]] = {}
            for biomarker_id in sorted(str(k) for k in filtered_biomarkers.keys()):
                if biomarker_id not in burden_registry_rows:
                    continue
                if biomarker_id not in filtered_biomarkers:
                    continue
                value = self._extract_biomarker_value(filtered_biomarkers[biomarker_id])
                if value is None:
                    continue
                ref = input_reference_ranges.get(biomarker_id, {})
                if not isinstance(ref, dict):
                    continue
                low = ref.get("min")
                high = ref.get("max")
                if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
                    continue
                measured_biomarkers[biomarker_id] = {"value": float(value)}
                measured_ranges[biomarker_id] = {"min": float(low), "max": float(high)}

            audited_registry = audit_risk_direction_registry(
                required_biomarkers=sorted(measured_biomarkers.keys()),
                registry_rows=burden_registry_rows,
            )
            biomarker_stats = build_bio_stats_v1(
                biomarker_values=measured_biomarkers,
                lab_reference_ranges=measured_ranges,
            )
            system_to_biomarkers: Dict[str, List[str]] = {}
            for system_id, biomarker_ids in sorted(system_to_biomarkers_full.items()):
                system_to_biomarkers[system_id] = sorted(
                    [bid for bid in biomarker_ids if bid in biomarker_stats]
                )
            covered_biomarkers = {
                bid for rows in system_to_biomarkers.values() for bid in rows
            }
            for biomarker_id in sorted(biomarker_stats.keys()):
                if biomarker_id in covered_biomarkers:
                    continue
                row = burden_registry_rows.get(biomarker_id, {})
                system_id = str(row.get("system", "")).strip() if isinstance(row, dict) else ""
                if not system_id:
                    raise ValueError(
                        f"system_burden_engine: missing system for scored biomarker {biomarker_id}"
                    )
                system_to_biomarkers.setdefault(system_id, [])
                system_to_biomarkers[system_id].append(biomarker_id)
            for system_id in sorted(system_to_biomarkers.keys()):
                system_to_biomarkers[system_id] = sorted(set(system_to_biomarkers[system_id]))
            has_scorable_inputs = bool(biomarker_stats) and any(
                bool(bids) for bids in system_to_biomarkers.values()
            )
            lifestyle_artifact: Optional[Dict[str, Any]] = None
            lifestyle_input_hash_value: Optional[str] = None
            if not has_scorable_inputs:
                # Deterministic not-computed contract when no range-qualified biomarkers are available.
                raw_system_burden_vector = {}
                adjusted_system_burden_vector = {}
                burden_path_distances = {}
                system_capacity_scores = {}
                burden_hash = compute_burden_hash(
                    adjusted_system_burden_vector=adjusted_system_burden_vector,
                    system_capacity_scores=system_capacity_scores,
                )
                validation_result = run_validation_gate_v1(
                    insight_graph_system_ids=[],
                    primary_driver_system_id="",
                    supporting_systems=[],
                    influence_order=[],
                    path_distances={},
                    adjusted_system_burden_vector={},
                    system_capacity_scores={},
                    burden_hash=burden_hash,
                )
            else:
                raw_system_burden_vector = build_raw_system_burden_v1(
                    system_to_biomarkers=system_to_biomarkers,
                    biomarker_stats=biomarker_stats,
                    audited_registry=audited_registry,
                )
                for node in sorted(getattr(insight_graph, "system_states", []), key=lambda n: n.system_id):
                    node_system_id = str(getattr(node, "system_id", "")).strip()
                    if node_system_id and node_system_id != "unknown":
                        raw_system_burden_vector.setdefault(node_system_id, 0.0)
                burden_driver_system_id = ""
                if insight_graph_driver and insight_graph_driver != "unknown":
                    burden_driver_system_id = insight_graph_driver
                elif raw_system_burden_vector:
                    burden_driver_system_id = sorted(str(k) for k in raw_system_burden_vector.keys())[0]
                else:
                    raise ValueError(
                        "influence_propagator: no scored systems available to establish burden propagation driver"
                    )
                if burden_driver_system_id not in raw_system_burden_vector:
                    raw_system_burden_vector[burden_driver_system_id] = 0.0
                adjusted_system_burden_vector, burden_path_distances = propagate_influence_v1(
                    raw_system_burden_vector=raw_system_burden_vector,
                    primary_driver_system_id=burden_driver_system_id,
                    causal_edges=[
                        edge.model_dump() if hasattr(edge, "model_dump") else edge
                        for edge in (getattr(insight_graph, "causal_edges", []) or [])
                    ],
                )
                # Sprint 20: Lifestyle modifier integration (Layer 2)
                lifestyle_adjusted_systems: set = set()
                effective_lifestyle_inputs = lifestyle_inputs or user.get("lifestyle_inputs")
                if effective_lifestyle_inputs and isinstance(effective_lifestyle_inputs, dict) and effective_lifestyle_inputs:
                    # Intentional lazy-load: lifestyle modules only when lifestyle_inputs provided.
                    from core.analytics.lifestyle_registry_loader import load_lifestyle_registry
                    from core.analytics.lifestyle_modifier_engine import LifestyleModifierEngine
                    registry = load_lifestyle_registry()
                    engine = LifestyleModifierEngine(registry)
                    engine_result = engine.apply(
                        dict(adjusted_system_burden_vector),
                        effective_lifestyle_inputs,
                    )
                    lifestyle_adjusted_systems = set(engine_result["adjusted_system_burdens"].keys())
                    for system, adj_data in engine_result["adjusted_system_burdens"].items():
                        adjusted_system_burden_vector[system] = adj_data["adjusted_burden"]
                    lifestyle_artifact = {
                        "derived_inputs": engine_result["derived_inputs"],
                        "system_modifiers": engine_result["system_modifiers"],
                        "confidence_adjustments": {
                            s: engine_result["adjusted_system_burdens"][s]["confidence_penalty"]
                            for s in sorted(engine_result["adjusted_system_burdens"].keys())
                        },
                    }
                    lifestyle_input_hash_value = hashlib.sha256(
                        json.dumps(effective_lifestyle_inputs, sort_keys=True, ensure_ascii=True).encode("utf-8")
                    ).hexdigest()
                system_capacity_scores = scale_capacity_scores_v1(
                    adjusted_system_burden_vector=adjusted_system_burden_vector
                )
                burden_hash = compute_burden_hash(
                    adjusted_system_burden_vector=adjusted_system_burden_vector,
                    system_capacity_scores=system_capacity_scores,
                )
                validation_system_ids = sorted(
                    {
                        str(node.system_id)
                        for node in (getattr(insight_graph, "system_states", []) or [])
                    }
                    | {str(k) for k in system_capacity_scores.keys()}
                )
                if soft_mode and not validation_system_ids:
                    validation_system_ids = sorted(system_capacity_scores.keys())
                validation_result = run_validation_gate_v1(
                    insight_graph_system_ids=validation_system_ids,
                    primary_driver_system_id=insight_graph_driver,
                    supporting_systems=list(getattr(insight_graph, "supporting_systems", [])),
                    influence_order=list(getattr(insight_graph, "influence_order", [])),
                    path_distances=burden_path_distances,
                    adjusted_system_burden_vector=adjusted_system_burden_vector,
                    system_capacity_scores=system_capacity_scores,
                    burden_hash=burden_hash,
                    allow_lifestyle_only_systems_without_influence_paths=lifestyle_adjusted_systems,
                )
                if validation_result.status != "PASS" and set(validation_result.violations) == {
                    "influence_order_not_descending_adjusted_burden"
                }:
                    burden_sorted_order = sorted(
                        [str(k) for k in adjusted_system_burden_vector.keys()],
                        key=lambda sid: (-float(adjusted_system_burden_vector[sid]), sid),
                    )
                    insight_graph.influence_order = burden_sorted_order
                    insight_graph.supporting_systems = [sid for sid in burden_sorted_order if sid != insight_graph_driver]
                    validation_result = run_validation_gate_v1(
                        insight_graph_system_ids=validation_system_ids,
                        primary_driver_system_id=insight_graph_driver,
                        supporting_systems=list(getattr(insight_graph, "supporting_systems", [])),
                        influence_order=list(getattr(insight_graph, "influence_order", [])),
                        path_distances=burden_path_distances,
                        adjusted_system_burden_vector=adjusted_system_burden_vector,
                        system_capacity_scores=system_capacity_scores,
                        burden_hash=burden_hash,
                        allow_lifestyle_only_systems_without_influence_paths=lifestyle_adjusted_systems,
                    )
                if validation_result.status != "PASS":
                    raise ValueError(f"validation_gate failed: {validation_result.violations}")

            insight_graph.bio_stats_engine_version = BIO_STATS_ENGINE_VERSION
            insight_graph.system_burden_engine_version = SYSTEM_BURDEN_ENGINE_VERSION
            insight_graph.influence_propagator_version = INFLUENCE_PROPAGATOR_VERSION
            insight_graph.capacity_scaler_version = CAPACITY_SCALER_VERSION
            insight_graph.validation_gate_version = VALIDATION_GATE_VERSION
            insight_graph.raw_system_burden_vector = {
                k: float(raw_system_burden_vector[k]) for k in sorted(raw_system_burden_vector.keys())
            }
            insight_graph.adjusted_system_burden_vector = {
                k: float(adjusted_system_burden_vector[k]) for k in sorted(adjusted_system_burden_vector.keys())
            }
            insight_graph.burden_path_distances = {
                k: (
                    -1.0
                    if burden_path_distances[k] == float("inf")
                    else float(burden_path_distances[k])
                )
                for k in sorted(burden_path_distances.keys())
            }
            insight_graph.system_capacity_scores = {
                k: int(system_capacity_scores[k]) for k in sorted(system_capacity_scores.keys())
            }
            insight_graph.burden_hash = burden_hash
            insight_graph.burden_validation_status = validation_result.status
            insight_graph.burden_validation_violations = list(validation_result.violations)

            # Rebuild explainability so burden vectors are replay-stamped in final report.
            explainability_report = build_explainability_report_v1(
                insight_graph,
                run_id=run_id,
                git_commit_short=git_commit_short,
                generated_at_utc=generated_at_utc,
                conflict_registry_version=conflict_stamp.conflict_registry_version,
                conflict_registry_hash=conflict_stamp.conflict_registry_hash,
                arbitration_registry_version=arbitration_registry_stamp.arbitration_registry_version,
                arbitration_registry_hash=arbitration_registry_stamp.arbitration_registry_hash,
                arbitration_version=getattr(insight_graph, "arbitration_version", ""),
                arbitration_hash=getattr(insight_graph, "arbitration_hash", ""),
                raw_system_burden_vector=insight_graph.raw_system_burden_vector,
                adjusted_system_burden_vector=insight_graph.adjusted_system_burden_vector,
                system_capacity_scores=insight_graph.system_capacity_scores,
                burden_validation_status=insight_graph.burden_validation_status,
                burden_validation_violations=insight_graph.burden_validation_violations,
                burden_hash=insight_graph.burden_hash,
            )
            explainability_driver = str(explainability_report.arbitration_decisions.primary_driver_system_id or "")
            if insight_graph_driver != explainability_driver:
                raise ValueError(
                    "Single-authority primary driver mismatch between insight graph and explainability report"
                )

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
                conflict_registry_version=conflict_stamp.conflict_registry_version,
                conflict_registry_hash=conflict_stamp.conflict_registry_hash,
                arbitration_registry_version=arbitration_registry_stamp.arbitration_registry_version,
                arbitration_registry_hash=arbitration_registry_stamp.arbitration_registry_hash,
                arbitration_version=getattr(insight_graph, "arbitration_version", ""),
                arbitration_hash=getattr(insight_graph, "arbitration_hash", ""),
                explainability_version=explainability_report.run_metadata.report_version,
                explainability_hash=explainability_report.replay_stamps.explainability_hash,
                explainability_artifact_filename="explainability_report.json",
                bio_stats_engine_version=getattr(insight_graph, "bio_stats_engine_version", ""),
                system_burden_engine_version=getattr(insight_graph, "system_burden_engine_version", ""),
                influence_propagator_version=getattr(insight_graph, "influence_propagator_version", ""),
                capacity_scaler_version=getattr(insight_graph, "capacity_scaler_version", ""),
                validation_gate_version=getattr(insight_graph, "validation_gate_version", ""),
                burden_hash=getattr(insight_graph, "burden_hash", ""),
                burden_artifact_filename="burden_vector.json",
                linked_snapshot_ids=linked_snapshot_ids,
                analysis_result_version="1.0.0",
                lifestyle_input_hash=lifestyle_input_hash_value,
            )

            # Step 5: Synthesize insights (LLM receives only InsightGraph_v1)
            logger.info("Step 5: Synthesizing insights")
            insights_result = self._synthesize_from_insight_graph(
                context=context,
                insight_graph=insight_graph,
                explainability_report=explainability_report,
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
                    
                    # Get reference range from input_reference_ranges only.
                    # Lab-Range Sovereignty: no SSOT fallback for scoring/display status paths.
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
                    range_source = None
                    if isinstance(reference_range_dict, dict):
                        source_val = str(reference_range_dict.get("source", "")).strip().lower()
                        if source_val in {"lab", "policy", "ssot"}:
                            range_source = source_val
                    
                    interpretation = f"Scored {biomarker_score['score']:.1f}/100"
                    if (
                        str(biomarker_score.get("unscored_reason", "")).strip()
                        or status == "unknown"
                        or not _has_valid_numeric_bounds(reference_range_dict)
                    ):
                        interpretation = "Not scored - no reference range available"

                    biomarker_dtos.append(BiomarkerScoreDTO(
                        biomarker_name=biomarker_name,
                        value=value,
                        unit=unit,
                        score=biomarker_score['score'] / 100.0,  # Convert to 0-1 scale
                        percentile=None,
                        status=status,
                        range_source=range_source,
                        reference_range=reference_range_dict,
                        interpretation=interpretation
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
                    
                    # Get reference range from input_reference_ranges only.
                    # Lab-Range Sovereignty: no SSOT fallback for scoring/display status paths.
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
                    
                    # If both failed, use fallback structure
                    if reference_range_dict is None:
                        fallback_source = "policy" if biomarker_name in policy_bounds_rejected_reason else None
                        reference_range_dict = {
                            'min': None,
                            'max': None,
                            'unit': unit,
                            'source': fallback_source,
                        }
                    
                    # Update unit to match reference_range unit if we have a lab range
                    # This ensures consistency: if source is 'lab', unit should match lab range unit
                    if reference_range_dict and reference_range_dict.get('source') == 'lab' and reference_range_dict.get('unit'):
                        unit = reference_range_dict.get('unit', unit)
                        logger.debug(f"[Unscored] Updated unit to match lab range unit for {biomarker_name}: {unit}")
                    
                    # Determine status and score using HAS primitives + scoring (single source)
                    status = "unknown"
                    score = 0.0
                    range_source = None
                    if isinstance(reference_range_dict, dict):
                        source_val = str(reference_range_dict.get("source", "")).strip().lower()
                        if source_val in {"lab", "policy", "ssot"}:
                            range_source = source_val
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
                    interpretation = "Not scored - no reference range available"
                    if status != "unknown":
                        if range_source == "policy":
                            interpretation = "Scored using HealthIQ fallback bounds (lab range not provided)"
                        elif range_source == "lab":
                            interpretation = "Scored using lab reference range"
                        else:
                            interpretation = "Scored using reference range"
                    elif biomarker_name in policy_bounds_rejected_reason:
                        interpretation = "Not scored - no compatible policy bounds"
                        if range_source is None:
                            range_source = "policy"
                    
                    biomarker_dtos.append(BiomarkerScoreDTO(
                        biomarker_name=biomarker_name,
                        value=value,
                        unit=unit,
                        score=score,
                        percentile=None,
                        status=status,
                        range_source=range_source,
                        reference_range=reference_range_dict,
                        interpretation=interpretation,
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
            exp_dump = explainability_report.model_dump() if hasattr(explainability_report, "model_dump") else {}
            if lifestyle_artifact is not None:
                exp_dump["lifestyle"] = lifestyle_artifact
            meta["explainability_report"] = exp_dump
            # Base system vectors must contain canonical systems only.
            # Derived diagnostic components are stored separately in derived_components.
            # Canonical system IDs are SSOT-derived from backend/ssot/system_burden_registry.yaml.
            canonical_ids = frozenset(
                str(row.get("system", "")).strip()
                for row in burden_registry_rows.values()
                if isinstance(row, dict) and str(row.get("system", "")).strip()
            )
            raw_full = dict(getattr(insight_graph, "raw_system_burden_vector", {}))
            adj_full = dict(getattr(insight_graph, "adjusted_system_burden_vector", {}))
            cap_full = dict(getattr(insight_graph, "system_capacity_scores", {}))
            raw_canonical = {k: float(v) for k, v in raw_full.items() if k in canonical_ids}
            adj_canonical = {k: float(v) for k, v in adj_full.items() if k in canonical_ids}
            cap_canonical = {k: int(v) for k, v in cap_full.items() if k in canonical_ids}
            derived_keys = sorted({k for k in raw_full.keys() | adj_full.keys() | cap_full.keys() if k not in canonical_ids})
            derived_components = {
                k: {
                    "raw": float(raw_full.get(k, 0.0)),
                    "adjusted": float(adj_full.get(k, 0.0)),
                    "capacity": int(cap_full.get(k, 100)),
                }
                for k in derived_keys
            }
            meta["burden_vector"] = {
                "raw_system_burden_vector": {k: raw_canonical[k] for k in sorted(raw_canonical.keys())},
                "adjusted_system_burden_vector": {k: adj_canonical[k] for k in sorted(adj_canonical.keys())},
                "system_capacity_scores": {k: cap_canonical[k] for k in sorted(cap_canonical.keys())},
                "derived_components": derived_components,
                "burden_hash": str(getattr(insight_graph, "burden_hash", "")),
                "validation_status": str(getattr(insight_graph, "burden_validation_status", "")),
                "validation_violations": list(getattr(insight_graph, "burden_validation_violations", [])),
            }
            analysis_primary_driver = insight_graph_driver
            assert_single_authority_driver(
                insight_graph_driver=insight_graph_driver,
                explainability_driver=explainability_driver,
                analysis_result_driver=analysis_primary_driver,
            )
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
                primary_driver_system_id=analysis_primary_driver,
                system_capacity_scores=dict(getattr(insight_graph, "system_capacity_scores", {})),
                burden_hash=str(getattr(insight_graph, "burden_hash", "")),
                unmapped_biomarkers=unmapped_biomarkers,
                derived_markers=derived_markers,
                meta=meta,
                replay_manifest=replay_manifest.model_dump(exclude_none=True),
                lifestyle=lifestyle_artifact,
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
