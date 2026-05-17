# LC-S10B — Protection of the Proven Launch-Core Slice

**Work ID:** LC-S10B  
**Branch:** `launch-core/lc-s10b-protect-proven-launch-core-slice`  
**Risk:** HIGH (protection / regression only — no product expansion)

## Preflight (governed)

| Item | State |
|------|--------|
| Branch | `launch-core/lc-s10b-protect-proven-launch-core-slice` |
| Kernel | START → implementation |
| Stash | `stash@{0}` LC-S1 frontend env on `feature/questionnaire-visual-redesign` — **retained, unrelated** |
| Porcelain at start | Clean after bus commit; no convenience stash |

## Authority paths

| Authority | Path |
|-----------|------|
| Proving harness | `backend/tools/launch_core_proving_harness.py` |
| Fingerprints | `docs/audit-papers/launch-core-proving/latest_fingerprints.json` |
| Matrix fixture | `backend/tests/fixtures/proving/launch_core_matrix.json` |
| CHECK 2/4/5/6 | `backend/tests/regression/test_lc_s5_proving_checks.py` |
| LC-S10B leakage guards | `backend/tests/regression/test_lc_s10b_launch_core_protection.py` |
| Statin isolation | `backend/tests/regression/test_lc_s4_statin_signal_isolation_regression.py` |
| Unit governance Sentinel | `backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py` |
| Sentinel pack (LC-S8D) | `sentinel/packs/lc_s8d_unit_governance_v1.json` |
| Sentinel pack (LC-S10B) | `sentinel/packs/lc_s10b_launch_core_protection_v1.json` |
| Uploaded-panel fidelity | `frontend/tests/lib/uploadPanelFidelity.test.ts` |
| HbA1c governance | `backend/tests/unit/test_hba1c_governance.py` |
| WHY fallback (unit) | `backend/tests/unit/test_report_compiler_v1.py` |

## Protection inventory

| Behaviour | Existing protection | Gap (pre-sprint) | Planned / done protection |
| --------- | ------------------- | ---------------- | ------------------------- |
| LC-S8D unit governance | `test_lc_s8d_unit_governance_sentinel.py`, `test_hba1c_governance.py` | None material | Verified; referenced in LC-S10B Sentinel pack |
| FE-S8E uploaded-panel fidelity | `frontend/tests/lib/uploadPanelFidelity.test.ts` | None material | Referenced in Sentinel pack; no new frontend architecture |
| LC-S9C lifestyle visible payoff | CHECK 2 matrix + orchestrator test | Baseline absence not explicit | `test_check2_baseline_has_no_lifestyle_visible_sentence` |
| LC-S9B statin bounded modifier | CHECK 4 present/absent + CV diff | `lipid_lowering_statin` class not asserted | CHECK 4 hardened + `test_lc_s4` class assertion |
| CHECK 5 band/consequence | `test_check5_wave1_consumer_domain_band_vs_consequence_consistency` | None | Unchanged; requires `consumer_domain_rows` |
| CHECK 6 lead alignment | `test_check6_clinician_retail_lead_family_alignment_ab_vr_baseline` | None | Unchanged |
| Lifestyle slug / WHY / signal_* leakage | Partial (CHECK 2 slug on lifestyle runs) | Matrix-wide scan missing | `test_lc_s10b_launch_core_protection.py` |
| Matrix `consumer_domain_rows` | Present in harness output | Not asserted in tests | `test_lc_s10b_matrix_runs_present_with_consumer_domain_rows` |

## Files changed (this sprint)

- `backend/tests/regression/test_lc_s5_proving_checks.py` — CHECK 2 baseline guard; CHECK 4 `lipid_lowering_statin` + bounded statin copy
- `backend/tests/regression/test_lc_s10b_launch_core_protection.py` — **new** matrix + leakage guards
- `backend/tests/regression/test_lc_s4_statin_signal_isolation_regression.py` — `lipid_lowering_statin` on statin_on
- `sentinel/packs/lc_s10b_launch_core_protection_v1.json` — **new** pack registry
- `docs/audit-papers/launch-core-proving/latest_fingerprints.json` — refreshed
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` — refreshed
- `docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md` — this document

**Not changed:** `backend/core/**`, SSOT, scoring, units, questionnaire, frontend runtime (protection-only).

## Tests added/updated

| Test | Role |
|------|------|
| `test_check2_baseline_has_no_lifestyle_visible_sentence` | AB/VR baseline omit LC-S9C body copy |
| `test_check4_*` (extended) | `lipid_lowering_statin` class + statin CV bounded wording |
| `test_lc_s10b_matrix_runs_present_with_consumer_domain_rows` | CHECK 4/5 fingerprint dependency |
| `test_lc_s10b_no_lifestyle_slug_or_why_fallback_leakage` | All matrix user-facing compact fields |
| `test_lc_s10b_fingerprint_sha_stamped` | Drift traceability |
| `test_lc_s4_*` (extended) | Orchestrator-level statin class |

## Sentinel

Added `sentinel/packs/lc_s10b_launch_core_protection_v1.json` mapping defect classes to pytest files. LC-S8D remains authoritative in `lc_s8d_unit_governance_v1.json` (cross-referenced, not duplicated).

## Proving harness result

Command: `python backend/tools/launch_core_proving_harness.py`  
Result: **PASS** (8 matrix runs written)

Fingerprint stamp: see `latest_fingerprints.json` → `git_short_sha` after final commit.

## Validation commands (Phase 6)

| Command | Result |
|---------|--------|
| `python backend/tools/launch_core_proving_harness.py` | PASS |
| `pytest backend/tests/regression/test_lc_s5_proving_checks.py -q` | PASS (8 tests) |
| `pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q` | PASS (3 tests) |
| `pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q` | PASS |
| `pytest backend/tests/unit/test_hba1c_governance.py -q` | PASS |
| Frontend `npm run test` | **Not run** — no frontend files changed |

## Known deferred gaps

- Full persisted-result replay Sentinel (`escaped_defects_v1` placeholder) — unchanged
- Broad WHY Wave 2 / medication ontology — out of scope
- Browser UAT re-run for FE-S8E — prior audit evidence stands; no new UAT in this sprint

## Protection verdict

**SPRINT_6_PROTECTION_COMPLETE** (implementation + regression guards; human approval and merge remain separate).

Protected slice: LC-S8D units, FE-S8E uploaded-panel fidelity (existing tests), LC-S9B CHECK 4/5/6 + statin class, LC-S9C lifestyle body_overview payoff, compact fingerprint leakage guards.
