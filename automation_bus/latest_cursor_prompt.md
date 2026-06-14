---
work_id: ARCH-COMPLETION-2_compiled_card_and_root_cause_authority_completion
branch: work/ARCH-COMPLETION-2-compiled-card-and-root-cause-authority-completion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# ARCH-COMPLETION-2 — Compiled Card and Root-Cause Authority Completion

## Purpose

Complete the remaining day-one architecture authority chain between:

```text
activated signals
runtime context
root-cause logic
card generation
compiled analytical output
```

The goal is to ensure that every user-facing analytical statement produced by the day-one runtime estate is traceable to governed runtime authority, and that no compiled card, root-cause explanation or output fragment is being generated from legacy, unclear, raw-research, ungoverned or duplicate paths.

This sprint is not a frontend polish sprint.

This sprint is not a signal activation sprint.

This sprint is the authority-completion sprint for the analytical output layer.

---

## Strategic context

The following foundations are now complete or merged:

```text
- ADR-RT-001 accepted the research-to-runtime day-one architecture.
- ARCH-COMPLETION-1 corrected orchestrator phase order.
- AnalysisContext now precedes signal evaluation.
- Runtime context is derived from AnalysisContext / governed post-context objects.
- BATCH2-MINIMUM-COVERAGE-1 removed ambiguity from remaining Batch 2 classification.
- BATCH2-FULL-COVERAGE-BUILD-1 added reusable runtime context primitives.
- BATCH2-FULL-COVERAGE-ACTIVATION-1 activated the research-supported thyroid/androgen signals with deterministic gates.
```

The remaining risk is now in the output-authority chain.

We need to confirm and, where required, repair how signals become:

```text
- insight cards
- root-cause explanations
- grouped analytical narratives
- compiled output payloads
- downstream renderable DTOs
```

The product must not contain apparently polished analytical output that is actually coming from legacy root-cause/card/hypothesis paths with unclear authority.

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
- user-facing analytical output authority may change
- card/root-cause pathways may be refactored or constrained
- compiled output may change
- legacy or duplicate analytical paths may be disabled
- traceability requirements may be introduced or enforced
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
work/ARCH-COMPLETION-2-compiled-card-and-root-cause-authority-completion
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- activate or deactivate signal packages
- change clinical thresholds
- change reference range policy
- change SSOT biomarker definitions
- change scoring algorithms
- change frontend rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into deterministic runtime output
- invent medical claims not traceable to governed runtime authority
- weaken context gates
- weaken package activation gates
- remove fail-closed behaviour
```

This sprint may:

```text
- inspect and repair root-cause authority wiring
- inspect and repair card authority wiring
- inspect and repair compiled output traceability
- classify legacy output paths
- disable or quarantine ungoverned legacy output paths
- add provenance and authority metadata to compiled outputs
- add tests proving output statements are governed and traceable
```

---

## Core design rule

Every analytical output element must answer:

```text
What governed runtime object authorised this statement?
```

Acceptable authority sources include:

```text
- activated signal package
- governed signal output
- governed runtime context snapshot
- governed root-cause mapping
- governed card authority mapping
- governed compiler authority manifest
```

Unacceptable authority sources include:

```text
- raw Pass 3 research file at runtime
- investigation spec at runtime
- legacy hypothesis path without authority mapping
- legacy root-cause path without authority mapping
- hardcoded analytical statement in compiler code
- frontend-derived medical inference
- LLM-generated runtime explanation without deterministic authority
```

If an output element cannot be traced, it must not be emitted as day-one governed analytical output.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
docs/audit-papers/BATCH2-FULL-COVERAGE-BUILD-1_reusable_context_layer_research_authority_and_activation_readiness.md
docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/sprints/launch_core_carry_forward_register.md

docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
```

If the exact paths differ, locate the equivalent repo-persisted files and document the actual paths used.

Inspect all runtime/output files that participate in:

```text
- signal output to card transformation
- root-cause generation
- card generation
- compiled output generation
- DTO/output payload generation
- result payload assembly
- any “insight”, “card”, “root_cause”, “hypothesis”, “compiled”, “summary”, “narrative” or “explanation” module
```

Do not assume the file list. Discover it.

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
5. The four research-supported Batch 2 endocrine signals are active.
6. DHEA high/low, FAI low and free testosterone percentage high/low remain inactive as primary signals.
7. AnalysisContext still precedes signal evaluation.
8. Runtime context is still derived from AnalysisContext or governed post-context object.
9. No frontend rendering change is required for this sprint.
10. Repository secret-file gate remains remediated.
```

STOP if the baseline is unclear.

---

# Phase 1 — Discover the output-authority estate

Before making changes, produce a read-only map of the analytical output estate.

Find and document all code paths that generate or transform:

```text
- cards
- card titles
- card summaries
- card bodies
- root-cause explanations
- grouped findings
- insight narratives
- hypothesis narratives
- compiled summaries
- output DTOs
- payload fragments sent to frontend or report generation
```

For each path, record:

```text
- file path
- function/class name
- input object(s)
- output object(s)
- whether it consumes activated signals
- whether it consumes runtime context
- whether it consumes root-cause mappings
- whether it consumes package metadata
- whether it consumes legacy hypothesis/card/root-cause files
- whether it contains hardcoded medical/analytical wording
- whether frontend depends on its output shape
- authority status
```

Allowed authority statuses:

```text
GOVERNED_RUNTIME_AUTHORITY
GOVERNED_MAPPING_AUTHORITY
LEGACY_CLASSIFIED_ALLOWED_TEMPORARY
LEGACY_UNGOVERNED_BLOCKER
DUPLICATE_AUTHORITY_BLOCKER
OUTPUT_SHAPE_ONLY_NO_MEDICAL_AUTHORITY
UNKNOWN_REQUIRES_REVIEW
```

STOP if the output-authority estate cannot be discovered.

---

# Phase 2 — Define compiled output authority model

Create or update a governed authority model for compiled analytical output.

Preferred artefact:

```text
knowledge_bus/governance/compiled_output_authority_model_v1.yaml
```

If an equivalent artefact already exists, update it rather than duplicating authority.

The model must define:

```text
- allowed output element types
- required authority source for each output element type
- required provenance fields
- allowed compiler inputs
- forbidden compiler inputs
- legacy-path handling rules
- frontend/render-only boundary
- root-cause authority rules
- card authority rules
- fail-closed behaviour for untraceable output
```

At minimum, cover:

```text
signal_card
root_cause_card
system_summary
cluster_summary
hypothesis_summary
biomarker_explanation
contextual_modifier_explanation
missing_context_notice
inactive_signal_notice
```

For each type, define:

```text
- may_emit: true / false
- required_authority
- required_trace_fields
- allowed_runtime_inputs
- forbidden_runtime_inputs
- fail_closed_if_missing_authority
```

The model must explicitly forbid raw research reads at runtime.

---

# Phase 3 — Root-cause authority audit and repair

Inspect all root-cause generation logic.

For each root-cause output path, determine whether it is based on:

```text
- activated signal outputs
- governed package metadata
- governed context mappings
- governed root-cause mapping file
- legacy hypothesis code
- static hardcoded rule
- raw/untraceable narrative
```

Create or update a root-cause authority register.

Preferred artefact:

```text
knowledge_bus/governance/root_cause_authority_register_v1.yaml
```

For each root-cause type, record:

```text
- root_cause_id
- display label
- authority source
- allowed source signals
- required companion evidence
- required context evidence
- allowed wording strength
- prohibited wording
- runtime consumed? true / false
- activation status
- fail-closed condition
```

If no root-cause type can be safely governed in this sprint, do not invent root-cause outputs. Instead, explicitly classify legacy root-cause output as blocked.

Allowed outcomes:

```text
ROOT_CAUSE_GOVERNED_ACTIVE
ROOT_CAUSE_GOVERNED_INACTIVE
ROOT_CAUSE_LEGACY_QUARANTINED
ROOT_CAUSE_UNTRACEABLE_BLOCKED
ROOT_CAUSE_REQUIRES_FUTURE_MAPPING
```

Do not leave unclassified root-cause output paths.

---

# Phase 4 — Card authority audit and repair

Inspect all card generation logic.

For each card type, determine whether it is authorised by:

```text
- activated signal
- signal family
- biomarker result
- package metadata
- root-cause mapping
- runtime context modifier
- legacy hardcoded logic
- frontend inference
```

Create or update a card authority register.

Preferred artefact:

```text
knowledge_bus/governance/card_authority_register_v1.yaml
```

For each card type, record:

```text
- card_id
- card_type
- display purpose
- authorised input
- required trace fields
- allowed wording strength
- prohibited wording
- whether card may include root-cause explanation
- whether card may include context explanation
- whether card may include missing-context notice
- runtime consumed? true / false
- activation status
- fail-closed condition
```

Allowed outcomes:

```text
CARD_GOVERNED_ACTIVE
CARD_GOVERNED_INACTIVE
CARD_RENDER_ONLY
CARD_LEGACY_QUARANTINED
CARD_UNTRACEABLE_BLOCKED
CARD_REQUIRES_FUTURE_MAPPING
```

Any card that contains analytical/medical wording must have an authority source.

Pure display/layout cards may be classified as `CARD_RENDER_ONLY`.

---

# Phase 5 — Implement compiled output provenance

Implement or extend provenance metadata on compiled analytical outputs.

Each emitted analytical output element should include, where applicable:

```text
- output_element_id
- output_element_type
- source_signal_ids
- source_package_ids
- source_biomarker_ids
- source_context_keys
- source_root_cause_ids
- authority_register_ref
- authority_status
- wording_strength
- generated_by
```

The implementation must not require frontend changes unless the frontend already tolerates extra fields.

If adding extra fields would break frontend consumers, STOP and report.

Preferred behaviour:

```text
- additive metadata fields only
- no breaking DTO changes
- frontend remains render-only
```

If a compiled output cannot be traced to authority, it must be suppressed, quarantined, or marked as non-governed and excluded from day-one governed output.

---

# Phase 6 — Quarantine or block legacy ungoverned paths

Any output path classified as:

```text
LEGACY_UNGOVERNED_BLOCKER
DUPLICATE_AUTHORITY_BLOCKER
UNKNOWN_REQUIRES_REVIEW
```

must be handled.

Allowed remediation:

```text
- quarantine from day-one output
- disable emission behind explicit inactive flag
- restrict to non-user-facing debug output
- require authority mapping before emission
- convert to render-only if no analytical claim remains
```

Do not delete large legacy systems unless clearly safe and covered by tests.

Do not leave ungoverned legacy analytical output active.

---

# Phase 7 — Integration with existing active signal estate

Validate compiled output against currently active signal estate, including:

```text
- previously active thyroid high / FT4 high / FT4 low signals
- creatine kinase packages
- eosinophil packages
- FT3 low
- FAI high
- free testosterone high
- free testosterone low
```

Confirm:

```text
- active signals can produce governed output where expected
- inactive signals do not produce output
- missing context produces missing-context notices only if governed
- suppressed signals do not produce analytical conclusions
- DHEA unresolved identity does not produce adrenal androgen output
- modifier-only future patterns do not produce primary signal cards
```

---

# Phase 8 — Tests

Add or update tests proving:

```text
1. every emitted analytical card has authority metadata
2. every emitted root-cause explanation has authority metadata
3. compiled output does not consume raw Pass 3 or investigation-spec files at runtime
4. frontend DTO shape is backward-compatible or explicitly tolerated
5. untraceable legacy card paths are quarantined or blocked
6. untraceable legacy root-cause paths are quarantined or blocked
7. inactive packages do not produce compiled cards
8. suppressed context-dependent signals do not produce analytical conclusions
9. missing-context notices are governed if emitted
10. active Batch 2 signals produce traceable output
11. DHEA unresolved identity does not produce adrenal androgen output
12. frontend remains render-only
13. no diagnosis wording is introduced
14. no treatment or supplement recommendation is introduced
```

Regression tests must cover at least:

```text
- FT3 low activated case
- FT3 low suppressed case
- FAI high activated case
- FAI high suppressed case
- free testosterone high activated case
- free testosterone high suppressed case
- free testosterone low activated case
- free testosterone low suppressed case
- inactive DHEA package
```

Do not rely only on governance-file tests.

There must be runtime/output tests.

---

# Phase 9 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Context and signal regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py -q
```

## Output authority tests

Run all new and existing tests covering:

```text
- compiled output
- card generation
- root-cause generation
- signal-to-card transformation
- output DTOs
```

## Governance tests

Run all relevant governance tests for:

```text
- compiled output authority model
- root-cause authority register
- card authority register
- Batch 2 activation registers
- runtime context registers
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
docs/audit-papers/ARCH-COMPLETION-2_compiled_card_and_root_cause_authority_completion.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- output-authority estate map
- compiled output authority model summary
- root-cause authority audit result
- card authority audit result
- legacy path classification
- legacy path remediation
- provenance implementation details
- active signal estate integration result
- confirmation no signal packages activated or deactivated
- confirmation no SSOT changed unless explicitly justified
- confirmation no scoring changed
- confirmation no frontend changed
- confirmation no report compiler changed unless explicitly justified
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

Expected carry-forward handling:

```text
- close or update any carry-forward relating to legacy root-cause/card/hypothesis path ambiguity
- add precise carry-forward if a legacy path remains quarantined but not deleted
- add precise carry-forward if a card/root-cause type remains inactive pending authority mapping
- do not create vague residuals
```

Do not mark day-one architecture complete unless:

```text
- output authority is governed
- ungoverned legacy output is blocked/quarantined
- compiled output provenance is implemented or explicitly not required
- all validators and tests pass
```

---

## Expected changed files

Expected changed files may include:

```text
knowledge_bus/governance/compiled_output_authority_model_v1.yaml
knowledge_bus/governance/root_cause_authority_register_v1.yaml
knowledge_bus/governance/card_authority_register_v1.yaml
backend/core/**
backend/tests/regression/**
backend/tests/governance/**
backend/tests/**
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/ARCH-COMPLETION-2_compiled_card_and_root_cause_authority_completion.md
automation_bus/latest_cursor_status.json
```

Possible but must be justified:

```text
backend/core/reporting/**
```

Only touch report compiler code if compiled output authority or provenance cannot be completed otherwise.

No frontend files are expected to change.

No SSOT files are expected to change.

No signal package activation files are expected to change.

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
1. compiled output paths cannot be discovered
2. root-cause generation paths cannot be discovered
3. card generation paths cannot be discovered
4. output authority cannot be represented without breaking frontend DTO consumers
5. untraceable analytical output cannot be quarantined safely
6. compiled output currently depends on raw Pass 3 / investigation-spec files at runtime
7. root-cause output currently depends on raw Pass 3 / investigation-spec files at runtime
8. card output currently depends on frontend inference
9. changes would require frontend rendering edits
10. changes would require SSOT edits
11. changes would require signal package activation/deactivation
12. changes would require clinical threshold changes
13. diagnosis wording would be emitted
14. treatment/supplement recommendation would be emitted
15. validators fail
16. tests fail
17. secret-file guardrail fails
18. rollback path cannot be defined
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
feat(output): add governed authority provenance for compiled analytical output
```

If no runtime/code change occurs and the sprint only classifies/quarantines authority paths, use:

```text
docs(governance): complete compiled output authority mapping
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
- output-authority estate is discovered and documented
- compiled output authority model exists
- root-cause authority register exists or equivalent authority is documented
- card authority register exists or equivalent authority is documented
- every active analytical output path is governed or quarantined
- emitted analytical cards carry authority/provenance metadata where applicable
- emitted root-cause explanations carry authority/provenance metadata where applicable
- inactive/suppressed signals do not produce analytical conclusions
- raw research files are not consumed at runtime
- frontend remains render-only
- no signal activation/deactivation occurs
- no SSOT changes occur
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
Then proceed to ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.
```
