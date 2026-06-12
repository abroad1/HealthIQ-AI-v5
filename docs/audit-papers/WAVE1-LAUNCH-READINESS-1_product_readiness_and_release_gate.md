# WAVE1-LAUNCH-READINESS-1 — Product Readiness & Release Gate Audit

**Audit ID:** WAVE1-LAUNCH-READINESS-1  
**Auditor:** Claude Code (adversarial review role, CLAUDE.md §6)  
**Date:** 2026-06-12  
**Branch audited:** `docs/wave1-launch-readiness-audit`  
**Preceding architecture verdict:** `DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW` → ACCEPTED_WITH_CONDITIONS  
**This audit:** Read-only product launch readiness — no runtime code, frontend code, package metadata, governance YAML, or merge actions taken.

---

## Executive Verdict

```
LAUNCH_READY_WITH_CONDITIONS
```

No absolute launch blockers were found. The prior session's concern about committed secrets in `backend/.env` was **incorrect** — that file is gitignored and is not in git history; credentials remain local-only. However, **four conditional blockers** must be resolved before public launch, plus one pre-existing production defect (unit registry Unicode collision) that will cause silent failures on a subset of real-world lab reports. All architecture guardrails pass. All 9 context-dependent packages remain inactive with fail-closed gates. The analytical engine is governed, deterministic, and safe for Wave 1.

---

## Repository Baseline

| Item | Value |
|------|-------|
| Branch | `docs/wave1-launch-readiness-audit` |
| Base commit | `edcec85` (BATCH2-CONTEXT-COMPLETION-1 COMPLETE) |
| Working tree | clean (this branch created fresh for audit) |
| Architecture validator | **PASS** |
| Medical frame identity index | **PASS (0 errors)** |
| Context modifier catalogue | **PASS (0 errors)** |
| Sentinel full scan | 54 passed / **6 failed** / 0 errors |
| Sentinel governance escalation | **true** (see §9 — unit registry Unicode bug) |

---

## Source Documents Inspected

| Document | Status |
|----------|--------|
| `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md` | ACCEPTED |
| `docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md` | ACCEPTED_WITH_CONDITIONS |
| `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md` | IMPLEMENTATION_COMPLETE_NO_ACTIVATION |
| `knowledge_bus/governance/context_runtime_execution_register_v1.yaml` | activated=0, gated=9 |
| `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml` | 0 eligible, 8 BLOCKED, 1 DEFERRED |
| `backend/app/routes/analysis.py` | inspected |
| `backend/app/routes/upload.py` | inspected |
| `frontend/app/(app)/results/page.tsx` | inspected |
| `frontend/app/services/analysis.ts` | inspected |
| `frontend/app/components/clusters/ClusterInsightPanel.tsx` | inspected |
| `frontend/app/lib/legacyInsightsVisibility.ts` | inspected |
| `backend/core/insights/synthesis.py` | inspected |
| `backend/core/insights/narrative_runtime_policy.py` | inspected |
| `backend/env.example` | inspected |
| `backend/.env.test` | inspected |
| `sentinel/reports/sentinel_run_87c5a2cd.json` | inspected (latest run) |

---

## 1. Launch Scope Assessment

**Verdict: PASS**

Wave 1 launch scope is consistent with the Day-One Architecture verdict.

- ADR-RT-001 accepted 2026-05-28; no scope changes detected since.
- Carry-forward register (`docs/sprints/launch_core_carry_forward_register.md`) states "no known launch-blocking carry-forwards" as of 2026-06-03.
- The four carry-forwards noted in the Day-One review (C-1 through C-4) are all classified as acceptable Wave 1 residuals: ARCH-ORCH-RESTRUCTURE-1 (open, safe), 9 inactive context-dependent packages (fail-closed), CF-BATCH2-010 (androgen clinical sign-off outstanding), and PSI compile-only (runtime-dead).
- No evidence of scope creep into Wave 2 capabilities.

---

## 2. User Journey Readiness

**Verdict: CONDITIONAL — pending conditional blockers CB-2 and CB-3 (§12)**

The core user journey (upload → parse → submit → results) is structurally complete:

- `/api/upload/parse` → biomarker extraction via LLM (Gemini) or deterministic CSV parser
- `/api/analysis/start` → synchronous analysis pipeline (no SSE streaming in production)
- `/api/analysis/result` → fetch completed result
- Results page renders `ClusterSummary` from backend DTO — render-only confirmed
- PDF export present; billing/paywall present; history endpoint present

**Gap:** The `/api/upload/parse` endpoint (CB-2) has no authentication dependency. Any party can submit files for LLM-powered biomarker extraction, incurring API cost and processing load without authentication. This blocks confident public launch.

**Gap:** The frontend console PII logging (CB-1) means every analysis submission exposes the full health data payload in the browser developer console. Unacceptable for any health data product serving real users.

---

## 3. Clinical Safety and Claim Safety

**Verdict: PASS (with noted residuals)**

- Frontend results page (`frontend/app/(app)/results/page.tsx`) confirmed: imports `ClusterSummary` only — NOT `ClusterInsightPanel`. Verified at line 15.
- `ClusterInsightPanel` contains `getClinicalRecommendations()` (lines 88–121) that generates frontend-authored clinical copy from cluster name pattern matching. This component is exported from `frontend/app/components/clusters/index.ts` but is **not imported by any live page or route**.
- `ClusterSummary` is a render-only component; all clinical copy comes from backend-provided DTO fields.
- LLM double opt-in confirmed: both `HEALTHIQ_NARRATIVE_LLM` and `HEALTHIQ_ENABLE_LLM` must be set for production LLM narrative. Defaults: OFF.
- `MockLLMClient` fallback in `InsightSynthesizer` returns deterministic placeholder responses when LLM is disabled or misconfigured — does not generate clinical claims.
- Layer B (deterministic analytical engine) confirmed free of LLM reasoning.
- `ClusterInsightPanel` export in `frontend/app/components/clusters/index.ts` is a **latent risk**: a future developer importing it could silently introduce frontend clinical inference. Should be removed or unexported as post-launch hardening (see §15).

---

## 4. Reference Range and Lab-Range Safety

**Verdict: PASS**

- No hardcoded reference ranges detected in the analytical core.
- SSOT reference ranges governed in `backend/ssot/biomarkers.yaml` per architectural non-negotiable §7.1.
- Lab-origin detection present (`backend/core/lab/detector.py`) — deterministic.
- Unit normalisation registry active — **but see CB-3 below**: a Unicode mu character collision (`μ` vs `\xb5`) causes `UnitConversionError` for urate when lab files encode µmol/L with the Greek mu character (U+03BC).

---

## 5. Parser and Upload Safety

**Verdict: CONDITIONAL — pending CB-2 (unauthenticated `/parse` endpoint)**

- Deterministic parser (`try_deterministic_parse`) is tried first for CSV-format text; falls through to LLM only for unstructured content. Correct layering.
- LLM parser is Gemini-backed; extraction produces structured biomarker objects with confidence scores.
- SSOT enrichment applied post-extraction.
- Canonical resolver applied to extracted biomarker IDs.

**CB-2:** `/api/upload/parse` (lines 42–46, `backend/app/routes/upload.py`) has no authentication dependency. The `@router.post("/parse")` handler accepts `UploadFile` or `text_content` from any caller without a bearer token check. An unauthenticated attacker can:
  - Submit arbitrary documents for LLM parsing (Gemini API cost risk)
  - Process medical documents without any access control

The `/api/analysis/start` route does enforce auth. The parse endpoint must be aligned.

---

## 6. Runtime Architecture Guardrails

**Verdict: PASS**

Confirmed via validators and code inspection:

| Check | Result |
|-------|--------|
| `validate_day_one_architecture` | **PASS** |
| No raw investigation-spec/Pass 3 reads at runtime | **CONFIRMED** |
| PSI translator compile-only (not in runtime path) | **CONFIRMED** — only in tests, validators, egg-info |
| LLM double opt-in (both flags required) | **CONFIRMED** — `narrative_runtime_policy.py` |
| MockLLMClient fallback is deterministic placeholder | **CONFIRMED** |
| `ClusterInsightPanel` not imported by live results page | **CONFIRMED** — `results/page.tsx` line 15 |
| Layer B free of LLM reasoning | **CONFIRMED** |
| SSOT as sole biomarker reference authority | **CONFIRMED** |

ARCH-ORCH-RESTRUCTURE-1 (Step 1.6 questionnaire threading before `create_analysis_context()`) remains open and is classified as an acceptable Wave 1 residual. The implementation at `backend/core/pipeline/orchestrator.py` Step 1.6 reads `questionnaire_responses=questionnaire_data` correctly; the architectural ordering issue does not produce incorrect output in the current implementation.

---

## 7. Context-Dependent Package Safety

**Verdict: PASS**

All 9 context-dependent packages remain inactive with fail-closed gates.

| Package class | Count | Status | Gate |
|---------------|-------|--------|------|
| Androgen packages | 8 | inactive / `compiled_not_promoted` | `BLOCKED_PENDING_CLINICAL_SIGNOFF` |
| FT3 low | 1 | inactive / `DEFERRED_NON_LAUNCH_CRITICAL` | `enable_lower_bound: false` |

- `knowledge_bus/governance/context_runtime_execution_register_v1.yaml`: `activated_package_count: 0`, `gated_inactive_package_count: 9`, `approval_received: false`
- CF-BATCH2-010 (androgen clinical sign-off) remains open — no androgen package activation is possible without this.
- `disclosed` context semantics implemented in BATCH2-CONTEXT-COMPLETION-1 (19+6+4 tests all PASS) — correctly distinguishes disclosed from present without activating packages.

---

## 8. Frontend Live-Route Safety

**Verdict: PASS (with latent risk noted)**

| Check | Result |
|-------|--------|
| `results/page.tsx` imports `ClusterSummary` (not `ClusterInsightPanel`) | **CONFIRMED** — line 15 |
| `ClusterSummary` is render-only | **CONFIRMED** |
| `legacyInsightsVisibility.ts` gates legacy insights on env flag | **CONFIRMED** — `NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS` |
| No frontend clinical inference in live render path | **CONFIRMED** |
| `supabaseHelpers` in `frontend/app/lib/supabase.ts` are mock placeholders | **CONFIRMED** — not called in production |

**Latent risk:** `ClusterInsightPanel` (which contains `getClinicalRecommendations()`) is exported from `frontend/app/components/clusters/index.ts`. It is not in the live path now, but the export makes it trivially importable. Post-launch hardening recommendation: unexport or move to a clearly-labelled legacy directory.

**`frontend/.env.local.example` has `NEXT_PUBLIC_DEBUG=true`** — this must be `false` in production deployment. Classify as pre-launch deployment checklist item.

---

## 9. Security, Privacy, and Operational Baseline

**Verdict: CONDITIONAL — CB-1 and CB-2 must be resolved**

### CB-1: Full health data payload logged to browser console (CRITICAL PII)

**File:** `frontend/app/services/analysis.ts` lines 96–121  
**Nature:** Every call to `AnalysisService.startAnalysis()` logs the complete analysis request payload to the browser developer console, including all biomarker values, user demographics (age, sex, weight, height), and questionnaire data.

Specific statements:
- Line 96: `console.log("📤 AnalysisService.startAnalysis() called with payload:", data)`
- Line 98: `console.log("📤 User data:", data.user)`
- Line 103: `console.log("📨 Request body:", JSON.stringify(data, null, 2))` — full JSON serialisation
- Lines 107–120: `console.group("[TRACE] Outgoing Analysis Payload")` block with `console.log("[TRACE] Full Payload JSON:\n", JSON.stringify(data, null, 2))`

Any user with developer tools open, any browser extension with console access, or any screen-share session will expose complete patient health data. This is unacceptable for a health data product launching to real users.

**Resolution required:** Remove all debug console logging from `startAnalysis()` before public launch.

### CB-2: Unauthenticated `/api/upload/parse` endpoint

**File:** `backend/app/routes/upload.py` line 42  
**Nature:** `@router.post("/parse")` accepts file and text submissions without any auth dependency. Contrast with `/api/analysis/start` which enforces authentication. The parse endpoint invokes the Gemini LLM API per request. Any unauthenticated party can drive API cost and process arbitrary documents.

**Resolution required:** Add the same auth dependency used by the analysis route.

### Git credential safety: PASS

- `backend/.env` is listed in `.gitignore` and confirmed not tracked in git (`git ls-files backend/.env` returns nothing, `git log -- backend/.env` returns no commits).
- `backend/.env.test` IS tracked in git — contains only localhost test credentials (`test-service-role-key`, localhost PostgreSQL test DB) — no real credentials.
- `backend/env.example` contains only placeholder values (`your-gemini-api-key-here`, etc.) — safe.

### Deployment config risk: CB-4

**File:** `backend/env.example`  
Lines 127–128 contain:
```
HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1
HEALTHIQ_FREE_COMPLETED_ANALYSES=99
```
Both are explicitly labelled as dev/local values. If this file is used as-is for a production deployment (e.g., by a CI/CD pipeline copying env.example to .env), billing enforcement will be disabled and 99 free analyses will be granted to every user. These values must be explicitly overridden in deployment config.

**Resolution required:** Remove or comment out both lines from `env.example`, or add a deployment checklist item explicitly calling them out.

### Backend debug print statements: POST_LAUNCH_HARDENING

`backend/app/routes/analysis.py` contains 6 `print()` debug statements in the production analysis route, including one that logs `user_id`. The catch-all exception handler exposes internal exception details to clients: `message=f"Analysis failed: {str(e)}"`. No immediate launch block but must be addressed before scale.

---

## 10. Product Readiness Evidence Gaps

| Gap | Severity | Notes |
|-----|----------|-------|
| Unit registry Unicode collision (urate) | CB-3 | 6 sentinel regression tests fail; real production defect |
| No end-to-end Playwright smoke test for full journey | ACCEPTABLE | Manual UAT covers golden path |
| `ClusterInsightPanel` exported but unused | ACCEPTABLE RESIDUAL | Latent risk, not active |
| No formal data processing agreement template | OUT OF SCOPE | Pre-commercial regulatory work |
| `supabaseHelpers` are mock placeholders | KNOWN | Functional auth via separate path |

---

## Launch Blocker Table

| ID | Finding | File | Verdict |
|----|---------|------|---------|
| — | No absolute launch blockers identified | — | — |

No findings meet the launch blocker threshold. The only candidate (committed backend credentials) was confirmed NOT to apply — `backend/.env` is gitignored and contains no git history.

---

## Conditional Blocker Table

Conditional blockers must be resolved before public launch to real users.

| ID | Finding | File | Risk |
|----|---------|------|------|
| CB-1 | Full health data payload (all biomarkers, user demographics, questionnaire) logged to browser console in production `startAnalysis()` | `frontend/app/services/analysis.ts` lines 96–121 | PII exposure to browser console — health data product regulatory risk |
| CB-2 | `/api/upload/parse` endpoint has no authentication dependency | `backend/app/routes/upload.py` line 42 | Unauthenticated LLM invocation; API cost risk; uncontrolled document processing |
| CB-3 | Unit registry raises `UnitConversionError` for urate expressed as `μmol/L` (U+03BC Greek mu) vs. expected base unit `µmol/L` (U+00B5 Micro sign) — 6 sentinel regression tests fail | `backend/core/units/registry.py` line 351 | Silent analysis failure for subset of real-world lab reports; sentinel governance escalation triggered |
| CB-4 | `backend/env.example` contains `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1` and `HEALTHIQ_FREE_COMPLETED_ANALYSES=99` without prominent production-override requirement | `backend/env.example` lines 127–128 | Accidental billing bypass in production deployment if env.example is used without override |

---

## Acceptable Wave 1 Residuals

| ID | Residual | Source | Rationale |
|----|---------|--------|-----------|
| R-1 | ARCH-ORCH-RESTRUCTURE-1 — orchestrator `build_runtime_context_snapshot()` at Step 1.6 before `create_analysis_context()` | Day-One CF-CONTEXT-001 | No incorrect output produced; architectural cleanup deferred |
| R-2 | PSI translator compile-only — not imported by orchestrator or pipeline | Day-One CF-ADR-002 | Runtime-dead confirmed; guarded by sentinel |
| R-3 | 9 context-dependent packages inactive (8 androgen + FT3 low), fail-closed | Day-One CF-CONTEXT-002 | CF-BATCH2-010 (clinical sign-off) outstanding; no activation possible or attempted |
| R-4 | Root-cause dual authority — 40 YAML root-cause definitions vs. 1 compiled | Day-One CF-ADR-003 | 39 compile-registered; activation-compile gap accepted for Wave 1 |
| R-5 | Wave1 subsystem evidence hard-coded in `backend/core/analytics/wave1_subsystem_evidence.py` | Day-One CF-SENTINEL-001 | Classified legacy; guarded by sentinel (`health_system_card_frontend_calculates_evidence_completeness`) |
| R-6 | `ClusterInsightPanel` exported but not imported by any live page | — | Latent risk only; not in live path |
| R-7 | Backend `print()` debug statements in analysis route and orchestrator | — | Post-launch hardening; not user-facing PII in most cases |
| R-8 | Exception message leakage to clients in catch-all handler | `backend/app/routes/analysis.py` | Post-launch hardening |
| R-9 | `supabaseHelpers` in `frontend/app/lib/supabase.ts` are mock placeholders | — | Auth path is functional via separate mechanism; mocks not called in production |

---

## Recommended Next Action

**Immediate (before any public user access):**

1. **CB-1 — Remove PII console logging:** Delete lines 96–121 of `frontend/app/services/analysis.ts` (all `console.log`, `console.group`, `console.groupEnd` calls in `startAnalysis()`). This is a one-sprint fix on a `fix/remove-analysis-pii-console-logging` branch.

2. **CB-2 — Authenticate `/parse` endpoint:** Add the same bearer-token auth dependency to `@router.post("/parse")` in `backend/app/routes/upload.py` that `/api/analysis/start` uses.

3. **CB-3 — Fix unit registry Unicode mu collision:** In `backend/core/units/registry.py`, normalise both U+03BC (Greek mu) and U+00B5 (Micro sign) to a single canonical form before unit matching. This resolves all 6 failing sentinel regression tests and prevents urate parse failures in production.

4. **CB-4 — Strip dev billing overrides from env.example:** Remove or comment out `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1` and `HEALTHIQ_FREE_COMPLETED_ANALYSES=99` from `backend/env.example`, or add a clearly-marked deployment checklist entry.

**Pre-launch deployment checklist additions:**
- Set `NEXT_PUBLIC_DEBUG=false` in production frontend environment
- Verify `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT` is unset or `0` in production
- Verify `HEALTHIQ_FREE_COMPLETED_ANALYSES=1` in production
- Confirm `HEALTHIQ_NARRATIVE_LLM` and `HEALTHIQ_ENABLE_LLM` reflect intended production state

**Post-launch hardening (not blocking):**
- Remove backend `print()` debug statements
- Replace `message=f"Analysis failed: {str(e)}"` with a generic error message in the analysis route catch-all
- Unexport `ClusterInsightPanel` from `frontend/app/components/clusters/index.ts`

---

## Appendix A — Validator and Test Output

### Architecture Validator
```
day_one_architecture_validation: PASS
```

### Medical Frame Identity Index Validator
```
validation_status: PASS
errors: 0
index_path: knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

### Context Modifier Catalogue Validator
```
validation_status: PASS
errors: 0
catalogue_path: knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

### Sentinel Full Scan (run_id: 87c5a2cd, 2026-06-12)
```
tests_run: 11 test files
test_counts: passed=54, failed=6, errors=0, skipped=0
pytest_exit_code: 1
governance_escalation_required: true
sentinel_note: Phase 1 — report only. No product code or governed assets were modified.
```

All 95 defect classes in `escaped_defect_pack_status`: **GUARDED**

**6 failing tests — all share a single root cause:**
```
UnitConversionError: No conversion from 'μmol/L' to base unit '\xb5mol/L' for biomarker 'urate'
  backend/core/units/registry.py:351
```

Failing tests:
1. `test_lc_s5_proving_checks.py::test_check2_alcohol_bridge_language_when_moderate_threshold_met`
2. `test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_ab_baseline_vs_statin_off_consumer_bands_align`
3. `test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_ab_statin_off_vs_on_analytical_invariants`
4. `test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_vr_baseline_vs_statin_off_consumer_bands_align`
5. `test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_lifestyle_fixture_with_partial_questionnaire_completes`
6. `test_lc_s4_statin_signal_isolation_regression.py::test_statin_on_vs_off_preserves_scoring_body_overview_framing_only`

Root cause: Test fixture files contain urate values with unit encoded as `μmol/L` (U+03BC Greek Small Letter Mu). The unit registry defines the base unit as `µmol/L` (U+00B5 Micro Sign). These are visually identical but treated as different Unicode codepoints. The registry has no conversion path between them.

### Context Runtime Execution Register
```
activated_package_count: 0
gated_inactive_package_count: 9
approval_received: false
```

### Integration Test — Stale Assertion (not a production defect)

```
FAILED tests/integration/test_clustering_orchestrator_integration.py::
  TestClusteringOrchestratorIntegration::test_clustering_result_structure

AssertionError: assert 'cluster_engine_v2' in ['rule_based', 'weighted_correlation', 'health_system_grouping']
```

The clustering engine now returns `algorithm_used = 'cluster_engine_v2'`. The integration test's expected algorithm list was written for an older engine version. This is a **test maintenance issue** — the test assertion is stale, not the engine. Classify as POST_LAUNCH_HARDENING: update the test's expected values to include `'cluster_engine_v2'`.

---

## Appendix B — Searches and Checks Performed

| Check | Method | Result |
|-------|--------|--------|
| `backend/.env` git tracking | `git ls-files backend/.env` | Not tracked |
| `backend/.env` git history | `git log -- backend/.env` | No history |
| `.gitignore` covers `.env` | `cat .gitignore \| grep -i .env` | `.env` present in gitignore |
| `backend/.env.test` tracking | `git ls-files backend/.env.test` | Tracked — localhost test creds only |
| `ClusterInsightPanel` live page imports | `grep -r "ClusterInsightPanel"` in pages/ routes/ | Not imported by any live page |
| PSI translator runtime imports | `grep -r "investigation_spec_to_promoted_signal"` | Tests, validators, egg-info only |
| `/parse` auth dependency | Read `backend/app/routes/upload.py` line 42 | No auth dependency confirmed |
| Analysis debug console.log | Read `frontend/app/services/analysis.ts` lines 96–121 | Full payload logging confirmed |
| LLM double opt-in | Read `backend/core/insights/narrative_runtime_policy.py` | Both flags required, defaults off |
| Unit registry failure | Run failing tests with `--tb=short` | Unicode mu character collision confirmed |

---

## Appendix C — Files Inspected (Full List)

```
backend/.env.test
backend/app/routes/analysis.py
backend/app/routes/upload.py
backend/core/insights/narrative_runtime_policy.py
backend/core/insights/synthesis.py
backend/env.example
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/activation_compile_gap_report.md
docs/architecture/intelligence_authority_inventory.md
docs/architecture/psi_coverage_and_manifest_opt_in_report.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_architecture_delta_report.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/audit-papers/CONTEXT-RUNTIME-1_context_threading_and_runtime_snapshot.md
docs/audit-papers/CONTEXT-THREADING-1_context_threading_implementation.md
docs/sprints/launch_core_carry_forward_register.md
frontend/.env.local.example
frontend/app/(app)/results/page.tsx
frontend/app/components/clusters/ClusterInsightPanel.tsx
frontend/app/components/clusters/ClusterSummary.tsx
frontend/app/components/clusters/index.ts
frontend/app/lib/legacyInsightsVisibility.ts
frontend/app/lib/supabase.ts
frontend/app/services/analysis.ts
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
sentinel/packs/day_one_architecture_guardrails_v1.json
sentinel/reports/sentinel_run_87c5a2cd.json
```
