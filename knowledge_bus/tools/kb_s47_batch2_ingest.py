#!/usr/bin/env python3
"""
KB-S47 / KB-S47a / KB-S47b Batch 2 — deterministic package generation from Batch_2_Pass_3_Rev1.json.

Emits one KB package per investigation object when primary + supporting biomarkers exist
in SSOT after governed ID alignment (total_testosterone→testosterone only).
`dhea` and `dhea_s` are distinct canonical IDs; lab alias ``DHEA-S`` must resolve to
``dhea_s`` via biomarker_alias_registry.yaml, not to ``dhea`` (KB-S47b).

Does not modify backend/ssot or backend/core at runtime; imports translator read-only.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.knowledge.investigation_spec_to_promoted_signal import (  # noqa: E402
    translate_investigation_spec_v3_to_promoted_signals,
)

BATCH_PATH = (
    ROOT
    / "knowledge_bus"
    / "research"
    / "investigation_specs"
    / "multi_llm_research"
    / "Batch_2_Pass_3_Rev1.json"
)
SSOT_PATH = ROOT / "backend" / "ssot" / "biomarkers.yaml"

# Deterministic naming alignment (SSOT canonical id for total testosterone).
BIOMARKER_ID_ALIGN = {
    "total_testosterone": "testosterone",
}


def _load_ssot_keys() -> set[str]:
    reg = yaml.safe_load(SSOT_PATH.read_text(encoding="utf-8"))
    return set((reg.get("biomarkers") or {}).keys())


def _aligned_id(bid: str) -> str:
    return BIOMARKER_ID_ALIGN.get(bid, bid)


def spec_ssot_ok(inv: dict, ssot: set[str]) -> tuple[bool, str]:
    primary = inv["primary_marker"]["biomarker_id"]
    if _aligned_id(primary) not in ssot:
        return False, f"primary {primary!r}"
    seen: set[str] = set()
    for sm in inv.get("supporting_markers") or []:
        raw = sm["biomarker_id"]
        aid = _aligned_id(raw)
        if aid not in ssot:
            return False, f"supporting {raw!r}"
        if aid == _aligned_id(primary):
            return False, f"supporting {raw!r} aligns to primary {primary!r} (duplicate metric)"
        if aid in seen:
            return False, f"duplicate supporting metric {aid!r}"
        seen.add(aid)
    return True, ""


def normalize_inv_biomarker_ids(inv: dict) -> dict:
    out = copy.deepcopy(inv)

    def rep(x: str) -> str:
        return BIOMARKER_ID_ALIGN.get(x, x)

    out["primary_marker"]["biomarker_id"] = rep(out["primary_marker"]["biomarker_id"])
    for sm in out.get("supporting_markers") or []:
        sm["biomarker_id"] = rep(sm["biomarker_id"])
    for hyp in out.get("hypotheses") or []:
        refs = hyp.get("supporting_marker_refs")
        if isinstance(refs, list):
            hyp["supporting_marker_refs"] = [rep(str(r)) for r in refs]
        for cm in hyp.get("contradiction_markers") or []:
            if "marker_reference" in cm and isinstance(cm["marker_reference"], str):
                cm["marker_reference"] = rep(cm["marker_reference"])
    for rule in out.get("override_rules") or []:
        for cond in rule.get("conditions") or []:
            if "metric_id" in cond and isinstance(cond["metric_id"], str):
                cond["metric_id"] = rep(cond["metric_id"])
    return out


def package_dir_name(spec_id: str) -> str:
    return "pkg_kb47_" + spec_id.removeprefix("inv_")


def signal_display_name(signal_id: str) -> str:
    body = signal_id.removeprefix("signal_").replace("_", " ")
    return body.title()


def map_trigger_for_library(td: str) -> str:
    if td == "both":
        return "bidirectional"
    if td in ("high", "low"):
        return td
    return "context_dependent"


def map_expected_direction(ed: str) -> str:
    if ed == "either":
        return "any"
    if ed in ("high", "low", "any"):
        return ed
    return "any"


def build_research_brief(inv: dict) -> dict:
    ev = inv["evidence"]
    sources = copy.deepcopy(ev.get("sources") or [])
    primary = inv["primary_marker"]["biomarker_id"]
    bio = {primary}
    for sm in inv.get("supporting_markers") or []:
        bio.add(sm["biomarker_id"])
    rs = ev.get("threshold_notes") or ""
    if not isinstance(rs, str) or not rs.strip():
        nar = inv.get("narrative") or {}
        rs = (nar.get("interpretation") or nar.get("implications") or "").strip()
    return {
        "research_domain": inv["research_domain"],
        "sources": sources,
        "biomarkers": sorted(bio),
        "derived_metrics": [],
        "physiological_claim": ev["physiological_claim"],
        "evidence_strength": ev["evidence_strength"],
        "research_summary": rs.strip() if isinstance(rs, str) else str(rs),
    }


def build_signal_library(inv: dict, *, kbp_id: str, pkg_id: str) -> dict:
    lib = inv["primary_marker"]
    primary_metric = lib["biomarker_id"]
    signal_id = inv["signal_id"]
    nar = inv.get("narrative") or {}
    supporting_yaml: list[dict] = []
    for sm in inv.get("supporting_markers") or []:
        supporting_yaml.append(
            {
                "biomarker_id": sm["biomarker_id"],
                "expected_direction": map_expected_direction(sm["expected_direction"]),
                "role": sm["role"],
                "availability": sm["availability"],
                "rationale": sm["rationale"],
            }
        )
    deps = [primary_metric] + [x["biomarker_id"] for x in supporting_yaml]
    threshold_slug = signal_id.replace("signal_", "")
    return {
        "library": {
            "package_id": kbp_id,
            "schema_version": "2.0.0",
            "package_version": "1.0.0",
            "library_name": f"KB-S47 {signal_display_name(signal_id)} signal library",
            "description": f"Translated from {inv['spec_id']} (Batch_2_Pass_3_Rev1.json).",
        },
        "signals": [
            {
                "signal_id": signal_id,
                "name": signal_display_name(signal_id),
                "description": lib["rationale"].strip(),
                "system": lib["signal_system"],
                "primary_metric": primary_metric,
                "trigger_direction": map_trigger_for_library(inv["trigger_direction"]),
                "supporting_metrics": supporting_yaml,
                "dependencies": {
                    "biomarkers": deps,
                    "derived_metrics": [],
                    "signals": [],
                },
                "optional_dependencies": {
                    "biomarkers": [],
                    "derived_metrics": [],
                    "signals": [],
                },
                "thresholds": [
                    {
                        "threshold_id": f"{threshold_slug}_lab_range_activation_placeholder",
                        "metric_id": primary_metric,
                        "operator": ">=",
                        "value": 9999.0,
                        "severity": "at_risk",
                        "description": "Validator placeholder; runtime activation uses lab_range_exceeded.",
                    }
                ],
                "activation_logic": "lab_range_exceeded",
                "activation_config": {
                    "upper_bound_state": "suboptimal",
                    "enable_lower_bound": False,
                    "lower_bound_state": "suboptimal",
                },
                "override_rules": copy.deepcopy(inv.get("override_rules") or []),
                "output": {
                    "signal_value": primary_metric,
                    "signal_state": "at_risk",
                    "confidence": "confidence_model_v1",
                    "primary_metric": primary_metric,
                    "supporting_markers": [x["biomarker_id"] for x in supporting_yaml],
                },
                "explanation": {
                    "mechanism": nar.get("mechanism", ""),
                    "biological_pathway": nar.get("biological_pathway", ""),
                    "interpretation": nar.get("interpretation", ""),
                    "implications": nar.get("implications", ""),
                    "supporting_marker_roles": nar.get("supporting_marker_roles", ""),
                },
            }
        ],
    }


def build_manifest(
    *,
    pkg_id: str,
    description: str,
    source_rel: str,
) -> dict:
    return {
        "package_id": pkg_id,
        "package_version": "1.0.0",
        "description": description.strip(),
        "research_brief": "research_brief.yaml",
        "signal_library": "signal_library.yaml",
        "promoted_signal_intelligence": "promoted_signal_intelligence.yaml",
        "author": "HealthIQ Knowledge Bus — KB-S47",
        "created_at": "2026-03-28",
        "source_document": source_rel,
        "translation_mode": "creation",
        "behavioural_impact": "NONE",
    }


def main() -> int:
    ssot = _load_ssot_keys()
    data = json.loads(BATCH_PATH.read_text(encoding="utf-8"))
    source_rel = "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3_Rev1.json"

    candidates: list[tuple[dict, str]] = []
    for inv in data:
        ok, reason = spec_ssot_ok(inv, ssot)
        if not ok:
            print(f"SKIP {inv.get('spec_id')}: {reason}")
            continue
        candidates.append((inv, reason))

    candidates.sort(key=lambda x: x[0]["spec_id"])
    kbp_base = 4700

    for i, (inv, _) in enumerate(candidates):
        norm = normalize_inv_biomarker_ids(inv)
        pkg_id = package_dir_name(inv["spec_id"])
        kbp_id = f"KBP-{kbp_base + i:04d}"
        out_dir = ROOT / "knowledge_bus" / "packages" / pkg_id
        out_dir.mkdir(parents=True, exist_ok=True)

        brief = build_research_brief(norm)
        sig_lib = build_signal_library(norm, kbp_id=kbp_id, pkg_id=pkg_id)
        promoted = translate_investigation_spec_v3_to_promoted_signals(
            norm, package_id=pkg_id
        )
        desc = (
            f"KB-S47 Batch 2 package for {inv['spec_id']} "
            f"({norm['signal_id']}). Biomarker IDs aligned to SSOT where governed."
        )
        manifest = build_manifest(
            pkg_id=pkg_id,
            description=desc,
            source_rel=source_rel,
        )

        yaml_kw = {"default_flow_style": False, "allow_unicode": True, "sort_keys": False}
        (out_dir / "research_brief.yaml").write_text(
            yaml.dump(brief, **yaml_kw), encoding="utf-8"
        )
        (out_dir / "signal_library.yaml").write_text(
            yaml.dump(sig_lib, **yaml_kw), encoding="utf-8"
        )
        (out_dir / "package_manifest.yaml").write_text(
            yaml.dump(manifest, **yaml_kw), encoding="utf-8"
        )
        (out_dir / "promoted_signal_intelligence.yaml").write_text(
            yaml.dump(promoted, **yaml_kw), encoding="utf-8"
        )
        print(f"WROTE {pkg_id} ({kbp_id})")

    print(f"Done. Packages written: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
