# ARCH-GOV-BASELINE-1 — Implementation and Verification Report

**Work ID:** ARCH-GOV-BASELINE-1  
**Branch:** `feature/arch-gov-baseline-1-programme-baseline-governance-reset`  
**Date:** 2026-07-25  
**Role:** Cursor (healthiq-core-engine) — implementation only; no self-certification of merge readiness beyond command evidence.

---

## 1. Executive outcome

Programme baseline and governance reset implemented within authorised scope: authority map reconciled, current-state baseline published, stale continuity/MR-BATCH docs corrected, historical governance exceptions recorded, RT-5D and golden-panel stale expectations refreshed to live estate/signatures, and `golden_gate.yml` protected-branch coverage extended to `main`/`develop` without duplicating CI jobs. No product runtime or medical content changed.

---

## 2. Pre-change authority table

| Authority question | Finding |
|---|---|
| Automation Bus SOP | `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` — LOCKED, authoritative |
| Knowledge Bus SOP | `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` exists (LOCKED); AUTHORITY_MAP previously pointed at v1.3 |
| Pass 3 protocol | `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` — Status DRAFT FOR GOVERNANCE REVIEW; absent from AUTHORITY_MAP |
| Pre-SOP workflow | `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md` exists; AUTHORITY_MAP cited non-existent v0_4 |
| Continuity register | `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` |
| Day-one carry-forward | `_FINAL_updated.md` current; `_FINAL.md` also present (superseded variant) |
| SPRINT_STATUS | Self-declared LIVE as of 2026-05-04 — stale |
| Duplicate authority risk | KB SOP v1.3 and v1.3.1 coexisted with map pointing at older; corrected by classification not by inventing a new SOP |

---

## 3. Reality-check results

| Claimed defect | Still present pre-change? | Evidence |
|---|---|---|
| AUTHORITY_MAP stale/conflicting | YES | KB SOP v1.3; missing v0_4; no Pass 3 entry |
| Pass 3 still DRAFT | YES | Header Status DRAFT |
| SPRINT_STATUS stale | YES | LIVE header 2026-05-04 |
| MR-BATCH completion/output conflict | YES | “Medical review then promote” recommendations |
| automation_bus latest_* stale vs HEAD | YES at session open | Status COMPLETE for P3-PROSE-DEPTH-1; superseded by this WP start |
| knowledge_bus/current/latest_knowledge_status.json | ABSENT | Only `.gitkeep` |
| RT-5D stale inventory | YES | 191≠186; 147≠142; 72≠67; 10≠7 |
| Golden-panel stale mocks/strings | YES | missing `runtime_context`; interpretation string drift |
| golden_gate.yml missing main/develop push | YES | Only `sprint17/...` on push; PR had no branch filter |
| Bilirubin regression | PASS retained | See §8 |
| Architecture / launch gates pre-change | PASS | Exit 0 |

No STOP condition triggered. Golden-panel failures classified as **stale tests**, not production defects.

---

## 4. Files changed

### Setup (pre-start, governed clean tree)

- `automation_bus/latest_cursor_prompt.md`
- `automation_bus/latest_prompt_hardening.json`
- `docs/audit-papers/CURSOR_sprint_governance_and_codebase_maturity_audit.md`
- `docs/audit-papers/CLAUDE_CODE_sprint_governance_and_codebase_maturity_audit.md`
- `docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md`
- `docs/audit-papers/CLAUDE_CODE_independent_executable_architecture_assurance_audit.md`

### Implementation

- `docs/AUTHORITY_MAP.md`
- `docs/SPRINT_STATUS.md`
- `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` (new)
- `docs/audit-papers/ARCH-GOV-BASELINE-1_historical_governance_exception_record.md` (new)
- `docs/audit-papers/ARCH-GOV-BASELINE-1_implementation_and_verification_report.md` (this file)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md`
- `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_test_output.md`
- `backend/tests/unit/test_arch_rt5d_package_provenance.py`
- `backend/tests/unit/test_golden_panel_runner.py`
- `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py` (directly related: output generator was overwriting Deliverable D supersession notes)
- `.github/workflows/golden_gate.yml`

---

## 5. Exact changes by deliverable

| Deliverable | Change |
|---|---|
| A Baseline | New current-state baseline with required maturity statements |
| B Authority map | KB SOP → v1.3.1; pre-SOP → v0.6.2; Pass 3 DRAFT; baseline; day-one; audit EVIDENCE; SPRINT_STATUS STALE |
| C SPRINT_STATUS | Superseded banner; historical body preserved |
| D MR-BATCH-001B | Supersession notes; struck medical-review promotion recommendations; assets untouched |
| E Exception record | Honest missing-lifecycle record; non-precedential |
| F Tests | RT-5D counts 191/147/72/10; golden interpretation + `runtime_context` stub |
| G CI | `golden_gate.yml` PR/push → `main`, `develop` (+ retain sprint17 push); NO-LLM steps preserved |
| H Verification | Commands in §8 |
| I Build register | ARCH-GOV-BASELINE-1 entry appended |

---

## 6. Before/after failing-test evidence

### RT-5D (before)

```
FAILED test_all_packages_classified — assert 191 == 186
FAILED test_classification_counts_match_inventory — assert 147 == 142
FAILED test_kb52c_packages_classified_batch_blocked — assert 72 == 67
FAILED test_estate_index_covers_launch_artefacts — assert 10 == 7
```

### RT-5D (after)

```
.................. [100%]  exit 0
```

### Golden panel (before)

```
FAILED test_primary_markers_never_use_policy_or_ssot_ranges
  expected "Not scored - no reference range available"
  actual   "Not scored - missing_lab_reference_range"
FAILED test_golden_panel_signal_results_carry_explanation_metadata
  TypeError: _stub_evaluate_all() got unexpected keyword argument 'runtime_context'
  → ValueError: stamped explainability_report missing (cascade)
```

### Golden panel (after)

```
.. [pair] exit 0; full file exit 0 (see §8)
```

Authority for refreshed counts: live `scan_all_package_provenance()` / `estate_index_v1.yaml`.  
Authority for interpretation string: `backend/ssot/scoring_policy.yaml` `unscored_reason_missing_lab_reference_range`.  
Authority for mock signature: `SignalEvaluator.evaluate_all(..., runtime_context=...)`.

---

## 7. CI trigger comparison

| Workflow | Before | After |
|---|---|---|
| `golden_gate.yml` pull_request | all PRs (no branch filter) | `main`, `develop` |
| `golden_gate.yml` push | only `sprint17/biomarker-expansion-ab-panel` | `main`, `develop`, + retained sprint17 |
| `ci.yml` | already push/PR on `main`/`develop` (unit suite; not the golden NO-LLM pack) | unchanged — no duplicate golden job layered |

NO-LLM enforcement steps in `golden_gate.yml` retained (`HEALTHIQ_ENABLE_LLM=0`, Gemini log grep).

---

## 8. Commands executed and exit codes

Pre-change / Phase 1:

| Command | Exit |
|---|---|
| `python backend/scripts/validate_day_one_architecture.py` | 0 |
| `python backend/scripts/validate_day_one_launch_estate_gate.py` | 0 |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| `python -m pytest backend/tests/unit/test_arch_rt5d_package_provenance.py -q` | 1 (before) |
| `python -m pytest backend/tests/unit/test_golden_panel_runner.py -q` | 1 (before; 2 failures) |

Post-change verification (recorded exit codes):

| Command | Exit |
|---|---|
| `python backend/scripts/validate_day_one_architecture.py` | 0 |
| `python backend/scripts/validate_day_one_launch_estate_gate.py` | 0 |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| `python -m pytest backend/tests/unit/test_arch_rt5d_package_provenance.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_golden_panel_runner.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_wave1_liver_marker_mapping_fix.py -q` | 0 |
| `python -m pytest backend/tests -k "mr_batch_001b or arch_rt5e" -q` | 0 |

---

## 9. Acceptance-criteria table

| Criterion | Status |
|---|---|
| AUTHORITY_MAP points to correct current governance docs | Met |
| No non-existent pre-SOP file presented as authoritative | Met |
| KB SOP v1.3.1 correctly classified | Met |
| Pass 3 retains honest DRAFT status | Met |
| SPRINT_STATUS marked superseded/stale | Met |
| Audit papers classified as evidence | Met |
| Baseline exists with evidence-backed claims | Met |
| No unsupported percentages | Met |
| Stage 0 directed to baseline | Met |
| MR-BATCH docs not authorising medical review/promotion | Met |
| Candidate assets unchanged | Met |
| Exception record honest / non-precedential | Met |
| RT-5D / golden / bilirubin / PSI isolation / gates | Met (all exit 0; see §8) |
| golden_gate covers protected flow without unnecessary duplication | Met |
| NO-LLM intact | Met |
| No product runtime / medical / package / PSI / Gemini activation / next-sprint authorship | Met |

---

## 10. STOP-condition assessment

None triggered. Notably STOP #4 (golden-panel real production defect) was evaluated and rejected: failures were stale string + stale mock signature only.

---

## 11. Remaining unknowns

- Full end-to-end multi-frame consumer completeness remains incomplete (documented in baseline; no new replay subsystem invented).
- Formal Pass 3 ratification still requires human governance decision.
- Whether any historical `.env` secret rotation is needed remains UNKNOWN_REQUIRES_REVIEW per independent audits (out of scope).

---

## 12. Carry-forwards for later Stage 0 planning

- Start from this baseline.
- Do not treat MR-BATCH-001B as promotion source.
- Do not treat Pass 3 protocol as APPROVED until ratified.
- Planning gate (e.g. SPRINT-BUILD-PLAN-AUDIT-1) remains a candidate planning action — not selected or authored here.

---

## 13. Confirmation — no product runtime or medical content changed

Confirmed: no edits under `backend/core/`, `backend/ssot/`, `backend/app/`, `knowledge_bus/packages|compiled|root_cause|pathway_explainers_v1|functional_explainers_v1/`, or `frontend/app/`. Candidate prose YAML untouched. PSI/Gemini not activated. No next implementation sprint selected or authored.
