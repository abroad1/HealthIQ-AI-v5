"""
Sample analysis fixture for testing and development.
Provides in-memory JSON data without database dependencies.
"""

SAMPLE_ANALYSIS = {
    "analysis_id": "fixture-0001",
    "biomarkers": [
        {
            "biomarker_name": "glucose",
            "value": 5.0,
            "unit": "mmol/L",
            "score": 0.75,
            "percentile": 65.0,
            "status": "normal",
            "reference_range": {"min": 3.0, "max": 6.0, "unit": "mmol/L"},
            "interpretation": "Within normal range"
        },
        {
            "biomarker_name": "hdl_cholesterol",
            "value": 1.5,
            "unit": "mmol/L",
            "score": 0.85,
            "percentile": 80.0,
            "status": "normal",
            "reference_range": {"min": 1.0, "max": 2.0, "unit": "mmol/L"},
            "interpretation": "Good HDL levels"
        },
        {
            "biomarker_name": "ldl_cholesterol",
            "value": 3.0,
            "unit": "mmol/L",
            "score": 0.60,
            "percentile": 45.0,
            "status": "normal",
            "reference_range": {"min": 1.0, "max": 4.0, "unit": "mmol/L"},
            "interpretation": "Within acceptable range"
        },
        {
            "biomarker_name": "triglycerides",
            "value": 1.2,
            "unit": "mmol/L",
            "score": 0.70,
            "percentile": 55.0,
            "status": "normal",
            "reference_range": {"min": 0.3, "max": 1.7, "unit": "mmol/L"},
            "interpretation": "Healthy triglyceride levels"
        },
        {
            "biomarker_name": "total_cholesterol",
            "value": 4.8,
            "unit": "mmol/L",
            "score": 0.65,
            "percentile": 50.0,
            "status": "normal",
            "reference_range": {"min": 3.0, "max": 5.0, "unit": "mmol/L"},
            "interpretation": "Total cholesterol in normal range"
        },
        {
            "biomarker_name": "hba1c",
            "value": 33,
            "unit": "mmol/mol",
            "score": 0.80,
            "percentile": 70.0,
            "status": "normal",
            "reference_range": {"min": 20, "max": 42, "unit": "mmol/mol"},
            "interpretation": "Good long-term glucose control"
        }
    ],
    "reference_ranges": {
        "glucose": {"min": 3.0, "max": 6.0, "unit": "mmol/L"},
        "hdl_cholesterol": {"min": 1.0, "max": 2.0, "unit": "mmol/L"},
        "ldl_cholesterol": {"min": 1.0, "max": 4.0, "unit": "mmol/L"},
        "triglycerides": {"min": 0.3, "max": 1.7, "unit": "mmol/L"},
        "total_cholesterol": {"min": 3.0, "max": 5.0, "unit": "mmol/L"},
        "hba1c": {"min": 20, "max": 42, "unit": "mmol/mol"}
    },
    "overall_score": 0.72,
    "risk_assessment": {
        "cardiovascular_risk": "low",
        "metabolic_risk": "low",
        "overall_risk": "low"
    },
    "recommendations": [
        "Maintain current healthy lifestyle",
        "Continue regular exercise routine",
        "Monitor biomarkers annually"
    ],
    "created_at": "2025-10-19T10:00:00Z",
    "result_version": "1.0.0"
}
