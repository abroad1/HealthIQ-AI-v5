"""
Multi-engine clustering orchestration for biomarker analysis.

This module provides the main clustering engine that combines results from
scoring engines using weighted combinations and rule-based clustering algorithms.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerCluster
from core.scoring.engine import ScoringResult, HealthSystemScore
from core.clustering.weights import EngineWeightingSystem, EngineType
from core.clustering.rules import ClusteringRuleEngine
from core.clustering.validation import ClusterValidator


class ClusteringAlgorithm(Enum):
    """Available clustering algorithms."""
    RULE_BASED = "rule_based"
    WEIGHTED_CORRELATION = "weighted_correlation"
    HEALTH_SYSTEM_GROUPING = "health_system_grouping"


@dataclass
class ClusteringResult:
    """Result of clustering analysis."""
    clusters: List[BiomarkerCluster]
    algorithm_used: ClusteringAlgorithm
    confidence_score: float  # 0-1
    validation_summary: Dict[str, Any]
    processing_time_ms: float


class ClusteringEngine:
    """Multi-engine clustering orchestration for biomarker analysis."""
    
    def __init__(self, 
                 weighting_system: Optional[EngineWeightingSystem] = None,
                 rule_engine: Optional[ClusteringRuleEngine] = None,
                 validator: Optional[ClusterValidator] = None):
        """
        Initialize the clustering engine.
        
        Args:
            weighting_system: Engine weighting system for score combination
            rule_engine: Rule-based clustering engine
            validator: Cluster validation engine
        """
        self.weighting_system = weighting_system or EngineWeightingSystem()
        self.rule_engine = rule_engine or ClusteringRuleEngine()
        self.validator = validator or ClusterValidator()
        self.algorithm = ClusteringAlgorithm.RULE_BASED
    
    def cluster_biomarkers(self, context: AnalysisContext, 
                          scoring_result) -> ClusteringResult:
        """
        Cluster biomarkers based on analysis context and scoring results.
        
        Args:
            context: Analysis context with biomarker data
            scoring_result: Results from scoring engines
            
        Returns:
            ClusteringResult with clusters and metadata
        """
        import time
        start_time = time.time()
        
        # Extract biomarker data
        biomarker_values = self._extract_biomarker_values(context)
        biomarker_scores = self._extract_biomarker_scores(scoring_result)
        
        # Apply clustering algorithm
        if self.algorithm == ClusteringAlgorithm.RULE_BASED:
            clusters = self._apply_rule_based_clustering(biomarker_values, biomarker_scores)
        elif self.algorithm == ClusteringAlgorithm.WEIGHTED_CORRELATION:
            clusters = self._apply_weighted_correlation_clustering(biomarker_values, biomarker_scores)
        elif self.algorithm == ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING:
            clusters = self._apply_health_system_grouping(scoring_result)
        else:
            clusters = []
        
        # Validate clusters
        validation_summary = self._validate_clusters(clusters)
        
        # Calculate overall confidence
        confidence_score = self._calculate_overall_confidence(clusters, validation_summary)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return ClusteringResult(
            clusters=clusters,
            algorithm_used=self.algorithm,
            confidence_score=confidence_score,
            validation_summary=validation_summary,
            processing_time_ms=processing_time
        )
    
    def _extract_biomarker_values(self, context: AnalysisContext) -> Dict[str, float]:
        """Extract biomarker values from analysis context."""
        biomarker_values = {}
        
        for biomarker_name, biomarker_value in context.biomarker_panel.biomarkers.items():
            if hasattr(biomarker_value, 'value'):
                try:
                    biomarker_values[biomarker_name] = float(biomarker_value.value)
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue
            else:
                try:
                    biomarker_values[biomarker_name] = float(biomarker_value)
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue
        
        return biomarker_values
    
    def _extract_biomarker_scores(self, scoring_result) -> Dict[str, float]:
        """Extract individual biomarker scores from scoring result."""
        biomarker_scores = {}
        
        # Handle both ScoringResult objects and dictionary formats
        if hasattr(scoring_result, 'health_system_scores'):
            # ScoringResult object
            for system_name, system_score in scoring_result.health_system_scores.items():
                for biomarker_score in system_score.biomarker_scores:
                    biomarker_scores[biomarker_score.biomarker_name] = biomarker_score.score
        elif isinstance(scoring_result, dict) and 'health_system_scores' in scoring_result:
            # Dictionary format from orchestrator
            for system_name, system_data in scoring_result['health_system_scores'].items():
                if 'biomarker_scores' in system_data:
                    for biomarker_score in system_data['biomarker_scores']:
                        biomarker_scores[biomarker_score['biomarker_name']] = biomarker_score['score']
        
        return biomarker_scores
    
    def _apply_rule_based_clustering(self, biomarker_values: Dict[str, float], 
                                   biomarker_scores: Dict[str, float]) -> List[BiomarkerCluster]:
        """Apply rule-based clustering algorithm."""
        return self.rule_engine.apply_rules(biomarker_values, biomarker_scores)
    
    def _apply_weighted_correlation_clustering(self, biomarker_values: Dict[str, float],
                                             biomarker_scores: Dict[str, float]) -> List[BiomarkerCluster]:
        """Apply weighted correlation-based clustering."""
        # Group biomarkers by health system
        health_system_groups = self._group_biomarkers_by_health_system(biomarker_values)
        
        clusters = []
        for system_name, biomarkers in health_system_groups.items():
            if len(biomarkers) >= 2:  # Minimum cluster size
                cluster = self._create_health_system_cluster(system_name, biomarkers, biomarker_scores)
                if cluster:
                    clusters.append(cluster)
        
        return clusters
    
    def _apply_health_system_grouping(self, scoring_result: ScoringResult) -> List[BiomarkerCluster]:
        """Apply health system-based grouping."""
        clusters = []
        
        for system_name, system_score in scoring_result.health_system_scores.items():
            if len(system_score.biomarker_scores) >= 2:  # Minimum cluster size
                biomarkers = [bs.biomarker_name for bs in system_score.biomarker_scores]
                cluster = self._create_health_system_cluster(
                    system_name, 
                    biomarkers, 
                    {bs.biomarker_name: bs.score for bs in system_score.biomarker_scores}
                )
                if cluster:
                    clusters.append(cluster)
        
        return clusters
    
    def _group_biomarkers_by_health_system(self, biomarker_values: Dict[str, float]) -> Dict[str, List[str]]:
        """Group biomarkers by their health system."""
        health_system_mapping = {
            "metabolic": ["glucose", "hba1c", "insulin", "homa_ir"],
            "cardiovascular": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "triglycerides"],
            "inflammatory": ["crp", "esr", "il6"],
            "kidney": ["creatinine", "bun", "egfr"],
            "liver": ["alt", "ast", "bilirubin", "alp"],
            "cbc": ["hemoglobin", "hematocrit", "wbc", "platelets"],
            "hormonal": ["tsh", "free_t4", "testosterone", "estradiol"],
            "nutritional": ["vitamin_d", "b12", "folate", "iron", "ferritin"]
        }
        
        grouped = {}
        for system, biomarkers in health_system_mapping.items():
            system_biomarkers = [b for b in biomarkers if b in biomarker_values]
            if system_biomarkers:
                grouped[system] = system_biomarkers
        
        return grouped
    
    def _create_health_system_cluster(self, system_name: str, biomarkers: List[str], 
                                    scores: Dict[str, float]) -> Optional[BiomarkerCluster]:
        """Create a cluster for a health system."""
        if len(biomarkers) < 2:
            return None
        
        # Calculate cluster metrics
        avg_score = sum(scores.get(b, 0.0) for b in biomarkers) / len(biomarkers)
        confidence = self._calculate_cluster_confidence(biomarkers, scores)
        
        # Determine severity
        if avg_score < 30:
            severity = "critical"
        elif avg_score < 50:
            severity = "high"
        elif avg_score < 70:
            severity = "moderate"
        elif avg_score < 85:
            severity = "mild"
        else:
            severity = "normal"
        
        cluster_id = f"{system_name}_{len(biomarkers)}_biomarkers"
        name = f"{system_name.title()} Health Pattern"
        
        description = f"{severity.title()} {system_name} health pattern affecting {', '.join(biomarkers[:3])}"
        if len(biomarkers) > 3:
            description += f" and {len(biomarkers) - 3} others"
        
        return BiomarkerCluster(
            cluster_id=cluster_id,
            name=name,
            biomarkers=biomarkers,
            description=description,
            severity=severity,
            confidence=confidence
        )
    
    def _calculate_cluster_confidence(self, biomarkers: List[str], scores: Dict[str, float]) -> float:
        """Calculate confidence score for a cluster."""
        if not biomarkers:
            return 0.0
        
        # Base confidence on score consistency
        score_values = [scores.get(b, 0.0) for b in biomarkers]
        if not score_values:
            return 0.0
        
        # Calculate score variance (lower variance = higher confidence)
        mean_score = sum(score_values) / len(score_values)
        variance = sum((score - mean_score) ** 2 for score in score_values) / len(score_values)
        
        # Convert variance to confidence (0-1)
        max_variance = 2500  # Maximum possible variance for 0-100 scores
        confidence = max(0.0, 1.0 - (variance / max_variance))
        
        # Boost confidence for larger clusters
        size_boost = min(0.2, len(biomarkers) * 0.05)
        confidence = min(1.0, confidence + size_boost)
        
        return confidence
    
    def _validate_clusters(self, clusters: List[BiomarkerCluster]) -> Dict[str, Any]:
        """Validate cluster quality."""
        if not clusters:
            return {"total_clusters": 0, "valid_clusters": 0, "is_valid": True}
        
        # Convert clusters to validation format
        cluster_data = []
        for cluster in clusters:
            cluster_data.append({
                "cluster_id": cluster.cluster_id,
                "biomarkers": cluster.biomarkers,
                "scores": {}  # Will be filled by validator if needed
            })
        
        return self.validator.validate_cluster_set(cluster_data)
    
    def _calculate_overall_confidence(self, clusters: List[BiomarkerCluster], 
                                    validation_summary: Dict[str, Any]) -> float:
        """Calculate overall confidence score."""
        if not clusters:
            return 0.0
        
        # Base confidence on cluster individual confidence scores
        avg_cluster_confidence = sum(cluster.confidence for cluster in clusters) / len(clusters)
        
        # Adjust based on validation results
        validation_penalty = 0.0
        if not validation_summary.get("is_valid", True):
            validation_penalty = 0.2
        
        # Adjust based on cluster count (optimal range)
        cluster_count = len(clusters)
        if cluster_count < 2 or cluster_count > 6:
            validation_penalty += 0.1
        
        return max(0.0, avg_cluster_confidence - validation_penalty)
    
    def set_clustering_algorithm(self, algorithm: ClusteringAlgorithm) -> None:
        """
        Set the clustering algorithm to use.
        
        Args:
            algorithm: Clustering algorithm to use
        """
        self.algorithm = algorithm
    
    def get_clustering_parameters(self) -> Dict[str, Any]:
        """
        Get current clustering parameters.
        
        Returns:
            Dictionary of clustering parameters
        """
        return {
            "algorithm": self.algorithm.value,
            "weighting_system": self.weighting_system.get_weight_summary(),
            "rule_count": len(self.rule_engine.get_rule_names()),
            "validation_thresholds": {
                "min_cluster_size": self.validator.min_cluster_size,
                "min_coherence_threshold": self.validator.min_coherence_threshold,
                "max_cluster_size": self.validator.max_cluster_size
            }
        }
    
    def set_clustering_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set clustering parameters.
        
        Args:
            parameters: Dictionary of clustering parameters
        """
        if "algorithm" in parameters:
            try:
                self.algorithm = ClusteringAlgorithm(parameters["algorithm"])
            except ValueError:
                pass  # Invalid algorithm, keep current
        
        if "validation_thresholds" in parameters:
            self.validator.set_validation_thresholds(**parameters["validation_thresholds"])
    
    def apply_clinical_priority(self, priority_engines: List[str]) -> None:
        """
        Apply clinical priority to specific engines.
        
        Args:
            priority_engines: List of engine names to prioritize
        """
        engine_types = []
        for engine_name in priority_engines:
            try:
                engine_type = EngineType(engine_name)
                engine_types.append(engine_type)
            except ValueError:
                pass  # Skip invalid engine names
        
        if engine_types:
            self.weighting_system.apply_clinical_priority(engine_types)
    
    def get_clustering_summary(self, result: ClusteringResult) -> Dict[str, Any]:
        """
        Get summary of clustering results.
        
        Args:
            result: Clustering result
            
        Returns:
            Dictionary with clustering summary
        """
        return {
            "total_clusters": len(result.clusters),
            "algorithm_used": result.algorithm_used.value,
            "confidence_score": result.confidence_score,
            "processing_time_ms": result.processing_time_ms,
            "validation_summary": result.validation_summary,
            "cluster_summary": [
                {
                    "cluster_id": cluster.cluster_id,
                    "name": cluster.name,
                    "biomarker_count": len(cluster.biomarkers),
                    "severity": cluster.severity,
                    "confidence": cluster.confidence
                }
                for cluster in result.clusters
            ]
        }
