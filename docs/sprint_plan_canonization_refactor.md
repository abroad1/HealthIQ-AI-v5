# **Mini Sprint Plan — Canonization and Validation Refactor (v4 → v5 Integration)**

## **Purpose**

Strengthen the HealthIQ-AI backend and frontend data pipeline by re-introducing mature version 4 logic for biomarker alias resolution, canonicalization, and context validation.
This programme ensures every biomarker and user record entering the analysis engine is validated, typed, and canonicalised before orchestration.

---

## **Overall Objectives**

1. Replace ad-hoc normalization with a **canonical alias registry**.
2. Introduce a **ContextFactory** for structured data validation.
3. Restore **validation utilities** for automated testing.
4. Add a **frontend alias resolution service** and API endpoint.
5. Validate performance parity and output integrity across the full pipeline.

---

## **Duration**

**5 sprints (approx. 10 weeks)**
Each sprint delivers a self-contained, testable increment.

---

## **Sprint 0 — Preparation and Baseline**

**Duration:** 1 week

**Goals**

* Snapshot current v5 working state.
* Create `/v4_reference` folder containing ported v4 files for read-only use.
* Map current canonicalization flow and dependencies.
* Define regression test panels and success criteria.

**Deliverables**

* Tagged repository `pre-canonization-baseline`.
* Updated architecture diagram (current v5).
* Agreed test datasets for validation.

---

## **Sprint 1 — Canonical Alias Registry Refactor**

**Duration:** 2 weeks

**Goals**

* Integrate v4 `biomarker_alias_registry.yaml` and extend current `biomarkers.yaml`.
* Implement robust alias resolver (Python) using v4 matching logic.
* Add new backend endpoint `/api/biomarker-aliases` for dynamic alias access.
* Ensure normalization returns canonical keys only.

**Validation**

* Run upload + analysis using test panels → all biomarkers retained.
* Confirm API returns full alias map.
* No “unmapped_” prefixes in logs.

**Deliverables**

* New alias registry file and resolver class.
* API documentation for `/api/biomarker-aliases`.
* Validation report showing 100 % mapping success.

---

## **Sprint 2 — Context Factory Integration**

**Duration:** 2 weeks

**Goals**

* Port and adapt `context_factory.py` into `backend/core/context`.
* Wire factory into `/api/analysis/start` to produce validated `AnalysisContext`.
* Ensure orchestrator consumes this context unchanged.
* Add structured error handling and logging.

**Validation**

* Invalid payloads rejected with descriptive 4xx errors.
* Valid payloads processed normally.
* Logs show `[TRACE] Created AnalysisContext`.

**Deliverables**

* Operational `ContextFactory` class.
* Unit tests for all parsing paths.
* Updated developer documentation: “Data Entry Pipeline”.

---

## **Sprint 3 — Validation & Testing Utilities**

**Duration:** 2 weeks

**Goals**

* Re-introduce `validate_panel_aliases_and_ranges.py` and `test_canonical_updates.py`.
* Add CI hooks to run validation on every PR.
* Generate automated test reports (JSON + HTML).

**Validation**

* Tools run successfully on baseline panels.
* CI passes all canonicalization tests.

**Deliverables**

* Two working tools under `backend/tools/`.
* Baseline `validation_report.json`.
* CI integration note.

---

## **Sprint 4 — Frontend Alias Service Integration**

**Duration:** 2 weeks

**Goals**

* Port v4 `biomarkerAliases.ts` to `frontend/app/services/`.
* Connect to backend `/api/biomarker-aliases`.
* Implement client-side validation before upload.
* Display clear “unknown biomarker” warnings.

**Validation**

* Manual PDF/text upload resolves all aliases.
* Fake biomarker flagged client-side, not sent to backend.
* Network tab shows zero failed POSTs due to alias errors.

**Deliverables**

* New TypeScript service with caching and metrics.
* Updated upload page integration.
* Frontend test cases.

---

## **Sprint 5 — Performance, Consolidation, and Documentation**

**Duration:** 1 week

**Goals**

* Benchmark performance before vs after refactor.
* Remove redundant v4 compatibility code.
* Update all architecture and developer docs.
* Final regression test: outputs identical to baseline.

**Validation**

* Upload-to-result time ≤ baseline × 1.10.
* Regression suite 100 % pass.
* Verified identical biomarker counts and scores.

**Deliverables**

* Benchmark summary report.
* Updated `IMPLEMENTATION_PLAN.md` and system diagrams.
* Final sign-off meeting notes.

---

## **Governance and Roles**

| Role                | Responsibility                                             |
| ------------------- | ---------------------------------------------------------- |
| **Anthony**         | Product owner / technical lead, approves sprint outcomes   |
| **Cursor**          | AI code generation and implementation                      |
| **ChatGPT (GPT-5)** | Architectural oversight, documentation, validation scripts |
| **QA Engineer**     | Test planning and execution                                |
| **Frontend Dev**    | Integrate alias service & UI validation                    |
| **Backend Dev**     | Implement resolver, context factory, and tools             |

---

## **Risks & Mitigation**

| Risk                                 | Mitigation                                                           |
| ------------------------------------ | -------------------------------------------------------------------- |
| Breaking existing orchestrator logic | Isolate ContextFactory behind flag until validated                   |
| Schema divergence between v4 & v5    | Maintain versioned SSOT (`biomarkers_v4.yaml`, `biomarkers_v5.yaml`) |
| Large alias registry merge errors    | Add YAML schema validator and automated diff check                   |
| Performance regressions              | Benchmark each sprint and tune before merge                          |

---

## **Success Criteria**

* 100 % canonical mapping of all incoming biomarkers.
* Zero “unmapped_” keys in production logs.
* All invalid payloads rejected gracefully with typed errors.
* Consistent analysis outputs pre- and post-refactor.
* Documented, test-driven pipeline ready for future module extensions.



---
### **TESTING BY SPRINT PHASE**

### **Sprint 1 — Canonization & Alias Registry**

**Goal:** canonical names pass cleanly end-to-end.

**Validation steps**

1. Run upload + analysis with known test panels.
   Expect: all biomarkers retained, no “unmapped_” prefixes.
2. Compare `biomarkers.yaml` vs input keys → 100 % match rate.
3. Verify `/api/biomarker-aliases` returns full alias map.
4. Unit-test `normalize_biomarkers()` for alias and case variations.

**Success metric:** canonical pipeline produces identical biomarker list count pre- and post-normalization.

---

### **Sprint 2 — Context Factory Integration**

**Goal:** validated `AnalysisContext` replaces ad-hoc input passing.

**Validation steps**

1. Feed malformed payloads (missing units, bad types) → factory rejects with structured errors.
2. Feed correct payloads → orchestrator runs unchanged.
3. Confirm backend log: `[TRACE] Created AnalysisContext …`.

**Success metric:** 100 % of bad data caught before orchestrator; 0 runtime type errors.

---

### **Sprint 3 — Validation Tools**

**Goal:** enable automated regression testing.

**Validation steps**

1. Run `python backend/tools/validate_panel_aliases_and_ranges.py` → no schema errors.
2. Execute `pytest backend/tools/test_canonical_updates.py` → all tests pass.
3. Generate validation report (`report.json`) and store in `tests/reports/`.

**Success metric:** tools run cleanly; baseline report established for future CI.

---

### **Sprint 4 — Frontend Alias Service**

**Goal:** frontend prevents alias errors before backend call.

**Validation steps**

1. Paste PDF text → client resolves all aliases using `/api/biomarker-aliases`.
2. Introduce fake biomarker → UI flags as “unknown” without sending to backend.
3. Observe network tab → no failed POSTs due to alias issues.

**Success metric:** 0 alias-related backend errors during manual upload.

---

### **Sprint 5 — Performance & Consolidation**

**Goal:** system parity and efficiency confirmed.

**Validation steps**

1. Benchmark upload-to-result time before vs after refactor.
2. Validate outputs for identical test panel → same biomarker counts, same scores.
3. Review logs → no duplicate alias loads, no warnings.

**Success metric:** identical outputs, ≤10 % performance delta.

---

### **Summary**

| Phase | Independent? | Testable via API/UI? | Rollback-safe? |
| :---- | :----------: | :------------------: | :------------: |
| 1     |       ✅      |           ✅          |        ✅       |
| 2     |       ✅      |           ✅          |        ✅       |
| 3     |       ✅      |       ⚙️ (CLI)       |        ✅       |
| 4     |       ✅      |           ✅          |        ✅       |
| 5     |       ✅      |           ✅          |        ✅       |

