# LC-S9B — Launch-Core Proving Closeout Notes

**work_id:** LC-S9B  
**branch:** `launch-core/lc-s9b-proving-closeout`  
**risk:** HIGH (MIXED)  
**date:** 2026-05-16  

## Authority preflight (recorded)

| Surface | Authoritative path |
|---------|-------------------|
| Proving harness | `backend/tools/launch_core_proving_harness.py` |
| AB/VR matrix | `backend/tests/fixtures/proving/launch_core_matrix.json` |
| Panel fixtures | `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`, `vr_full_panel_with_ranges.json` |
| Lifestyle fixture | `backend/tests/fixtures/lifestyle_minimal.json` |
| Statin questionnaire | Matrix `statin_on` / `statin_off` + `STATINS_LONG_TERM_MEDICATION_LABEL` |
| WHY fallback | `backend/core/analytics/root_cause_compiler_v1.py` |
| Clinician report | `backend/core/analytics/report_compiler_v1.py` |
| Frontend results | `frontend/app/lib/resultsPageLayout.ts`, `clinicianPage1Placeholders.ts` |
| CHECK 2/4/5/6 | `backend/tests/regression/test_lc_s5_proving_checks.py` |

**Stash (governed):** `stash@{0}` LC-S1 frontend env on `feature/questionnaire-visual-redesign` — retained, unrelated; no convenience stash used.

---

## Phase 1 — Refresh proving evidence

**Command:** `python backend/tools/launch_core_proving_harness.py`  
**Result:** PASS — regenerated `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` and `latest_fingerprints.json` (stamp `20260516T203902Z`, git `b8e77e3` at harness run).

**Matrix runs present:** AB/VR × baseline, lifestyle_context, statin_off, statin_on (8 runs).

**Findings:**

- Lead family: **Homocysteine Elevation Context** on all eight runs.
- Statin invariants: top findings, signal states, band labels match off/on (PASS in report).
- Statin payoff: intervention absent→present; CV `consequence_sentence` differs on statin_on (PASS).
- Lifestyle: `narrative block differs=True` for AB and VR baseline vs lifestyle_context.

**Next phase:** Safe to enter Phase 2.

---

## Phase 2 — Binary CHECK automation

**Commands:** `python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py -q`

**Changes:**

- Added `test_check4_statin_intervention_and_bounded_framing_from_fingerprints` (CV consequence framing).
- Added `test_check2_lifestyle_context_narrative_differs_from_baseline`.
- Existing CHECK 2 orchestrator test, CHECK 5, CHECK 6 retained.

**Result:** PASS (7 tests in module).

**Fixture:** `lifestyle_minimal.json` alcohol_units_per_week 7 → 10 (moderate threshold for matrix lifestyle scenario).

**Next phase:** Safe to enter Phase 3.

---

## Phase 3 — WHY / fallback trust correction

**Problem:** Consumer surfaces showed `No governed WHY for signal_*` via `top_hypothesis_line` / legacy payloads.

**Change:** `root_cause_compiler_v1.py` — governed honest fallback title/summary without internal signal IDs or activation debug strings.

**Frontend:** `sanitizePrimaryConcernForDisplay` + extended `sanitizeTopHypothesisLineForDisplay` for legacy API payloads.

**Tests:** `test_engine_trust_r1`, `test_report_compiler_v1` — PASS after fix.

**Next phase:** Safe to enter Phase 4.

---

## Phase 4 — Visible lifestyle/statin payoff

**Evidence (fingerprints + PROVING_REPORT):**

| Payoff | Result |
|--------|--------|
| Lifestyle narrative differs vs baseline | PASS (AB, VR) |
| Lifestyle bridge language | PASS (CHECK 2 matrix + orchestrator tests) |
| Statin intervention present only when on | PASS |
| Analytical invariants preserved statin off/on | PASS |
| User-visible statin caveat | PASS (cardiovascular consequence_sentence) |

**No new modifier system invented.**

**Next phase:** Safe to enter Phase 5.

---

## Phase 5 — Human walkthrough pack and verdict

**Deliverable:** `docs/audit-papers/LC-S9B_human_walkthrough_pack.md`

### Final Sprint 5 closeout decision

```text
SPRINT_5_PASS_WITH_GAPS
```

**Rationale:**

- Launch-core AB/VR matrix passes automated proving harness and CHECK 2/4/5/6 on current build.
- Visible lifestyle and statin payoff demonstrated on real pipeline outputs.
- Raw internal WHY fallback strings removed from governed fallback path and consumer sanitizers.
- **Gaps:** Named human sign-off not completed in this session; not every lead has full governed WHY assets (honest fallback only); full `pytest backend/tests` not used as gate; legacy_v1 consumer CHECK 4 (Jest) unchanged from lc_s5 preflight.

**Recommended next work package:** Governed WHY asset completion for launch-core lead signals still on fallback (programme-owned), plus optional human sign-off on walkthrough pack.

---

## Files changed

| File | Phase |
|------|-------|
| `backend/core/analytics/root_cause_compiler_v1.py` | 3 |
| `backend/tests/fixtures/lifestyle_minimal.json` | 1/4 |
| `backend/tests/fixtures/proving/launch_core_matrix.json` | 1 |
| `backend/tests/regression/test_lc_s5_proving_checks.py` | 2 |
| `backend/tests/unit/test_report_compiler_v1.py` | 3 |
| `frontend/app/lib/clinicianPage1Placeholders.ts` | 3 |
| `frontend/app/lib/bodyOverviewPrimarySentence.ts` | 3 |
| `frontend/app/lib/resultsPageLayout.ts` | 3 |
| `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` | 1 (generated) |
| `docs/audit-papers/launch-core-proving/latest_fingerprints.json` | 1 (generated) |
| `docs/audit-papers/LC-S9B_human_walkthrough_pack.md` | 5 |
| `docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md` | all |

## Validation run

```text
python backend/tools/launch_core_proving_harness.py  → exit 0
python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py \
  backend/tests/regression/test_lc_s4_statin_signal_isolation_regression.py \
  backend/tests/unit/test_engine_trust_r1.py \
  backend/tests/unit/test_report_compiler_v1.py -q  → 19 passed
cd frontend && npm run type-check  → pass
```

## Residual risk

- LC-S8D/FE-S8E not reopened; no unit-governance edits.
- Mixed-unit sentinel fixture may still rank leads without full WHY (fallback is non-speculative).
- Human walkthrough sign-off pending.
