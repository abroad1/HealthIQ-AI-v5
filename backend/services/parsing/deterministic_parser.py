"""
Deterministic biomarker parser for canonical CSV-ish format.

Parses lines in format: "marker,value,unit" (e.g., "ALT,42,U/L" or "HDL,1.0,mmol/L").
Trim whitespace, case-insensitive marker names. Returns structured biomarker list.
"""

import re
from typing import Dict, Any, List, Optional


def _parse_numeric_value(s: str) -> Optional[float]:
    """Parse a string as float, handling common formats."""
    s = (s or "").strip()
    if not s:
        return None
    # Remove trailing unit chars that might have bled into value (e.g. "42" from "42,U/L")
    try:
        return float(s)
    except ValueError:
        return None


def _looks_like_csv_biomarker_lines(text: str) -> bool:
    """
    Heuristic: text looks like one or more "marker,value,unit" lines.
    Each line has 3 comma-separated parts; middle part is numeric.
    """
    if not text or not text.strip():
        return False
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        return False
    # Require at least one line matching pattern
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3 and parts[0] and _parse_numeric_value(parts[1]) is not None:
            return True
    return False


def parse_csv_biomarker_lines(text: str) -> List[Dict[str, Any]]:
    """
    Parse text with lines in format "marker,value,unit".
    Returns list of biomarker dicts compatible with upload route expectations:
    {id, name, value, unit, referenceRange, confidence, ref_low, ref_high, healthStatus}
    """
    biomarkers: List[Dict[str, Any]] = []
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split(",", 2)]  # max 2 splits -> marker, value, unit
        if len(parts) < 3:
            continue
        marker_raw = parts[0]
        value_raw = parts[1]
        unit_raw = parts[2] if len(parts) > 2 else ""

        value = _parse_numeric_value(value_raw)
        if value is None:
            continue

        # Use trimmed marker as id; canonical resolution happens in upload route
        marker = marker_raw.strip() if marker_raw else ""
        if not marker:
            continue

        biomarkers.append({
            "id": marker,
            "name": marker,
            "value": value,
            "unit": unit_raw,
            "referenceRange": "",
            "confidence": 1.0,
            "ref_low": None,
            "ref_high": None,
            "healthStatus": "Unknown",
        })

    return biomarkers


def try_deterministic_parse(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    If text looks like CSV biomarker lines, parse deterministically.
    Returns list of biomarkers or None if format doesn't match.
    """
    if not _looks_like_csv_biomarker_lines(text):
        return None
    return parse_csv_biomarker_lines(text)
