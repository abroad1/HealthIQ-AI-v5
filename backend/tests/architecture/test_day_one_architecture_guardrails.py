"""ARCH-RT-6 — architecture guardrail tests (validator + acceptance invariants)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import importlib.util

_REPO = Path(__file__).resolve().parents[3]
_VALIDATOR = _REPO / "backend" / "scripts" / "validate_day_one_architecture.py"
_SENTINEL_PACK = _REPO / "sentinel" / "packs" / "day_one_architecture_guardrails_v1.json"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_day_one_architecture", _VALIDATOR)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_validator_passes_on_current_repo():
    mod = _load_validator()
    errors = mod.run_day_one_architecture_validation(repo_root=_REPO)
    assert errors == [], "\n".join(errors)


def test_validator_cli_exit_zero():
    proc = subprocess.run(
        [sys.executable, str(_VALIDATOR)],
        cwd=_REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_sentinel_pack_exists_and_references_validator():
    assert _SENTINEL_PACK.is_file(), "Sentinel pack must exist at sentinel/packs/"
    import json

    payload = json.loads(_SENTINEL_PACK.read_text(encoding="utf-8"))
    assert payload.get("pack_id") == "day_one_architecture_guardrails_v1"
    assert "validate_day_one_architecture" in payload.get("validator_script", "")


def test_acceptance_audit_has_explicit_classification():
    audit = (
        _REPO / "docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md"
    ).read_text(encoding="utf-8")
    assert "accepted_for_wave1_launch" in audit
    assert "**Yes**" in audit
