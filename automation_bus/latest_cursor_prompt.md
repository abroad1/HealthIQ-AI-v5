---
work_id: V5-RUNTIME-AUTHORITY-INTEGRITY-1
branch: fix/v5-runtime-authority-integrity-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# V5 Runtime Medical-Authority Integrity

## Objective

Restore confidence that governed medical activation decisions control V5 runtime reachability.

This is a bounded architecture/integrity package. It must:

1. close the confirmed lipid rejection-versus-runtime contradiction;
2. introduce a deterministic fail-closed validation invariant between governed medical activation authority and runtime activation state;
3. perform a bounded estate sweep for other instances of the same failure class;
4. add regression coverage capable of detecting this class of authority violation;
5. document the transition path from the current multi-mechanism activation model toward one canonical runtime activation gate.

Do not resume residual ARCH-CONV-A medical-content migration in this work package.

## Stage 1A — Authority Preflight

The current architectural authorities to preserve are:

- medical / compiled-WHY authority:
  `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- runtime package activation authority:
  `knowledge_bus/governance/package_runtime_activation_register_v1.yaml`
- runtime loader:
  `backend/core/analytics/signal_evaluator.py` (`SignalRegistry._load`)
- compiled-WHY selector / consumer:
  `backend/core/analytics/root_cause_compiler_v1.py`
- existing day-one architecture guardrail:
  `backend/scripts/validate_day_one_architecture.py`
- canonical regression module for this work package:
  `backend/tests/architecture/test_runtime_medical_authority_integrity.py`

Architectural rule:

These sources govern different dimensions and must not be replaced by a new parallel SSOT.

This sprint may add a deterministic validator / enforcement check that reconciles them, but must not create a third medical activation authority.

Important semantic boundary:

`LEGACY_RETIRED`, WHY-skip, non-owning, or equivalent WHY-authority states must **not automatically be interpreted as "signal must not fire."**

Runtime activation may be prohibited only where existing governed authority explicitly establishes that the signal / activation must not be active.

If the current authority artefacts cannot express that distinction without inventing a new medical-policy meaning, STOP and escalate for GPT + Anthony architectural review.

Claude Stage D must re-read the above files and verify their current repository paths and semantics before execution. If any stated path or authority assumption is stale, hardening must correct the prompt before HARDENED status.

## Stage 1B — Reality Check

The current baseline is evidenced to contain a real unresolved defect:

- `signal_total_cholesterol_high`
- `signal_lipid_transport_dysfunction`
- `signal_apoa1_cardio_risk`

were explicitly rejected for creation / activation by the ratified ARCH-CONV-A Wave 2 Gate 1 + Gate 2 decision, but were subsequently found runtime-loaded and present in `package_runtime_activation_register_v1.yaml`.

The V5/V6 strategic reassessment independently identified the root architectural gap as absence of a cross-validation invariant between governed medical authority and runtime activation state.

Therefore this is not a no-op sprint.

Stage D must independently reproduce the contradiction before implementation. If the contradiction no longer exists on the current branch, STOP and return `NO_OP_OR_REBASE_REQUIRED`; do not implement speculative remediation.

## Stage 1C — Intelligence Preflight

### Intelligence Core components potentially affected

- `backend/core/analytics/signal_evaluator.py`
- runtime activation governance consumed by `SignalRegistry._load`
- existing medical/WHY authority consumed by `root_cause_compiler_v1.py`
- architecture validation / regression paths

### Behavioural surface

Intended behaviour change is limited to preventing runtime activation where a pre-existing ratified authority explicitly prohibits that activation.

No new signal may become active.

No threshold, comparator, biomarker identity, prioritisation rule, severity rule, WHY wording, research content, consumer narrative, or medical conclusion may be changed.

### Expected output change

For the three confirmed lipid violations, prohibited signals must no longer be runtime-reachable / emitted.

For all other signals, behaviour must remain unchanged unless the bounded same-class sweep proves an equivalent explicit activation-authority violation.

Any additional removal requires direct cited evidence of an already-ratified `DO_NOT_ACTIVATE`, `REJECTED_FOR_ACTIVATION`, or semantically equivalent decision.

### Canonical regression targets

At minimum prove:

1. the three known lipid signals are not runtime-loaded after correction;
2. existing approved lipid signals remain runtime-loadable and behaviourally unchanged;
3. a deliberately rejected activation fixture fails validation / fails closed;
4. a WHY-retired-but-still-legitimately-firing fixture is not incorrectly blocked;
5. duplicate / conflicting authority data fails closed rather than silently choosing one;
6. identical repository/input state produces identical validator and registry results;
7. existing day-one architecture guardrails remain PASS.

## Scope

### A. Reproduce and trace the known violation

Before mutation, produce a concise evidence report showing:

- the ratified Wave 2 decision prohibiting the three signals;
- their current entries in runtime activation authority;
- the loader path by which they become runtime-reachable;
- the commit / bootstrap mechanism if still verifiable;
- why existing validators failed to detect the contradiction.

Write:

`docs/architecture/V5_RUNTIME_AUTHORITY_INTEGRITY_prechange_evidence.md`

### B. Define the enforceable invariant

Implement the narrowest safe deterministic rule that prevents an explicitly prohibited activation from being accepted into runtime authority.

The invariant must operate at a governed validation/enforcement boundary and must be reusable estate-wide.

It must:

- fail closed on an explicit activation prohibition;
- identify the exact signal / activation key and conflicting authorities;
- return non-zero on violation;
- be deterministic;
- avoid medical inference;
- not treat generic WHY retirement as signal deactivation;
- not create another SSOT.

Preferred implementation shape:

- one read-only validator dedicated to runtime medical-authority integrity;
- wired into the existing architecture validation path so future gate execution catches the violation.

Stage D must verify the exact existing validation entry point before implementation.

Do **not** modify:
- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/scripts/update_cursor_status.py`

unless hardening proves there is no safe existing validation hook. If one of those control-plane files becomes necessary, STOP and re-scope under the SOP control-plane execution-deferral rule.

### C. Correct the known runtime-authority drift

Correct the three confirmed lipid activation violations using existing ratified authority only:

- `signal_total_cholesterol_high`
- `signal_lipid_transport_dysfunction`
- `signal_apoa1_cardio_risk`

Do not author new lipid medical content.

Do not reinterpret the original Wave 2 medical decision.

Do not activate any replacement signal.

If the current repository contains a later valid ratified decision explicitly superseding the Wave 2 prohibition, STOP and escalate the authority conflict rather than choosing one.

### D. Bounded same-class estate sweep

Search only for the same architectural failure class:

> runtime-active / activation-registered signal or activation key that conflicts with an explicit pre-existing governed decision prohibiting its activation.

Do not turn this into a general medical-content audit.

For every candidate found, classify:

- `CONFIRMED_VIOLATION`
- `NO_CONFLICT`
- `AMBIGUOUS_AUTHORITY_STOP`

Additional runtime corrections are permitted only for `CONFIRMED_VIOLATION` with direct file + line evidence.

Write:

`docs/architecture/V5_RUNTIME_AUTHORITY_same_class_sweep.md`

If any `AMBIGUOUS_AUTHORITY_STOP` candidate is found, do not infer medical intent. Record it and STOP before mutating that candidate.

### E. Estate-level regression coverage

Create:

`backend/tests/architecture/test_runtime_medical_authority_integrity.py`

Tests must cover the invariant semantically, not only the three current lipid IDs.

Where practical, use generated/in-memory fixtures so the tests prove the rule class rather than hard-code only current production examples.

Also add a direct estate test that runs the validator against current governed registries.

### F. Canonical activation-gate transition decision

Do not refactor all five current activation mechanisms in this sprint.

Produce a short architecture decision / implementation map describing:

- the five current runtime activation gates identified by the reassessment;
- which one should become the canonical future gate;
- which are supporting constraints rather than independent activation authorities;
- the minimum safe transition sequence;
- explicit retirement / demotion targets;
- whether a later implementation package is genuinely required.

Write:

`docs/architecture/V5_RUNTIME_ACTIVATION_CANONICAL_GATE_TRANSITION.md`

This document must be based on current code inspection, not prior report wording alone.

## Explicit Non-Scope

Do not:

- resume ARCH-CONV-A residual compiled-WHY migration;
- perform thyroid, iron, bilirubin, metabolic or other medical research;
- alter clinical prioritisation;
- alter `clinical_concern_set`;
- change signal thresholds or firing predicates except to enforce an existing explicit activation prohibition;
- create new signal identities;
- merge or split existing medical identities;
- modify Knowledge Bus research;
- regenerate packages;
- redesign root-cause / WHY content;
- change frontend or consumer copy;
- perform general code cleanup;
- rewrite `SignalRegistry`;
- collapse all five activation mechanisms in this sprint;
- reopen the V5/V6 strategic decision unless the STOP criteria below are triggered.

## STOP Conditions

STOP and escalate before further implementation if any of the following occurs:

1. The three known lipid signals are no longer active on the current baseline and no equivalent confirmed violation remains.
2. A later ratified authority is found that legitimately supersedes the Wave 2 `do not activate` decision.
3. `compiled_why_authority_register_v1.yaml` cannot safely distinguish WHY retirement from signal-activation prohibition.
4. Enforcing the invariant would require treating all `LEGACY_RETIRED` / WHY-skip states as runtime-deactivated.
5. More than one materially different uncontrolled activation path is discovered that can bypass governed authority.
6. The same-class sweep finds multiple independent leak mechanisms rather than one missing cross-authority invariant.
7. Safe enforcement requires a redesign of `SignalRegistry` rather than a bounded validation/enforcement change.
8. Safe integration requires changing Automation Bus control-plane scripts listed above.
9. The proposed correction would alter medical policy, thresholds, prioritisation, or accepted clinical meaning.
10. Regression evidence shows unrelated approved signals become non-reachable.
11. The work reveals that the current five-gate activation model cannot be centralised without continuing distributed exception logic.

For STOP 5, 6, 7 or 11, explicitly state that the conditional `RETAIN_V5` decision requires GPT + Anthony reassessment before further repair work.

## Success Criteria

The work package is successful only if all are true:

- Current baseline defect reproduced before mutation.
- The three confirmed lipid violations are corrected unless a superseding authority is proven.
- A deterministic estate-wide invariant exists for explicit activation prohibitions.
- The invariant is wired into an existing governed validation path.
- Same-class estate sweep is complete and evidence-backed.
- No ambiguous authority is silently resolved.
- WHY-retired-but-valid signal activity is not accidentally blocked.
- No new signal becomes active.
- No medical policy is changed.
- Canonical regression module passes.
- Existing relevant architecture / signal-registry / lipid regressions pass.
- Day-one architecture guardrails pass.
- Determinism is demonstrated.
- Canonical activation-gate transition document is produced.
- Repository closure protocol passes.
- Kernel finish returns PASS.

## Evidence Required for Finish

Cursor must include in implementation evidence:

- pre-change reproduction commands and outputs;
- post-change runtime registry evidence;
- validator output on current estate;
- same-class sweep summary with file + line citations;
- targeted pytest results;
- relevant existing regression results;
- day-one architecture validator result;
- `git diff --check`;
- exact files changed;
- confirmation that no medical research, threshold, prioritisation or consumer-output content changed.

## Post-Implementation Closure

Before `python backend/scripts/run_work_package.py finish`, execute the mandatory Automation Bus post-implementation closure protocol from SOP v1.3.1, including branch/status/diff checks.

After successful finish, Claude must independently audit the package and explicitly assess:

- whether the authority invariant is semantically correct;
- whether WHY-retirement was incorrectly conflated with signal deactivation;
- whether the same-class sweep was genuinely bounded and complete;
- whether any new uncontrolled activation path was discovered;
- whether the conditional V5-retention premise remains supportable.

HIGH-risk merge still requires GPT architectural review and Anthony approval.

## Hardening Invocation

Use exactly:

`harden work_id: V5-RUNTIME-AUTHORITY-INTEGRITY-1 — verify source content and produce evidence checklist`
