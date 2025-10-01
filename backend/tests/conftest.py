"""
Pytest configuration and fixtures for backend tests.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
