"""
Validate AB panel staging files against Sprint 17 SSOT governance rules.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml


CHECKS_IN_ORDER = [
    "CHECK 0 — AB Full Panel Completeness",
    "CHECK 1 — System Allowlist Enforcement",
    "CHECK 2 — Canonical Naming Standards",
    "CHECK 3 — Duplicate Canonical ID Drift",
    "CHECK 4 — Burden Registry Coverage",
    "CHECK 5 — Risk Direction Validity",
    "CHECK 6 — Alias Collision Detection",
    "CHECK 7 — Derived Marker Separation",
]

ALLOWED_SYSTEMS = {
    "metabolic",
    "cardiovascular",
    "hepatic",
    "renal",
    "immune",
    "hematological",
    "hormonal",
    "nutritional",
    "thyroid",
}

ALLOWED_RISK_DIRECTIONS = {"HIGH_IS_RISK", "LOW_IS_RISK", "BOTH_SIDES_RISK"}

CANONICAL_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# UK -> US normalization for alternate-spelling drift checks.
UK_US_TOKENS = [
    ("haemoglobin", "hemoglobin"),
    ("haematocrit", "hematocrit"),
    ("haemochromatosis", "hemochromatosis"),
    ("haemolysis", "hemolysis"),
    ("oestradiol", "estradiol"),
    ("glycaemic", "glycemic"),
    ("anaemia", "anemia"),
    ("leukaemia", "leukemia"),
]


class ValidationReport:
    def __init__(self) -> None:
        self.failures: dict[str, list[str]] = {check: [] for check in CHECKS_IN_ORDER}
        self.notes: dict[str, list[str]] = {check: [] for check in CHECKS_IN_ORDER}
        self.counts: dict[str, int] = {}

    def fail(self, check: str, message: str) -> None:
        self.failures[check].append(message)

    def note(self, check: str, message: str) -> None:
        self.notes[check].append(message)

    def has_failures(self) -> bool:
        return any(self.failures[check] for check in CHECKS_IN_ORDER)

    def print(self) -> None:
        print("=" * 78)
        print("AB PANEL SSOT VALIDATION REPORT")
        print("=" * 78)
        if self.counts:
            print(
                "COUNTS: "
                f"n_ab_biomarkers={self.counts.get('n_ab_biomarkers', 0)}, "
                f"n_ab_burden_entries={self.counts.get('n_ab_burden_entries', 0)}, "
                f"n_ab_aliases={self.counts.get('n_ab_aliases', 0)}, "
                f"n_raw_labels_resolvable={self.counts.get('n_raw_labels_resolvable', 0)}"
            )
        for check in CHECKS_IN_ORDER:
            status = "FAIL" if self.failures[check] else "PASS"
            print(f"\n{check}: {status}")
            for message in sorted(self.notes[check]):
                print(f"  [NOTE] {message}")
            for message in sorted(self.failures[check]):
                print(f"  [FAIL] {message}")

        final_status = "FAIL" if self.has_failures() else "PASS"
        print("\n" + "=" * 78)
        print(f"OVERALL: {final_status}")
        print("=" * 78)


def load_yaml_or_fail(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def get_biomarkers_map(document: Any, path: Path) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ValueError(f"{path} must load as a mapping.")
    biomarkers = document.get("biomarkers")
    if not isinstance(biomarkers, dict):
        raise ValueError(f"{path} must contain a top-level 'biomarkers' mapping.")
    return biomarkers


def normalize_alias(alias: str) -> str:
    return " ".join(alias.strip().split()).lower()


def fold_canonical_for_spelling(name: str) -> str:
    folded = name.lower()
    for uk, us in UK_US_TOKENS:
        folded = folded.replace(uk, us)
    folded = folded.replace("_", "")
    return re.sub(r"[^a-z0-9]", "", folded)


def uk_us_duplicate_variant(name: str) -> str | None:
    lowered = name.lower()
    for uk, us in UK_US_TOKENS:
        if uk in lowered:
            return lowered.replace(uk, us)
    return None


def canonical_has_derived_pattern(canonical_id: str) -> bool:
    return "_ratio" in canonical_id or "ratio" in canonical_id or "non_hdl" in canonical_id


def main() -> int:
    report = ValidationReport()
    backend_dir = Path(__file__).resolve().parents[1]
    ssot_dir = backend_dir / "ssot"
    staging_dir = ssot_dir / "_ab_panel_staging"

    required_files = {
        "prod_biomarkers": ssot_dir / "biomarkers.yaml",
        "prod_alias": ssot_dir / "biomarker_alias_registry.yaml",
        "prod_burden": ssot_dir / "system_burden_registry.yaml",
        "ab_biomarkers": staging_dir / "ab_panel_biomarkers.yaml",
        "ab_alias": staging_dir / "ab_panel_alias_registry.yaml",
        "ab_burden": staging_dir / "ab_panel_system_burden_registry.yaml",
    }

    optional_files = {
        "ranges": ssot_dir / "ranges.yaml",
        "scoring_policy": ssot_dir / "scoring_policy.yaml",
    }

    loaded: dict[str, Any] = {}
    try:
        for key, path in required_files.items():
            loaded[key] = load_yaml_or_fail(path)
    except Exception as exc:  # pragma: no cover - deterministic hard-stop path
        print("AB PANEL SSOT VALIDATION REPORT")
        print("[FAIL] Unable to load required SSOT file.")
        print(f"[FAIL] {exc}")
        return 1

    # Optional registries used only for CHECK 7.
    optional_loaded: dict[str, Any] = {}
    for key, path in optional_files.items():
        if path.exists():
            try:
                optional_loaded[key] = load_yaml_or_fail(path)
            except Exception:
                optional_loaded[key] = None

    try:
        prod_biomarkers = get_biomarkers_map(loaded["prod_biomarkers"], required_files["prod_biomarkers"])
        ab_biomarkers = get_biomarkers_map(loaded["ab_biomarkers"], required_files["ab_biomarkers"])
        prod_burden = get_biomarkers_map(loaded["prod_burden"], required_files["prod_burden"])
        ab_burden = get_biomarkers_map(loaded["ab_burden"], required_files["ab_burden"])
    except Exception as exc:
        print("AB PANEL SSOT VALIDATION REPORT")
        print("[FAIL] Invalid SSOT structure.")
        print(f"[FAIL] {exc}")
        return 1

    check0 = CHECKS_IN_ORDER[0]
    ab_alias_doc = loaded["ab_alias"] if isinstance(loaded["ab_alias"], dict) else {}
    ab_alias_entries = ab_alias_doc.get("ab_full_panel", [])
    if not isinstance(ab_alias_entries, list):
        report.fail(check0, "AB alias registry must contain list at key 'ab_full_panel'.")
        ab_alias_entries = []

    if not ab_alias_entries:
        report.fail(check0, "AB alias registry cannot be empty; ab_full_panel must contain entries.")

    explicit_expected_ids = ab_alias_doc.get("expected_canonical_ids", [])
    expected_canonical_ids: set[str] = set()
    if isinstance(explicit_expected_ids, list):
        expected_canonical_ids = {item for item in explicit_expected_ids if isinstance(item, str)}
    if not expected_canonical_ids:
        expected_canonical_ids = {
            entry.get("canonical_id")
            for entry in ab_alias_entries
            if isinstance(entry, dict) and isinstance(entry.get("canonical_id"), str)
        }
    expected_canonical_ids.discard(None)
    if not expected_canonical_ids:
        report.fail(
            check0,
            "Unable to derive expected AB canonical IDs from alias registry (empty spec list).",
        )
    elif len(ab_biomarkers) < len(expected_canonical_ids):
        report.fail(
            check0,
            f"AB biomarkers appear to be a subset: {len(ab_biomarkers)} biomarkers < "
            f"expected minimum {len(expected_canonical_ids)} from AB alias spec.",
        )

    check1 = CHECKS_IN_ORDER[1]
    for canonical_id, definition in sorted(ab_biomarkers.items()):
        system = definition.get("system") if isinstance(definition, dict) else None
        if system not in ALLOWED_SYSTEMS:
            report.fail(
                check1,
                f"AB biomarker '{canonical_id}' uses non-allowlisted system '{system}'.",
            )
    for canonical_id, definition in sorted(ab_burden.items()):
        system = definition.get("system") if isinstance(definition, dict) else None
        if system not in ALLOWED_SYSTEMS:
            report.fail(
                check1,
                f"AB burden entry '{canonical_id}' uses non-allowlisted system '{system}'.",
            )

    check2 = CHECKS_IN_ORDER[2]

    ab_ids_from_alias = []
    for entry in ab_alias_entries:
        if not isinstance(entry, dict):
            continue
        canonical_id = entry.get("canonical_id")
        if isinstance(canonical_id, str):
            ab_ids_from_alias.append(canonical_id)

    prod_canonical_ids = set(prod_biomarkers.keys())
    ab_all_canonical_ids = set(ab_biomarkers.keys()) | set(ab_burden.keys()) | set(ab_ids_from_alias)
    all_known_canonical_ids = prod_canonical_ids | ab_all_canonical_ids

    for canonical_id in sorted(ab_all_canonical_ids):
        # Production SSOT contains a small number of legacy mixed-case canonicals.
        # Allow those exact IDs while enforcing snake_case for net-new AB-only IDs.
        if not CANONICAL_PATTERN.match(canonical_id) and canonical_id not in prod_canonical_ids:
            report.fail(
                check2,
                f"Canonical ID '{canonical_id}' violates snake_case naming standards.",
            )
        uk_variant = uk_us_duplicate_variant(canonical_id)
        if uk_variant and uk_variant in all_known_canonical_ids:
            report.fail(
                check2,
                f"Canonical ID '{canonical_id}' duplicates US spelling '{uk_variant}'.",
            )

    check3 = CHECKS_IN_ORDER[3]
    for canonical_id in sorted(ab_biomarkers.keys()):
        ab_definition = ab_biomarkers[canonical_id]
        if canonical_id in prod_biomarkers:
            prod_definition = prod_biomarkers[canonical_id]
            if ab_definition == prod_definition:
                report.note(check3, f"EXPANSION: '{canonical_id}' matches production definition.")
            else:
                report.fail(
                    check3,
                    f"CONFLICT: '{canonical_id}' exists in production but definition differs.",
                )
            continue

        folded_ab = fold_canonical_for_spelling(canonical_id)
        for prod_canonical in sorted(prod_biomarkers.keys()):
            if fold_canonical_for_spelling(prod_canonical) == folded_ab:
                report.fail(
                    check3,
                    "CONFLICT: "
                    f"'{canonical_id}' appears to duplicate production canonical "
                    f"'{prod_canonical}' via alternate spelling.",
                )
                break

    check4 = CHECKS_IN_ORDER[4]
    missing_in_burden = sorted(set(ab_biomarkers.keys()) - set(ab_burden.keys()))
    for canonical_id in missing_in_burden:
        report.fail(
            check4,
            f"AB biomarker '{canonical_id}' is missing from AB burden registry.",
        )

    check5 = CHECKS_IN_ORDER[5]
    for canonical_id, definition in sorted(ab_burden.items()):
        risk_direction = definition.get("risk_direction") if isinstance(definition, dict) else None
        if risk_direction not in ALLOWED_RISK_DIRECTIONS:
            report.fail(
                check5,
                f"AB burden '{canonical_id}' has invalid risk_direction '{risk_direction}'.",
            )

    check6 = CHECKS_IN_ORDER[6]
    prod_alias_doc = loaded["prod_alias"]
    alias_to_canonicals: dict[str, set[str]] = {}
    alias_debug: dict[str, set[str]] = {}

    def record_alias(canonical_id: str, alias_value: str) -> None:
        normalized = normalize_alias(alias_value)
        alias_to_canonicals.setdefault(normalized, set()).add(canonical_id)
        alias_debug.setdefault(normalized, set()).add(alias_value)

    if isinstance(prod_alias_doc, dict):
        for _, entry in sorted(prod_alias_doc.items()):
            if not isinstance(entry, dict):
                continue
            canonical_id = entry.get("canonical_id")
            aliases = entry.get("aliases", [])
            if not isinstance(canonical_id, str):
                continue
            if not isinstance(aliases, list):
                report.fail(
                    check6,
                    f"Production alias entry for '{canonical_id}' has non-list aliases.",
                )
                continue
            for alias in aliases:
                if not isinstance(alias, str):
                    report.fail(check6, f"Non-string alias under production canonical '{canonical_id}'.")
                    continue
                record_alias(canonical_id, alias)

    for entry in ab_alias_entries:
        if not isinstance(entry, dict):
            report.fail(check6, "AB alias entry must be a mapping.")
            continue
        canonical_id = entry.get("canonical_id")
        aliases = entry.get("aliases", [])
        if not isinstance(canonical_id, str):
            report.fail(check6, "AB alias entry missing string canonical_id.")
            continue
        if canonical_id not in ab_biomarkers:
            report.fail(
                check6,
                f"AB alias canonical_id '{canonical_id}' does not exist in AB biomarker file.",
            )
        if not isinstance(aliases, list):
            report.fail(check6, f"AB alias entry '{canonical_id}' has non-list aliases.")
            continue
        for alias in aliases:
            if not isinstance(alias, str):
                report.fail(check6, f"Non-string alias under AB canonical '{canonical_id}'.")
                continue
            record_alias(canonical_id, alias)

    for normalized_alias in sorted(alias_to_canonicals.keys()):
        canonical_ids = sorted(alias_to_canonicals[normalized_alias])
        if len(canonical_ids) > 1:
            source_examples = sorted(alias_debug.get(normalized_alias, set()))
            report.fail(
                check6,
                f"Alias collision for '{normalized_alias}' (seen as {source_examples}): maps to {canonical_ids}.",
            )

    # Every AB raw label must resolve to exactly one canonical in combined registries.
    n_resolvable = 0
    for entry in ab_alias_entries:
        if not isinstance(entry, dict):
            continue
        aliases = entry.get("aliases", [])
        if not isinstance(aliases, list):
            continue
        for raw_label in aliases:
            if not isinstance(raw_label, str):
                continue
            normalized = normalize_alias(raw_label)
            mapped = sorted(alias_to_canonicals.get(normalized, set()))
            if not mapped:
                report.fail(check6, f"AB raw label '{raw_label}' does not resolve to any canonical.")
            elif len(mapped) > 1:
                report.fail(
                    check6,
                    f"AB raw label '{raw_label}' resolves to multiple canonicals: {mapped}.",
                )
            else:
                n_resolvable += 1

    check7 = CHECKS_IN_ORDER[7]
    ranges_doc = optional_loaded.get("ranges")
    reference_ranges = {}
    if isinstance(ranges_doc, dict) and isinstance(ranges_doc.get("reference_ranges"), dict):
        reference_ranges = ranges_doc["reference_ranges"]
    else:
        report.note(check7, "No parseable ranges registry found; skipped reference-range cross-check.")

    scoring_doc = optional_loaded.get("scoring_policy")
    derived_registry: set[str] | None = None
    if isinstance(scoring_doc, dict) and isinstance(scoring_doc.get("derived_ratios"), list):
        derived_registry = {
            item for item in scoring_doc["derived_ratios"] if isinstance(item, str)
        }
    else:
        report.note(check7, "No derived ratio registry found; skipped derived-registry membership check.")

    for canonical_id in sorted(ab_biomarkers.keys()):
        if not canonical_has_derived_pattern(canonical_id):
            continue
        definition = ab_biomarkers.get(canonical_id, {})
        if not isinstance(definition, dict):
            continue

        # Treat presence in reference ranges as "requires lab reference ranges".
        if canonical_id in reference_ranges:
            report.fail(
                check7,
                f"Derived marker '{canonical_id}' appears in lab reference ranges (not allowed).",
            )

        explicit_requires_range_keys = [
            "requires_lab_reference_range",
            "requires_lab_reference_ranges",
            "requires_reference_range",
        ]
        for key in explicit_requires_range_keys:
            if bool(definition.get(key)):
                report.fail(
                    check7,
                    f"Derived marker '{canonical_id}' sets '{key}=true' (not allowed).",
                )

        if derived_registry is not None and canonical_id not in derived_registry:
            report.fail(
                check7,
                f"Derived marker '{canonical_id}' is missing from derived ratio registry.",
            )

        primary_markers = {
            "marker_type": "primary",
            "type": "primary",
            "classification": "primary",
        }
        for key, expected in primary_markers.items():
            if str(definition.get(key, "")).strip().lower() == expected:
                report.fail(
                    check7,
                    f"Derived marker '{canonical_id}' is explicitly marked as primary via '{key}'.",
                )
        if "is_derived" in definition and definition.get("is_derived") is False:
            report.fail(
                check7,
                f"Derived marker '{canonical_id}' is marked with is_derived=false.",
            )
        if "derived" in definition and definition.get("derived") is False:
            report.fail(
                check7,
                f"Derived marker '{canonical_id}' is marked with derived=false.",
            )

    report.counts = {
        "n_ab_biomarkers": len(ab_biomarkers),
        "n_ab_burden_entries": len(ab_burden),
        "n_ab_aliases": len(ab_alias_entries),
        "n_raw_labels_resolvable": n_resolvable,
    }
    report.print()
    return 1 if report.has_failures() else 0


if __name__ == "__main__":
    sys.exit(main())
