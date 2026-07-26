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
| End-to-end Layer C integrity | No incorrect/legacy logic + no Layer C medical decision logic | **FAIL to close** | Frontend BOUNDARY_LEAKs (see Layer C inventory); human UAT not yet run |
| Human UAT gate | Anthony fresh frontend UAT | **OPEN** | Mandatory STOP — plan in `docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md` |

---

## Programme audit question

> Does the complete pipeline prove Layer C receives only current, provenance-valid, activation-frame-correct and medically ratified Layer B output, and that no incorrect/blocked/rejected/retired/legacy medical logic survives into the final UX?

| Layer | Result |
|---|---|
| Layer B identity / provenance / WHY pilot | Independently re-verified **PASS** |
| Layer C medical-decision boundary | **BOUNDARY_LEAKs present** — PASS forbidden |
| Human UAT | **Not completed** — PASS forbidden |

---

## Kill-criteria assessment (automated kernel)

| Criterion | Assessment |
|---|---|
| >1 unplanned mandatory architecture package now required? | **No** for PKG1–3 Layer B. One bounded Layer C FE correction package is indicated (CORRECT path), not multiple architecture rebuilds. |
| Any package exceeded 25% scope-growth without authorisation? | **No evidence** in this audit of unauthorised PKG1–3 scope growth beyond ratified work. |
| Unresolved medical-review throughput undermine convergence? | **No** for the 10-frame pilot — Gate C complete. Estate-wide WHY beyond pilot remains open by design. |
| Overlapping authority remains? | **No** for pilot WHY keys (register-driven). Residual: intentional family-level aggregation on some launch surfaces (auditable). |
| Provenance vs reachability disagree? | **No** on production path (6 reachable / 14 blocked). Residual: env override `HEALTHIQ_ALLOW_LAUNCH_CRITICAL_BLOCKED`. |
| Layer C boundary leakage remains? | **Yes** — blocks programme PASS. |
| End-to-end clinically unexplained output? | Automated Layer B scenarios clean; FE can re-rank/invent confidence/prose — unexplained UX risk until corrected + UAT. |
| Correction would reopen closed architecture domain? | Layer C FE correction should **not** reopen PKG1–3 if bounded to presentation/ranking leaks. |

---

## Provisional programme decision (automated only)

**Not final.** Final `PASS` / `CORRECT` / `STOP` / `V6` awaits Anthony UAT.

Automated lean: **CORRECT** — Layer B convergence obligations for PKG1–3 hold; Layer C FE boundary leaks require a bounded correction package before programme closure.

Controlled-beta readiness: **not assessed** in this package.
