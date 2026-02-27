"""
Sprint 6 - Cluster Definition Schema Loader & Validator.

Schema-driven clusters: load clusters.yaml, validate against canonical biomarkers,
deterministic version stamp. No hardcoded cluster logic.
"""

from typing import Dict, List, Any, Set, Optional
from dataclasses import dataclass
from pathlib import Path
import hashlib
import yaml


@dataclass
class ClusterDefinition:
    """Single cluster definition from schema."""

    cluster_id: str
    description: str
    required: List[str]
    important: List[str]
    optional: List[str]

    def all_biomarkers(self) -> Set[str]:
        return set(self.required) | set(self.important) | set(self.optional)


@dataclass
class ClusterSchema:
    """Loaded and validated cluster schema."""

    version: str
    schema_version: str
    clusters: Dict[str, ClusterDefinition]
    schema_hash: str  # Deterministic hash for reproducibility


_schema_cache: Optional[ClusterSchema] = None


def _get_canonical_biomarker_ids() -> Set[str]:
    """Load canonical biomarker IDs from biomarkers.yaml."""
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    if not ssot_path.exists():
        return set()
    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    bm = data.get("biomarkers", {})
    return set(bm.keys()) if isinstance(bm, dict) else set()


def _compute_schema_hash(version: str, schema_version: str, clusters: Dict[str, ClusterDefinition]) -> str:
    """Deterministic hash for reproducibility."""
    parts = [version, schema_version]
    for cid in sorted(clusters.keys()):
        c = clusters[cid]
        parts.append(f"{cid}:r={','.join(sorted(c.required))}:i={','.join(sorted(c.important))}:o={','.join(sorted(c.optional))}")
    content = "|".join(parts)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _validate_cluster(
    cluster_id: str,
    raw: Dict[str, Any],
    canonical_ids: Set[str],
) -> ClusterDefinition:
    """
    Validate a single cluster and return ClusterDefinition.
    Raises ValueError on validation failure.
    """
    bm = raw.get("biomarker_membership") or {}
    required = list(bm.get("required") or [])
    important = list(bm.get("important") or [])
    optional = list(bm.get("optional") or [])

    all_ids = set(required) | set(important) | set(optional)
    if not all_ids:
        raise ValueError(f"Cluster '{cluster_id}': empty cluster (no biomarkers in required/important/optional)")

    # No duplicate biomarker across categories
    if len(all_ids) != len(required) + len(important) + len(optional):
        raise ValueError(f"Cluster '{cluster_id}': duplicate biomarker in required/important/optional")

    # No unknown biomarker IDs
    unknown = all_ids - canonical_ids
    if unknown:
        raise ValueError(f"Cluster '{cluster_id}': unknown biomarker IDs: {sorted(unknown)}")

    return ClusterDefinition(
        cluster_id=cluster_id,
        description=str(raw.get("description", "")),
        required=required,
        important=important,
        optional=optional,
    )


def load_cluster_schema() -> ClusterSchema:
    """Load and validate cluster schema from ssot/clusters.yaml. Cached."""
    global _schema_cache
    if _schema_cache is not None:
        return _schema_cache

    clusters_path = Path(__file__).parent.parent.parent / "ssot" / "clusters.yaml"
    if not clusters_path.exists():
        raise FileNotFoundError(f"Cluster schema not found: {clusters_path}")

    with open(clusters_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    version = str(data.get("version", "1.0.0"))
    schema_version = str(data.get("schema_version", "1.0"))
    raw_clusters = data.get("clusters") or {}

    if not isinstance(raw_clusters, dict):
        raise ValueError("clusters.yaml: 'clusters' must be a mapping")

    canonical_ids = _get_canonical_biomarker_ids()
    clusters: Dict[str, ClusterDefinition] = {}

    for cluster_id, raw in raw_clusters.items():
        if not isinstance(raw, dict):
            raise ValueError(f"Cluster '{cluster_id}' must be a mapping")
        if raw.get("cluster_id") != cluster_id:
            raise ValueError(f"Cluster key '{cluster_id}' must match cluster_id field")
        clusters[cluster_id] = _validate_cluster(cluster_id, raw, canonical_ids)

    schema_hash = _compute_schema_hash(version, schema_version, clusters)
    _schema_cache = ClusterSchema(
        version=version,
        schema_version=schema_version,
        clusters=clusters,
        schema_hash=schema_hash,
    )
    return _schema_cache


def compute_cluster_status(
    cluster_def: ClusterDefinition,
    available_biomarkers: Set[str],
) -> Dict[str, Any]:
    """
    Given a cluster definition and available biomarkers, compute deterministic cluster status.

    Returns:
        - complete: bool (all required present)
        - required_present: set
        - required_missing: set
        - important_present: set
        - important_missing: set
        - optional_present: set
    """
    req_present = set(cluster_def.required) & available_biomarkers
    req_missing = set(cluster_def.required) - available_biomarkers
    imp_present = set(cluster_def.important) & available_biomarkers
    imp_missing = set(cluster_def.important) - available_biomarkers
    opt_present = set(cluster_def.optional) & available_biomarkers

    return {
        "complete": len(req_missing) == 0,
        "required_present": req_present,
        "required_missing": req_missing,
        "important_present": imp_present,
        "important_missing": imp_missing,
        "optional_present": opt_present,
    }


def get_cluster_schema_version_stamp() -> Dict[str, str]:
    """Return version stamp for DTO inclusion."""
    schema = load_cluster_schema()
    return {
        "cluster_schema_version": schema.version,
        "cluster_schema_hash": schema.schema_hash,
    }
