"""
Test canonical-only enforcement - ensures no non-canonical biomarker keys.
"""

import pytest
from core.canonical.normalize import BiomarkerNormalizer
from core.pipeline.orchestrator import AnalysisOrchestrator


class TestCanonicalOnlyEnforcement:
    """Test that canonical-only enforcement works correctly."""
    
    def test_normalizer_validates_canonical_keys(self):
        """Test that normalizer correctly identifies canonical vs non-canonical keys."""
        normalizer = BiomarkerNormalizer()
        
        # Test with canonical keys
        canonical_biomarkers = {
            "total_cholesterol": 200,
            "glucose": 95,
            "hdl_cholesterol": 45
        }
        
        non_canonical = normalizer.validate_canonical_only(canonical_biomarkers)
        assert len(non_canonical) == 0, f"Expected no non-canonical keys, got: {non_canonical}"
    
    def test_normalizer_detects_non_canonical_keys(self):
        """Test that normalizer detects non-canonical keys."""
        normalizer = BiomarkerNormalizer()
        
        # Test with non-canonical keys (aliases)
        non_canonical_biomarkers = {
            "cholesterol": 200,  # alias for total_cholesterol
            "blood_sugar": 95,   # alias for glucose
            "hdl": 45            # alias for hdl_cholesterol
        }
        
        non_canonical = normalizer.validate_canonical_only(non_canonical_biomarkers)
        assert len(non_canonical) == 3, f"Expected 3 non-canonical keys, got: {non_canonical}"
        assert "cholesterol" in non_canonical
        assert "blood_sugar" in non_canonical
        assert "hdl" in non_canonical
    
    def test_normalizer_maps_aliases_to_canonical(self):
        """Test that normalizer correctly maps aliases to canonical names."""
        normalizer = BiomarkerNormalizer()
        
        # Test with mixed canonical and alias keys
        mixed_biomarkers = {
            "total_cholesterol": 200,  # canonical
            "blood_sugar": 95,         # alias
            "hdl": 45                  # alias
        }
        
        panel, unmapped = normalizer.normalize_biomarkers(mixed_biomarkers)
        
        # Should have no unmapped keys
        assert len(unmapped) == 0, f"Expected no unmapped keys, got: {unmapped}"
        
        # Should have canonical keys in the panel
        assert "total_cholesterol" in panel.biomarkers
        assert "glucose" in panel.biomarkers  # blood_sugar -> glucose
        assert "hdl_cholesterol" in panel.biomarkers  # hdl -> hdl_cholesterol
        
        # Should not have alias keys
        assert "blood_sugar" not in panel.biomarkers
        assert "hdl" not in panel.biomarkers
    
    def test_orchestrator_enforces_canonical_only(self):
        """Test that orchestrator enforces canonical-only keys."""
        orchestrator = AnalysisOrchestrator()
        
        # Test with non-canonical keys - should raise ValueError
        non_canonical_biomarkers = {
            "cholesterol": 200,  # alias
            "blood_sugar": 95    # alias
        }
        
        user_data = {
            "user_id": "test_user",
            "age": 30,
            "gender": "male"
        }
        
        with pytest.raises(ValueError, match="Non-canonical biomarker keys found"):
            orchestrator.create_analysis_context(
                analysis_id="test_analysis",
                raw_biomarkers=non_canonical_biomarkers,
                user_data=user_data
            )
    
    def test_orchestrator_accepts_canonical_keys(self):
        """Test that orchestrator accepts canonical keys."""
        orchestrator = AnalysisOrchestrator()
        
        # Test with canonical keys - should succeed
        canonical_biomarkers = {
            "total_cholesterol": 200,
            "glucose": 95,
            "hdl_cholesterol": 45
        }
        
        user_data = {
            "user_id": "test_user",
            "age": 30,
            "gender": "male"
        }
        
        # Should not raise an exception
        context = orchestrator.create_analysis_context(
            analysis_id="test_analysis",
            raw_biomarkers=canonical_biomarkers,
            user_data=user_data
        )
        
        assert context.analysis_id == "test_analysis"
        assert len(context.biomarker_panel.biomarkers) == 3
        assert "total_cholesterol" in context.biomarker_panel.biomarkers
        assert "glucose" in context.biomarker_panel.biomarkers
        assert "hdl_cholesterol" in context.biomarker_panel.biomarkers
    
    def test_post_normalize_validation_fails_with_aliases(self):
        """Test that post-normalization validation fails if aliases remain."""
        normalizer = BiomarkerNormalizer()
        
        # Create a scenario where aliases might remain after normalization
        # This is a contrived test since normalize_biomarkers should handle this
        # but we want to ensure the validation catches any edge cases
        
        # Test with completely unknown keys
        unknown_biomarkers = {
            "unknown_biomarker_1": 100,
            "unknown_biomarker_2": 200
        }
        
        non_canonical = normalizer.validate_canonical_only(unknown_biomarkers)
        assert len(non_canonical) == 2
        assert "unknown_biomarker_1" in non_canonical
        assert "unknown_biomarker_2" in non_canonical
