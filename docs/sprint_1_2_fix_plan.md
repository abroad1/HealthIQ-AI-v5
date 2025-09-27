# 🚧 FIX_SPRINT_PLAN.md

## 🌟 Purpose
This plan exists to **repair and complete all missing deliverables from Sprint 1–2**, as verified in the validated codebase report dated **2025-09-22**.

Although foundational infrastructure is in place, **core functionality is still missing or incomplete**. This fix sprint will ensure:
- All backend functionality is implemented and tested
- All frontend state management and services are functional
- Test coverage meets the original Definition of Done
- SSOT schema validation is in place
- CI/CD, coverage, and test reporting pipelines are fully operational

Estimated effort: **2–3 days of focused development**.

---

## ✅ Overview of Fix Priorities

### ✅ Priority 1: Backend Test Failures (8 Failures)
- **Location:** `tests/unit/test_biomarker_service.py`, `tests/unit/test_user_service.py`
- **Root causes:** Missing keys, improperly configured mocks, incomplete validation logic
- **Fix tasks:**
  - [ ] Fix `TypeError: argument of type 'Mock' is not iterable`
  - [ ] Ensure `validate_biomarker_panel()` returns `score` key
  - [ ] Patch test mocks with correct fields (e.g., `.name` instead of `Mock(name="...")`)
  - [ ] Implement type checks in `UserService.validate_user_data()`

### ✅ Priority 2: Zustand Store Logic (Scaffolded Only)
- **Files:**
- `frontend/state/analysisStore.ts`
- `frontend/state/clusterStore.ts`
- `frontend/state/uiStore.ts`
- **Fix tasks:**
  - [ ] Implement business logic in each store
  - [ ] Include TypeScript interfaces
  - [ ] Ensure state reflects backend analysis workflow phases (e.g. ingestion, normalization, scoring, etc.)
  - [ ] Wire up `devApiProbe.tsx` to display store state transitions

### ✅ Priority 3: Frontend API Services (Stubbed)
- **Files:**
  - `frontend/app/services/analysis.ts`
  - `frontend/app/services/auth.ts`
  - `frontend/app/services/reports.ts`
- **Fix tasks:**
  - [ ] Implement real `fetch` or `axios` logic
  - [ ] Add proper TypeScript types for inputs/outputs
  - [ ] Include loading, error, and success state support
  - [ ] Integrate with Zustand stores

### ✅ Priority 4: SSOT YAML Schema Validation (Missing)
- **Files:** `backend/ssot/` (and new validation module)
- **Fix tasks:**
  - [ ] Define schema using `pydantic` or `cerberus`
  - [ ] Validate `biomarkers.yaml`, `ranges.yaml`, `units.yaml` on load
  - [ ] Add CLI utility to run validation
  - [ ] Add test coverage for schema validation
  - [ ] Log and flag any invalid SSOT entries

### ✅ Priority 5: Test Coverage Reporting & Targets

#### Backend:
- **Coverage target:** ≥Critical path coverage 60% for canonical engine + services
- **Fix tasks:**
  - [ ] Add missing tests for:
    - `core/clustering/engine.py`
    - `core/clustering/rules.py`
    - `core/insights/base.py`, `registry.py`
    - `core/dto/builders.py`
    - Error-handling paths in services
  - [ ] Generate coverage report with `pytest-cov`
  - [ ] Integrate with Codecov via GitHub Actions

#### Frontend:
- **Coverage target:** ≥Critical path coverage 60%
- **Fix tasks:**
  - [ ] Fix Jest config typo: `moduleNameMapping` ➞ `moduleNameMapper`
  - [ ] Add component tests for:
    - `ClusterCard.tsx`
    - `BiomarkerChart.tsx`
    - `InsightPanel.tsx`
    - `PipelineStatus.tsx`
  - [ ] Generate coverage via `jest --coverage`
  - [ ] Push results to Codecov

### ✅ Priority 6: Test Ledger & Archive Updates
- [ ] Update `TEST_LEDGER.md` with:
  - Current failures
  - Updated test results
  - Coverage summaries
- [ ] Archive failed test outputs (2025-09-22 run)
- [ ] Record new tests written in this sprint

---

## 📅 Timeline (Recommended)

| Day | Task | Owner |
|-----|------|-------|
| Day 1 AM | Fix all 8 backend test failures | Cursor |
| Day 1 PM | Implement Zustand store logic | Cursor |
| Day 2 AM | Implement frontend services | Cursor |
| Day 2 PM | Add SSOT schema validation | Cursor |
| Day 3 AM | Achieve test coverage targets (backend + frontend) | Cursor |
| Day 3 PM | Final test pass, update test ledger, CI validation | Cursor |

---

## 🎯 Definition of Done (Sprint 1-2 Fix Completion)

- [ ] 78/78 backend tests passing
- [ ] Backend coverage ≥Critical path coverage 60%
- [ ] Frontend coverage ≥Critical path coverage 60%
- [ ] Zustand stores contain real logic
- [ ] Frontend services are functional and type-safe
- [ ] SSOT YAML schema validation implemented and passing
- [ ] CI/CD pipeline green with coverage reports
- [ ] Test ledger updated and archived

---

## 🔧 Cursor Execution Prompt
```
You are to implement the Sprint 1-2 Fix Plan as defined in FIX_SPRINT_PLAN.md.

Begin with Phase 1:
1. Fix all failing backend tests
2. Re-run backend tests using `scripts/tests/run_backend_tests.ps1`
3. Update TEST_LEDGER.md with new results

Confirm completion before moving to Phase 2.
```

---

## 🚀 Summary
This plan restores full alignment with the original Sprint 1–2 Definition of Done and provides a **complete, verifiable, and auditable development path**. Cursor must execute each phase sequentially and validate with tests.

Once complete, we can **lock Sprint 1-2** and confidently proceed to Sprint 3 with a working, tested, production-grade baseline.

