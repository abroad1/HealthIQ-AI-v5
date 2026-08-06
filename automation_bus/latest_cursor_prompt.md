---
work_id: THYROID-FT3-TSH-FIRING-FIX-1
branch: fix/thyroid-ft3-tsh-firing
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# THYROID-FT3-TSH-FIRING-FIX-1

## Objective

Correct the confirmed runtime defect in which the governed `signal_free_t3_high` activation frame does not fire when free T3 is high and the required suppressed-TSH companion condition is satisfied.

The correction must restore the existing governed behaviour only. It must not create or revise thyroid medical policy.

## Confirmed baseline defect

The current baseline has exhibited the following failing test:

```text
backend/tests/unit/test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate
```

Recorded representative case:

```text
FT3 = 7.0
TSH = 0.2
```

Expected:

```text
signal_free_t3_high fires
```

Observed:

```text
no signal returned
```

Treat this as the observed defect, not as a pre-judged root cause.

## Architectural and authority constraints

The implementation must preserve the accepted research-to-runtime architecture:

```text
canonical research authority
→ governed compiled/runtime artefacts
→ thin runtime loaders/evaluators
→ structured outputs
→ frontend render-only
```

Do not introduce:

- a second thyroid authority source;
- raw investigation-spec reads at runtime;
- hand-authored fallback medical logic;
- a signal-specific bypass around the governed activation path;
- frontend medical inference.

The runtime identity model remains:

```text
signal_id = signal-family identity
activation_key = activation-frame identity
```

Do not collapse, rename, duplicate, or replace the existing activation frame.

## Stage D authority verification requirements

During hardening, Claude must identify and read the repository files that are authoritative for:

1. the `signal_free_t3_high` activation-frame definition;
2. its primary free-T3 condition;
3. its suppressed-TSH companion condition;
4. biomarker identity and alias resolution for free T3 and TSH;
5. reference-range or threshold comparison semantics;
6. the runtime loader/evaluator path consuming that authority;
7. the canonical test module and adjacent regression coverage.

Claude must verify that:

- the baseline defect still exists;
- the test, authority source, loader and evaluator refer to the same governed activation frame;
- no duplicate or parallel thyroid activation authority exists;
- the proposed sprint remains a bounded behavioural correction;
- the exact in-scope implementation and test files can be named before hardening completes.

If the defect no longer exists, hardening must BLOCK the sprint as a no-op.

## In scope

- Reproduce the confirmed failing case on the current branch.
- Trace the failure through the existing governed thyroid activation path.
- Identify the exact root cause.
- Apply the smallest policy-preserving correction at the true defect source.
- Add or strengthen regression coverage for the affected activation frame.
- Prove that the correction does not change unrelated thyroid activation behaviour.
- Preserve signal-estate identity and count.
- Produce implementation and validation evidence.
- Update the existing Build Deliverable Register at closure.

## Required behavioural coverage

The hardened prompt must require tests covering at least:

1. free T3 high + TSH suppressed  
   `signal_free_t3_high` fires.

2. free T3 high + TSH not suppressed  
   `signal_free_t3_high` does not fire.

3. free T3 not high + TSH suppressed  
   `signal_free_t3_high` does not fire.

4. free T3 high + TSH absent  
   behaviour matches the current governed missing-companion rule.

5. boundary behaviour at the governed free-T3 high threshold.

6. boundary behaviour at the governed TSH suppression threshold.

7. canonical biomarker identifiers and any currently supported aliases implicated in the defect.

8. no duplicate `signal_free_t3_high` result.

9. no unintended firing or suppression of adjacent thyroid signals.

10. unchanged active signal-estate baseline, unless Stage D finds a later repository-ratified baseline.

The test values must be drawn from existing governed authority and current test conventions. Do not encode `7.0` or `0.2` as new policy constants merely because they appear in the observed failing fixture.

## Implementation rules

- Correct the defect at the existing authority, loader, evaluator, normalisation, or filtering point demonstrated by evidence.
- Preserve deterministic behaviour.
- Preserve the governed suppressed-TSH companion requirement.
- Preserve existing signal identity, activation identity, severity, urgency and prioritisation.
- Preserve existing compiled-WHY and research artefacts.
- Keep the change bounded to the thyroid firing defect and required tests.
- Do not edit unrelated files.

## Out of scope

- Changing thyroid thresholds or reference-range policy.
- Changing the clinical meaning of high free T3.
- Weakening or removing the suppressed-TSH companion condition.
- Adding new thyroid signals or activation frames.
- Resuming ARCH-CONV-A medical-review waves.
- Editing compiled-WHY medical content.
- Changing root-cause or narrative content.
- Changing system/subsystem visibility.
- Changing consumer copy or frontend presentation.
- Changing cross-domain clinical prioritisation.
- Broad refactoring of the signal evaluator.
- Knowledge Bus package promotion or canonical research edits.

## STOP conditions

STOP and report the exact blocker if any of the following applies:

- the baseline defect cannot be reproduced;
- the sprint would be a no-op;
- the governing activation authority is ambiguous or duplicated;
- the test and governing medical authority legitimately disagree;
- fixing the defect requires a threshold, companion-rule, severity, urgency, or other medical-policy decision;
- the active signal baseline cannot be reconciled;
- the correct fix requires broad evaluator redesign outside this bounded package;
- the defect is caused by unresolved or unratified thyroid research/compiled-WHY authority;
- unrelated working-tree changes prevent clean isolation;
- required regression coverage cannot be made deterministic.

Where medical authority is insufficient, stop with:

```text
STOP — MEDICAL AUTHORITY REQUIRED
```

Do not infer or invent the missing rule.

## Required validation

The hardened prompt must name the exact commands after repository inspection.

Validation must include, as applicable:

- the confirmed failing thyroid test;
- the complete thyroid activation-pack test module;
- directly affected evaluator/loader tests;
- thyroid regression tests;
- signal registry/package validation relevant to the changed path;
- signal-estate baseline validation;
- relevant cross-domain prioritisation regressions;
- deterministic repeat execution for the corrected case;
- repository-standard broader backend validation proportionate to the touched files.

Do not claim full-suite success unless the full suite is run.

## Required evidence

Cursor must record:

- starting branch and HEAD;
- reproduced baseline failure;
- authoritative source and runtime path inspected;
- root cause;
- exact files changed;
- why the correction preserves rather than changes policy;
- tests added or changed;
- every validation command and result;
- signal-estate baseline before and after;
- any unrelated pre-existing failures;
- final working-tree and stash state.

## Automation Bus execution

After Stage D hardening succeeds:

```powershell
python backend/scripts/run_work_package.py start
```

Cursor must verify the active execution token before modifying repository files.

After implementation, commits and the mandatory closure audit are complete, Cursor must run:

```powershell
python backend/scripts/run_work_package.py finish
```

Cursor must follow the full post-implementation closure protocol in Automation Bus SOP v1.3.1, including branch, status, diff, log and stash evidence before finish.

Cursor must not self-certify correctness and must not merge.

## Completion condition

After successful kernel finish, stop for independent Claude audit.

Required terminal handoff:

```text
READY_FOR_CLAUDE_AUDIT
```

Merge requires:

- successful kernel finish;
- gate PASS;
- Claude audit summary;
- GPT architectural review;
- explicit Anthony merge authority.
