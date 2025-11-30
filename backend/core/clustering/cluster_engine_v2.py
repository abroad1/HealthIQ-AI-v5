"""
Cluster Engine v2 - Deterministic cluster scoring engine.

Sprint 16: Engine-only implementation (not wired to runtime).
Provides deterministic cluster scoring based on biomarker values and derived metrics.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml


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
    # Load SSOT biomarkers to determine cluster membership
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    with open(ssot_path, 'r', encoding='utf-8') as f:
        ssot_data = yaml.safe_load(f) or {}
    
    ssot_biomarkers = ssot_data.get("biomarkers", {})
    
    # Define 8 health system clusters
    cluster_ids = [
        "metabolic",
        "cardiovascular",
        "hepatic",
        "renal",
        "inflammatory",
        "hematological",
        "hormonal",
        "nutritional"
    ]
    
    # Build cluster -> biomarkers mapping from SSOT
    cluster_biomarkers: Dict[str, List[str]] = {}
    for biomarker_name, definition in ssot_biomarkers.items():
        system = definition.get("system", "")
        if system in cluster_ids:
            if system not in cluster_biomarkers:
                cluster_biomarkers[system] = []
            cluster_biomarkers[system].append(biomarker_name)
    
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

