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
