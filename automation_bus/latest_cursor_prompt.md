---
work_id: ARCH-CONV-D
branch: feature/arch-conv-d-alt-identity-closure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: DOCS_GOVERNANCE
---

# ARCH-CONV-D — ALT Identity and Authority Closure

## Objective

Resolve the repository identity relationship between:

- `signal_alt_high`
- `signal_hepatic_alt_context`

Produce one explicit, auditable architecture decision that gives the later ALT
WHY-authority migration package an unambiguous target.

This package is identity and governance closure only.

It must not:

- adjudicate ALT medical WHY roles;
- compile or activate ALT WHY;
- change emitted reasoning or runtime behaviour;
- disconnect legacy ALT WHY;
- remediate hardcoded ALT-context thresholds;
- create AST authority;
- alter `cholestatic_source_axis`;
- change bilirubin/hyperbilirubinemia authority;
- modify frontend logic.

## Governing rules

Apply the repository-governed versions of:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

Preserve:

- identity from embedded governed fields, never filenames or package names;
- canonical research authority separately from package-authored signals;
- signal identity separately from WHY authority;
- explicit alias, predecessor and retirement relationships;
- no medical meaning inferred from repository age or naming;
- no runtime reads of raw investigation specs;
- no frontend medical inference;
- fail-closed handling of unresolved authority;
- no implicit migration of legacy WHY ownership.

If any required change would affect runtime behaviour, emitted reasoning,
thresholds, signal activation, loaders, compiler logic or medical authority,
STOP and rescope as HIGH/MIXED.

## Authoritative programme baseline

Use current `main` after the completed and merged ARCH-CONV-C package
(`e2d7ce38adc095387e632c6e50ebad68110cbe10`).

ARCH-CONV-D must not reopen or modify any ARCH-CONV-C decision.

## Branch

`feature/arch-conv-d-alt-identity-closure`

## Phase boundary for current execution

Phase 0 only: identity reconstruction and STOP A submission artefacts.

Do not proceed to Phase 1 until explicit STOP A approval records one of:

- `MERGE_TO_SIGNAL_ALT_HIGH`
- `RETAIN_AS_DISTINCT_CONTEXT_SIGNAL`
- `RETIRE_WITHOUT_TRANSFER`
- `DEFER_IDENTITY_UNRESOLVED`

## Required Phase 0 artefacts

- `docs/architecture/ARCH-CONV-D_STOP_A_alt_identity_closure.md`
- `docs/architecture/ARCH-CONV-D_alt_identity_map.md`
- `docs/architecture/ARCH-CONV-D_identity_decision_register.yaml`

Register initial state must be:

`STOP_A_SUBMISSION_READY_FOR_HEAD_OF_ARCHITECTURE`

Every final decision field must remain PENDING.

## Explicit exclusions

- `signal_ast_high`
- `cholestatic_source_axis` / ALP / GGT
- bilirubin / hyperbilirubinemia
- frontend
- ALT WHY compile / activate / disconnect
- hardcoded threshold remediation

## Stop condition

STOP after Phase 0 for independent Head of Architecture STOP A approval.
