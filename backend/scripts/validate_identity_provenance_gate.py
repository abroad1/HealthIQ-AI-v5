#!/usr/bin/env python3
"""
ARCH-RT-IDENTITY-PROV-1 — Launch-critical identity and provenance gate.

Evaluates the bounded launch-critical cohort against ADR-RT-IDENTITY-PROV-001.
Distinguishes runtime compatibility from controlled-beta eligibility.
Does not fail the whole estate for out-of-cohort legacy packages.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "backend") not in sys.path:
    sys.path.insert(0, str(REPO / "backend"))

from core.knowledge.package_provenance_scan_v1 import scan_all_package_provenance  # noqa: E402
from core.knowledge.provenance_status_v1 import (  # noqa: E402
    classify_package_provenance_status,
    is_beta_eligible_explicit_lineage,
)
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity  # noqa: E402


LAUNCH_CRITICAL_PACKAGE_PREFIXES = ("pkg_kb47_",)


def _active_kb47_packages() -> List[Path]:
    packages_root = REPO / "knowledge_bus" / "packages"
    out: List[Path] = []
    for path in sorted(packages_root.iterdir()):
        if not path.is_dir():
            continue
        if not path.name.startswith(LAUNCH_CRITICAL_PACKAGE_PREFIXES):
            continue
        manifest = path / "package_manifest.yaml"
        if not manifest.is_file():
            continue
        payload = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        # Cohort: runtime-active packages (canonical activation register).
        status = str(payload.get("governance_runtime_activation_status") or "").strip()
        behavioural = str(payload.get("behavioural_impact") or "").strip()
        if status == "runtime_active_canonical" or behavioural == "SIGNAL_RUNTIME_ACTIVATION":
            out.append(path)
    return out


def main() -> int:
    errors: List[str] = []
    warnings: List[str] = []
    inventory: List[Dict[str, Any]] = []

    scan_rows = {r.package_id: r for r in scan_all_package_provenance()}
    packages = _active_kb47_packages()
    if not packages:
        errors.append("No launch-critical kb47 runtime-active packages found")

    seen_keys: Dict[str, str] = {}
    for pkg_dir in packages:
        manifest_path = pkg_dir / "package_manifest.yaml"
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        package_id = pkg_dir.name
        scan = scan_rows.get(package_id)
        scan_class = scan.classification if scan else None
        status = classify_package_provenance_status(
            manifest=payload if isinstance(payload, dict) else {},
            classification_scan=scan_class,
        )
        lib = pkg_dir / "signal_library.yaml"
        signal_id = ""
        activation_key = ""
        source_spec_id = ""
        if lib.is_file():
            lib_payload = yaml.safe_load(lib.read_text(encoding="utf-8")) or {}
            signals = lib_payload.get("signals") if isinstance(lib_payload, dict) else None
            if isinstance(signals, list) and signals:
                first = signals[0] if isinstance(signals[0], dict) else {}
                signal_id = str(first.get("signal_id") or "").strip()
            if signal_id:
                activation_key, source_spec_id, _ = resolve_activation_identity(
                    signal_id=signal_id,
                    signal_library_path=lib,
                )
        if activation_key:
            if activation_key in seen_keys and seen_keys[activation_key] != package_id:
                errors.append(
                    f"activation_key collision: {activation_key} in {seen_keys[activation_key]} and {package_id}"
                )
            seen_keys[activation_key] = package_id

        if status == "EXPLICIT_SPEC" and not (REPO / "knowledge_bus" / "research" / "investigation_specs" / f"{source_spec_id}.yaml").is_file():
            errors.append(f"{package_id}: false EXPLICIT_SPEC claim for {source_spec_id}")

        beta_ok = is_beta_eligible_explicit_lineage(status)
        if not beta_ok:
            warnings.append(
                f"{package_id}: provenance_status={status} — beta-ineligible for explicit-lineage claims"
            )

        inventory.append(
            {
                "package_id": package_id,
                "signal_id": signal_id,
                "source_spec_id": source_spec_id,
                "activation_key": activation_key,
                "provenance_status": status,
                "scan_classification": scan_class,
                "compile_manifest_ref": None,
                "runtime_consumer": "SignalRegistry / SignalEvaluator",
                "beta_eligible_explicit_lineage": beta_ok,
                "unresolved_action": (
                    None
                    if beta_ok
                    else "Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim"
                ),
            }
        )

    # Compiled vitamin-D hypothesis — COMPILED_MANIFEST cohort member
    inventory.append(
        {
            "package_id": None,
            "signal_id": "signal_vitamin_d_low",
            "source_spec_id": None,
            "activation_key": None,
            "provenance_status": "COMPILED_MANIFEST",
            "scan_classification": None,
            "compile_manifest_ref": "knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml",
            "runtime_consumer": "compiled_hypothesis / root_cause_compiler",
            "beta_eligible_explicit_lineage": True,
            "unresolved_action": None,
        }
    )

    out_path = REPO / "docs" / "architecture" / "ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md"
    lines = [
        "# ARCH-RT-IDENTITY-PROV-1 — Launch-critical provenance inventory",
        "",
        "Generated deterministically by `backend/scripts/validate_identity_provenance_gate.py`.",
        "",
        "| package_id | signal_id | source_spec_id | activation_key | provenance_status | beta_eligible_explicit | unresolved_action |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in inventory:
        lines.append(
            "| {package_id} | {signal_id} | {source_spec_id} | {activation_key} | {provenance_status} | {beta} | {action} |".format(
                package_id=row.get("package_id") or "—",
                signal_id=row.get("signal_id") or "—",
                source_spec_id=row.get("source_spec_id") or "—",
                activation_key=row.get("activation_key") or "—",
                provenance_status=row.get("provenance_status"),
                beta=row.get("beta_eligible_explicit_lineage"),
                action=row.get("unresolved_action") or "—",
            )
        )
    lines.extend(
        [
            "",
            "## Naming authority",
            "",
            "- `compile_manifest_ref` — canonical logical reference on compiled artefacts.",
            "- `compile_manifest_path` — estate-index internal path field (same files; not a competing authority).",
            "",
            "## Scanner roles",
            "",
            "- `package_provenance_scan_v1.scan_all_package_provenance` — estate-wide classification inventory.",
            "- `launch_estate_v1.scan_package_provenance` — launch-estate focused row set.",
            "- Shared overlapping facts must use consistent terminology; this gate is the beta-readiness view for the launch-critical cohort.",
            "",
        ]
    )
    # newline='\n' avoids Windows text-mode CRLF rewrites that dirty porcelain at kernel finish.
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"errors": errors, "warnings": warnings, "inventory_rows": len(inventory)}, indent=2))
    if errors:
        print("identity_provenance_gate: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("identity_provenance_gate: PASS")
    for w in warnings:
        print(f"  warning: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
