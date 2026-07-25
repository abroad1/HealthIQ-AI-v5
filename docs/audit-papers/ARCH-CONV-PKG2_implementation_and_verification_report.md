# ARCH-CONV-PKG2 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKG2`  
**Branch:** `feature/arch-conv-pkg2-provenance-reachability`  
**Baseline HEAD (kernel start):** `d696fca3ba5483ae59d547a55a817c9284b2e981`  
**change_type:** MIXED  
**runtime_change:** YES  
**STOP Gate 1:** PASS  
**Gate 2 recommendation:** **GO**

---

## 1. Outcome

Closed the launch-critical provenance / runtime-reachability mismatch for the Gate 0 `pkg_kb47_*` cohort:

- Wave 1 INCLUDE (6): explicit Pass 3 lineage attached; production-reachable with `EXPLICIT_SPEC`.
- Androgen + CK/eos (14): remain on disk; **non-reachable** on the production registry path; test opt-in retained.
- Canonical eligibility decision at load time (`package_runtime_eligibility_v1`).

No WHY, prose, PSI, Gemini, threshold, or firing-logic changes. No architecture-completion or beta-readiness claim.

---

## 2. Files changed

| Path | Role |
|---|---|
| `backend/core/knowledge/package_runtime_eligibility_v1.py` | Canonical production eligibility |
| `backend/core/analytics/signal_evaluator.py` | Enforce eligibility in `SignalRegistry._load`; audit exclusions |
| `knowledge_bus/research/investigation_specs/inv_free_t3_*.yaml` (2) | Wave 1 inv specs extracted from Pass 3 |
| `knowledge_bus/research/investigation_specs/inv_free_t4_*.yaml` (2) | Wave 1 inv specs |
| `knowledge_bus/research/investigation_specs/inv_egfr_low_*.yaml` (2) | Wave 1 inv specs |
| `knowledge_bus/packages/pkg_kb47_{free_t3,free_t4,egfr}_*/package_manifest.yaml` (6) | `source_spec_id` / `activation_key` / `lineage_attach_work_id` |
| `backend/scripts/validate_launch_critical_provenance_reachability_gate.py` | Behavioural reachability gate |
| `backend/scripts/run_architecture_validation_gate.py` | Wire new gate |
| `backend/tests/unit/test_arch_conv_pkg2_provenance_reachability.py` | Acceptance coverage |
| `docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md` | Phase 1 decisions + STOP Gate 1 |
| `docs/architecture/ARCH-CONV-PKG2_runtime_suppression_impact_report.md` | Golden / impact + approvals |
| `docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md` | Regenerated inventory (Wave 1 no longer BLOCKED) |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Continuity entry |
| This report | Verification |

---

## 3. Package-by-package decisions

| Disposition | Count | Packages |
|---|---:|---|
| ATTACH_EXPLICIT_LINEAGE + KEEP_REACHABLE | 6 | free_t3×2, free_t4×2, egfr×2 |
| MAKE_NON_REACHABLE | 14 | androgen×8, CK×2, eos×4 |
| Unresolved | 0 | — |

**Lineage sources:** exact frames from `Batch_2_Pass_3.json` → standalone `inv_*.yaml`. No invented `source_spec_id`.

---

## 4. Runtime policy before / after

| Aspect | Before | After |
|---|---|---|
| Provenance classification | Offline / inventory only | Still used; now drives load |
| Production `pkg_kb47_*` load | All 20 with BLOCKED provenance | 6 EXPLICIT_SPEC only |
| Blocked packages fire/rank | Possible if biomarkers/gates pass | Impossible on production registry |
| Test fixtures | Same as production | `allow_launch_critical_blocked=True` or env opt-in |
| Non-kb47 packages | Unchanged | Unchanged (`out_of_launch_critical_cohort`) |

Live counts: production registry **183** signals (6 kb47); opt-in **197** (20 kb47); excluded audit rows **14**.

---

## 5. Golden-output impact

See `ARCH-CONV-PKG2_runtime_suppression_impact_report.md`.

- `golden_panel_160`: no user-visible delta for suppressed families under fixture values.
- Forced CK stress: fires only under opt-in — intended.
- Wave 1 not suppressed.

---

## 6. Human approvals

| Approval | Source |
|---|---|
| Keep Wave 1 reachable + attach lineage | Gate 0 INCLUDE (merged) |
| Make androgen non-reachable | Gate 0 EXCLUDE_FROM_BETA / medical-review |
| Make CK/eos non-reachable | Gate 0 DEFER |
| STOP Gate 1 PASS | Package 2 decision inventory |

---

## 7. Test commands and results

| Command | Exit |
|---|---:|
| `python -m pytest backend/tests/unit/test_arch_conv_pkg2_provenance_reachability.py backend/tests/unit/test_arch_conv_pkg1_frame_identity.py backend/tests/unit/test_arch_rt_identity_prov_1.py -q` | 0 |
| `python backend/scripts/validate_launch_critical_provenance_reachability_gate.py` | 0 |
| `python backend/scripts/validate_identity_provenance_gate.py` | 0 (warnings for remaining BLOCKED non-Wave-1 assets on disk) |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| `python -m pytest backend/tests/regression/test_batch2_thyroid_tsh_gating.py backend/tests/regression/test_context_threading.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_signal_evaluator.py::test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures -q` | 1 (pre-existing: `ab_n9b_lifestyle_bridge` fixture lacks biomarkers/user after normalise — unrelated to PKG2) |

---

## 8. Acceptance criteria

| Criterion | Status |
|---|---|
| Gate 0 cohort used without silent expansion | PASS |
| Every affected package has documented disposition | PASS |
| STOP Gate 1 passed or escalated | PASS |
| Every reachable launch-critical package has explicit lineage | PASS |
| Every launch-critical package without acceptable lineage is non-reachable | PASS |
| No blocked package can fire or rank on production path | PASS |
| One canonical loader eligibility policy | PASS |
| No user-visible finding removed without impact review/approval | PASS |
| Golden/representative changes documented | PASS |
| Replay/report provenance deterministic and explicit for reachable results | PASS |
| Package 1 frame-identity intact | PASS |
| Relevant tests and validation gates pass | PASS |
| No WHY/prose/PSI/Gemini/threshold scope | PASS |
| No architecture-completion or beta-readiness claim | PASS |

---

## 9. STOP-condition assessment

| Condition | Result |
|---|---|
| Wave 1 finding removed without approval | Not triggered |
| Lineage invention required | Not triggered |
| Scope >25% growth | Not triggered |
| Unplanned mandatory follow-ons | None beyond Gate 2.5 MR confirmation (pre-existing) |
| Cohort isolation failure | Not triggered |
| Medical signal logic change required | Not triggered |
| Unresolved output regressions | None observed |
| Unexplained gate failure | Not triggered |
| Package 3 medical-content prerequisite | Not triggered |

---

## 10. Gate 2 recommendation

**GO** — Package 2 provenance/reachability obligation is closed. Proceed to Gate 2.5 medical-review owner confirmation before Package 3B. Do not merge without explicit human authority.

---

## 11. Unresolved limitations

- Non–Wave-1 kb47 assets remain on disk with BLOCKED provenance (by design); identity inventory still warns on those assets.
- Governance “active” androgen packages in context-gate catalogues are unchanged; production `SignalRegistry` excludes them.
- Estate-wide non-kb47 provenance enforcement is out of scope.
