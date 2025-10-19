"""
Analysis routes for biomarker processing and SSE streaming.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/fixture")
def load_fixture_analysis():
    """
    Load sample analysis data from fixture for testing and development.
    Returns in-memory JSON data without database dependencies.
    """
    from tests.fixtures.sample_analysis import SAMPLE_ANALYSIS
    return SAMPLE_ANALYSIS