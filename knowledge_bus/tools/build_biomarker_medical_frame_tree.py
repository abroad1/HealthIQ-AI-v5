#!/usr/bin/env python3
"""
MED-FRAME-TREE-1 — Generate human-readable biomarker medical frame tree (non-authoritative).

Reads governed YAML only. Writes docs/architecture/biomarker_medical_frame_tree.md.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

GENERATOR_VERSION = "1.0.0"
GENERATOR_ID = "build_biomarker_medical_frame_tree"

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "docs" / "architecture" / "biomarker_medical_frame_tree.md"

SOURCE_PATHS: tuple[str, ...] = (
    "knowledge_bus/governance/medical_frame_identity_index_v1.yaml",
    "knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml",
    "knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml",
    "knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml",
    "knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml",
)


def _utc_now() -> str:
    override = os.environ.get("MED_FRAME_TREE_UTC")
    if override:
        return override
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        return "missing"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest[:16]


def _load(rel: str) -> Any:
    path = ROOT / rel
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _norm_notes(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return " ".join(text.split())


def _modifiers_by_frame(catalogue: dict[str, Any]) -> dict[str, list[str]]:
    by_frame: dict[str, list[str]] = {}
    by_family: dict[str, list[str]] = {}
    for mod in catalogue.get("modifiers") or []:
        if not isinstance(mod, dict):
            continue
        mid = mod.get("modifier_id", "")
        if not mid:
            continue
        applies = mod.get("applies_to") or {}
        for fid in applies.get("medical_frame_ids") or []:
            by_frame.setdefault(str(fid), []).append(mid)
        for sfid in applies.get("signal_family_ids") or []:
            by_family.setdefault(str(sfid), []).append(mid)
    for bucket in (by_frame, by_family):
        for key in bucket:
            bucket[key] = sorted(set(bucket[key]))
    return by_frame, by_family


def _audit_by_package(audit: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not audit:
        return out
    for row in audit.get("packages") or []:
        if isinstance(row, dict) and row.get("package_id"):
            out[str(row["package_id"])] = row
    return out


def _context_inputs_line(frame: dict[str, Any]) -> str:
    supported = frame.get("context_inputs_supported") or {}
    if not isinstance(supported, dict):
        return "none"
    enabled = sorted(k for k, v in supported.items() if v)
    return ", ".join(enabled) if enabled else "none"


def _render_frame(
    frame: dict[str, Any],
    modifiers_by_frame: dict[str, list[str]],
    modifiers_by_family: dict[str, list[str]],
    audit_by_pkg: dict[str, dict[str, Any]],
) -> list[str]:
    fid = frame.get("medical_frame_id", "")
    lines: list[str] = []
    label = frame.get("frame_label", fid)
    lines.append(f"├── **{label}**")
    lines.append(f"│   ├── Frame ID: `{fid}`")
    lines.append(f"│   ├── Frame role: `{frame.get('frame_role', '')}`")
    lines.append(f"│   ├── Signal ID: `{frame.get('signal_id', '')}`")
    lines.append(f"│   ├── Activation key: `{frame.get('activation_key', '')}`")
    lines.append(f"│   ├── Source package: `{frame.get('source_package_id', '')}`")
    lines.append(f"│   ├── Source package path: `{frame.get('source_package_path', '')}`")
    lines.append(f"│   ├── Research spec ID: `{frame.get('research_spec_id', '')}`")
    lines.append(f"│   ├── Promotion state: `{frame.get('promotion_state', '')}`")
    lines.append(f"│   ├── Runtime authority: `{frame.get('runtime_authority_status', '')}`")
    lines.append(f"│   ├── Clinical adjudication: `{frame.get('clinical_adjudication_status', '')}`")
    lines.append(f"│   ├── Collision status: `{frame.get('collision_status', '')}`")
    lines.append(f"│   ├── Context inputs supported: {_context_inputs_line(frame)}")
    pkg = frame.get("source_package_id", "")
    if pkg in audit_by_pkg:
        row = audit_by_pkg[pkg]
        lines.append(
            f"│   ├── Package promotion safety (audit): `{row.get('promotion_safety_status', '')}`"
        )
        lines.append(f"│   ├── Package frame coverage (audit): `{row.get('frame_coverage_status', '')}`")
    linked = sorted(
        set(modifiers_by_frame.get(fid, []))
        | set(modifiers_by_family.get(frame.get("signal_family_id", ""), []))
    )
    if linked:
        lines.append(f"│   ├── Linked context modifiers: {', '.join(f'`{m}`' for m in linked)}")
    else:
        lines.append("│   ├── Linked context modifiers: _none catalogued_")
    notes = _norm_notes(frame.get("notes"))
    if notes:
        lines.append(f"│   └── Notes: {notes}")
    else:
        lines.append("│   └── Notes: _none_")
    return lines


def build_markdown(
    *,
    generated_utc: str,
    index: dict[str, Any],
    catalogue: dict[str, Any],
    audit: dict[str, Any] | None,
) -> str:
    modifiers_by_frame, modifiers_by_family = _modifiers_by_frame(catalogue)
    audit_by_pkg = _audit_by_package(audit)

    families = sorted(
        (f for f in (index.get("signal_families") or []) if isinstance(f, dict)),
        key=lambda f: str(f.get("signal_family_id", "")),
    )

    lines: list[str] = [
        "# Biomarker Medical Frame Tree (Generated)",
        "",
        "> **This document is generated from governed HealthIQ architecture artefacts.**",
        "> **Do not edit this file manually.**",
        "> Update the underlying governance files and regenerate.",
        "",
        "## Generation metadata",
        "",
        f"- Generator: `{GENERATOR_ID}` v{GENERATOR_VERSION}",
        f"- Generated UTC: `{generated_utc}`",
        "- Authority: output only — **not** a source of truth",
        "- Primary authority chain: Pass_3 / investigation specs → "
        "`medical_frame_identity_index_v1.yaml` → `context_modifier_catalogue_draft_v1.yaml` "
        "→ package / promotion governance → this tree",
        "",
        "### Source artefacts",
        "",
    ]
    for rel in SOURCE_PATHS:
        lines.append(f"- `{rel}` — sha256 prefix `{_sha256(rel)}`")

    frame_count = 0
    for fam in families:
        frames = [fr for fr in (fam.get("frames") or []) if isinstance(fr, dict)]
        frame_count += len(frames)

    lines.extend(
        [
            "",
            f"- Indexed signal families: **{len(families)}**",
            f"- Indexed medical frames: **{frame_count}**",
            "",
            "## Legend — promotion / authority states",
            "",
            "| State | Meaning in tree |",
            "|-------|-----------------|",
            "| `runtime_active_canonical` | Active Pass_3 / canonical runtime authority |",
            "| `runtime_active_legacy_unadjudicated` | Legacy runtime frame preserved; medical review open |",
            "| `compiled_not_promoted` | Compiled candidate; not runtime-active |",
            "| `deferred` | Pass_3 frame indexed but not compiled/promoted |",
            "| `superseded` / `retired` | Historical; not active authority |",
            "",
            "---",
            "",
        ]
    )

    for fam in families:
        sfid = fam.get("signal_family_id", "")
        bio = fam.get("primary_biomarker_id", "")
        system = fam.get("system", "")
        lines.append(f"## {sfid} — {bio}")
        if system:
            lines.append(f"")
            lines.append(f"_System: {system}_")
        lines.append("")
        frames = sorted(
            [fr for fr in (fam.get("frames") or []) if isinstance(fr, dict)],
            key=lambda fr: str(fr.get("medical_frame_id", "")),
        )
        for frame in frames:
            lines.extend(_render_frame(frame, modifiers_by_frame, modifiers_by_family, audit_by_pkg))
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _assert_output_under_docs_architecture(output_path: Path) -> None:
    try:
        output_path.resolve().relative_to((ROOT / "docs" / "architecture").resolve())
    except ValueError as exc:
        raise ValueError("Output must be under docs/architecture/") from exc


def generate(*, output_path: Path, dry_run: bool = False) -> str:
    _assert_output_under_docs_architecture(output_path)
    generated_utc = _utc_now()
    index = _load(SOURCE_PATHS[0])
    if not index:
        raise FileNotFoundError(SOURCE_PATHS[0])
    catalogue = _load(SOURCE_PATHS[1]) or {"modifiers": []}
    audit = _load(SOURCE_PATHS[2])
    _load(SOURCE_PATHS[3])
    _load(SOURCE_PATHS[4])
    content = build_markdown(
        generated_utc=generated_utc,
        index=index,
        catalogue=catalogue,
        audit=audit,
    )
    if not dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8", newline="\n")
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate biomarker medical frame tree Markdown.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output Markdown path (must be under docs/architecture/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Build but do not write file")
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        _assert_output_under_docs_architecture(output)
    except ValueError:
        print("Output must be under docs/architecture/", file=sys.stderr)
        return 2
    generate(output_path=output, dry_run=args.dry_run)
    print(f"biomarker_medical_frame_tree: written {output.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
