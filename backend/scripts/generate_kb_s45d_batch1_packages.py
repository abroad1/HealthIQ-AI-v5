#!/usr/bin/env python3
"""
Generate KB-S45d individual pkg_kb45_* packages from investigation-spec JSON + batch-1 signal library.

Run from repo root: python backend/scripts/generate_kb_s45d_batch1_packages.py
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "knowledge_bus/research/investigation_specs/investigation-spec-collection-batch1-10.json"
BATCH_LIB_PATH = ROOT / (
    "knowledge_bus/research/investigation_specs/investigation-batch1-signal-library-reference.yaml"
)

PACKAGES: list[dict[str, str]] = [
    {
        "signal_id": "signal_active_b12_deficiency",
        "dir": "pkg_kb45_active_b12_low_deficiency",
        "kbp": "KBP-2500",
        "library_name": "KB-S45d Active B12 Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: active B12 low (inv_active_b12_low, batch-1).",
    },
    {
        "signal_id": "signal_apoa1_cardio_risk",
        "dir": "pkg_kb45_apoa1_low_cardio_risk",
        "kbp": "KBP-2501",
        "library_name": "KB-S45d ApoA1 Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: ApoA1 low cardio risk (inv_apoa1_low, batch-1).",
    },
    {
        "signal_id": "signal_apob_atherogenic",
        "dir": "pkg_kb45_apob_high_atherogenic",
        "kbp": "KBP-2502",
        "library_name": "KB-S45d ApoB Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: ApoB high atherogenic (inv_apob_high, batch-1).",
    },
    {
        "signal_id": "signal_lipid_imbalance",
        "dir": "pkg_kb45_apob_apoa1_ratio_high_imbalance",
        "kbp": "KBP-2503",
        "library_name": "KB-S45d ApoB/ApoA1 Ratio Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: ApoB/ApoA1 ratio imbalance (inv_apob_apoa1_ratio_high, batch-1).",
    },
    {
        "signal_id": "signal_basophilia_pct",
        "dir": "pkg_kb45_basophil_pct_high_basophilia",
        "kbp": "KBP-2504",
        "library_name": "KB-S45d Basophil Percentage Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: basophil percentage high (inv_basophil_pct_high, batch-1).",
    },
    {
        "signal_id": "signal_basophilia_abs",
        "dir": "pkg_kb45_basophils_abs_high_basophilia",
        "kbp": "KBP-2505",
        "library_name": "KB-S45d Absolute Basophilia Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: absolute basophils high (inv_basophils_abs_high, batch-1).",
    },
    {
        "signal_id": "signal_hyperbilirubinemia",
        "dir": "pkg_kb45_bilirubin_high_hyperbilirubinemia",
        "kbp": "KBP-2506",
        "library_name": "KB-S45d Bilirubin Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: bilirubin high / hyperbilirubinemia (inv_bilirubin_high, batch-1).",
    },
    {
        "signal_id": "signal_hyperchloremia",
        "dir": "pkg_kb45_chloride_high_hyperchloremia",
        "kbp": "KBP-2507",
        "library_name": "KB-S45d Chloride Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: chloride high / hyperchloremia (inv_chloride_high, batch-1).",
    },
    {
        "signal_id": "signal_hypercalcemia",
        "dir": "pkg_kb45_corrected_calcium_high_hypercalcemia",
        "kbp": "KBP-2508",
        "library_name": "KB-S45d Corrected Calcium Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: corrected calcium high / hypercalcemia (inv_corrected_calcium_high, batch-1).",
    },
    {
        "signal_id": "signal_hypercortisolism",
        "dir": "pkg_kb45_cortisol_high_hypercortisolism",
        "kbp": "KBP-2509",
        "library_name": "KB-S45d Cortisol Investigation Signal Library",
        "manifest_desc": "KB-S45d regenerated package: cortisol high / hypercortisolism (inv_cortisol_high, batch-1).",
    },
]


def _spec_by_signal_id(specs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(s["signal_id"]): s for s in specs if isinstance(s, dict)}


def _batch_signal_by_id(batch: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for s in batch.get("signals", []):
        if isinstance(s, dict) and s.get("signal_id"):
            out[str(s["signal_id"])] = s
    return out


def _build_structured_supporting(spec: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sm in spec.get("supporting_markers", []):
        if not isinstance(sm, dict):
            continue
        rows.append(
            {
                "biomarker_id": sm["biomarker_id"],
                "expected_direction": sm["expected_direction"],
                "role": sm["role"],
                "availability": sm["availability"],
                "rationale": str(sm["rationale"]).strip(),
            }
        )
    return rows


def _merge_override_rules(batch_sig: dict[str, Any], spec: dict[str, Any]) -> list[dict[str, Any]]:
    brules = batch_sig.get("override_rules") or []
    jrules = spec.get("override_rules") or []
    merged: list[dict[str, Any]] = []
    for i, br in enumerate(brules):
        rule = copy.deepcopy(br)
        if i < len(jrules) and isinstance(jrules[i], dict):
            rule["source_refs"] = list(jrules[i].get("source_refs") or [])
        merged.append(rule)
    return merged


def _build_signal(batch_sig: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    sm_struct = _build_structured_supporting(spec)
    sup_ids = [str(x["biomarker_id"]) for x in sm_struct]
    out_block = copy.deepcopy(batch_sig.get("output") or {})
    out_block["supporting_markers"] = sup_ids

    return {
        "signal_id": batch_sig["signal_id"],
        "name": batch_sig["name"],
        "description": batch_sig["description"],
        "system": batch_sig["system"],
        "primary_metric": batch_sig["primary_metric"],
        "trigger_direction": spec["trigger_direction"],
        "supporting_metrics": sm_struct,
        "dependencies": copy.deepcopy(batch_sig.get("dependencies") or {}),
        "optional_dependencies": copy.deepcopy(batch_sig.get("optional_dependencies") or {}),
        "thresholds": copy.deepcopy(batch_sig.get("thresholds") or []),
        "activation_logic": batch_sig["activation_logic"],
        "activation_config": copy.deepcopy(batch_sig.get("activation_config") or {}),
        "override_rules": _merge_override_rules(batch_sig, spec),
        "output": out_block,
        "explanation": copy.deepcopy(batch_sig.get("explanation") or {}),
    }


def _build_research_brief(spec: dict[str, Any], batch_sig: dict[str, Any]) -> dict[str, Any]:
    ev = spec["evidence"]
    deps = batch_sig.get("dependencies") or {}
    biomarkers = [str(x) for x in (deps.get("biomarkers") or []) if isinstance(x, str)]
    derived = [str(x) for x in (deps.get("derived_metrics") or []) if isinstance(x, str)]
    sources_out: list[dict[str, Any]] = []
    for src in ev.get("sources", []):
        if not isinstance(src, dict):
            continue
        entry: dict[str, Any] = {
            "source_id": src["source_id"],
            "paper_title": src["paper_title"],
            "journal": src["journal"],
            "year": int(src["year"]) if isinstance(src["year"], (int, float)) and not isinstance(src["year"], bool) else src["year"],
        }
        sources_out.append(entry)

    brief: dict[str, Any] = {
        "research_domain": spec["research_domain"],
        "sources": sources_out,
        "biomarkers": sorted(set(biomarkers)),
        "physiological_claim": str(ev["physiological_claim"]).strip(),
        "evidence_strength": ev["evidence_strength"],
        "research_summary": str(ev["threshold_notes"]).strip(),
    }
    if derived:
        brief["derived_metrics"] = sorted(set(derived))
    return brief


def _build_library_yaml(
    meta: dict[str, str],
    signal: dict[str, Any],
) -> str:
    payload = {
        "library": {
            "package_id": meta["kbp"],
            "schema_version": "2.0.0",
            "package_version": "1.0.0",
            "library_name": meta["library_name"],
            "description": (
                f"Regenerated from investigation-spec-collection-batch1-10.json. "
                f"{meta['manifest_desc']}"
            ),
        },
        "signals": [signal],
    }
    return yaml.dump(
        payload,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )


def _build_manifest(meta: dict[str, str]) -> str:
    lines = [
        f"package_id: {meta['dir']}",
        "package_version: 1.0.0",
        "description: >",
        f"  {meta['manifest_desc']}",
        "research_brief: research_brief.yaml",
        "signal_library: signal_library.yaml",
        "author: HealthIQ Knowledge Bus — KB-S45d",
        'created_at: "2026-03-21"',
        "source_document: knowledge_bus/research/investigation_specs/investigation-spec-collection-batch1-10.json",
        "translation_mode: regeneration",
        "behavioural_impact: NONE",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    specs_raw = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(specs_raw, list):
        raise SystemExit("JSON must be a list")
    by_spec = _spec_by_signal_id(specs_raw)

    batch = yaml.safe_load(BATCH_LIB_PATH.read_text(encoding="utf-8"))
    if not isinstance(batch, dict):
        raise SystemExit("batch signal_library invalid")
    by_batch = _batch_signal_by_id(batch)

    for meta in PACKAGES:
        sid = meta["signal_id"]
        spec = by_spec.get(sid)
        bsig = by_batch.get(sid)
        if spec is None or bsig is None:
            raise SystemExit(f"missing spec or batch signal for {sid}")

        signal = _build_signal(bsig, spec)
        brief = _build_research_brief(spec, bsig)

        pkg_dir = ROOT / "knowledge_bus" / "packages" / meta["dir"]
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "signal_library.yaml").write_text(_build_library_yaml(meta, signal), encoding="utf-8")
        (pkg_dir / "research_brief.yaml").write_text(
            yaml.dump(brief, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        (pkg_dir / "package_manifest.yaml").write_text(_build_manifest(meta), encoding="utf-8")
        print(f"Wrote {pkg_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
