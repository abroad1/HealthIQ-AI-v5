#!/usr/bin/env python3
"""
Build pass3_frame_coverage_audit_v1.yaml from pass3_legacy_package_mapping_plan_v1.yaml.

Governance audit helper — reads package signal libraries for override-rule counts only.
Does not modify packages.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "knowledge_bus" / "governance" / "pass3_legacy_package_mapping_plan_v1.yaml"
OUTPUT = ROOT / "knowledge_bus" / "governance" / "pass3_frame_coverage_audit_v1.yaml"
PACKAGES_DIR = ROOT / "knowledge_bus" / "packages"

WORK_ID = "PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit"

# Packages with known multiframe adjudication (estate governance references)
KNOWN_HIGH_RISK = frozenset(
    {
        "pkg_s24_creatinine_high_renal",
        "pkg_s24_crp_high_inflammation",
        "pkg_chronic_inflammation",
        "pkg_s24_alt_high_hepatocellular_injury",
        "pkg_s24_ferritin_high_overload",
        "pkg_kb45_apob_high_atherogenic",
    }
)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _override_rule_count(package_id: str) -> int:
    lib_path = PACKAGES_DIR / package_id / "signal_library.yaml"
    if not lib_path.is_file():
        return 0
    doc = _load_yaml(lib_path)
    signals = (doc or {}).get("signals") or []
    if not signals or not isinstance(signals[0], dict):
        return 0
    rules = signals[0].get("override_rules") or []
    return len(rules) if isinstance(rules, list) else 0


def _classify(entry: dict[str, Any]) -> dict[str, Any]:
    package_id = entry["package_id"]
    route = entry.get("promotion_route", "")
    multi = bool(entry.get("multiple_pass3_frames"))
    specs = list(entry.get("pass3_primary_biomarker_match_spec_ids") or [])
    pass3_count = len(specs)
    signal_ids = entry.get("current_signal_ids") or []
    biomarkers = entry.get("current_primary_biomarkers") or []
    signal_family = signal_ids[0] if signal_ids else "unknown"
    primary_bio = biomarkers[0] if biomarkers else "unknown"
    overrides = _override_rule_count(package_id)
    legacy_frames = max(1, overrides) if overrides else (1 if entry.get("runtime_loaded") else 0)

    manual_review = bool(entry.get("manual_review_required"))

    if route == "ROUTE_F_retire_candidate":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            legacy_frames,
            "legacy package scaffold",
            "legacy_likely_scaffold_or_retire_candidate",
            "none_detected",
            "retire_candidate",
            "retire_package",
            False,
            entry.get("notes", ""),
        )

    if package_id == "pkg_s24_creatinine_high_renal":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            2,
            "eGFR CKD-stage override; potassium acute-imbalance override (legacy s24)",
            "pass3_partial_legacy_frames_not_fully_represented",
            "high",
            "blocked_pending_pass3_enrichment",
            "creatinine_multiframe_adjudication; CF-CREATININE-001",
            True,
            "Pattern case: kb52c canonical; s24 eGFR/K+ not in Pass_3 GFR frame.",
        )

    if route == "ROUTE_D_legacy_accepted_with_rationale":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            len(signal_ids),
            "multi-signal KBP-0001 baseline library",
            "pass3_multiple_frames_need_adjudication",
            "medium",
            "blocked_pending_frame_adjudication",
            "per-signal frame adjudication before promotion",
            True,
            entry.get("notes", ""),
        )

    if route == "ROUTE_G_manual_medical_review_exception":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            1,
            "distinct signal_systemic_inflammation vs signal_crp_high",
            "legacy_contains_valid_unmapped_frame",
            "high",
            "blocked_pending_frame_adjudication",
            "author_new_pass3_frame",
            True,
            entry.get("notes", ""),
        )

    if route == "ROUTE_E_provenance_recovery_needed":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            1,
            "runtime package; provenance gap",
            "unclear_requires_manual_review",
            "unknown",
            "blocked_pending_provenance_recovery",
            "recover_provenance_then_re_audit",
            False,
            entry.get("notes", ""),
        )

    if route == "ROUTE_B_primary_biomarker_match_signal_mapping_needed":
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            1,
            "signal_id mismatch vs Pass_3",
            "pass3_partial_legacy_frames_not_fully_represented",
            "medium",
            "blocked_pending_frame_adjudication",
            "map_signal_id_then_compile",
            False,
            entry.get("notes", ""),
        )

    if route == "ROUTE_C_multiple_pass3_frames_adjudication_needed":
        edge = "high" if package_id in KNOWN_HIGH_RISK or pass3_count >= 3 else "medium"
        safety = (
            "blocked_pending_frame_adjudication"
            if multi
            else "blocked_pending_pass3_enrichment"
        )
        if package_id == "pkg_s24_crp_high_inflammation":
            safety = "blocked_pending_frame_adjudication"
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            legacy_frames,
            f"legacy runtime; {overrides} override rule(s) in package" if overrides else "legacy or context package",
            "pass3_multiple_frames_need_adjudication",
            edge,
            safety,
            entry.get("recommended_action", "adjudicate_pass3_frames_then_map"),
            manual_review,
            entry.get("notes", ""),
        )

    if route == "ROUTE_A_exact_signal_match_compile_candidate":
        if overrides >= 2:
            return _row(
                entry,
                signal_family,
                primary_bio,
                pass3_count,
                specs,
                overrides,
                f"{overrides} legacy override rules in signal_library",
                "pass3_partial_legacy_frames_not_fully_represented",
                "medium",
                "blocked_pending_pass3_enrichment",
                "frame_coverage_audit_before_route_a_promotion",
                True,
                "ROUTE_A label; legacy override richness requires enrichment check.",
            )
        if pass3_count > 1 and not multi:
            return _row(
                entry,
                signal_family,
                primary_bio,
                pass3_count,
                specs,
                1,
                "single active Pass_3 spec match; additional Pass_3 specs exist",
                "pass3_partial_legacy_frames_not_fully_represented",
                "low",
                "safe_after_documented_divergence_acceptance",
                "document_pass3_frame_selection_then_compile",
                False,
                entry.get("notes", ""),
            )
        return _row(
            entry,
            signal_family,
            primary_bio,
            pass3_count,
            specs,
            legacy_frames,
            "single-frame ROUTE_A; no multi-rule legacy override detected",
            "pass3_complete_for_known_frames",
            "low",
            "safe_for_route_a_promotion",
            "compile_and_promotion_pilot",
            False,
            entry.get("notes", ""),
        )

    return _row(
        entry,
        signal_family,
        primary_bio,
        pass3_count,
        specs,
        legacy_frames,
        "unclassified route",
        "unclear_requires_manual_review",
        "unknown",
        "blocked_pending_frame_adjudication",
        "manual_review",
        True,
        entry.get("notes", ""),
    )


def _row(
    entry: dict[str, Any],
    signal_family: str,
    primary_bio: str,
    pass3_count: int,
    specs: list[str],
    legacy_count: int,
    legacy_summary: str,
    coverage: str,
    edge_risk: str,
    safety: str,
    action: str,
    med_review: bool,
    notes: str,
) -> dict[str, Any]:
    authority = "runtime_loaded" if entry.get("runtime_loaded") else "not_runtime_loaded"
    return {
        "package_id": entry["package_id"],
        "signal_family_id": signal_family,
        "primary_biomarker_id": primary_bio,
        "current_route": entry.get("promotion_route"),
        "current_package_authority": authority,
        "pass3_frame_count": pass3_count,
        "pass3_frame_ids": specs,
        "legacy_frame_count": legacy_count,
        "legacy_frame_summary": legacy_summary.strip(),
        "frame_coverage_status": coverage,
        "edge_case_loss_risk": edge_risk,
        "promotion_safety_status": safety,
        "recommended_next_action": action,
        "requires_medical_review": med_review,
        "notes": notes.strip(),
    }


def build_audit() -> dict[str, Any]:
    plan = _load_yaml(MAPPING)
    packages_raw = plan.get("packages") or []
    rows = [_classify(p) for p in packages_raw]

    summary_keys = [
        "pass3_complete_for_known_frames",
        "pass3_partial_legacy_frames_not_fully_represented",
        "pass3_multiple_frames_need_adjudication",
        "legacy_contains_valid_unmapped_frame",
        "legacy_likely_scaffold_or_retire_candidate",
        "unclear_requires_manual_review",
    ]
    summary = {k: 0 for k in summary_keys}
    for r in rows:
        status = r["frame_coverage_status"]
        if status in summary:
            summary[status] += 1

    return {
        "schema_version": "1.0.0",
        "runtime_consumed": False,
        "status": "governance_audit_non_runtime",
        "work_id": WORK_ID,
        "source_register": "knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml",
        "package_count": len(rows),
        "summary_counts": summary,
        "packages": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Pass_3 frame coverage audit YAML.")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    audit = build_audit()
    args.output.write_text(
        yaml.safe_dump(audit, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"wrote {args.output} ({audit['package_count']} packages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
