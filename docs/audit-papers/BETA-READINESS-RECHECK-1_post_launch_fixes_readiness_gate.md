# BETA-READINESS-RECHECK-1 — Post Launch-Fixes Readiness Gate

**Date:** 2026-06-14  
**Reviewer:** Claude Code  
**Sprint:** Read-only re-check post merge of `WAVE1-PUBLIC-LAUNCH-FIXES-1`

---

## Executive verdict

**VERDICT: NOT_READY_PENDING_BLOCKERS**

A critical security defect exists on `main`: two files containing real production credentials (`GEMINI_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_PASSWORD`, full `DATABASE_URL`) are committed to git — `.env` and `old.env(copy)`. This is a hard BETA_BLOCKER per STOP condition 12.

All four Wave 1 remediation items (CB-1 through CB-4) are confirmed CLOSED on `main`. All architecture validators pass. All context-dependent packages remain inactive. The committed-secrets defect is pre-existing and was not introduced by the WAVE1 fixes sprint, but it must be resolved and independently verified before proceeding to any controlled beta environment.

**Do not proceed to BETA-ENV-SMOKE-1 until the committed-secrets blocker is resolved.**

---

## Repository baseline

| Field | Value |
|---|---|
| Branch | `main` |
| HEAD | `f6054d4` |
| Working tree | Clean (0 modified, 0 staged, 0 untracked) |
| WAVE1-PUBLIC-LAUNCH-FIXES-1 merged | Yes — commit `77221cb fix(launch): remediate Wave 1 public launch blockers` |
| Latest remediation audit paper | Present at `docs/audit-papers/WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation.md` |

---

## Source documents inspected

- `docs/audit-papers/WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation.md`
- `docs/audit-papers/WAVE1-LAUNCH-READINESS-1_product_readiness_and_release_gate.md` (via prior context)
- `docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md` (via prior context)
- `docs/sprints/launch_core_carry_forward_register.md` (not read — not referenced as a blocker dependency)
- `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md` (not read — architecture validators PASS)

---

## Remediation closure check

### CB-1 — Frontend PII console logging

**File inspected:** `frontend/app/services/analysis.ts`

Grep for `console.log`, `console.group`, `console.groupEnd`: **no matches found**.

The only `JSON.stringify(data)` occurrence (line 104) is the fetch request body — not console logging. No biomarker values, questionnaire data, user demographics, or debug trace blocks remain in `startAnalysis()`.

**Classification: CLOSED**

---

### CB-2 — Upload parse authentication

**Files inspected:** `backend/app/routes/upload.py`, `backend/app/routes/analysis.py`

`POST /api/upload/parse` (upload.py:44-48):
```python
@router.post("/parse")
async def parse_upload(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None),
    _auth_user: CurrentUser = Depends(require_analysis_submitter),
```

`POST /api/analysis/start` (analysis.py:94-98):
```python
@router.post("/start", response_model=AnalysisStartResponse)
async def start_analysis(
    request: AnalysisStartRequest,
    auth_user: CurrentUser = Depends(require_analysis_submitter),
```

Both endpoints use the same `require_analysis_submitter` auth dependency. No new parallel auth mechanism was introduced.

**Note:** `POST /api/upload/validate` (upload.py:196) has no auth dependency. This was flagged as out of scope in the prior remediation audit. It is carried forward as a condition.

**Classification: CLOSED** (for `/parse`; `/validate` is a separate tracked condition)

---

### CB-3 — Unicode unit normalisation

**File inspected:** `backend/core/units/registry.py`

`normalize_unit_token()` (registry.py:109-114) present:
```python
def normalize_unit_token(unit: str) -> str:
    token = (unit or "").strip()
    if not token:
        return token
    return token.replace(_GREEK_SMALL_MU, _MICRO_SIGN)
```

Constants defined at registry.py:105-106:
```python
_GREEK_SMALL_MU = "μ"
_MICRO_SIGN = "µ"
```

`_UMOL_EQUIVALENTS` frozenset (registry.py:102) includes `µmol/L`, `umol/L`, `uMol/L`. `_unit_in_equivalent_set()` normalises before comparison, ensuring Greek mu (U+03BC) and micro sign (U+00B5) resolve to the same token.

Unit registry test suite: **45 passed, 0 failed**.

Urate conversion path (registry.py:301-316) uses `_unit_in_equivalent_set(to_u, _UMOL_EQUIVALENTS)` for both directions, ensuring urate values encoded with either mu character convert identically.

**Classification: CLOSED**

---

### CB-4 — Billing env safety

**File inspected:** `backend/env.example`

```ini
# Free completed analyses for users without an active subscription.
# Production-safe default:
HEALTHIQ_FREE_COMPLETED_ANALYSES=1

# Skip POST /api/analysis/start billing/paywall (402) entirely; environment flag only.
# Must remain disabled (0) outside explicit local development.
HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=0

# Local development only. Do not enable in production.
# HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1
# HEALTHIQ_FREE_COMPLETED_ANALYSES=99
```

Active defaults: `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=0`, `HEALTHIQ_FREE_COMPLETED_ANALYSES=1`. Dev bypass values are commented and clearly marked "Local development only. Do not enable in production."

**Classification: CLOSED**

---

## Architecture guardrails

All validators run from `main` HEAD (`f6054d4`):

```
run_architecture_validation_gate.py          → architecture_validation_gate: PASS
validate_day_one_architecture.py             → day_one_architecture_validation: PASS
validate_medical_frame_identity_index.py     → validation_status: PASS (errors: 0)
validate_context_modifier_catalogue.py       → validation_status: PASS (errors: 0)
medical_intelligence_architecture_validation → PASS
pytest_architecture_guardrails               → PASS
pytest_governance_regression                 → PASS
```

**Classification: PASS**

---

## Context-dependent package safety

**Source:** `knowledge_bus/governance/context_runtime_execution_register_v1.yaml` and `batch2_context_clearance_register_v1.yaml`

| Check | Evidence |
|---|---|
| `activated_package_count` | 0 |
| `runtime_activation_performed` | false |
| Androgen packages (8 packages) | All `activated: false`, `final_state: compiled_not_promoted_inactive_gated` |
| FT3 low | `activated: false`, `clearance_decision: DEFERRED_NON_LAUNCH_CRITICAL` |
| `approval_received` | false (human_stop_gate) |
| CF-BATCH2-010 | Open — no clinical sign-off artefact in repo |

All 9 context-dependent packages remain inactive. No package was activated by WAVE1 remediation work. CF-BATCH2-010 remains open as expected.

**Classification: PASS**

---

## Frontend live-route safety

**Files inspected:** `frontend/app/(app)/results/page.tsx`, `frontend/app/components/clusters/ClusterSummary.tsx`, `frontend/app/components/clusters/ClusterInsightPanel.tsx`, `frontend/app/components/clusters/index.ts`

**results/page.tsx imports:**
- Line 15: `import ClusterSummary from '@/components/clusters/ClusterSummary';` — direct import, render-only
- Line 960: `<ClusterSummary clusters={clusterSummaries} isLoading={clustersLoading} showDetails={showDetails} />` — live use confirmed

`ClusterSummary` is a render-only component (no clinical inference logic). It displays server-provided cluster data without pattern matching.

**ClusterInsightPanel status:**
- `index.ts:2` exports it via the barrel
- **NOT imported in any live route or page** (grep confirms: only self-definition and barrel export)
- However, it contains `getClinicalRecommendations()` (ClusterInsightPanel.tsx:89-122) which generates clinical recommendations from frontend pattern matching on cluster names — e.g. "Immediate medical attention recommended" for severity:critical. This is frontend-authored clinical inference and would be a governance violation if it ever reached a live route.
- Current status: non-live, architectural debt to retire

**InsightPanel** (imported at results/page.tsx:11 from `@/components/insights/InsightPanel`) — a different component from `ClusterInsightPanel`. Used inside the "Advanced analysis" disclosure with `contextOnly` prop (line 944-948). Passing `contextOnly` is consistent with this being a read/display mode.

**Classification: PASS** — live results route correctly uses `ClusterSummary` only. `ClusterInsightPanel` is non-live. Barrel export of `ClusterInsightPanel` is an acceptable-for-next-sprint cleanup item.

---

## Parser and upload safety

Grep for `fallback parser`, `dummy parser`, `mock parser`, `fake parser`, `placeholder parser` across `backend/` Python files: **no matches found**.

`POST /api/upload/parse` (upload.py:69-105):
- File path: uses `LLMParser.extract_biomarkers()` 
- Text path: attempts `try_deterministic_parse()` first (canonical CSV format); falls back to `LLMParser.extract_biomarkers()` for unstructured content
- The LLM fallback is Gemini for parsing surface only (Layer C translation, not Layer B reasoning)
- Error path (upload.py:114-122): returns `success=False` with error message — does not fabricate user data

Auth on `/parse`: `Depends(require_analysis_submitter)` confirmed CLOSED (CB-2).

**Classification: PASS**

---

## Reference range and unit safety

Unit normalisation is fully deterministic. Conversion factors are loaded from `ssot/units.yaml`. No reference ranges, thresholds, or biomarker identities changed in WAVE1 fixes. All 45 unit registry tests pass.

`_STRICT_CONVERSION_BIOMARKERS` (registry.py:86-100) includes urate, creatinine, glucose, cholesterol, triglycerides, vitamin D, hemoglobin, hematocrit, calcium, magnesium, free T4, HbA1c, urea. These fail explicitly on unknown units rather than silently passing.

**Classification: PASS**

---

## Operational safety baseline

### Committed secrets — CRITICAL BLOCKER

**Finding:** Two files with real production credentials are committed to git and present on `main`.

**File 1: `.env`** (present since commit `1228c12` / `08a73d7`):
```
GEMINI_API_KEY=[REDACTED]      ← REAL key
SUPABASE_URL=https://[REDACTED].supabase.co         ← REAL project
SUPABASE_SERVICE_ROLE_KEY=[REDACTED]  ← REAL admin key
SUPABASE_PASSWORD=[REDACTED]                             ← REAL password
DATABASE_URL=[REDACTED]  ← REAL connection string
```

**File 2: `old.env(copy)`** (committed to git):
```
GEMINI_API_KEY=[REDACTED]      ← same Gemini key
SUPABASE_SERVICE_ROLE_KEY=[REDACTED]  ← REAL key (different project: [REDACTED-PROJECT-ID-2])
```

Both files have a header reading "DO NOT COMMIT THIS FILE — Contains sensitive secrets". Both are in `.gitignore` (line 56: `.env`). Despite this, both were force-added to git tracking. They remain tracked and committed.

**`SUPABASE_SERVICE_ROLE_KEY` is an admin credential that bypasses Supabase row-level security.** Exposure of this key is a critical production risk.

**Classification: BETA_BLOCKER — STOP**

### Backend debug traces

`backend/app/routes/analysis.py` lines 122-136 contain `print()` statements that will emit to server stdout in production:
```python
print("[TRACE] Incoming payload keys:", list(request.model_dump().keys()))
print("[TRACE] Biomarker count:", len(request.biomarkers))
print("[TRACE] Route received biomarkers:", list(request.biomarkers.keys()))
print("[TRACE] Questionnaire present:", questionnaire_for_run is not None)
# ...
print(f"[TRACE] Created AnalysisContext with {len(context.biomarkers)} biomarkers, user={context.user.user_id}")
```

These log: payload key names (not values), biomarker count, biomarker names (not values), questionnaire presence (boolean), biomarker count, and user UUID. No actual health values or demographic data are logged. The user_id is a UUID — arguable PII, but not health data. These are server-side only (not browser-accessible).

Classification: Not a BETA_BLOCKER for this sprint, but must be resolved before invite-only beta user access.

### Other operational safety findings

- `NEXT_PUBLIC_DEBUG=true` in production examples: not found
- `SECRET_KEY=your-secret-key-here` in `backend/env.example`: placeholder, clearly marked — acceptable
- `GEMINI_API_KEY=your-gemini-api-key-here` in `backend/env.example`: placeholder — acceptable
- `.env.test` committed (backend/.env.test): contains `GEMINI_API_KEY=test-key-123` — test placeholder, acceptable
- `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT`: confirmed `=0` in env.example — acceptable

---

## Remaining beta evidence gaps

| Gap | Classification |
|---|---|
| Committed `.env` and `old.env(copy)` with real credentials | **BETA_BLOCKER** |
| No production-like end-to-end smoke test | CONDITION_BEFORE_INVITE_ONLY_BETA |
| No beta deployment environment validation | CONDITION_BEFORE_INVITE_ONLY_BETA |
| Final user-facing disclaimer review not documented | CONDITION_BEFORE_INVITE_ONLY_BETA |
| No beta support / feedback route defined | CONDITION_BEFORE_INVITE_ONLY_BETA |
| No explicit pause / rollback criteria for beta | CONDITION_BEFORE_INVITE_ONLY_BETA |
| Backend print traces in `analysis.py` lines 122-136 | CONDITION_BEFORE_INVITE_ONLY_BETA |
| `/api/upload/validate` unauthenticated (pre-existing, not CB-2 scope) | CONDITION_BEFORE_INVITE_ONLY_BETA |
| 3 pre-existing regression test failures (maintenance backlog) | CONDITION_BEFORE_INVITE_ONLY_BETA |
| `ClusterInsightPanel` accessible via barrel export (architectural debt) | ACCEPTABLE_FOR_NEXT_SPRINT |
| `gotrue` package deprecation warning | POST_BETA_HARDENING |

---

## Beta blocker table

| ID | Finding | Classification | Evidence | Required action | Blocks next sprint? |
|---|---|---|---|---|---|
| BB-1 | Real `GEMINI_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (admin), `SUPABASE_PASSWORD`, and full `DATABASE_URL` committed to git in `.env` | BETA_BLOCKER | `git show HEAD:.env` — credentials present on `main` HEAD f6054d4 | Immediately rotate all exposed credentials. Remove `.env` from git tracking. Purge from git history (BFG / git-filter-repo). Confirm `.gitignore` enforcement | YES |
| BB-2 | Second real `SUPABASE_SERVICE_ROLE_KEY` (different project) and `GEMINI_API_KEY` in committed `old.env(copy)` | BETA_BLOCKER | `git show HEAD:old.env(copy)` — credentials present | Remove `old.env(copy)` from git tracking. Rotate the `[REDACTED-PROJECT-ID-2]` Supabase service role key | YES |

---

## Conditions before invite-only beta

| ID | Condition | Why it matters | Must resolve before invite-only beta? | Recommended owner / sprint |
|---|---|---|---|---|
| C-1 | Production-like end-to-end smoke test in a controlled environment | Cannot confirm real user journey completes correctly without live backend test | YES | BETA-ENV-SMOKE-1 |
| C-2 | Beta deployment environment validation (env vars, DB config, Supabase prod config) | Credential rotation creates a fresh config dependency | YES | BETA-ENV-SMOKE-1 |
| C-3 | Final user-facing disclaimer review | Medical information liability requires explicit disclaimer text review before real users | YES | Pre-invite |
| C-4 | Beta support / feedback route defined | Users need a known path to report issues or questions | YES | Pre-invite |
| C-5 | Pause / rollback criteria and runbook | Must know when and how to halt beta | YES | Pre-invite |
| C-6 | Backend print traces removed from `analysis.py` (lines 122-136) | User UUID and biomarker structure emitting to server logs is not production-appropriate | YES | BETA-ENV-SMOKE-1 or dedicated fix sprint |
| C-7 | `/api/upload/validate` authentication | Unauthenticated endpoint in live surface (minor — validate does not parse or store data, but inconsistent with auth model) | NO — low risk in isolation; YES if beta includes untrusted network access | Dedicated fix sprint |
| C-8 | Resolve 3 pre-existing regression test failures | `test_fe_r3_fe_r2_journey_order_preserved`, `test_fe_r5a_idl_not_duplicated_in_secondary_disclosure`, `test_lc_s11a_blood_sugar_no_unsupported_early_ir_narrative` — failures indicate stale test assertions or analytical drift | YES before invite-only beta | Test maintenance sprint |

---

## Acceptable next-sprint items

| Item | Why acceptable | When to address |
|---|---|---|
| `ClusterInsightPanel` accessible via barrel export | Non-live; not imported in any route | Architectural cleanup sprint |
| `gotrue` package deprecation warning | No impact; successor package not yet required | Post-beta dependency refresh |
| `ClusterInsightPanel.getClinicalRecommendations()` frontend pattern-matching clinical inference | Component is not live; clean up before any A/B or experimental route includes it | Before any route activation |

---

## Recommended next action

**IMMEDIATE (before any beta environment work):**

1. Rotate all exposed credentials:
   - Gemini API key (`[REDACTED]`)
   - Supabase service role key for project `[REDACTED-PROJECT-ID-1]`
   - Supabase service role key for project `[REDACTED-PROJECT-ID-2]`
   - Supabase database password (`[REDACTED]`)

2. Remove `.env` and `old.env(copy)` from git tracking:
   ```
   git rm --cached .env "old.env(copy)"
   git commit -m "chore(security): remove committed .env files from tracking"
   ```

3. Purge from git history using BFG Repo-Cleaner or `git filter-repo` to remove both files from all commits.

4. Run this beta readiness re-check again after credential rotation and history purge to confirm BETA_READY_WITH_CONDITIONS.

**After credential rotation and history purge, recommended next sprint:**

```
BETA-ENV-SMOKE-1_controlled_environment_and_end_to_end_smoke
```

Scope: deploy to controlled environment with rotated credentials, run full end-to-end user journey, confirm Wave 1 UX, resolve backend print traces, confirm billing enforcement in staging.

---

## Appendix A — Full validator and test output

### Architecture validation gate
```
architecture_validation_gate: PASS
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
validation_status: PASS (medical_frame_identity_index, errors: 0)
validation_status: PASS (context_modifier_catalogue, errors: 0)
pytest_architecture_guardrails: PASS
pytest_governance_regression: PASS
```

### Test suites
```
backend/tests/unit/test_unit_registry.py          → 45 passed, 0 failed
backend/tests/regression/test_runtime_context_evaluation.py → 35 passed (all)
backend/tests/regression/test_context_threading.py → all passed
backend/tests/integration/test_upload_api.py       → all passed

backend/tests/regression/ (full suite)            → 3 FAILED (pre-existing)
  test_fe_r3_evidence_depth_ux_quality.py::test_fe_r3_fe_r2_journey_order_preserved
    AssertionError: '<BiomarkerDials' not found in expected slice of results page source
  test_fe_r5a_limited_idl_pattern_surface.py::test_fe_r5a_idl_not_duplicated_in_secondary_disclosure
    ValueError: substring not found (IDL section assertion)
  test_lc_s11a_trust_blocker_correction.py::test_lc_s11a_blood_sugar_no_unsupported_early_ir_narrative
    AssertionError: ['signal_homocysteine_high'] != []
  1 SKIPPED (test_lc_s13_lifestyle_coherence_narrative.py — AB panel guard not applicable)
```

### Sentinel
```
sentinel/sentinel_runner.py --all
Issues found: 0 | Coverage gaps: 0 | Governance escalation required: False
```

---

## Appendix B — Searches performed

| Search | Target | Result |
|---|---|---|
| `console.(log\|group\|groupEnd\|error\|warn\|debug)` | `frontend/app/services/analysis.ts` | No matches |
| `ClusterInsightPanel` | `frontend/**/*.{tsx,ts}` | Only self-definition and barrel export — not live |
| `fallback.parser\|dummy.parser\|mock.parser\|fake.parser\|placeholder.parser` | `backend/**/*.py` | No matches |
| `NEXT_PUBLIC_DEBUG\|NEXT_PUBLIC.*=true` | `frontend/**/*.{env,example,local}` | No matches |
| `GEMINI_API_KEY\|SECRET_KEY` | `backend/env.example` | Placeholders only — acceptable |
| Committed `.env` files | `git ls-files \| grep ".env"` | `.env`, `old.env(copy)` — CRITICAL |
| `HEALTHIQ_DISABLE_BILLING_ENFORCEMENT` | `backend/env.example` | `=0` (safe default) |
| `print(\|console\.log` | `backend/app/routes/analysis.py` | Lines 122, 123, 124, 125, 136 — traces to stdout |

---

## Appendix C — Files inspected

| File | Status |
|---|---|
| `frontend/app/services/analysis.ts` | Read (340 lines) |
| `backend/app/routes/upload.py` | Read (251 lines) |
| `backend/app/routes/analysis.py` | Read (624 lines) |
| `backend/core/units/registry.py` | Read (617 lines) |
| `backend/env.example` | Read (143 lines) |
| `frontend/app/(app)/results/page.tsx` | Read (985 lines) |
| `frontend/app/components/clusters/ClusterSummary.tsx` | Read (389 lines) |
| `frontend/app/components/clusters/ClusterInsightPanel.tsx` | Read (265 lines) |
| `frontend/app/components/clusters/index.ts` | Read (2 lines) |
| `knowledge_bus/governance/context_runtime_execution_register_v1.yaml` | Read (148 lines) |
| `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml` | Read (239 lines) |
| `docs/audit-papers/WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation.md` | Read (252 lines) |
| `.env` (committed) | Read via `git show` |
| `old.env(copy)` (committed) | Read via `git show` |
