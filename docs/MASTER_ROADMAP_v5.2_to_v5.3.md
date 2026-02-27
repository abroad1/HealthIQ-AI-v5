# HealthIQ AI — Master Roadmap (v5.2 → v5.3)

## 1. Executive Positioning

HealthIQ AI v5.2 is the deterministic biological substrate completion phase. Its purpose is to establish computation discipline: strict Layer B/Layer C boundary, versioned analytical assets, replayability, deterministic contracts, and enforceable safety constraints around raw biomarker leakage.  
HealthIQ AI v5.3 is the biological intelligence expansion phase. Its purpose is to increase inference depth: richer multi-marker interpretation, conflict handling, longitudinal state understanding, and outcome-grounded calibration while preserving deterministic execution and replay integrity.

v5.2 builds computation discipline.  
v5.3 builds inference depth.

## 2. v5.2 — Deterministic Substrate Completion

### 2.1 Completed (Reference Existing Contracts)

- InsightGraph_v1: establishes the deterministic structured handshake from Layer B to Layer C and prevents narrative-layer computation.
- ReplayManifest_v1: stamps core analytical asset versions and schema hashes to support deterministic replay and auditability.
- ConfidenceModel_v1: provides deterministic confidence and missing-data visibility as explicit structured outputs.
- RelationshipRegistry_v1: introduces schema-driven, versioned, deterministic relationship detection for pairwise biomarker patterns.
- BiomarkerContext_v1: adds code-only explanatory context per biomarker without exposing raw values or units.
- RatioRegistry: centralizes derived marker computation with deterministic provenance and no local ratio recomputation requirement.
- Cluster schema: moves cluster membership definitions into SSOT and validates against canonical biomarker IDs.
- LLM boundary enforcement: integration and enforcement tests verify no raw biomarker values, units, or ranges pass into prompt payloads.

### 2.2 Remaining Mandatory 5.2 Work

1. Runtime unification (single clustering engine path)  
   What it is: a single production clustering execution path with no ambiguity between active and inactive engines.  
   Why it matters: operational clarity and audit traceability require one runtime truth for clustering behavior.  
   Business impact: reduces explainability friction in enterprise, regulatory, and diligence conversations.  
   Risk if skipped: ongoing governance ambiguity and higher maintenance risk from parallel, partially overlapping clustering logic.

2. SSOT migration for scoring thresholds  
   What it is: move remaining hardcoded scoring thresholds and scoring policy constants into versioned SSOT artifacts.  
   Why it matters: full policy traceability requires scoring logic to be declarative, versioned, and centrally governed.  
   Business impact: improves reviewability and accelerates policy updates without hidden code-level drift.  
   Risk if skipped: policy changes remain harder to audit, and threshold drift risk persists across code paths.

3. Deterministic signal arbitration layer  
   What it is: explicit deterministic precedence rules when multiple deterministic signals disagree or overlap.  
   Why it matters: as registries grow, conflict resolution must be explicit to keep outputs stable and explainable.  
   Business impact: higher consistency in insights, fewer contradictory narratives, stronger clinician trust.  
   Risk if skipped: emergent inconsistency as rule volume increases, weakening confidence in engine coherence.

4. Evidence provenance registry scaffold  
   What it is: documentation and metadata scaffold to attach sources, rationale, and review ownership to inference assets.  
   Why it matters: deterministic logic is necessary but insufficient for medical credibility without provenance.  
   Business impact: strengthens clinical defensibility and partner confidence in the inference corpus.  
   Risk if skipped: weaker credibility under clinical and regulatory scrutiny despite good technical architecture.

5. Deterministic failure manifest  
   What it is: standard deterministic failure artifact for failed analyses with stable error taxonomy and replay context.  
   Why it matters: replay integrity must include failure cases, not only successful runs.  
   Business impact: improves support, incident triage, and enterprise reliability posture.  
   Risk if skipped: non-uniform failure outputs reduce reproducibility and complicate operational governance.

6. Documentation governance alignment  
   What it is: synchronize baseline docs so execution state, priorities, and authority markers are consistent.  
   Why it matters: stale sprint markers create execution drift even when runtime architecture is sound.  
   Business impact: faster decision-making and cleaner executive/engineering alignment.  
   Risk if skipped: repeated mis-sequencing, onboarding confusion, and reduced execution quality.

## 3. v5.3 — Biological Intelligence Expansion

### 3.1 Multi-Marker State Engine

v5.3 introduces deterministic state interpretation across biomarker groups, not just isolated threshold outcomes. The objective is to model biologically meaningful state signatures from combinations of markers and derived signals. This shifts value from rule hygiene to inference richness while preserving replayability and contract boundaries.

### 3.2 Deterministic Conflict Modelling

v5.3 formalizes conflict handling when signals disagree (for example, discordant marker and relationship evidence). The objective is explicit deterministic arbitration with stable rationale codes. This increases interpretive consistency and prevents narrative contradictions as inference density grows.

### 3.3 Longitudinal State Transitions

v5.3 expands from single-snapshot interpretation to deterministic transition interpretation across snapshots. The objective is structured detection of directional, stability, and transition patterns without introducing non-deterministic logic. This creates materially deeper biological intelligence than static status interpretation.

### 3.4 Outcome Calibration Layer

v5.3 adds deterministic calibration scaffolding that links inference behavior to measurable outcome alignment over time. The objective is to convert inference quality from subjective plausibility to measurable system performance. This strengthens clinical trust and strategic defensibility.

## 4. Moat & Defensibility Narrative

Architecture discipline alone is necessary but not sufficient for defensibility; deterministic pipelines can be replicated if inference behavior remains shallow. Proprietary inference behavior is defensible because it accumulates through structured rule interaction, conflict policy, longitudinal state logic, and calibrated outcome alignment. Replay determinism supports regulatory credibility by enabling exact reconstruction, auditability, and controlled evolution of inference assets. Longitudinal modelling supports valuation because it moves the product from static report interpretation to a compounding intelligence system with increasing decision quality over time.

## 5. Execution Order

- Phase A — Finish 5.2 hardening: complete runtime unification, SSOT scoring migration, deterministic signal arbitration, deterministic failure manifest, provenance scaffold, and documentation alignment.
- Phase B — Begin 5.3 modelling layer: establish multi-marker state reasoning and deterministic conflict modelling as first-order inference capabilities.
- Phase C — Longitudinal + outcomes: expand into state transitions and outcome calibration to create durable technical and commercial moat.
