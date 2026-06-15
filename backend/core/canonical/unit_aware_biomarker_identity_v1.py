"""
Unit-aware biomarker identity resolution for ambiguous lab labels.

Governed by knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MODEL_PATH = (
    _REPO_ROOT / "knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml"
)

CONFIDENCE_HIGH_UNIT_RANGE = "HIGH_CONFIDENCE_UNIT_RANGE_MATCH"
CONFIDENCE_MODERATE_UNIT = "MODERATE_CONFIDENCE_UNIT_MATCH"
CONFIDENCE_LOW_LABEL_ONLY = "LOW_CONFIDENCE_LABEL_ONLY"
CONFIDENCE_FAIL_CLOSED = "AMBIGUOUS_FAIL_CLOSED"

_DHEA_S_EXPLICIT = (
    "dhea-s",
    "dheas",
    "dhea_s",
    "dehydroepiandrosterone sulfate",
    "dehydroepiandrosterone sulphate",
)
_DHEA_AMBIGUOUS_NORMALIZED = {
    "dhea",
    "dhea_venous",
    "dehydroepiandrosterone",
}
_DHEA_S_UNITS = {"umol/l", "umol_l", "µmol/l", "μmol/l"}
_UNSULFATED_UNITS = {"ng/ml", "ng/dl", "nmol/l", "nmol_l"}


@dataclass(frozen=True)
class BiomarkerIdentityResolution:
    canonical_id: str
    confidence: str
    reason: str
    raw_label: str
    fail_closed: bool = False
    preserved_unit: str = ""
    preserved_reference_range: Optional[Dict[str, Any]] = None


def _load_model() -> Dict[str, Any]:
    if not _MODEL_PATH.is_file():
        return {}
    return yaml.safe_load(_MODEL_PATH.read_text(encoding="utf-8")) or {}


def governance_model_ref() -> str:
    return str(_MODEL_PATH.relative_to(_REPO_ROOT)).replace("\\", "/")


def _normalize_unit(unit: str) -> str:
    normalized = (unit or "").strip().lower()
    normalized = normalized.replace("µ", "u").replace("μ", "u")
    normalized = normalized.replace(" ", "")
    return normalized


def _normalize_label(raw_label: str) -> str:
    normalized = (raw_label or "").strip().lower()
    normalized = re.sub(r"[-/\s]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    for suffix in ("_venous", "_(venous)"):
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)]
    return normalized.strip("_")


def _is_explicit_dhea_s_label(raw_label: str) -> bool:
    lower = (raw_label or "").lower()
    return any(token in lower for token in _DHEA_S_EXPLICIT)


def _is_ambiguous_dhea_label(raw_label: str) -> bool:
    norm = _normalize_label(raw_label)
    if _is_explicit_dhea_s_label(raw_label):
        return False
    if norm in _DHEA_AMBIGUOUS_NORMALIZED:
        return True
    if norm.startswith("dhea") and "sulfate" not in norm and "sulphate" not in norm and "dheas" not in norm:
        return True
    return False


def _reference_range_dict(reference_range: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(reference_range, dict):
        return None
    return dict(reference_range)


def _matches_dhea_s_umol_reference(reference_range: Optional[Dict[str, Any]]) -> bool:
    if reference_range is None:
        return False
    min_val = reference_range.get("min")
    max_val = reference_range.get("max")
    if not isinstance(max_val, (int, float)):
        return False
    max_f = float(max_val)
    if not (3.0 <= max_f <= 30.0):
        return False
    if min_val is None:
        return True
    if isinstance(min_val, (int, float)):
        return 0.0 <= float(min_val) <= 5.0
    return False


def resolve_unit_aware_biomarker_identity(
    *,
    raw_label: str,
    unit: Optional[str] = None,
    reference_range: Any = None,
    label_canonical_hint: Optional[str] = None,
) -> Optional[BiomarkerIdentityResolution]:
    """
    Resolve ambiguous biomarker identity using unit and reference-range evidence.

    Returns None when the label is outside governed ambiguous families.
    """
    if not raw_label:
        return None

    ref = _reference_range_dict(reference_range)
    unit_norm = _normalize_unit(unit or (ref or {}).get("unit", ""))
    preserved_unit = unit or (ref or {}).get("unit", "") or ""

    if _is_explicit_dhea_s_label(raw_label):
        return BiomarkerIdentityResolution(
            canonical_id="dhea_s",
            confidence=CONFIDENCE_HIGH_UNIT_RANGE if _matches_dhea_s_umol_reference(ref) else CONFIDENCE_MODERATE_UNIT,
            reason="explicit_dhea_s_label",
            raw_label=raw_label,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    if not _is_ambiguous_dhea_label(raw_label):
        return None

    if label_canonical_hint == "dhea_s":
        return BiomarkerIdentityResolution(
            canonical_id="dhea_s",
            confidence=CONFIDENCE_MODERATE_UNIT,
            reason="alias_registry_explicit_dhea_s",
            raw_label=raw_label,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    has_unit = bool(unit_norm)
    has_range = _matches_dhea_s_umol_reference(ref)

    if not has_unit and not has_range:
        return BiomarkerIdentityResolution(
            canonical_id=f"unmapped_{raw_label}",
            confidence=CONFIDENCE_FAIL_CLOSED,
            reason="ambiguous_dhea_label_without_unit_or_range",
            raw_label=raw_label,
            fail_closed=True,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    if unit_norm in _DHEA_S_UNITS and _matches_dhea_s_umol_reference(ref):
        return BiomarkerIdentityResolution(
            canonical_id="dhea_s",
            confidence=CONFIDENCE_HIGH_UNIT_RANGE,
            reason="dhea_s_unit_and_reference_range_convention_match",
            raw_label=raw_label,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    if unit_norm in _DHEA_S_UNITS and has_unit and not has_range:
        return BiomarkerIdentityResolution(
            canonical_id=f"unmapped_{raw_label}",
            confidence=CONFIDENCE_FAIL_CLOSED,
            reason="dhea_s_unit_without_confirming_reference_range",
            raw_label=raw_label,
            fail_closed=True,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    if unit_norm in _UNSULFATED_UNITS:
        return BiomarkerIdentityResolution(
            canonical_id="dhea",
            confidence=CONFIDENCE_MODERATE_UNIT,
            reason="unsulfated_dhea_unit_convention",
            raw_label=raw_label,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    if unit_norm in _DHEA_S_UNITS and has_range and not _matches_dhea_s_umol_reference(ref):
        return BiomarkerIdentityResolution(
            canonical_id=f"unmapped_{raw_label}",
            confidence=CONFIDENCE_FAIL_CLOSED,
            reason="dhea_s_unit_with_conflicting_reference_range",
            raw_label=raw_label,
            fail_closed=True,
            preserved_unit=preserved_unit,
            preserved_reference_range=ref,
        )

    return BiomarkerIdentityResolution(
        canonical_id=f"unmapped_{raw_label}",
        confidence=CONFIDENCE_FAIL_CLOSED,
        reason="ambiguous_dhea_identity_unresolved",
        raw_label=raw_label,
        fail_closed=True,
        preserved_unit=preserved_unit,
        preserved_reference_range=ref,
    )


def resolve_canonical_with_identity(
    *,
    raw_label: str,
    label_canonical_hint: str,
    unit: Optional[str] = None,
    reference_range: Any = None,
) -> BiomarkerIdentityResolution:
    """Apply unit-aware resolution when governed; otherwise pass through label hint."""
    identity = resolve_unit_aware_biomarker_identity(
        raw_label=raw_label,
        unit=unit,
        reference_range=reference_range,
        label_canonical_hint=label_canonical_hint,
    )
    if identity is not None:
        return identity
    return BiomarkerIdentityResolution(
        canonical_id=label_canonical_hint,
        confidence=CONFIDENCE_LOW_LABEL_ONLY,
        reason="label_only_alias_resolution",
        raw_label=raw_label,
        preserved_unit=unit or "",
        preserved_reference_range=_reference_range_dict(reference_range),
    )


def load_governance_model() -> Mapping[str, Any]:
    return _load_model()
