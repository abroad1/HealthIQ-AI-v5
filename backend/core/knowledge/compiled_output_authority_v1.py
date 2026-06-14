"""
ARCH-COMPLETION-2 — Load and validate compiled output authority governance artefacts.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AUTHORITY_MODEL_PATH = (
    _REPO_ROOT / "knowledge_bus" / "governance" / "compiled_output_authority_model_v1.yaml"
)
_ROOT_CAUSE_REGISTER_PATH = (
    _REPO_ROOT / "knowledge_bus" / "governance" / "root_cause_authority_register_v1.yaml"
)
_CARD_REGISTER_PATH = _REPO_ROOT / "knowledge_bus" / "governance" / "card_authority_register_v1.yaml"

WHY_ENGINE_FALLBACK_HYPOTHESIS_ID = "why_engine_fallback_v1"
WHY_ENGINE_FALLBACK_AUTHORITY_STATUS = "ROOT_CAUSE_UNTRACEABLE_BLOCKED"

GOVERNED_ROOT_CAUSE_COMPILED = "ROOT_CAUSE_GOVERNED_ACTIVE"
GOVERNED_ROOT_CAUSE_LEGACY = "ROOT_CAUSE_GOVERNED_ACTIVE"
GOVERNED_SIGNAL_CARD = "CARD_GOVERNED_ACTIVE"
GOVERNED_DOMAIN_CARD = "CARD_GOVERNED_ACTIVE"
GOVERNED_IDL_CARD = "CARD_GOVERNED_ACTIVE"


class CompiledOutputAuthorityError(RuntimeError):
    """Raised when governance authority artefacts cannot be loaded."""


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise CompiledOutputAuthorityError(f"Missing governance artefact: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise CompiledOutputAuthorityError(f"Invalid governance artefact root: {path}")
    return payload


@lru_cache(maxsize=1)
def load_compiled_output_authority_model() -> Dict[str, Any]:
    return _load_yaml(_AUTHORITY_MODEL_PATH)


@lru_cache(maxsize=1)
def load_root_cause_authority_register() -> Dict[str, Any]:
    return _load_yaml(_ROOT_CAUSE_REGISTER_PATH)


@lru_cache(maxsize=1)
def load_card_authority_register() -> Dict[str, Any]:
    return _load_yaml(_CARD_REGISTER_PATH)


def authority_model_ref() -> str:
    return str(load_compiled_output_authority_model().get("artefact_path") or _AUTHORITY_MODEL_PATH.as_posix())


def root_cause_register_ref() -> str:
    return str(
        load_root_cause_authority_register().get("artefact_path") or _ROOT_CAUSE_REGISTER_PATH.as_posix()
    )


def card_register_ref() -> str:
    return str(load_card_authority_register().get("artefact_path") or _CARD_REGISTER_PATH.as_posix())


def root_cause_entry_for_signal(signal_id: str) -> Optional[Dict[str, Any]]:
    sid = str(signal_id or "").strip()
    if not sid:
        return None
    reg = load_root_cause_authority_register()
    for row in reg.get("entries") or []:
        if isinstance(row, dict) and str(row.get("signal_id", "")).strip() == sid:
            return row
    for row in reg.get("pattern_entries") or []:
        if not isinstance(row, dict):
            continue
        prefix = str(row.get("signal_id_prefix", "")).strip()
        if prefix and sid.startswith(prefix):
            return row
    return None


def card_entry_for_type(card_type: str) -> Optional[Dict[str, Any]]:
    token = str(card_type or "").strip()
    reg = load_card_authority_register()
    for row in reg.get("entries") or []:
        if isinstance(row, dict) and str(row.get("card_type", "")).strip() == token:
            return row
    return None


def is_forbidden_runtime_input(token: str) -> bool:
    model = load_compiled_output_authority_model()
    forbidden = model.get("forbidden_compiler_inputs") or []
    return str(token).strip() in {str(x).strip() for x in forbidden if str(x).strip()}


def element_type_policy(element_type: str) -> Optional[Dict[str, Any]]:
    model = load_compiled_output_authority_model()
    for row in model.get("output_element_types") or []:
        if isinstance(row, dict) and str(row.get("element_type", "")).strip() == element_type:
            return row
    return None


def classify_root_cause_finding(
    *,
    signal_id: str,
    hypothesis_ids: Mapping[str, Any],
    uses_compiled_artefact: bool,
) -> str:
    if WHY_ENGINE_FALLBACK_HYPOTHESIS_ID in {str(x).strip() for x in hypothesis_ids}:
        return WHY_ENGINE_FALLBACK_AUTHORITY_STATUS
    entry = root_cause_entry_for_signal(signal_id)
    if entry is not None:
        return str(entry.get("activation_status") or GOVERNED_ROOT_CAUSE_LEGACY)
    if uses_compiled_artefact:
        return GOVERNED_ROOT_CAUSE_COMPILED
    return GOVERNED_ROOT_CAUSE_LEGACY
