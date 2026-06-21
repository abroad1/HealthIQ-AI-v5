#!/usr/bin/env python3
"""
Report-only activation-readiness audit for staged promoted_signal_intelligence artefacts.

Reads staged PSI under knowledge_bus/generated_pilot/ (P1-10, P1-11, P1-12 batches).
Does not mutate files, activate runtime, or resolve biomarker identity mappings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SSOT_PATH = ROOT / "backend" / "ssot" / "biomarkers.yaml"
DEFAULT_PSI_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "promoted_signal_intelligence_schema_v1.yaml"
DEFAULT_PACKAGES_ROOT = ROOT / "knowledge_bus" / "packages"

STAGED_BATCHES: dict[str, Path] = {
    "p1_10_batch_a": ROOT / "knowledge_bus" / "generated_pilot" / "p1_10_batch_a",
    "p1_11_batch_b": ROOT / "knowledge_bus" / "generated_pilot" / "p1_11_batch_b",
    "p1_12_batch_c": ROOT / "knowledge_bus" / "generated_pilot" / "p1_12_batch_c",
}

# Metrics requiring runtime calculation before signal evaluation may be listed here.
# Lab-provided SSOT-canonical markers must not appear (P1-18: transferrin_saturation is
# canonical in biomarkers.yaml and accepted on the runtime input model as lab-provided).
DERIVED_MARKER_IDS: frozenset[str] = frozenset()

FORBIDDEN_PSI_ROOT_KEYS = frozenset(
    {
        "hypotheses",
        "hypothesis_ranking",
        "narrative",
        "rendering",
        "presentation",
        "display",
        "report_layout",
        "ui_hints",
    }
)

# Documented carry-forwards from P1-10/11/12 batch manifests — not medical adjudication.
MEDICAL_REVIEW_PACKAGE_IDS = frozenset(
    {
        "pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment",
        "pkg_kb52c_homocysteine_high_renal_clearance_reduction",
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "pkg_kb52c_iron_high_iron_overload_context",
        "pkg_kb52c_iron_high_hepatocellular_or_hemolytic_release",
        "pkg_kb52c_neutrophil_pct_high_neutrophil_predominant_leukocyte_shift",
        "pkg_kb52c_lym_low_lymphopenia_stress_or_immunosuppression",
        "pkg_kb52c_wbc_high_reactive_leukocytosis",
    }
)

FRAME_AUTHORITY_PACKAGE_IDS = frozenset(
    {
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "pkg_kb52c_iron_high_iron_overload_context",
        "pkg_kb52c_iron_high_hepatocellular_or_hemolytic_release",
    }
)

SYSTEM_MAPPING_REVIEW_PACKAGE_IDS = frozenset(
    {
        "pkg_kb52c_neutrophil_pct_high_neutrophil_predominant_leukocyte_shift",
        "pkg_kb52c_lym_low_lymphopenia_stress_or_immunosuppression",
        "pkg_kb52c_wbc_high_reactive_leukocytosis",
    }
)


@dataclass
class AuditItem:
    id: str
    batch: str
    psi_path: str
    compile_manifest_path: str | None
    primary_metric_biomarker_id: str | None
    primary_metric_ssot_status: str
    supporting_marker_ssot_status: str
    runtime_active: str
    production_manifest_opt_in: str
    compile_manifest_hash_status: str
    activation_readiness: str
    blockers: list[str] = field(default_factory=list)
    recommended_next_action: str = ""


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_ssot_keys(ssot_path: Path) -> set[str]:
    data = _load_yaml(ssot_path)
    biomarkers = data.get("biomarkers") if isinstance(data, dict) else None
    if not isinstance(biomarkers, dict):
        raise ValueError(f"Invalid SSOT structure in {ssot_path}")
    return set(biomarkers.keys())


def load_psi_schema_vocab(schema_path: Path) -> tuple[set[str], set[str]]:
    schema = _load_yaml(schema_path)
    systems = set((schema or {}).get("signal_system_allowed") or [])
    triggers = set((schema or {}).get("trigger_direction_allowed") or [])
    return systems, triggers


def load_production_opt_in_package_ids(packages_root: Path) -> set[str]:
    opted_in: set[str] = set()
    if not packages_root.is_dir():
        return opted_in
    for manifest_path in packages_root.glob("*/package_manifest.yaml"):
        try:
            doc = _load_yaml(manifest_path)
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(doc, dict) and doc.get("promoted_signal_intelligence"):
            opted_in.add(manifest_path.parent.name)
    return opted_in


def validate_psi_structure(doc: dict[str, Any], schema_path: Path) -> list[str]:
    if str(ROOT / "backend") not in sys.path:
        sys.path.insert(0, str(ROOT / "backend"))
    from scripts.validate_promoted_signal_intelligence import (  # noqa: WPS433
        validate_promoted_signal_intelligence,
    )

    schema_doc = _load_yaml(schema_path)
    errors: list[str] = []
    validate_promoted_signal_intelligence(doc, schema_doc=schema_doc, source_path=None, errors=errors)
    return errors


def classify_item(blockers: list[str]) -> str:
    priority = [
        ("runtime_active is not false", "NOT_ELIGIBLE_FOR_ACTIVATION"),
        ("production package manifest opt-in present", "NOT_ELIGIBLE_FOR_ACTIVATION"),
        ("compile manifest missing", "BLOCKED_MANIFEST_OR_HASH"),
        ("psi file without matching compile manifest", "BLOCKED_MANIFEST_OR_HASH"),
        ("compile manifest hash mismatch", "BLOCKED_MANIFEST_OR_HASH"),
        ("PSI structural validation failed", "BLOCKED_SCHEMA_OR_VALIDATOR"),
        ("forbidden PSI root field", "BLOCKED_SCHEMA_OR_VALIDATOR"),
        ("invalid signal_system", "BLOCKED_SCHEMA_OR_VALIDATOR"),
        ("invalid trigger_direction", "BLOCKED_SCHEMA_OR_VALIDATOR"),
        ("primary_metric.biomarker_id not in SSOT", "BLOCKED_BIOMARKER_IDENTITY"),
        ("supporting marker biomarker_id not in SSOT", "BLOCKED_BIOMARKER_IDENTITY"),
        ("derived-marker supporting dependency", "BLOCKED_DERIVED_MARKER_DEPENDENCY"),
        ("documented medical-review carry-forward", "BLOCKED_MEDICAL_REVIEW_REQUIRED"),
        ("documented frame-authority carry-forward", "BLOCKED_FRAME_AUTHORITY"),
        ("documented system-mapping review carry-forward", "BLOCKED_SYSTEM_MAPPING"),
        ("missing source spec ID in compile manifest", "BLOCKED_SOURCE_SUPPORT"),
    ]
    blocker_set = set(blockers)
    for needle, classification in priority:
        if any(needle in b for b in blocker_set):
            return classification
    return "ACTIVATION_READY"


def audit_staged_batch(
    batch_name: str,
    batch_root: Path,
    *,
    ssot_keys: set[str],
    signal_systems: set[str],
    trigger_directions: set[str],
    production_opt_ins: set[str],
    psi_schema_path: Path,
) -> list[AuditItem]:
    items: list[AuditItem] = []
    if not batch_root.is_dir():
        return items

    psi_files = sorted(batch_root.glob("*/promoted_signal_intelligence.yaml"))
    manifest_paths = {
        p.parent.name: p for p in batch_root.glob("*/compile_manifest.yaml")
    }

    for psi_path in psi_files:
        package_id = psi_path.parent.name
        try:
            rel_psi = psi_path.relative_to(ROOT).as_posix()
        except ValueError:
            rel_psi = psi_path.as_posix()
        manifest_path = manifest_paths.get(package_id)
        if manifest_path:
            try:
                rel_manifest = manifest_path.relative_to(ROOT).as_posix()
            except ValueError:
                rel_manifest = manifest_path.as_posix()
        else:
            rel_manifest = None
        item_id = f"{batch_name}__{package_id}"

        blockers: list[str] = []
        primary_id: str | None = None
        primary_ssot = "not_checked"
        supporting_status = "not_applicable"
        runtime_active = "unknown"
        production_opt_in = "unknown"
        hash_status = "not_checked"

        try:
            psi_doc = _load_yaml(psi_path)
        except (OSError, yaml.YAMLError) as exc:
            blockers.append(f"PSI YAML unreadable: {exc}")
            psi_doc = None

        if isinstance(psi_doc, dict):
            for forbidden in FORBIDDEN_PSI_ROOT_KEYS:
                if forbidden in psi_doc:
                    blockers.append(f"forbidden PSI root field present: {forbidden}")

            signals = psi_doc.get("signals")
            if isinstance(signals, list) and signals and isinstance(signals[0], dict):
                sig = signals[0]
                primary = sig.get("primary_metric")
                if isinstance(primary, dict):
                    bid = primary.get("biomarker_id")
                    if isinstance(bid, str):
                        primary_id = bid
                        primary_ssot = "canonical" if bid in ssot_keys else "non_canonical"
                        if bid not in ssot_keys:
                            blockers.append(
                                f"primary_metric.biomarker_id not in SSOT: {bid}"
                            )

                td = sig.get("trigger_direction")
                if isinstance(td, str) and trigger_directions and td not in trigger_directions:
                    blockers.append(f"invalid trigger_direction: {td}")

                ss = sig.get("signal_system")
                if isinstance(ss, str) and signal_systems and ss not in signal_systems:
                    blockers.append(f"invalid signal_system: {ss}")

                supporting = sig.get("supporting_markers")
                non_canonical_supporting: list[str] = []
                derived_hits: list[str] = []
                if isinstance(supporting, list):
                    for sm in supporting:
                        if not isinstance(sm, dict):
                            continue
                        sm_id = sm.get("biomarker_id")
                        if not isinstance(sm_id, str):
                            continue
                        if sm_id not in ssot_keys:
                            non_canonical_supporting.append(sm_id)
                        if sm_id in DERIVED_MARKER_IDS:
                            derived_hits.append(sm_id)
                    if non_canonical_supporting:
                        supporting_status = "fail"
                        for sm_id in non_canonical_supporting:
                            blockers.append(
                                f"supporting marker biomarker_id not in SSOT: {sm_id}"
                            )
                    else:
                        supporting_status = "pass"
                    if derived_hits:
                        for dm in derived_hits:
                            blockers.append(
                                f"derived-marker supporting dependency: {dm}"
                            )
                else:
                    supporting_status = "not_applicable"

            struct_errors = validate_psi_structure(psi_doc, psi_schema_path)
            if struct_errors:
                blockers.append("PSI structural validation failed")
        else:
            primary_ssot = "missing"

        if manifest_path is None:
            blockers.append("compile manifest missing")
            blockers.append("psi file without matching compile manifest")
        else:
            try:
                manifest_doc = _load_yaml(manifest_path)
            except (OSError, yaml.YAMLError) as exc:
                blockers.append(f"compile manifest unreadable: {exc}")
                manifest_doc = None

            if isinstance(manifest_doc, dict):
                ra = manifest_doc.get("runtime_active")
                if ra is False:
                    runtime_active = "false"
                elif ra is True:
                    runtime_active = "true"
                    blockers.append("runtime_active is not false")
                else:
                    runtime_active = "unknown"
                    blockers.append("runtime_active is not false")

                if not manifest_doc.get("source_spec_id"):
                    blockers.append("missing source spec ID in compile manifest")

                output_hashes = manifest_doc.get("output_hashes_sha256")
                if isinstance(output_hashes, dict):
                    expected = output_hashes.get("promoted_signal_intelligence.yaml")
                    if isinstance(expected, str):
                        actual = _sha256_file(psi_path)
                        if actual != expected:
                            blockers.append("compile manifest hash mismatch")
                            hash_status = "fail"
                        else:
                            hash_status = "pass"
                    else:
                        hash_status = "fail"
                        blockers.append("compile manifest missing output_hashes_sha256 entry")
                else:
                    hash_status = "fail"
                    blockers.append("compile manifest hash mismatch")

        if package_id in production_opt_ins:
            production_opt_in = "true"
            blockers.append("production package manifest opt-in present")
        else:
            production_opt_in = "false"

        if package_id in MEDICAL_REVIEW_PACKAGE_IDS:
            blockers.append("documented medical-review carry-forward")
        if package_id in FRAME_AUTHORITY_PACKAGE_IDS:
            blockers.append("documented frame-authority carry-forward")
        if package_id in SYSTEM_MAPPING_REVIEW_PACKAGE_IDS:
            blockers.append("documented system-mapping review carry-forward")

        activation = classify_item(blockers)
        if activation == "ACTIVATION_READY":
            recommended = "eligible for future production opt-in review sprint"
        elif "primary_metric.biomarker_id not in SSOT" in " ".join(blockers):
            recommended = "SSOT biomarker identity adjudication required before opt-in"
        elif any("derived-marker" in b for b in blockers):
            recommended = "derived-marker runtime support review before opt-in"
        elif "documented medical-review" in " ".join(blockers):
            recommended = "medical-review sign-off required before opt-in"
        else:
            recommended = "resolve reported blockers before opt-in"

        items.append(
            AuditItem(
                id=item_id,
                batch=batch_name,
                psi_path=rel_psi,
                compile_manifest_path=rel_manifest,
                primary_metric_biomarker_id=primary_id,
                primary_metric_ssot_status=primary_ssot,
                supporting_marker_ssot_status=supporting_status,
                runtime_active=runtime_active,
                production_manifest_opt_in=production_opt_in,
                compile_manifest_hash_status=hash_status,
                activation_readiness=activation,
                blockers=sorted(set(blockers)),
                recommended_next_action=recommended,
            )
        )

    manifest_only = set(manifest_paths) - {p.parent.name for p in psi_files}
    for package_id in sorted(manifest_only):
        blockers = ["compile manifest without matching PSI file"]
        orphan_manifest = manifest_paths[package_id]
        try:
            rel_orphan_manifest = orphan_manifest.relative_to(ROOT).as_posix()
        except ValueError:
            rel_orphan_manifest = orphan_manifest.as_posix()
        items.append(
            AuditItem(
                id=f"{batch_name}__{package_id}__orphan_manifest",
                batch=batch_name,
                psi_path="",
                compile_manifest_path=rel_orphan_manifest,
                primary_metric_biomarker_id=None,
                primary_metric_ssot_status="missing",
                supporting_marker_ssot_status="not_applicable",
                runtime_active="unknown",
                production_manifest_opt_in="false",
                compile_manifest_hash_status="not_checked",
                activation_readiness="BLOCKED_MANIFEST_OR_HASH",
                blockers=blockers,
                recommended_next_action="restore matching PSI artefact or remove orphan manifest",
            )
        )

    return items


def audit_all_staged(
    *,
    ssot_path: Path = DEFAULT_SSOT_PATH,
    psi_schema_path: Path = DEFAULT_PSI_SCHEMA_PATH,
    packages_root: Path = DEFAULT_PACKAGES_ROOT,
    batches: dict[str, Path] | None = None,
) -> dict[str, Any]:
    ssot_keys = load_ssot_keys(ssot_path)
    signal_systems, trigger_directions = load_psi_schema_vocab(psi_schema_path)
    production_opt_ins = load_production_opt_in_package_ids(packages_root)
    batch_map = batches or STAGED_BATCHES

    all_items: list[AuditItem] = []
    for batch_name, batch_root in batch_map.items():
        all_items.extend(
            audit_staged_batch(
                batch_name,
                batch_root,
                ssot_keys=ssot_keys,
                signal_systems=signal_systems,
                trigger_directions=trigger_directions,
                production_opt_ins=production_opt_ins,
                psi_schema_path=psi_schema_path,
            )
        )

    activation_ready = sum(1 for i in all_items if i.activation_readiness == "ACTIVATION_READY")
    blocked = len(all_items) - activation_ready
    blocker_counts: dict[str, int] = {}
    for item in all_items:
        blocker_counts[item.activation_readiness] = blocker_counts.get(item.activation_readiness, 0) + 1

    top_blockers = sorted(
        ((k, v) for k, v in blocker_counts.items() if k != "ACTIVATION_READY"),
        key=lambda x: (-x[1], x[0]),
    )
    top_blocker_labels = [f"{name} ({count})" for name, count in top_blockers[:6]]

    psi_count = sum(1 for i in all_items if i.psi_path)
    manifest_count = sum(1 for i in all_items if i.compile_manifest_path)

    return {
        "staged_estate": {
            "batches_inspected": list(batch_map.keys()),
            "psi_files_found": psi_count,
            "compile_manifests_found": manifest_count,
            "production_opt_ins_found": len(production_opt_ins),
        },
        "summary": {
            "activation_ready_count": activation_ready,
            "blocked_count": blocked,
            "top_blockers": top_blocker_labels,
            "blocker_counts": blocker_counts,
        },
        "items": [asdict(i) for i in all_items],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report-only staged PSI activation-readiness audit (P1-13)."
    )
    parser.add_argument(
        "--ssot",
        default=str(DEFAULT_SSOT_PATH),
        help="Path to backend/ssot/biomarkers.yaml (read-only)",
    )
    parser.add_argument(
        "--psi-schema",
        default=str(DEFAULT_PSI_SCHEMA_PATH),
        help="Path to promoted_signal_intelligence_schema_v1.yaml",
    )
    parser.add_argument(
        "--packages-root",
        default=str(DEFAULT_PACKAGES_ROOT),
        help="Path to knowledge_bus/packages for opt-in scan",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit full audit report as JSON",
    )
    parser.add_argument(
        "--fail-on-blocked",
        action="store_true",
        help="Exit non-zero if any staged PSI is not ACTIVATION_READY",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    report = audit_all_staged(
        ssot_path=Path(args.ssot),
        psi_schema_path=Path(args.psi_schema),
        packages_root=Path(args.packages_root),
    )

    summary = report["summary"]
    estate = report["staged_estate"]
    print(f"staged_psi_activation_readiness: scanned")
    print(f"psi_files_found: {estate['psi_files_found']}")
    print(f"compile_manifests_found: {estate['compile_manifests_found']}")
    print(f"production_opt_ins_found: {estate['production_opt_ins_found']}")
    print(f"activation_ready_count: {summary['activation_ready_count']}")
    print(f"blocked_count: {summary['blocked_count']}")
    for label in summary["top_blockers"]:
        print(f"top_blocker: {label}")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))

    if args.fail_on_blocked and summary["blocked_count"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
