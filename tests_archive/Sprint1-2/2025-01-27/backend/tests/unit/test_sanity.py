"""
Unit test sanity check for HealthIQ AI v5 backend.
ARCHIVED: 2025-01-27 - Sprint 1-2 Prerequisites Implementation
"""

import pytest


class TestSanity:
    """Basic sanity tests to verify unit test infrastructure."""

    def test_sanity_check(self):
        """Test that the unit test infrastructure is working."""
        assert True

    def test_basic_math(self):
        """Test basic mathematical operations."""
        assert 2 + 2 == 4
        assert 10 * 5 == 50

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works correctly."""
        assert True
