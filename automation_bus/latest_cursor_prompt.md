---
work_id: ARCH-CONV-PKG2
branch: feature/arch-conv-pkg2-provenance-reachability
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
stage_b_mode: MODE_2
runtime_change: YES
---

# ARCH-CONV-PKG2 — Launch-Critical Provenance and Runtime-Reachability Closure

## Outcome

Align launch-critical provenance status with actual runtime behaviour.

Every package in the controlled-beta architecture cohort must either:

1. have explicit, defensible research lineage and remain runtime-reachable; or
2. be non-claimable and non-reachable by explicit governed decision.

This package closes the current mismatch where provenance-blocked packages can still load, fire, rank and appear in user-facing output.

Do not change WHY authority, prose assets, PSI, Gemini, signal thresholds, signal firing logic, medical hypotheses or frontend medical-selection behaviour.

Standard Automation Bus and Knowledge Bus governance apply.

## Required inputs

Read only:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS_CC.md
docs/architecture/HEALTHIQ_AI_ARCHITECTURE_RECONCILIATION_VARIANCE_CC_VS_CURSOR.md
docs/architecture/ADR-RT-004*
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md
docs/audit-papers/ARCH-CONV-PKG1_implementation_and_verification_report.md
```

Resolve actual repository paths where names differ.

Inspect current production code and tests for:

```text
signal registry package discovery and loading
package-manifest parsing
provenance classification
signal evaluation
top-finding ranking
report compilation
replay / audit manifests
launch-critical provenance gates
golden and representative outputs
```

## Controlled-beta cohort

Use the exact cohort and dispositions from Gate 0.

Do not expand this package to all package generations or all 191 manifests.

At minimum assess all launch-critical `pkg_kb47_*` packages identified by Gate 0 and the provenance inventory.

## Phase 1 — Cohort decision and impact analysis

Before changing runtime behaviour, produce a package-level decision table.

For every launch-critical provenance-blocked or inferred-only package, record:

```text
package_id
signal_id
activation_key
current provenance status
current beta eligibility
source research location
explicit source_spec_id available
lineage recoverable
currently loadable
currently capable of firing
currently capable of ranking
appears in golden or representative outputs
product impact if made non-reachable
medical impact if made non-reachable
recommended disposition
human approval required
```

Allowed dispositions:

```text
ATTACH_EXPLICIT_LINEAGE
KEEP_REACHABLE_AFTER_LINEAGE
MAKE_NON_REACHABLE
EXCLUDE_FROM_BETA_COHORT
DEFER_PENDING_RESEARCH
STOP_FOR_HUMAN_DECISION
```

Create:

```text
docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md
```

## STOP Gate 1 — Before implementation

STOP and escalate if:

- a package is currently relied upon in Wave 1 or representative outputs and suppression lacks product/medical approval;
- `source_spec_id` would need to be invented;
- batch research cannot be mapped to a defensible activation frame;
- a package contains multiple possible source frames and no approved selection exists;
- package eligibility and runtime reachability cannot be separated safely;
- scope expands into estate-wide regeneration;
- Package 3 WHY decisions become a prerequisite;
- the approved controlled-beta cohort must materially change.

Do not silently choose suppression over lineage recovery.

## Required implementation

### 1. Explicit lineage attachment

For packages approved to remain in the controlled-beta cohort:

- attach a genuine `source_spec_id`;
- preserve `activation_key`;
- record source hashes and compile identity where the existing contract supports them;
- update package manifests through the governed schema;
- do not infer explicit lineage from directory names or descriptive text;
- do not alter the medical meaning of the signal.

Where extraction from approved batch research is required:

- preserve exact frame identity;
- create or attach a governed investigation specification;
- STOP if extraction introduces new medical interpretation.

### 2. Runtime reachability policy

Implement one canonical runtime-eligibility decision used by package discovery/loading.

The policy must distinguish:

```text
production reachable
test-only
candidate
blocked for explicit claim
excluded from controlled beta
non-reachable
```

Requirements:

- launch-critical packages without acceptable explicit lineage must not load into the controlled-beta runtime path;
- test and validation modes may load excluded fixtures only through explicit opt-in;
- policy must fail closed for unknown or contradictory status;
- package discovery must not rely on directory globbing alone;
- runtime behaviour must agree with provenance inventory and validation gates;
- no silent fallback to legacy/inferred eligibility.

Do not delete package assets merely to achieve non-reachability.

### 3. Signal evaluation and ranking

Prove that a non-reachable package:

- does not enter `SignalRegistry`;
- cannot fire;
- cannot be scored;
- cannot rank as a top finding;
- cannot appear in narrative, clinician or consumer reports;
- cannot appear in replay as an active result.

Its exclusion decision must remain auditable.

### 4. Report and replay honesty

For reachable launch-critical results:

- carry explicit provenance;
- preserve activation identity;
- expose the governed authority status;
- preserve deterministic replay.

For excluded packages:

- record exclusion in the appropriate architecture or launch-estate inventory;
- do not create phantom result rows.

### 5. Golden and representative-output review

Before making any package non-reachable:

- run the relevant golden and representative panels;
- identify changed outputs;
- classify each change as intended, unintended or unresolved;
- obtain explicit human approval for intended removal of user-visible findings;
- STOP on unexplained clinical or product regression.

Create:

```text
docs/architecture/ARCH-CONV-PKG2_runtime_suppression_impact_report.md
```

## Shared implementation rules

- Reuse the existing provenance status model.
- Prefer one canonical loader eligibility function.
- Do not create separate eligibility logic in registry, evaluator and report compiler.
- Unknown status must fail closed.
- Preserve test-only access through explicit test flags only.
- Do not change signal thresholds or medical firing conditions.
- Do not suppress a package because it is inconvenient to migrate.
- Do not attach lineage without a source artefact.
- Keep all changes bounded to the Gate 0 controlled-beta cohort plus shared loader/gate infrastructure.

## Tests

At minimum prove:

1. every included launch-critical package has explicit lineage;
2. a blocked launch-critical package cannot enter the production registry;
3. a blocked package cannot fire or rank;
4. a blocked package cannot appear in consumer or clinician output;
5. test-only opt-in can still load designated fixtures;
6. unknown or contradictory status fails closed;
7. valid explicitly sourced packages remain reachable;
8. activation keys survive lineage attachment;
9. replay preserves explicit provenance for reachable results;
10. exclusion decisions are auditable;
11. golden-output changes match the approved impact report;
12. no unrelated package generation is affected;
13. repeated runs are deterministic;
14. architecture and provenance gates fail on deliberately invalid fixtures.

Run relevant existing:

- signal-registry tests;
- provenance status tests;
- package-manifest schema tests;
- signal-evaluator tests;
- report compiler tests;
- narrative and clinician-report tests;
- replay/auditability tests;
- golden panels;
- launch-estate validation;
- architecture validation gate;
- NO-LLM tests;
- Package 1 identity tests.

## Validation gate

Extend or add one executable launch-critical provenance/reachability gate.

It must detect:

- reachable launch-critical package without explicit lineage;
- beta-ineligible package loaded into the production registry;
- contradictory manifest and inventory status;
- unknown eligibility status;
- inferred lineage represented as explicit;
- excluded package appearing in user-facing output;
- activation-key/source-spec mismatch.

The gate must exercise real loading behaviour, not only source-text inspection.

## Forbidden scope

Do not:

- migrate or edit WHY assets;
- change root-cause hypotheses;
- create or promote prose;
- wire PSI;
- enable Gemini;
- change medical thresholds;
- change signal firing conditions;
- redesign the frontend;
- perform estate-wide package regeneration;
- remove package directories as a substitute for governed exclusion;
- declare architecture convergence or beta readiness.

## Deliverables

Create:

```text
docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md
docs/architecture/ARCH-CONV-PKG2_runtime_suppression_impact_report.md
docs/audit-papers/ARCH-CONV-PKG2_implementation_and_verification_report.md
```

Update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Record:

- exact packages given explicit lineage;
- exact packages made non-reachable;
- human approvals obtained;
- golden-output changes;
- unresolved packages;
- no beta-readiness claim.

## Acceptance criteria

- [ ] Gate 0 launch-critical cohort was used without silent expansion.
- [ ] Every affected package has a documented disposition.
- [ ] STOP Gate 1 passed or escalated.
- [ ] Every reachable launch-critical package has explicit lineage.
- [ ] Every launch-critical package without acceptable lineage is non-reachable.
- [ ] No blocked or beta-ineligible package can fire or rank.
- [ ] Runtime loading and provenance classification use one canonical policy.
- [ ] No user-visible finding was removed without impact review and approval.
- [ ] Golden and representative-output changes are documented.
- [ ] Replay and report provenance remain deterministic and explicit.
- [ ] Package 1 frame-identity behaviour remains intact.
- [ ] Relevant tests and validation gates pass.
- [ ] No WHY, prose, PSI, Gemini or threshold scope entered.
- [ ] No architecture-completion or beta-readiness claim was made.

## STOP conditions

STOP if:

1. a relied-upon Wave 1 finding would be removed without explicit approval;
2. canonical lineage cannot be recovered without invention;
3. package scope grows by more than 25% without human reauthorisation;
4. more than one unplanned mandatory follow-on package is identified;
5. the controlled-beta cohort cannot be isolated from the wider estate;
6. provenance policy requires changing medical signal logic;
7. unresolved output regressions remain;
8. required gates fail for an unexplained reason;
9. completion requires Package 3 medical-content decisions.

## Gate 2 output

At completion, recommend exactly one:

```text
GO
CORRECT
STOP
V6
```

Definitions:

- `GO`: Package 2 obligation is closed; proceed to Gate 2.5.
- `CORRECT`: one bounded correction is required.
- `STOP`: convergence approach requires redesign.
- `V6`: kill criteria are met; freeze v5 architecture changes.

## Verification report

Include:

- baseline SHA;
- branch;
- files changed;
- package-by-package decisions;
- lineage sources attached;
- runtime-policy before/after;
- golden-output impact;
- human approvals;
- test commands and exit codes;
- validation-gate evidence;
- acceptance-criteria table;
- STOP-condition assessment;
- Gate 2 recommendation;
- unresolved limitations.

Do not merge without explicit human authority.
