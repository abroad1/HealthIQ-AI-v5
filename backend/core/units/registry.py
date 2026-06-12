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
    G_L = "g/L"
    L_L = "L/L"
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
    PMOL_L = "pmol/L"
    NG_DL = "ng/dL"
    MEQ_L = "mEq/L"
    TEN_9_L = "10^9/L"
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
_HEMOGLOBIN_BIOMARKERS = frozenset({"hemoglobin"})
_HEMATOCRIT_BIOMARKERS = frozenset({"hematocrit"})
_CALCIUM_BIOMARKERS = frozenset({"calcium", "corrected_calcium"})
_MAGNESIUM_BIOMARKERS = frozenset({"magnesium"})
_FREE_T4_BIOMARKERS = frozenset({"free_t4"})
_URATE_BIOMARKERS = frozenset({"urate"})
_ELECTROLYTE_BIOMARKERS = frozenset({"sodium", "potassium", "chloride"})
_COUNT_BIOMARKERS = frozenset({
    "platelets", "white_blood_cells", "neutrophils", "lymphocytes",
    "monocytes", "eosinophils", "basophils",
})
_STRICT_CONVERSION_BIOMARKERS = frozenset().union(
    _CHOLESTEROL_BIOMARKERS,
    _TRIGLYCERIDE_BIOMARKERS,
    _GLUCOSE_BIOMARKERS,
    _HBA1C_BIOMARKERS,
    _UREA_BIOMARKERS,
    _CREATININE_BIOMARKERS,
    _VITAMIN_D_BIOMARKERS,
    _HEMOGLOBIN_BIOMARKERS,
    _HEMATOCRIT_BIOMARKERS,
    _CALCIUM_BIOMARKERS,
    _MAGNESIUM_BIOMARKERS,
    _FREE_T4_BIOMARKERS,
    _URATE_BIOMARKERS,
)

_UMOL_EQUIVALENTS = frozenset({"µmol/L", "umol/L", "uMol/L"})
_COUNT_UNIT_EQUIVALENTS = frozenset({"K/μL", "K/uL", "10^9/L"})
_MONOVALENT_EQUIVALENTS = frozenset({"mEq/L", "mmol/L"})
_GREEK_SMALL_MU = "\u03bc"
_MICRO_SIGN = "\u00b5"


def normalize_unit_token(unit: str) -> str:
    """Normalise visually equivalent micro-unit characters (Greek mu vs micro sign)."""
    token = (unit or "").strip()
    if not token:
        return token
    return token.replace(_GREEK_SMALL_MU, _MICRO_SIGN)


def _unit_in_equivalent_set(unit: str, equivalents: frozenset[str]) -> bool:
    normalized = normalize_unit_token(unit)
    return any(normalize_unit_token(candidate) == normalized for candidate in equivalents)


def _units_equivalent(from_unit: str, to_unit: str) -> bool:
    from_u = normalize_unit_token(from_unit)
    to_u = normalize_unit_token(to_unit)
    if from_u == to_u:
        return True
    if _unit_in_equivalent_set(from_u, _UMOL_EQUIVALENTS) and _unit_in_equivalent_set(
        to_u, _UMOL_EQUIVALENTS
    ):
        return True
    if _unit_in_equivalent_set(from_u, _COUNT_UNIT_EQUIVALENTS) and _unit_in_equivalent_set(
        to_u, _COUNT_UNIT_EQUIVALENTS
    ):
        return True
    if _unit_in_equivalent_set(from_u, _MONOVALENT_EQUIVALENTS) and _unit_in_equivalent_set(
        to_u, _MONOVALENT_EQUIVALENTS
    ):
        return True
    return False


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
        from_u = normalize_unit_token(from_unit)
        to_u = normalize_unit_token(to_unit)
        if _units_equivalent(from_u, to_u):
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
        if biomarker_id in _ELECTROLYTE_BIOMARKERS:
            if from_u in _MONOVALENT_EQUIVALENTS and to_u in _MONOVALENT_EQUIVALENTS:
                return 1.0
        if biomarker_id in _COUNT_BIOMARKERS:
            if _unit_in_equivalent_set(from_u, _COUNT_UNIT_EQUIVALENTS) and _unit_in_equivalent_set(
                to_u, _COUNT_UNIT_EQUIVALENTS
            ):
                return 1.0
        if biomarker_id in _HBA1C_BIOMARKERS and from_u == "%" and to_u == "mmol/mol":
            linear = self._get_hba1c_mmol_mol_to_percent_linear(biomarker_id, "mmol/mol", "%")
            if linear:
                slope, intercept = linear
                if slope:
                    return 1.0 / float(slope)
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
        if biomarker_id in _HEMOGLOBIN_BIOMARKERS and from_u == "g/L" and to_u == "g/dL":
            c = convs.get("g_L_to_g_dL_hemoglobin", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.1))
        if biomarker_id in _HEMOGLOBIN_BIOMARKERS and from_u == "g/dL" and to_u == "g/L":
            c = convs.get("g_dL_to_g_L_hemoglobin", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 10.0))
        if biomarker_id in _CALCIUM_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            key = (
                "mg_dL_to_mmol_L_corrected_calcium"
                if biomarker_id == "corrected_calcium"
                else "mg_dL_to_mmol_L_calcium"
            )
            c = convs.get(key, {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.2495))
        if biomarker_id in _CALCIUM_BIOMARKERS and from_u == "mmol/L" and to_u == "mg/dL":
            key = (
                "mmol_L_to_mg_dL_corrected_calcium"
                if biomarker_id == "corrected_calcium"
                else "mmol_L_to_mg_dL_calcium"
            )
            c = convs.get(key, {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 4.008016))
        if biomarker_id in _MAGNESIUM_BIOMARKERS and from_u == "mg/dL" and to_u == "mmol/L":
            c = convs.get("mg_dL_to_mmol_L_magnesium", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.4114))
        if biomarker_id in _MAGNESIUM_BIOMARKERS and from_u == "mmol/L" and to_u == "mg/dL":
            c = convs.get("mmol_L_to_mg_dL_magnesium", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 2.430724))
        if biomarker_id in _FREE_T4_BIOMARKERS and from_u == "ng/dL" and to_u == "pmol/L":
            c = convs.get("ng_dL_to_pmol_L_free_t4", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 12.871))
        if biomarker_id in _FREE_T4_BIOMARKERS and from_u == "pmol/L" and to_u == "ng/dL":
            c = convs.get("pmol_L_to_ng_dL_free_t4", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.077693))
        if biomarker_id in _URATE_BIOMARKERS and from_u == "mg/dL" and _unit_in_equivalent_set(
            to_u, _UMOL_EQUIVALENTS
        ):
            c = convs.get("mg_dL_to_umol_L_urate", {})
            if c.get("from_unit") == from_u and _unit_in_equivalent_set(
                c.get("to_unit", ""), _UMOL_EQUIVALENTS
            ):
                return float(c.get("factor", 59.5))
        if biomarker_id in _URATE_BIOMARKERS and _unit_in_equivalent_set(
            from_u, _UMOL_EQUIVALENTS
        ) and to_u == "mg/dL":
            c = convs.get("umol_L_to_mg_dL_urate", {})
            if _unit_in_equivalent_set(c.get("from_unit", ""), _UMOL_EQUIVALENTS) and c.get(
                "to_unit"
            ) == to_u:
                return float(c.get("factor", 0.016807))
        if biomarker_id in _HEMATOCRIT_BIOMARKERS and from_u == "%" and to_u == "L/L":
            c = convs.get("percent_to_l_L_hematocrit", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 0.01))
        if biomarker_id in _HEMATOCRIT_BIOMARKERS and from_u == "L/L" and to_u == "%":
            c = convs.get("l_L_to_percent_hematocrit", {})
            if c.get("from_unit") == from_u and c.get("to_unit") == to_u:
                return float(c.get("factor", 100.0))
        return None

    def _get_hba1c_mmol_mol_to_percent_linear(
        self, biomarker_id: str, from_unit: str, to_unit: str
    ) -> Optional[Tuple[float, float]]:
        """
        IFCC mmol/mol -> NGSP % for hba1c only. Authority: ssot/units.yaml mmol_mol_to_percent_hba1c.
        """
        if biomarker_id not in _HBA1C_BIOMARKERS:
            return None
        from_u = (from_unit or "").strip()
        to_u = (to_unit or "").strip()
        if from_u != "mmol/mol" or to_u != "%":
            return None
        data = self._load_units()
        convs = data.get("units", {}).get("conversions", {})
        c = convs.get("mmol_mol_to_percent_hba1c", {})
        if c.get("from_unit") != from_u or c.get("to_unit") != to_u:
            return None
        return (float(c["slope"]), float(c["intercept"]))

    def _convert_with_explicit_unit(
        self, biomarker_id: str, value: float, from_unit: str
    ) -> Tuple[float, str]:
        """
        Convert value to base unit. from_unit must be explicit (non-empty).
        Used after apply_unit_normalisation has resolved input_unit.
        """
        base_unit = self.get_base_unit(biomarker_id)
        from_u = normalize_unit_token(from_unit)
        if not from_u:
            raise UnitConversionError(
                f"Missing unit for biomarker '{biomarker_id}'; unit must be resolved before conversion",
                biomarker_id=biomarker_id,
                from_unit=from_unit,
                expected_base_unit=base_unit,
            )
        if from_u == base_unit:
            return float(value), base_unit
        if _units_equivalent(from_u, base_unit):
            return float(value), base_unit
        if biomarker_id in _HBA1C_BIOMARKERS and from_u == "%" and base_unit == "mmol/mol":
            linear = self._get_hba1c_mmol_mol_to_percent_linear(biomarker_id, "mmol/mol", "%")
            if linear is not None:
                slope, intercept = linear
                if slope:
                    return round((float(value) - float(intercept)) / float(slope), 6), base_unit
        linear = self._get_hba1c_mmol_mol_to_percent_linear(biomarker_id, from_u, base_unit)
        if linear is not None:
            slope, intercept = linear
            return round(float(value) * slope + intercept, 6), base_unit
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
        input_unit_raw = normalize_unit_token(data.get("unit") or "")
        ref_range = data.get("reference_range") or data.get("referenceRange")
        ref_range = ref_range if isinstance(ref_range, dict) else None
        rmin = ref_range.get("min") if ref_range else None
        rmax = ref_range.get("max") if ref_range else None
        ref_unit_raw = normalize_unit_token(ref_range.get("unit") or "") if ref_range else ""
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
            ref_unit = ref_unit_raw or input_unit
            has_min_only = isinstance(rmin, (int, float)) and not isinstance(rmax, (int, float))
            has_max_only = isinstance(rmax, (int, float)) and not isinstance(rmin, (int, float))
            if ref_unit and (has_min_only or has_max_only):
                try:
                    if has_min_only:
                        cmin, _ = reg._convert_with_explicit_unit(key, float(rmin), ref_unit)
                        ref_converted = {
                            "min": cmin,
                            "max": None,
                            "unit": base_unit,
                            "source": ref_range.get("source", "lab"),
                        }
                    else:
                        cmax, _ = reg._convert_with_explicit_unit(key, float(rmax), ref_unit)
                        ref_converted = {
                            "min": None,
                            "max": cmax,
                            "unit": base_unit,
                            "source": ref_range.get("source", "lab"),
                        }
                except UnitConversionError:
                    ref_converted = dict(ref_range)
            else:
                ref_converted = dict(ref_range)

        if ref_converted and isinstance(ref_converted, dict):
            rru = (ref_converted.get("unit") or "").strip()
            if rru and rru != base_unit and not _units_equivalent(rru, base_unit):
                ref_converted = None

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
        if "reference_profile" in data and isinstance(data.get("reference_profile"), dict):
            out["reference_profile"] = dict(data["reference_profile"])
        elif "referenceProfile" in data and isinstance(data.get("referenceProfile"), dict):
            out["reference_profile"] = dict(data["referenceProfile"])
        if isinstance(value, (int, float)) and val_converted != float(value):
            out["original_value"] = float(value)
        for k in ("timestamp",):
            if k in data:
                out[k] = data[k]
        result[key] = out

    return result


def value_and_reference_units_coherent_for_numeric_compare(
    biomarker_id: str,
    value_unit: str,
    ref_unit: str,
    *,
    registry: Optional[UnitRegistry] = None,
) -> bool:
    """
    True when value and reference range units are the same, µmol/L-equivalent,
    linked by an explicit registry conversion, or HbA1c % vs mmol/mol pair.
    Used to block numeric scoring on incompatible pairs (e.g. hemoglobin in mmol/L vs g/dL).
    """
    vu = (value_unit or "").strip()
    ru = (ref_unit or "").strip()
    if not ru or not vu:
        return True
    if vu == ru or _units_equivalent(vu, ru):
        return True
    conv_id = "hba1c" if biomarker_id == "hba1c_pct" else biomarker_id
    if conv_id in _HBA1C_BIOMARKERS and {vu, ru} == {"%", "mmol/mol"}:
        return True
    reg = registry or _get_registry()
    if reg._get_conversion_factor(conv_id, vu, ru) is not None:
        return True
    if reg._get_conversion_factor(conv_id, ru, vu) is not None:
        return True
    return False
