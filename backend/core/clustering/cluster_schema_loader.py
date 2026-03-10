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
_cluster_scoring_policy_cache: Optional["ClusterScoringPolicy"] = None


@dataclass
class ClusterScoringPolicy:
    """Loaded cluster scoring policy for active ClusterEngineV2 runtime."""

    policy_version: str
    schema_version: str
    min_members_per_cluster: int
    severity_thresholds: Dict[str, float]
    confidence: Dict[str, float]
    overall_confidence: Dict[str, float]


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


def _cluster_scoring_policy_path() -> Path:
    return Path(__file__).parent.parent.parent / "ssot" / "cluster_scoring_policy.yaml"


def _validate_cluster_scoring_policy(raw: Dict[str, Any]) -> ClusterScoringPolicy:
    policy_version = str(raw.get("policy_version", "")).strip()
    if not policy_version:
        raise ValueError("cluster_scoring_policy.yaml must include policy_version")
    schema_version = str(raw.get("schema_version", "")).strip()
    if not schema_version:
        raise ValueError("cluster_scoring_policy.yaml must include schema_version")

    membership = raw.get("cluster_membership", {})
    if not isinstance(membership, dict):
        raise ValueError("cluster_membership must be a mapping")
    min_members = membership.get("min_members_per_cluster")
    if not isinstance(min_members, int) or min_members < 1:
        raise ValueError("cluster_membership.min_members_per_cluster must be int >= 1")

    severity = raw.get("severity_thresholds", {})
    if not isinstance(severity, dict):
        raise ValueError("severity_thresholds must be a mapping")
    required_severity_keys = ["critical_lt", "high_lt", "moderate_lt", "mild_lt"]
    for key in required_severity_keys:
        if not isinstance(severity.get(key), (int, float)):
            raise ValueError(f"severity_thresholds.{key} must be numeric")
    if not (
        float(severity["critical_lt"])
        < float(severity["high_lt"])
        < float(severity["moderate_lt"])
        < float(severity["mild_lt"])
    ):
        raise ValueError(
            "severity_thresholds must be strictly increasing: critical_lt < high_lt < moderate_lt < mild_lt"
        )

    confidence = raw.get("confidence", {})
    if not isinstance(confidence, dict):
        raise ValueError("confidence must be a mapping")
    for key in ["variance_divisor", "size_boost_per_member", "max_size_boost"]:
        if not isinstance(confidence.get(key), (int, float)):
            raise ValueError(f"confidence.{key} must be numeric")
    if float(confidence["variance_divisor"]) <= 0.0:
        raise ValueError("confidence.variance_divisor must be > 0")
    if float(confidence["size_boost_per_member"]) < 0.0:
        raise ValueError("confidence.size_boost_per_member must be >= 0")
    if float(confidence["max_size_boost"]) < 0.0:
        raise ValueError("confidence.max_size_boost must be >= 0")

    overall = raw.get("overall_confidence", {})
    if not isinstance(overall, dict):
        raise ValueError("overall_confidence must be a mapping")
    for key in [
        "invalid_cluster_penalty",
        "out_of_range_cluster_count_penalty",
        "optimal_cluster_count_min",
        "optimal_cluster_count_max",
    ]:
        if not isinstance(overall.get(key), (int, float)):
            raise ValueError(f"overall_confidence.{key} must be numeric")
    if float(overall["invalid_cluster_penalty"]) < 0.0:
        raise ValueError("overall_confidence.invalid_cluster_penalty must be >= 0")
    if float(overall["out_of_range_cluster_count_penalty"]) < 0.0:
        raise ValueError("overall_confidence.out_of_range_cluster_count_penalty must be >= 0")
    min_count = int(overall["optimal_cluster_count_min"])
    max_count = int(overall["optimal_cluster_count_max"])
    if min_count < 0 or max_count < 0 or min_count > max_count:
        raise ValueError(
            "overall_confidence optimal cluster count bounds must satisfy 0 <= min <= max"
        )

    return ClusterScoringPolicy(
        policy_version=policy_version,
        schema_version=schema_version,
        min_members_per_cluster=min_members,
        severity_thresholds={k: float(severity[k]) for k in required_severity_keys},
        confidence={
            "variance_divisor": float(confidence["variance_divisor"]),
            "size_boost_per_member": float(confidence["size_boost_per_member"]),
            "max_size_boost": float(confidence["max_size_boost"]),
        },
        overall_confidence={
            "invalid_cluster_penalty": float(overall["invalid_cluster_penalty"]),
            "out_of_range_cluster_count_penalty": float(overall["out_of_range_cluster_count_penalty"]),
            "optimal_cluster_count_min": float(min_count),
            "optimal_cluster_count_max": float(max_count),
        },
    )


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


def load_cluster_scoring_policy() -> ClusterScoringPolicy:
    """Load and validate active cluster scoring policy. Cached."""
    global _cluster_scoring_policy_cache
    if _cluster_scoring_policy_cache is not None:
        return _cluster_scoring_policy_cache

    policy_path = _cluster_scoring_policy_path()
    if not policy_path.exists():
        raise FileNotFoundError(f"Cluster scoring policy not found: {policy_path}")
    with open(policy_path, "r", encoding="utf-8") as f:
        payload = yaml.safe_load(f) or {}
    if not isinstance(payload, dict):
        raise ValueError("cluster_scoring_policy.yaml must parse to a top-level mapping")
    _cluster_scoring_policy_cache = _validate_cluster_scoring_policy(payload)
    return _cluster_scoring_policy_cache


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
