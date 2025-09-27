"""
Unit tests for clustering rules.

Tests the rule-based clustering algorithms and biomarker correlation grouping.
"""

import pytest
from core.clustering.rules import (
    ClusteringRuleEngine,
    BiomarkerCorrelationRule,
    ClusterType,
    ClusteringRule
)


class TestBiomarkerCorrelationRule:
    """Test cases for BiomarkerCorrelationRule."""
    
    def test_initialization(self):
        """Test rule initialization."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test clustering rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        assert rule.name == "test_rule"
        assert rule.description == "Test clustering rule"
        assert rule.cluster_type == ClusterType.METABOLIC_DYSFUNCTION
        assert rule.correlation_threshold == 0.6
        assert rule.min_cluster_size == 2
        assert rule.priority == 1
    
    def test_apply_rule_no_matching_biomarkers(self):
        """Test applying rule with no matching biomarkers."""
        rule = BiomarkerCorrelationRule(
            name="metabolic_rule",
            description="Metabolic dysfunction rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        rule.required_biomarkers = ["glucose", "hba1c"]
        rule.score_thresholds = {"glucose": (0, 70), "hba1c": (0, 70)}
        
        biomarkers = {"total_cholesterol": 220.0, "ldl_cholesterol": 140.0}
        scores = {"total_cholesterol": 45.0, "ldl_cholesterol": 40.0}
        
        cluster = rule.apply(biomarkers, scores)
        
        assert cluster is None
    
    def test_apply_rule_insufficient_required_biomarkers(self):
        """Test applying rule with insufficient required biomarkers."""
        rule = BiomarkerCorrelationRule(
            name="metabolic_rule",
            description="Metabolic dysfunction rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        rule.required_biomarkers = ["glucose", "hba1c"]
        rule.min_cluster_size = 2
        rule.score_thresholds = {"glucose": (0, 70), "hba1c": (0, 70)}
        
        biomarkers = {"glucose": 95.0}
        scores = {"glucose": 75.0}
        
        cluster = rule.apply(biomarkers, scores)
        
        assert cluster is None
    
    def test_apply_rule_sufficient_required_biomarkers(self):
        """Test applying rule with sufficient required biomarkers."""
        rule = BiomarkerCorrelationRule(
            name="metabolic_rule",
            description="Metabolic dysfunction rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        rule.required_biomarkers = ["glucose", "hba1c"]
        rule.min_cluster_size = 2
        rule.score_thresholds = {"glucose": (70, 100), "hba1c": (70, 100)}
        
        biomarkers = {"glucose": 95.0, "hba1c": 5.2}
        scores = {"glucose": 75.0, "hba1c": 80.0}
        
        cluster = rule.apply(biomarkers, scores)
        
        assert cluster is not None
        assert cluster.name == "Metabolic Dysfunction"
        assert "glucose" in cluster.biomarkers
        assert "hba1c" in cluster.biomarkers
        assert cluster.severity in ["normal", "mild", "moderate", "high", "critical"]
        assert 0.0 <= cluster.confidence <= 1.0
    
    def test_apply_rule_with_optional_biomarkers(self):
        """Test applying rule with optional biomarkers."""
        rule = BiomarkerCorrelationRule(
            name="metabolic_rule",
            description="Metabolic dysfunction rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        rule.required_biomarkers = ["glucose"]
        rule.optional_biomarkers = ["hba1c", "insulin"]
        rule.min_cluster_size = 1
        rule.score_thresholds = {
            "glucose": (70, 100),
            "hba1c": (70, 100),
            "insulin": (60, 100)
        }
        
        biomarkers = {"glucose": 95.0, "hba1c": 5.2, "insulin": 15.0}
        scores = {"glucose": 75.0, "hba1c": 80.0, "insulin": 65.0}
        
        cluster = rule.apply(biomarkers, scores)
        
        assert cluster is not None
        assert "glucose" in cluster.biomarkers
        assert "hba1c" in cluster.biomarkers
        assert "insulin" in cluster.biomarkers
    
    def test_meets_score_threshold(self):
        """Test score threshold checking."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        rule.score_thresholds = {"glucose": (50, 100)}
        
        # Score within threshold
        assert rule._meets_score_threshold("glucose", 75.0) is True
        
        # Score below threshold
        assert rule._meets_score_threshold("glucose", 40.0) is False
        
        # Score above threshold
        assert rule._meets_score_threshold("glucose", 120.0) is False
        
        # No threshold defined
        assert rule._meets_score_threshold("unknown", 50.0) is True
    
    def test_calculate_cluster_confidence(self):
        """Test cluster confidence calculation."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        biomarkers = ["glucose", "hba1c", "insulin"]
        scores = {"glucose": 75.0, "hba1c": 80.0, "insulin": 70.0}
        
        confidence = rule._calculate_cluster_confidence(biomarkers, scores)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0  # Should have some confidence
    
    def test_calculate_cluster_confidence_empty(self):
        """Test cluster confidence calculation with empty biomarkers."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        confidence = rule._calculate_cluster_confidence([], {})
        
        assert confidence == 0.0
    
    def test_generate_cluster_name(self):
        """Test cluster name generation."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        name = rule._generate_cluster_name()
        
        assert name == "Metabolic Dysfunction"
    
    def test_generate_cluster_description(self):
        """Test cluster description generation."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        biomarkers = ["glucose", "hba1c", "insulin"]
        scores = {"glucose": 75.0, "hba1c": 80.0, "insulin": 70.0}
        
        description = rule._generate_cluster_description(biomarkers, scores)
        
        assert "metabolic dysfunction" in description.lower()
        assert "glucose" in description
        assert "hba1c" in description
        assert "insulin" in description
    
    def test_determine_severity(self):
        """Test severity determination."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        # Test different severity levels
        biomarkers = ["glucose", "hba1c"]
        
        # Critical severity
        scores_critical = {"glucose": 20.0, "hba1c": 25.0}
        severity = rule._determine_severity(biomarkers, scores_critical)
        assert severity == "critical"
        
        # High severity
        scores_high = {"glucose": 40.0, "hba1c": 45.0}
        severity = rule._determine_severity(biomarkers, scores_high)
        assert severity == "high"
        
        # Moderate severity
        scores_moderate = {"glucose": 60.0, "hba1c": 65.0}
        severity = rule._determine_severity(biomarkers, scores_moderate)
        assert severity == "moderate"
        
        # Mild severity
        scores_mild = {"glucose": 80.0, "hba1c": 82.0}
        severity = rule._determine_severity(biomarkers, scores_mild)
        assert severity == "mild"
        
        # Normal severity
        scores_normal = {"glucose": 90.0, "hba1c": 95.0}
        severity = rule._determine_severity(biomarkers, scores_normal)
        assert severity == "normal"
        
        # Empty biomarkers
        severity = rule._determine_severity([], {})
        assert severity == "normal"


class TestClusteringRuleEngine:
    """Test cases for ClusteringRuleEngine."""
    
    def test_initialization(self):
        """Test rule engine initialization."""
        engine = ClusteringRuleEngine()
        
        assert len(engine.rules) > 0  # Should have default rules
        assert isinstance(engine.rules[0], BiomarkerCorrelationRule)
    
    def test_add_rule(self):
        """Test adding a rule."""
        engine = ClusteringRuleEngine()
        initial_count = len(engine.rules)
        
        rule = BiomarkerCorrelationRule(
            name="custom_rule",
            description="Custom clustering rule",
            cluster_type=ClusterType.GENERAL_HEALTH
        )
        
        engine.add_rule(rule)
        
        assert len(engine.rules) == initial_count + 1
        assert engine.rules[-1] == rule
    
    def test_apply_rules_no_matches(self):
        """Test applying rules with no matches."""
        engine = ClusteringRuleEngine()
        
        biomarkers = {"unknown_biomarker": 100.0}
        scores = {"unknown_biomarker": 50.0}
        
        clusters = engine.apply_rules(biomarkers, scores)
        
        assert len(clusters) == 0
    
    def test_apply_rules_with_matches(self):
        """Test applying rules with matches."""
        engine = ClusteringRuleEngine()
        
        biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 220.0,
            "ldl_cholesterol": 140.0,
            "crp": 2.5
        }
        scores = {
            "glucose": 75.0,
            "hba1c": 80.0,
            "total_cholesterol": 45.0,
            "ldl_cholesterol": 40.0,
            "crp": 35.0
        }
        
        clusters = engine.apply_rules(biomarkers, scores)
        
        assert len(clusters) > 0
        
        # Check that clusters have required fields
        for cluster in clusters:
            assert hasattr(cluster, 'cluster_id')
            assert hasattr(cluster, 'name')
            assert hasattr(cluster, 'biomarkers')
            assert hasattr(cluster, 'description')
            assert hasattr(cluster, 'severity')
            assert hasattr(cluster, 'confidence')
            assert len(cluster.biomarkers) > 0
    
    def test_apply_rules_no_overlapping_biomarkers(self):
        """Test that rules don't create overlapping biomarker clusters."""
        engine = ClusteringRuleEngine()
        
        biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 220.0,
            "ldl_cholesterol": 140.0
        }
        scores = {
            "glucose": 75.0,
            "hba1c": 80.0,
            "total_cholesterol": 45.0,
            "ldl_cholesterol": 40.0
        }
        
        clusters = engine.apply_rules(biomarkers, scores)
        
        # Check that no biomarker appears in multiple clusters
        all_biomarkers = []
        for cluster in clusters:
            all_biomarkers.extend(cluster.biomarkers)
        
        assert len(all_biomarkers) == len(set(all_biomarkers))  # No duplicates
    
    def test_get_rule_names(self):
        """Test getting rule names."""
        engine = ClusteringRuleEngine()
        
        names = engine.get_rule_names()
        
        assert len(names) == len(engine.rules)
        assert all(isinstance(name, str) for name in names)
        assert all(len(name) > 0 for name in names)
    
    def test_get_rule_by_name(self):
        """Test getting rule by name."""
        engine = ClusteringRuleEngine()
        
        # Get a rule by name
        rule_name = engine.get_rule_names()[0]
        rule = engine.get_rule_by_name(rule_name)
        
        assert rule is not None
        assert rule.name == rule_name
        
        # Test with non-existent rule
        non_existent_rule = engine.get_rule_by_name("non_existent_rule")
        assert non_existent_rule is None
    
    def test_merge_overlapping_clusters(self):
        """Test merging overlapping clusters."""
        engine = ClusteringRuleEngine()
        
        # Create test clusters with overlapping biomarkers
        from core.models.biomarker import BiomarkerCluster
        
        cluster1 = BiomarkerCluster(
            cluster_id="cluster1",
            name="Cluster 1",
            biomarkers=["glucose", "hba1c", "insulin"],
            description="Test cluster 1",
            severity="moderate",
            confidence=0.8
        )
        
        cluster2 = BiomarkerCluster(
            cluster_id="cluster2",
            name="Cluster 2",
            biomarkers=["glucose", "hba1c", "total_cholesterol"],
            description="Test cluster 2",
            severity="high",
            confidence=0.7
        )
        
        cluster3 = BiomarkerCluster(
            cluster_id="cluster3",
            name="Cluster 3",
            biomarkers=["crp", "esr"],
            description="Test cluster 3",
            severity="mild",
            confidence=0.9
        )
        
        clusters = [cluster1, cluster2, cluster3]
        merged = engine._merge_overlapping_clusters(clusters)
        
        # Should merge clusters 1 and 2 due to overlap
        assert len(merged) == 2  # 2 clusters after merging
        
        # Check that merged cluster contains all biomarkers
        merged_cluster = merged[0]
        assert "glucose" in merged_cluster.biomarkers
        assert "hba1c" in merged_cluster.biomarkers
        assert "insulin" in merged_cluster.biomarkers
        assert "total_cholesterol" in merged_cluster.biomarkers
    
    def test_merge_cluster_list(self):
        """Test merging a list of clusters."""
        engine = ClusteringRuleEngine()
        
        from core.models.biomarker import BiomarkerCluster
        
        clusters = [
            BiomarkerCluster(
                cluster_id="cluster1",
                name="Cluster 1",
                biomarkers=["glucose", "hba1c"],
                description="Test cluster 1",
                severity="moderate",
                confidence=0.8
            ),
            BiomarkerCluster(
                cluster_id="cluster2",
                name="Cluster 2",
                biomarkers=["insulin"],
                description="Test cluster 2",
                severity="high",
                confidence=0.7
            )
        ]
        
        merged = engine._merge_cluster_list(clusters)
        
        assert merged.cluster_id.startswith("merged_")
        assert merged.name == "Merged Health Pattern"
        assert len(merged.biomarkers) == 3  # glucose, hba1c, insulin
        assert "glucose" in merged.biomarkers
        assert "hba1c" in merged.biomarkers
        assert "insulin" in merged.biomarkers
        assert merged.severity == "high"  # Should take the highest severity
        assert merged.confidence == 0.7  # Should take the lowest confidence


class TestClusterType:
    """Test cases for ClusterType enum."""
    
    def test_cluster_type_values(self):
        """Test ClusterType enum values."""
        assert ClusterType.METABOLIC_DYSFUNCTION.value == "metabolic_dysfunction"
        assert ClusterType.CARDIOVASCULAR_RISK.value == "cardiovascular_risk"
        assert ClusterType.INFLAMMATORY_BURDEN.value == "inflammatory_burden"
        assert ClusterType.NUTRITIONAL_DEFICIENCY.value == "nutritional_deficiency"
        assert ClusterType.ORGAN_FUNCTION.value == "organ_function"
        assert ClusterType.HORMONAL_IMBALANCE.value == "hormonal_imbalance"
        assert ClusterType.GENERAL_HEALTH.value == "general_health"


class TestClusteringRule:
    """Test cases for ClusteringRule dataclass."""
    
    def test_clustering_rule_creation(self):
        """Test creating a ClusteringRule instance."""
        rule = ClusteringRule(
            name="test_rule",
            description="Test clustering rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION,
            required_biomarkers=["glucose", "hba1c"],
            optional_biomarkers=["insulin"],
            score_thresholds={"glucose": (0, 70), "hba1c": (0, 70)},
            correlation_threshold=0.6,
            min_cluster_size=2,
            priority=1
        )
        
        assert rule.name == "test_rule"
        assert rule.description == "Test clustering rule"
        assert rule.cluster_type == ClusterType.METABOLIC_DYSFUNCTION
        assert rule.required_biomarkers == ["glucose", "hba1c"]
        assert rule.optional_biomarkers == ["insulin"]
        assert rule.score_thresholds == {"glucose": (0, 70), "hba1c": (0, 70)}
        assert rule.correlation_threshold == 0.6
        assert rule.min_cluster_size == 2
        assert rule.priority == 1
    
    def test_apply_rules_no_matching_biomarkers(self):
        """Test applying rules when no biomarkers match any rules."""
        engine = ClusteringRuleEngine()
        
        # Use biomarkers that don't match any default rules
        biomarkers = {"unknown_biomarker_1": 100.0, "unknown_biomarker_2": 200.0}
        scores = {"unknown_biomarker_1": 50.0, "unknown_biomarker_2": 60.0}
        
        clusters = engine.apply_rules(biomarkers, scores)
        
        assert len(clusters) == 0
    
    def test_apply_rules_threshold_boundaries(self):
        """Test rule application with threshold boundary values."""
        engine = ClusteringRuleEngine()
        
        # Test with biomarkers that are exactly on threshold boundaries
        biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 220.0,
            "ldl_cholesterol": 140.0
        }
        
        # Test exact threshold values (70.0 is the threshold for many rules)
        scores_exact = {
            "glucose": 70.0,  # Exactly on threshold
            "hba1c": 70.0,    # Exactly on threshold
            "total_cholesterol": 70.0,  # Exactly on threshold
            "ldl_cholesterol": 70.0     # Exactly on threshold
        }
        
        clusters_exact = engine.apply_rules(biomarkers, scores_exact)
        
        # Test just over threshold
        scores_over = {
            "glucose": 70.1,  # Just over threshold
            "hba1c": 70.1,    # Just over threshold
            "total_cholesterol": 70.1,  # Just over threshold
            "ldl_cholesterol": 70.1     # Just over threshold
        }
        
        clusters_over = engine.apply_rules(biomarkers, scores_over)
        
        # Test just under threshold
        scores_under = {
            "glucose": 69.9,  # Just under threshold
            "hba1c": 69.9,    # Just under threshold
            "total_cholesterol": 69.9,  # Just under threshold
            "ldl_cholesterol": 69.9     # Just under threshold
        }
        
        clusters_under = engine.apply_rules(biomarkers, scores_under)
        
        # All should produce valid results (may be empty if no rules match)
        assert isinstance(clusters_exact, list)
        assert isinstance(clusters_over, list)
        assert isinstance(clusters_under, list)
    
    def test_calculate_cluster_confidence_empty_scores(self):
        """Test cluster confidence calculation with empty scores."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        biomarkers = ["glucose", "hba1c"]
        empty_scores = {}
        
        confidence = rule._calculate_cluster_confidence(biomarkers, empty_scores)
        
        # When scores are empty, the method returns 1.0 (maximum confidence)
        # because there's no variance to calculate
        assert confidence == 1.0
    
    def test_generate_cluster_description_boundary_values(self):
        """Test cluster description generation with boundary values."""
        rule = BiomarkerCorrelationRule(
            name="test_rule",
            description="Test rule",
            cluster_type=ClusterType.METABOLIC_DYSFUNCTION
        )
        
        biomarkers = ["glucose", "hba1c", "insulin", "homa_ir", "additional_biomarker"]
        
        # Test boundary values for severity description
        test_cases = [
            (39.0, "severe"),    # Just below 40
            (40.0, "moderate"),  # Exactly 40
            (59.0, "moderate"),  # Just below 60
            (60.0, "mild"),      # Exactly 60
            (79.0, "mild"),      # Just below 80
            (80.0, "optimal"),   # Exactly 80
            (90.0, "optimal")    # Above 80
        ]
        
        for avg_score, expected_severity in test_cases:
            scores = {b: avg_score for b in biomarkers}
            description = rule._generate_cluster_description(biomarkers, scores)
            
            assert expected_severity in description.lower()
            assert "glucose" in description
            assert "hba1c" in description
            assert "insulin" in description
            # Should mention "2 others" for the 5th biomarker
            assert "2 others" in description
    
    def test_merge_overlapping_clusters_no_overlap(self):
        """Test merging clusters with no overlapping biomarkers."""
        engine = ClusteringRuleEngine()
        
        from core.models.biomarker import BiomarkerCluster
        
        cluster1 = BiomarkerCluster(
            cluster_id="cluster1",
            name="Cluster 1",
            biomarkers=["glucose", "hba1c"],
            description="Test cluster 1",
            severity="moderate",
            confidence=0.8
        )
        
        cluster2 = BiomarkerCluster(
            cluster_id="cluster2",
            name="Cluster 2",
            biomarkers=["total_cholesterol", "ldl_cholesterol"],
            description="Test cluster 2",
            severity="high",
            confidence=0.7
        )
        
        clusters = [cluster1, cluster2]
        merged = engine._merge_overlapping_clusters(clusters)
        
        # Should return original clusters since no overlap
        assert len(merged) == 2
        assert merged[0] == cluster1
        assert merged[1] == cluster2
    
    def test_merge_overlapping_clusters_single_cluster(self):
        """Test merging with single cluster."""
        engine = ClusteringRuleEngine()
        
        from core.models.biomarker import BiomarkerCluster
        
        cluster = BiomarkerCluster(
            cluster_id="cluster1",
            name="Cluster 1",
            biomarkers=["glucose", "hba1c"],
            description="Test cluster 1",
            severity="moderate",
            confidence=0.8
        )
        
        clusters = [cluster]
        merged = engine._merge_overlapping_clusters(clusters)
        
        # Should return original cluster
        assert len(merged) == 1
        assert merged[0] == cluster
    
    def test_merge_overlapping_clusters_empty_list(self):
        """Test merging with empty cluster list."""
        engine = ClusteringRuleEngine()
        
        clusters = []
        merged = engine._merge_overlapping_clusters(clusters)
        
        # Should return empty list
        assert len(merged) == 0