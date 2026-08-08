---
work_id: V5-CANONICAL-ACTIVATION-GATE-2
branch: refactor/v5-canonical-activation-gate-2
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# V5 Canonical Runtime Activation Gate — Stage 2 Launch-Critical Fold-In

## Objective

Complete the V5 runtime-activation convergence begun by `V5-CANONICAL-ACTIVATION-GATE-1`.

The target architecture is now ratified:

> There must be one positive runtime activation-grant authority estate-wide.

`knowledge_bus/governance/package_runtime_activation_register_v1.yaml` is the positive activation authority.

Launch-critical provenance / lineage eligibility remains mandatory for the `pkg_kb47_*` cohort, but only as a fail-closed prerequisite / veto. It must no longer independently grant runtime activation.

The intended runtime rule after this package is:

> canonical activation grant  
> AND all applicable eligibility / provenance / safety constraints  
> = runtime reachable

This sprint must retire the temporary two-authority exception documented by Stage 1.

## Stage 1A — Authority Preflight

Before implementation, verify on current merged `main`:

1. `docs/architecture/V5_RUNTIME_ACTIVATION_CANONICAL_GATE_TRANSITION.md` exists and records the Stage 1 temporary two-authority state and required Stage 2 launch-critical fold-in.
2. `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` is the canonical positive runtime activation authority for the non-launch-critical estate.
3. `backend/core/knowledge/canonical_runtime_activation_gate_v1.py` is the Stage 1 canonical-gate implementation.
4. `backend/core/knowledge/activation_register_mutation_v1.py` is the governed write path for activation-register mutation and preserves medical-prohibition enforcement.
5. `backend/core/knowledge/runtime_medical_authority_integrity_v1.py` is the explicit medical-prohibition integrity guard.
6. `backend/core/knowledge/package_runtime_eligibility_v1.py` is the currently separate launch-critical provenance/lineage eligibility authority and is explicitly marked as a temporary ratified exception after Stage 1.
7. `backend/core/analytics/signal_evaluator.py` still contains the launch-critical runtime-loading path that can admit `pkg_kb47_*` packages without activation-register membership.
8. No later merged decision has ratified permanent dual positive authorities.

If any authority/path assumption is stale or materially different, STOP for GPT architectural review before implementation.

## Stage 1B — Reality Check

Independently confirm the current baseline still has the temporary Stage 1 state:

- non-launch-critical runtime activation requires canonical activation-register membership;
- launch-critical `pkg_kb47_*` runtime activation can still be granted through the separate provenance/lineage eligibility path without canonical activation-register membership.

If launch-critical fold-in is already complete, STOP with `NO_OP_OR_REBASE_REQUIRED`.

If the launch-critical path is no longer cleanly identifiable as a bounded cohort, STOP and escalate rather than broadening the sprint.

## Stage 1C — Intelligence Preflight

### Affected Intelligence Core components

At minimum inspect:

- `backend/core/analytics/signal_evaluator.py`
- `backend/core/knowledge/canonical_runtime_activation_gate_v1.py`
- `backend/core/knowledge/package_runtime_eligibility_v1.py`
- `backend/core/knowledge/activation_register_mutation_v1.py`
- `backend/core/knowledge/runtime_medical_authority_integrity_v1.py`
- `knowledge_bus/governance/package_runtime_activation_register_v1.yaml`

### Behavioural surface

Only runtime activation/reachability of the launch-critical `pkg_kb47_*` cohort may change structurally.

No medical-policy meaning may change.

### Expected behavioural result

After implementation:

- every runtime-loaded activation frame, including launch-critical frames, requires canonical activation-register membership;
- launch-critical frames additionally require their existing provenance/lineage eligibility;
- launch-critical eligibility cannot independently grant activation;
- explicit medical prohibitions remain fail-closed;
- existing authorised launch-critical runtime behaviour remains unchanged after migration;
- previously blocked/ineligible launch-critical packages remain blocked/ineligible;
- no new signal becomes active;
- exact estate-wide activation-key membership is deterministic under identical governed inputs.

### Canonical regression target

Create:

`backend/tests/architecture/test_canonical_runtime_activation_gate_stage2.py`

Also preserve and run:

- `backend/tests/architecture/test_canonical_runtime_activation_gate.py`
- `backend/tests/architecture/test_runtime_medical_authority_integrity.py`

## Required implementation

### A. Re-derive the launch-critical cohort before mutation

Do not assume package count, frame count, or exact package IDs from prior conversational material.

Using current repo state, enumerate the launch-critical `pkg_kb47_*` cohort that is currently runtime-reachable through `package_runtime_eligibility_v1.py`.

For each currently eligible launch-critical package/frame, capture:

- package ID;
- signal ID;
- activation key / frame identity where applicable;
- provenance/lineage eligibility status;
- current runtime reachability;
- whether canonical activation-register membership currently exists.

Write:

`docs/architecture/V5_CANONICAL_ACTIVATION_GATE_STAGE2_prechange_inventory.md`

The inventory must distinguish:

- `CURRENTLY_ELIGIBLE_AND_ACTIVE`
- `CURRENTLY_BLOCKED_OR_INELIGIBLE`
- `AMBIGUOUS_STOP`

Any `AMBIGUOUS_STOP` item stops the migration for that item and requires escalation.

### B. Migrate authorised launch-critical activations into the canonical register

For each launch-critical activation currently authorised and runtime-reachable under the ratified ARCH-CONV-PKG2 provenance/lineage model:

- add the corresponding canonical activation entry through the governed activation-register mutation path;
- preserve exact signal/frame identity;
- preserve existing medical meaning;
- preserve existing provenance/lineage requirements;
- preserve existing activation behaviour.

Do not create activation entries for packages/frames currently blocked or ineligible.

Do not infer new medical authorisation from package existence alone.

If current launch-critical eligibility can identify a package as technically eligible but does not constitute sufficient existing authority to create a canonical activation entry, STOP and escalate rather than inventing promotion authority.

### C. Remove independent launch-critical positive grant behaviour

Refactor the launch-critical loading path so provenance/lineage eligibility can only:

- permit consideration;
- constrain;
- veto;
- fail closed.

It must not independently grant runtime activation.

A launch-critical frame lacking canonical activation-register membership must not load, even if provenance/lineage eligibility passes.

Do not remove provenance/lineage validation itself.

### D. Preserve launch-critical safety semantics

The Stage 2 fold-in must not weaken ARCH-CONV-PKG2 safety guarantees.

At minimum preserve:

- provenance/lineage eligibility checks;
- blocked launch-critical packages remaining unreachable;
- explicit medical-prohibition enforcement;
- duplicate activation-key fail-closed behaviour;
- package/frame identity integrity;
- deterministic loading.

If one positive authority cannot be achieved without weakening any of these safeguards, STOP.

### E. Close the write-path exception

`activation_register_mutation_v1.py` currently refuses launch-critical mutations as a Stage 1 safety boundary.

Update the governed write path so launch-critical canonical activation entries can now be written only when all required launch-critical eligibility/provenance checks pass.

The mutation path must fail closed if:

- explicit medical prohibition exists;
- launch-critical provenance/lineage eligibility fails;
- package/frame identity is ambiguous;
- duplicate/conflicting activation authority exists;
- required source evidence is missing.

Do not introduce a second launch-critical mutation helper or parallel activation file.

### F. Estate-wide exact-set determinism

Extend determinism coverage from the Stage 1 non-launch-critical cohort to the complete runtime estate.

Required proof:

> identical repository/governed inputs → identical complete set of runtime activation keys across all cohorts.

The test must compare exact sets, not numeric counts.

Use repeated fresh `SignalRegistry()` constructions under identical inputs.

Failure output must identify missing/added keys.

### G. Estate-wide canonical-authority proof

Add tests proving:

1. every non-launch-critical loaded activation key is in the canonical activation register;
2. every launch-critical loaded activation key is also in the canonical activation register;
3. launch-critical canonical membership alone is insufficient when provenance/lineage eligibility fails;
4. launch-critical eligibility alone is insufficient when canonical activation membership is absent;
5. explicit medical prohibition overrides canonical membership;
6. WHY-retired-but-still-legitimately-firing signals remain unaffected where canonically activated;
7. blocked launch-critical packages remain blocked;
8. currently authorised launch-critical signals continue to load after migration;
9. exact full-estate activation-key set is deterministic across repeated identical loads;
10. no runtime branch remains that independently grants activation outside the canonical register.

### H. Retire the temporary two-authority exception

Update:

`docs/architecture/V5_RUNTIME_ACTIVATION_CANONICAL_GATE_TRANSITION.md`

or supersede it with a final architecture note if clearer.

The final document must state unambiguously:

- one positive activation authority now exists estate-wide;
- launch-critical provenance/lineage is a prerequisite/veto, not an activation authority;
- the temporary Stage 1 exception is retired;
- whether any further activation-gate convergence work remains.

If any second positive activation authority remains at finish, this sprint must not claim success.

## Explicit Non-Scope

Do not:

- resume ARCH-CONV-A residual clinical-intelligence work;
- perform thyroid, iron, hepatic, renal, lipid, metabolic or other medical research;
- change signal thresholds or comparator logic;
- change medical meaning;
- change clinical prioritisation or concern-set rules;
- rename signal identities;
- merge/split clinical frames;
- rewrite WHY/root-cause content;
- redesign the Knowledge Bus;
- alter frontend/consumer narrative;
- rewrite `SignalRegistry` wholesale;
- migrate unrelated package generations;
- remove provenance/lineage safeguards merely to simplify the architecture;
- create a permanent two-authority cohort model;
- introduce another activation SSOT.

## STOP Conditions

STOP and escalate before further implementation if:

1. current repo state no longer matches the documented temporary Stage 1 two-authority architecture;
2. a later ratified decision explicitly requires permanent independent launch-critical activation authority;
3. current launch-critical eligibility is insufficient authority to create canonical activation entries without a new human/medical promotion decision;
4. one positive activation authority cannot be achieved without weakening launch-critical provenance/lineage safety;
5. fold-in requires inventing new medical policy or changing clinical meaning;
6. launch-critical package/frame identity cannot be mapped deterministically to canonical activation keys;
7. duplicate/conflicting activation identities are discovered;
8. exact full-estate activation-key determinism fails under identical governed inputs;
9. any runtime path still independently grants activation after the intended refactor;
10. unrelated authorised signals become unreachable;
11. previously blocked/ineligible launch-critical packages become reachable;
12. safe implementation requires a broad loader rewrite or unrelated package migration;
13. safe implementation requires modifying Automation Bus control-plane scripts:
    - `backend/scripts/run_work_package.py`
    - `backend/scripts/golden_gate_local.py`
    - `backend/scripts/update_cursor_status.py`

STOP 3, 4, 6, 7, 8, or 9 requires explicit GPT + Anthony architectural reassessment before further V5 convergence work.

## Success Criteria

All must be true:

- current temporary dual-authority baseline independently reproduced;
- launch-critical cohort inventoried from current repo reality;
- currently authorised launch-critical activations migrated into canonical activation authority without changing medical meaning;
- blocked/ineligible launch-critical packages remain blocked/ineligible;
- launch-critical provenance/lineage eligibility remains mandatory as a veto/prerequisite;
- launch-critical eligibility no longer independently grants activation;
- one positive runtime activation authority exists estate-wide;
- no new activation SSOT created;
- explicit medical-prohibition enforcement remains fail-closed;
- exact full-estate activation-key membership is deterministic;
- canonical Stage 2 regression module passes;
- Stage 1 canonical-gate tests pass;
- runtime medical-authority integrity tests pass;
- relevant existing regression suites pass;
- Day-One architecture validation passes;
- no control-plane files changed;
- temporary two-authority exception is explicitly retired in architecture documentation;
- mandatory post-implementation closure protocol passes;
- kernel finish returns PASS.

## Finish Evidence Required

Cursor must provide:

- pre-change launch-critical inventory with file + line citations;
- exact canonical activation entries added;
- before/after launch-critical activation-flow description;
- proof that launch-critical eligibility is now a veto/prerequisite only;
- proof that no runtime-loaded activation key exists outside the canonical register;
- proof that blocked/ineligible launch-critical packages remain unreachable;
- proof that currently authorised launch-critical behaviour is preserved;
- exact full-estate activation-key determinism outputs across repeated fresh loads;
- targeted test results;
- relevant regression results;
- Day-One architecture validator result;
- `git diff --check`;
- exact files changed;
- confirmation that no medical content, thresholds, prioritisation, WHY content or frontend output changed.

## Post-Implementation Closure

Before:

`python backend/scripts/run_work_package.py finish`

Cursor must execute the mandatory Automation Bus v1.3.1 post-implementation closure protocol, including branch/status/log/diff/stash evidence and explicit finish-readiness confirmation.

After successful finish, Cursor must re-run the required post-finish repo checks and handle the kernel-owned `latest_cursor_status.json` exactly per SOP v1.3.1.

Claude must then independently audit the completed package and explicitly answer:

1. Is there now exactly one positive runtime activation-grant authority estate-wide?
2. Can launch-critical provenance/lineage eligibility still independently activate anything?
3. Are all runtime-loaded activation keys represented in the canonical activation register?
4. Are blocked/ineligible launch-critical packages still unreachable?
5. Are explicit medical prohibitions still fail-closed?
6. Is full-estate activation-key membership deterministic under identical governed inputs?
7. Was the temporary Stage 1 two-authority exception genuinely retired?
8. Does the conditional `RETAIN_V5` decision remain supportable after full activation-authority convergence?

HIGH-risk merge requires GPT architectural review and Anthony approval.

## Hardening Invocation

Use exactly:

`harden work_id: V5-CANONICAL-ACTIVATION-GATE-2 — verify source content and produce evidence checklist`
