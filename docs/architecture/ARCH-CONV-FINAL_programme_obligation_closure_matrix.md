# ARCH-CONV-FINAL — Programme Obligation Closure Matrix

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Branch:** `audit/arch-conv-final-programme`  
**Baseline HEAD:** `522873428882d9f47093e283a3ab31dc16fcd684`  
**Auditor:** Cursor (implementation/audit execution) with disjoint independent review agents  
**Independence model:** Fresh re-execution at baseline SHA; prior PKG reports used only as corroboration

---

## Package-level obligations

| Package | Gate 0 / programme obligation | Independent result | Evidence |
|---|---|---|---|
| ARCH-CONV-PKG1 | Launch-path activation-frame identity closure (5 surfaces) | **PASS** | `validate_launch_path_frame_identity_gate.py` exit 0; `test_arch_conv_pkg1_frame_identity.py` 10/10; code review of five surfaces |
| ARCH-CONV-PKG2 | Launch-critical provenance + runtime reachability | **PASS** | `validate_launch_critical_provenance_reachability_gate.py` exit 0; production kb47=6 excluded=14 |
| ARCH-CONV-PKG3 | WHY authority migration for 5/10 pilot | **PASS** (Layer B) | `validate_compiled_why_authority_gate.py` exit 0; `test_why_authority_pkg3.py` 8/8; 9 COMPILED_ACTIVE + 1 REJECTED live-proven |
| End-to-end Layer C integrity | No incorrect/legacy logic + no Layer C medical decision logic | **FAIL** | Live UAT `e34aaedf-…`: rejected metabolic still in signals/top_findings/interventions; “methylation capacity” in clinician synthesis; FE BOUNDARY_LEAKs remain |
| Human UAT gate | Anthony fresh frontend UAT | **COMPLETE (evidence captured)** | `docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md` |

---

## Programme audit question

> Does the complete pipeline prove Layer C receives only current, provenance-valid, activation-frame-correct and medically ratified Layer B output, and that no incorrect/blocked/rejected/retired/legacy medical logic survives into the final UX?

| Layer | Result |
|---|---|
| Layer B identity / provenance / WHY pilot compile path | Independently re-verified **PASS** |
| Live end-to-end rejected-frame / wording silence | **FAIL — ACTIVE_LEAKs** |
| Layer C medical-decision boundary | **BOUNDARY_LEAKs present** — PASS forbidden |
| Human UAT | Completed inspection on real analysis |

---

## Final programme decision

**CORRECT**

PASS forbidden. STOP/V6 not selected (bounded corrections sufficient). Controlled-beta readiness not assessed.

## Kill-criteria assessment

| Criterion | Assessment |
|---|---|
| >1 unplanned mandatory architecture package now required? | **No** — one bounded CORRECT package (rejected-frame inactivation + wording + MCV co-service + FE boundary) is indicated, not multiple architecture rebuilds. |
| Any package exceeded 25% scope-growth without authorisation? | **No evidence** of unauthorised PKG1–3 scope growth beyond ratified work. |
| Unresolved medical-review throughput undermine convergence? | **No** for the 10-frame pilot — Gate C complete. Estate-wide WHY beyond pilot remains open by design. |
| Overlapping authority remains? | **Yes (residual)** — rejected metabolic still coexists with compiled B-vitamin frame in signals/rankings/interventions; legacy elevation-context WHY coexists with compiled pilot WHY. |
| Provenance vs reachability disagree? | **No** on production path for blocked kb47. |
| Layer C boundary leakage remains? | **Yes** — blocks programme PASS. |
| End-to-end clinically unexplained / unsafe wording? | **Yes** — live UAT “methylation capacity” + rejected-frame ranking. |
| Correction would reopen closed architecture domain? | CORRECT themes should extend PKG3 inactivation to non-WHY surfaces without reopening PKG1 identity design. |
