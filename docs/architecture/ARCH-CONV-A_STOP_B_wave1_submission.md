# ARCH-CONV-A — STOP B Submission (Wave 1)

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Gate:** STOP B — first medical-review pack  
**Automation Bus:** remain IN_PROGRESS; **do not finish**

---

## Submission

| Field | Value |
|---|---|
| first medical-review pack complete | **YES** (assembly complete; medical decisions PENDING) |
| wave | 1 — Thyroid axis (spec-ready subset) |
| frames submitted | 5 |
| pack path | `docs/architecture/ARCH-CONV-A_wave1_thyroid_medical_review_pack.md` |
| decision register | embedded in pack (all PENDING) |

### Frames submitted

1. `signal_tsh_high::inv_tsh_high_hypothyroidism`  
2. `signal_tsh_low::inv_tsh_low_hyperthyroidism`  
3. `signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis`  
4. `signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context`  
5. `signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency`  

### Medical decisions requested

For each frame: Gate 1 GPT structured review + Gate 2 Anthony ratification using  
`APPROVE | APPROVE_WITH_NARROWING | REJECT | DEFER_EVIDENCE_INSUFFICIENT | CONTEXT_ONLY`.

### Related artefacts (not this STOP B decision set)

| Artefact | Role |
|---|---|
| `ARCH-CONV-A_wave0_suppression_closure.md` | Wave 0 closed as FOLD_SUPPRESS |
| `ARCH-CONV-A_bilirubin_provisional_frames_research_pack.md` | Research assembly only; frames unapproved |
| `ARCH-CONV-A_phase2_spec_ready_frame_index.md` | Index of all 17 spec-ready frames |

---

## Unresolved blockers

| Blocker | Impact |
|---|---|
| Wave 1 medical decisions PENDING | No Phase 3 compile until STOP B ratification |
| `signal_thyroid_tsh_context`, `signal_tgab_high` research gaps | Remain outside Wave 1 STOP B |
| Bilirubin Pass3 lacks `inv_*.yaml` | Wave 4 Gate 1 blocked until research promotion |
| Package B hand-offs (hcy shared file / selectors) | Not in this STOP B |

---

## Explicit non-claims

Cursor has **not** made medical decisions, compiled WHY, activated runtime authority, disconnected legacy sources, or called Automation Bus `finish`.
