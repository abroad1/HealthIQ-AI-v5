"""
LC-S18 — Root-cause / WHY target registry (hybrid manual table + validation).

Preserves legacy registration order and loaders. Does not auto-discover from orphan KB packages.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Sequence, Tuple

from core.knowledge import load_root_cause_hypotheses as lrc

HypothesesLoader = Callable[[], Dict[str, Any]]


@dataclass(frozen=True)
class RootCauseTargetSpec:
    signal_id: str
    loader: HypothesesLoader
    asset_filename: str
    registration_source: str = "manual_v1"


# Order preserved from legacy _ROOT_CAUSE_TARGETS (root_cause_compiler_v1.py).
ROOT_CAUSE_TARGET_SPECS: Tuple[RootCauseTargetSpec, ...] = (
    RootCauseTargetSpec("signal_homocysteine_elevation_context", lrc.load_hcy_hypotheses_v1, "hcy_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_homocysteine_high", lrc.load_hcy_hypotheses_v1, "hcy_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hba1c_high", lrc.load_hba1c_hypotheses_v1, "hba1c_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hepatic_alt_context", lrc.load_alt_hypotheses_v1, "alt_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_thyroid_tsh_context", lrc.load_tsh_hypotheses_v1, "tsh_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_insulin_resistance", lrc.load_insulin_resistance_hypotheses_v1, "insulin_resistance_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_systemic_inflammation", lrc.load_systemic_inflammation_hypotheses_v1, "systemic_inflammation_hypotheses_v1.yaml"),
    RootCauseTargetSpec(
        "signal_lipid_transport_dysfunction",
        lrc.load_lipid_transport_dysfunction_hypotheses_v1,
        "lipid_transport_dysfunction_hypotheses_v1.yaml",
    ),
    RootCauseTargetSpec("signal_mcv_high", lrc.load_mcv_high_hypotheses_v1, "mcv_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_ldl_cholesterol_high", lrc.load_ldl_cholesterol_high_hypotheses_v1, "ldl_cholesterol_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_apoa1_cardio_risk", lrc.load_apoa1_cardio_risk_hypotheses_v1, "apoa1_cardio_risk_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hdl_cholesterol_low", lrc.load_hdl_cholesterol_low_hypotheses_v1, "hdl_cholesterol_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_triglycerides_high", lrc.load_triglycerides_high_hypotheses_v1, "triglycerides_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_total_cholesterol_high", lrc.load_total_cholesterol_high_hypotheses_v1, "total_cholesterol_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec(
        "signal_iron_deficiency_context",
        lrc.load_iron_deficiency_context_hypotheses_v1,
        "iron_deficiency_context_hypotheses_v1.yaml",
    ),
    RootCauseTargetSpec(
        "signal_iron_overload_context",
        lrc.load_iron_overload_context_hypotheses_v1,
        "iron_overload_context_hypotheses_v1.yaml",
    ),
    RootCauseTargetSpec(
        "signal_oxygen_transport_capacity",
        lrc.load_oxygen_transport_capacity_hypotheses_v1,
        "oxygen_transport_capacity_hypotheses_v1.yaml",
    ),
    RootCauseTargetSpec("signal_ferritin_low", lrc.load_ferritin_low_hypotheses_v1, "ferritin_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_ferritin_high", lrc.load_ferritin_high_hypotheses_v1, "ferritin_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hemoglobin_low", lrc.load_hemoglobin_low_hypotheses_v1, "hemoglobin_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_transferrin_high", lrc.load_transferrin_high_hypotheses_v1, "transferrin_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_transferrin_low", lrc.load_transferrin_low_hypotheses_v1, "transferrin_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_ggt_high", lrc.load_ggt_high_hypotheses_v1, "ggt_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_tsh_high", lrc.load_tsh_high_hypotheses_v1, "tsh_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_tsh_low", lrc.load_tsh_low_hypotheses_v1, "tsh_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec(
        "signal_hepatic_metabolic_stress",
        lrc.load_hepatic_metabolic_stress_hypotheses_v1,
        "hepatic_metabolic_stress_hypotheses_v1.yaml",
    ),
    RootCauseTargetSpec("signal_alp_high", lrc.load_alp_high_hypotheses_v1, "alp_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_alp_low", lrc.load_alp_low_hypotheses_v1, "alp_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_bilirubin_high", lrc.load_bilirubin_high_hypotheses_v1, "bilirubin_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hyperbilirubinemia", lrc.load_hyperbilirubinemia_hypotheses_v1, "hyperbilirubinemia_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_hypercortisolism", lrc.load_hypercortisolism_hypotheses_v1, "hypercortisolism_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_free_t3_high", lrc.load_free_t3_high_hypotheses_v1, "free_t3_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_free_t3_low", lrc.load_free_t3_low_hypotheses_v1, "free_t3_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_free_t4_high", lrc.load_free_t4_high_hypotheses_v1, "free_t4_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_free_t4_low", lrc.load_free_t4_low_hypotheses_v1, "free_t4_low_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_tgab_high", lrc.load_tgab_high_hypotheses_v1, "tgab_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_tpo_ab_high", lrc.load_tpo_ab_high_hypotheses_v1, "tpo_ab_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_creatinine_high", lrc.load_creatinine_high_hypotheses_v1, "creatinine_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_urea_high", lrc.load_urea_high_hypotheses_v1, "urea_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_urate_high", lrc.load_urate_high_hypotheses_v1, "urate_high_hypotheses_v1.yaml"),
    RootCauseTargetSpec("signal_vitamin_d_low", lrc.load_vitamin_d_low_hypotheses_v1, "vitamin_d_low_hypotheses_v1.yaml"),
)


class RootCauseRegistryValidationError(ValueError):
    """Raised when root-cause registry metadata is invalid."""


def validate_root_cause_registry(
    specs: Sequence[RootCauseTargetSpec] = ROOT_CAUSE_TARGET_SPECS,
    *,
    load_assets: bool = True,
) -> None:
    seen: set[str] = set()
    for spec in specs:
        sid = spec.signal_id.strip()
        if not sid:
            raise RootCauseRegistryValidationError("root-cause target signal_id must be non-empty")
        if sid in seen:
            raise RootCauseRegistryValidationError(f"duplicate root-cause target signal_id: {sid}")
        seen.add(sid)
        if not callable(spec.loader):
            raise RootCauseRegistryValidationError(f"loader not callable for {sid}")
        if not spec.asset_filename.strip():
            raise RootCauseRegistryValidationError(f"missing asset_filename for {sid}")
        if load_assets:
            payload = spec.loader()
            path = str(payload.get("path", ""))
            if spec.asset_filename not in path.replace("\\", "/"):
                raise RootCauseRegistryValidationError(
                    f"asset_filename mismatch for {sid}: expected {spec.asset_filename} in {path}"
                )
            hypotheses = payload.get("hypotheses")
            if not isinstance(hypotheses, list) or not hypotheses:
                raise RootCauseRegistryValidationError(f"no hypotheses loaded for {sid}")


def get_root_cause_targets(
    specs: Sequence[RootCauseTargetSpec] = ROOT_CAUSE_TARGET_SPECS,
    *,
    validate: bool = True,
) -> List[Tuple[str, HypothesesLoader]]:
    if validate:
        validate_root_cause_registry(specs, load_assets=True)
    return [(spec.signal_id, spec.loader) for spec in specs]


def _hypothesis_asset_fingerprint(payload: Dict[str, Any]) -> str:
    hypotheses = payload.get("hypotheses") or []
    rows = []
    for row in hypotheses:
        if not isinstance(row, dict):
            continue
        rows.append(
            {
                "hypothesis_id": str(row.get("hypothesis_id", "")).strip(),
                "title": str(row.get("title", "")).strip(),
                "summary_template": str(row.get("summary_template", "")).strip(),
                "confirmatory_tests": sorted(str(x) for x in (row.get("confirmatory_tests") or [])),
            }
        )
    rows.sort(key=lambda r: r["hypothesis_id"])
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fingerprint_root_cause_targets(
    specs: Sequence[RootCauseTargetSpec] = ROOT_CAUSE_TARGET_SPECS,
) -> Dict[str, Any]:
    validate_root_cause_registry(specs, load_assets=True)
    entries: List[Dict[str, Any]] = []
    for spec in specs:
        entry: Dict[str, Any] = {
            "signal_id": spec.signal_id,
            "asset_filename": spec.asset_filename,
            "registration_source": spec.registration_source,
            "asset_loads": False,
            "governed": False,
            "hypothesis_asset_fingerprint": None,
            "error": None,
        }
        try:
            payload = spec.loader()
            entry["asset_path"] = payload.get("path")
            entry["asset_loads"] = True
            entry["governed"] = True
            entry["hypothesis_count"] = len(payload.get("hypotheses") or [])
            entry["hypothesis_asset_fingerprint"] = _hypothesis_asset_fingerprint(payload)
        except Exception as exc:  # noqa: BLE001 — fingerprint must record failures
            entry["error"] = f"{type(exc).__name__}: {exc}"
        entries.append(entry)
    return {
        "registry_version": "lc-s18-v1",
        "target_count": len(entries),
        "targets": entries,
    }
