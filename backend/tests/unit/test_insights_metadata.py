"""
Unit tests for insight metadata and result models.
"""

import pytest
from core.insights.metadata import InsightMetadata, InsightResult


class TestInsightMetadata:
    """Test InsightMetadata dataclass."""
    
    def test_insight_metadata_creation(self):
        """Test creating InsightMetadata with all fields."""
        metadata = InsightMetadata(
            insight_id="test_insight",
            version="v1.2.0",
            category="metabolic",
            required_biomarkers=["glucose", "insulin"],
            optional_biomarkers=["hba1c"],
            description="Test insight description",
            author="Test Author",
            created_at="2024-01-30T00:00:00Z",
            updated_at="2024-01-30T00:00:00Z"
        )
        
        assert metadata.insight_id == "test_insight"
        assert metadata.version == "v1.2.0"
        assert metadata.category == "metabolic"
        assert metadata.required_biomarkers == ["glucose", "insulin"]
        assert metadata.optional_biomarkers == ["hba1c"]
        assert metadata.description == "Test insight description"
        assert metadata.author == "Test Author"
        assert metadata.created_at == "2024-01-30T00:00:00Z"
        assert metadata.updated_at == "2024-01-30T00:00:00Z"
    
    def test_insight_metadata_defaults(self):
        """Test InsightMetadata with default values."""
        metadata = InsightMetadata(
            insight_id="test_insight",
            version="v1.0.0",
            category="test",
            required_biomarkers=["glucose"]
        )
        
        assert metadata.optional_biomarkers is None
        assert metadata.description == ""
        assert metadata.author == "HealthIQ Team"
        assert metadata.created_at == ""
        assert metadata.updated_at == ""


class TestInsightResult:
    """Test InsightResult dataclass."""
    
    def test_insight_result_creation(self):
        """Test creating InsightResult with all fields."""
        result = InsightResult(
            insight_id="test_insight",
            version="v1.0.0",
            manifest_id="test_manifest",
            result_key="test_key",
            drivers={"glucose": 100, "insulin": 8.5},
            evidence={"metabolic_age": 35, "chronological_age": 30},
            biomarkers_involved=["glucose", "insulin"],
            confidence=0.85,
            severity="warning",
            error_code=None,
            error_detail=None
        )
        
        assert result.insight_id == "test_insight"
        assert result.version == "v1.0.0"
        assert result.manifest_id == "test_manifest"
        assert result.result_key == "test_key"
        assert result.drivers == {"glucose": 100, "insulin": 8.5}
        assert result.evidence == {"metabolic_age": 35, "chronological_age": 30}
        assert result.biomarkers_involved == ["glucose", "insulin"]
        assert result.confidence == 0.85
        assert result.severity == "warning"
        assert result.error_code is None
        assert result.error_detail is None
    
    def test_insight_result_defaults(self):
        """Test InsightResult with default values."""
        result = InsightResult(
            insight_id="test_insight",
            version="v1.0.0",
            manifest_id="test_manifest"
        )
        
        assert result.result_key is None
        assert result.drivers is None
        assert result.evidence is None
        assert result.biomarkers_involved is None
        assert result.confidence is None
        assert result.severity is None
        assert result.error_code is None
        assert result.error_detail is None
    
    def test_insight_result_error_case(self):
        """Test InsightResult for error case."""
        result = InsightResult(
            insight_id="test_insight",
            version="v1.0.0",
            manifest_id="test_manifest",
            error_code="CALCULATION_FAILED",
            error_detail="Division by zero error"
        )
        
        assert result.error_code == "CALCULATION_FAILED"
        assert result.error_detail == "Division by zero error"
        assert result.drivers is None
        assert result.evidence is None
        assert result.confidence is None
        assert result.severity is None
