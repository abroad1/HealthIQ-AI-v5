---
work_id: LC-S21-23-23B
branch: scaffold/lc-s21-23-23b-orchestrator-docs-ssot
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S21/23/23B — Orchestrator Decomposition, Scaffold Documentation and SSOT Metadata

## Classification

This is a HIGH-risk MIXED scaffold sprint.

Reason: this sprint may touch backend orchestration / pipeline structure, scaffold documentation, contributor guidance, SSOT biomarker metadata, validators, tests and Sentinel packs.

This sprint combines:

```text
LC-S21  — Orchestrator Phase Decomposition
LC-S23  — Scaffold-Level Documentation and Developer Onboarding
LC-S23B — SSOT Metadata Completion for Active Signal Biomarkers
````

This is part of the approved HealthIQ AI core scaffold completion programme.

This is not an analytical redesign sprint.
This is not a scoring sprint.
This is not a unit-governance sprint.
This is not a Knowledge Bus content expansion sprint.
This is not a frontend redesign sprint.
This is not a Gemini/LLM sprint.
This is not a launch-readiness sprint.

## Core principle

Preserve behaviour.

The orchestrator decomposition must make the pipeline easier to maintain without changing analytical output.

Documentation must describe the real runtime architecture, not an aspirational architecture.

SSOT metadata completion must support future Knowledge Bus authoring, but it must not become runtime interpretation authority unless explicitly wired in a later sprint.

## Important split rule

This sprint contains both BEHAVIOUR work and CONTENT work.

If the orchestrator decomposition becomes risky, blocked, or requires broader architectural redesign, STOP.

Do not let blocked BEHAVIOUR work automatically block separable documentation / SSOT metadata work.

If Scope A blocks, report and request GPT/human authority to either:

```text
1. continue Scope B/C as a CONTENT-only split package
2. pause all scopes
3. defer orchestrator decomposition
4. create a new Automation Bus work package
```

Cursor may not self-authorise a split.

---

# Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S20_persisted_replay_stale_result_strategy.md
docs/audit-papers/LC-S22_sentinel_phase2_scaffold_notes.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document is missing, STOP.

---

# Required output documentation

Create:

```text
docs/audit-papers/LC-S21_orchestrator_phase_decomposition_notes.md
docs/audit-papers/LC-S23_scaffold_documentation_onboarding_notes.md
docs/audit-papers/LC-S23B_ssot_metadata_completion_notes.md
```

Also create or update the following standing scaffold documentation:

```text
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/how_to_add_signal_package_v1.md
docs/developer-guides/how_to_add_why_coverage_v1.md
docs/developer-guides/how_to_add_lifestyle_modifier_v1.md
docs/developer-guides/how_to_test_intelligence_asset_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/developer-guides/scaffold_defect_vs_missing_content_classification_v1.md
```

If these directories do not exist, create them.

Also create one combined implementation note:

```text
docs/audit-papers/LC-S21_23_23B_orchestrator_docs_ssot_notes.md
```

The combined implementation note must include:

1. preflight results
2. prior scaffold guard results
3. orchestrator current-state map
4. decomposition decision and scope
5. whether split rule was triggered
6. documentation files created/updated
7. SSOT metadata fields completed
8. Tier 1/Tier 2 biomarker status
9. files changed
10. tests added/updated
11. Sentinel updates
12. residual risks
13. final scaffold completion recommendation

---

# Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S21-23-23B`
* branch is `scaffold/lc-s21-23-23b-orchestrator-docs-ssot`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
Test-Path docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

If any are missing, STOP.

---

# Cross-sprint guard preflight

Before implementation, run prior scaffold / launch-core protections.

At minimum run the current equivalents of:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

---

# Phase 1 — Current-state inventory

Before making changes, identify and record current authority paths for:

1. orchestration entry point
2. canonicalisation phase
3. unit normalisation phase
4. scoring phase
5. signal evaluation phase
6. root-cause / WHY phase
7. IDL/display layer publication
8. report/narrative assembly
9. replay/audit manifest generation
10. DTO builder
11. scaffold documentation currently available
12. biomarker SSOT metadata fields
13. active signal biomarker list
14. Sentinel packs covering scaffold behaviours

Known likely files to inspect:

```text
backend/core/pipeline/**/*
backend/core/analytics/**/*
backend/core/dto/**/*
backend/ssot/biomarkers.yaml
backend/ssot/scoring_policy.yaml
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/**/*
docs/planning-papers/**/*
```

STOP if there are multiple competing orchestrator authorities and the correct one cannot be established.

---

# Scope A — LC-S21 Orchestrator Phase Decomposition

## Objective

Make the analytical pipeline maintainable before the Knowledge Bus and signal estate grows further.

This is a behaviour-preserving decomposition.

Do not change analytical output.

## Required current-state mapping

Before editing code, produce a current-state map in:

```text
docs/audit-papers/LC-S21_orchestrator_phase_decomposition_notes.md
```

Include:

* current entry point
* current call order
* current major responsibilities
* current pain points
* candidate phase boundaries
* files that would need to change
* tests that would prove no behavioural drift

## Target phase model

Decompose orchestration into named phase modules where safe:

```text
canonicalisation phase
unit normalisation phase
scoring phase
signal evaluation phase
root-cause phase
IDL phase
report assembly phase
replay/audit phase
```

The final shape may differ if the real codebase suggests better boundaries, but the notes must explain why.

## Required behaviour

* Preserve one high-level orchestration entry point.
* Preserve output shape.
* Preserve call order unless there is a clearly documented no-op refactor reason.
* Preserve all existing DTO fields.
* Preserve all scoring/signal/root-cause results.
* Preserve all replay/persisted compatibility behaviour.
* Add phase-level tests where feasible.
* Do not move clinical logic into frontend or docs.

## STOP conditions for Scope A

STOP if:

* behaviour preservation cannot be proven
* output fingerprints change unexpectedly
* phase boundaries require redesigning analytics rather than moving orchestration structure
* DTO shape changes are required
* scoring or signal semantics change
* unit governance is affected
* root-cause output changes
* persisted replay compatibility changes
* more than a minimal number of core analytics modules require invasive edits

If any STOP condition triggers, invoke the split rule.

## Required tests for Scope A

Add or update deterministic tests proving:

* orchestrator output is unchanged for representative AB baseline fixture
* homocysteine lead remains intact
* LC-S13 lifestyle visible payoff remains intact
* LC-S14 direction-aware scoring remains intact
* LC-S18 WHY registry output remains intact
* LC-S20 persisted replay compatibility remains intact
* new phase functions can be invoked or inspected independently where appropriate
* no output fingerprint drift unless explicitly approved

## Optional proving harness

If orchestrator decomposition touches output assembly or pipeline call order, run:

```powershell
python backend/tools/launch_core_proving_harness.py
```

If only metadata/stamp changes occur, revert or do not commit metadata-only proving artefacts.

If payload fingerprints change, STOP and report before committing unless the change is expected and approved.

---

# Scope B — LC-S23 Scaffold-Level Documentation and Developer Onboarding

## Objective

Make the actual runtime architecture understandable to a future developer or content author without requiring chat history.

Documentation must describe the real implementation, not a desired future architecture.

## Required standing docs

Create or update:

```text
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/how_to_add_signal_package_v1.md
docs/developer-guides/how_to_add_why_coverage_v1.md
docs/developer-guides/how_to_add_lifestyle_modifier_v1.md
docs/developer-guides/how_to_test_intelligence_asset_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/developer-guides/scaffold_defect_vs_missing_content_classification_v1.md
```

## Required content

### Runtime architecture map

Must cover:

* ingestion
* canonicalisation
* units
* lab-derived reference ranges
* scoring
* direction-aware scoring
* signals
* Knowledge Bus package lifecycle
* root-cause / WHY registry
* lifestyle propagation
* DTO contract
* persisted replay
* frontend rendering boundary
* Sentinel / regression guard layers
* Automation Bus workflow

### How to add signal package

Must cover:

* package lifecycle states
* required files
* signal-only vs WHY-enabled distinction
* package estate inventory
* orphan detection
* validators/tests
* Sentinel expectations
* documentation update obligation

### How to add WHY coverage

Must cover:

* root-cause registry
* hypothesis asset requirements
* governed vs fallback WHY
* fingerprint expectations
* duplicate/malformed metadata failure
* how to avoid backend-code coupling where possible
* LC-S18 hybrid registry state

### How to add lifestyle modifier

Must cover:

* questionnaire mapping
* lifestyle modifier computation
* confidence/caveat/explanation limits
* allowed and forbidden claims
* visible user-surface requirements
* Sentinel expectations

### How to test intelligence asset

Must cover:

* unit tests
* regression tests
* fixture tests
* DTO contract checks
* Sentinel pack updates
* proving harness use
* before/after fingerprint expectations

### Guardrails

Must cover:

* no fallback parser
* no global/default ranges where lab ranges exist
* no frontend clinical logic
* no hidden Gemini interpretation
* no silent mutation of historical persisted reports
* no raw signal/governance/internal IDs in user text
* no DTO restructuring without frontend consumer tracing
* no unvalidated orphan package auto-loading
* no hardcoded biomarker exceptions where policy should exist

### Scaffold defect vs missing content classification

Must include the categories from LC-S12B:

* scaffold defect
* missing knowledge asset
* frontend presentation issue
* clinical content backlog
* escaped defect
* governance gap

## Documentation maintenance obligation

Each guide must include a short standing-maintenance note:

```text
Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
```

## Tests / validation for docs

Add lightweight deterministic checks where feasible:

* required docs exist
* docs include required headings
* docs reference real files/paths where applicable
* docs do not mention non-existent authority paths as current runtime

---

# Scope C — LC-S23B SSOT Metadata Completion for Active Signal Biomarkers

## Objective

Complete minimum biomarker metadata needed to support governed future WHY authoring.

This is SSOT metadata work, not runtime interpretation work.

Metadata completion must not alter runtime biomarker interpretation unless already wired by existing code.

## Important non-negotiable policy

Do not substitute global/default reference ranges for lab-derived ranges.

Do not use SSOT metadata to override lab-provided ranges.

Do not add speculative clinical claims.

Do not make metadata runtime-authoritative unless explicitly already used by code.

## Current metadata fields to inspect

In:

```text
backend/ssot/biomarkers.yaml
```

Inspect fields such as:

* key risks when high
* key risks when low
* known modifiers
* clinical caveats
* relevant systems
* common confounders
* interpretation direction notes
* signal/WHY relevance

Use actual field names from the file. Do not invent new field names if equivalent fields already exist.

If required fields do not exist, STOP and propose a minimal schema extension before editing.

## Tier 1 biomarkers — required

Complete metadata for:

```text
LDL
HDL
ApoB
ApoA1
total cholesterol
triglycerides
TSH
Free T4
ferritin
transferrin
CRP
eGFR
creatinine
ALT
AST
GGT
ALP
homocysteine
B12
folate
HbA1c
```

Use canonical biomarker IDs from `biomarkers.yaml`.

If an item is absent from the SSOT, record it as absent and do not invent a new biomarker unless explicitly approved.

## Tier 2 biomarkers — optional / carry-forward

Complete only if safe and time allows:

```text
glucose
insulin
cortisol
creatine kinase
additional sex hormone markers
```

If not completed, record them as carry-forward to KB-WAVE preparation.

## Metadata quality bar

For each Tier 1 biomarker, metadata should support future WHY authoring by capturing:

* high-direction risk/context where clinically relevant
* low-direction risk/context where clinically relevant
* known modifiers/confounders
* relevant systems
* interpretation caveats
* directionality caveat where applicable
* relationship to current or future signal/WHY work

Avoid overclaiming. Use concise, conservative, clinically bounded wording.

## Required validators / tests

Add or update tests/validators proving:

* Tier 1 biomarkers have required metadata fields populated
* metadata values are not empty placeholders
* metadata does not include prohibited placeholder strings
* metadata does not introduce global/default range values
* metadata does not contradict LC-S14 direction-aware scoring policy for representative markers
* active signal biomarkers required for early KB-WAVE work have metadata coverage

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed backend behaviour files for Scope A:

```text
backend/core/pipeline/**/*
backend/core/analytics/**/*
backend/core/dto/**/*
backend/tests/unit/**/*
backend/tests/regression/**/*
```

Potentially allowed SSOT files for Scope C:

```text
backend/ssot/biomarkers.yaml
```

Potentially allowed docs:

```text
docs/architecture/**/*
docs/developer-guides/**/*
docs/audit-papers/LC-S21_orchestrator_phase_decomposition_notes.md
docs/audit-papers/LC-S23_scaffold_documentation_onboarding_notes.md
docs/audit-papers/LC-S23B_ssot_metadata_completion_notes.md
docs/audit-papers/LC-S21_23_23B_orchestrator_docs_ssot_notes.md
```

Potentially allowed Sentinel:

```text
sentinel/packs/**/*
sentinel/**/*
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
knowledge_bus/**/*
frontend/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify scoring, unit governance, Knowledge Bus content, frontend rendering, or Automation Bus scripts in this sprint.

If those appear necessary, STOP.

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add or update defect classes:

```text
orchestrator_phase_output_changed
pipeline_phase_regression
scaffold_documentation_missing_for_new_pattern
active_signal_biomarker_missing_ssot_metadata
ssot_metadata_unreviewed_for_kb_wave_target
```

Each must point to an active deterministic regression test or validator.

Do not add placeholder Sentinel entries.

If Scope A is split/deferred, adjust Sentinel obligations accordingly and document.

---

# Required validation commands

Run prior scaffold guards and new tests.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Run the new LC-S21/23/23B tests explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py -q
```

If orchestrator output could change, run the launch-core proving harness:

```powershell
python backend/tools/launch_core_proving_harness.py
```

If only metadata/stamp changes occur, revert or do not commit metadata-only proving artefacts.

If payload fingerprints change, STOP and report before committing unless the change is expected and approved.

If any required existing test file name differs, find and run the current equivalent, then record the substitution.

---

# Acceptance criteria

This sprint is complete only if:

* Scope A either completes behaviour-preserving orchestration decomposition or cleanly STOPs/splits
* orchestrator output is proven unchanged if Scope A changes runtime code
* scaffold documentation exists and describes actual runtime architecture
* contributor guides exist and are usable without chat history
* Tier 1 SSOT metadata is complete or explicit approved exceptions are recorded
* metadata does not change runtime interpretation unless already wired
* Sentinel defect classes are active and deterministic
* prior scaffold/launch-core guards still pass
* no scoring/unit/frontend/Knowledge Bus content work is smuggled into this sprint
* documentation includes standing maintenance obligation
* residual risks and KB-WAVE transition readiness are documented

---

# Closure requirements

When complete:

1. Run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

2. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries

3. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.

4. Run finish:

```powershell
python backend/scripts/run_work_package.py finish
```

5. Report whether finish completed or failed.

6. Do not merge.

7. Do not create `automation_bus/latest_audit_summary.md`.

8. Do not claim final approval.

## Cursor completion statement

Cursor implements and reports only.

Cursor may not self-certify clinical correctness, architecture correctness, scaffold completion, merge readiness, launch readiness, or permission to begin KB-WAVE work.

```
```
