# ARCH-CONV-PKG3 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKG3`  
**Branch:** `feature/arch-conv-pkg3-why-authority-migration`  
**Baseline HEAD (kernel start):** `d090747dac279f9983cb6a934f1a6e2128cd99c5`  
**change_type:** MIXED  
**runtime_change:** YES  
**Kernel boundary:** Gate C closed; Phases 4–6 implemented on continuation

---

## 1. Outcome

Completed Phases **1–6** for the Gate 0 / Gate 2.5 WHY pilot (exact **5** signals / **10** frames):

1. Evidence/identity prerequisites (Phases 1–3) — prior kernel  
2. Gate C pack: GPT review + Anthony ratification for all ten frames — installed  
3. Phase 4: per-`activation_key` compiled WHY authority + artefacts for approved frames  
4. Phase 5: legacy retirement register + dual-authority prevention  
5. Phase 6: validation gate, unit tests, parity + verification reports  

**Implemented only Anthony-ratified dispositions.**  
**Rejected** `signal_homocysteine_high::inv_homocysteine_high_metabolic` remains inactive (no artefact, no fallback).

---

## 2. Gate evidence

| Gate | Result |
|---|---|
| A — evidence/identity | **PASS** |
| B — compiled-authority design | **PASS** |
| C — GPT review + Anthony ratification | **PASS — COMPLETE** |

Continuation authority: **AUTHORISED** (pack annex, 2026-07-26).

---

## 3. Ten-frame disposition (final)

| # | activation_key | GPT | Anthony | Implementation |
|---:|---|---|---|---|
| 1 | `…::inv_vitamin_d_low_deficiency` | RETIREMENT_CONFIRMATION_ONLY | APPROVED | COMPILED_ACTIVE; legacy retired |
| 2 | `…::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 3 | `…::inv_homocysteine_high_metabolic` | REJECT | APPROVED | REJECTED / inactive |
| 4 | `…::inv_homocysteine_high_renal_clearance_reduction` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 5 | `…::inv_mcv_high_macrocytosis` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE (anchor) |
| 6 | `…::inv_mcv_high_megaloblastic_macrocytosis` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 7 | `…::inv_mcv_high_nonmegaloblastic_macrocytosis` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 8 | `…::inv_free_t3_low_low_t3_syndrome` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 9 | `…::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |
| 10 | `…::inv_tpo_ab_high_euthyroid_autoimmune_risk` | APPROVE_WITH_REVISIONS | APPROVED | COMPILED_ACTIVE |

---

## 4. Authority before / after

| Frame class | Before | After |
|---|---|---|
| vitamin_d_low | Compiled signal-promoted; legacy YAML still registry-reachable | Compiled sole runtime; legacy `LEGACY_RETIRED` |
| hcy approved frames | Shared legacy YAML | Per-key compiled artefacts |
| hcy metabolic | Legacy catch-all risk | REJECTED — skip; no fallback |
| mcv / free_t3 / tpo pilot frames | Legacy YAML | Per-key compiled artefacts |

Selection SSOT: `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` via `why_authority_v1.resolve_frame_why_authority`.

`RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS` remains vitamin-D-only (ARCH-RT-5C signal-level contract). PKG3 frame promotion is register-driven by `activation_key`.

---

## 5. Key files

| Path | Role |
|---|---|
| `backend/core/knowledge/why_authority_v1.py` | Per-key authority resolver |
| `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` | 10-frame register |
| `knowledge_bus/compiled/hypotheses/inv_*.yaml` (8) + manifests | Approved compiled WHY |
| `backend/core/analytics/root_cause_compiler_v1.py` | Register-driven selection; reject no-fallback |
| `backend/scripts/validate_compiled_why_authority_gate.py` | Executable dual-authority / reject gate |
| `backend/tests/unit/test_why_authority_pkg3.py` | Unit coverage |
| Retirement / parity docs | Phase 5–6 evidence |
| Consolidated medical review | Gate C SSOT |

---

## 6. Tests / gates

| Command | Expected |
|---|---|
| `python backend/scripts/validate_compiled_why_authority_gate.py` | PASS |
| `python -m pytest backend/tests/unit/test_why_authority_pkg3.py …` | PASS |
| `python backend/scripts/run_architecture_validation_gate.py` | PASS (includes new gate) |

---

## 7. Acceptance criteria

| Criterion | Status |
|---|---|
| Exact 5/10 cohort preserved | PASS |
| Gate C complete for all frames | PASS |
| Only ratified frames promoted | PASS |
| Rejected metabolic inactive + no fallback | PASS |
| Dual authority prevented for pilot keys | PASS |
| Vitamin D legacy retirement confirmed | PASS |
| Output parity classified; no unexplained drift | PASS |
| No merge without human authority | Observed |
| No beta-readiness / estate-wide claim | PASS |

---

## 8. STOP-condition assessment

| # | Condition | Result |
|---|---|---|
| Medical rejection of metabolic | Honoured (REJECTED) | Not a programme STOP |
| Dual authority / bare signal collapse | Prevented by register + gate | Not triggered |
| Unexplained clinical drift | None | Not triggered |
| Material conflict vs ratified pack | None | Not triggered |

---

## 9. Final Package 3 recommendation

**GO**

Package 3 pilot obligations for the ratified 10-frame cohort are closed on this branch.  
Do **not** merge without explicit human authority.  
Do **not** expand beyond the pilot cohort without a new work package.

---

## 10. Unresolved limitations (non-blocking)

- Supporting-pattern gates from the medical pack are encoded as caveats / wording in compiled artefacts; they are not additional fail-closed marker predicates in the compiler.  
- Shared legacy YAML files remain on disk for history and for out-of-pilot signals (e.g. `signal_homocysteine_elevation_context`).  
- Per-frame decision checkbox sections above the annex in the review pack remain historical placeholders; the annex + Anthony table are authoritative.
