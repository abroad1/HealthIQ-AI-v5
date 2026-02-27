"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module A: lab-range anchored z-score computation.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

BIO_STATS_ENGINE_VERSION = "1.0.0"


def _extract_numeric_value(row: Any, biomarker_id: str) -> float:
    if isinstance(row, dict):
        raw = row.get("value", row.get("measurement"))
    else:
        raw = row
    if not isinstance(raw, (int, float)):
        raise ValueError(f"bio_stats_engine: non-numeric value for {biomarker_id}")
    return float(raw)


def build_bio_stats_v1(
    *,
    biomarker_values: Mapping[str, Any],
    lab_reference_ranges: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Compute deterministic z-scores from lab ranges.

    Formula:
      mid = (low + high) / 2
      half_range = (high - low) / 2
      z = (value - mid) / half_range
    """
    output: Dict[str, Dict[str, Any]] = {}
    for biomarker_id in sorted(str(k) for k in biomarker_values.keys()):
        if biomarker_id not in lab_reference_ranges:
            raise ValueError(f"bio_stats_engine: missing lab reference range for {biomarker_id}")
        ref = lab_reference_ranges[biomarker_id]
        low = ref.get("min")
        high = ref.get("max")
        if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
            raise ValueError(f"bio_stats_engine: invalid min/max for {biomarker_id}")
        half_range = (float(high) - float(low)) / 2.0
        if half_range == 0:
            raise ValueError(f"bio_stats_engine: zero half_range for {biomarker_id}")
        value = _extract_numeric_value(biomarker_values[biomarker_id], biomarker_id)
        mid = (float(low) + float(high)) / 2.0
        z = (value - mid) / half_range
        clamped = False
        if z > 4.0:
            z = 4.0
            clamped = True
        elif z < -4.0:
            z = -4.0
            clamped = True
        output[biomarker_id] = {"z_score": float(z), "clamped": clamped}
    return output
