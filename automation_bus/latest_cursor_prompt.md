---
work_id: ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate
branch: work/ARCH-COMPLETION-3-full-traceability-manifest-and-launch-estate-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# ARCH-COMPLETION-3 — Full Traceability Manifest and Launch Estate Gate

## Purpose

Complete the final day-one architecture gate for HealthIQ AI.

This sprint must produce a full runtime traceability manifest and a launch-estate gate that proves the day-one analytical architecture is governed, traceable, fail-closed and free from unresolved legacy runtime authority paths.

This sprint should answer one question:

```text
Is the day-one intelligence architecture now complete enough to be formally closed?
```

If yes, the sprint must produce evidence and close the relevant carry-forward items.

If no, the sprint must identify precise residual blockers with named files, named authority gaps and named remediation conditions.

This is not a frontend polish sprint.

This is not a new signal activation sprint.

This is not a new medical research sprint.

This is the final architecture-completion gate.

---

## Strategic context

The following work is now complete and merged:

```text
- ADR-RT-001 accepted the research-to-runtime day-one architecture.
- ARCH-COMPLETION-1 corrected orchestrator phase ordering.
- AnalysisContext now precedes signal evaluation.
- Runtime context is derived from AnalysisContext / governed post-context objects.
- BATCH2-MINIMUM-COVERAGE-1 clarified the unresolved Batch 2 estate.
- BATCH2-FULL-COVERAGE-BUILD-1 added reusable runtime context primitives.
- BATCH2-FULL-COVERAGE-ACTIVATION-1 activated the research-supported thyroid/androgen signals with deterministic gates.
- ARCH-COMPLETION-2 added compiled output authority, root-cause authority, card authority and additive ReportV1 provenance.
```

`ARCH-COMPLETION-2` carried forward two non-blocking items:

```text
1. The full traceability manifest must explicitly classify narrative_report_compiler_v1.py runtime YAML reads as governed compiled assets.
2. Provenance-specific regression tests must be added for FAI high, free testosterone high and free testosterone low.
```

This sprint must resolve those carry-forwards and perform the final launch-estate architecture gate.

---

## Governance classification

This sprint is classified as:

```yaml
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text
- this sprint may alter validators, launch gates and runtime traceability enforcement
- it touches the final architecture closure decision
- it may quarantine or block any remaining ungoverned analytical output
- it may add provenance tests and authority-manifest requirements
- it may update day-one completion status
```

Required route:

```text
Cursor implementation
Claude hardening / audit
GPT architectural review
Human approval before merge
```

Do not merge without explicit human approval.

---

## Required branch

Work only on:

```text
work/ARCH-COMPLETION-3-full-traceability-manifest-and-launch-estate-gate
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- activate or deactivate signal packages
- change clinical thresholds
- change biomarker reference range policy
- change SSOT biomarker definitions
- change scoring algorithms
- change frontend rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into deterministic runtime output
- invent medical claims not traceable to governed runtime authority
- weaken runtime context gates
- weaken package activation gates
- remove fail-closed behaviour
- downgrade governance failures to warnings unless explicitly justified and approved
```

This sprint may:

```text
- create or update the full traceability manifest
- create or update the launch-estate gate model
- add or update architecture validators
- add provenance-specific regression tests
- classify remaining output/runtime authority sources
- quarantine ungoverned runtime paths
- update carry-forward registers
- formally mark day-one architecture complete if evidence supports it
```

---

## Core design rule

Every runtime analytical path must be classifiable as one of:

```text
GOVERNED_RUNTIME_AUTHORITY
GOVERNED_COMPILED_ASSET
GOVERNED_MAPPING_AUTHORITY
GOVERNED_RENDER_ONLY
GOVERNED_DEBUG_ONLY
LEGACY_QUARANTINED
INACTIVE_NOT_RUNTIME_CONSUMED
BLOCKED_UNGOVERNED
UNKNOWN_BLOCKER
```

No runtime analytical path may remain `UNKNOWN_BLOCKER` or `BLOCKED_UNGOVERNED` if day-one architecture is to be marked complete.

No user-facing analytical output may be emitted from an ungoverned source.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
docs/audit-papers/ARCH-COMPLETION-2_compiled_card_and_root_cause_authority_completion.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/sprints/launch_core_carry_forward_register.md

docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md

knowledge_bus/governance/compiled_output_authority_model_v1.yaml
knowledge_bus/governance/root_cause_authority_register_v1.yaml
knowledge_bus/governance/card_authority_register_v1.yaml
knowledge_bus/governance/reusable_runtime_context_primitive_model_v1.yaml
knowledge_bus/governance/context_questionnaire_contract_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

If exact paths differ, locate the equivalent repo-persisted files and document the actual paths used.

Inspect all relevant runtime and output authority files, including but not limited to:

```text
backend/core/pipeline/orchestrator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/contracts/report_v1.py
backend/core/contracts/output_authority_provenance_v1.py
backend/core/knowledge/compiled_output_authority_v1.py
```

Also explicitly inspect and classify:

```text
backend/core/analytics/narrative_report_compiler_v1.py
```

Do not assume the file list is complete. Discover all runtime reads and analytical output paths.

---

## Authority preflight

Before editing, verify and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text
1. Current branch matches this work package branch.
2. Working tree is clean.
3. ARCH-COMPLETION-1 is merged.
4. BATCH2-FULL-COVERAGE-ACTIVATION-1 is merged.
5. ARCH-COMPLETION-2 is merged.
6. ReportV1 contains additive output_authority_provenance_v1.
7. compiled_output_authority_model_v1.yaml exists.
8. root_cause_authority_register_v1.yaml exists.
9. card_authority_register_v1.yaml exists.
10. why_engine_fallback_v1 is quarantined from clinician-report output.
11. No frontend rendering change is required.
12. Repository secret-file gate remains remediated.
```

STOP if the baseline is unclear.

---

# Phase 1 — Full runtime authority discovery

Perform a full discovery of runtime analytical authority sources.

Inspect and document all runtime paths that:

```text
- read YAML/JSON/Markdown/domain authority files
- assemble AnalysisContext
- build runtime context
- evaluate signals
- build root-cause findings
- build cards
- build insight or narrative output
- compile reports
- attach provenance
- assemble DTOs or API response payloads
```

For every runtime read or generated output path, record:

```text
- file path
- function/class
- runtime input
- runtime output
- source artefact read, if any
- whether source artefact is governed
- whether source artefact is raw research
- whether source artefact is compiled/promoted authority
- whether path emits user-facing analytical output
- whether path emits debug-only output
- whether frontend consumes the output
- authority classification
- evidence
```

Allowed classifications:

```text
GOVERNED_RUNTIME_AUTHORITY
GOVERNED_COMPILED_ASSET
GOVERNED_MAPPING_AUTHORITY
GOVERNED_RENDER_ONLY
GOVERNED_DEBUG_ONLY
LEGACY_QUARANTINED
INACTIVE_NOT_RUNTIME_CONSUMED
BLOCKED_UNGOVERNED
UNKNOWN_BLOCKER
```

Required explicit classification:

```text
backend/core/analytics/narrative_report_compiler_v1.py
```

The narrative compiler’s runtime YAML reads must be classified accurately. If they are governed compiled assets, document them as:

```text
GOVERNED_COMPILED_ASSET
```

If any runtime path reads raw Pass 3 research or investigation specs, STOP.

---

# Phase 2 — Create full traceability manifest

Create or update:

```text
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
```

This manifest must provide a single authoritative map of the day-one runtime estate.

It must include at least:

```text
- runtime pipeline phases
- key runtime modules
- runtime authority files
- compiled authority assets
- signal package authority
- runtime context authority
- card authority
- root-cause authority
- compiled output authority
- report compiler authority
- narrative compiler authority
- frontend/render-only boundary
- inactive/quarantined legacy paths
- forbidden runtime inputs
- launch-blocking classifications
```

For each entry, include:

```text
- id
- path
- role
- authority_classification
- runtime_consumed: true / false
- user_facing: true / false
- source_authority
- allowed_runtime_inputs
- forbidden_runtime_inputs
- provenance_required: true / false
- governed_by
- launch_gate_status
- evidence
```

Allowed `launch_gate_status` values:

```text
PASS
PASS_WITH_CARRY_FORWARD
BLOCKED
NOT_RUNTIME_CONSUMED
QUARANTINED
DEBUG_ONLY
```

Do not duplicate authority unnecessarily. The manifest should reference existing governance artefacts where they already exist.

---

# Phase 3 — Create launch estate gate model

Create or update:

```text
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
```

This gate must define the final closure criteria for day-one architecture.

It must include:

```text
- gate name
- gate version
- launch scope
- required architecture conditions
- required runtime authority conditions
- required output authority conditions
- required context safety conditions
- required signal activation conditions
- required inactive/quarantined path conditions
- required frontend/render-only conditions
- required security/repo-hygiene conditions
- allowed carry-forwards
- disallowed carry-forwards
- final verdict values
```

Allowed final verdict values:

```text
DAY_ONE_ARCHITECTURE_COMPLETE
DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD
DAY_ONE_ARCHITECTURE_NOT_COMPLETE
```

The gate must make clear that day-one architecture cannot be complete if:

```text
- any user-facing analytical runtime path is ungoverned
- any raw Pass 3 file is consumed at runtime
- any investigation spec is consumed at runtime
- any frontend medical inference is required
- any active signal lacks package authority
- any compiled output lacks authority/provenance where required
- any root-cause output is emitted from ungoverned fallback
- any diagnosis/treatment/supplement wording is introduced
- any SSOT/reference-range policy is bypassed
```

Allowed non-blocking carry-forwards may include:

```text
- additional optional provenance regression coverage
- future modifier-only signal architecture
- DHEA/DHEA-S identity remediation if the relevant packages remain inactive
- non-launch-blocking UX/frontend polish
- broader future biomarker expansion
```

---

# Phase 4 — Implement or update launch gate validator

Create or update a deterministic validator.

Preferred file:

```text
backend/scripts/validate_day_one_launch_estate_gate.py
```

The validator must check:

```text
1. day_one_full_traceability_manifest_v1.yaml exists.
2. day_one_launch_estate_gate_v1.yaml exists.
3. No manifest entry is UNKNOWN_BLOCKER.
4. No user-facing runtime analytical path is BLOCKED_UNGOVERNED.
5. Raw Pass 3 runtime reads are forbidden.
6. Investigation-spec runtime reads are forbidden.
7. compiled_output_authority_model_v1.yaml exists.
8. root_cause_authority_register_v1.yaml exists.
9. card_authority_register_v1.yaml exists.
10. ReportV1 includes output_authority_provenance_v1.
11. why_engine_fallback_v1 is quarantined or blocked from governed clinician output.
12. narrative_report_compiler_v1.py is classified in the manifest.
13. active Batch 2 signals are represented in provenance tests or explicitly carried forward.
14. inactive DHEA/DHEA-S and modifier-only signals remain inactive.
15. frontend paths are classified render-only or out of scope.
16. launch estate final verdict is one of the allowed values.
```

If the validator already exists, extend it rather than creating a duplicate.

The validator must fail hard on launch-blocking conditions.

Do not create a validator that always passes.

---

# Phase 5 — Close ARCH-COMPLETION-2 carry-forwards

Resolve the two carry-forward items from `ARCH-COMPLETION-2`.

## Carry-forward 1 — narrative compiler classification

Explicitly classify:

```text
backend/core/analytics/narrative_report_compiler_v1.py
```

Also classify any runtime YAML/authority assets it reads.

Expected classification, if verified:

```text
GOVERNED_COMPILED_ASSET
```

Do not quarantine this path if it is reading governed compiled assets and producing authorised narrative output.

If it reads raw research or ungoverned assets, STOP.

## Carry-forward 2 — Batch 2 provenance-specific tests

Add provenance-specific regression tests for:

```text
- FAI high activated case
- FAI high suppressed case
- free testosterone high activated case
- free testosterone high suppressed case
- free testosterone low activated case
- free testosterone low suppressed case
```

These tests must verify output authority provenance, not merely signal activation/suppression.

They should prove:

```text
- activated signal produces governed provenance element
- suppressed signal does not produce governed analytical output
- source_signal_ids include the expected signal ID
- authority_status is appropriate
- inactive or suppressed states do not produce misleading output
```

Do not remove existing FT3 low or DHEA inactive provenance tests.

---

# Phase 6 — Final raw-research runtime read scan

Add or update tests/scripts to prove the day-one runtime does not consume:

```text
- raw Pass 3 files
- investigation specs
- multi-LLM research specs
- unpromoted research assets
```

The scan must cover at least:

```text
backend/core/**
backend/routes/**
backend/scripts used by runtime gates where relevant
```

The scan must not falsely fail on:

```text
- build-time promotion scripts
- governance documentation references
- audit papers
- tests that intentionally mention forbidden paths
```

If existing tests already cover part of this, extend them rather than duplicating.

---

# Phase 7 — Launch estate verdict

Using the manifest and validator evidence, set a launch estate verdict in:

```text
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
```

Allowed verdicts:

```text
DAY_ONE_ARCHITECTURE_COMPLETE
DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD
DAY_ONE_ARCHITECTURE_NOT_COMPLETE
```

Choose the verdict honestly.

Use:

```text
DAY_ONE_ARCHITECTURE_COMPLETE
```

only if there are no architecture carry-forwards.

Use:

```text
DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD
```

only if remaining items are explicitly non-blocking and do not affect day-one runtime safety.

Use:

```text
DAY_ONE_ARCHITECTURE_NOT_COMPLETE
```

if any launch-blocking governance, traceability, runtime authority or safety defect remains.

Do not inflate the verdict.

---

# Phase 8 — Tests

Add or update tests proving:

```text
1. full traceability manifest exists and contains required domains.
2. narrative_report_compiler_v1.py is classified.
3. no manifest entry has UNKNOWN_BLOCKER.
4. no user-facing analytical runtime path is BLOCKED_UNGOVERNED.
5. day-one launch estate gate exists and has an allowed verdict.
6. launch estate validator passes.
7. raw Pass 3 runtime reads are absent.
8. investigation-spec runtime reads are absent.
9. why_engine_fallback_v1 remains quarantined or blocked from clinician output.
10. ReportV1 still includes output_authority_provenance_v1.
11. FT3 low provenance test still passes.
12. FAI high activated provenance test passes.
13. FAI high suppressed provenance test passes.
14. free testosterone high activated provenance test passes.
15. free testosterone high suppressed provenance test passes.
16. free testosterone low activated provenance test passes.
17. free testosterone low suppressed provenance test passes.
18. inactive DHEA does not produce governed analytical output.
19. frontend remains render-only.
20. no signal package activation/deactivation occurred.
```

Do not rely only on YAML structure tests.

There must be runtime/provenance tests.

---

# Phase 9 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

If any validator does not exist, create it if in scope, or report why it is absent.

## Context and signal regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py -q
python -m pytest backend/tests/regression/test_output_authority_provenance.py -q
```

## Governance tests

Run all relevant governance tests for:

```text
- full traceability manifest
- launch estate gate
- compiled output authority
- root-cause authority
- card authority
- Batch 2 activation registers
- runtime context registers
```

## Unit tests

Run all relevant unit tests for:

```text
- report compiler
- provenance builder
- compiled output authority loader
```

## Secret-file guardrail

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

---

# Phase 10 — Required audit paper

Create:

```text
docs/audit-papers/ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- carry-forward items inherited from ARCH-COMPLETION-2
- carry-forward resolution evidence
- full runtime authority discovery summary
- full traceability manifest summary
- launch estate gate summary
- launch estate final verdict
- validator implementation details
- raw-research runtime read scan result
- narrative_report_compiler_v1.py classification
- Batch 2 provenance test coverage result
- inactive/quarantined path status
- confirmation no signal packages activated or deactivated
- confirmation no SSOT changed unless explicitly justified
- confirmation no scoring changed
- confirmation no frontend changed
- confirmation no report compiler output contract broken
- confirmation no raw research runtime reads introduced
- confirmation no diagnosis wording introduced
- confirmation no treatment/supplement recommendation introduced
- full validator output
- full test output
- rollback path
- carry-forward impact
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 11 — Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only where justified.

Expected handling:

```text
- close ARCH-COMPLETION-2 narrative compiler traceability carry-forward if resolved
- close ARCH-COMPLETION-2 Batch 2 provenance-test carry-forward if resolved
- close day-one architecture carry-forward only if launch estate verdict supports completion
- add precise non-blocking carry-forwards only where appropriate
- keep DHEA/DHEA-S future remediation open if packages remain inactive
```

Do not create vague residuals.

Do not mark day-one architecture complete unless evidence supports it.

---

## Expected changed files

Expected changed files may include:

```text
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
backend/scripts/validate_day_one_launch_estate_gate.py
backend/tests/regression/test_output_authority_provenance.py
backend/tests/governance/test_arch_completion_3_traceability_manifest.py
backend/tests/governance/test_day_one_launch_estate_gate.py
backend/tests/unit/*
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.md
automation_bus/latest_cursor_status.json
```

Possible but must be justified:

```text
backend/core/knowledge/compiled_output_authority_v1.py
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/contracts/report_v1.py
```

Only touch these if the launch estate gate or traceability manifest proves a genuine implementation gap.

No frontend files are expected to change.

No SSOT files are expected to change.

No signal package files are expected to change.

---

## Forbidden changes

Do not change:

```text
frontend/**
backend/ssot/**
```

Do not activate or deactivate packages under:

```text
knowledge_bus/packages/**
```

unless the change is strictly non-behavioural documentation/provenance metadata and is explicitly justified.

Do not introduce:

```text
- fallback parsers
- dummy parsers
- raw research runtime reads
- frontend clinical inference
- LLM clinical reasoning
- diagnosis wording
- treatment recommendations
- supplement recommendations
```

---

## STOP conditions

STOP and report if:

```text
1. full runtime authority discovery cannot be completed.
2. narrative_report_compiler_v1.py reads raw research or ungoverned assets.
3. full traceability manifest cannot classify all user-facing analytical runtime paths.
4. any manifest entry remains UNKNOWN_BLOCKER.
5. any user-facing analytical runtime path remains BLOCKED_UNGOVERNED.
6. launch estate gate cannot be represented deterministically.
7. launch estate validator would need to be superficial or always-pass.
8. raw Pass 3 runtime reads are found.
9. investigation-spec runtime reads are found.
10. provenance tests cannot be added for FAI high, free testosterone high or free testosterone low.
11. changes would require frontend rendering edits.
12. changes would require SSOT edits.
13. changes would require signal package activation/deactivation.
14. changes would require clinical threshold changes.
15. diagnosis wording would be emitted.
16. treatment/supplement recommendation would be emitted.
17. validators fail.
18. tests fail.
19. secret-file guardrail fails.
20. rollback path cannot be defined.
```

If a STOP condition is triggered, do not perform ad hoc remediation beyond scope.

---

## Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Commit message:

```text
feat(governance): add day-one traceability manifest and launch estate gate
```

If no runtime/code change occurs and the sprint only creates governance/test artefacts, use:

```text
docs(governance): complete day-one launch estate traceability gate
```

After commit, report:

```powershell
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Do not merge.

Return evidence for Claude audit and GPT architectural review.

---

## Success criteria

This sprint succeeds only if:

```text
- full runtime authority discovery is complete
- day_one_full_traceability_manifest_v1.yaml exists
- day_one_launch_estate_gate_v1.yaml exists
- launch estate validator exists and passes
- narrative_report_compiler_v1.py is explicitly classified
- FAI high provenance tests pass
- free testosterone high provenance tests pass
- free testosterone low provenance tests pass
- raw Pass 3 runtime reads are absent
- investigation-spec runtime reads are absent
- every user-facing analytical runtime path is governed or quarantined
- no UNKNOWN_BLOCKER entries remain
- no BLOCKED_UNGOVERNED user-facing paths remain
- no signal packages are activated or deactivated
- no SSOT changes occur
- no frontend changes occur
- no scoring changes occur
- no diagnosis wording is introduced
- no treatment/supplement recommendation is introduced
- validators pass
- tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text
Claude audit
GPT architectural review
Human approval
Merge

If launch verdict is DAY_ONE_ARCHITECTURE_COMPLETE or DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD:
  formally close day-one architecture rework and move to product / beta readiness estate.

If launch verdict is DAY_ONE_ARCHITECTURE_NOT_COMPLETE:
  remediate the named blockers before product readiness work.
```
