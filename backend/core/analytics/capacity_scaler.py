"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module D: convert adjusted burden into 0..100 capacity integers.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Mapping

CAPACITY_SCALER_VERSION = "1.0.0"
SCALING_CONSTANT = 12.5
# Chosen to map typical severe single-system burden (~8 units)
# to near-zero capacity. Deterministic shaping constant only.


def _round_half_away_from_zero(value: float) -> int:
    if value == 0:
        return 0
    dec = Decimal(str(abs(float(value)))).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(dec) if value > 0 else -int(dec)


def scale_capacity_scores_v1(
    *,
    adjusted_system_burden_vector: Mapping[str, float],
) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for system_id in sorted(str(k) for k in adjusted_system_burden_vector.keys()):
        adjusted = float(adjusted_system_burden_vector[system_id])
        capacity_raw = 100.0 - (adjusted * SCALING_CONSTANT)
        if capacity_raw < 0.0:
            capacity_raw = 0.0
        elif capacity_raw > 100.0:
            capacity_raw = 100.0
        out[system_id] = _round_half_away_from_zero(capacity_raw)
    return out
