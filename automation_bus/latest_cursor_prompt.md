---
work_id: P1-5
branch: work/P1-5-ft3-thyroid-authority-reconciliation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-5 — FT3 / Thyroid Authority Reconciliation

## Objective

Resolve the governance contradiction that blocked P1-4.

P1-4 correctly stopped before thyroid runtime implementation because FT3 low authority was contradictory across multiple governance/register files, the hormonal scoring rail was inert, TSH package authority was inactive, and kb59 antibody material was not runtime-governed.

This sprint is a governance reconciliation sprint.

It must not implement the thyroid / energy regulation domain card.

It must produce a clear, auditable authority position for thyroid runtime readiness and define the exact preconditions for retrying P1-4.

---

## Required outcome

The sprint must answer and, where safe, reconcile:

```text
What is the authoritative runtime position for FT3 low, FT3 high, FT4 high, FT4 low, TSH high/low, and thyroid antibodies?
```

The safest default is:

```text
No thyroid signal may be treated as runtime active unless all relevant governance files clearly support that status.
```

FT3 low must not be activated by this sprint.

If the evidence remains unresolved, the sprint must document the conflict and stop without changing authority files beyond the blocker report/register entry.

---

## Critical scope rule

This is not a thyroid implementation sprint.

Do not change runtime code.

Do not change scoring logic.

Do not create a thyroid compiled card.

Do not wire a thyroid domain row.

Do not alter `domain_score_assembler.py`.

Do not alter `domain_narrative_wave1.py`.

Do not alter `wave1_subsystem_evidence.py`.

Do not alter DTO/replay contracts.

Do not touch frontend files.

Do not use Gemini.

Do not introduce fallback parser logic.

Do not promote Pass 3 material.

Do not modify Knowledge Bus source packages.

Do not activate blocked or context-dependent thyroid signals.

Do not create diagnostic thyroid disease language.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull
git status --short
git switch -c work/P1-5-ft3-thyroid-authority-reconciliation
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Prerequisites

Required files on `main`:

```text
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text
P1-5 prerequisite evidence is not present on main. P1-5 must not proceed.
```

---

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

P1-4 is the immediate trigger authority for this reconciliation sprint.

---

## Files/registers to locate and inspect

Locate the following files by exact filename search if their full paths are not already known:

```text
batch2_thyroid_gate_execution_register_v1.yaml
batch2_full_coverage_activation_execution_register_v1.yaml
batch2_context_clearance_register_v1.yaml
medical_frame_identity_index_v1.yaml
root_cause_authority_register_v1.yaml
```

Also search for:

```text
FT3
Free T3
free_t3
T3
FT4
Free T4
free_t4
T4
TSH
thyroid
thyrotoxicosis
low T3
non-thyroidal illness
thyroid authority
activation_eligibility
runtime_active_canonical
blocked
deferred
```

If any expected file cannot be found, record that clearly and do not invent its contents.

---

## Phase 1 — Authority audit

Create a concise authority audit table covering at least:

```text
FT3 low
FT3 high
FT4 low
FT4 high
TSH high
TSH low
thyroid antibodies
```

For each item, record:

```text
- register/file path
- current status
- activation eligibility
- runtime active/inactive/deferred/blocked/context-dependent status
- notes/comments
- contradictions
- whether medical review is present or absent
- whether root-cause mapping is present or future-mapped
```

You must explicitly cover the P1-4 findings:

```text
- FT3 low deferred in batch2_thyroid_gate_execution_register_v1.yaml
- FT3 low runtime_active_canonical in batch2_full_coverage_activation_execution_register_v1.yaml
- FT3 low inactive / activation_eligibility false in batch2_context_clearance_register_v1.yaml
- FT3 low internal contradiction in medical_frame_identity_index_v1.yaml
- FT3 low ROOT_CAUSE_REQUIRES_FUTURE_MAPPING in root_cause_authority_register_v1.yaml
- hormonal scoring rail has system_weight 0.0 and no biomarkers
- kb52c TSH packages inactive
- kb59 antibodies inactive
```

If any of the above are not confirmed from the repository, state that honestly.

---

## Phase 2 — Reconciliation decision

After Phase 1, decide whether a safe reconciliation can be made.

The only acceptable reconciliation directions are:

```text
1. Confirm FT3 low and any unresolved thyroid patterns as NOT runtime active / deferred / blocked pending governance.
2. Confirm specific thyroid patterns as eligible only if every relevant authority source supports that status.
3. Leave files unchanged and produce a blocker report if authority cannot be reconciled safely.
```

Do not choose the permissive interpretation where files conflict.

Do not treat `runtime_active_canonical` in one file as sufficient authority if another register says deferred, inactive, or future-mapped.

Do not activate FT3 low.

Do not create runtime authority for context-dependent thyroid patterns.

---

## Permitted changes

This sprint may change only documentation/governance files required to remove contradiction or document unresolved contradiction.

Permitted outputs:

```text
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Governance/register YAML files may be changed only if all of the following are true:

```text
- the intended correction is to make authority more conservative, not more permissive;
- the correction resolves an internal contradiction or known drift;
- the corrected status is NOT runtime active / deferred / blocked / requires future mapping;
- no thyroid signal becomes newly active;
- no package becomes promoted;
- no runtime behaviour is created;
- the final report identifies every file changed and every status changed.
```

If a governance file appears to be runtime-consumed and the behavioural effect is uncertain, do not modify it. Record the required correction in the ADR and leave the file unchanged for a later dedicated activation-control sprint.

---

## Prohibited changes

Do not change:

```text
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
backend/ssot/scoring_policy.yaml
knowledge_bus/compiled/
frontend/
```

Do not change Knowledge Bus source packages.

Do not change Pass 3 source material.

Do not change medical-review conclusions.

Do not write new clinical interpretations.

Do not add tests for a runtime thyroid implementation because no implementation is authorised in this sprint.

---

## Required deliverable 1 — Reconciliation report

Create:

```text
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
```

Use this structure:

```markdown
# P1-5 — FT3 / Thyroid Authority Reconciliation

## 1. Summary
- why this sprint was required
- whether authority was reconciled or remains blocked
- whether any governance/register files were changed
- whether P1-4 retry is allowed or still blocked

## 2. Authority files inspected
- list each file inspected
- path
- purpose
- whether it was changed

## 3. Thyroid marker and signal status table
| Marker / pattern | File/register | Current status before P1-5 | Conflict? | P1-5 reconciled position | File changed? | Notes |
|---|---|---|---|---|---|---|

Must include:
- FT3 low
- FT3 high
- FT4 low
- FT4 high
- TSH high
- TSH low
- thyroid antibodies

## 4. FT3 low reconciliation
- all positions found
- contradiction analysis
- final authority position
- rationale
- whether any file was corrected
- why FT3 low remains inactive/deferred if applicable

## 5. Other thyroid authority findings
- FT3 high
- FT4 high
- FT4 low
- TSH high/low
- thyroid antibodies
- TSH package status
- antibody package status
- root-cause mapping status

## 6. Hormonal scoring rail assessment
- current scoring rail status
- whether it is inert
- whether scoring policy was changed
- why scoring policy was not changed if left untouched
- preconditions for future thyroid scoring activation

## 7. P1-4 retry decision
State one of:
- P1-4 retry permitted
- P1-4 retry blocked
- P1-4 retry permitted only after named preconditions

List the exact preconditions.

## 8. Files changed
- list every changed file
- for each governance/register file changed, list the exact status correction

## 9. Safety and architecture boundaries
Confirm:
- no runtime code changed
- no scoring policy changed unless explicitly justified
- no signal activated
- no package promoted
- no Knowledge Bus source packages changed
- no Pass 3 artefacts changed
- no Gemini/frontend/fallback parser introduced

## 10. Recommended next sprint
Recommend the next sprint:
- P1-4 retry if all blockers resolved
- or next governance/scoring/package-promotion sprint if blockers remain
```

---

## Required deliverable 2 — ADR

Create:

```text
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
```

Use this structure:

```markdown
# ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1

## Status
Accepted / Proposed / Blocked

## Context
Summarise why P1-4 stopped and why this ADR is needed.

## Decision
State the authoritative runtime position for:
- FT3 low
- FT3 high
- FT4 high
- FT4 low
- TSH high/low
- thyroid antibodies

If unresolved, state that clearly.

## Non-negotiable constraints
- no permissive interpretation where registers conflict
- no FT3 low activation without explicit resolved authority
- no context-dependent thyroid signal activation without required context model
- no hardcoded reference ranges
- no diagnostic thyroid disease wording
- no Layer C/Gemini/frontend reasoning

## Consequences
- what P1-4 retry may or may not do
- what remains blocked
- what future sprint must resolve if needed

## Files/registers reviewed
List reviewed files.

## Supersession / correction notes
State whether this ADR supersedes, clarifies, or requires correction to any existing register entry.
```

If the ADR status cannot be Accepted because authority remains unresolved, use:

```text
Status: Blocked
```

Do not pretend the authority is resolved if it is not.

---

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-5 — FT3 / thyroid authority reconciliation

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major governance decision or reconciliation outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the register entry short.

Do not list every file touched.

Do not duplicate the full reconciliation report.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

If YAML governance/register files are changed, run any available YAML/schema validation for those files.

If no schema validation exists, state that clearly.

No runtime test suite is required if no runtime files are changed.

If any prohibited runtime/code file is changed, stop and report failure.

---

## Required final report

Return:

```text
- branch name
- whether authority was reconciled or remains blocked
- FT3 low final position
- thyroid marker/pattern statuses agreed
- files changed
- whether any governance/register YAML files were changed
- whether any runtime/code/scoring files were changed
- validation run and results
- whether P1-4 retry is now permitted
- remaining blockers
- recommended next sprint
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text
1. P1-5 reconciliation report exists at:
   docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md

2. ADR exists at:
   docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md

3. FT3 low status is explicitly resolved or explicitly declared unresolved/blocked.

4. The report covers at least:
   - FT3 low
   - FT3 high
   - FT4 low
   - FT4 high
   - TSH high
   - TSH low
   - thyroid antibodies

5. No permissive runtime interpretation is chosen where registers conflict.

6. No thyroid signal is newly activated.

7. No thyroid package is promoted.

8. No runtime code, frontend code, Gemini path, fallback parser, compiled thyroid card, DTO contract, domain assembler, narrative helper, subsystem evidence file, or scoring policy is changed unless the sprint stops and reports a failure.

9. Any governance/register file change is conservative and explicitly documented.

10. The hormonal scoring rail position is assessed and either left unchanged with rationale or reported as requiring a separate scoring sprint.

11. P1-4 retry decision is explicit.

12. Build deliverable register is updated with a short P1-5 entry.

13. Final report includes validation output and clean git status.
```
