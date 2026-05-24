"""
LC-S17 — Knowledge Bus lifecycle contract (machine-enforced subset).

Full framework: docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, FrozenSet, Iterable, List, Sequence

import yaml

LIFECYCLE_STATES: Final[FrozenSet[str]] = frozenset(
    {
        "draft",
        "validated",
        "runtime-loaded",
        "signal-only",
        "WHY-enabled",
        "frontend-surfaced",
        "Sentinel-protected",
    }
)

PACKAGE_TYPES: Final[FrozenSet[str]] = frozenset(
    {
        "signal-only",
        "WHY-enabled",
        "IDL-display-enabled",
        "lifestyle-modifier",
        "medication-overlay",
        "combination-case",
    }
)

STANDARD_PACKAGE_FILES: Final[FrozenSet[str]] = frozenset(
    {
        "package_manifest.yaml",
        "research_brief.yaml",
        "signal_library.yaml",
    }
)

WHY_ENABLED_PACKAGE_FILES: Final[FrozenSet[str]] = frozenset(
    STANDARD_PACKAGE_FILES
    | {
        "promoted_signal_intelligence.yaml",
    }
)

EXCLUDED_RUNTIME_PACKAGES: Final[FrozenSet[str]] = frozenset({"pkg_example"})

ESTATE_INVENTORY_PATH: Final[str] = (
    "knowledge_bus/governance/package_estate_KB-S49_v1.yaml"
)

POST_KB_S49_BATCH_PREFIXES: Final[tuple[str, ...]] = (
    "pkg_kb52c_",
    "pkg_kb52d_",
    "pkg_kb56_",
    "pkg_kb58_",
    "pkg_kb59_",
    "pkg_kb60_",
    "pkg_kb61_",
)

LIPID_KB_WAVE1_FRAGMENTS: Final[tuple[str, ...]] = (
    "ldl",
    "apob",
    "apoa",
    "hdl",
    "lipid",
    "cholesterol",
    "triglycer",
    "non_hdl",
)

GOVERNED_TIER_POST_KB_S49_UNREVIEWED: Final[str] = (
    "post_kb_s49_unreviewed_batch"
)


@dataclass(frozen=True)
class PackageEstateAssessment:
    inventory_path: str
    disk_package_count: int
    inventory_package_count: int
    orphan_disk_not_in_inventory: tuple[str, ...]
    orphan_inventory_not_on_disk: tuple[str, ...]
    duplicate_package_ids: tuple[str, ...]
    why_enabled_count: int
    signal_only_count: int
    unknown_type_count: int
    draft_incomplete_count: int
    lipid_relevant_orphans: tuple[str, ...]
    review_queue_count: int


@dataclass(frozen=True)
class OrphanPackageReport:
    disk_not_in_inventory: tuple[str, ...]
    inventory_not_on_disk: tuple[str, ...]

    @property
    def has_orphans(self) -> bool:
        return bool(self.disk_not_in_inventory or self.inventory_not_on_disk)


def list_package_dirs(packages_root: Path) -> List[str]:
    if not packages_root.is_dir():
        return []
    return sorted(
        p.name
        for p in packages_root.iterdir()
        if p.is_dir() and p.name.startswith("pkg_")
    )


def load_estate_inventory_package_ids(repo_root: Path) -> FrozenSet[str]:
    path = repo_root / ESTATE_INVENTORY_PATH
    if not path.is_file():
        return frozenset()
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return frozenset()
    packages = payload.get("packages")
    if not isinstance(packages, list):
        return frozenset()
    ids: set[str] = set()
    for row in packages:
        if isinstance(row, dict):
            pid = row.get("package_id")
            if isinstance(pid, str) and pid.strip():
                ids.add(pid.strip())
    return frozenset(ids)


def detect_orphan_packages(repo_root: Path) -> OrphanPackageReport:
    packages_root = repo_root / "knowledge_bus" / "packages"
    on_disk = frozenset(list_package_dirs(packages_root)) - EXCLUDED_RUNTIME_PACKAGES
    in_inventory = load_estate_inventory_package_ids(repo_root)
    if not in_inventory:
        return OrphanPackageReport(tuple(sorted(on_disk)), ())
    disk_not_in_inventory = tuple(sorted(on_disk - in_inventory))
    inventory_not_on_disk = tuple(
        sorted(pid for pid in in_inventory if pid not in on_disk and pid not in EXCLUDED_RUNTIME_PACKAGES)
    )
    return OrphanPackageReport(disk_not_in_inventory, inventory_not_on_disk)


def package_has_required_files(package_dir: Path, required: FrozenSet[str]) -> List[str]:
    missing: List[str] = []
    for name in sorted(required):
        if not (package_dir / name).is_file():
            missing.append(name)
    return missing


def classify_package_type(package_dir: Path) -> str:
    manifest_path = package_dir / "package_manifest.yaml"
    if not manifest_path.is_file():
        return "unknown"
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return "unknown"
    if not isinstance(manifest, dict):
        return "unknown"
    if manifest.get("promoted_signal_intelligence"):
        psi = package_dir / "promoted_signal_intelligence.yaml"
        if psi.is_file():
            return "WHY-enabled"
    return "signal-only"


def iter_why_enabled_packages(repo_root: Path) -> Iterable[Path]:
    root = repo_root / "knowledge_bus" / "packages"
    for name in list_package_dirs(root):
        if name in EXCLUDED_RUNTIME_PACKAGES:
            continue
        pkg = root / name
        if classify_package_type(pkg) == "WHY-enabled":
            yield pkg


def _read_manifest(package_dir: Path) -> dict | None:
    manifest_path = package_dir / "package_manifest.yaml"
    if not manifest_path.is_file():
        return None
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return payload if isinstance(payload, dict) else None


def _signal_library_schema_version(package_dir: Path) -> str:
    path = package_dir / "signal_library.yaml"
    if not path.is_file():
        return "unknown"
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return "unknown"
    if not isinstance(payload, dict):
        return "unknown"
    library = payload.get("library")
    if isinstance(library, dict):
        version = library.get("schema_version")
        if isinstance(version, str) and version.strip():
            return version.strip()
    return "1.0.0"


def infer_governed_tier(package_id: str, package_dir: Path) -> str:
    missing = package_has_required_files(package_dir, STANDARD_PACKAGE_FILES)
    if missing:
        return "unknown_requires_review"
    manifest = _read_manifest(package_dir) or {}
    has_psi = (package_dir / "promoted_signal_intelligence.yaml").is_file()
    if package_id.startswith("pkg_kb47_") and manifest.get("promoted_signal_intelligence") and has_psi:
        return "v3_grade_rich_governed"
    if package_id.startswith("pkg_kb45_"):
        return "partially_uplifted_research_fidelity_no_psi"
    if package_id.startswith("pkg_s24_"):
        return "structured_translation_batch_no_psi"
    if any(package_id.startswith(prefix) for prefix in POST_KB_S49_BATCH_PREFIXES):
        return GOVERNED_TIER_POST_KB_S49_UNREVIEWED
    return "legacy_thin_pre_v3_context"


def is_lipid_kb_wave1_relevant(package_id: str) -> bool:
    lowered = package_id.lower()
    return any(fragment in lowered for fragment in LIPID_KB_WAVE1_FRAGMENTS)


def build_inventory_row(repo_root: Path, package_id: str, *, requires_review: bool) -> dict:
    package_dir = repo_root / "knowledge_bus" / "packages" / package_id
    manifest = _read_manifest(package_dir) or {}
    has_psi = (package_dir / "promoted_signal_intelligence.yaml").is_file()
    schema_version = _signal_library_schema_version(package_dir)
    governed_tier = infer_governed_tier(package_id, package_dir)
    source_document = manifest.get("source_document")
    if source_document is not None and not isinstance(source_document, str):
        source_document = None
    translation_mode = manifest.get("translation_mode")
    if translation_mode is not None and not isinstance(translation_mode, str):
        translation_mode = None
    package_type = classify_package_type(package_dir)
    row = {
        "package_id": package_id,
        "files": {
            "package_manifest": (package_dir / "package_manifest.yaml").is_file(),
            "research_brief": (package_dir / "research_brief.yaml").is_file(),
            "signal_library": (package_dir / "signal_library.yaml").is_file(),
            "promoted_signal_intelligence": has_psi,
        },
        "manifest_promoted_key": bool(manifest.get("promoted_signal_intelligence")),
        "manifest_intelligence_model": bool(manifest.get("intelligence_model")),
        "manifest_behavioural_impact": bool(manifest.get("behavioural_impact")),
        "translation_mode": translation_mode,
        "signal_library_schema_version": schema_version,
        "integrity_flag": None,
        "governed_tier": governed_tier,
        "signal_contract_tier": (
            "signal_contract_v2" if schema_version.startswith("2.") else "signal_contract_v1_or_default"
        ),
        "validator_ready_for_implementation": not requires_review,
        "validate_knowledge_package_exit_code": None if requires_review else 0,
        "manifest_source_document": source_document,
        "package_type": package_type,
        "requires_review": requires_review,
        "runtime_loaded": False,
        "kb_wave_1_lipid_relevant": is_lipid_kb_wave1_relevant(package_id),
    }
    if requires_review:
        row["inventory_refresh_work_id"] = "LC-S18A"
    return row


def find_duplicate_inventory_package_ids(repo_root: Path) -> tuple[str, ...]:
    path = repo_root / ESTATE_INVENTORY_PATH
    if not path.is_file():
        return ()
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ()
    packages = payload.get("packages")
    if not isinstance(packages, list):
        return ()
    seen: dict[str, int] = {}
    for row in packages:
        if isinstance(row, dict):
            pid = row.get("package_id")
            if isinstance(pid, str) and pid.strip():
                seen[pid.strip()] = seen.get(pid.strip(), 0) + 1
    return tuple(sorted(pid for pid, count in seen.items() if count > 1))


def count_review_queue_packages(repo_root: Path) -> int:
    path = repo_root / ESTATE_INVENTORY_PATH
    if not path.is_file():
        return 0
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return 0
    packages = payload.get("packages")
    if not isinstance(packages, list):
        return 0
    count = 0
    for row in packages:
        if isinstance(row, dict) and row.get("requires_review") is True:
            count += 1
    return count


def assess_package_estate(repo_root: Path) -> PackageEstateAssessment:
    packages_root = repo_root / "knowledge_bus" / "packages"
    on_disk = list_package_dirs(packages_root)
    report = detect_orphan_packages(repo_root)
    why_enabled = 0
    signal_only = 0
    unknown_type = 0
    draft_incomplete = 0
    for name in on_disk:
        if name in EXCLUDED_RUNTIME_PACKAGES:
            continue
        pkg = packages_root / name
        pkg_type = classify_package_type(pkg)
        if pkg_type == "WHY-enabled":
            why_enabled += 1
        elif pkg_type == "signal-only":
            signal_only += 1
        else:
            unknown_type += 1
        missing = package_has_required_files(pkg, STANDARD_PACKAGE_FILES)
        if missing:
            draft_incomplete += 1
    lipid_orphans = tuple(
        sorted(pid for pid in report.disk_not_in_inventory if is_lipid_kb_wave1_relevant(pid))
    )
    inventory_ids = load_estate_inventory_package_ids(repo_root)
    return PackageEstateAssessment(
        inventory_path=ESTATE_INVENTORY_PATH,
        disk_package_count=len(on_disk),
        inventory_package_count=len(inventory_ids),
        orphan_disk_not_in_inventory=report.disk_not_in_inventory,
        orphan_inventory_not_on_disk=report.inventory_not_on_disk,
        duplicate_package_ids=find_duplicate_inventory_package_ids(repo_root),
        why_enabled_count=why_enabled,
        signal_only_count=signal_only,
        unknown_type_count=unknown_type,
        draft_incomplete_count=draft_incomplete,
        lipid_relevant_orphans=lipid_orphans,
        review_queue_count=count_review_queue_packages(repo_root),
    )
