---
work_id: ARCH-RT-IDENTITY-PROV-1-C1
branch: feature/arch-rt-identity-prov-1-c1-evidence-completion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# ARCH-RT-IDENTITY-PROV-1-C1 — Evidence Completion Correction

## Outcome

Regularise and independently verify the completed evidence correction for `ARCH-RT-IDENTITY-PROV-1` using a valid new kernel lifecycle.

Base this branch on commit:

```text
2c8819c
```

Standard Automation Bus governance applies.

## Required inputs

```text
docs/audit-papers/ARCH-RT-IDENTITY-PROV-1_implementation_and_verification_report.md
automation_bus/latest_audit_summary.md
backend/tests/unit/test_arch_rt_identity_prov_1.py
```

Also inspect the clinician fixtures changed at `2c8819c` and the original hardened prompt for `ARCH-RT-IDENTITY-PROV-1`.

## Scope

1. Start a new kernel lifecycle under `ARCH-RT-IDENTITY-PROV-1-C1`.
2. Verify the expanded identity/provenance test matrix.
3. Verify the completed implementation report.
4. Verify regenerated clinician fixtures for additive `root_causes` and nullable legacy `root_cause`.
5. Re-run the required gates and targeted regressions.
6. Classify the disclosed unrelated failures.
7. Update the implementation report only if verification evidence is missing or incorrect.
8. Complete kernel finish under this correction work ID.
9. Submit for independent Claude audit.

## Constraints

- Do not modify the original `ARCH-RT-IDENTITY-PROV-1` kernel state.
- Do not redesign production code.
- Modify production code only if a new test exposes a genuine defect; STOP first and report evidence.
- Do not start Package 3.
- Do not activate PSI, MR-BATCH-001B or Gemini.
- Do not weaken tests or suppress failures.
- Keep all changes limited to correction evidence, tests, fixtures and bus-managed files.

## Required verification

Run the relevant repository commands for:

- identity/provenance test suite;
- architecture validation gate;
- launch-estate gate;
- signal evaluator and activation identity;
- interaction, root-cause, report and clinician-report contracts;
- output-authority provenance;
- replay/auditability;
- golden-panel;
- bilirubin and Wave 1 liver regressions;
- MR-BATCH isolation;
- PSI isolation;
- narrative NO-LLM;
- frontend TypeScript check.

Record exact commands and exit codes.

For each disclosed failure, classify it as one of:

```text
PRE_EXISTING_OUT_OF_SCOPE
INTRODUCED_BY_CORRECTION
BLOCKING
NON_BLOCKING
```

Do not relabel a failure without evidence.

## Acceptance criteria

- [ ] New kernel `start` succeeds under `ARCH-RT-IDENTITY-PROV-1-C1`.
- [ ] Expanded test matrix is present and passes where in scope.
- [ ] Implementation report contains the required evidence and command log.
- [ ] Clinician fixtures match the additive contract.
- [ ] Required gates pass.
- [ ] Disclosed unrelated failures are independently classified.
- [ ] No production redesign occurred.
- [ ] Original kernel state remains unchanged.
- [ ] Kernel `finish` succeeds under the correction work ID.
- [ ] Branch is ready for independent audit.

## STOP conditions

STOP if:

1. branch is not based on `2c8819c`;
2. correction requires editing the original work ID status;
3. a new test exposes a real production defect;
4. any disclosed failure is introduced by this correction;
5. scope expands beyond tests, evidence, fixtures or bus-managed files;
6. required gates fail for an unexplained reason.

## Output

Create:

```text
docs/audit-papers/ARCH-RT-IDENTITY-PROV-1-C1_correction_verification_report.md
```

Include:

- baseline SHA;
- files changed;
- verification results;
- exact commands and exit codes;
- failure classifications;
- acceptance-criteria table;
- STOP-condition assessment;
- confirmation that production code was not redesigned;
- confirmation that the original kernel record was untouched.

Do not merge without explicit human authority.
