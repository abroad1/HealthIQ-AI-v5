---
work_id: P1-13
branch: work/P1-13-staged-psi-activation-readiness-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-13 — Staged PSI Activation-Readiness Gate and Integrity Validator

## Objective

Create the activation-readiness gate for staged promoted signal intelligence.

This sprint must audit the staged PSI estate created by P1-10, P1-11 and P1-12, identify anything that would block future production opt-in, and add report-only integrity validation so staged PSI artefacts can be checked before any runtime activation sprint.

This is not a runtime activation sprint.

This is not a one-marker fix sprint.

This sprint must not resolve medical identity questions by guessing.

It must create a governed activation-readiness view across the staged PSI estate and tooling to detect structural integrity issues before runtime use.

## Strategic purpose

P1-10, P1-11 and P1-12 proved the batch-promotion pattern:

```text
Pass 3 investigation specs
→ staged PSI artefacts
→ compile manifests
→ batch manifests
→ build register entries
→ no runtime activation
```

P1-12 exposed the next programme-level need: staged PSI may validate structurally but still contain pre-runtime blockers such as non-canonical biomarker IDs, derived-marker dependencies, system-mapping ambiguity, or medical-review gaps.

This sprint creates the quality-control gate between:

```text
staged medical intelligence exists
```

and:

```text
runtime may use this intelligence
```

Promotion is not activation.

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
git switch -c work/P1-13-staged-psi-activation-readiness-gate
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

## Required prerequisites on main

These files must exist on `main`:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

These staged PSI directories must also exist:

```text
knowledge_bus/generated_pilot/p1_10_batch_a/
knowledge_bus/generated_pilot/p1_11_batch_b/
knowledge_bus/generated_pilot/p1_12_batch_c/
```

If any are missing, stop and report:

```text
P1-13 prerequisite staged PSI evidence is not present on main. P1-13 must not proceed.
```

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Use the `healthiq-knowledge-bus-medical-intelligence` agent rule if available.

If the agent rule is missing, continue under the approved sprint prompt, but record that the specialist rule was not available.

## Scope

This sprint has two linked workstreams.

### Workstream A — activation-readiness audit

Audit all staged PSI artefacts under:

```text
knowledge_bus/generated_pilot/p1_10_batch_a/
knowledge_bus/generated_pilot/p1_11_batch_b/
knowledge_bus/generated_pilot/p1_12_batch_c/
```

For each staged PSI artefact, assess whether it is:

```text
ACTIVATION_READY
BLOCKED_BIOMARKER_IDENTITY
BLOCKED_DERIVED_MARKER_DEPENDENCY
BLOCKED_MEDICAL_REVIEW_REQUIRED
BLOCKED_FRAME_AUTHORITY
BLOCKED_SYSTEM_MAPPING
BLOCKED_SOURCE_SUPPORT
BLOCKED_SCHEMA_OR_VALIDATOR
BLOCKED_MANIFEST_OR_HASH
NOT_ELIGIBLE_FOR_ACTIVATION
```

Use these classifications only in the P1-13 report and activation-readiness manifest.

Do not put unsupported fields into PSI.

### Workstream B — report-only integrity validator

Add a report-only validator or audit script that checks staged PSI integrity before runtime activation.

The validator must not mutate files.

It must not activate anything.

It must not make medical decisions.

It should detect and report issues such as:

```text
- primary_metric.biomarker_id not found in SSOT biomarker keys
- supporting_markers[].biomarker_id not found in SSOT biomarker keys
- non-canonical biomarker aliases needing adjudication
- runtime_active not false in staged compile manifests
- missing or inconsistent compile manifest hashes
- missing source Pass 3 references or spec IDs
- PSI files without matching compile manifests
- compile manifest entries without PSI files
- forbidden PSI root fields
- invalid signal_system or trigger_direction values where schema vocabulary is discoverable
```

If existing validators already cover some checks, do not duplicate them unnecessarily. Reuse or wrap them where sensible.

## Important boundary

The validator may report:

```text
lym is not a canonical SSOT biomarker key
wbc is not a canonical SSOT biomarker key
transferrin_saturation has a derived-marker dependency
```

But it must not decide:

```text
lym = lymphocytes_abs
wbc = leukocytes
transferrin_saturation should be created in SSOT
```

Those are future medical / SSOT authority decisions.

## Permitted changes

Expected product changes may include:

```text
backend/scripts/validate_staged_psi_activation_readiness.py
backend/tests/unit/test_validate_staged_psi_activation_readiness.py
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_gate.md
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

Only create the validator script if no suitable existing script already provides this report-only staged PSI integrity check.

If an existing script can be safely extended without runtime impact, use the smallest safe extension.

## Prohibited changes

Do not modify:

```text
frontend/
Gemini paths
fallback parser paths
backend/core/
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
runtime DTO contracts
domain assemblers
narrative assemblers
compiled runtime cards
production package manifests
Pass 3 source files
investigation-spec source files
Knowledge Bus source package files
staged PSI files from P1-10, P1-11 or P1-12
staged compile manifests from P1-10, P1-11 or P1-12
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

This sprint audits staged PSI artefacts but does not correct their medical identifiers.

If the audit identifies corrections, record them as carry-forwards.

## Activation-readiness dimensions

For each staged PSI artefact, assess:

```text
- PSI schema validity
- source lineage present
- source spec ID present
- primary biomarker ID canonicality
- supporting biomarker ID canonicality
- derived-marker dependency
- signal_system validity
- trigger_direction validity
- runtime_active false
- compile manifest present
- compile manifest hash consistency
- production manifest opt-in absent
- medical-review dependency
- frame-authority dependency
- system/subsystem mapping clarity
- activation-readiness classification
```

## Required deliverable 1 — Sprint report

Create:

```text
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_gate.md
```

Use this structure:

```markdown
# P1-13 — Staged PSI Activation-Readiness Gate and Integrity Validator

## 1. Executive summary
- why this sprint was run
- staged PSI estate audited
- validator/tooling added or reused
- activation-readiness finding
- top blockers
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness
- relationship to P1-10
- relationship to P1-11
- relationship to P1-12
- why this is not a micro-sprint
- why this is not runtime activation

## 3. Staged PSI estate inventory
- staged paths inspected
- number of PSI files found
- number of compile manifests found
- number of clusters/batches represented
- limitations

## 4. Integrity validator implementation
- script added or existing script reused
- checks performed
- files changed
- why validator is report-only
- what the validator intentionally does not decide

## 5. Activation-readiness matrix summary
Summarise:
- activation-ready count
- biomarker-identity blocked count
- derived-marker blocked count
- medical-review blocked count
- frame-authority blocked count
- system-mapping blocked count
- manifest/hash blocked count
- other blocked count

## 6. Detailed blocker findings
For each blocker category:
- affected PSI files
- reason
- whether the blocker is medical, SSOT, derived-marker, frame-authority, schema, or manifest related
- recommended resolution path

## 7. Specific known carry-forwards
Must address:
- `lym` identity decision
- `wbc` identity / SSOT decision
- transferrin saturation / derived-marker dependency
- leukocyte system mapping
- high-risk haematology medical-review cohort
- haemoglobin Pass 3 source-support gap

## 8. Runtime non-activation confirmation
Confirm:
- no PSI artefacts were activated
- no production package manifests changed
- no scoring_policy change
- no SSOT biomarker change
- no backend/core change
- no frontend/Gemini/parser change
- no DTO/domain assembler change
- no compiled card change
- no Pass 3 source change

## 9. Validation
- validator commands run
- test commands run
- YAML parse checks
- git diff checks
- limitations

## 10. Business value delivered
Explain:
- how this enables safe future production opt-in
- how it prevents staged PSI issues from becoming runtime defects
- how it supports parallel medical review and codebase readiness
- why it avoids micro-sprinting

## 11. Carry-forwards
Group carry-forwards into:
- medical-review decisions
- SSOT / biomarker identity decisions
- derived-marker decisions
- frame-authority decisions
- production opt-in readiness
- validator/tooling improvements

## 12. Recommended next sprint
Recommend the next sprint with:
- title
- risk_level
- change_type
- scope
- STOP gates
- rationale
```

## Required deliverable 2 — Activation-readiness manifest

Create:

```text
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml
```

Use this structure:

```yaml
work_id: P1-13
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
staged_estate:
  batches_inspected:
    - p1_10_batch_a
    - p1_11_batch_b
    - p1_12_batch_c
  psi_files_found: <number>
  compile_manifests_found: <number>
  production_opt_ins_found: <number>
summary:
  activation_ready_count: <number>
  blocked_count: <number>
  top_blockers:
    - <blocker>
items:
  - id: <stable_item_id>
    batch: p1_10_batch_a | p1_11_batch_b | p1_12_batch_c
    psi_path: <path>
    compile_manifest_path: <path>
    primary_metric_biomarker_id: <id>
    primary_metric_ssot_status: canonical | non_canonical | missing | not_checked
    supporting_marker_ssot_status: pass | fail | partial | not_applicable | not_checked
    runtime_active: false | true | unknown
    production_manifest_opt_in: false | true | unknown
    compile_manifest_hash_status: pass | fail | not_checked
    activation_readiness: ACTIVATION_READY | BLOCKED_BIOMARKER_IDENTITY | BLOCKED_DERIVED_MARKER_DEPENDENCY | BLOCKED_MEDICAL_REVIEW_REQUIRED | BLOCKED_FRAME_AUTHORITY | BLOCKED_SYSTEM_MAPPING | BLOCKED_SOURCE_SUPPORT | BLOCKED_SCHEMA_OR_VALIDATOR | BLOCKED_MANIFEST_OR_HASH | NOT_ELIGIBLE_FOR_ACTIVATION
    blockers:
      - <blocker>
    recommended_next_action: <short action>
validation:
  manifest_yaml_parse: pass | fail | not_run
  staged_psi_validator: pass | fail | partial | not_run
  unit_tests: pass | fail | partial | not_run
  runtime_activation_check: pass | fail | not_run
```

The manifest is a planning and audit artefact.

It must not be consumed by runtime.

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-13 — Staged PSI activation-readiness gate

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major activation-readiness / validator outcome>

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

Do not duplicate the sprint report.

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Validate the activation-readiness manifest YAML:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-13'; assert 'items' in data; print('P1-13 activation-readiness manifest YAML parsed successfully')"
```

Run the staged PSI activation-readiness validator against all staged batches.

Run targeted tests for any new or modified validator script.

Run existing PSI validator only if the new validator wraps it or if the implementation report says it is required.

Do not run broad unrelated test suites unless necessary.

## Runtime non-activation validation

Confirm:

```text
- no staged PSI files were modified
- no staged compile manifests were modified
- no production package manifests changed
- no backend/core files changed
- no backend/ssot/scoring_policy.yaml changed
- no backend/ssot/biomarkers.yaml changed
- no frontend files changed
- no Gemini or fallback parser files changed
- no runtime DTO or assembler files changed
- no compiled cards changed
- no Pass 3 source files changed
- no runtime activation flags changed
```

## Required final report

Return:

```text
- branch name
- main SHA baseline
- specialist agent availability
- staged PSI batches inspected
- PSI files found
- compile manifests found
- activation-ready count
- blocked count by blocker type
- validator script added/reused
- validator commands and outputs
- tests run and results
- manifest YAML parse result
- files changed
- whether any staged PSI files changed
- whether production package manifests changed
- whether scoring_policy.yaml or biomarkers.yaml changed
- whether backend/core/frontend/runtime files changed
- whether Pass 3 source files changed
- recommended next sprint
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

## Acceptance criteria

This sprint is complete only if:

```text
1. All staged PSI artefacts from P1-10, P1-11 and P1-12 are inventoried.

2. Activation-readiness is classified for every staged PSI artefact.

3. Biomarker ID alignment against SSOT is checked and reported.

4. Derived-marker dependencies are checked and reported.

5. Runtime activation status is checked and reported.

6. Production manifest opt-in status is checked and reported.

7. Compile manifest presence and hash consistency are checked or explicitly reported as not checked with rationale.

8. Report-only validator/tooling is added or an existing equivalent is reused.

9. Targeted tests are added or updated if new validator code is added.

10. No staged PSI files are modified.

11. No production package manifests are modified.

12. No runtime activation occurs.

13. No scoring policy or SSOT biomarker file is changed.

14. No backend/core, frontend, Gemini, parser, DTO, assembler or compiled-card files are changed.

15. No Pass 3 or investigation-spec source file is changed.

16. P1-13 report exists at:
    docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_gate.md

17. P1-13 activation-readiness manifest exists at:
    docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml

18. Build deliverable register is updated with a short P1-13 entry.

19. Manifest YAML validation passes.

20. Final report includes validator output, test output and clean git status.
```
