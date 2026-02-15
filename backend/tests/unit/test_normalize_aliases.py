"""
Unit tests for alias normalization functionality.

Tests the normalization logic to ensure proper handling of unmapped biomarkers
and prevention of recursive unmapped prefixing.
"""

import pytest
from core.canonical.normalize import BiomarkerNormalizer, normalize_panel


class TestNormalizeAliases:
    """Test cases for alias normalization."""
    
    def test_double_unmapped_prefix_prevention(self):
        """Test that already unmapped biomarkers don't get double prefixes."""
        normalizer = BiomarkerNormalizer()
        input_data = {"unmapped_calcium_(venous)": 1.2}
        result = normalizer.normalize_biomarkers(input_data)
        
        # Check that no double unmapped prefixes exist
        panel = result[0]  # Get the BiomarkerPanel
        for key in panel.biomarkers.keys():
            assert not key.startswith("unmapped_unmapped_"), f"Found double unmapped prefix: {key}"
    
    def test_normalize_panel_unmapped_prevention(self):
        """Test that normalize_panel doesn't re-process unmapped biomarkers."""
        input_data = {"unmapped_calcium_(venous)": 1.2}
        result = normalize_panel(input_data)
        
        # Should return the same data without processing
        assert result == input_data
        assert "unmapped_calcium_(venous)" in result
        assert result["unmapped_calcium_(venous)"] == 1.2
    
    def test_mixed_unmapped_and_normal_biomarkers(self):
        """Test handling of mixed unmapped and normal biomarkers."""
        normalizer = BiomarkerNormalizer()
        input_data = {
            "unmapped_calcium_(venous)": 1.2,
            "HDL": 45.0,
            "unmapped_unknown_test": 10.0
        }
        
        result = normalizer.normalize_biomarkers(input_data)
        panel = result[0]
        unmapped_keys = result[1]
        
        # Check that unmapped biomarkers are preserved
        assert "unmapped_calcium_(venous)" in panel.biomarkers
        assert "unmapped_unknown_test" in panel.biomarkers
        
        # Check that normal biomarkers are processed (HDL -> hdl_cholesterol per PR)
        assert "hdl_cholesterol" in panel.biomarkers
        
        # Check unmapped keys list
        assert "unmapped_calcium_(venous)" in unmapped_keys
        assert "unmapped_unknown_test" in unmapped_keys
        assert "HDL" not in unmapped_keys  # HDL should be mapped
    
    def test_no_double_processing_of_unmapped(self):
        """Test that unmapped biomarkers are not processed twice."""
        normalizer = BiomarkerNormalizer()
        input_data = {"unmapped_calcium_(venous)": 1.2}
        
        # Process once
        result1 = normalizer.normalize_biomarkers(input_data)
        panel1 = result1[0]
        
        # Process the result again (simulating double processing)
        panel_dict = {name: value.value for name, value in panel1.biomarkers.items()}
        result2 = normalizer.normalize_biomarkers(panel_dict)
        panel2 = result2[0]
        
        # Check that no double prefixes were created
        for key in panel2.biomarkers.keys():
            assert not key.startswith("unmapped_unmapped_"), f"Found double unmapped prefix: {key}"
            assert not key.startswith("unmapped_unmapped_unmapped_"), f"Found triple unmapped prefix: {key}"
    
    def test_normalize_panel_skips_unmapped_entirely(self):
        """Test that normalize_panel completely skips processing if unmapped biomarkers present."""
        input_data = {
            "unmapped_calcium_(venous)": 1.2,
            "HDL": 45.0
        }
        
        result = normalize_panel(input_data)
        
        # Should return exactly the same data without any processing
        assert result == input_data
        assert "unmapped_calcium_(venous)" in result
        assert "HDL" in result  # Should not be converted to "hdl"
    
    def test_guard_clause_prevents_recursion(self):
        """Test that the guard clause prevents recursive processing."""
        normalizer = BiomarkerNormalizer()
        # Test with various unmapped prefixes
        test_cases = [
            "unmapped_calcium_(venous)",
            "unmapped_unknown_biomarker",
            "unmapped_test_value",
            "unmapped_",
        ]
        
        for test_key in test_cases:
            input_data = {test_key: 1.2}
            result = normalizer.normalize_biomarkers(input_data)
            panel = result[0]
            
            # Should preserve the original key without adding more prefixes
            assert test_key in panel.biomarkers
            assert not any(key.startswith("unmapped_unmapped_") for key in panel.biomarkers.keys())
    
    def test_normal_biomarkers_still_processed(self):
        """Test that normal biomarkers are still processed correctly."""
        normalizer = BiomarkerNormalizer()
        input_data = {
            "HDL": 45.0,
            "LDL Cholesterol": 120.0,
            "Total Cholesterol": 200.0
        }
        
        result = normalizer.normalize_biomarkers(input_data)
        panel = result[0]
        
        # Should convert to canonical names (hdl/ldl -> hdl_cholesterol/ldl_cholesterol per PR)
        assert "hdl_cholesterol" in panel.biomarkers
        assert "ldl_cholesterol" in panel.biomarkers
        assert "total_cholesterol" in panel.biomarkers
        
        # Should not have unmapped prefixes for known biomarkers
        for key in panel.biomarkers.keys():
            if not key.startswith("unmapped_"):
                assert key in ["hdl_cholesterol", "ldl_cholesterol", "total_cholesterol"]
    
    def test_venous_aliases_resolve_to_canonical(self):
        """Test that _(venous) variants resolve to correct canonical IDs."""
        normalizer = BiomarkerNormalizer()
        
        # Test all required _(venous) aliases
        test_cases = [
            ("c-reactive_protein_crp_(venous)", "crp"),
            ("total_creatine_kinese_ck_(venous)", "creatine_kinase"),
            ("magnesium_(venous)", "magnesium"),
            ("potassium_(venous)", "potassium"),
            ("calcium_(venous)", "calcium"),
            ("sodium_(venous)", "sodium"),
            ("chloride_(venous)", "chloride"),
            ("corrected_calcium_(venous)", "corrected_calcium"),
            ("triglycerides_(venous)", "triglycerides"),  # Already working
        ]
        
        for raw_key, expected_canonical in test_cases:
            input_data = {raw_key: 100.0}
            result = normalizer.normalize_biomarkers(input_data)
            panel = result[0]
            unmapped_keys = result[1]
            
            # Should resolve to canonical name, not unmapped
            assert expected_canonical in panel.biomarkers, \
                f"Failed to resolve '{raw_key}' to '{expected_canonical}'. Got keys: {list(panel.biomarkers.keys())}"
            assert raw_key not in unmapped_keys, \
                f"'{raw_key}' should not be in unmapped_keys"
            assert not any(key.startswith("unmapped_") for key in panel.biomarkers.keys() if expected_canonical in key), \
                f"'{raw_key}' should not produce unmapped_ prefix"
    
    def test_venous_aliases_preserve_values(self):
        """Test that _(venous) aliases preserve biomarker values correctly."""
        normalizer = BiomarkerNormalizer()
        
        input_data = {
            "c-reactive_protein_crp_(venous)": 2.5,
            "magnesium_(venous)": 1.8,
            "calcium_(venous)": 9.5,
        }
        
        result = normalizer.normalize_biomarkers(input_data)
        panel = result[0]
        
        # Check values are preserved
        assert panel.biomarkers["crp"].value == 2.5
        assert panel.biomarkers["magnesium"].value == 1.8
        assert panel.biomarkers["calcium"].value == 9.5