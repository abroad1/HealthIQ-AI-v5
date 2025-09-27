"""
Cluster quality validation and coherence checks for clustering analysis.

This module provides validation mechanisms to ensure cluster quality,
coherence, and statistical significance of clustering results.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class ValidationLevel(Enum):
    """Validation severity levels."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class ClusterQuality(Enum):
    """Cluster quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    INVALID = "invalid"


@dataclass
class ValidationIssue:
    """A validation issue found during cluster validation."""
    level: ValidationLevel
    message: str
    cluster_id: Optional[str] = None
    biomarker: Optional[str] = None
    metric: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None


@dataclass
class ClusterValidationResult:
    """Result of cluster validation."""
    cluster_id: str
    quality: ClusterQuality
    coherence_score: float  # 0-1
    issues: List[ValidationIssue]
    metrics: Dict[str, float]
    is_valid: bool


class ClusterValidator:
    """Validates cluster quality and coherence."""
    
    def __init__(self):
        """Initialize cluster validator with default thresholds."""
        self.min_cluster_size = 2
        self.min_coherence_threshold = 0.6
        self.max_cluster_size = 10
        self.min_biomarker_correlation = 0.3
        self.max_cluster_variance = 0.4
    
    def validate_cluster(self, cluster_data: Dict[str, Any]) -> ClusterValidationResult:
        """
        Validate a single cluster.
        
        Args:
            cluster_data: Dictionary containing cluster information
            
        Returns:
            ClusterValidationResult with validation details
        """
        cluster_id = cluster_data.get("cluster_id", "unknown")
        biomarkers = cluster_data.get("biomarkers", [])
        scores = cluster_data.get("scores", {})
        
        issues = []
        metrics = {}
        
        # Validate cluster size
        size_issues = self._validate_cluster_size(len(biomarkers))
        issues.extend(size_issues)
        metrics["cluster_size"] = len(biomarkers)
        
        # Validate biomarker coherence
        coherence_score = self._calculate_coherence_score(biomarkers, scores)
        metrics["coherence_score"] = coherence_score
        
        if coherence_score < self.min_coherence_threshold:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Low coherence score: {coherence_score:.2f} < {self.min_coherence_threshold}",
                cluster_id=cluster_id,
                metric="coherence_score",
                value=coherence_score,
                threshold=self.min_coherence_threshold
            ))
        
        # Validate score consistency
        consistency_issues = self._validate_score_consistency(scores)
        issues.extend(consistency_issues)
        metrics["score_variance"] = self._calculate_score_variance(scores)
        
        # Validate biomarker correlations
        correlation_issues = self._validate_biomarker_correlations(biomarkers, scores)
        issues.extend(correlation_issues)
        metrics["avg_correlation"] = self._calculate_average_correlation(biomarkers, scores)
        
        # Determine overall quality
        quality = self._determine_cluster_quality(issues, coherence_score)
        
        # Check if cluster is valid
        is_valid = self._is_cluster_valid(issues)
        
        return ClusterValidationResult(
            cluster_id=cluster_id,
            quality=quality,
            coherence_score=coherence_score,
            issues=issues,
            metrics=metrics,
            is_valid=is_valid
        )
    
    def validate_cluster_set(self, clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate a set of clusters.
        
        Args:
            clusters: List of cluster data dictionaries
            
        Returns:
            Dictionary with overall validation results
        """
        validation_results = []
        all_issues = []
        
        for cluster_data in clusters:
            result = self.validate_cluster(cluster_data)
            validation_results.append(result)
            all_issues.extend(result.issues)
        
        # Calculate overall metrics
        total_clusters = len(clusters)
        valid_clusters = sum(1 for r in validation_results if r.is_valid)
        avg_coherence = sum(r.coherence_score for r in validation_results) / total_clusters if total_clusters > 0 else 0
        
        # Determine overall quality
        quality_distribution = {}
        for quality in ClusterQuality:
            quality_distribution[quality.value] = sum(
                1 for r in validation_results if r.quality == quality
            )
        
        # Check for global issues
        global_issues = self._validate_cluster_set_globally(clusters, validation_results)
        
        return {
            "total_clusters": total_clusters,
            "valid_clusters": valid_clusters,
            "invalid_clusters": total_clusters - valid_clusters,
            "overall_quality": self._determine_overall_quality(validation_results),
            "average_coherence": avg_coherence,
            "quality_distribution": quality_distribution,
            "cluster_results": validation_results,
            "global_issues": global_issues,
            "is_valid": valid_clusters == total_clusters and len(global_issues) == 0
        }
    
    def _validate_cluster_size(self, size: int) -> List[ValidationIssue]:
        """Validate cluster size."""
        issues = []
        
        if size < self.min_cluster_size:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                message=f"Cluster too small: {size} < {self.min_cluster_size}",
                metric="cluster_size",
                value=size,
                threshold=self.min_cluster_size
            ))
        
        if size > self.max_cluster_size:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Cluster too large: {size} > {self.max_cluster_size}",
                metric="cluster_size",
                value=size,
                threshold=self.max_cluster_size
            ))
        
        return issues
    
    def _calculate_coherence_score(self, biomarkers: List[str], scores: Dict[str, float]) -> float:
        """Calculate cluster coherence score."""
        if len(biomarkers) < 2:
            return 0.0
        
        # Calculate score variance (lower variance = higher coherence)
        score_values = [scores.get(b, 0.0) for b in biomarkers if b in scores]
        if not score_values:
            return 0.0
        
        mean_score = sum(score_values) / len(score_values)
        variance = sum((score - mean_score) ** 2 for score in score_values) / len(score_values)
        
        # Convert variance to coherence score (0-1, higher is better)
        max_variance = 2500  # Maximum possible variance for 0-100 scores
        coherence = max(0.0, 1.0 - (variance / max_variance))
        
        return coherence
    
    def _validate_score_consistency(self, scores: Dict[str, float]) -> List[ValidationIssue]:
        """Validate score consistency within cluster."""
        issues = []
        
        if not scores:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                message="No scores provided for validation",
                metric="score_consistency"
            ))
            return issues
        
        score_values = list(scores.values())
        
        # Check for extreme outliers
        mean_score = sum(score_values) / len(score_values)
        std_dev = math.sqrt(sum((score - mean_score) ** 2 for score in score_values) / len(score_values))
        
        for biomarker, score in scores.items():
            if std_dev > 0:
                z_score = abs(score - mean_score) / std_dev
                if z_score > 2.5:  # More than 2.5 standard deviations
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Score outlier detected: {score:.1f} (z-score: {z_score:.2f})",
                        cluster_id=None,
                        biomarker=biomarker,
                        metric="score_consistency",
                        value=score
                    ))
        
        return issues
    
    def _validate_biomarker_correlations(self, biomarkers: List[str], scores: Dict[str, float]) -> List[ValidationIssue]:
        """Validate biomarker correlations within cluster."""
        issues = []
        
        if len(biomarkers) < 2:
            return issues
        
        # Check if biomarkers are clinically related
        clinical_groups = self._get_clinical_groups()
        group_counts = {}
        
        for biomarker in biomarkers:
            for group, group_biomarkers in clinical_groups.items():
                if biomarker in group_biomarkers:
                    group_counts[group] = group_counts.get(group, 0) + 1
                    break
        
        # Check for mixed clinical groups
        if len(group_counts) > 1:
            issues.append(ValidationIssue(
                level=ValidationLevel.INFO,
                message=f"Mixed clinical groups: {list(group_counts.keys())}",
                metric="biomarker_correlation",
                value=len(group_counts)
            ))
        
        return issues
    
    def _calculate_score_variance(self, scores: Dict[str, float]) -> float:
        """Calculate variance of scores in cluster."""
        if len(scores) < 2:
            return 0.0
        
        score_values = list(scores.values())
        mean_score = sum(score_values) / len(score_values)
        variance = sum((score - mean_score) ** 2 for score in score_values) / len(score_values)
        
        return variance
    
    def _calculate_average_correlation(self, biomarkers: List[str], scores: Dict[str, float]) -> float:
        """Calculate average correlation between biomarkers."""
        # Simplified correlation based on clinical grouping
        clinical_groups = self._get_clinical_groups()
        same_group_count = 0
        total_pairs = 0
        
        for i, biomarker1 in enumerate(biomarkers):
            for biomarker2 in biomarkers[i+1:]:
                total_pairs += 1
                
                # Check if biomarkers are in the same clinical group
                for group_biomarkers in clinical_groups.values():
                    if biomarker1 in group_biomarkers and biomarker2 in group_biomarkers:
                        same_group_count += 1
                        break
        
        if total_pairs == 0:
            return 0.0
        
        return same_group_count / total_pairs
    
    def _determine_cluster_quality(self, issues: List[ValidationIssue], coherence_score: float) -> ClusterQuality:
        """Determine overall cluster quality."""
        critical_issues = sum(1 for issue in issues if issue.level == ValidationLevel.CRITICAL)
        warning_issues = sum(1 for issue in issues if issue.level == ValidationLevel.WARNING)
        
        if critical_issues > 0:
            return ClusterQuality.INVALID
        elif warning_issues > 2 or coherence_score < 0.5:
            return ClusterQuality.POOR
        elif warning_issues > 0 or coherence_score < 0.7:
            return ClusterQuality.FAIR
        elif coherence_score >= 0.8:
            return ClusterQuality.EXCELLENT
        else:
            return ClusterQuality.GOOD
    
    def _is_cluster_valid(self, issues: List[ValidationIssue]) -> bool:
        """Check if cluster is valid."""
        critical_issues = sum(1 for issue in issues if issue.level == ValidationLevel.CRITICAL)
        return critical_issues == 0
    
    def _validate_cluster_set_globally(self, clusters: List[Dict[str, Any]], 
                                     validation_results: List[ClusterValidationResult]) -> List[ValidationIssue]:
        """Validate cluster set globally."""
        issues = []
        
        # Check for duplicate biomarkers across clusters
        all_biomarkers = []
        for cluster_data in clusters:
            all_biomarkers.extend(cluster_data.get("biomarkers", []))
        
        duplicate_biomarkers = []
        seen_biomarkers = set()
        for biomarker in all_biomarkers:
            if biomarker in seen_biomarkers:
                duplicate_biomarkers.append(biomarker)
            else:
                seen_biomarkers.add(biomarker)
        
        if duplicate_biomarkers:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                message=f"Duplicate biomarkers across clusters: {duplicate_biomarkers}",
                metric="global_duplicates"
            ))
        
        # Check for optimal number of clusters
        optimal_clusters = self._calculate_optimal_cluster_count(len(all_biomarkers))
        actual_clusters = len(clusters)
        
        if actual_clusters < optimal_clusters * 0.5:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Too few clusters: {actual_clusters} (optimal: ~{optimal_clusters})",
                metric="cluster_count",
                value=actual_clusters,
                threshold=optimal_clusters
            ))
        elif actual_clusters > optimal_clusters * 2:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Too many clusters: {actual_clusters} (optimal: ~{optimal_clusters})",
                metric="cluster_count",
                value=actual_clusters,
                threshold=optimal_clusters
            ))
        
        return issues
    
    def _determine_overall_quality(self, validation_results: List[ClusterValidationResult]) -> str:
        """Determine overall quality of cluster set."""
        if not validation_results:
            return "unknown"
        
        quality_counts = {}
        for quality in ClusterQuality:
            quality_counts[quality] = sum(1 for r in validation_results if r.quality == quality)
        
        # Return the most common quality level
        return max(quality_counts, key=quality_counts.get).value
    
    def _calculate_optimal_cluster_count(self, biomarker_count: int) -> int:
        """Calculate optimal number of clusters based on biomarker count."""
        # Simple heuristic: sqrt of biomarker count, with bounds
        optimal = max(2, min(8, int(math.sqrt(biomarker_count))))
        return optimal
    
    def _get_clinical_groups(self) -> Dict[str, List[str]]:
        """Get clinical grouping of biomarkers."""
        return {
            "metabolic": ["glucose", "hba1c", "insulin", "homa_ir"],
            "cardiovascular": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "triglycerides"],
            "inflammatory": ["crp", "esr", "il6"],
            "kidney": ["creatinine", "bun", "egfr"],
            "liver": ["alt", "ast", "bilirubin", "alp"],
            "cbc": ["hemoglobin", "hematocrit", "wbc", "platelets"],
            "hormonal": ["tsh", "free_t4", "testosterone", "estradiol"],
            "nutritional": ["vitamin_d", "b12", "folate", "iron"]
        }
    
    def set_validation_thresholds(self, **kwargs) -> None:
        """Set custom validation thresholds."""
        if "min_cluster_size" in kwargs:
            self.min_cluster_size = kwargs["min_cluster_size"]
        if "min_coherence_threshold" in kwargs:
            self.min_coherence_threshold = kwargs["min_coherence_threshold"]
        if "max_cluster_size" in kwargs:
            self.max_cluster_size = kwargs["max_cluster_size"]
        if "min_biomarker_correlation" in kwargs:
            self.min_biomarker_correlation = kwargs["min_biomarker_correlation"]
        if "max_cluster_variance" in kwargs:
            self.max_cluster_variance = kwargs["max_cluster_variance"]
