"""
Pytest configuration and fixtures for backend tests.
"""

import sys
import os
import pytest
from pathlib import Path

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session", autouse=True)
def _register_insights_once():
    """Ensure all insight modules are registered before any tests run."""
    from core.insights.registry import ensure_insights_registered
    ensure_insights_registered()
