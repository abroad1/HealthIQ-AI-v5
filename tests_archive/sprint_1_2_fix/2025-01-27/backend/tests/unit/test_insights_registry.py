# ARCHIVED TEST
# Reason: Medium-value test (registry mechanics, not business logic)
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_insights_registry.py

"""
Unit tests for insights registry
HealthIQ-AI v5 Backend
"""

import pytest
from unittest.mock import patch, MagicMock

from core.insights.registry import InsightRegistry, insight_registry
from core.insights.base import BaseInsight


class MockInsight(BaseInsight):
    """Mock insight class for testing"""
    
    def get_required_biomarkers(self):
        """Get required biomarkers for testing"""
        return ["total_cholesterol", "glucose"]
    
    def analyze(self, context):
        """Analyze context and generate mock insights"""
        from core.models.biomarker import BiomarkerInsight
        return [BiomarkerInsight(
            insight_id="test-insight-1",
            title="Test Insight",
            description="A test insight",
            biomarkers=["total_cholesterol"],
            category="test",
            severity="medium",
            confidence=0.8,
            recommendations=["test recommendation"]
        )]


class TestInsightRegistry:
    """Test insight registry functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.registry = InsightRegistry()
    
    def test_registry_initialization(self):
        """Test insight registry initializes correctly"""
        assert self.registry is not None
        assert hasattr(self.registry, 'register')
        assert hasattr(self.registry, 'get_insight')
        assert hasattr(self.registry, 'get_all_insights')
        assert hasattr(self.registry, 'get_insight_names')
        assert hasattr(self.registry, 'clear')
    
    def test_register_insight(self):
        """Test registering an insight class"""
        self.registry.register(MockInsight)
        
        assert "MockInsight" in self.registry._insights
        assert self.registry._insights["MockInsight"] == MockInsight
    
    def test_get_insight_success(self):
        """Test getting an insight instance successfully"""
        self.registry.register(MockInsight)
        
        insight = self.registry.get_insight("MockInsight")
        
        assert isinstance(insight, MockInsight)
        assert "MockInsight" in self.registry._instances
    
    def test_get_insight_not_registered(self):
        """Test getting an insight that's not registered"""
        with pytest.raises(KeyError, match="Insight generator 'NonExistent' not registered"):
            self.registry.get_insight("NonExistent")
    
    def test_get_insight_caching(self):
        """Test that insight instances are cached"""
        self.registry.register(MockInsight)
        
        insight1 = self.registry.get_insight("MockInsight")
        insight2 = self.registry.get_insight("MockInsight")
        
        assert insight1 is insight2  # Same instance
    
    def test_get_all_insights(self):
        """Test getting all insight instances"""
        self.registry.register(MockInsight)
        
        insights = self.registry.get_all_insights()
        
        assert isinstance(insights, list)
        assert len(insights) == 1
        assert isinstance(insights[0], MockInsight)
    
    def test_get_all_insights_empty(self):
        """Test getting all insights when none are registered"""
        insights = self.registry.get_all_insights()
        
        assert isinstance(insights, list)
        assert len(insights) == 0
    
    def test_get_insight_names(self):
        """Test getting insight names"""
        self.registry.register(MockInsight)
        
        names = self.registry.get_insight_names()
        
        assert isinstance(names, list)
        assert "MockInsight" in names
    
    def test_get_insight_names_empty(self):
        """Test getting insight names when none are registered"""
        names = self.registry.get_insight_names()
        
        assert isinstance(names, list)
        assert len(names) == 0
    
    def test_clear(self):
        """Test clearing the registry"""
        self.registry.register(MockInsight)
        self.registry.get_insight("MockInsight")  # Create instance
        
        self.registry.clear()
        
        assert len(self.registry._insights) == 0
        assert len(self.registry._instances) == 0
    
    def test_register_multiple_insights(self):
        """Test registering multiple insight classes"""
        class MockInsight2(BaseInsight):
            def generate_insights(self, data):
                return []
        
        self.registry.register(MockInsight)
        self.registry.register(MockInsight2)
        
        assert len(self.registry._insights) == 2
        assert "MockInsight" in self.registry._insights
        assert "MockInsight2" in self.registry._insights
    
    def test_get_insight_after_clear(self):
        """Test getting insight after clearing registry"""
        self.registry.register(MockInsight)
        self.registry.clear()
        
        with pytest.raises(KeyError):
            self.registry.get_insight("MockInsight")
    
    def test_insight_instance_creation(self):
        """Test that insight instances are created correctly"""
        self.registry.register(MockInsight)
        
        insight = self.registry.get_insight("MockInsight")
        
        # Test that the insight can analyze (using the correct method)
        from core.models.context import AnalysisContext
        from core.models.biomarker import BiomarkerPanel, BiomarkerValue
        from core.models.user import User
        
        user = User(user_id="test", age=30, gender="male")
        biomarkers = {
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL"),
            "glucose": BiomarkerValue(name="glucose", value=95, unit="mg/dL")
        }
        panel = BiomarkerPanel(biomarkers=biomarkers)
        context = AnalysisContext(
            analysis_id="test-analysis-1",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
        
        insights = insight.analyze(context)
        
        assert isinstance(insights, list)
        assert len(insights) == 1
        assert insights[0].title == "Test Insight"
    
    def test_insight_registry_global_instance(self):
        """Test the global insight registry instance"""
        assert insight_registry is not None
        assert isinstance(insight_registry, InsightRegistry)
    
    def test_register_invalid_class(self):
        """Test registering an invalid class"""
        class NotAnInsight:
            pass
        
        # Should not raise an error, but won't work properly
        self.registry.register(NotAnInsight)
        
        # Getting the insight should work (class can be instantiated)
        # but it won't have the required methods
        insight = self.registry.get_insight("NotAnInsight")
        assert isinstance(insight, NotAnInsight)
        
        # But it should fail when trying to use it as a BaseInsight
        with pytest.raises(AttributeError):
            insight.get_required_biomarkers()
    
    def test_get_insight_with_none_name(self):
        """Test getting insight with None name"""
        with pytest.raises(KeyError):
            self.registry.get_insight(None)
    
    def test_get_insight_with_empty_name(self):
        """Test getting insight with empty name"""
        with pytest.raises(KeyError):
            self.registry.get_insight("")
    
    def test_register_same_class_twice(self):
        """Test registering the same class twice"""
        self.registry.register(MockInsight)
        self.registry.register(MockInsight)  # Should overwrite
        
        assert len(self.registry._insights) == 1
        assert self.registry._insights["MockInsight"] == MockInsight
    
    def test_get_all_insights_with_multiple_classes(self):
        """Test getting all insights with multiple registered classes"""
        class MockInsight2(BaseInsight):
            def get_required_biomarkers(self):
                return ["hdl_cholesterol"]
            
            def analyze(self, context):
                return []
        
        class MockInsight3(BaseInsight):
            def get_required_biomarkers(self):
                return ["glucose"]
            
            def analyze(self, context):
                return []
        
        self.registry.register(MockInsight)
        self.registry.register(MockInsight2)
        self.registry.register(MockInsight3)
        
        insights = self.registry.get_all_insights()
        
        assert len(insights) == 3
        assert all(isinstance(insight, BaseInsight) for insight in insights)
    
    def test_insight_names_consistency(self):
        """Test that insight names are consistent"""
        self.registry.register(MockInsight)
        
        names1 = self.registry.get_insight_names()
        names2 = self.registry.get_insight_names()
        
        assert names1 == names2
        assert "MockInsight" in names1
    
    def test_clear_removes_instances(self):
        """Test that clear removes both classes and instances"""
        self.registry.register(MockInsight)
        self.registry.get_insight("MockInsight")  # Create instance
        
        assert len(self.registry._instances) == 1
        
        self.registry.clear()
        
        assert len(self.registry._instances) == 0
        assert len(self.registry._insights) == 0