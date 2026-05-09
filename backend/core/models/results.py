"""
Analysis results models - immutable Pydantic v2 models for analysis results.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field

from core.contracts.retail_explainer_v1 import (
    BiomarkerEducationalExplainerV1,
    ContributionContextV1,
    SystemEducationalExplainerV1,
)
from core.models.biomarker import BiomarkerCluster, BiomarkerInsight
from core.models.context import AnalysisContext
from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayLayerBundleV1
from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.narrative_report_v1 import NarrativeReportV1


class BiomarkerScore(BaseModel):
    """Immutable biomarker scoring result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    biomarker_name: str = Field(..., description="Canonical biomarker name")
    value: Any = Field(..., description="Biomarker value")
    unit: str = Field(default="", description="Unit of measurement")
    score: float = Field(..., description="Normalized score (0-1)")
    percentile: Optional[float] = Field(default=None, description="Population percentile")
    status: str = Field(..., description="Status (normal, elevated, low, etc.)")
    range_source: Optional[str] = Field(
        default=None,
        description="Range provenance: lab | policy | ssot"
    )
    reference_range: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Reference range information"
    )
    reference_profile: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional lab reference profile (bands, effective date, note)"
    )
    lab_band_label: Optional[str] = Field(
        default=None,
        description="Band label matched from reference_profile.bands when deterministically classifiable"
    )
    interpretation: str = Field(
        default="",
        description="Engine/lab mechanics interpretation — not retail educational explainer text",
    )
    biomarker_educational_explainer: Optional[BiomarkerEducationalExplainerV1] = Field(
        default=None,
        description="FE-VISUALISATION-B1A: reusable educational copy; separate from interpretation",
    )
    contribution_context: Optional[ContributionContextV1] = Field(
        default=None,
        description="FE-VISUALISATION-B1A: bounded factual grouping context (e.g. cluster membership)",
    )


class AnalysisResult(BaseModel):
    """Immutable analysis result containing clusters and insights."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    context: AnalysisContext = Field(..., description="Analysis context")
    biomarkers: List[BiomarkerScore] = Field(
        default_factory=list, 
        description="Individual biomarker results with scores and status"
    )
    clusters: List[BiomarkerCluster] = Field(
        default_factory=list, 
        description="Biomarker clusters"
    )
    insights: List[BiomarkerInsight] = Field(
        default_factory=list, 
        description="Generated insights"
    )
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
    risk_assessment: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Risk assessment results"
    )
    recommendations: List[str] = Field(
        default_factory=list, 
        description="General recommendations"
    )
    created_at: str = Field(..., description="Result creation timestamp")
    result_version: str = Field(default="1.0.0", description="Result schema version for DTO parity")
    processing_time_seconds: Optional[float] = Field(
        default=None, 
        description="Total processing time"
    )
    derived_markers: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Derived/ratio markers (registry_version + derived dict) for replay determinism"
    )
    replay_manifest: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Sprint 9: ReplayManifestV1 for determinism/replay"
    )


class AnalysisSummary(BaseModel):
    """Immutable analysis summary for quick overview."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    user_id: str = Field(..., description="User identifier")
    status: str = Field(..., description="Analysis status")
    total_biomarkers: int = Field(default=0, description="Number of biomarkers analyzed")
    clusters_found: int = Field(default=0, description="Number of clusters identified")
    insights_generated: int = Field(default=0, description="Number of insights generated")
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
    created_at: str = Field(..., description="Analysis creation timestamp")
    completed_at: Optional[str] = Field(default=None, description="Analysis completion timestamp")


class ClusterHit(BaseModel):
    """Immutable cluster hit result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    cluster_id: str = Field(..., description="Cluster identifier")
    name: str = Field(..., description="Cluster name")
    biomarkers: List[str] = Field(default_factory=list, description="Biomarkers in cluster")
    confidence: float = Field(..., description="Confidence score (0-1)")
    severity: str = Field(..., description="Severity level")
    description: str = Field(default="", description="Cluster description")
    system_educational_explainer: Optional[SystemEducationalExplainerV1] = Field(
        default=None,
        description="FE-VISUALISATION-B1A: reusable body-system education; not personalised proof",
    )


class InsightResult(BaseModel):
    """Immutable insight result with provenance tracking."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    # Core insight data
    insight_id: str = Field(..., description="Insight identifier")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    category: str = Field(..., description="Insight category (maintained for frontend compatibility)")
    confidence: float = Field(..., description="Confidence score (0-1)")
    severity: str = Field(..., description="Severity level")
    biomarkers: List[str] = Field(default_factory=list, description="Related biomarkers")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    
    # Provenance fields (Sprint 9c)
    version: str = Field(default="v1.0.0", description="Insight version")
    manifest_id: str = Field(default="legacy_v1", description="Manifest identifier")
    experiment_id: Optional[str] = Field(default=None, description="Experiment identifier")
    drivers: Optional[Dict[str, Any]] = Field(default=None, description="Insight drivers")
    evidence: Optional[Dict[str, Any]] = Field(default=None, description="Supporting evidence")
    error_code: Optional[str] = Field(default=None, description="Error code if failed")
    error_detail: Optional[str] = Field(default=None, description="Error details if failed")
    latency_ms: int = Field(default=0, description="Processing latency in milliseconds")


ConfidenceTierV1 = Literal["high", "medium", "low"]


class ConsumerDomainScoreV1(BaseModel):
    """
    Wave 1 — deterministic customer domain translation (Strategy A).
    D-1: score + band + confidence + raw references.
    D-2: consumer narrative sentences (retail only; not injected into clinician surfaces).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    domain_id: str = Field(
        ...,
        description="Stable id, e.g. wave1_cardiovascular / wave1_blood_sugar / wave1_liver",
    )
    card_schema_version: str = Field(
        default="1.0",
        description="Wave 1 card contract version: 1.0 legacy, 1.1 D-6 single-authority + aligned drivers",
    )
    consumer_label: str = Field(..., description="Consumer-facing domain label (dashboard copy)")
    clinical_label: str = Field(..., description="Clinician-oriented label; does not replace clinician report elsewhere")
    score: float = Field(..., ge=0.0, le=1.0, description="0–1 domain score (deterministic mapping from base rails)")
    band_label: str = Field(
        ...,
        description="Coarse band: strong | stable | watch | review (0–100 rail mapping, pre-normalisation buckets)",
    )
    confidence_tier: ConfidenceTierV1 = Field(
        ...,
        description="Domain confidence; emitted together with score (no score-without-confidence)",
    )
    active_signal_ids: List[str] = Field(default_factory=list, description="Active governed signals in this domain")
    primary_idl_record_id: Optional[str] = Field(
        default=None,
        description="Primary Wave-1 IDL ph_* id for narrative assembly, if any",
    )
    missing_marker_ids: List[str] = Field(
        default_factory=list,
        description="Scoring-rail and domain-pool markers still missing (canonical ids)",
    )
    source_track: str = Field(
        ...,
        description="Calibration provenance, e.g. base:scoring_rail:cardiovascular; no silent track mixing",
    )
    caveat_flags: List[str] = Field(
        default_factory=list,
        description="Truthfulness / scope flags (e.g. liver enzyme_limited_assessment)",
    )
    contributing_system_keys: List[str] = Field(
        default_factory=list,
        description="Scoring or burden system keys that contributed to evidence (e.g. cardiovascular, hepatic)",
    )
    raw_evidence_refs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured refs for D-2 narrative (Layer3 card ids, burden keys, IDL list)",
    )
    headline_sentence: str = Field(
        default="",
        description="D-2: score-band consumer headline; assembled from D-1 band + domain copy tables",
    )
    contributor_sentence: str = Field(
        default="",
        description="D-2: deterministic contributor line (IDL subtitle / signal priority / fallbacks)",
    )
    confidence_sentence: str = Field(
        default="",
        description="D-2: copy derived from D-1 confidence tier + coverage; no second confidence model",
    )
    consequence_sentence: str = Field(
        default="",
        description="D-2: primarily IDL why_it_matters or governed idl_registry text; CV lipid path routed in D-2",
    )
    next_step_sentence: str = Field(
        default="",
        description="D-2: follow-up from insights recommendations or narrative next_steps, else generic",
    )
    evidence_anchor_sentence: str = Field(
        default="",
        description="D-4: compact based-on / traceability line for the collapsed card (IDL retail label or safe fallback)",
    )


class AnalysisDTO(BaseModel):
    """Immutable analysis data transfer object."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    biomarkers: List[BiomarkerScore] = Field(default_factory=list, description="Biomarker results")
    clusters: List[ClusterHit] = Field(default_factory=list, description="Cluster hits")
    insights: List[InsightResult] = Field(default_factory=list, description="Insight results")
    status: str = Field(..., description="Analysis status")
    created_at: str = Field(..., description="Creation timestamp")
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
    primary_driver_system_id: str = Field(
        default="",
        description="Single-authority primary driver from final arbitration/explainability",
    )
    system_capacity_scores: Dict[str, int] = Field(
        default_factory=dict,
        description="Deterministic system capacity scores from burden engine",
    )
    burden_hash: str = Field(
        default="",
        description="Deterministic hash of adjusted burden + capacity vectors",
    )
    unmapped_biomarkers: List[str] = Field(
        default_factory=list,
        description="Unrecognised biomarkers excluded from analysis"
    )
    derived_markers: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Derived/ratio markers (registry_version + derived dict with provenance)"
    )
    meta: Optional[Dict[str, Any]] = Field(default=None, description="Analysis meta (criticality, etc.)")
    replay_manifest: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Sprint 9: ReplayManifestV1 for determinism/replay (version stamps + schema hashes)"
    )
    lifestyle: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Sprint 20: Lifestyle modifier artifact (derived_inputs, system_modifiers, confidence_adjustments) when lifestyle_inputs provided",
    )
    interpretation_display_layer_v1: Optional[InterpretationDisplayLayerBundleV1] = Field(
        default=None,
        description="BE-IDL-1: governed interpretation display bundle for Section 5 pattern cards",
    )
    narrative_report_v1: Optional[NarrativeReportV1] = Field(
        default=None,
        description="N-8: deterministic compiled narrative sections (governed asset assembly, no LLM)",
    )
    consumer_domain_scores: Optional[List[ConsumerDomainScoreV1]] = Field(
        default=None,
        description="D-1: Wave1 domain scores + confidence (backend contract; not wired to product shell in D-1)",
    )
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = Field(
        default=None,
        description="LC-S2+: Layer B intervention annotations (parallel; no signal/ranking mutation)",
    )
