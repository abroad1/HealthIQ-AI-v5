---
work_id: P1-10
branch: work/P1-10-pass3-launch-core-signal-intelligence-batch-a
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-10 — Pass 3 Launch-Core Signal Intelligence Batch A

## Objective

Promote a meaningful first batch of rich Pass 3 medical research into the governed HealthIQ AI signal-intelligence estate.

This sprint is part of the eight-block beta-readiness programme.

It follows:

```text
P1-7 — Research-to-runtime adequacy gate
P1-8 — Scoring lab-range engine
P1-9 — Pass 3 research-to-runtime exploitation map
```

P1-9 established that the upstream Pass 3 research estate is rich, but a large part of that richness has not yet been promoted into governed signal intelligence, root-cause / WHY material, compiled-card support, scoring readiness, prose/explainer substrate, test coverage and runtime-readiness states.

This sprint starts the batch-based promotion factory.

It must not become a one-marker micro-sprint.

It must not become uncontrolled sitewide mass promotion.

It must promote a sensible first cohort of related, high-value, launch-core or launch-adjacent signal clusters from Pass 3 into the appropriate governed signal-intelligence repository, with explicit inactive / blocked / review-required states where runtime activation is not yet safe.

## Strategic purpose

HealthIQ AI’s defensible value is not simply that research exists.

The strategic value is the repeatable, auditable production line that converts rich medical research into:

```text
governed signal intelligence
safe activation conditions
context requirements
root-cause / WHY reasoning
evidence and provenance
scoring readiness
prose/explainer substrate
testable runtime artefacts
```

This sprint is the first production use of that promotion discipline.

The business goal is to capture the richness of the Pass 3 research estate in a governed signal repository without prematurely exposing that intelligence to users.

## Critical architectural rule

Promotion is not activation.

This sprint may promote signal intelligence into governed repository structures.

This sprint must not activate new runtime signals unless the existing governance model already allows that safely and the prompt explicitly permits it.

For this sprint, default all newly promoted or newly enriched signal intelligence to non-runtime-active states unless the existing repository schema requires a different explicit inactive state.

Use repository-native state names only.

Do not invent new lifecycle enums.

If the required inactive / review / blocked state vocabulary is unclear, stop and report the blocker.

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull origin main
git status --short
git rev-parse main
git rev-parse origin/main
```

Confirm:

```text
- current branch is main
- local main == origin/main
- working tree is clean
```

Then create:

```powershell
git switch -c work/P1-10-pass3-launch-core-signal-intelligence-batch-a
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

## Required prerequisites on main

These files must exist on `main`:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text
P1-10 prerequisite beta-readiness evidence is not present on main. P1-10 must not proceed.
```

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

The Pass 3 promotion protocol is included here because this sprint directly concerns research-to-signal promotion.

Do not list standard SOP files as authority documents in the deliverable unless a specific governance requirement cannot otherwise be located.

## Authoritative signal repository discovery

Before writing any signal content, discover the authoritative signal-intelligence repository path and loader/validator.

Search for:

```text
promoted_signal_intelligence
signal_intelligence
signal intelligence
activation_eligibility
runtime_active
signal_id
signal_repository
intelligence_model
root_cause
why
```

Inspect likely locations:

```text
knowledge_bus/
knowledge_bus/governance/
knowledge_bus/compiled/
knowledge_bus/manifests/
backend/core/
backend/core/knowledge/
backend/core/analytics/
backend/ssot/
docs/architecture/
docs/intelligence/
```

You must establish:

```text
- the authoritative file or files that represent promoted signal intelligence;
- the schema or contract governing those files;
- the validator, tests or loaders that consume them;
- whether runtime currently consumes them;
- whether they support inactive / blocked / review-required states;
- whether a duplicate or legacy authority source exists.
```

STOP if:

```text
- no authoritative signal repository can be identified;
- multiple competing signal-intelligence authorities exist and no clear source of truth is documented;
- there is no clear schema/contract for the target artefact;
- adding entries would require inventing lifecycle states;
- adding entries would make them runtime-active unintentionally.
```

If stopped, produce the sprint report and build-register entry as Blocked. Do not create ad hoc signal files.

## Batch A scope

Use P1-9 to select the first batch.

This batch should cover a meaningful cohort of high-value, launch-core or launch-adjacent research clusters, not individual isolated markers.

Target size:

```text
Minimum: 4 material clusters
Maximum: 8 material clusters
```

The intended Batch A candidates should be selected from P1-9’s highest-value unpromoted or partially promoted areas, prioritising:

```text
- launch-core relevance;
- evidence richness in Pass 3;
- downstream signal-intelligence gap;
- scoring readiness or scoring-blocked clarity after P1-8;
- ability to promote intelligence without runtime activation;
- commercial value for HealthIQ’s systems-level interpretation.
```

Expected candidate clusters to consider include, if supported by P1-9 and repository evidence:

```text
- cardiovascular lipid / derived cluster
- kidney / eGFR / creatinine / urea cluster
- thyroid axis cluster
- thyroid antibodies cluster
- liver enzyme / liver stress cluster
- homocysteine / one-carbon cluster
- metabolic / glycaemic cluster if P1-9 identifies residual signal-depth gaps
- CBC / iron / oxygen cluster only where frame authority does not block safe inactive promotion
```

Do not force all of these into the batch.

Do not exceed the maximum batch size unless the report justifies why clusters are inseparable.

If the selected scope would become too large to preserve quality, stop after the first 4–6 highest-value clusters and record the remainder as Batch B carry-forward.

## Pass 3 depth requirement

For each selected cluster, inspect the related Pass 3 / investigation-spec research directly.

Do not rely only on:

```text
- P1-9 summary
- package files
- compiled cards
- estate index
- runtime registers
- previous sprint notes
```

Use P1-9 as the map, but re-read the relevant Pass 3 source content for the selected Batch A clusters.

For each selected cluster, extract and preserve:

```text
- biomarkers involved;
- high/low/directional patterns;
- biological rationale;
- context requirements;
- corroborating markers;
- suppression/avoidance conditions;
- safety cautions;
- non-diagnostic wording constraints;
- root-cause / WHY material;
- system/subsystem mapping;
- evidence/provenance references;
- scoring implications;
- prose/explainer implications;
- whether runtime activation is safe, blocked, or deferred.
```

Do not flatten rich research into a one-line signal.

The purpose is to preserve usable medical intelligence, not merely to create a signal placeholder.

## Promotion principles

For each selected cluster, create or enrich governed signal-intelligence entries according to the repository’s existing schema.

Each promoted signal-intelligence entry must include, where the schema supports it:

```text
- stable signal identifier;
- source Pass 3 path/spec reference;
- biomarker(s);
- directionality;
- activation concept;
- required lab evidence;
- contextual requirements;
- corroborating markers;
- suppression or non-activation conditions;
- safety cautions;
- root-cause / WHY explanation substrate;
- system/subsystem mapping;
- scoring readiness state;
- medical-review status;
- runtime visibility / activation state;
- evidence/provenance;
- test requirement or validation note.
```

Use existing field names and schema conventions only.

Do not invent schema fields unless the existing schema explicitly allows extensions and the validator is updated accordingly.

If schema extension is required, stop and report the proposed extension rather than implementing it in this sprint.

## Runtime activation rule

No newly promoted Batch A signal may become user-visible or runtime-active in this sprint.

Default expected status:

```text
research-promoted / signal-intelligence-promoted / inactive / blocked / review-required
```

Use the repository’s real status terminology.

If the only available status is runtime-active, stop.

## Specific safety constraints

Do not add diagnostic claims.

Do not recommend treatment.

Do not add user-facing prose that implies diagnosis.

Do not add global/default reference ranges.

Do not override lab-provided reference ranges.

Do not add placeholder scoring bands.

Do not add new production scoring-policy entries.

Do not add thyroid production scoring.

Do not activate FT3, FT4, TSH, thyroid antibody, eGFR, urea, lipid-derived or homocysteine signals unless a later sprint explicitly authorises activation.

Do not change runtime interpretation behaviour.

## Permitted changes

Expected product changes may include:

```text
- governed signal-intelligence repository entries or enrichments, if the authoritative repository is identified;
- associated signal-intelligence manifest entries, if required by the existing schema;
- validation fixtures for the promoted signal-intelligence content, if the repository already has validation patterns;
- documentation report;
- build deliverable register entry.
```

Expected documentation deliverables:

```text
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

The manifest is a planning/audit artefact unless the existing repository contract says otherwise.

Do not place the manifest in a runtime path.

## Prohibited changes

Do not modify:

```text
frontend/
Gemini paths
fallback parser paths
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
backend/ssot/scoring_policy.yaml
knowledge_bus/source package files
Pass 3 source files
compiled health-system cards
compiled subsystem cards
runtime DTO contracts
```

Do not modify:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

Do not create a duplicate signal repository.

Do not create a parallel authority file because the real target was hard to find.

## Required deliverable 1 — Sprint report

Create:

```text
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
```

Use this structure exactly:

```markdown
# P1-10 — Pass 3 Launch-Core Signal Intelligence Batch A

## 1. Executive summary
- why this sprint was run
- what Batch A promoted
- whether the authoritative signal repository was found
- whether runtime activation remains unchanged
- estate-level value delivered
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness
- relationship to P1-7
- relationship to P1-8
- relationship to P1-9
- why this sprint is batch-based rather than one-marker-at-a-time

## 3. Signal repository discovery
- paths searched
- authoritative signal repository found
- loader/validator found
- schema/contract found
- duplicate/legacy authority check
- STOP concerns, if any

## 4. Batch A selection rationale
- clusters considered
- clusters selected
- clusters deferred
- why this is the right-sized batch
- why this is not uncontrolled mass promotion

## 5. Pass 3 source inspection
For each selected cluster:
- Pass 3 files/specs inspected
- biomarkers/patterns found
- rich research themes extracted
- limitations

## 6. Promotion implementation
For each selected cluster:
- signal intelligence created or enriched
- source evidence path
- state/status applied
- runtime activation state
- scoring readiness state
- medical-review state
- system/subsystem mapping
- root-cause / WHY material captured
- prose/explainer substrate captured
- tests/validation implications

## 7. Safety and non-activation confirmation
Confirm:
- no runtime activation
- no frontend/Gemini change
- no scoring_policy change
- no compiled card change
- no DTO change
- no Pass 3 source change
- no Knowledge Bus source package change
- no global/default ranges
- no placeholder bands
- no diagnostic or treatment claims

## 8. Validation
- validators run
- YAML parse checks
- repository-specific validation
- git diff checks
- limitations

## 9. Business value delivered
Explain:
- how much Pass 3 richness was captured
- why Batch A improves HealthIQ’s defensibility
- how this improves the signal estate without exposing unsafe runtime behaviour
- what future batches can now copy as a pattern

## 10. Carry-forwards
- clusters deferred to Batch B
- blockers requiring medical review
- blockers requiring frame adjudication
- blockers requiring scoring policy
- blockers requiring prose/WHY uplift
- blockers requiring runtime integration

## 11. Recommended next sprint
Recommend the next sprint with:
- title
- risk_level
- change_type
- scope
- STOP gates
- rationale
```

## Required deliverable 2 — Batch A manifest

Create:

```text
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
```

Use this structure:

```yaml
work_id: P1-10
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
signal_repository:
  authoritative_path: <path>
  schema_or_contract_path: <path>
  validator_or_loader_path: <path>
  runtime_consumed: true | false | unknown
batch:
  name: Pass 3 Launch-Core Signal Intelligence Batch A
  selection_basis:
    - <reason>
  clusters_selected: <number>
  clusters_deferred: <number>
clusters:
  - id: <stable_cluster_slug>
    name: <human readable cluster name>
    source_pass3_paths:
      - <path>
    source_spec_ids:
      - <spec_id>
    biomarkers:
      - <biomarker>
    system_mapping:
      - <system>
    subsystem_mapping:
      - <subsystem>
    promotion_action: created | enriched | deferred | blocked
    signal_repository_entries:
      - <signal_id_or_entry_path>
    runtime_activation_state: inactive | blocked | review_required | not_runtime_consumed | unknown
    scoring_readiness: ready | partial | blocked | deferred | not_applicable | unknown
    medical_review_status: reviewed | partial | required | blocked | unknown
    downstream_gaps:
      - <gap>
    evidence_paths:
      - <path>
    recommended_next_action: <short action>
deferred_clusters:
  - id: <stable_cluster_slug>
    reason: <reason>
validation:
  yaml_parse: pass | fail | not_run
  repository_validator: pass | fail | not_run | not_found
  runtime_activation_check: pass | fail | not_run
```

The manifest must describe what was promoted and what was deferred.

It must not be consumed by runtime unless an existing documented contract already says that this path is consumed.

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-10 — Pass 3 launch-core signal intelligence Batch A

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major signal-intelligence promotion outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the entry short.

Do not list every file touched.

Do not duplicate the full report.

## Required validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Validate any changed YAML files with a PowerShell-compatible Python command.

At minimum:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-10'; assert 'clusters' in data; print('P1-10 Batch A manifest YAML parsed successfully')"
```

Run any existing repository validators for the signal-intelligence artefact.

If no validator exists, record this clearly.

If a validator exists and fails, stop and report failure.

Run targeted tests only if signal repository changes are covered by tests.

Do not run broad unrelated suites unless necessary.

## Runtime non-activation validation

Prove that runtime activation did not change.

At minimum, report:

```text
- git diff --name-only
- whether backend runtime files changed
- whether scoring_policy.yaml changed
- whether compiled cards changed
- whether DTO/replay contracts changed
- whether frontend/Gemini/fallback parser paths changed
- whether any runtime-active flags were introduced or changed
```

If the repository uses explicit `runtime_active`, `activation_status`, `visibility`, or similar fields, search the diff and report all status changes.

## Required final report

Return:

```text
- branch name
- main SHA baseline
- authoritative signal repository path found
- schema/contract path found
- validator/loader path found
- Batch A clusters selected
- clusters deferred
- files changed
- whether runtime activation changed
- whether scoring_policy.yaml changed
- whether backend/frontend/runtime files changed
- whether Pass 3 source files changed
- whether Knowledge Bus source packages changed
- validation run and results
- signal repository validator result, if any
- manifest YAML parse result
- recommended next sprint
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

## Acceptance criteria

This sprint is complete only if:

```text
1. The authoritative signal-intelligence repository path is identified, or the sprint stops as Blocked.

2. The schema/contract and loader/validator status are documented.

3. A meaningful Batch A cohort is selected from P1-9 findings.

4. The batch includes multiple material clusters unless blocked by repository authority discovery.

5. Selected clusters are grounded in direct Pass 3 source inspection.

6. Signal intelligence is created or enriched only in the governed repository.

7. No duplicate or ad hoc signal repository is created.

8. Newly promoted/enriched signal intelligence is not made runtime-active.

9. No production scoring policy is changed.

10. No frontend, Gemini, fallback parser, DTO, compiled card or domain assembler file is changed.

11. No Pass 3 source file is changed.

12. No Knowledge Bus source package is changed.

13. Batch A report exists at:
    docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md

14. Batch A manifest exists at:
    docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml

15. Build deliverable register is updated with a short P1-10 entry.

16. YAML validation passes for the manifest.

17. Existing signal repository validator passes if one exists.

18. Runtime non-activation is explicitly confirmed.

19. The final report recommends the next batch or STOP-gated sprint.

20. Final report includes validation output and clean git status.
```
