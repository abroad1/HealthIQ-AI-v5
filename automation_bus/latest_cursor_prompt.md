---
work_id: V5-CANONICAL-ACTIVATION-GATE-1
branch: refactor/v5-canonical-activation-gate-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# V5 Canonical Runtime Activation Gate

## Objective

Implement the next bounded step in the ratified V5-retention architecture:

> Runtime activation must have one canonical write-path authority. Other existing mechanisms may constrain eligibility, provenance, or safety, but must not independently grant activation.

Use the transition design produced by `V5-RUNTIME-AUTHORITY-INTEGRITY-1` as the starting architecture. Do not broaden this sprint into residual medical-content work or a full SignalRegistry rewrite.

## Stage 1A — Authority Preflight

Before implementation, verify on the current merged `main`:

1. `docs/architecture/V5_RUNTIME_ACTIVATION_CANONICAL_GATE_TRANSITION.md` exists and still identifies the current activation mechanisms and the intended canonical future gate.
2. `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` is the intended canonical runtime activation authority.
3. `backend/core/analytics/signal_evaluator.py` is the runtime loader/consumer path whose activation decisions must converge on that authority.
4. `backend/core/knowledge/runtime_medical_authority_integrity_v1.py` remains the prohibition-integrity guard introduced by `V5-RUNTIME-AUTHORITY-INTEGRITY-1`.
5. The other activation-related mechanisms identified in the transition document are classified correctly as either:
   - supporting eligibility/provenance/safety constraints; or
   - duplicate/parallel activation-granting paths requiring demotion.
6. No proposed change creates a new activation SSOT.

If current repository reality differs materially from the transition document, STOP for GPT architectural review rather than implementing the stale design.

## Stage 1B — Reality Check

Confirm that the current baseline still contains more than one mechanism capable of independently causing a signal/package/frame to become runtime-active.

If the canonical-gate transition has already been completed by another merged change, STOP with `NO_OP_OR_REBASE_REQUIRED`.

## Stage 1C — Intelligence Preflight

Affected Intelligence Core surface is limited to runtime activation eligibility/loading and the validators/tests governing that behaviour.

Expected behavioural result:

- no currently authorised signal becomes inactive solely because supporting eligibility/provenance checks are retained;
- no currently unauthorised signal becomes active;
- activation permission is granted only through the canonical activation authority;
- supporting mechanisms can veto/restrict activation where already governed to do so, but cannot independently activate;
- identical governed inputs produce the identical complete activation-key set.

Canonical regression module:

`backend/tests/architecture/test_canonical_runtime_activation_gate.py`

Also preserve and run:

`backend/tests/architecture/test_runtime_medical_authority_integrity.py`

## Required implementation

### 1. Re-derive current gate topology

Using live code, produce a short pre-change evidence map showing each mechanism identified in the transition document, where it is consumed, and whether it currently:

- grants activation;
- restricts eligibility;
- verifies provenance;
- protects launch-critical behaviour;
- or performs another bounded function.

Write:

`docs/architecture/V5_CANONICAL_ACTIVATION_GATE_prechange_map.md`

Do not infer from names alone; cite code/config locations.

### 2. Enforce one canonical activation grant

Refactor the narrowest safe runtime path so that:

`package_runtime_activation_register_v1.yaml`

is the single mechanism that grants runtime activation.

Other existing mechanisms must be treated only as preconditions, vetoes, provenance checks, or safety constraints according to their already-governed semantics.

Do not remove a supporting mechanism merely because it participates in loading.

Do not change medical policy or activation content except where required to eliminate duplicate grant authority.

### 3. Prevent parallel write paths

Identify every repository path that can create/update runtime activation state.

Ensure new activation entries cannot be introduced through an alternate write/bootstrap path without passing:

- canonical activation-authority rules;
- `runtime_medical_authority_integrity_v1` prohibition validation;
- existing applicable provenance/eligibility constraints.

If safe enforcement requires modifying Automation Bus control-plane scripts, STOP under SOP §13.

### 4. Preserve fail-closed medical prohibition enforcement

The invariant from `V5-RUNTIME-AUTHORITY-INTEGRITY-1` must remain effective.

Explicit activation prohibitions must continue to block activation.

Do not interpret:

- `LEGACY_RETIRED`;
- WHY retirement;
- `SUPERSEDED_BY_*`;
- non-owning WHY status

as signal deactivation unless an existing governed activation authority explicitly says so.

### 5. Add exact-set determinism proof

Add regression coverage proving:

> identical repository/governed inputs → identical complete runtime activation-key set

Do not test only the numeric count.

At minimum:

- instantiate the real registry repeatedly under identical inputs;
- compare sorted activation-key sets exactly;
- fail on missing, added, or reordered/unstable membership;
- run enough repeated fresh constructions to catch hidden state/order dependence without introducing probabilistic tests.

### 6. Canonical-gate regression coverage

Create:

`backend/tests/architecture/test_canonical_runtime_activation_gate.py`

Cover at minimum:

1. canonical activation entry + all required constraints satisfied → loads;
2. no canonical activation entry → cannot load solely because another mechanism permits it;
3. explicit medical prohibition → cannot load even if canonical activation entry exists;
4. valid WHY-retired-but-still-firing signal remains loadable when canonically activated;
5. provenance/eligibility veto continues to veto where already governed;
6. conflicting authority fails closed;
7. repeated identical loads return the exact same activation-key set;
8. no duplicate activation grant path exists in the tested runtime flow.

### 7. Update transition evidence

After implementation, update or supersede the transition document with the exact resulting architecture and remaining carry-forward, if any.

The result must state clearly:

- what now grants activation;
- what only constrains/vetoes;
- what legacy grant path was removed/demoted;
- whether any further activation-gate consolidation sprint is still genuinely required.

## Explicit non-scope

Do not:

- resume ARCH-CONV-A residual medical work;
- add or research thyroid, iron, hepatic, metabolic or other clinical content;
- change signal thresholds, comparators, clinical meaning, severity or prioritisation;
- create/remove signal identities except where an already-governed activation entry is being structurally migrated without semantic change;
- rewrite root-cause/WHY content;
- change frontend or consumer narrative;
- redesign the full Knowledge Bus;
- rewrite `SignalRegistry` wholesale;
- modify Automation Bus control-plane scripts;
- change package activation decisions merely to make tests pass;
- treat this as general cleanup.

## STOP conditions

STOP and escalate before further implementation if:

1. the transition document is stale relative to current code in a way that changes the proposed canonical gate;
2. more than one mechanism has legitimate, irreducible authority to grant activation and cannot be demoted without new architecture policy;
3. making the activation register canonical would change medical meaning or deactivate currently-authorised signals without explicit authority;
4. safe implementation requires inventing new activation policy;
5. safe implementation requires changing:
   - `backend/scripts/run_work_package.py`
   - `backend/scripts/golden_gate_local.py`
   - `backend/scripts/update_cursor_status.py`
6. exact-set determinism fails for reasons not explained by governed repository/input differences;
7. the runtime still contains an independent activation-granting bypass after the intended refactor;
8. regression evidence shows unrelated authorised signals are lost or unauthorised signals become active;
9. the work expands into a full loader rewrite or broad package migration.

STOP 2, 6, or 7 requires explicit GPT + Anthony reassessment of whether the conditional V5-retention premise still holds.

## Success criteria

All must pass:

- current multi-gate reality independently verified;
- one canonical runtime activation grant established;
- other mechanisms correctly retained only as constraints/vetoes where governed;
- no new SSOT created;
- prohibition validator remains effective;
- no medical content/policy changed;
- exact activation-key set deterministic across repeated identical loads;
- canonical regression module passes;
- prior runtime medical-authority integrity tests pass;
- relevant existing architecture/regression suites pass;
- day-one architecture validation passes;
- no control-plane files changed;
- post-implementation closure protocol passes;
- kernel finish PASS.

## Finish evidence

Cursor must provide:

- pre-change topology evidence with file + line citations;
- exact files changed;
- before/after activation-flow description;
- proof that only the canonical authority grants activation;
- proof that supporting gates still perform their existing constraint roles;
- exact-set determinism outputs across repeated loads;
- targeted and relevant regression results;
- day-one architecture validator result;
- `git diff --check`;
- confirmation that no medical research/content/threshold/prioritisation/frontend output changed.

Before `python backend/scripts/run_work_package.py finish`, run the mandatory Automation Bus post-implementation closure protocol.

After finish, Claude must independently audit the implementation and explicitly answer:

1. Is there now exactly one runtime activation-grant authority?
2. Can any supporting mechanism still independently activate?
3. Are explicit medical prohibitions still fail-closed?
4. Were WHY-retired-but-valid firing signals preserved correctly?
5. Is exact activation-key membership deterministic under identical inputs?
6. Does the conditional `RETAIN_V5` architecture decision remain supportable?

HIGH-risk merge requires GPT architectural review and Anthony approval.

## Hardening invocation

Use exactly:

`harden work_id: V5-CANONICAL-ACTIVATION-GATE-1 — verify source content and produce evidence checklist`
