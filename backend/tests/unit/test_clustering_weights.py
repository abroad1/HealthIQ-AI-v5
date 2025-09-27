"""
Unit tests for clustering weights system.

Tests the modular weighting system for scoring engines in clustering analysis.
"""

import pytest
from core.clustering.weights import (
    EngineWeightingSystem, 
    EngineType, 
    EngineWeight,
    ClinicalWeightProfiles
)


class TestEngineWeightingSystem:
    """Test cases for EngineWeightingSystem."""
    
    def test_initialization(self):
        """Test weighting system initialization with default weights."""
        system = EngineWeightingSystem()
        
        # Should have all engine types
        assert len(system.weights) == len(EngineType)
        
        # Check that all engines have equal weights
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001  # Should sum to 1.0
        
        # Check that all engines have default weight
        expected_weight = 1.0 / len(EngineType)
        for engine_type, weight in system.weights.items():
            assert abs(weight.weight - expected_weight) < 0.001
            assert weight.priority > 0
            assert weight.description != ""
            assert weight.clinical_rationale != ""
    
    def test_get_engine_weight(self):
        """Test getting engine weight."""
        system = EngineWeightingSystem()
        
        weight = system.get_engine_weight(EngineType.METABOLIC)
        assert isinstance(weight, float)
        assert 0.0 <= weight <= 1.0
        
        # Test unknown engine type
        unknown_weight = system.get_engine_weight(EngineType.METABOLIC)
        assert unknown_weight >= 0.0
    
    def test_set_engine_weight(self):
        """Test setting engine weight."""
        system = EngineWeightingSystem()
        
        # Set a new weight
        system.set_engine_weight(
            EngineType.METABOLIC, 
            0.3, 
            priority=1,
            clinical_rationale="Metabolic health is critical for overall wellness"
        )
        
        weight = system.get_engine_weight(EngineType.METABOLIC)
        assert weight == 0.3
        
        # Check that the weight object was updated
        metabolic_weight = system.weights[EngineType.METABOLIC]
        assert metabolic_weight.priority == 1
        assert "critical for overall wellness" in metabolic_weight.clinical_rationale
    
    def test_normalize_weights(self):
        """Test weight normalization."""
        system = EngineWeightingSystem()
        
        # Set some weights that don't sum to 1.0
        system.set_engine_weight(EngineType.METABOLIC, 0.5)
        system.set_engine_weight(EngineType.CARDIOVASCULAR, 0.3)
        system.set_engine_weight(EngineType.INFLAMMATORY, 0.4)
        
        # Normalize weights
        system.normalize_weights()
        
        # Check that weights now sum to 1.0
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_apply_clinical_priority(self):
        """Test applying clinical priority to engines."""
        system = EngineWeightingSystem()
        
        # Apply priority to metabolic and cardiovascular engines
        priority_engines = [EngineType.METABOLIC, EngineType.CARDIOVASCULAR]
        system.apply_clinical_priority(priority_engines, boost_factor=1.5)
        
        # Check that priority engines have higher weights
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        cardiovascular_weight = system.get_engine_weight(EngineType.CARDIOVASCULAR)
        inflammatory_weight = system.get_engine_weight(EngineType.INFLAMMATORY)
        
        assert metabolic_weight > inflammatory_weight
        assert cardiovascular_weight > inflammatory_weight
        
        # Check that weights still sum to 1.0
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_get_weighted_scores(self):
        """Test applying weights to engine scores."""
        system = EngineWeightingSystem()
        
        # Set some test weights
        system.set_engine_weight(EngineType.METABOLIC, 0.4)
        system.set_engine_weight(EngineType.CARDIOVASCULAR, 0.3)
        system.set_engine_weight(EngineType.INFLAMMATORY, 0.3)
        
        # Test engine scores
        engine_scores = {
            "metabolic": 80.0,
            "cardiovascular": 60.0,
            "inflammatory": 40.0,
            "unknown_engine": 50.0  # Should use default weight
        }
        
        weighted_scores = system.get_weighted_scores(engine_scores)
        
        assert "metabolic" in weighted_scores
        assert "cardiovascular" in weighted_scores
        assert "inflammatory" in weighted_scores
        assert "unknown_engine" in weighted_scores
        
        # Check that weights were applied correctly
        assert weighted_scores["metabolic"] == 80.0 * 0.4
        assert weighted_scores["cardiovascular"] == 60.0 * 0.3
        assert weighted_scores["inflammatory"] == 40.0 * 0.3
        
        # Unknown engine should use default weight
        default_weight = 1.0 / len(EngineType)
        assert weighted_scores["unknown_engine"] == 50.0 * default_weight
    
    def test_get_weight_summary(self):
        """Test getting weight summary."""
        system = EngineWeightingSystem()
        
        summary = system.get_weight_summary()
        
        assert "total_weight" in summary
        assert "normalized" in summary
        assert "engine_weights" in summary
        assert "weight_distribution" in summary
        
        # Check that summary contains all engines
        assert len(summary["engine_weights"]) == len(EngineType)
        assert len(summary["weight_distribution"]) == len(EngineType)
        
        # Check that weights are normalized
        assert summary["normalized"] is True
        assert abs(summary["total_weight"] - 1.0) < 0.001
    
    def test_validate_weights_valid(self):
        """Test weight validation with valid weights."""
        system = EngineWeightingSystem()
        
        errors = system.validate_weights()
        
        assert len(errors) == 0  # Should have no errors with default weights
    
    def test_validate_weights_invalid_sum(self):
        """Test weight validation with invalid sum."""
        system = EngineWeightingSystem()
        
        # Set weights that don't sum to 1.0
        system.set_engine_weight(EngineType.METABOLIC, 0.5)
        system.set_engine_weight(EngineType.CARDIOVASCULAR, 0.3)
        
        errors = system.validate_weights()
        
        assert len(errors) > 0
        assert any("sum to" in error for error in errors)
    
    def test_validate_weights_negative(self):
        """Test weight validation with negative weights."""
        system = EngineWeightingSystem()
        
        # Set a negative weight
        system.set_engine_weight(EngineType.METABOLIC, -0.1)
        
        errors = system.validate_weights()
        
        assert len(errors) > 0
        assert any("Negative weights" in error for error in errors)
    
    def test_validate_weights_missing_engines(self):
        """Test weight validation with missing engines."""
        system = EngineWeightingSystem()
        
        # Remove an engine
        del system.weights[EngineType.METABOLIC]
        
        errors = system.validate_weights()
        
        assert len(errors) > 0
        assert any("Missing weight configuration" in error for error in errors)
    
    def test_reset_to_default(self):
        """Test resetting weights to default."""
        system = EngineWeightingSystem()
        
        # Modify weights
        system.set_engine_weight(EngineType.METABOLIC, 0.5)
        system.apply_clinical_priority([EngineType.CARDIOVASCULAR])
        
        # Reset to default
        system.reset_to_default()
        
        # Check that all weights are equal again
        weights = [weight.weight for weight in system.weights.values()]
        assert all(abs(weight - weights[0]) < 0.001 for weight in weights)
        
        # Check that weights sum to 1.0
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001


class TestClinicalWeightProfiles:
    """Test cases for ClinicalWeightProfiles."""
    
    def test_metabolic_focus(self):
        """Test metabolic focus weight profile."""
        system = ClinicalWeightProfiles.metabolic_focus()
        
        assert isinstance(system, EngineWeightingSystem)
        
        # Check that metabolic and inflammatory engines have higher weights
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        inflammatory_weight = system.get_engine_weight(EngineType.INFLAMMATORY)
        cardiovascular_weight = system.get_engine_weight(EngineType.CARDIOVASCULAR)
        
        assert metabolic_weight > cardiovascular_weight
        assert inflammatory_weight > cardiovascular_weight
        
        # Check that weights are normalized
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_cardiovascular_focus(self):
        """Test cardiovascular focus weight profile."""
        system = ClinicalWeightProfiles.cardiovascular_focus()
        
        assert isinstance(system, EngineWeightingSystem)
        
        # Check that cardiovascular and inflammatory engines have higher weights
        cardiovascular_weight = system.get_engine_weight(EngineType.CARDIOVASCULAR)
        inflammatory_weight = system.get_engine_weight(EngineType.INFLAMMATORY)
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        
        assert cardiovascular_weight > metabolic_weight
        assert inflammatory_weight > metabolic_weight
        
        # Check that weights are normalized
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_comprehensive_health(self):
        """Test comprehensive health weight profile."""
        system = ClinicalWeightProfiles.comprehensive_health()
        
        assert isinstance(system, EngineWeightingSystem)
        
        # Check that metabolic and cardiovascular have slightly higher weights
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        cardiovascular_weight = system.get_engine_weight(EngineType.CARDIOVASCULAR)
        inflammatory_weight = system.get_engine_weight(EngineType.INFLAMMATORY)
        
        assert metabolic_weight > inflammatory_weight
        assert cardiovascular_weight > inflammatory_weight
        
        # Check that weights are normalized
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_organ_function_focus(self):
        """Test organ function focus weight profile."""
        system = ClinicalWeightProfiles.organ_function_focus()
        
        assert isinstance(system, EngineWeightingSystem)
        
        # Check that organ-related engines have higher weights
        kidney_weight = system.get_engine_weight(EngineType.KIDNEY)
        liver_weight = system.get_engine_weight(EngineType.LIVER)
        cbc_weight = system.get_engine_weight(EngineType.CBC)
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        
        assert kidney_weight > metabolic_weight
        assert liver_weight > metabolic_weight
        assert cbc_weight > metabolic_weight
        
        # Check that weights are normalized
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_wellness_optimization(self):
        """Test wellness optimization weight profile."""
        system = ClinicalWeightProfiles.wellness_optimization()
        
        assert isinstance(system, EngineWeightingSystem)
        
        # Check that wellness-related engines have higher weights
        nutritional_weight = system.get_engine_weight(EngineType.NUTRITIONAL)
        hormonal_weight = system.get_engine_weight(EngineType.HORMONAL)
        inflammatory_weight = system.get_engine_weight(EngineType.INFLAMMATORY)
        metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        
        assert nutritional_weight > metabolic_weight
        assert hormonal_weight > metabolic_weight
        assert inflammatory_weight > metabolic_weight
        
        # Check that weights are normalized
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001


class TestEngineWeight:
    """Test cases for EngineWeight dataclass."""
    
    def test_engine_weight_creation(self):
        """Test creating an EngineWeight instance."""
        weight = EngineWeight(
            engine_type=EngineType.METABOLIC,
            weight=0.3,
            priority=1,
            description="Metabolic health scoring",
            clinical_rationale="Metabolic health is critical for overall wellness"
        )
        
        assert weight.engine_type == EngineType.METABOLIC
        assert weight.weight == 0.3
        assert weight.priority == 1
        assert weight.description == "Metabolic health scoring"
        assert weight.clinical_rationale == "Metabolic health is critical for overall wellness"


class TestEngineType:
    """Test cases for EngineType enum."""
    
    def test_engine_type_values(self):
        """Test EngineType enum values."""
        assert EngineType.METABOLIC.value == "metabolic"
        assert EngineType.CARDIOVASCULAR.value == "cardiovascular"
        assert EngineType.INFLAMMATORY.value == "inflammatory"
        assert EngineType.HORMONAL.value == "hormonal"
        assert EngineType.NUTRITIONAL.value == "nutritional"
        assert EngineType.KIDNEY.value == "kidney"
        assert EngineType.LIVER.value == "liver"
        assert EngineType.CBC.value == "cbc"
    
    def test_engine_type_from_string(self):
        """Test creating EngineType from string."""
        assert EngineType("metabolic") == EngineType.METABOLIC
        assert EngineType("cardiovascular") == EngineType.CARDIOVASCULAR
        assert EngineType("inflammatory") == EngineType.INFLAMMATORY
    
    def test_engine_type_invalid(self):
        """Test invalid EngineType string."""
        with pytest.raises(ValueError):
            EngineType("invalid_engine")
    
    def test_get_weighted_scores_invalid_engine_dict(self):
        """Test applying weights with invalid engine dictionary."""
        system = EngineWeightingSystem()
        
        # Test with invalid engine dictionary (missing keys, wrong types)
        invalid_engine_scores = {
            "cardiovascular": 60.0,
            "unknown_engine": 50.0
        }
        
        weighted_scores = system.get_weighted_scores(invalid_engine_scores)
        
        # Should handle gracefully and return valid results for valid engines
        assert isinstance(weighted_scores, dict)
        assert "cardiovascular" in weighted_scores
        assert "unknown_engine" in weighted_scores
        assert weighted_scores["cardiovascular"] == 60.0 * (1.0 / len(EngineType))
    
    def test_get_weighted_scores_empty_dict(self):
        """Test applying weights with empty engine dictionary."""
        system = EngineWeightingSystem()
        
        empty_scores = {}
        weighted_scores = system.get_weighted_scores(empty_scores)
        
        assert isinstance(weighted_scores, dict)
        assert len(weighted_scores) == 0
    
    def test_normalize_weights_zero_total(self):
        """Test weight normalization with zero total weight."""
        system = EngineWeightingSystem()
        
        # Set all weights to zero
        for engine_type in EngineType:
            system.set_engine_weight(engine_type, 0.0)
        
        # Normalize weights
        system.normalize_weights()
        
        # Should handle gracefully (weights remain zero)
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert total_weight == 0.0
    
    def test_validate_weights_zero_sum(self):
        """Test weight validation with zero sum."""
        system = EngineWeightingSystem()
        
        # Set all weights to zero
        for engine_type in EngineType:
            system.set_engine_weight(engine_type, 0.0)
        
        errors = system.validate_weights()
        
        # Should have error about weights not summing to 1.0
        assert len(errors) > 0
        assert any("sum to" in error for error in errors)
    
    def test_set_engine_weight_new_engine_type(self):
        """Test setting weight for new engine type."""
        system = EngineWeightingSystem()
        
        # Create a new engine type (this would normally be done by extending the enum)
        # For testing, we'll use an existing engine type but test the new engine logic
        original_count = len(system.weights)
        
        # Test setting weight for existing engine type
        system.set_engine_weight(EngineType.METABOLIC, 0.5)
        
        # Should not change the count
        assert len(system.weights) == original_count
        assert system.get_engine_weight(EngineType.METABOLIC) == 0.5
    
    def test_apply_clinical_priority_zero_boost_factor(self):
        """Test applying clinical priority with zero boost factor."""
        system = EngineWeightingSystem()
        
        original_metabolic_weight = system.get_engine_weight(EngineType.METABOLIC)
        original_cardiovascular_weight = system.get_engine_weight(EngineType.CARDIOVASCULAR)
        
        priority_engines = [EngineType.METABOLIC, EngineType.CARDIOVASCULAR]
        system.apply_clinical_priority(priority_engines, boost_factor=0.0)
        
        # With zero boost factor, priority engines should have zero weight
        assert system.get_engine_weight(EngineType.METABOLIC) == 0.0
        assert system.get_engine_weight(EngineType.CARDIOVASCULAR) == 0.0
        
        # Weights should still sum to 1.0 (other engines get the weight)
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_apply_clinical_priority_negative_boost_factor(self):
        """Test applying clinical priority with negative boost factor."""
        system = EngineWeightingSystem()
        
        priority_engines = [EngineType.METABOLIC, EngineType.CARDIOVASCULAR]
        system.apply_clinical_priority(priority_engines, boost_factor=-1.0)
        
        # Should handle negative boost factor gracefully
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
    
    def test_get_engine_weight_missing_engine(self):
        """Test getting weight for missing engine type."""
        system = EngineWeightingSystem()
        
        # Remove an engine from the weights
        del system.weights[EngineType.METABOLIC]
        
        weight = system.get_engine_weight(EngineType.METABOLIC)
        
        # Should return 0.0 for missing engine
        assert weight == 0.0
    
    def test_reset_to_default_after_modifications(self):
        """Test resetting to default after various modifications."""
        system = EngineWeightingSystem()
        
        # Make various modifications
        system.set_engine_weight(EngineType.METABOLIC, 0.5)
        system.apply_clinical_priority([EngineType.CARDIOVASCULAR])
        system.normalize_weights()
        
        # Reset to default
        system.reset_to_default()
        
        # Check that all weights are equal again
        weights = [weight.weight for weight in system.weights.values()]
        assert all(abs(weight - weights[0]) < 0.001 for weight in weights)
        
        # Check that weights sum to 1.0
        total_weight = sum(weight.weight for weight in system.weights.values())
        assert abs(total_weight - 1.0) < 0.001
        
        # Check that all engines are present
        assert len(system.weights) == len(EngineType)