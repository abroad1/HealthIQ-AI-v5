#!/usr/bin/env python3
"""
KB-UTIL-2-PILOT — deterministic Pass_3 → pilot package artefact compiler.

Non-runtime: outputs under knowledge_bus/generated_pilot/kb_util_2_pilot/<package_id>/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPILER_VERSION = "kb_util2_pass3_pilot_compiler_v1.0.0"
OUTPUT_ROOT = ROOT / "knowledge_bus" / "generated_pilot" / "kb_util_2_pilot"
PASS3_BATCH4 = (
    ROOT / "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json"
)

PASS3_TOP_LEVEL_FIELDS = (
    "investigation_spec_contract_version",
    "spec_id",
    "signal_id",
    "research_domain",
    "primary_marker",
    "trigger_direction",
    "activation",
    "states",
    "supporting_markers",
    "hypotheses",
    "hypothesis_ranking",
    "confirmatory_tests",
    "override_rules",
    "evidence",
    "narrative",
)

PILOT_PACKAGES: tuple[dict[str, str], ...] = (
    {
        "package_id": "pkg_s24_creatinine_high_renal",
        "kbp_id": "KBP-9201",
        "spec_id": "inv_creatinine_high_reduced_glomerular_filtration",
        "pass3_path": str(PASS3_BATCH4.relative_to(ROOT)).replace("\\", "/"),
    },
    {
        "package_id": "pkg_s24_ferritin_low_iron_deficiency",
        "kbp_id": "KBP-9202",
        "spec_id": "inv_ferritin_low_iron_store_depletion",
        "pass3_path": str(PASS3_BATCH4.relative_to(ROOT)).replace("\\", "/"),
    },
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=True, allow_unicode=True, default_flow_style=False, width=120)


def _write_yaml(path: Path, data: Any) -> str:
    text = _canonical_yaml(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return _sha256_bytes(text.encode("utf-8"))


def _load_pass3_specs(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON array in {path}")
    return [item for item in payload if isinstance(item, dict)]


def _find_spec(specs: list[dict[str, Any]], spec_id: str) -> dict[str, Any]:
    for spec in specs:
        if spec.get("spec_id") == spec_id:
            return spec
    raise KeyError(f"spec_id not found: {spec_id}")


def _collect_contradiction_markers(hypotheses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for hyp in hypotheses:
        for ctr in hyp.get("contradiction_markers") or []:
            if not isinstance(ctr, dict):
                continue
            cid = str(ctr.get("contradiction_id", ""))
            if cid and cid in seen:
                continue
            if cid:
                seen.add(cid)
            out.append(
                {
                    "contradiction_id": ctr.get("contradiction_id"),
                    "marker_reference": ctr.get("marker_reference"),
                    "contradiction_rationale": ctr.get("contradiction_rationale"),
                    "contradiction_strength": ctr.get("contradiction_strength"),
                }
            )
    return out


def _collect_missing_data_policies(hypotheses: list[dict[str, Any]]) -> list[str]:
    policies: list[str] = []
    for hyp in hypotheses:
        md = hyp.get("missing_data") or {}
        policy = md.get("policy") if isinstance(md, dict) else None
        if isinstance(policy, str) and policy.strip():
            policies.append(policy.strip())
    return policies


def _map_override_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mapped: list[dict[str, Any]] = []
    for rule in rules or []:
        if not isinstance(rule, dict):
            continue
        entry: dict[str, Any] = {
            "rule_id": rule.get("rule_id"),
            "resulting_state": rule.get("resulting_state"),
            "description": rule.get("description"),
            "conditions": [],
        }
        for cond in rule.get("conditions") or []:
            if not isinstance(cond, dict):
                continue
            mapped_cond: dict[str, Any] = {
                "metric_id": cond.get("metric_id"),
                "operator": cond.get("operator"),
                "condition_type": cond.get("condition_type", "all_of"),
            }
            if cond.get("comparator_type"):
                mapped_cond["comparator_type"] = cond.get("comparator_type")
            if cond.get("boundary"):
                mapped_cond["boundary"] = cond.get("boundary")
            if cond.get("comparator_type") != "lab_range_boundary" and cond.get("value") is not None:
                mapped_cond["value"] = cond.get("value")
            entry["conditions"].append(mapped_cond)
        if rule.get("source_refs"):
            entry["source_refs"] = list(rule["source_refs"])
        mapped.append(entry)
    return mapped


def _compile_research_brief(spec: dict[str, Any]) -> dict[str, Any]:
    evidence = spec.get("evidence") or {}
    narrative = spec.get("narrative") or {}
    biomarkers = [spec["primary_marker"]["biomarker_id"]]
    for sm in spec.get("supporting_markers") or []:
        if isinstance(sm, dict) and sm.get("biomarker_id"):
            biomarkers.append(sm["biomarker_id"])
    sources_out: list[dict[str, Any]] = []
    for src in evidence.get("sources") or []:
        if not isinstance(src, dict):
            continue
        sources_out.append(
            {
                "source_id": src.get("source_id"),
                "paper_title": src.get("paper_title"),
                "journal": src.get("journal"),
                "year": src.get("year"),
            }
        )
    return {
        "research_domain": spec.get("research_domain"),
        "sources": sources_out,
        "biomarkers": sorted(set(biomarkers)),
        "derived_metrics": [],
        "physiological_claim": evidence.get("physiological_claim"),
        "evidence_strength": evidence.get("evidence_strength"),
        "research_summary": narrative.get("implications") or narrative.get("interpretation"),
    }


def _compile_signal_library(spec: dict[str, Any], kbp_id: str) -> dict[str, Any]:
    pm = spec["primary_marker"]
    primary_metric = pm["biomarker_id"]
    supporting = spec.get("supporting_markers") or []
    supporting_ids: list[str] = []
    for sm in supporting:
        if not isinstance(sm, dict) or not sm.get("biomarker_id"):
            continue
        supporting_ids.append(sm["biomarker_id"])
    biomarkers = sorted({primary_metric, *supporting_ids})
    narrative = spec.get("narrative") or {}
    activation = spec.get("activation") or {}
    activation_config = activation.get("activation_config") or {}
    trigger = spec.get("trigger_direction", "high")
    enable_lower = bool(activation_config.get("enable_lower_bound"))
    enable_upper = bool(activation_config.get("enable_upper_bound"))
    placeholder_op = ">=" if trigger == "high" else "<="

    signal_entry = {
        "signal_id": spec["signal_id"],
        "name": spec["signal_id"].replace("signal_", "").replace("_", " ").title(),
        "description": pm.get("rationale"),
        "system": pm.get("signal_system") or spec.get("research_domain"),
        "primary_metric": primary_metric,
        "trigger_direction": trigger,
        "supporting_metrics": supporting_ids,
        "dependencies": {
            "biomarkers": biomarkers,
            "derived_metrics": [],
            "signals": [],
        },
        "optional_dependencies": {"biomarkers": [], "derived_metrics": [], "signals": []},
        "thresholds": [
            {
                "threshold_id": f"{spec['signal_id']}_lab_range_activation_placeholder",
                "metric_id": primary_metric,
                "operator": placeholder_op,
                "value": 9999.0 if trigger == "high" else 0.0,
                "severity": "at_risk",
                "description": (
                    "Validator-compatibility placeholder; runtime activation is "
                    "lab-range driven per Pass 3 activation block."
                ),
            }
        ],
        "activation_logic": activation.get("activation_logic", "lab_range_exceeded"),
        "activation_config": {
            "enable_upper_bound": enable_upper,
            "upper_bound_state": activation_config.get("upper_bound_state", "suboptimal"),
            "enable_lower_bound": enable_lower,
            "lower_bound_state": activation_config.get("lower_bound_state", "suboptimal"),
        },
        "override_rules": _map_override_rules(spec.get("override_rules") or []),
        "output": {
            "signal_value": primary_metric,
            "signal_state": (spec.get("states") or {}).get("escalation_state", "at_risk"),
            "confidence": "confidence_model_v1",
            "primary_metric": primary_metric,
            "supporting_markers": supporting_ids,
        },
        "explanation": {
            "mechanism": narrative.get("mechanism"),
            "biological_pathway": narrative.get("biological_pathway"),
            "interpretation": narrative.get("interpretation"),
            "implications": narrative.get("implications"),
            "supporting_marker_roles": narrative.get("supporting_marker_roles"),
        },
    }
    return {
        "library": {
            "package_id": kbp_id,
            "schema_version": "1.0.0",
            "package_version": "1.0.0",
            "library_name": f"{spec['signal_id']} Investigation Library (Pass 3 pilot)",
            "description": f"Pilot-compiled from {spec['spec_id']} via {COMPILER_VERSION}.",
        },
        "signals": [signal_entry],
    }


def _compile_promoted_signal_intelligence(spec: dict[str, Any], package_id: str) -> dict[str, Any]:
    pm = spec["primary_marker"]
    hypotheses = spec.get("hypotheses") or []
    evidence = spec.get("evidence") or {}
    activation = spec.get("activation") or {}
    states = spec.get("states") or {}
    supporting_markers = []
    for sm in spec.get("supporting_markers") or []:
        if isinstance(sm, dict):
            supporting_markers.append(
                {
                    "biomarker_id": sm.get("biomarker_id"),
                    "expected_direction": sm.get("expected_direction"),
                    "role": sm.get("role"),
                    "relationship_kind": sm.get("relationship_kind"),
                    "availability": sm.get("availability"),
                    "rationale": sm.get("rationale"),
                }
            )
    confirmatory_refs = []
    for ct in spec.get("confirmatory_tests") or []:
        if isinstance(ct, dict):
            confirmatory_refs.append(
                {"test_id": ct.get("test_id"), "rationale": ct.get("rationale")}
            )
    evidence_sources = []
    for src in evidence.get("sources") or []:
        if isinstance(src, dict):
            evidence_sources.append(
                {
                    "source_id": src.get("source_id"),
                    "paper_title": src.get("paper_title"),
                    "journal": src.get("journal"),
                    "year": src.get("year"),
                }
            )
    return {
        "promoted_signal_intelligence_contract_version": "1.0.0",
        "schema_version": "1.0.0",
        "package_id": package_id,
        "translation": {
            "source": "investigation_spec_v3_pass3_pilot",
            "investigation_spec_contract_version": spec.get("investigation_spec_contract_version"),
            "investigation_spec_id": spec.get("spec_id"),
            "signal_id": spec.get("signal_id"),
            "compiler_version": COMPILER_VERSION,
        },
        "signals": [
            {
                "signal_id": spec["signal_id"],
                "research_domain": spec.get("research_domain"),
                "signal_system": pm.get("signal_system") or spec.get("research_domain"),
                "primary_metric": {
                    "biomarker_id": pm.get("biomarker_id"),
                    "rationale": pm.get("rationale"),
                },
                "trigger_direction": spec.get("trigger_direction"),
                "activation": activation,
                "states": states,
                "supporting_markers": supporting_markers,
                "contradiction_markers": _collect_contradiction_markers(hypotheses),
                "missing_data": {"policies": _collect_missing_data_policies(hypotheses)},
                "confidence": {"evidence_strength": evidence.get("evidence_strength")},
                "override_rules": _map_override_rules(spec.get("override_rules") or []),
                "evidence": {
                    "evidence_strength": evidence.get("evidence_strength"),
                    "physiological_claim": evidence.get("physiological_claim"),
                    "threshold_notes": evidence.get("threshold_notes"),
                    "sources": evidence_sources,
                },
                "confirmatory_test_refs": confirmatory_refs,
            }
        ],
    }


def _compile_package_manifest(spec: dict[str, Any], package_id: str, pass3_path: str) -> dict[str, Any]:
    return {
        "package_id": package_id,
        "package_version": "1.0.0",
        "description": (
            f"KB-UTIL-2-PILOT generated package from Pass 3 spec {spec['spec_id']}. "
            "Not runtime-active."
        ),
        "research_brief": "research_brief.yaml",
        "signal_library": "signal_library.yaml",
        "promoted_signal_intelligence": "promoted_signal_intelligence.yaml",
        "author": "KB-UTIL-2-PILOT compiler",
        "created_at": "2026-06-01",
        "source_document": pass3_path,
        "source_spec_id": spec["spec_id"],
        "translation_mode": "pass3_pilot_compile",
        "behavioural_impact": "NONE",
        "pilot_status": "generated_non_runtime",
    }


def _field_audit_entry(
    field: str,
    status: str,
    target_artifact: str,
    target_path: str,
    reason: str,
) -> dict[str, str]:
    return {
        "status": status,
        "target_artifact": target_artifact,
        "target_path": target_path,
        "reason": reason,
    }


def _build_preservation_audit(spec: dict[str, Any], pass3_path: str, source_hash: str) -> dict[str, Any]:
    fields: dict[str, dict[str, str]] = {}
    fields["investigation_spec_contract_version"] = _field_audit_entry(
        "investigation_spec_contract_version",
        "preserved",
        "COMPILE_MANIFEST",
        "compile_manifest.yaml#source_contract_version",
        "Recorded in compile manifest.",
    )
    fields["spec_id"] = _field_audit_entry(
        "spec_id",
        "preserved",
        "COMPILE_MANIFEST",
        "package_manifest.yaml#source_spec_id",
        "Explicit source spec linkage.",
    )
    fields["signal_id"] = _field_audit_entry(
        "signal_id",
        "preserved",
        "PACKAGE_ACTIVATION",
        "signal_library.yaml#signals[].signal_id",
        "Exact signal_id retained.",
    )
    fields["research_domain"] = _field_audit_entry(
        "research_domain",
        "preserved",
        "PACKAGE_ACTIVATION",
        "research_brief.yaml#research_domain",
        "Copied to research_brief and PSI.",
    )
    fields["primary_marker"] = _field_audit_entry(
        "primary_marker",
        "preserved",
        "PACKAGE_ACTIVATION",
        "signal_library.yaml#signals[].primary_metric",
        "Biomarker_id and rationale in PSI primary_metric.",
    )
    fields["trigger_direction"] = _field_audit_entry(
        "trigger_direction",
        "preserved",
        "PROMOTED_SIGNAL_INTELLIGENCE",
        "promoted_signal_intelligence.yaml#signals[].trigger_direction",
        "Exact copy.",
    )
    fields["activation"] = _field_audit_entry(
        "activation",
        "preserved",
        "PACKAGE_ACTIVATION",
        "signal_library.yaml#signals[].activation_logic",
        "Activation block copied to signal_library and PSI.",
    )
    fields["states"] = _field_audit_entry(
        "states",
        "preserved",
        "PROMOTED_SIGNAL_INTELLIGENCE",
        "promoted_signal_intelligence.yaml#signals[].states",
        "Exact copy.",
    )
    fields["supporting_markers"] = _field_audit_entry(
        "supporting_markers",
        "preserved",
        "PROMOTED_SIGNAL_INTELLIGENCE",
        "promoted_signal_intelligence.yaml#signals[].supporting_markers",
        "Roles, relationship_kind, rationale preserved.",
    )
    fields["hypotheses"] = _field_audit_entry(
        "hypotheses",
        "deferred",
        "ROOT_CAUSE_FUTURE",
        "(not compiled in pilot)",
        "Ranked hypotheses deferred; contradiction_markers extracted to PSI.",
    )
    fields["hypothesis_ranking"] = _field_audit_entry(
        "hypothesis_ranking",
        "deferred",
        "ROOT_CAUSE_FUTURE",
        "(not compiled in pilot)",
        "Future hypothesis registry compile.",
    )
    fields["confirmatory_tests"] = _field_audit_entry(
        "confirmatory_tests",
        "preserved",
        "PROMOTED_SIGNAL_INTELLIGENCE",
        "promoted_signal_intelligence.yaml#signals[].confirmatory_test_refs",
        "Mapped to confirmatory_test_refs.",
    )
    fields["override_rules"] = _field_audit_entry(
        "override_rules",
        "preserved",
        "PACKAGE_ACTIVATION",
        "signal_library.yaml#signals[].override_rules",
        "Also in PSI override_rules.",
    )
    fields["evidence"] = _field_audit_entry(
        "evidence",
        "preserved",
        "PROMOTED_SIGNAL_INTELLIGENCE",
        "promoted_signal_intelligence.yaml#signals[].evidence",
        "Sources and strength in research_brief.",
    )
    fields["narrative"] = _field_audit_entry(
        "narrative",
        "partially_preserved",
        "PACKAGE_ACTIVATION",
        "signal_library.yaml#signals[].explanation",
        "Mechanism/pathway/interpretation in explanation; not duplicated in PSI per schema.",
    )
    for key in spec:
        if key not in fields:
            fields[key] = _field_audit_entry(
                key,
                "not_applicable",
                "COMPILE_MANIFEST",
                f"(source key {key})",
                "Unexpected field logged.",
            )
    return {
        "source_spec_id": spec["spec_id"],
        "source_path": pass3_path,
        "source_hash": source_hash,
        "compiler_version": COMPILER_VERSION,
        "fields": fields,
    }


def compile_pilot_package(
    package_id: str,
    spec_id: str,
    pass3_path: str,
    pass3_file: Path,
    kbp_id: str,
) -> dict[str, Any]:
    specs = _load_pass3_specs(pass3_file)
    spec = _find_spec(specs, spec_id)
    spec_bytes = json.dumps(spec, sort_keys=True, separators=(",", ":")).encode("utf-8")
    source_hash = _sha256_bytes(spec_bytes)

    out_dir = OUTPUT_ROOT / package_id
    hashes: dict[str, str] = {}
    hashes["research_brief.yaml"] = _write_yaml(out_dir / "research_brief.yaml", _compile_research_brief(spec))
    hashes["signal_library.yaml"] = _write_yaml(
        out_dir / "signal_library.yaml", _compile_signal_library(spec, kbp_id)
    )
    hashes["package_manifest.yaml"] = _write_yaml(
        out_dir / "package_manifest.yaml", _compile_package_manifest(spec, package_id, pass3_path)
    )
    hashes["promoted_signal_intelligence.yaml"] = _write_yaml(
        out_dir / "promoted_signal_intelligence.yaml",
        _compile_promoted_signal_intelligence(spec, package_id),
    )
    audit = _build_preservation_audit(spec, pass3_path, source_hash)
    hashes["source_field_preservation_audit.yaml"] = _write_yaml(
        out_dir / "source_field_preservation_audit.yaml", audit
    )

    compile_manifest = {
        "compile_id": f"kb_util2_pilot_{package_id}",
        "compiler_name": COMPILER_VERSION,
        "compiled_at_utc": f"deterministic-{source_hash[:12]}",
        "source_contract_version": spec.get("investigation_spec_contract_version"),
        "source_spec_id": spec_id,
        "source_path": pass3_path,
        "source_hash_sha256": source_hash,
        "output_root": str(out_dir.relative_to(ROOT)).replace("\\", "/"),
        "pilot_status": "generated_non_runtime",
        "runtime_active": False,
        "output_hashes_sha256": dict(sorted(hashes.items())),
    }
    hashes["compile_manifest.yaml"] = _write_yaml(out_dir / "compile_manifest.yaml", compile_manifest)

    return {
        "package_id": package_id,
        "spec_id": spec_id,
        "output_dir": str(out_dir.relative_to(ROOT)).replace("\\", "/"),
        "source_hash": source_hash,
        "output_hashes": hashes,
    }


def compile_all() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for pilot in PILOT_PACKAGES:
        pass3_file = ROOT / pilot["pass3_path"]
        results.append(
            compile_pilot_package(
                pilot["package_id"],
                pilot["spec_id"],
                pilot["pass3_path"],
                pass3_file,
                pilot["kbp_id"],
            )
        )
    return results


def write_governance_index(results: list[dict[str, Any]]) -> None:
    index_path = ROOT / "knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml"
    payload = {
        "schema_version": "1.0.0",
        "index_id": "pass3_pilot_compile_manifest_index_v1",
        "work_id": "KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot",
        "compiler_version": COMPILER_VERSION,
        "generated_utc": "2026-06-01",
        "runtime_consumed": False,
        "pilot_output_root": "knowledge_bus/generated_pilot/kb_util_2_pilot",
        "pilots": results,
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(_canonical_yaml(payload), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile Pass 3 pilot package artefacts.")
    parser.add_argument(
        "--package-id",
        action="append",
        help="Limit to package_id (default: all pilot packages).",
    )
    args = parser.parse_args(argv)
    selected = list(PILOT_PACKAGES)
    if args.package_id:
        allowed = set(args.package_id)
        selected = [p for p in PILOT_PACKAGES if p["package_id"] in allowed]
        if not selected:
            print("No matching pilot packages.", file=sys.stderr)
            return 1
    results: list[dict[str, Any]] = []
    for pilot in selected:
        pass3_file = ROOT / pilot["pass3_path"]
        results.append(
            compile_pilot_package(
                pilot["package_id"],
                pilot["spec_id"],
                pilot["pass3_path"],
                pass3_file,
                pilot["kbp_id"],
            )
        )
    write_governance_index(results)
    for row in results:
        print(f"compiled {row['package_id']} -> {row['output_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
