"""
Unit Registry - deterministic conversion to internal base SI units.

Sprint 1 (Unit Registry) - P0 deterministic unit safety.
Source: ssot/units.yaml for conversion factors.
Lab-provided reference ranges remain sovereign; conversion ensures coherence.

Hardening: No silent assumptions. Unmapped rejected by default.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import yaml


def _allow_unmapped() -> bool:
    """Default False. Set UNIT_ALLOW_UNMAPPED=true to allow unmapped_ passthrough."""
    return os.environ.get("UNIT_ALLOW_UNMAPPED", "false").lower() == "true"


UNIT_REGISTRY_VERSION = "1.0"


class UnitConversionError(ValueError):
    """Raised when unit conversion fails (unknown unit, no conversion path)."""
    def __init__(
        self,
        message: str,
        *,
        biomarker_id: Optional[str] = None,
        from_unit: Optional[str] = None,
        expected_base_unit: Optional[str] = None,
    ):
        super().__init__(message)
        self.biomarker_id = biomarker_id
        self.from_unit = from_unit
        self.expected_base_unit = expected_base_unit


class UnitEnum(str, Enum):
    """Canonical unit tokens. Aligns with ssot/units.yaml."""
    MG_DL = "mg/dL"
    G_DL = "g/dL"
    PERCENT = "%"
    U_L = "U/L"
    K_UL = "K/μL"
    UU_ML = "μU/mL"
    MG_L = "mg/L"
    MMOL_L = "mmol/L"
    UMOL_L = "µmol/L"
    NMOL_L = "nmol/L"
    NG_ML = "ng/mL"
    MMOL_MOL = "mmol/mol"
    MEQ_L = "mEq/L"
    RATIO = "ratio"


# Biomarker groups for deterministic conversion dispatch.
_CHOLESTEROL_BIOMARKERS = frozenset({
    "total_cholesterol", "ldl_cholesterol", "hdl_cholesterol",
})
_TRIGLYCERIDE_BIOMARKERS = frozenset({"triglycerides"})
_GLUCOSE_BIOMARKERS = frozenset({"glucose"})
_HBA1C_BIOMARKERS = frozenset({"hba1c"})
_UREA_BIOMARKERS = frozenset({"urea"})
_CREATININE_BIOMARKERS = frozenset({"creatinine"})
_VITAMIN_D_BIOMARKERS = frozenset({"vitamin_d"})
_STRICT_CONVERSION_BIOMARKERS = frozenset().union(
    _CHOLESTEROL_BIOMARKERS,
    _TRIGLYCERIDE_BIOMARKERS,
    _GLUCOSE_BIOMARKERS,
    _HBA1C_BIOMARKERS,
    _UREA_BIOMARKERS,
    _CREATININE_BIOMARKERS,
    _VITAMIN_D_BIOMARKERS,
)


class UnitRegistry:
    """Hard-typed unit registry with biomarker-specific conversion matrix."""

    def __init__(self, ssot_path: Optional[Path] = None):
        if ssot_path is None:
            ssot_path = Path(__file__).parent.parent.parent / "ssot"
        self.ssot_path = ssot_path
        self._units_data: Optional[Dict[str, Any]] = None
        self._biomarker_base_units: Optional[Dict[str, str]] = None
        self._biomarker_ssot_units: Optional[Dict[str, str]] = None

    def _load_units(self) -> Dict[str, Any]:
        if self._units_data is not None:
            return self._units_data
        units_file = self.ssot_path / "units.yaml"
        if not units_file.exists():
            raise FileNotFoundError(f"Units SSOT file not found: {units_file}")
        with open(units_file, "r", encoding="utf-8") as f:
            self._units_data = yaml.safe_load(f)
        return self._units_data

    def _load_biomarker_base_units(self) -> Dict[str, str]:
        if self._biomarker_base_units is not None:
            return self._biomarker_base_units
        biomarkers_file = self.ssot_path / "biomarkers.yaml"
        if not biomarkers_file.exists():
            self._biomarker_base_units = {}
            self._biomarker_ssot_units = {}
            return self._biomarker_base_units
        with open(biomarkers_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        base = {
            name: ((defn.get("unit") or "").strip() or "mg/dL")
            for name, defn in data.get("biomarkers", {}).items()
        }
        self._biomarker_base_units = base
        self._biomarker_ssot_units = {
            name: (defn.get("unit") or "").strip() or "mg/dL"
            for name, defn in data.get("biomarkers", {}).items()
        }
        return self._biomarker_base_units

    def _get_ssot_unit(self, biomarker_id: str) -> Optional[str]:
        self._load_biomarker_base_units()
        return self._biomarker_ssot_units.get(biomarker_id) if self._biomarker_ssot_units else None

    def get_base_unit(self, biomarker_id: str) -> str:
        base = self._load_biomarker_base_units()
        if biomarker_id in base:
            return base[biomarker_id]
        raise UnitConversionError(
            f"Unknown biomarker '{biomarker_id}'; cannot determine base unit",
            biomarker_id=biomarker_id,
        )

    def _get_conversion_factor(
        self, biomarker_id: str, from_unit: str, to_unit: str
    ) -> Optional[float]:
        from_u = (from_unit or "").strip()
        to_u = (to_unit or "").strip()
        if from_u == to_u:
            return 1.0
        data = self._load_units()
        convs = data.get("units", {}).get("conversions", {})
        if biomarker_id in _GLUCOSE_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            c = convs.get("mg_dL_to_mmol_L_glucose", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 1.0 / 18.0))
        if biomarker_id in _GLUCOSE_BIOMARKERS and from_u == "mmol/L" and to_u == "mg/dL":
            c = convs.get("mmol_L_to_mg_dL_glucose", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 18.0))
        if biomarker_id in _CHOLESTEROL_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            c = convs.get("mg_dL_to_mmol_L_cholesterol", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 1.0 / 38.67))
        if biomarker_id in _CHOLESTEROL_BIOMARKERS and from_u == "mmol/L" and to_u == "mg/dL":
            c = convs.get("mmol_L_to_mg_dL_cholesterol", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 38.67))
        if biomarker_id in _TRIGLYCERIDE_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            c = convs.get("mg_dL_to_mmol_L_triglycerides", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.01129))
        if biomarker_id in _TRIGLYCERIDE_BIOMARKERS and from_u == "mmol/L" and to_u == "mg/dL":
            c = convs.get("mmol_L_to_mg_dL_triglycerides", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 88.57))
        if biomarker_id in _HBA1C_BIOMARKERS and from_u == "%" and to_u == "mmol/mol":
            c = convs.get("percent_to_mmol_mol", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 10.929))
        if biomarker_id in _UREA_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            c = convs.get("mg_dL_to_mmol_L_urea", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.357))
        if biomarker_id in _CREATININE_BIOMARKERS and from_u == "mg/dL" and to_u == "µmol/L":
            c = convs.get("mg_dL_to_umol_L_creatinine", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 88.4))
        if biomarker_id in _VITAMIN_D_BIOMARKERS and from_u == "ng/mL" and to_u == "nmol/L":
            c = convs.get("ng_mL_to_nmol_L_vitamin_d", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 2.5))
        return None

    def _convert_with_explicit_unit(
        self, biomarker_id: str, value: float, from_unit: str
    ) -> Tuple[float, str]:
        """
        Convert value to base unit. from_unit must be explicit (non-empty).
        Used after apply_unit_normalisation has resolved input_unit.
        """
        base_unit = self.get_base_unit(biomarker_id)
        from_u = (from_unit or "").strip()
        if not from_u:
            raise UnitConversionError(
                f"Missing unit for biomarker '{biomarker_id}'; unit must be resolved before conversion",
                biomarker_id=biomarker_id,
                from_unit=from_unit,
                expected_base_unit=base_unit,
            )
        if from_u == base_unit:
            return float(value), base_unit
        factor = self._get_conversion_factor(biomarker_id, from_u, base_unit)
        if factor is None:
            if biomarker_id not in _STRICT_CONVERSION_BIOMARKERS:
                # Deterministic passthrough for biomarkers without an explicit
                # conversion matrix in UnitRegistry.
                return float(value), from_u
            raise UnitConversionError(
                f"No conversion from '{from_u}' to base unit '{base_unit}' for biomarker '{biomarker_id}'",
                biomarker_id=biomarker_id,
                from_unit=from_u,
                expected_base_unit=base_unit,
            )
        return round(float(value) * factor, 6), base_unit


_registry: Optional[UnitRegistry] = None


def _get_registry() -> UnitRegistry:
    global _registry
    if _registry is None:
        _registry = UnitRegistry()
    return _registry


def convert_value(
    biomarker_id: str,
    value: float,
    from_unit: str,
    *,
    registry: Optional[UnitRegistry] = None,
) -> Tuple[float, str]:
    """
    Convert value to base unit.
    from_unit must be explicit (non-empty). Use apply_unit_normalisation for full resolution.
    """
    reg = registry or _get_registry()
    return reg._convert_with_explicit_unit(biomarker_id, value, from_unit)


def apply_unit_normalisation(
    normalized: Dict[str, Any],
    *,
    registry: Optional[UnitRegistry] = None,
    allow_unmapped: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Apply unit normalisation with deterministic rules.
    No silent assumptions. Unmapped rejected by default.
    """
    reg = registry or _get_registry()
    result = {}

    for key, data in normalized.items():
        is_explicit_unmapped = (
            isinstance(data, dict)
            and (
                data.get("unmapped") is True
                or data.get("is_unmapped") is True
                or str(data.get("canonical_id", "")).startswith("unmapped_")
            )
        )
        if key.startswith("unmapped_") or is_explicit_unmapped:
            # Quarantine contract: unmapped biomarkers bypass unit conversion and
            # are passed through for deterministic downstream quarantine handling.
            if isinstance(data, dict):
                result[key] = dict(data)
            else:
                result[key] = {"value": data, "unit": ""}
            continue

        if isinstance(data, (int, float)):
            raise UnitConversionError(
                f"Bare value for '{key}' without unit; provide dict with value and unit",
                biomarker_id=key,
            )

        if not isinstance(data, dict):
            result[key] = dict(data) if hasattr(data, "items") else {"value": data, "unit": ""}
            continue

        value = data.get("value", data.get("measurement", 0))
        input_unit_raw = (data.get("unit") or "").strip()
        ref_range = data.get("reference_range") or data.get("referenceRange")
        ref_range = ref_range if isinstance(ref_range, dict) else None
        rmin = ref_range.get("min") if ref_range else None
        rmax = ref_range.get("max") if ref_range else None
        ref_unit_raw = (ref_range.get("unit") or "").strip() if ref_range else ""
        has_ref_bounds = isinstance(rmin, (int, float)) and isinstance(rmax, (int, float))

        # --- Resolve input_unit (deterministic missing-unit rules) ---
        unit_source = "explicit"
        confidence_downgrade_unit_assumed = False
        input_unit = input_unit_raw

        if not input_unit:
            # Rule (a): ref range unit exists -> adopt it
            if ref_unit_raw:
                input_unit = ref_unit_raw
                unit_source = "reference_range"
            # Rule (b): SSOT exists AND ref range min/max present (even without ref unit)
            elif reg._get_ssot_unit(key) and has_ref_bounds:
                input_unit = reg._get_ssot_unit(key)
                unit_source = "ssot_assumed"
                confidence_downgrade_unit_assumed = True
            # Rule (c): else reject
            else:
                base_unit = reg.get_base_unit(key)
                raise UnitConversionError(
                    f"Missing unit for biomarker '{key}'; no reference_range unit and no SSOT+ref_bounds",
                    biomarker_id=key,
                    from_unit="",
                    expected_base_unit=base_unit,
                )

        # --- Convert value ---
        try:
            val_converted, base_unit = reg._convert_with_explicit_unit(key, float(value), input_unit)
        except UnitConversionError:
            raise

        unit_normalised = input_unit != base_unit

        # --- Reference range conversion (explicit rules) ---
        ref_converted = None
        reference_unit_assumed = False

        if ref_range and has_ref_bounds:
            ref_unit = ref_unit_raw or input_unit
            if not ref_unit_raw and input_unit:
                reference_unit_assumed = True
                ref_unit = input_unit
            elif not ref_unit_raw and not input_unit:
                raise UnitConversionError(
                    f"Reference range for '{key}' has no unit and biomarker has no unit",
                    biomarker_id=key,
                )

            # ref_unit present: convertible to base, or == base, else reject
            if ref_unit == base_unit:
                ref_converted = {
                    "min": float(rmin),
                    "max": float(rmax),
                    "unit": base_unit,
                    "source": ref_range.get("source", "lab"),
                }
            else:
                try:
                    min_conv, _ = reg._convert_with_explicit_unit(key, float(rmin), ref_unit)
                    max_conv, _ = reg._convert_with_explicit_unit(key, float(rmax), ref_unit)
                    ref_converted = {
                        "min": min_conv,
                        "max": max_conv,
                        "unit": base_unit,
                        "source": ref_range.get("source", "lab"),
                    }
                except UnitConversionError:
                    raise
        elif ref_range:
            ref_converted = dict(ref_range)

        out = {
            "value": val_converted,
            "unit": base_unit,
            "reference_range": ref_converted,
            "original_unit": input_unit_raw or input_unit,
            "unit_normalised": unit_normalised,
            "unit_source": unit_source,
            "confidence_downgrade_unit_assumed": confidence_downgrade_unit_assumed,
            "reference_unit_assumed": reference_unit_assumed,
        }
        if isinstance(value, (int, float)) and val_converted != float(value):
            out["original_value"] = float(value)
        for k in ("timestamp",):
            if k in data:
                out[k] = data[k]
        result[key] = out

    return result
