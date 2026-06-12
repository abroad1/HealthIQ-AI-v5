# CONTEXT-THREADING-1 — Pre-Sprint Architecture Audit

---
work_id: CONTEXT-THREADING-1_pre_sprint_architecture_audit
audit_type: pre_sprint_architecture
audited_by: Claude Code
audit_utc: 2026-06-12
status: COMPLETE
source_sprint: CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer
---

## Executive Verdict

The orchestrator segmentation that was previously flagged as needed has been **partially completed** — a `pipeline/` directory exists with extracted phase functions. However, the segmentation is incomplete: the 2,289-line `orchestrator.py` still holds the monolith body, and the signal evaluation phase was extracted as a function but its signature was never extended to accept context data.

The wiring is straightforward. The raw questionnaire data is already available in `orchestrator.run()` before the signal evaluation call. `build_runtime_context_snapshot()` already exists and accepts raw questionnaire responses. The fix is **two files, two additions** — no new module required.

The one structural constraint that matters: signal evaluation runs at **Step 1.6**, but `create_analysis_context()` (which produces fully-mapped `lifestyle_factors` and `medical_history`) runs at **Step 2** — after signal evaluation. Threading must use the raw `questionnaire_data` dict, not the mapped output.

---

## Q1–Q3: Current Orchestrator Map

| File | Role | Line count |
|------|------|------------|
| `backend/core/pipeline/orchestrator.py` | Main orchestrator — `AnalysisOrchestrator.run()` entry point | 2,289 |
| `backend/core/pipeline/orchestrator_phases_v1.py` | Extracted named phase functions | 170 |
| `backend/core/pipeline/context_factory.py` | `AnalysisContextFactory` — builds immutable `AnalysisContext` | 194 |
| `backend/core/pipeline/questionnaire_mapper.py` | `QuestionnaireMapper` — maps questionnaire to `MappedLifestyleFactors` / `MappedMedicalHistory` | ~670 |
| `backend/core/pipeline/events.py` | Pipeline event definitions | ~30 |

**Prior segmentation state:** A prior sprint extracted `quarantine_unmapped_biomarkers()`, `prepare_scoring_inputs_from_panel()`, and `evaluate_signal_evaluation_phase()` into `orchestrator_phases_v1.py`. This was behaviour-preserving. The `PIPELINE_PHASE_ORDER` tuple documents the intended phase sequence. The `orchestrator.py` body still calls these as local delegates — it remains the single execution thread at ~2,289 lines. Segmentation is partial; the monolith body has not been broken up further.

---

## Q4–Q6: Where Context Data Lives

**Questionnaire data flow:**

```
API: start_analysis() [backend/app/routes/analysis.py:95]
  → questionnaire_data: Optional[Dict[str, Any]] received
  → AnalysisOrchestrator.run() [backend/core/pipeline/orchestrator.py]
    → raw questionnaire_data available in scope from ~line 306
    → Step 1.6: evaluate_signal_evaluation_phase() called [line 1254]
        ← questionnaire_data NOT passed (gap)
    → Step 2: create_analysis_context() called [line 1267+]
        → questionnaire_mapper.map_submission() maps to lifestyle_factors + medical_history
        → AnalysisContextFactory creates AnalysisContext with all three stored
```

**Field availability at the signal evaluation step (Step 1.6):**

| Field | In raw `questionnaire_data`? | Forwarded to `evaluate_signal_evaluation_phase`? |
|-------|------------------------------|--------------------------------------------------|
| `biological_sex` | Yes | No — not forwarded |
| `date_of_birth` | Yes | No — not forwarded |
| `long_term_medications` | Yes | No |
| `supplements` | Yes | No |
| `symptoms` | Yes | No |
| `chronic_conditions` | Yes | No |
| `stress_level` | Yes | No |
| Companion biomarkers | Yes (via `signal_biomarkers`) | Yes — already in scope |

All questionnaire fields exist in the raw `questionnaire_data` dict that is available in `orchestrator.run()` at the time signal evaluation is called. They are simply not forwarded.

**Important ordering constraint:** `create_analysis_context()` runs at Step 2 — after signal evaluation. The fully mapped `lifestyle_factors` and `medical_history` dicts are therefore NOT available at the signal evaluation step. Threading must use `questionnaire_data` (the raw dict) as the source, not the mapped outputs.

`build_runtime_context_snapshot()` (`backend/core/analytics/runtime_context_evaluator.py:164`) already accepts `questionnaire_responses: Optional[Mapping[str, Any]]` and extracts all relevant fields directly from the raw dict — it is designed for exactly this usage.

---

## Q7–Q9: Signal Evaluator Call Site

**Single call site:** `backend/core/pipeline/orchestrator_phases_v1.py` line 147

```python
signal_results_raw = signal_evaluator.evaluate_all(
    signal_biomarkers,
    signal_derived,
    lab_ranges=input_reference_ranges,
    reference_profiles=input_reference_profiles,
    # runtime_context NOT passed
)
```

**Variables in scope at this call site:** `signal_evaluator`, `simple_biomarkers`, `derived_ratios_meta`, `input_reference_ranges`, `input_reference_profiles` — nothing carrying questionnaire, demographic, medication, or clinical context.

**`build_runtime_context_snapshot()` called outside tests:** Never. The function exists in `runtime_context_evaluator.py` and is only called in `backend/tests/regression/test_runtime_context_evaluation.py`.

---

## Q10: Recommended Insertion Point

The insertion point is precisely identified.

**`orchestrator.py` — before line 1254** (the `evaluate_signal_evaluation_phase()` call):

```python
# Build runtime context snapshot from raw questionnaire data.
# lifestyle_factors/medical_history are not yet mapped at this pipeline stage.
runtime_ctx = build_runtime_context_snapshot(
    questionnaire_responses=questionnaire_data,
)
```

Then pass it into the phase call:

```python
signal_phase = evaluate_signal_evaluation_phase(
    ...
    runtime_context=runtime_ctx,
)
```

**`orchestrator_phases_v1.py` — `evaluate_signal_evaluation_phase()` signature** (line 131):

Add `runtime_context: Optional[Dict[str, Any]] = None` to the function signature and forward it to `evaluate_all()`.

---

## Q11: Does a New Module Belong Here?

No new module is required for CONTEXT-THREADING-1. The existing `build_runtime_context_snapshot()` in `runtime_context_evaluator.py` is the right tool. Creating a new `context_assembler` module would be premature — the function already exists and its placement in the evaluator module is correct (it builds the shape that the evaluator consumes).

A new module would only be warranted if the orchestrator needed to assemble and use runtime context in multiple places (scoring, clustering, narrative) — not in scope here.

---

## Q12: Minimum Safe File Changes for CONTEXT-THREADING-1

**Two files. No others.**

| File | Change | Risk |
|------|--------|------|
| `backend/core/pipeline/orchestrator_phases_v1.py` | Add `runtime_context: Optional[Dict[str, Any]] = None` to `evaluate_signal_evaluation_phase()` signature (line 131); forward to `evaluate_all()` (line 147) | Low — backward-compatible optional param |
| `backend/core/pipeline/orchestrator.py` | Import `build_runtime_context_snapshot`; call it using raw `questionnaire_data` before line 1254; pass result to `evaluate_signal_evaluation_phase()` | Low — three-line addition before an existing call |

`signal_evaluator.py` and `runtime_context_evaluator.py` do not need to change — they are already correct from CONTEXT-RUNTIME-1.

---

## Q13: Files That Must Not Be Touched

- `backend/core/analytics/signal_evaluator.py` — already updated; must not be re-edited
- `backend/core/analytics/runtime_context_evaluator.py` — already correct; must not be re-edited
- All `signal_library.yaml` package files — `runtime_context_requirements` metadata already in place
- `backend/core/pipeline/questionnaire_mapper.py` — raw `questionnaire_data` is sufficient; do not modify
- All forbidden surfaces: SSOT, frontend, scoring, reference ranges, signal IDs, activation keys, report compiler, clinical wording
- `knowledge_bus/governance/` files — no governance changes needed for threading

---

## Q14: Regression Tests Needed

New tests required in a dedicated regression test file (e.g., `test_context_threading.py`):

| Test | What it proves |
|------|---------------|
| Orchestrator builds non-None `runtime_context` when `questionnaire_data` includes `biological_sex` and `date_of_birth` | Threading produces valid context from real questionnaire input |
| `evaluate_signal_evaluation_phase()` with `runtime_context=None` produces identical results to calling without it | Backward compatibility — existing callers unaffected |
| Signal with `runtime_context_requirements` does NOT emit when `runtime_context` is passed but required key is absent | Gate enforces at the orchestrator level |
| Signal with `runtime_context_requirements` DOES emit when `runtime_context` is passed with all required keys present | Gate passes correctly |
| Unrelated signals (no `runtime_context_requirements` declared) emit identically regardless of `runtime_context` value | No regression on existing signal set |
| End-to-end: full panel with questionnaire produces same signal set as same panel without questionnaire, for all currently active signals | No unintended suppression of the existing active signal estate |

The final integration test is the critical safety check — it must confirm that the current active signal estate (which has no `runtime_context_requirements` on any currently-active package) is completely unaffected by the threading change.

---

## Q15: Sprint Shape and STOP Gate Decision

**Single sprint. No STOP gate needed within the sprint.**

Rationale:
- The change is two files, both low-risk additions
- No package activation is performed — the context gate goes from "never checked in production" to "checked in production," but all in-scope packages already have `enable_lower_bound: false` (FT3) or are blocked by CF-BATCH2-010 (androgen). The gate fires but suppresses, exactly as designed.
- The `runtime_context` parameter is optional — existing callers not touching questionnaire data are completely unaffected
- Risk is LOW once test coverage confirms existing active signals are unaffected

**One pre-implementation STOP condition** that must be verified in Phase 1 (before code changes): confirm the full list of currently active signals (those whose packages do NOT declare `runtime_context_requirements`) to prove the threading change cannot suppress any of them. This is a read-only audit step, not a separate sprint gate.

**The existing activation STOP gate (APPROVE BATCH2 CONTEXT GATED ACTIVATION) remains in place.** Threading is not activation. CONTEXT-THREADING-1 makes the mechanism live; package activation remains a separate gated decision requiring resolution of Observation 2 from the CONTEXT-RUNTIME-1 audit (androgen context gate semantics) and CF-BATCH2-010 clinical sign-off.

---

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Variable name for questionnaire data in `run()` scope must be confirmed before authoring the prompt | Medium | Read `orchestrator.run()` signature before drafting CONTEXT-THREADING-1 prompt |
| `build_runtime_context_snapshot()` with only `questionnaire_responses` set (no `lifestyle_factors`, `medical_history`) produces incomplete context | Low | By design — snapshot is additive; absent inputs produce empty buckets, not errors. Currently active signals have no context requirements. |
| Any currently active package with `runtime_context_requirements` accidentally added would now suppress in production | Low | Confirmed: only the 9 inactive in-scope packages carry `runtime_context_requirements`. Verify with a grep before authoring the sprint. |
| `inject_questionnaire_age()` (`orchestrator_phases_v1.py:160`) already injects age into `simple_biomarkers["age"]` — must not duplicate via context | Low | Age as biomarker value and age as demographic context gate serve different purposes; `signal_biomarkers` strips `age` at line 141 (`k != "age"`). No conflict. |
| Androgen context gate semantics (Observation 2 from CONTEXT-RUNTIME-1 audit) — `medication.hormone_therapy: present` currently means "patient IS on hormone therapy" not "context disclosed" | Medium | No activation sprint may be authored without GPT resolving this semantic issue first. Threading itself is safe regardless. |

---

## Open Items for GPT (Pre-CONTEXT-THREADING-1)

Two items from the CONTEXT-RUNTIME-1 audit remain open and must be resolved by GPT before authoring the activation sprint (not blocking for CONTEXT-THREADING-1 itself):

1. **CF-CONTEXT-MOD-3 finality** — Is the carry-forward genuinely resolved at "capability level," or does orchestrator threading need to complete before CF-CONTEXT-MOD-3 is treated as closed? Recommend GPT decides whether CONTEXT-THREADING-1 completion is the condition that closes CF-CONTEXT-MOD-3.

2. **Androgen context gate semantics** — `medication.hormone_therapy: present` and `clinical_context.aas_exposure: present` as required gates mean only patients who ARE on hormone therapy / using AAS can emit androgen signals. This is a false-negative risk for any future activation. Requires architecture decision before the androgen activation sprint prompt is authored.
