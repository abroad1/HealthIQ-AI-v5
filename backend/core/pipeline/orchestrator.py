"""
Analysis orchestrator - enforces canonical-only keys and coordinates analysis.
"""

from typing import Dict, Any, List, Mapping, Optional

from core.canonical.normalize import BiomarkerNormalizer, normalize_panel
from core.canonical.resolver import resolve_to_canonical
from core.pipeline.context_factory import AnalysisContextFactory
from core.models.context import AnalysisContext
from core.models.user import User


class AnalysisOrchestrator:
    """Orchestrates biomarker analysis with canonical enforcement."""
    
    def __init__(self, normalizer: Optional[BiomarkerNormalizer] = None):

        """
        Initialize the orchestrator.
        
        Args:
            normalizer: BiomarkerNormalizer instance, creates new one if None
        """
        self.normalizer = normalizer or BiomarkerNormalizer()
        self.context_factory = AnalysisContextFactory()
    
    def create_analysis_context(
        self,
        analysis_id: str,
        raw_biomarkers: Dict[str, Any],
        user_data: Dict[str, Any],
        *,
        assume_canonical: bool = False
    ) -> AnalysisContext:
        """
        Create analysis context with canonical enforcement.
        
        Args:
            analysis_id: Unique analysis identifier
            raw_biomarkers: Raw biomarker data (may contain aliases)
            user_data: Raw user data
            assume_canonical: If True, skip canonical validation
            
        Returns:
            AnalysisContext with canonical biomarkers only
            
        Raises:
            ValueError: If non-canonical biomarkers are found after normalization
        """
        if not assume_canonical:
            self._assert_canonical_only(raw_biomarkers, where="create_analysis_context")
        
        # Normalize biomarkers (maps aliases to canonical names)
        biomarker_panel, unmapped_keys = self.normalizer.normalize_biomarkers(raw_biomarkers)
        
        # Log unmapped keys (in production, this would be proper logging)
        if unmapped_keys:
            print(f"Warning: Unmapped biomarker keys: {unmapped_keys}")
        
        # Enforce canonical-only keys in the final panel
        non_canonical = self.normalizer.validate_canonical_only(biomarker_panel.biomarkers)
        if non_canonical:
            raise ValueError(
                f"Non-canonical biomarker keys found after normalization: {non_canonical}. "
                "All biomarkers must use canonical names only."
            )
        
        # Create user object
        user = self.context_factory.create_user_from_dict(user_data)
        
        # Create analysis context
        context = self.context_factory.create_context(
            analysis_id=analysis_id,
            user=user,
            biomarker_panel=biomarker_panel
        )
        
        return context
    
    def validate_biomarker_panel(self, biomarkers: Dict[str, Any]) -> List[str]:
        """
        Validate that all biomarker keys are canonical.
        
        Args:
            biomarkers: Biomarker data to validate
            
        Returns:
            List of non-canonical keys found
        """
        return self.normalizer.validate_canonical_only(biomarkers)
    
    def get_canonical_biomarkers(self) -> List[str]:
        """
        Get list of all canonical biomarker names.
        
        Returns:
            List of canonical biomarker names
        """
        return self.normalizer.get_canonical_biomarkers()
    
    def _assert_canonical_only(self, raw_map: Mapping[str, Any], *, where: str = "pre-context") -> None:
        """Raise if any biomarker keys are not already canonical.
        We resolve each key; if resolution changes the name, it was an alias.
        """
        offenders = []
        for k in raw_map.keys():
            canonical = resolve_to_canonical(k)
            if canonical != k:
                offenders.append(k)
        if offenders:
            offenders.sort()
            raise ValueError(f"Non-canonical biomarker keys found: {', '.join(offenders)}")

    def run(self, biomarkers: Mapping[str, Any], user: Mapping[str, Any], *, assume_canonical: bool = False):
        if not assume_canonical:
            self._assert_canonical_only(biomarkers, where="run")
        
        canonical_map = dict(biomarkers)

        # continue with existing scoring → clustering → insights using `canonical_map`
        # For now, return a stub result
        from core.models.results import AnalysisDTO
        return AnalysisDTO(
            analysis_id="stub_analysis_id",
            clusters=[],
            insights=[],
            status="complete",
            created_at="2024-01-01T00:00:00Z"
        )
