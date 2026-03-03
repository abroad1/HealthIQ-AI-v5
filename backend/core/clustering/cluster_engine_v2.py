"""
Cluster Engine v2 - Deterministic cluster scoring engine.

Sprint 16: Engine-only implementation (not wired to runtime).
Provides deterministic cluster scoring based on biomarker values and derived metrics.
"""

from dataclasses import dataclass
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml

from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerCluster


def load_cluster_rules(path: str = "backend/ssot/cluster_rules.yaml") -> Dict[str, Any]:
    """
    Load cluster rules from YAML file.
    
    Args:
        path: Path to cluster_rules.yaml (relative to repo root or absolute)
        
    Returns:
        Dictionary with "rules" list and "version" string.
        Returns {"rules": [], "version": "v1"} if file is empty or missing.
    """
    rules_path = Path(path)
    
    # Handle relative paths from repo root
    if not rules_path.is_absolute():
        # Try current directory first
        if not rules_path.exists():
            # Try from repo root (assuming we're in backend/)
            repo_root = Path(__file__).parent.parent.parent.parent
            rules_path = repo_root / path
        else:
            rules_path = Path(path).resolve()
    
    if not rules_path.exists():
        return {"rules": [], "version": "v1"}
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    
    return {
        "rules": data.get("rules", []),
        "version": data.get("version", "v1")
    }


def score_clusters(
    biomarkers: List[Dict[str, Any]], 
    derived: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Score health system clusters based on biomarkers and derived metrics.
    
    Args:
        biomarkers: List of biomarker dicts with fields:
            - name or biomarker_name: str (canonical name)
            - value: float (optional)
            - flag or status: str (optional, "low", "high", "normal")
        derived: List of derived metric dicts with fields:
            - id: str (e.g. "tg_hdl", "alt_ast")
            - value: float (optional)
            - band: str (optional, "optimal", "borderline", "high", "low")
    
    Returns:
        List of cluster result dicts (ClusterDTO-like) with structure:
        {
            "id": str,              # Cluster ID (e.g. "metabolic", "hepatic")
            "score": int,            # Score 0-100
            "band": str,             # "green", "amber", or "red"
            "drivers": List[str],    # Driver descriptions
            "confidence": float,     # Confidence 0.0-1.0
            "tags": List[str]        # Optional tags from rules
        }
    """
    # Sprint 6: Schema-driven cluster definitions
    try:
        from core.clustering.cluster_schema_loader import load_cluster_schema
        schema = load_cluster_schema()
        cluster_biomarkers = {
            cid: list(cdef.all_biomarkers())
            for cid, cdef in schema.clusters.items()
        }
        cluster_ids = list(cluster_biomarkers.keys())
    except (ImportError, FileNotFoundError, ValueError):
        cluster_ids = []
        cluster_biomarkers = {}
    
    # Load cluster rules
    rules = load_cluster_rules()
    
    # Create biomarker lookup
    biomarker_lookup: Dict[str, Dict[str, Any]] = {}
    for bm in biomarkers:
        name = bm.get("name") or bm.get("biomarker_name")
        if name:
            biomarker_lookup[name] = bm
    
    # Create derived lookup
    derived_lookup: Dict[str, Dict[str, Any]] = {}
    for dm in derived:
        dm_id = dm.get("id")
        if dm_id:
            derived_lookup[dm_id] = dm
    
    results: List[Dict[str, Any]] = []
    
    for cluster_id in cluster_ids:
        # Compute base score from biomarkers in cluster
        base_score = 0.0
        cluster_bm_names = cluster_biomarkers.get(cluster_id, [])
        present_count = 0
        
        drivers: List[str] = []
        
        for bm_name in cluster_bm_names:
            if bm_name in biomarker_lookup:
                bm = biomarker_lookup[bm_name]
                present_count += 1
                
                # Get flag/status
                flag = bm.get("flag") or bm.get("status", "normal")
                value = bm.get("value")
                
                # Map flag to score contribution
                if flag == "high":
                    base_score += 10.0  # Positive contribution
                    if value is not None:
                        drivers.append(f"{bm_name} {value} high")
                    else:
                        drivers.append(f"{bm_name} high")
                elif flag == "low":
                    base_score -= 5.0  # Negative contribution
                    if value is not None:
                        drivers.append(f"{bm_name} {value} low")
                    else:
                        drivers.append(f"{bm_name} low")
                # "normal" contributes 0
        
        # Apply rule-based compensations
        tags: List[str] = []
        for rule in rules.get("rules", []):
            rule_cluster = rule.get("then", {}).get("cluster")
            if rule_cluster != cluster_id:
                continue
            
            # Check if all conditions match
            if_all = rule.get("if_all", [])
            all_match = True
            
            for condition in if_all:
                if ":" not in condition:
                    all_match = False
                    break
                
                key, value = condition.split(":", 1)
                
                # Check biomarker flags
                if key in biomarker_lookup:
                    bm_flag = biomarker_lookup[key].get("flag") or biomarker_lookup[key].get("status", "normal")
                    if bm_flag != value:
                        all_match = False
                        break
                # Check derived bands
                elif key in derived_lookup:
                    dm_band = derived_lookup[key].get("band", "")
                    if dm_band != value:
                        all_match = False
                        break
                else:
                    all_match = False
                    break
            
            if all_match:
                compensation = rule.get("then", {}).get("add", 0.0)
                base_score += compensation
                
                if "tag" in rule:
                    tags.append(rule["tag"])
        
        # Scale to 0-100 (simple linear mapping for now)
        # Base score of 0 -> 50, positive -> 50-100, negative -> 0-50
        score = max(0, min(100, int(50 + base_score)))
        
        # Assign band
        if score < 50:
            band = "green"
        elif score < 70:
            band = "amber"
        else:
            band = "red"
        
        # Compute confidence: fraction of required members present
        total_members = len(cluster_bm_names)
        if total_members == 0:
            confidence = 0.0
        else:
            confidence = min(1.0, present_count / total_members)
        
        results.append({
            "id": cluster_id,
            "score": score,
            "band": band,
            "drivers": drivers,
            "confidence": round(confidence, 2),
            "tags": tags
        })
    
    return results


@dataclass
class ClusterEngineV2Result:
    """Runtime result shape used by orchestrator."""

    clusters: List[BiomarkerCluster]
    algorithm_used: str
    confidence_score: float
    validation_summary: Dict[str, Any]
    processing_time_ms: float


class ClusterEngineV2:
    """
    Sole runtime clustering engine (Sprint 12 convergence).

    Deterministic single-path clustering over schema-defined groups.
    """

    algorithm_name = "cluster_engine_v2"

    def cluster_biomarkers(self, context: AnalysisContext, scoring_result: Any) -> ClusterEngineV2Result:
        start_time = time.time()
        biomarker_scores = self._extract_biomarker_scores(scoring_result)
        groups = self._group_biomarkers_by_health_system(set(biomarker_scores.keys()))
        clusters = self._build_clusters(groups, biomarker_scores)
        validation_summary = self._validate_clusters(clusters)
        confidence_score = self._calculate_overall_confidence(clusters, validation_summary)
        elapsed_ms = (time.time() - start_time) * 1000
        return ClusterEngineV2Result(
            clusters=clusters,
            algorithm_used=self.algorithm_name,
            confidence_score=confidence_score,
            validation_summary=validation_summary,
            processing_time_ms=elapsed_ms,
        )

    def _extract_biomarker_scores(self, scoring_result: Any) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        if hasattr(scoring_result, "health_system_scores"):
            for _, system_score in scoring_result.health_system_scores.items():
                for biomarker_score in system_score.biomarker_scores:
                    scores[biomarker_score.biomarker_name] = float(biomarker_score.score)
            return scores
        if isinstance(scoring_result, dict):
            for _, system_data in (scoring_result.get("health_system_scores") or {}).items():
                for biomarker_score in (system_data or {}).get("biomarker_scores", []):
                    name = biomarker_score.get("biomarker_name")
                    score = biomarker_score.get("score")
                    if name and isinstance(score, (int, float)):
                        scores[name] = float(score)
        return scores

    def _group_biomarkers_by_health_system(self, available_biomarkers: set[str]) -> Dict[str, List[str]]:
        try:
            from core.clustering.cluster_schema_loader import load_cluster_schema
            schema = load_cluster_schema()
        except (ImportError, FileNotFoundError, ValueError):
            return {}
        grouped: Dict[str, List[str]] = {}
        for cluster_id, cluster_def in schema.clusters.items():
            present = sorted([b for b in cluster_def.all_biomarkers() if b in available_biomarkers])
            if present:
                grouped[cluster_id] = present
        return grouped

    def _build_clusters(self, groups: Dict[str, List[str]], scores: Dict[str, float]) -> List[BiomarkerCluster]:
        clusters: List[BiomarkerCluster] = []
        for system_name, biomarkers in sorted(groups.items()):
            if len(biomarkers) < 2:
                continue
            avg_score = sum(scores.get(b, 0.0) for b in biomarkers) / len(biomarkers)
            if avg_score < 30:
                severity = "critical"
            elif avg_score < 50:
                severity = "high"
            elif avg_score < 70:
                severity = "moderate"
            elif avg_score < 85:
                severity = "mild"
            else:
                severity = "normal"
            confidence = self._calculate_cluster_confidence(biomarkers, scores)
            clusters.append(
                BiomarkerCluster(
                    cluster_id=f"{system_name}_{len(biomarkers)}_biomarkers",
                    name=f"{system_name.title()} Health Pattern",
                    biomarkers=biomarkers,
                    description=f"{severity.title()} {system_name} health pattern affecting {', '.join(biomarkers[:3])}"
                    + (f" and {len(biomarkers) - 3} others" if len(biomarkers) > 3 else ""),
                    severity=severity,
                    confidence=confidence,
                )
            )
        return clusters

    def _calculate_cluster_confidence(self, biomarkers: List[str], scores: Dict[str, float]) -> float:
        if not biomarkers:
            return 0.0
        score_values = [scores.get(b, 0.0) for b in biomarkers]
        if not score_values:
            return 0.0
        mean_score = sum(score_values) / len(score_values)
        variance = sum((score - mean_score) ** 2 for score in score_values) / len(score_values)
        confidence = max(0.0, 1.0 - (variance / 2500))
        size_boost = min(0.2, len(biomarkers) * 0.05)
        return min(1.0, confidence + size_boost)

    def _validate_clusters(self, clusters: List[BiomarkerCluster]) -> Dict[str, Any]:
        if not clusters:
            return {"total_clusters": 0, "valid_clusters": 0, "is_valid": True}
        return {
            "total_clusters": len(clusters),
            "valid_clusters": len(clusters),
            "is_valid": True,
        }

    def _calculate_overall_confidence(self, clusters: List[BiomarkerCluster], validation_summary: Dict[str, Any]) -> float:
        if not clusters:
            return 0.0
        avg_cluster_confidence = sum(cluster.confidence for cluster in clusters) / len(clusters)
        validation_penalty = 0.2 if not validation_summary.get("is_valid", True) else 0.0
        cluster_count = len(clusters)
        if cluster_count < 2 or cluster_count > 6:
            validation_penalty += 0.1
        return max(0.0, avg_cluster_confidence - validation_penalty)

