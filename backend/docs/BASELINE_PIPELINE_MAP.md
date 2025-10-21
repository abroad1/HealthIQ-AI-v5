# Baseline Pipeline Map - HealthIQ-AI v5

**Sprint 0 - Pre-Canonization Baseline Documentation**

This document maps the current v5 pipeline flow from upload to analysis results, serving as the baseline for the Canonization & Validation Refactor.

## Pipeline Overview

The HealthIQ-AI v5 system processes biomarker data through the following stages:

```
Upload → Parse → Normalize → Orchestrator → Score → Insights → DTO → Frontend
```

## Detailed Pipeline Flow

### Stage 1: Upload (Frontend)
**File:** `frontend/app/upload/page.tsx`
**Key Functions:**
- `handleFileUpload()` - Processes file uploads via FileDropzone
- `handleTextPaste()` - Processes text input via PasteInput
- `handleParsedData()` - Handles fixture mode data loading

**Entry Points:**
- File upload (PDF, TXT, CSV, JSON)
- Text paste input
- Fixture mode (`?fixture=true`)

### Stage 2: Parse (Backend)
**File:** `backend/app/routes/upload.py`
**Key Functions:**
- `parse_upload()` - Main parsing endpoint
- Uses `LLMParser` service for biomarker extraction

**Process:**
1. Receives file or text content
2. Generates analysis ID
3. Calls `LLMParser` for biomarker extraction
4. Returns parsed data with confidence scores

### Stage 3: Normalize (Backend)
**File:** `backend/core/canonical/normalize.py`
**Key Functions:**
- `BiomarkerNormalizer.normalize_biomarkers()`
- `normalize_panel()` - Convenience function

**Process:**
1. Maps aliases to canonical names using `BiomarkerAliasResolver`
2. Builds `BiomarkerPanel` with canonical keys only
3. Returns unmapped keys for logging

**Current Implementation:**
- Uses `backend/core/canonical/alias_registry.py` for alias resolution
- Integrates with v4 alias resolver for comprehensive mapping
- Enforces canonical-only keys in downstream processing

### Stage 4: Orchestrator (Backend)
**File:** `backend/core/pipeline/orchestrator.py`
**Key Functions:**
- `AnalysisOrchestrator.create_analysis_context()`
- `AnalysisOrchestrator.run_analysis()`

**Process:**
1. Creates `AnalysisContext` from raw data
2. Validates data completeness and gaps
3. Runs scoring engine
4. Generates insights and recommendations
5. Performs clustering analysis
6. Synthesizes final results

**Components:**
- `AnalysisContextFactory` - Context creation
- `DataCompletenessValidator` - Data validation
- `BiomarkerGapAnalyzer` - Gap analysis
- `RecommendationEngine` - Recommendation generation
- `ScoringEngine` - Biomarker scoring
- `ClusteringEngine` - Biomarker clustering
- `InsightSynthesizer` - Insight generation

### Stage 5: Score (Backend)
**File:** `backend/core/scoring/engine.py`
**Key Functions:**
- `ScoringEngine.score_biomarkers()`
- `ScoringEngine.score_health_systems()`

**Process:**
1. Scores individual biomarkers (0-100 scale)
2. Aggregates scores by health system
3. Applies lifestyle overlays
4. Calculates confidence levels
5. Generates recommendations

### Stage 6: Insights (Backend)
**File:** `backend/core/insights/synthesis.py`
**Key Functions:**
- `InsightSynthesizer.synthesize_insights()`

**Process:**
1. Analyzes biomarker patterns
2. Identifies health trends
3. Generates actionable insights
4. Creates recommendation priorities

### Stage 7: DTO (Backend)
**File:** `backend/core/dto/builders.py`
**Key Functions:**
- `build_analysis_result_dto()`
- `build_biomarker_score_dto()`

**Process:**
1. Transforms internal objects to frontend-safe dictionaries
2. Ensures proper data serialization
3. Adds metadata and versioning

### Stage 8: Frontend Display
**File:** `frontend/app/results/page.tsx`
**Key Functions:**
- Results visualization and display
- Interactive biomarker exploration
- Recommendation presentation

## Key Modules and Dependencies

### Core Canonicalization Chain
1. `backend/core/canonical/alias_registry.py` - Alias resolution
2. `backend/core/canonical/normalize.py` - Biomarker normalization
3. `backend/core/canonical/resolver.py` - Canonical name resolution

### Pipeline Orchestration
1. `backend/core/pipeline/orchestrator.py` - Main orchestration
2. `backend/core/pipeline/context_factory.py` - Context creation
3. `backend/core/pipeline/events.py` - Event streaming

### Analysis Components
1. `backend/core/scoring/engine.py` - Scoring engine
2. `backend/core/validation/completeness.py` - Data validation
3. `backend/core/clustering/engine.py` - Clustering analysis
4. `backend/core/insights/synthesis.py` - Insight generation

### API Endpoints
1. `backend/app/routes/upload.py` - Upload and parsing
2. `backend/app/routes/analysis.py` - Analysis orchestration
3. `backend/app/routes/health.py` - Health checks

## Trace Statements and Logging

### Current Trace Points
- `[INIT] Running HealthIQ-AI in fixture-only mode` - Startup
- `[TRACE] Created AnalysisContext` - Context creation
- `[TRACE] DTO biomarkers in result: {count}` - DTO building
- `[TRACE] Normalized {count} biomarkers` - Normalization
- `[TRACE] Unmapped keys: {keys}` - Alias resolution

### Logging Levels
- **INFO**: General flow progression
- **TRACE**: Detailed processing steps
- **WARN**: Unmapped biomarkers or validation issues
- **ERROR**: Processing failures

## Current Limitations and Gaps

### Identified Issues
1. **Ad-hoc Normalization**: Current normalization lacks comprehensive alias coverage
2. **Limited Validation**: Minimal input validation before processing
3. **No Context Factory**: Missing structured context creation
4. **Incomplete Error Handling**: Limited graceful error recovery
5. **No Frontend Validation**: Client-side validation missing

### Performance Considerations
- Alias resolution happens on every request
- No caching of canonical mappings
- Limited parallel processing capabilities

## Test Run Results (Sprint 0)

*[Test results will be appended after running the test suite]*

## Next Steps for Sprint 1

1. **Implement Canonical Alias Registry**: Replace ad-hoc normalization
2. **Add Context Factory**: Structured data validation
3. **Enhance Error Handling**: Graceful failure recovery
4. **Add Frontend Validation**: Client-side alias resolution
5. **Performance Optimization**: Caching and parallel processing

---

**Document Version:** 1.0  
**Created:** Sprint 0 - Preparation & Baseline  
**Last Updated:** Sprint 0 - Preparation & Baseline  
**Status:** Pre-Canonization Baseline
