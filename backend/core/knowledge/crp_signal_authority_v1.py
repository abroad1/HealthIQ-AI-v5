"""
CRP-PASS3-MIGRATION — governed CRP / systemic inflammation runtime authority registry.

Read-only classification consumed by ARCH-RT-6 validator and regression tests.
Does not alter signal evaluation behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, FrozenSet, Mapping, Tuple

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AUTHORITY_PATH = _REPO_ROOT / "knowledge_bus" / "governance" / "crp_runtime_authority_v1.yaml"

CRP_SIGNAL_IDS: FrozenSet[str] = frozenset(
    {
        "signal_crp_high",
        "signal_systemic_inflammation",
        "signal_inflammation_crp_context",
    }
)
CRP_RUNTIME_PACKAGE_SIGNAL_CRP_HIGH = "pkg_s24_crp_high_inflammation"
ROOT_CAUSE_INFLAMMATION_SIGNAL_ID = "signal_systemic_inflammation"
WAVE1_VASCULAR_STRAIN_SUBSYSTEM_ID = "wave1_cv_vascular_strain"
PASS3_CRP_FRAME_IDS: Tuple[str, ...] = (
    "inv_crp_high_active_inflammatory_or_infective_state",
    "inv_crp_high_residual_cardiometabolic_inflammatory_risk",
)


@dataclass(frozen=True)
class CrpSignalAuthorityRow:
    signal_id: str
    clinical_role: str
    primary_metric: str
    activation_logic: str
    runtime_package_id: str | None
    runtime_package_ids: Tuple[str, ...]
    root_cause_target: bool
    pass3_runtime_status: str


def authority_path() -> Path:
    return _AUTHORITY_PATH


@lru_cache(maxsize=1)
def load_crp_runtime_authority() -> Dict[str, Any]:
    if not _AUTHORITY_PATH.is_file():
        raise FileNotFoundError(f"CRP authority registry missing: {_AUTHORITY_PATH}")
    payload = yaml.safe_load(_AUTHORITY_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("crp_runtime_authority_v1 must be a mapping")
    return payload


def signal_authority_rows() -> Tuple[CrpSignalAuthorityRow, ...]:
    doc = load_crp_runtime_authority()
    signals = doc.get("signals")
    if not isinstance(signals, dict):
        raise ValueError("crp_runtime_authority_v1.signals must be a mapping")
    rows: list[CrpSignalAuthorityRow] = []
    for signal_id, spec in signals.items():
        if not isinstance(spec, dict):
            continue
        pkg_single = spec.get("runtime_package_id")
        pkg_many = spec.get("runtime_package_ids") or []
        if not isinstance(pkg_many, list):
            pkg_many = []
        rows.append(
            CrpSignalAuthorityRow(
                signal_id=str(signal_id),
                clinical_role=str(spec.get("clinical_role") or ""),
                primary_metric=str(spec.get("primary_metric") or ""),
                activation_logic=str(spec.get("activation_logic") or ""),
                runtime_package_id=str(pkg_single).strip() if isinstance(pkg_single, str) and pkg_single.strip() else None,
                runtime_package_ids=tuple(str(p).strip() for p in pkg_many if str(p).strip()),
                root_cause_target=bool(spec.get("root_cause_target")),
                pass3_runtime_status=str(spec.get("pass3_runtime_status") or ""),
            )
        )
    return tuple(rows)


def authority_by_signal_id() -> Mapping[str, CrpSignalAuthorityRow]:
    return {row.signal_id: row for row in signal_authority_rows()}
