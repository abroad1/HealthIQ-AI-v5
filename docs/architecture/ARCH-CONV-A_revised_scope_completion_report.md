# ARCH-CONV-A — Revised-Scope Completion Report

**Work ID:** `ARCH-CONV-A`  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Date (UTC):** 2026-07-28  
**Companion decision:** `docs/architecture/ARCH-CONV-A_revised_scope_and_split_decision.md`

## Programme status

```text
programme-level Package A status:
PARTIALLY COMPLETED / SPLIT FOR SAFE DELIVERY

current branch status:
COMPLETE FOR REVISED SCOPE
```

This report certifies completion of the **revised** delivery boundary only (Waves 0–2).
It does **not** claim full original seven-wave Package A completion.

## Revised completed scope

```text
Wave 0 — Homocysteine elevation-context disposition
Wave 1 — Thyroid WHY authority migration
Wave 2 — Lipid/cardiometabolic WHY authority migration
```

## Deferred scope (not cancelled)

```text
Wave 3 — Renal
Wave 4 — Hepatic/biliary
Wave 5 — Iron/haematology
Wave 6 — Metabolic/systemic residual
```

Wave 3 STOP B preparation is preserved on:

```text
feature/arch-conv-a-renal-migration @ 31c37a2
```

and was removed from this branch by revert:

```text
366512f
```

## Delivered outcomes

| Outcome | Evidence |
|---|---|
| STOP A identity/source closure | `ARCH-CONV-A_STOP_A_identity_and_source_closure.md` |
| D-2 homocysteine `FOLD_SUPPRESS` disposition | `ARCH-CONV-A_wave0_suppression_closure.md` |
| D-3 bilirubin `MERGE_TO_ONE` identity decision and bounded registry correction | STOP A / identity artefacts on branch |
| Wave 0 closure | Wave 0 suppression closure artefact |
| Wave 1 thyroid Gate 1 / Gate 2 ratification | `ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md` + decision register |
| Wave 1 compile and runtime integration | compiled thyroid artefacts + authority register + `why_authority_v1` pilot extension |
| Wave 1 STOP C correction and clean independent re-audit | `ARCH-CONV-A_STOP_C_wave1_runtime_proof.md` (`STOP C final status: PASS`) |
| Wave 2 lipid Gate 1 / Gate 2 ratification | `ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md` + decision register |
| Wave 2 compile and runtime integration | compiled lipid artefacts + HDL `morphology_context` + authority rows |
| Wave 2 clean independent STOP C audit | `ARCH-CONV-A_STOP_C_wave2_runtime_proof.md` (`Wave 2 STOP C: PASS`) |
| Named duplicate-authority resolution mechanism | `backend/core/knowledge/duplicate_authority_resolution_v1.py` + unit proofs |
| 0 new regression failures versus main at the audited Wave 2 boundary | Wave 2 STOP C evidence + re-verified at revised-scope closure |

## Explicitly not delivered

```text
Wave 3 renal migration
Wave 4 hepatic/biliary migration
Wave 5 iron/haematology migration
Wave 6 metabolic/systemic migration
full original seven-wave Package A completion
Package B fallback or dual-authority retirement
Package C replay/provenance/versioning work
estate-wide legacy disconnection
```

## Repository verification (revised-scope closure)

| Check | Result |
|---|---|
| Current branch | `feature/arch-conv-a-estate-why-authority-migration` |
| Wave 3 pack absent | YES |
| Wave 3 decision register absent | YES |
| Renal compile / runtime changes from Wave 3 | NO |
| Waves 0–2 intact | YES |
| Wave 1 / Wave 2 independent audits referenced | YES |
| Renal preservation branch untouched by this closure | YES (`feature/arch-conv-a-renal-migration` @ `31c37a2`) |
| Legacy WHY physical deletion without authority | NO |
| Package B / C absorbed | NO |
| Merge performed | NO |

## Key commits (illustrative trail)

| Commit | Meaning |
|---|---|
| `82f4031` / earlier | Wave 0 / STOP B prep lineage on branch |
| `0f401c3` | Wave 1 STOP C compile + runtime |
| `95dfb6c` | Wave 1 STOP C CORRECT |
| `e449c32` | Selector test path portability fix |
| `f044f2b` | Wave 2 STOP C compile + runtime |
| `31c37a2` | Wave 3 prep (preserved on renal branch only) |
| `366512f` | Revert Wave 3 prep from Package A branch |

## Closure statement

Package A on this branch is **complete for revised scope (Waves 0–2)** and **partial at programme level**.
Deferred waves remain open as separate governed work packages.
