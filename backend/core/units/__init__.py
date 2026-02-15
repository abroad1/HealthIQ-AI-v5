"""
Unit registry and conversion layer for deterministic base-unit normalisation.

Sprint 1 (Unit Registry) - P0 deterministic unit safety.
Source: Delivery_Sprint_Plan_v5.2, Master_PRD_v5.2 §3.2.
"""

from core.units.registry import (
    UnitConversionError,
    UnitRegistry,
    convert_value,
    apply_unit_normalisation,
)

__all__ = [
    "UnitConversionError",
    "UnitRegistry",
    "convert_value",
    "apply_unit_normalisation",
]
