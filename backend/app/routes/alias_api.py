"""
Alias API routes - provides access to biomarker alias registry.

This module exposes the v4 alias registry through REST API endpoints,
enabling frontend and external services to access comprehensive
biomarker alias mappings.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from core.canonical.alias_registry_service import AliasRegistryService

router = APIRouter()

# Global alias service instance (singleton pattern for performance)
_alias_service = None

def get_alias_service() -> AliasRegistryService:
    """Get or create the global alias service instance."""
    global _alias_service
    if _alias_service is None:
        _alias_service = AliasRegistryService(use_v4_registry=True)
    return _alias_service


@router.get("/aliases")
async def get_aliases() -> Dict[str, List[str]]:
    """
    Get all biomarker aliases grouped by canonical name.
    
    Returns:
        Dict mapping canonical biomarker names to lists of aliases
        
    Example:
        {
            "hdl": ["HDL", "HDL Cholesterol", "High-Density Lipoprotein"],
            "ldl": ["LDL", "LDL Cholesterol", "Low-Density Lipoprotein"]
        }
    """
    try:
        service = get_alias_service()
        aliases = service.get_all_aliases()
        return aliases
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load alias registry: {str(e)}"
        )


@router.get("/aliases/canonical")
async def get_canonical_biomarkers() -> List[str]:
    """
    Get list of all canonical biomarker names.
    
    Returns:
        List of canonical biomarker names
    """
    try:
        service = get_alias_service()
        canonical = service.get_canonical_biomarkers()
        return canonical
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load canonical biomarkers: {str(e)}"
        )


@router.get("/aliases/resolve/{alias}")
async def resolve_alias(alias: str) -> Dict[str, str]:
    """
    Resolve a specific alias to its canonical name.
    
    Args:
        alias: The alias to resolve
        
    Returns:
        Dict with 'alias' and 'canonical' keys
    """
    try:
        service = get_alias_service()
        canonical = service.resolve(alias)
        
        return {
            "alias": alias,
            "canonical": canonical,
            "is_mapped": not canonical.startswith("unmapped_")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resolve alias '{alias}': {str(e)}"
        )


@router.get("/aliases/stats")
async def get_alias_stats() -> Dict[str, Any]:
    """
    Get statistics about the alias registry.
    
    Returns:
        Dict with alias count, canonical count, and other metrics
    """
    try:
        service = get_alias_service()
        
        return {
            "alias_count": service.get_alias_count(),
            "canonical_count": service.get_canonical_count(),
            "using_v4_registry": service.use_v4_registry,
            "loaded": service._loaded
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get alias statistics: {str(e)}"
        )


@router.post("/aliases/normalize")
async def normalize_biomarkers(panel: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a biomarker panel to use canonical names.
    
    Args:
        panel: Dict with biomarker names as keys and values as values
        
    Returns:
        Normalized panel with canonical names as keys
    """
    try:
        service = get_alias_service()
        normalized = service.normalize_panel(panel)
        
        return {
            "original_panel": panel,
            "normalized_panel": normalized,
            "biomarker_count": len(normalized)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to normalize biomarker panel: {str(e)}"
        )
