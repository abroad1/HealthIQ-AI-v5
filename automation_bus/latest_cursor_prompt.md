---
work_id: ARCH-CONV-GATE0
branch: feature/arch-conv-gate0-cohort-viability
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
stage_b_mode: MODE_2
runtime_change: NONE
---

# ARCH-CONV-GATE0 — Controlled-Beta Cohort and Convergence Viability Definition

## Outcome

Define the exact launch-critical cohort for the final HealthIQ AI v5 convergence programme and decide whether the programme is viable before any runtime changes begin.

This is a read-only planning and verification package.

Do not change runtime code, schemas, medical assets, tests, package manifests, loaders or production behaviour.

Standard Automation Bus governance applies.

## Required inputs

Read only:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION.md
docs/architecture/HEALTHIQ_AI_ARCHITECTURE_PROGRAMME_RECONCILIATION_CC.md
docs/architecture/HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS.md
docs/architecture/HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS_CC.md
docs/architecture/HEALTHIQ_AI_ARCHITECTURE_RECONCILIATION_VARIANCE_CC_VS_CURSOR.md
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Also inspect current `main` code and governed assets only where needed to verify:

```text
the five residual identity surfaces
signal registry loading
provenance classification and reachability
launch-critical package cohorts
root-cause authority
current representative and golden outputs
```

Do not reopen unrelated historical architecture questions already settled by the reconciliation.

## Questions to answer

### 1. Controlled-beta architecture cohort

Enumerate the exact proposed controlled-beta cohort.

For each item record:

```text
signal_id
activation_key
source_spec_id
biomarker or domain
package_id
runtime reachability
current firing status
launch relevance
provenance status
explicit lineage availability
WHY authority type
medical-review requirement
recommended cohort disposition
```

Allowed dispositions:

```text
INCLUDE
EXCLUDE
DEFER
REQUIRES_LINEAGE
REQUIRES_MEDICAL_REVIEW
UNVERIFIABLE
```

Do not estimate silently.

### 2. Residual identity exposure

Verify live exposure for:

```text
interpretation_display_layer_publish_v1.py
domain_score_assembler.py
narrative_report_compiler_v1.py
intervention_selector_v1.py
signal_interaction_builder.py
```

For each surface state:

```text
file and function
current keying behaviour
whether frame collapse is possible
which active multi-frame families can reach it
whether the behaviour is launch-critical
whether a full behaviour fix or smaller hardening package is justified
```

Do not assume every identified code smell has current live exposure.

### 3. Provenance-blocked runtime cohort

Enumerate every launch-critical package that is:

- provenance `BLOCKED`;
- `beta_eligible_explicit: false`;
- inferred-only;
- or otherwise unsuitable for an explicit beta claim.

For each determine:

```text
can load
can fire
can rank
can appear in user-facing output
appears in representative or golden output
canonical research source available
explicit lineage recoverable
product impact if suppressed
medical impact if suppressed
recommended action
```

Allowed actions:

```text
EXTRACT_AND_ATTACH
KEEP_ACTIVE_WITH_EXPLICIT_LINEAGE
MAKE_NON_REACHABLE
EXCLUDE_FROM_BETA_COHORT
DEFER_PENDING_RESEARCH
UNVERIFIABLE
```

Do not remove anything in this package.

### 4. WHY migration pilot cohort

Define a bounded representative pilot for the WHY convergence proof.

The pilot must be large enough to test:

- single-frame and multi-frame signals;
- current compiled and legacy authority paths;
- consumer and clinician outputs;
- provenance and replay;
- medical-review workflow;
- legacy retirement.

For each proposed pilot item record:

```text
signal_id
activation frames
current WHY authority
canonical research availability
existing medical review
new medical review required
migration complexity
reason for inclusion
```

Do not default to all 40 legacy hypotheses.

### 5. Medical-review viability

Confirm:

- medical-review owner;
- review inputs;
- review output format;
- expected decision route;
- unresolved dependencies;
- whether the pilot can be completed within the approved programme window.

Do not invent availability or commitment.

If capacity is not evidenced, mark it unresolved.

### 6. Programme ceilings

Propose explicit values for human approval:

```text
maximum planned architecture packages
maximum unplanned follow-on packages
maximum material scope growth per package
maximum programme duration
maximum engineering effort
maximum medical-review effort
lineage failure threshold
```

The existing plan already fixes:

```text
maximum unplanned mandatory packages: 1
maximum unauthorised material scope growth: 25%
```

Do not change those without explicit justification.

## Required outputs

Create:

```text
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md
```

### Controlled-beta cohort

Include:

- exact cohort inventory;
- inclusions and exclusions;
- activation-frame inventory;
- provenance and reachability status;
- launch relevance;
- unresolved evidence.

### Viability assessment

Include:

- identity exposure findings;
- provenance-blocked runtime findings;
- product impact of suppression;
- canonical lineage recoverability;
- medical-review viability;
- proposed programme ceilings;
- kill-criteria assessment;
- decision.

### WHY pilot cohort

Include:

- exact pilot;
- selection rationale;
- medical-review dependencies;
- architecture coverage;
- exclusions;
- pilot success criteria.

## Decision

Issue exactly one decision:

```text
GO
REDESIGN
V6
```

### GO

Use only if:

- the launch-critical cohort is isolatable;
- identity scope is bounded;
- provenance lineage or safe exclusion is feasible;
- the WHY pilot is bounded;
- medical-review route is credible;
- programme ceilings can be set.

### REDESIGN

Use if v5 still appears salvageable but the proposed package sequence or cohort must change before implementation.

State the exact revised sequence.

### V6

Use if any kill criterion is already met, including:

- cohort isolation failure;
- unrecoverable canonical lineage at material scale;
- unavoidable estate-wide disruption;
- no executable WHY pilot;
- architecture scope already exceeds the approved ceiling.

## Quantitative requirements

Report verified counts where possible:

- proposed beta signal families;
- activation frames;
- active multi-frame families in the cohort;
- exposed identity surfaces;
- blocked launch-critical packages;
- blocked packages currently reachable;
- packages requiring lineage extraction;
- packages recommended for suppression;
- proposed WHY pilot signals and frames;
- medical reviews required.

Where a count is not reliable, state why.

## STOP conditions

STOP and escalate if:

1. latest `main` cannot be identified;
2. the planning paper is missing or not merged;
3. any of the five identity surfaces cannot be inspected;
4. runtime reachability cannot be verified;
5. canonical research sources cannot be located for the proposed cohort;
6. cohort membership requires a new medical or product policy decision;
7. medical-review ownership cannot be established;
8. repository state is not clean at package start;
9. verification would require runtime changes.

## Acceptance criteria

- [ ] Exact controlled-beta architecture cohort is documented.
- [ ] All five identity surfaces have verified exposure findings.
- [ ] Provenance-blocked runtime cohort is fully enumerated.
- [ ] Product and medical impact of suppression is recorded.
- [ ] Canonical lineage recoverability is assessed.
- [ ] WHY migration pilot is bounded and representative.
- [ ] Medical-review viability is assessed honestly.
- [ ] Programme ceilings are proposed.
- [ ] Kill criteria are explicitly tested.
- [ ] GO / REDESIGN / V6 decision is issued.
- [ ] No runtime, schema, test or medical-content files are changed.
- [ ] No Package 1 implementation prompt is authored.
- [ ] No beta-readiness declaration is made.

## Verification report

Create:

```text
docs/audit-papers/ARCH-CONV-GATE0_implementation_and_verification_report.md
```

Include:

- baseline SHA;
- branch;
- evidence read;
- files inspected;
- commands used;
- quantitative totals;
- acceptance-criteria table;
- STOP-condition assessment;
- final decision and rationale;
- unresolved limitations.

Do not merge without explicit human authority.
