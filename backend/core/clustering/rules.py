"""
Rule-based clustering engine for biomarker correlation grouping.

Sprint 6: Schema-driven clusters. Definitions loaded from ssot/clusters.yaml;
no hardcoded cluster logic. Layer B computes; Layer C translates.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import uuid

from core.models.biomarker import BiomarkerCluster

# Schema-driven clustering (Sprint 6)
try:
    from core.analytics.cluster_schema import (
        load_cluster_schema,
        compute_cluster_status,
    )
    _SCHEMA_AVAILABLE = True
except ImportError:
    _SCHEMA_AVAILABLE = False


class ClusterType(Enum):
    """Types of biomarker clusters."""
    METABOLIC_DYSFUNCTION = "metabolic_dysfunction"
    CARDIOVASCULAR_RISK = "cardiovascular_risk"
    INFLAMMATORY_BURDEN = "inflammatory_burden"
    NUTRITIONAL_DEFICIENCY = "nutritional_deficiency"
    ORGAN_FUNCTION = "organ_function"
    HORMONAL_IMBALANCE = "hormonal_imbalance"
    GENERAL_HEALTH = "general_health"


@dataclass
class ClusteringRule:
    """Rule for biomarker clustering."""
    name: str
    description: str
    cluster_type: ClusterType
    required_biomarkers: List[str]
    optional_biomarkers: List[str]
    score_thresholds: Dict[str, Tuple[float, float]]  # biomarker -> (min, max)
    correlation_threshold: float
    min_cluster_size: int
    priority: int


class BiomarkerCorrelationRule:
    """Rule for clustering based on biomarker correlations."""
    
    def __init__(self, name: str, description: str, cluster_type: ClusterType):
        """
        Initialize correlation rule.
        
        Args:
            name: Rule name
            description: Rule description
            cluster_type: Type of cluster this rule creates
        """
        self.name = name
        self.description = description
        self.cluster_type = cluster_type
        self.required_biomarkers = []
        self.optional_biomarkers = []
        self.score_thresholds = {}
        self.correlation_threshold = 0.6
        self.min_cluster_size = 2
        self.priority = 1
    
    def apply(self, biomarkers: Dict[str, float], scores: Dict[str, float]) -> Optional[BiomarkerCluster]:
        """
        Apply correlation rule to biomarkers.
        
        Args:
            biomarkers: Biomarker values
            scores: Biomarker scores
            
        Returns:
            BiomarkerCluster if rule matches, None otherwise
        """
        # Find biomarkers that meet the criteria
        matching_biomarkers = self._find_matching_biomarkers(biomarkers, scores)
        
        if len(matching_biomarkers) < self.min_cluster_size:
            return None
        
        # Calculate cluster confidence
        confidence = self._calculate_cluster_confidence(matching_biomarkers, scores)
        
        # Create cluster
        cluster_id = f"{self.cluster_type.value}_{uuid.uuid4().hex[:8]}"
        
        return BiomarkerCluster(
            cluster_id=cluster_id,
            name=self._generate_cluster_name(),
            biomarkers=matching_biomarkers,
            description=self._generate_cluster_description(matching_biomarkers, scores),
            severity=self._determine_severity(matching_biomarkers, scores),
            confidence=confidence
        )
    
    def _find_matching_biomarkers(self, biomarkers: Dict[str, float], scores: Dict[str, float]) -> List[str]:
        """Find biomarkers that match the rule criteria."""
        matching = []
        
        # Check required biomarkers first
        for biomarker in self.required_biomarkers:
            if biomarker in biomarkers and biomarker in scores:
                if self._meets_score_threshold(biomarker, scores[biomarker]):
                    matching.append(biomarker)
        
        # If we don't have enough required biomarkers, return empty
        if len(matching) < self.min_cluster_size:
            return []
        
        # Add optional biomarkers that meet criteria
        for biomarker in self.optional_biomarkers:
            if biomarker in biomarkers and biomarker in scores:
                if self._meets_score_threshold(biomarker, scores[biomarker]):
                    matching.append(biomarker)
        
        return matching
    
    def _meets_score_threshold(self, biomarker: str, score: float) -> bool:
        """Check if biomarker score meets threshold."""
        if biomarker not in self.score_thresholds:
            return True  # No threshold defined
        
        min_score, max_score = self.score_thresholds[biomarker]
        return min_score <= score <= max_score
    
    def _calculate_cluster_confidence(self, biomarkers: List[str], scores: Dict[str, float]) -> float:
        """Calculate confidence score for the cluster."""
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
    
    def _generate_cluster_name(self) -> str:
        """Generate cluster name."""
        name_mapping = {
            ClusterType.METABOLIC_DYSFUNCTION: "Metabolic Dysfunction",
            ClusterType.CARDIOVASCULAR_RISK: "Cardiovascular Risk",
            ClusterType.INFLAMMATORY_BURDEN: "Inflammatory Burden",
            ClusterType.NUTRITIONAL_DEFICIENCY: "Nutritional Deficiency",
            ClusterType.ORGAN_FUNCTION: "Organ Function Concern",
            ClusterType.HORMONAL_IMBALANCE: "Hormonal Imbalance",
            ClusterType.GENERAL_HEALTH: "General Health Pattern"
        }
        return name_mapping.get(self.cluster_type, "Unknown Cluster")
    
    def _generate_cluster_description(self, biomarkers: List[str], scores: Dict[str, float]) -> str:
        """Generate cluster description."""
        avg_score = sum(scores.get(b, 0.0) for b in biomarkers) / len(biomarkers)
        
        if avg_score < 40:
            severity_desc = "severe"
        elif avg_score < 60:
            severity_desc = "moderate"
        elif avg_score < 80:
            severity_desc = "mild"
        else:
            severity_desc = "optimal"
        
        biomarker_list = ", ".join(biomarkers[:3])
        if len(biomarkers) > 3:
            biomarker_list += f" and {len(biomarkers) - 3} others"
        
        return f"{severity_desc.title()} {self.cluster_type.value.replace('_', ' ')} affecting {biomarker_list}"
    
    def _determine_severity(self, biomarkers: List[str], scores: Dict[str, float]) -> str:
        """Determine cluster severity."""
        if not biomarkers:
            return "normal"
        
        avg_score = sum(scores.get(b, 0.0) for b in biomarkers) / len(biomarkers)
        
        if avg_score < 30:
            return "critical"
        elif avg_score < 50:
            return "high"
        elif avg_score < 70:
            return "moderate"
        elif avg_score < 85:
            return "mild"
        else:
            return "normal"


class ClusteringRuleEngine:
    """Engine for applying clustering rules."""
    
    def __init__(self):
        """Initialize the rule engine."""
        self.rules: List[BiomarkerCorrelationRule] = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Sprint 6: No hardcoded rules. Clusters loaded from ssot/clusters.yaml."""
        pass
    
    def add_rule(self, rule: BiomarkerCorrelationRule) -> None:
        """
        Add a clustering rule.
        
        Args:
            rule: Clustering rule to add
        """
        self.rules.append(rule)
    
    def apply_rules(self, biomarkers: Dict[str, float], scores: Dict[str, float]) -> List[BiomarkerCluster]:
        """
        Apply clustering rules to biomarkers. Sprint 6: schema-driven only.
        
        Args:
            biomarkers: Biomarker values
            scores: Biomarker scores
            
        Returns:
            List of clusters from ssot/clusters.yaml
        """
        if _SCHEMA_AVAILABLE:
            return self._apply_schema_rules(biomarkers, scores)
        return []

    def _apply_schema_rules(self, biomarkers: Dict[str, float], scores: Dict[str, float]) -> List[BiomarkerCluster]:
        """Schema-driven cluster assignment. Deterministic; no hardcoded logic."""
        try:
            schema = load_cluster_schema()
        except (FileNotFoundError, ValueError) as _:
            return []

        available = set(biomarkers.keys()) | set(scores.keys())
        clusters: List[BiomarkerCluster] = []

        for cid, cdef in schema.clusters.items():
            status = compute_cluster_status(cdef, available)
            present = status["required_present"] | status["important_present"] | status["optional_present"]
            if not present:
                continue

            total = len(cdef.required) + len(cdef.important) + len(cdef.optional)
            conf = len(present) / total if total > 0 else 0.0
            if status["complete"]:
                conf = max(conf, 0.9)
            conf = round(min(1.0, conf), 2)

            severity = "normal" if status["complete"] else "moderate"
            desc = ("Complete: " if status["complete"] else "Incomplete: ") + cdef.description

            clusters.append(
                BiomarkerCluster(
                    cluster_id=cid,
                    name=cdef.description,
                    biomarkers=sorted(present),
                    description=desc,
                    severity=severity,
                    confidence=conf,
                )
            )

        return clusters
    
    def _merge_overlapping_clusters(self, clusters: List[BiomarkerCluster]) -> List[BiomarkerCluster]:
        """Merge clusters that have overlapping biomarkers."""
        if len(clusters) <= 1:
            return clusters
        
        merged = []
        processed = set()
        
        for i, cluster1 in enumerate(clusters):
            if i in processed:
                continue
            
            # Find clusters to merge with
            to_merge = [cluster1]
            cluster1_biomarkers = set(cluster1.biomarkers)
            
            for j, cluster2 in enumerate(clusters[i+1:], i+1):
                if j in processed:
                    continue
                
                cluster2_biomarkers = set(cluster2.biomarkers)
                
                # Check for overlap (more than 50% overlap)
                overlap = cluster1_biomarkers.intersection(cluster2_biomarkers)
                if len(overlap) > 0.5 * min(len(cluster1_biomarkers), len(cluster2_biomarkers)):
                    to_merge.append(cluster2)
                    processed.add(j)
            
            if len(to_merge) > 1:
                # Merge clusters
                merged_cluster = self._merge_cluster_list(to_merge)
                merged.append(merged_cluster)
            else:
                merged.append(cluster1)
            
            processed.add(i)
        
        return merged
    
    def _merge_cluster_list(self, clusters: List[BiomarkerCluster]) -> BiomarkerCluster:
        """Merge a list of clusters into one."""
        all_biomarkers = []
        all_descriptions = []
        min_confidence = 1.0
        max_severity = "normal"
        
        severity_order = ["normal", "mild", "moderate", "high", "critical"]
        
        for cluster in clusters:
            all_biomarkers.extend(cluster.biomarkers)
            all_descriptions.append(cluster.description)
            min_confidence = min(min_confidence, cluster.confidence)
            
            # Get severity level
            current_severity_idx = severity_order.index(cluster.severity)
            max_severity_idx = severity_order.index(max_severity)
            if current_severity_idx > max_severity_idx:
                max_severity = cluster.severity
        
        # Remove duplicates
        unique_biomarkers = list(set(all_biomarkers))
        
        # Create merged cluster
        cluster_id = f"merged_{uuid.uuid4().hex[:8]}"
        merged_description = "; ".join(all_descriptions[:2])  # Limit description length
        
        return BiomarkerCluster(
            cluster_id=cluster_id,
            name="Merged Health Pattern",
            biomarkers=unique_biomarkers,
            description=merged_description,
            severity=max_severity,
            confidence=min_confidence
        )
    
    def get_rule_names(self) -> List[str]:
        """
        Get names of all registered rules. Sprint 6: from schema when available.
        
        Returns:
            List of rule/cluster names
        """
        if _SCHEMA_AVAILABLE:
            try:
                schema = load_cluster_schema()
                return list(schema.clusters.keys())
            except (FileNotFoundError, ValueError):
                pass
        return [rule.name for rule in self.rules]
    
    def get_rule_by_name(self, name: str) -> Optional[BiomarkerCorrelationRule]:
        """
        Get rule by name.
        
        Args:
            name: Rule name
            
        Returns:
            Rule if found, None otherwise
        """
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None
