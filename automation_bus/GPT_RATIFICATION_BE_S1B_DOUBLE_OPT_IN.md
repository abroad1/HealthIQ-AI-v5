# GPT architectural ratification — BE-S1B narrative runtime policy

**Evidence type:** governance / architecture (not implementation scope expansion)  
**Recorded:** 2026-04-09  

## Ratified design

GPT explicitly approved the **BE-S1B governed runtime policy** for Layer C insight narrative (`insights[]`) using a **double opt-in**:

1. **`HEALTHIQ_ENABLE_LLM`** — network LLM enablement (existing operator gate; also used inside `InsightSynthesizer._create_llm_client`).
2. **`HEALTHIQ_NARRATIVE_LLM`** — narrative-specific production master switch read in `backend/core/insights/narrative_runtime_policy.py` for the default `AnalysisOrchestrator()` / HTTP path (`allow_llm=None`).

## What this approval means

- The **design is approved** as the governed production posture (no accidental single-env activation for API defaults).
- **No further code change is required** solely to ratify this policy; implementation already encodes the double opt-in and explicit `allow_llm` paths documented in-repo.
- This record is **architectural/governance evidence** for audit and gate readiness — **not** a request for additional product scope, new narrative surfaces, or new environment variables beyond the two named flags.

## Out of scope (unchanged)

Ratification does **not** extend to FE presentation, clinician-report LLM generation, validator redesign, or deterministic Layer B changes.
