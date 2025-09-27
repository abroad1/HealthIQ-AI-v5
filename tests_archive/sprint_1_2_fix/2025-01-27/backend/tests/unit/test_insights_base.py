# ARCHIVED TEST
# Reason: Medium-value test (framework test)
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_insights_base.py

"""
Unit tests for insights base
HealthIQ-AI v5 Backend
"""

import pytest
from unittest.mock import patch, MagicMock

from core.insights.base import BaseInsight
from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerInsight, BiomarkerPanel, BiomarkerValue
from core.models.user import User


class ConcreteInsight(BaseInsight):
    """Concrete implementation of BaseInsight for testing"""
    
    def get_required_biomarkers(self):
        """Get required biomarkers for testing"""
        return ["total_cholesterol", "glucose"]
    
    def analyze(self, context):
        """Analyze context and generate mock insights"""
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


class TestBaseInsight:
    """Test BaseInsight functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.insight = ConcreteInsight()
        
        # Create test context
        user = User(user_id="test", age=30, gender="male")
        biomarkers = {
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL"),
            "glucose": BiomarkerValue(name="glucose", value=95, unit="mg/dL")
        }
        panel = BiomarkerPanel(biomarkers=biomarkers)
        self.context = AnalysisContext(
            analysis_id="test-analysis-1",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
    
    def test_get_insight_name(self):
        """Test getting insight name"""
        name = self.insight.get_insight_name()
        
        assert isinstance(name, str)
        assert name == "ConcreteInsight"
    
    def test_get_insight_category(self):
        """Test getting insight category"""
        category = self.insight.get_insight_category()
        
        assert isinstance(category, str)
        assert category == "general"
    
    def test_can_analyze_with_all_required_biomarkers(self):
        """Test can_analyze when all required biomarkers are available"""
        can_analyze = self.insight.can_analyze(self.context)
        
        assert can_analyze is True
    
    def test_can_analyze_with_missing_biomarkers(self):
        """Test can_analyze when some required biomarkers are missing"""
        # Create context with missing biomarkers
        user = User(user_id="test", age=30, gender="male")
        biomarkers = {
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL")
            # Missing glucose
        }
        panel = BiomarkerPanel(biomarkers=biomarkers)
        context = AnalysisContext(
            analysis_id="test-analysis-2",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
        
        can_analyze = self.insight.can_analyze(context)
        
        assert can_analyze is False
    
    def test_can_analyze_with_no_biomarkers(self):
        """Test can_analyze when no biomarkers are available"""
        # Create context with no biomarkers
        user = User(user_id="test", age=30, gender="male")
        panel = BiomarkerPanel(biomarkers={})
        context = AnalysisContext(
            analysis_id="test-analysis-3",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
        
        can_analyze = self.insight.can_analyze(context)
        
        assert can_analyze is False
    
    def test_can_analyze_with_extra_biomarkers(self):
        """Test can_analyze when extra biomarkers are available"""
        # Create context with extra biomarkers
        user = User(user_id="test", age=30, gender="male")
        biomarkers = {
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL"),
            "glucose": BiomarkerValue(name="glucose", value=95, unit="mg/dL"),
            "hdl_cholesterol": BiomarkerValue(name="hdl_cholesterol", value=60, unit="mg/dL")
        }
        panel = BiomarkerPanel(biomarkers=biomarkers)
        context = AnalysisContext(
            analysis_id="test-analysis-4",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
        
        can_analyze = self.insight.can_analyze(context)
        
        assert can_analyze is True
    
    def test_analyze_method(self):
        """Test analyze method implementation"""
        insights = self.insight.analyze(self.context)
        
        assert isinstance(insights, list)
        assert len(insights) == 1
        assert isinstance(insights[0], BiomarkerInsight)
        assert insights[0].title == "Test Insight"
    
    def test_get_required_biomarkers_method(self):
        """Test get_required_biomarkers method implementation"""
        biomarkers = self.insight.get_required_biomarkers()
        
        assert isinstance(biomarkers, list)
        assert "total_cholesterol" in biomarkers
        assert "glucose" in biomarkers
        assert len(biomarkers) == 2
    
    def test_can_analyze_with_empty_required_biomarkers(self):
        """Test can_analyze when insight requires no biomarkers"""
        class NoBiomarkerInsight(BaseInsight):
            def get_required_biomarkers(self):
                return []
            
            def analyze(self, context):
                return []
        
        insight = NoBiomarkerInsight()
        can_analyze = insight.can_analyze(self.context)
        
        assert can_analyze is True
    
    def test_can_analyze_with_none_required_biomarkers(self):
        """Test can_analyze when insight returns None for required biomarkers"""
        class NoneBiomarkerInsight(BaseInsight):
            def get_required_biomarkers(self):
                return None
            
            def analyze(self, context):
                return []
        
        insight = NoneBiomarkerInsight()
        
        # This should handle None gracefully
        with pytest.raises(TypeError):
            insight.can_analyze(self.context)
    
    def test_can_analyze_performance(self):
        """Test can_analyze performance with many biomarkers"""
        import time
        
        # Create context with many biomarkers
        user = User(user_id="test", age=30, gender="male")
        biomarkers = {}
        for i in range(1000):
            biomarkers[f"biomarker_{i}"] = BiomarkerValue(
                name=f"biomarker_{i}", 
                value=100, 
                unit="mg/dL"
            )
        
        # Add required biomarkers
        biomarkers["total_cholesterol"] = BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL")
        biomarkers["glucose"] = BiomarkerValue(name="glucose", value=95, unit="mg/dL")
        
        panel = BiomarkerPanel(biomarkers=biomarkers)
        context = AnalysisContext(
            analysis_id="test-analysis-5",
            user=user, 
            biomarker_panel=panel,
            created_at="2025-01-27T10:00:00Z"
        )
        
        start_time = time.time()
        can_analyze = self.insight.can_analyze(context)
        end_time = time.time()
        
        assert can_analyze is True
        # Should be fast (less than 100ms)
        assert (end_time - start_time) < 0.1
    
    def test_abstract_class_cannot_be_instantiated(self):
        """Test that BaseInsight cannot be instantiated directly"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseInsight()
    
    def test_concrete_class_can_be_instantiated(self):
        """Test that concrete implementation can be instantiated"""
        insight = ConcreteInsight()
        assert isinstance(insight, BaseInsight)
        assert isinstance(insight, ConcreteInsight)
    
    def test_get_insight_name_different_classes(self):
        """Test that different classes return different names"""
        class AnotherInsight(BaseInsight):
            def get_required_biomarkers(self):
                return []
            
            def analyze(self, context):
                return []
        
        insight1 = ConcreteInsight()
        insight2 = AnotherInsight()
        
        assert insight1.get_insight_name() == "ConcreteInsight"
        assert insight2.get_insight_name() == "AnotherInsight"
        assert insight1.get_insight_name() != insight2.get_insight_name()
    
    def test_get_insight_category_override(self):
        """Test that subclasses can override get_insight_category"""
        class CustomCategoryInsight(BaseInsight):
            def get_required_biomarkers(self):
                return []
            
            def analyze(self, context):
                return []
            
            def get_insight_category(self):
                return "custom_category"
        
        insight = CustomCategoryInsight()
        category = insight.get_insight_category()
        
        assert category == "custom_category"
        assert category != "general"