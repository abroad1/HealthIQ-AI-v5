"""
Unit tests for insight registry functionality.
"""

import pytest
from core.insights.registry import InsightRegistry, register_insight, insight_registry, ensure_insights_registered
from core.insights.base import BaseInsight
from core.insights.metadata import InsightMetadata, InsightResult
from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


class TestInsightRegistry:
    """Test insight registry functionality."""
    
    def test_registry_initialization(self):
        """Test registry initializes correctly."""
        registry = InsightRegistry()
        assert registry._registry == {}
        assert registry._instances == {}
    
    def test_register_insight(self):
        """Test registering an insight."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        assert "test_insight" in registry._registry
        assert "v1.0.0" in registry._registry["test_insight"]
        assert registry._registry["test_insight"]["v1.0.0"] == TestInsight
    
    def test_register_duplicate_raises_error(self):
        """Test registering duplicate insight raises ValueError."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        
        with pytest.raises(ValueError, match="already registered"):
            registry.register("test_insight", "v1.0.0", TestInsight)
    
    def test_get_insight(self):
        """Test getting insight instance."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        instance = registry.get("test_insight", "v1.0.0")
        
        assert isinstance(instance, TestInsight)
        assert instance.metadata.insight_id == "test_insight"
    
    def test_get_nonexistent_insight_raises_error(self):
        """Test getting nonexistent insight raises KeyError."""
        registry = InsightRegistry()
        
        with pytest.raises(KeyError, match="not registered"):
            registry.get("nonexistent", "v1.0.0")
    
    def test_get_all_insights(self):
        """Test getting all registered insights."""
        registry = InsightRegistry()
        
        class TestInsight1(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight_1",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        class TestInsight2(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight_2",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["insulin"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight_1", "v1.0.0", TestInsight1)
        registry.register("test_insight_2", "v1.0.0", TestInsight2)
        
        all_insights = registry.get_all()
        assert len(all_insights) == 2
        insight_ids = [insight.metadata.insight_id for insight in all_insights]
        assert "test_insight_1" in insight_ids
        assert "test_insight_2" in insight_ids
    
    def test_list_versions(self):
        """Test listing versions for an insight."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        registry.register("test_insight", "v2.0.0", TestInsight)
        
        versions = registry.list_versions("test_insight")
        assert "v1.0.0" in versions
        assert "v2.0.0" in versions
        assert len(versions) == 2
    
    def test_is_registered(self):
        """Test checking if insight is registered."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        
        assert registry.is_registered("test_insight", "v1.0.0")
        assert not registry.is_registered("test_insight", "v2.0.0")
        assert not registry.is_registered("nonexistent", "v1.0.0")
    
    def test_assert_registered(self):
        """Test asserting insight is registered."""
        registry = InsightRegistry()
        
        class TestInsight(BaseInsight):
            @property
            def metadata(self):
                return InsightMetadata(
                    insight_id="test_insight",
                    version="v1.0.0",
                    category="test",
                    required_biomarkers=["glucose"]
                )
            
            def analyze(self, context):
                return []
        
        registry.register("test_insight", "v1.0.0", TestInsight)
        
        # Should not raise
        registry.assert_registered("test_insight", "v1.0.0")
        
        # Should raise
        with pytest.raises(KeyError, match="not registered"):
            registry.assert_registered("nonexistent", "v1.0.0")


class TestRegisterInsightDecorator:
    """Test the register_insight decorator."""
    
    def test_decorator_registers_insight(self):
        """Test decorator registers insight correctly."""
        # Create a separate registry for this test to avoid interfering with other tests
        test_registry = InsightRegistry()
        
        # Temporarily replace the global registry for this test
        original_registry = insight_registry._registry
        original_instances = insight_registry._instances
        
        try:
            insight_registry._registry = test_registry._registry
            insight_registry._instances = test_registry._instances
            
            @register_insight("decorator_test", "v1.0.0")
            class DecoratorTestInsight(BaseInsight):
                @property
                def metadata(self):
                    return InsightMetadata(
                        insight_id="decorator_test",
                        version="v1.0.0",
                        category="test",
                        required_biomarkers=["glucose"]
                    )
                
                def analyze(self, context):
                    return []
            
            assert insight_registry.is_registered("decorator_test", "v1.0.0")
            instance = insight_registry.get("decorator_test", "v1.0.0")
            assert isinstance(instance, DecoratorTestInsight)
        finally:
            # Restore original registry
            insight_registry._registry = original_registry
            insight_registry._instances = original_instances


class TestInsightModules:
    """Test actual insight modules are registered."""
    
    @pytest.fixture(autouse=True)
    def ensure_insights_loaded(self):
        """Ensure all insight modules are registered before each test."""
        ensure_insights_registered()
    
    def test_metabolic_age_registered(self):
        """Test metabolic age insight is registered."""
        assert "metabolic_age" in insight_registry._registry
        assert "v1.0.0" in insight_registry._registry["metabolic_age"]
        instance = insight_registry.get("metabolic_age", "v1.0.0")
        assert instance.metadata.insight_id == "metabolic_age"
        assert instance.metadata.category == "metabolic"
    
    def test_heart_insight_registered(self):
        """Test heart insight is registered."""
        assert "heart_insight" in insight_registry._registry
        assert "v1.0.0" in insight_registry._registry["heart_insight"]
        instance = insight_registry.get("heart_insight", "v1.0.0")
        assert instance.metadata.insight_id == "heart_insight"
        assert instance.metadata.category == "cardiovascular"
    
    def test_inflammation_registered(self):
        """Test inflammation insight is registered."""
        assert "inflammation" in insight_registry._registry
        assert "v1.0.0" in insight_registry._registry["inflammation"]
        instance = insight_registry.get("inflammation", "v1.0.0")
        assert instance.metadata.insight_id == "inflammation"
        assert instance.metadata.category == "inflammatory"
    
    def test_fatigue_root_cause_registered(self):
        """Test fatigue root cause insight is registered."""
        assert "fatigue_root_cause" in insight_registry._registry
        assert "v1.0.0" in insight_registry._registry["fatigue_root_cause"]
        instance = insight_registry.get("fatigue_root_cause", "v1.0.0")
        assert instance.metadata.insight_id == "fatigue_root_cause"
        assert instance.metadata.category == "metabolic"
    
    def test_detox_filtration_registered(self):
        """Test detox filtration insight is registered."""
        assert "detox_filtration" in insight_registry._registry
        assert "v1.0.0" in insight_registry._registry["detox_filtration"]
        instance = insight_registry.get("detox_filtration", "v1.0.0")
        assert instance.metadata.insight_id == "detox_filtration"
        assert instance.metadata.category == "metabolic"
    
    def test_ensure_insights_registered(self):
        """Test ensure_insights_registered returns at least 5 insights."""
        all_insights = insight_registry.get_all()
        assert len(all_insights) >= 5
        insight_ids = [insight.metadata.insight_id for insight in all_insights]
        expected_insights = [
            "metabolic_age", "heart_insight", "inflammation", 
            "fatigue_root_cause", "detox_filtration"
        ]
        for expected in expected_insights:
            assert expected in insight_ids
