"""
Rule-based clustering engine for biomarker correlation grouping.

This module provides rule-based clustering algorithms that group biomarkers
based on clinical correlations, score patterns, and health system relationships.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import uuid

from core.models.biomarker import BiomarkerCluster


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
        """Initialize default clustering rules."""
        # Metabolic dysfunction rule
        metabolic_rule = BiomarkerCorrelationRule(
            name="metabolic_dysfunction",
            description="Clusters biomarkers indicating metabolic dysfunction",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        metabolic_rule.required_biomarkers = ["glucose", "hba1c"]
        metabolic_rule.optional_biomarkers = ["insulin", "homa_ir"]
        metabolic_rule.score_thresholds = {
            "glucose": (0, 70),  # Low to moderate scores
            "hba1c": (0, 70),
            "insulin": (0, 70)
        }
        metabolic_rule.min_cluster_size = 2
        self.rules.append(metabolic_rule)
        
        # Cardiovascular risk rule
        cardio_rule = BiomarkerCorrelationRule(
            name="cardiovascular_risk",
            description="Clusters biomarkers indicating cardiovascular risk",
            cluster_type=ClusterType.CARDIOVASCULAR_RISK
        )
        cardio_rule.required_biomarkers = ["total_cholesterol", "ldl_cholesterol"]
        cardio_rule.optional_biomarkers = ["hdl_cholesterol", "triglycerides"]
        cardio_rule.score_thresholds = {
            "total_cholesterol": (0, 70),
            "ldl_cholesterol": (0, 70),
            "hdl_cholesterol": (30, 100),  # HDL is inverted (higher is better)
            "triglycerides": (0, 70)
        }
        cardio_rule.min_cluster_size = 2
        self.rules.append(cardio_rule)
        
        # Inflammatory burden rule
        inflammatory_rule = BiomarkerCorrelationRule(
            name="inflammatory_burden",
            description="Clusters biomarkers indicating inflammatory burden",
            cluster_type=ClusterType.INFLAMMATORY_BURDEN
        )
        inflammatory_rule.required_biomarkers = ["crp"]
        inflammatory_rule.optional_biomarkers = ["esr", "il6"]
        inflammatory_rule.score_thresholds = {
            "crp": (0, 70),
            "esr": (0, 70)
        }
        inflammatory_rule.min_cluster_size = 1
        self.rules.append(inflammatory_rule)
        
        # Organ function rule
        organ_rule = BiomarkerCorrelationRule(
            name="organ_function",
            description="Clusters biomarkers indicating organ function concerns",
            cluster_type=ClusterType.ORGAN_FUNCTION
        )
        organ_rule.required_biomarkers = ["creatinine", "alt"]
        organ_rule.optional_biomarkers = ["bun", "ast", "egfr"]
        organ_rule.score_thresholds = {
            "creatinine": (0, 70),
            "alt": (0, 70),
            "ast": (0, 70),
            "bun": (0, 70)
        }
        organ_rule.min_cluster_size = 2
        self.rules.append(organ_rule)
        
        # Nutritional deficiency rule
        nutritional_rule = BiomarkerCorrelationRule(
            name="nutritional_deficiency",
            description="Clusters biomarkers indicating nutritional deficiencies",
            cluster_type=ClusterType.NUTRITIONAL_DEFICIENCY
        )
        nutritional_rule.required_biomarkers = ["vitamin_d", "b12"]
        nutritional_rule.optional_biomarkers = ["folate", "iron", "ferritin"]
        nutritional_rule.score_thresholds = {
            "vitamin_d": (0, 70),
            "b12": (0, 70),
            "folate": (0, 70),
            "iron": (0, 70)
        }
        nutritional_rule.min_cluster_size = 2
        self.rules.append(nutritional_rule)
        
        # Hormonal imbalance rule
        hormonal_rule = BiomarkerCorrelationRule(
            name="hormonal_imbalance",
            description="Clusters biomarkers indicating hormonal imbalances",
            cluster_type=ClusterType.HORMONAL_IMBALANCE
        )
        hormonal_rule.required_biomarkers = ["tsh"]
        hormonal_rule.optional_biomarkers = ["free_t4", "testosterone", "estradiol"]
        hormonal_rule.score_thresholds = {
            "tsh": (0, 70),
            "free_t4": (0, 70)
        }
        hormonal_rule.min_cluster_size = 1
        self.rules.append(hormonal_rule)
    
    def add_rule(self, rule: BiomarkerCorrelationRule) -> None:
        """
        Add a clustering rule.
        
        Args:
            rule: Clustering rule to add
        """
        self.rules.append(rule)
    
    def apply_rules(self, biomarkers: Dict[str, float], scores: Dict[str, float]) -> List[BiomarkerCluster]:
        """
        Apply all clustering rules to biomarkers.
        
        Args:
            biomarkers: Biomarker values
            scores: Biomarker scores
            
        Returns:
            List of clusters found by rules
        """
        clusters = []
        used_biomarkers = set()
        
        # Sort rules by priority (lower number = higher priority)
        sorted_rules = sorted(self.rules, key=lambda r: r.priority)
        
        for rule in sorted_rules:
            cluster = rule.apply(biomarkers, scores)
            if cluster:
                # Check if any biomarkers are already used
                cluster_biomarkers = set(cluster.biomarkers)
                if not cluster_biomarkers.intersection(used_biomarkers):
                    clusters.append(cluster)
                    used_biomarkers.update(cluster_biomarkers)
        
        # Merge overlapping clusters if needed
        merged_clusters = self._merge_overlapping_clusters(clusters)
        
        return merged_clusters
    
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
        Get names of all registered rules.
        
        Returns:
            List of rule names
        """
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
