# ARCH-CONV-A — Revised Scope and Split Decision

**Work ID:** `ARCH-CONV-A`  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Date (UTC):** 2026-07-28  
**Decision class:** delivery-boundary revision (programme governance)

## Decision

```text
original design:
7 internal waves on one branch

revised delivery boundary:
Waves 0–2 only on this branch

reason:
the original branch scope was operationally over-broad and created excessive audit, rollback, review and cross-domain risk

programme-level Package A status:
PARTIALLY COMPLETED / SPLIT FOR SAFE DELIVERY

current branch status:
COMPLETE FOR REVISED SCOPE

deferred work:
not cancelled
not completed
must continue as separate governed work packages
```

## Completed on this branch (revised scope)

| Wave | Domain | Status on this branch |
|---|---|---|
| 0 | Homocysteine elevation-context disposition | COMPLETE (`FOLD_SUPPRESS`) |
| 1 | Thyroid WHY authority migration | COMPLETE (Gate 1/2 + STOP C + clean re-audit) |
| 2 | Lipid / cardiometabolic WHY authority migration | COMPLETE (Gate 1/2 + STOP C + clean independent audit) |

## Deferred into separate governed branches / work packages

| Wave | Domain | Preservation / next vehicle |
|---|---|---|
| 3 | Renal | `feature/arch-conv-a-renal-migration` @ `31c37a2` (STOP B pack preserved; no compile) |
| 4 | Hepatic / biliary | Separate future governed work package |
| 5 | Iron / haematology | Separate future governed work package |
| 6 | Metabolic / systemic residual | Separate future governed work package |

## Split mechanics (already executed)

1. Wave 3 STOP B preparation was committed as `31c37a2` on the Package A branch.
2. Preservation branch `feature/arch-conv-a-renal-migration` was created at `31c37a2`.
3. Package A branch reverted Wave 3 preparation via `366512f` without rewriting history.
4. Wave 0–2 implementation and Wave 2 independent audit record remain on this branch.
5. No further renal work was performed on the preservation branch during the split.

## Explicit non-claims

- This decision does **not** declare full seven-wave Package A completion.
- This decision does **not** cancel Waves 3–6.
- This decision does **not** authorise Package B dual-authority retirement or Package C replay/versioning work.
- This decision does **not** authorise estate-wide legacy disconnection or physical deletion of legacy WHY assets.
- This decision does **not** merge either branch.

## Authority references retained on this branch

| Artefact | Role |
|---|---|
| `docs/architecture/ARCH-CONV-A_STOP_A_identity_and_source_closure.md` | STOP A |
| `docs/architecture/ARCH-CONV-A_wave0_suppression_closure.md` | Wave 0 |
| `docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md` | Wave 1 Gate 1/2 |
| `docs/architecture/ARCH-CONV-A_STOP_C_wave1_runtime_proof.md` | Wave 1 STOP C (+ re-audit PASS) |
| `docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md` | Wave 2 Gate 1/2 |
| `docs/architecture/ARCH-CONV-A_STOP_C_wave2_runtime_proof.md` | Wave 2 STOP C (+ independent audit PASS) |

## Next programme actions (outside this finish)

- Independent revised-scope closure audit of this branch.
- Continue Wave 3+ as separate governed packages starting from preserved renal preparation where applicable.
- Human merge authority remains separate from Automation Bus `finish`.
