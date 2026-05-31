#!/usr/bin/env python3
"""
ARCH-RT-6 — Deterministic day-one architecture guardrail validator.

Read-only: does not mutate repository files. Exits non-zero on violation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence

import yaml

_REPO = Path(__file__).resolve().parents[2]

_LAUNCH_CRITICAL_REL_PATHS: Sequence[str] = (
    "backend/core/knowledge/health_system_card_evidence.py",
    "backend/core/knowledge/compiled_hypothesis.py",
    "backend/core/knowledge/load_root_cause_hypotheses.py",
    "backend/core/analytics/root_cause_compiler_v1.py",
    "backend/core/analytics/wave1_subsystem_evidence.py",
    "backend/core/analytics/report_compiler_v1.py",
    "backend/core/analytics/domain_narrative_wave1.py",
    "backend/core/analytics/signal_evaluator.py",
    "backend/core/pipeline/orchestrator.py",
    "backend/core/pipeline/orchestrator_phases_v1.py",
)

_PSI_FORBIDDEN_MARKERS: Sequence[str] = (
    "load_promoted_signal_intelligence",
    "from core.knowledge.load_promoted_signal_intelligence",
)

_INVESTIGATION_SPEC_RUNTIME_MARKERS: Sequence[str] = (
    "knowledge_bus/research/investigation_specs",
    "investigation_specs/",
    "validate_investigation_spec",
    "investigation_spec_to_promoted_signal",
)

_LAUNCH_MANIFEST_NAMES: Sequence[str] = (
    "arch_rt3_glycaemic_card_evidence.yaml",
    "arch_rt4_vitamin_d_hypothesis.yaml",
    "arch_rt5b_lipid_transport_card_evidence.yaml",
    "arch_rt5b_homocysteine_pathway_card_evidence.yaml",
    "arch_rt5b_vascular_strain_card_evidence.yaml",
    "arch_rt5b_insulin_metabolic_card_evidence.yaml",
    "arch_rt5b_enzyme_pattern_card_evidence.yaml",
    "arch_rt5b_processing_context_card_evidence.yaml",
)

_AUTHORITY_MANIFEST = _REPO / "docs/audit-papers/active_intelligence_authority_manifest.md"
_FRONTEND_SUBSYSTEM = (
    _REPO / "frontend" / "app" / "components" / "results" / "Wave1SubsystemEvidenceSection.tsx"
)


def _read(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def validate_wave1_card_estate(errors: List[str]) -> None:
    sys.path.insert(0, str(_REPO / "backend"))
    from core.knowledge.health_system_card_evidence import (  # noqa: PLC0415
        WAVE1_COMPILED_SUBSYSTEM_IDS,
        get_card_evidence_artefact,
    )
    from core.knowledge.launch_estate_v1 import (  # noqa: PLC0415
        estate_index_path,
        resolve_compile_manifest_ref,
        wave1_subsystem_authority_rows,
    )

    rows = wave1_subsystem_authority_rows()
    if len(rows) != 7:
        _err(errors, f"expected 7 Wave 1 subsystems, got {len(rows)}")
    for row in rows:
        sid = row["subsystem_id"]
        if sid in WAVE1_COMPILED_SUBSYSTEM_IDS:
            if row["active_authority"] != "compiled_card_evidence":
                _err(
                    errors,
                    f"{sid} must use compiled_card_evidence, got {row['active_authority']!r}",
                )
        elif row["active_authority"] == "hard_coded_python":
            _err(errors, f"unexpected hard_coded_python authority for {sid}")

    index = yaml.safe_load(estate_index_path().read_text(encoding="utf-8")) or {}
    legacy = (index.get("wave1_subsystems_legacy_hard_coded") or {}).get("subsystem_ids") or []
    if legacy:
        _err(errors, f"legacy hard-coded Wave 1 subsystems must be empty, got {legacy!r}")

    indexed = {r["subsystem_id"] for r in index.get("card_evidence_artefacts") or []}
    if indexed != set(WAVE1_COMPILED_SUBSYSTEM_IDS):
        _err(errors, "estate index card_evidence_artefacts must match WAVE1_COMPILED_SUBSYSTEM_IDS")

    for subsystem_id in WAVE1_COMPILED_SUBSYSTEM_IDS:
        artefact = get_card_evidence_artefact(subsystem_id)
        if "total_bilirubin" in {m.marker_id for m in artefact.markers}:
            _err(errors, f"{subsystem_id} artefact must not list total_bilirubin")
        if not resolve_compile_manifest_ref(artefact.compile_manifest_ref):
            _err(errors, f"{subsystem_id} compile_manifest_ref does not resolve")


def validate_compile_manifests(errors: List[str]) -> None:
    manifests_dir = _REPO / "knowledge_bus" / "compiled" / "manifests"
    for name in _LAUNCH_MANIFEST_NAMES:
        path = manifests_dir / name
        if not path.is_file():
            _err(errors, f"missing launch manifest: {name}")
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        compile_id = doc.get("compile_id")
        compile_run_id = doc.get("compile_run_id")
        if isinstance(compile_run_id, str) and compile_run_id.strip():
            if not isinstance(compile_id, str) or compile_run_id.strip() != compile_id.strip():
                _err(
                    errors,
                    f"{name}: compile_run_id must equal compile_id",
                )
        for spec in doc.get("source_specs") or []:
            if isinstance(spec, dict) and spec.get("source_hash") == "pending_inventory_refresh":
                _err(errors, f"{name}: pending_inventory_refresh in source_specs")
        for out in doc.get("outputs") or []:
            if isinstance(out, dict) and out.get("output_hash") == "pending_inventory_refresh":
                _err(errors, f"{name}: pending_inventory_refresh in outputs")


def validate_compiled_hypothesis_promotion(errors: List[str]) -> None:
    sys.path.insert(0, str(_REPO / "backend"))
    from core.knowledge.compiled_hypothesis import (  # noqa: PLC0415
        RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS,
        get_compiled_hypothesis_artefact,
        runtime_summary_for_hypothesis,
    )

    if "signal_vitamin_d_low" not in RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS:
        _err(errors, "signal_vitamin_d_low must be runtime-promoted compiled hypothesis")
    artefact = get_compiled_hypothesis_artefact("signal_vitamin_d_low")
    if len(artefact.hypotheses) != 1:
        _err(errors, "signal_vitamin_d_low must remain single-frame (no multi-frame promotion)")
    row = artefact.hypotheses[0]
    if not row.summary_template or not row.summary_template.strip():
        _err(errors, "promoted compiled hypothesis must have summary_template")
    summary = runtime_summary_for_hypothesis(row)
    claim = (row.physiological_claim or "").strip()
    if claim and claim == summary:
        _err(errors, "runtime summary must not equal physiological_claim verbatim")


def validate_package_provenance(errors: List[str]) -> None:
    sys.path.insert(0, str(_REPO / "backend"))
    from core.knowledge.package_provenance_scan_v1 import (  # noqa: PLC0415
        ARCH_RT5D_CLASSIFICATIONS,
        scan_all_package_provenance,
    )

    rows = scan_all_package_provenance()
    if len(rows) != 186:
        _err(errors, f"expected 186 classified packages, got {len(rows)}")
    for row in rows:
        if row.classification not in ARCH_RT5D_CLASSIFICATIONS:
            _err(errors, f"unclassified package {row.package_id}: {row.classification!r}")
        if row.classification == "unknown_requires_review":
            _err(errors, f"package {row.package_id} requires review")
        if row.source_spec_id_on_manifest and row.classification != "explicit_source_spec_id":
            _err(
                errors,
                f"package {row.package_id}: manifest source_spec_id without explicit classification",
            )


def validate_psi_isolation(errors: List[str]) -> None:
    for rel in _LAUNCH_CRITICAL_REL_PATHS:
        text = _read(rel)
        for marker in _PSI_FORBIDDEN_MARKERS:
            if marker in text:
                _err(errors, f"{rel} must not import PSI ({marker!r})")


def validate_no_runtime_investigation_spec_reads(errors: List[str]) -> None:
    allowed_translation = "backend/core/knowledge/investigation_spec_to_promoted_signal.py"
    for rel in _LAUNCH_CRITICAL_REL_PATHS:
        if rel == allowed_translation:
            continue
        text = _read(rel)
        for marker in _INVESTIGATION_SPEC_RUNTIME_MARKERS:
            if marker in text:
                _err(errors, f"{rel} must not reference raw investigation specs at runtime ({marker!r})")


def validate_frontend_guards(errors: List[str]) -> None:
    if not _FRONTEND_SUBSYSTEM.is_file():
        _err(errors, f"missing frontend component: {_FRONTEND_SUBSYSTEM}")
        return
    src = _FRONTEND_SUBSYSTEM.read_text(encoding="utf-8")
    if "isConsumerSafeSourceTrace" not in src:
        _err(errors, "frontend must filter internal source_trace via isConsumerSafeSourceTrace")
    if "wave1_subsystem_evidence_v1:" in src:
        _err(errors, "frontend must not render raw wave1_subsystem_evidence_v1 source traces")
    if "inferMarkerRole" in src or "deriveClinical" in src:
        _err(errors, "frontend must not infer marker clinical roles")


def validate_authority_manifest(errors: List[str]) -> None:
    if not _AUTHORITY_MANIFEST.is_file():
        _err(errors, "missing active_intelligence_authority_manifest.md")
        return
    text = _AUTHORITY_MANIFEST.read_text(encoding="utf-8")
    for token in (
        "ARCH-RT-6",
        "ARCH-RT-5E",
        "deferred_non_launch_blocker",
        "launch_included_compiled",
        "validate_day_one_architecture",
    ):
        if token not in text:
            _err(errors, f"authority manifest missing required token: {token!r}")


def validate_med_rev1_wave1_visibility(errors: List[str]) -> None:
    """MED-REV-1: compiled tier assignments must match medical review v1 visibility model."""
    sys.path.insert(0, str(_REPO / "backend"))
    from core.knowledge.health_system_card_evidence import (  # noqa: PLC0415
        WAVE1_COMPILED_SUBSYSTEM_IDS,
        WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS,
        WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS,
        get_card_evidence_artefact,
    )

    for subsystem_id in WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS:
        tier = get_card_evidence_artefact(subsystem_id).visibility_tier
        if tier != "scored_subsystem":
            _err(
                errors,
                f"MED-REV-1: {subsystem_id} must be scored_subsystem, got {tier!r}",
            )

    for subsystem_id in WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS:
        tier = get_card_evidence_artefact(subsystem_id).visibility_tier
        if tier != "hidden_v1":
            _err(
                errors,
                f"MED-REV-1: {subsystem_id} must be hidden_v1, got {tier!r}",
            )

    lipid = get_card_evidence_artefact("wave1_cv_lipid_transport")
    if "atherogenic" not in lipid.subsystem_label.lower():
        _err(errors, "MED-REV-1: lipid subsystem label must reference atherogenic lipid pattern")

    glycaemic = get_card_evidence_artefact("wave1_met_glycaemic_control")
    if glycaemic.subsystem_label != "Long-term blood sugar":
        _err(errors, "MED-REV-1: glycaemic subsystem label must be 'Long-term blood sugar'")

    glucose = next(m for m in glycaemic.markers if m.marker_id == "glucose")
    if glucose.presence_policy != "optional_on_panel":
        _err(errors, "MED-REV-1: glycaemic glucose must use optional_on_panel presence policy")

    if WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS | WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS != WAVE1_COMPILED_SUBSYSTEM_IDS:
        _err(errors, "MED-REV-1: visibility partition must cover all seven Wave 1 subsystems")


def validate_kb_util1_wave1_card_enrichment(errors: List[str]) -> None:
    """KB-UTIL-1: visible Wave 1 card surfaces must expose governed enrichment fields."""
    sys.path.insert(0, str(_REPO / "backend"))
    from core.knowledge.domain_flat_card_evidence import load_domain_flat_evidence_artefact  # noqa: PLC0415
    from core.knowledge.health_system_card_evidence import get_card_evidence_artefact  # noqa: PLC0415

    lipid = get_card_evidence_artefact("wave1_cv_lipid_transport")
    if not lipid.subsystem_summary or not lipid.evidence_limitations_line:
        _err(errors, "KB-UTIL-1: lipid artefact must include subsystem_summary and evidence_limitations_line")

    glycaemic = get_card_evidence_artefact("wave1_met_glycaemic_control")
    if not glycaemic.subsystem_summary or not glycaemic.evidence_limitations_line:
        _err(errors, "KB-UTIL-1: glycaemic artefact must include enrichment summary/limitations")

    liver_flat = load_domain_flat_evidence_artefact("wave1_liver")
    if not liver_flat.domain_summary_line or not liver_flat.evidence_limitations_line:
        _err(errors, "KB-UTIL-1: liver flat artefact must include summary and limitations")

    assembler = _read("backend/core/analytics/domain_score_assembler.py")
    if "flat_domain_evidence" not in assembler:
        _err(errors, "KB-UTIL-1: domain_score_assembler must attach flat_domain_evidence for liver")


def validate_wave1_assembler_routing(errors: List[str]) -> None:
    src = _read("backend/core/analytics/wave1_subsystem_evidence.py")
    if "PILOT_COMPILED_SUBSYSTEM_IDS" not in src:
        _err(errors, "wave1_subsystem_evidence must route compiled subsystems via PILOT_COMPILED_SUBSYSTEM_IDS")
    if "assemble_subsystem_from_compiled_card_evidence" not in src:
        _err(errors, "wave1_subsystem_evidence must call assemble_subsystem_from_compiled_card_evidence")


def validate_signal_library_uniqueness(errors: List[str]) -> None:
    """
    Rule 13–15: fail closed on silent within-file collapse; activation_key is frame identity.

    Cross-package signal_id reuse is permitted when activation_key differs (MULTI_FRAME policy).
    """
    packages = _REPO / "knowledge_bus" / "packages"
    global_activation: dict[str, str] = {}
    for lib_path in sorted(packages.glob("*/signal_library.yaml")):
        doc = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        pkg = lib_path.parent.name
        local_signal: dict[str, int] = {}
        local_activation: dict[str, int] = {}
        for entry in doc.get("signals") or []:
            if not isinstance(entry, dict):
                continue
            sid = str(entry.get("signal_id") or "").strip()
            if sid:
                local_signal[sid] = local_signal.get(sid, 0) + 1
            akey = str(entry.get("activation_key") or "").strip()
            if akey:
                local_activation[akey] = local_activation.get(akey, 0) + 1
                if akey in global_activation:
                    _err(
                        errors,
                        f"duplicate activation_key {akey!r} in {pkg} and {global_activation[akey]}",
                    )
                global_activation[akey] = pkg
        for sid, count in local_signal.items():
            if count > 1:
                _err(errors, f"duplicate signal_id {sid!r} within {pkg}/signal_library.yaml ({count} entries)")
        for akey, count in local_activation.items():
            if count > 1:
                _err(
                    errors,
                    f"duplicate activation_key {akey!r} within {pkg}/signal_library.yaml ({count} entries)",
                )


def run_day_one_architecture_validation(*, repo_root: Path | None = None) -> List[str]:
    global _REPO  # noqa: PLW0603
    if repo_root is not None:
        _REPO = repo_root
    errors: List[str] = []
    validate_wave1_card_estate(errors)
    validate_compile_manifests(errors)
    validate_compiled_hypothesis_promotion(errors)
    validate_package_provenance(errors)
    validate_psi_isolation(errors)
    validate_no_runtime_investigation_spec_reads(errors)
    validate_frontend_guards(errors)
    validate_authority_manifest(errors)
    validate_wave1_assembler_routing(errors)
    validate_med_rev1_wave1_visibility(errors)
    validate_kb_util1_wave1_card_enrichment(errors)
    validate_signal_library_uniqueness(errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ARCH-RT day-one architecture guardrails.")
    parser.add_argument("--repo", type=Path, default=_REPO, help="Repository root")
    args = parser.parse_args()
    errors = run_day_one_architecture_validation(repo_root=args.repo)
    if errors:
        print("day_one_architecture_validation: FAIL", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("day_one_architecture_validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
