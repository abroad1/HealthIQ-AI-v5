# Sprint 5 Targeted Evidence Extraction (Read-Only)

**Authority:** docs/README_V5.2_BASELINE.md, Master_PRD_v5.2.md §3.2, §3.4, §5, Delivery_Sprint_Plan_v5.2.md Sprint 5 DoD

---

## PART 1 — Persistence Snapshot Contract

### 1.1 AnalysisResult (SQLAlchemy database model)

**File path:** `backend/core/models/database.py`  
**Line range:** 139–178

```python
class AnalysisResult(Base):
    """Analysis results model."""
    __tablename__ = "analysis_results"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), 
                        nullable=False, unique=True, index=True)
    
    # Result data
    biomarkers = Column(JSON, nullable=True)
    clusters = Column(JSON, nullable=True)
    insights = Column(JSON, nullable=True)
    overall_score = Column(Float, nullable=True)
    risk_assessment = Column(JSON, nullable=True)
    recommendations = Column(ARRAY(Text), nullable=True)
    
    # Metadata
    result_version = Column(String(50), nullable=False, default="1.0.0", index=True)
    confidence_score = Column(Float, nullable=True)
    processing_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="result")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("overall_score >= 0 AND overall_score <= 1", name="ck_analysis_results_score_range"),
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 1", name="ck_analysis_results_confidence_range"),
        CheckConstraint("result_version ~ '^\\d+\\.\\d+\\.\\d+$'", name="ck_analysis_results_version_format"),
        Index("idx_analysis_results_analysis_id", "analysis_id"),
        Index("idx_analysis_results_overall_score", "overall_score"),
        Index("idx_analysis_results_created_at", "created_at"),
    )
```

**Short explanation:** The SQLAlchemy model has no top-level `derived_markers` column. It uses `processing_metadata` (JSON) for extra metadata.

---

### 1.2 create_analysis_result (full method)

**File path:** `backend/services/storage/persistence_service.py`  
**Line range:** 455–546

```python
    def create_analysis_result(self, analysis_id: UUID, dto: AnalysisResultDTO) -> bool:
        """
        Create or upsert analysis_results record with idempotence.
        """
        try:
            from datetime import datetime, timezone
            
            # Prepare payload using only valid AnalysisResult fields
            result_payload = {
                "analysis_id": str(analysis_id),
                "biomarkers": dto.biomarkers,
                "clusters": getattr(dto, "clusters", []),
                "insights": getattr(dto, "insights", []),
                "overall_score": getattr(dto, "overall_score", 0.0),
                "risk_assessment": getattr(dto, "risk_assessment", {}) or {},
                "recommendations": getattr(dto, "recommendations", []) or [],
                "context": getattr(dto, "context", {}),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "result_version": getattr(dto, "result_version", "1.0.0"),
                "processing_time_seconds": getattr(dto, "processing_time_seconds", None)
            }
            
            # Remove deprecated or disallowed fields if present
            result_payload.pop("confidence_score", None)
            result_payload.pop("processing_metadata", None)
            
            # Convert to dict format for database persistence
            derived_markers = getattr(dto, "derived_markers", None)
            result_data = {
                "biomarkers": [b.model_dump() if hasattr(b, 'model_dump') else b for b in result_payload["biomarkers"]] if result_payload["biomarkers"] else [],
                "clusters": [c.model_dump() if hasattr(c, 'model_dump') else c for c in result_payload["clusters"]] if result_payload["clusters"] else [],
                "insights": [i.model_dump() if hasattr(i, 'model_dump') else i for i in result_payload["insights"]] if result_payload["insights"] else [],
                "overall_score": result_payload["overall_score"],
                "risk_assessment": result_payload["risk_assessment"],
                "recommendations": result_payload["recommendations"],
                "result_version": result_payload["result_version"]
            }
            if derived_markers is not None:
                result_data["processing_metadata"] = {
                    **(result_payload.get("processing_metadata") or {}),
                    "derived_markers": derived_markers,
                }
            
            # Use upsert to ensure idempotence
            analysis_result = self.analysis_result_repo.upsert_by_analysis_id(analysis_id, **result_data)
            # ... (rest of method: biomarker scores, clusters, insights persistence)
```

**Exact payload written to persistence (result_data passed to upsert_by_analysis_id):**
```
{
  "biomarkers": [...],      // list of dicts
  "clusters": [...],        // list of dicts
  "insights": [...],        // list of dicts
  "overall_score": float,
  "risk_assessment": dict,
  "recommendations": list,
  "result_version": str
}
```
When `derived_markers` is present:
```
{
  ...,
  "processing_metadata": {
    "derived_markers": { ... }  // includes registry_version and derived ratios
  }
}
```

**processing_metadata structure:** `{"derived_markers": <dto.derived_markers>}` when `derived_markers` is present. Merged with `result_payload.get("processing_metadata") or {}` (typically empty since processing_metadata is popped).

**derived_markers:** (b) nested inside `processing_metadata`, not a top-level DB column. Persisted only when `dto.derived_markers` is not None.

**registry_version:** Stored implicitly inside `derived_markers`, which is persisted under `processing_metadata["derived_markers"]`. No separate top-level field.

---

### 1.3 get_analysis_result (full method)

**File path:** `backend/services/storage/persistence_service.py`  
**Line range:** 353–421

```python
    @fallback_decorator("get_analysis_result")
    def get_analysis_result(self, analysis_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get analysis result from database.
        """
        try:
            analysis = self.analysis_repo.get_by_id(analysis_id)
            if not analysis:
                return None
            
            result = self.analysis_result_repo.get_by_analysis_id(analysis_id)
            if not result:
                return None
            
            # Get biomarker scores
            biomarker_scores = self.biomarker_score_repo.list_by_analysis_id(analysis_id)
            biomarkers = []
            for score in biomarker_scores:
                biomarkers.append({
                    "biomarker_name": score.biomarker_name,
                    "value": score.value,
                    "unit": score.unit,
                    "score": score.score,
                    "percentile": score.percentile,
                    "status": score.status,
                    "reference_range": score.reference_range,
                    "interpretation": score.interpretation
                })
            
            # Get clusters
            clusters = self.cluster_repo.list_by_analysis_id(analysis_id)
            cluster_list = []
            for cluster in clusters:
                cluster_list.append({
                    "cluster_id": str(cluster.id),
                    "name": cluster.cluster_name,
                    "biomarkers": cluster.biomarkers or [],
                    "description": cluster.description,
                    "severity": cluster.severity,
                    "confidence": cluster.confidence
                })
            
            # Get insights
            insights = self.insight_repo.list_by_analysis_id(analysis_id)
            insight_list = []
            for insight in insights:
                insight_list.append({
                    "id": str(insight.id),
                    "title": insight.title,
                    "description": insight.content,
                    "category": insight.category,
                    "confidence": insight.confidence,
                    "severity": insight.severity,
                    "biomarkers": insight.biomarkers_involved or [],
                    "recommendations": insight.recommendations or []
                })
            
            derived_markers = None
            if isinstance(result.processing_metadata, dict) and "derived_markers" in result.processing_metadata:
                derived_markers = result.processing_metadata["derived_markers"]

            return {
                "analysis_id": str(analysis_id),
                "result_version": result.result_version,
                "biomarkers": biomarkers,
                "clusters": cluster_list,
                "insights": insight_list,
                "recommendations": result.recommendations or [],
                "overall_score": result.overall_score,
                "derived_markers": derived_markers,
                "meta": {
                    "confidence_score": result.confidence_score,
                    "processing_metadata": result.processing_metadata
                },
                "created_at": result.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting analysis result for {analysis_id}: {str(e)}")
            return None
```

**Payload shape returned:**
```json
{
  "analysis_id": "uuid",
  "result_version": "1.0.0",
  "biomarkers": [...],
  "clusters": [...],
  "insights": [...],
  "recommendations": [...],
  "overall_score": float,
  "derived_markers": { ... } | null,
  "meta": {
    "confidence_score": float,
    "processing_metadata": { ... }
  },
  "created_at": "iso8601"
}
```

**derived_markers:** Read from `result.processing_metadata["derived_markers"]` and exposed as a top-level key in the returned dict.

**registry_version:** Contained within `derived_markers` when present; not stored as its own field.

---

## PART 2 — Orchestrator Unit Normalisation Invariant

### 2.1 run() signature and first 60 lines

**File path:** `backend/core/pipeline/orchestrator.py`  
**Line range:** 612–689

```python
    def run(self, biomarkers: Mapping[str, Any], user: Mapping[str, Any], *, assume_canonical: bool = False):
        """
        Run the complete analysis pipeline: scoring → clustering → insights.
        
        Args:
            biomarkers: Canonical biomarker data
            user: User data
            assume_canonical: Whether to skip canonical validation
            
        Returns:
            AnalysisDTO with complete analysis results
        """
        import logging
        import uuid
        from datetime import datetime, UTC
        from core.models.results import AnalysisDTO, BiomarkerScore as BiomarkerScoreDTO, ClusterHit, InsightResult
        
        logger = logging.getLogger(__name__)
        
        try:
            if not assume_canonical:
                self._assert_canonical_only(biomarkers, where="run")
            
            # Initialize canonical resolver for units and reference ranges
            resolver = CanonicalResolver()
            
            # Generate unique analysis ID
            analysis_id = str(uuid.uuid4())
            logger.info(f"Starting analysis {analysis_id} with {len(biomarkers)} biomarkers")
            
            # Trace biomarkers received by orchestrator
            print("[TRACE] Orchestrator input biomarkers:", list(biomarkers.keys()))
            
            # Quarantine unmapped biomarkers before downstream processing
            unmapped_biomarkers = []
            filtered_biomarkers = {}
            alias_service = self.normalizer.alias_service
            for key, value in biomarkers.items():
                if key.startswith("unmapped_"):
                    unmapped_biomarkers.append(key)
                    continue
                resolved = alias_service.resolve(key)
                if resolved.startswith("unmapped_"):
                    unmapped_biomarkers.append(resolved)
                    continue
                filtered_biomarkers[key] = value
            unmapped_biomarkers = sorted(set(unmapped_biomarkers))
            skipped_unmapped = len(biomarkers) - len(filtered_biomarkers)
            logger.info(
                "Biomarker quarantine: total=%s, canonical=%s, unmapped_skipped=%s",
                len(biomarkers),
                len(filtered_biomarkers),
                skipped_unmapped,
            )

            # Step 1: Convert biomarkers to simple format for scoring engine and preserve reference ranges
            logger.info("Step 1: Converting biomarkers for scoring")
            simple_biomarkers = {}
            input_reference_ranges = {}
            for biomarker_name, biomarker_data in filtered_biomarkers.items():
                if isinstance(biomarker_data, dict):
                    simple_biomarkers[biomarker_name] = biomarker_data.get('value', biomarker_data.get('measurement', 0))
                    # ... reference range extraction ...
```

**Internal calls to apply_unit_normalisation / normalize_biomarkers_with_metadata / unit registry:** None. The orchestrator does not call `apply_unit_normalisation` or `normalize_biomarkers_with_metadata` inside `run()`.

---

### 2.2 RatioRegistry.compute call site

**File path:** `backend/core/pipeline/orchestrator.py`  
**Line range:** 666–692

```python
            # Step 1: Convert biomarkers to simple format for scoring engine and preserve reference ranges
            logger.info("Step 1: Converting biomarkers for scoring")
            simple_biomarkers = {}
            input_reference_ranges = {}  # Preserve reference ranges from input
            for biomarker_name, biomarker_data in filtered_biomarkers.items():
                if isinstance(biomarker_data, dict):
                    simple_biomarkers[biomarker_name] = biomarker_data.get('value', biomarker_data.get('measurement', 0))
                    # ... ref range extraction ...
                else:
                    simple_biomarkers[biomarker_name] = biomarker_data

            # Step 1.5: Compute derived markers (RatioRegistry; lab-supplied wins; never overwrite)
            logger.info("Step 1.5: Computing derived markers")
            derived_result = compute(simple_biomarkers)
```

**Object passed into compute():** `simple_biomarkers` — a `Dict[str, float]` built from `filtered_biomarkers` by taking `value` or `measurement` (or raw value). No internal unit normalisation in the orchestrator; unit normalisation is expected on the input `biomarkers` before `run()`.

---

### 2.3 Analysis route (entry point) unit normalisation order

**File path:** `backend/app/routes/analysis.py`  
**Line range:** 89–109

```python
        # Normalize incoming raw biomarkers to canonical form, preserving reference_range metadata
        normalized = normalize_biomarkers_with_metadata(request.biomarkers)

        # Sprint 1: Convert to base units at ingestion (Layer A). Deterministic; rejects unknown units.
        try:
            normalized = apply_unit_normalisation(normalized)
        except UnitConversionError as e:
            # ...

        # Create orchestrator and run analysis
        orchestrator = AnalysisOrchestrator()
        dto = orchestrator.run(normalized, request.user, assume_canonical=True)
```

**Order:** `normalize_biomarkers_with_metadata` → `apply_unit_normalisation` → `orchestrator.run(normalized, ...)`. Unit normalisation is done before `run()` in the analysis route. The orchestrator receives unit-normalised data and passes it through to `compute()`.

---

## PART 3 — Entry Point Inventory (runtime only, tests excluded)

| File | Line | Snippet |
|------|------|---------|
| `backend/app/routes/analysis.py` | 109 | `dto = orchestrator.run(normalized, request.user, assume_canonical=True)` |
| `backend/core/pipeline/orchestrator.py` | 692 | `derived_result = compute(simple_biomarkers)` |

**Note:** `compute` is defined in `backend/core/analytics/ratio_registry.py` at line 70. The only runtime caller is `orchestrator.py` line 692. The only runtime caller of `orchestrator.run()` is `backend/app/routes/analysis.py` line 109.
