"""
ARCH-CONV-PKG2 — canonical package runtime eligibility (launch-critical cohort).

Production reachability for launch-critical packages (pkg_kb47_*) requires
acceptable explicit lineage (EXPLICIT_SPEC or COMPILED_MANIFEST).

Non-launch-critical packages are out of Package 2 scope and remain loadable
under existing behaviour.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

from core.knowledge.provenance_status_v1 import (
    classify_package_provenance_status,
    is_beta_eligible_explicit_lineage,
)

LAUNCH_CRITICAL_PACKAGE_PREFIXES: Tuple[str, ...] = ("pkg_kb47_",)

# Eligibility vocabulary (auditable decisions)
ELIGIBILITY_PRODUCTION_REACHABLE = "production_reachable"
ELIGIBILITY_NON_REACHABLE = "non_reachable"
ELIGIBILITY_TEST_ONLY_OPT_IN = "test_only_opt_in"
ELIGIBILITY_OUT_OF_COHORT = "out_of_launch_critical_cohort"
ELIGIBILITY_UNKNOWN_FAIL_CLOSED = "unknown_fail_closed"

_REPO_ROOT = Path(__file__).resolve().parents[3]


def is_launch_critical_package_id(package_id: str) -> bool:
    pid = str(package_id or "").strip()
    return any(pid.startswith(prefix) for prefix in LAUNCH_CRITICAL_PACKAGE_PREFIXES)


def _env_allows_blocked_launch_critical() -> bool:
    raw = str(os.environ.get("HEALTHIQ_ALLOW_LAUNCH_CRITICAL_BLOCKED", "")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def load_package_manifest(package_dir: Path) -> Dict[str, Any]:
    path = package_dir / "package_manifest.yaml"
    if not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def classify_package_runtime_eligibility(
    *,
    package_id: str,
    manifest: Optional[Dict[str, Any]] = None,
    allow_launch_critical_blocked: bool = False,
    investigation_specs_root: Optional[Path] = None,
) -> Tuple[str, str]:
    """
    Return (eligibility, provenance_status).

    Fail closed for launch-critical packages without acceptable explicit lineage,
    unless an explicit test/harness opt-in is set.
    """
    pid = str(package_id or "").strip()
    if not pid:
        return ELIGIBILITY_UNKNOWN_FAIL_CLOSED, "UNRESOLVED"

    man = dict(manifest or {})
    status = classify_package_provenance_status(
        manifest=man,
        investigation_specs_root=investigation_specs_root,
    )

    if not is_launch_critical_package_id(pid):
        return ELIGIBILITY_OUT_OF_COHORT, status

    if is_beta_eligible_explicit_lineage(status):
        return ELIGIBILITY_PRODUCTION_REACHABLE, status

    if allow_launch_critical_blocked or _env_allows_blocked_launch_critical():
        return ELIGIBILITY_TEST_ONLY_OPT_IN, status

    return ELIGIBILITY_NON_REACHABLE, status


def is_production_reachable(
    *,
    package_id: str,
    manifest: Optional[Dict[str, Any]] = None,
    allow_launch_critical_blocked: bool = False,
    investigation_specs_root: Optional[Path] = None,
) -> bool:
    eligibility, _status = classify_package_runtime_eligibility(
        package_id=package_id,
        manifest=manifest,
        allow_launch_critical_blocked=allow_launch_critical_blocked,
        investigation_specs_root=investigation_specs_root,
    )
    return eligibility in {
        ELIGIBILITY_PRODUCTION_REACHABLE,
        ELIGIBILITY_OUT_OF_COHORT,
        ELIGIBILITY_TEST_ONLY_OPT_IN,
    }


def audit_launch_critical_exclusions(
    packages_root: Optional[Path] = None,
    *,
    allow_launch_critical_blocked: bool = False,
) -> List[Dict[str, str]]:
    """Deterministic audit rows for launch-critical packages excluded from production load."""
    root = packages_root or (_REPO_ROOT / "knowledge_bus" / "packages")
    rows: List[Dict[str, str]] = []
    for path in sorted(root.glob("pkg_kb47_*/package_manifest.yaml")):
        package_id = path.parent.name
        manifest = load_package_manifest(path.parent)
        eligibility, status = classify_package_runtime_eligibility(
            package_id=package_id,
            manifest=manifest,
            allow_launch_critical_blocked=allow_launch_critical_blocked,
        )
        if eligibility == ELIGIBILITY_NON_REACHABLE:
            rows.append(
                {
                    "package_id": package_id,
                    "eligibility": eligibility,
                    "provenance_status": status,
                    "disposition": "MAKE_NON_REACHABLE",
                }
            )
    return rows
