"""
Generate a deterministic AB panel delta report (read-only audit).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def get_biomarker_map(doc: Any, source: Path) -> dict[str, dict[str, Any]]:
    if not isinstance(doc, dict):
        raise ValueError(f"{source} must be a mapping.")
    biomarkers = doc.get("biomarkers")
    if not isinstance(biomarkers, dict):
        raise ValueError(f"{source} must contain top-level 'biomarkers' mapping.")
    normalized: dict[str, dict[str, Any]] = {}
    for canonical_id, definition in biomarkers.items():
        if isinstance(canonical_id, str) and isinstance(definition, dict):
            normalized[canonical_id] = definition
    return normalized


def parse_prod_aliases(doc: Any) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    if not isinstance(doc, dict):
        return parsed
    for _, entry in sorted(doc.items()):
        if not isinstance(entry, dict):
            continue
        canonical_id = entry.get("canonical_id")
        aliases = entry.get("aliases")
        if not isinstance(canonical_id, str) or not isinstance(aliases, list):
            continue
        clean_aliases = [alias for alias in aliases if isinstance(alias, str)]
        if canonical_id not in parsed:
            parsed[canonical_id] = []
        parsed[canonical_id].extend(clean_aliases)
    for canonical_id in list(parsed.keys()):
        parsed[canonical_id] = sorted(set(parsed[canonical_id]))
    return parsed


def parse_ab_aliases(doc: Any) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    if not isinstance(doc, dict):
        return parsed
    entries = doc.get("ab_full_panel", [])
    if not isinstance(entries, list):
        return parsed
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        canonical_id = entry.get("canonical_id")
        aliases = entry.get("aliases")
        if not isinstance(canonical_id, str) or not isinstance(aliases, list):
            continue
        clean_aliases = [alias for alias in aliases if isinstance(alias, str)]
        if canonical_id not in parsed:
            parsed[canonical_id] = []
        parsed[canonical_id].extend(clean_aliases)
    for canonical_id in list(parsed.keys()):
        parsed[canonical_id] = sorted(set(parsed[canonical_id]))
    return parsed


def total_raw_labels(alias_map: dict[str, list[str]]) -> int:
    return sum(len(aliases) for aliases in alias_map.values())


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    ssot_dir = repo_root / "backend" / "ssot"
    staging_dir = ssot_dir / "_ab_panel_staging"
    report_path = repo_root / "backend" / "reports" / "ab_panel_delta_report.md"

    files = {
        "prod_biomarkers": ssot_dir / "biomarkers.yaml",
        "prod_burden": ssot_dir / "system_burden_registry.yaml",
        "prod_alias": ssot_dir / "biomarker_alias_registry.yaml",
        "ab_biomarkers": staging_dir / "ab_panel_biomarkers.yaml",
        "ab_burden": staging_dir / "ab_panel_system_burden_registry.yaml",
        "ab_alias": staging_dir / "ab_panel_alias_registry.yaml",
    }

    try:
        loaded = {key: load_yaml(path) for key, path in files.items()}
        prod_biomarkers = get_biomarker_map(loaded["prod_biomarkers"], files["prod_biomarkers"])
        prod_burden = get_biomarker_map(loaded["prod_burden"], files["prod_burden"])
        ab_biomarkers = get_biomarker_map(loaded["ab_biomarkers"], files["ab_biomarkers"])
        ab_burden = get_biomarker_map(loaded["ab_burden"], files["ab_burden"])
        prod_alias = parse_prod_aliases(loaded["prod_alias"])
        ab_alias = parse_ab_aliases(loaded["ab_alias"])
    except Exception as exc:
        print(f"[FAIL] Unable to load/parse required files: {exc}", file=sys.stderr)
        return 1

    prod_biomarker_ids = set(prod_biomarkers.keys())
    ab_biomarker_ids = set(ab_biomarkers.keys())
    new_in_ab = sorted(ab_biomarker_ids - prod_biomarker_ids)
    missing_from_ab = sorted(prod_biomarker_ids - ab_biomarker_ids)

    prod_raw_labels = sorted({label for labels in prod_alias.values() for label in labels})
    prod_raw_label_set = set(prod_raw_labels)

    ab_label_to_canonicals: dict[str, set[str]] = {}
    for canonical_id, labels in sorted(ab_alias.items()):
        for label in labels:
            ab_label_to_canonicals.setdefault(label, set()).add(canonical_id)

    ab_only_labels = sorted(label for label in ab_label_to_canonicals if label not in prod_raw_label_set)

    missing_burden_for_new = sorted(canonical_id for canonical_id in new_in_ab if canonical_id not in ab_burden)
    missing_alias_for_new = []
    for canonical_id in new_in_ab:
        has_ab_aliases = len(ab_alias.get(canonical_id, [])) > 0
        has_prod_aliases = len(prod_alias.get(canonical_id, [])) > 0
        if not has_ab_aliases and not has_prod_aliases:
            missing_alias_for_new.append(canonical_id)
    missing_alias_for_new = sorted(missing_alias_for_new)

    lines: list[str] = []
    lines.append("# AB Panel Delta Report")
    lines.append("")
    lines.append("## 1) Counts Summary (Prod vs AB)")
    lines.append("")
    lines.append("| Metric | Production | AB Staging |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Biomarker count | {len(prod_biomarkers)} | {len(ab_biomarkers)} |")
    lines.append(f"| Burden entry count | {len(prod_burden)} | {len(ab_burden)} |")
    lines.append(f"| Alias entry count | {len(prod_alias)} | {len(ab_alias)} |")
    lines.append(f"| Raw labels count (sum aliases) | {total_raw_labels(prod_alias)} | {total_raw_labels(ab_alias)} |")
    lines.append("")

    lines.append("## 2) Canonical ID Set Deltas")
    lines.append("")
    lines.append(f"- **NEW_IN_AB** ({len(new_in_ab)}):")
    for canonical_id in new_in_ab:
        lines.append(f"  - `{canonical_id}`")
    lines.append(f"- **MISSING_FROM_AB** ({len(missing_from_ab)}), informational:")
    for canonical_id in missing_from_ab:
        lines.append(f"  - `{canonical_id}`")
    lines.append("")

    lines.append("## 3) NEW_IN_AB Canonical Details")
    lines.append("")
    if not new_in_ab:
        lines.append("- None")
    else:
        for canonical_id in new_in_ab:
            biomarker = ab_biomarkers.get(canonical_id, {})
            burden = ab_burden.get(canonical_id, {})
            alias_count = len(ab_alias.get(canonical_id, []))
            lines.append(f"- `{canonical_id}`")
            lines.append(f"  - system: `{biomarker.get('system', 'N/A')}`")
            lines.append(f"  - unit: `{biomarker.get('unit', 'N/A')}`")
            lines.append(f"  - category: `{biomarker.get('category', 'N/A')}`")
            lines.append(f"  - clinical_weight: `{biomarker.get('clinical_weight', 'N/A')}`")
            lines.append(f"  - AB aliases: `{alias_count}`")
            lines.append(
                "  - burden: "
                f"risk_direction=`{burden.get('risk_direction', 'MISSING')}`, "
                f"weight=`{burden.get('weight', 'MISSING')}`"
            )
    lines.append("")

    lines.append("## 4) Alias Deltas (AB-only Raw Labels)")
    lines.append("")
    lines.append(f"- AB-only raw labels not present in production alias registry: **{len(ab_only_labels)}**")
    for label in ab_only_labels:
        mapped = sorted(ab_label_to_canonicals[label])
        mapped_str = ", ".join(f"`{canonical}`" for canonical in mapped)
        lines.append(f"  - `{label}` -> {mapped_str}")
    lines.append("")

    lines.append("## 5) Sanity Checks")
    lines.append("")
    if missing_burden_for_new:
        lines.append("- [FAIL] NEW_IN_AB without AB burden entries:")
        for canonical_id in missing_burden_for_new:
            lines.append(f"  - `{canonical_id}`")
    else:
        lines.append("- [PASS] All NEW_IN_AB canonicals have AB burden entries.")

    if missing_alias_for_new:
        lines.append("- [FAIL] NEW_IN_AB without alias coverage (AB or production):")
        for canonical_id in missing_alias_for_new:
            lines.append(f"  - `{canonical_id}`")
    else:
        lines.append("- [PASS] All NEW_IN_AB canonicals have alias coverage.")
    lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
