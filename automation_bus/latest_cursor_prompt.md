---
work_id: MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation
branch: work/MED-RESEARCH-REVIEW-1-non-pass3-package-revalidation
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# MED-RESEARCH-REVIEW-1 — Non-Pass 3 Package Revalidation Audit

## Purpose

Audit and classify the non-Pass_3 / unclear-provenance Knowledge Bus packages discovered during CRP-PASS3-MIGRATION.

This sprint must determine which runtime-active or governance-relevant packages need to be:

```text
- accepted as currently valid
- re-run through the current Knowledge Bus / Pass_3 medical research process
- replaced
- retired
- deferred with rationale
- escalated for clinical/medical review
````

This is an audit/classification sprint only.

Do not modify production code, runtime package logic, SignalEvaluator, SignalRegistry, thresholds, scoring, frontend, compiled artefacts, schemas, or medical content.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
MED-REV-1 merged
MED-REV-2 merged
KB-UTIL-1 merged
LAYER-B-1 merged
ARCH-LEGACY-1 merged
ARCH-LEGACY-2 merged
CRP-PASS3-MIGRATION merged
docs/sprints/launch_core_carry_forward_register.md present and updated
```

Before creating or switching branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- CRP-PASS3-MIGRATION is not merged
- docs/sprints/launch_core_carry_forward_register.md is missing
- CRP-PASS3 non-Pass_3 package audit artefacts are missing
```

## Governance classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This is an audit/classification sprint only. It must not change runtime behaviour. It may recommend future HIGH-risk medical research or package migration work.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Carry-forward register handling

Before investigation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Relevant carry-forwards include:

```text
CF-MRIMPROVE-001 — Re-review non-Pass_3 runtime packages through Knowledge Bus
CF-MRIMPROVE-002 — pkg_kb45_* pre–Pass 3 batch JSON lineage
CF-MRIMPROVE-003 — architecture-doc anchor package cohort
CF-MRIMPROVE-004 — pkg_lipid_transport provenance gap
CF-CHRONICINFL-001 — Pass 3 frame for signal_systemic_inflammation
CF-CRPPASS3-001 — Compile Batch_4 Pass_3 CRP frames into governed runtime package
```

If this sprint resolves, reclassifies, or creates carry-forwards, update the register.

Do not leave carry-forwards only in chat, audit summaries, or sprint reports.

## Authoritative inputs

Read these sprint-specific files before investigation:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment_report.md
docs/audit-papers/CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md
docs/audit-papers/_crp_pkg_audit_non_pass3.json
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md
docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as needed:

```text
knowledge_bus/packages/**
knowledge_bus/research/**
knowledge_bus/compiled/**
knowledge_bus/governance/**
backend/core/analytics/signal_evaluator.py
backend/core/knowledge/**
backend/scripts/validate_day_one_architecture.py
```

If paths differ, locate and report the actual paths.

## Problem statement

CRP-PASS3-MIGRATION discovered that not all runtime-active packages were generated through the current Pass_3 research process.

Known estate summary from CRP-PASS3-MIGRATION:

```text
Total packages: 187
Pass_3-sourced: 132
Not Pass_3-sourced: 55
Runtime-loaded: 186
Research/context-only: 0
```

This does not mean the non-Pass_3 packages are wrong.

It means they need internal Knowledge Bus re-review so HealthIQ can confirm, update, replace, retire, or defer them before treating them as mature launch intelligence.

No user-facing disclosure is required or desired.

## Key principle

Do not overclaim internally or externally.

Classify package maturity honestly, but do not create user-facing warnings.

The intended internal position is:

```text
Runtime-active does not automatically mean Pass_3-mature.
Non-Pass_3 does not automatically mean clinically invalid.
Non-Pass_3 runtime packages require Knowledge Bus re-review before being treated as mature launch intelligence.
```

## Required investigation

Using the 55-row non-Pass_3 package audit as the starting point, classify each package by:

```text
- package_id
- signal_id(s)
- source_type
- source_document
- has signal_library.yaml
- runtime_loaded
- current runtime or product use
- provenance confidence
- medical maturity tier
- likely launch relevance
- recommended action
- future sprint/workstream
```

## Package cohort groups

At minimum classify these cohorts:

### 1. Study-derived packages

Known examples:

```text
pkg_chronic_inflammation
pkg_insulin_resistance
pkg_hepatic_metabolic_stress
```

Questions:

```text
- What study markdown or source document created them?
- Which signals do they define?
- Are they runtime-loaded?
- Do they affect visible launch surfaces?
- Do they need dedicated Pass_3 frames?
- Should they remain temporarily classified or be prioritised for re-review?
```

### 2. `pkg_kb45_*` batch JSON packages

Questions:

```text
- Which batch JSON files created them?
- Are they pre-Pass_3 or equivalent to Pass_3?
- Are they runtime-loaded?
- Which signals do they define?
- Are any launch-visible?
- Should they be re-run through Pass_3 or mapped to existing Pass_3 frames?
```

### 3. Architecture-doc anchor packages

Questions:

```text
- Which packages cite architecture documents rather than medical research specs?
- Are they runtime-loaded?
- Are they product-context packages or signal-driving packages?
- Should they be reclassified as internal scaffolding, reworked through Pass_3, or retired?
```

### 4. `pkg_lipid_transport` provenance gap

Questions:

```text
- What evidence exists for its source?
- Is it runtime-loaded?
- Does it affect the atherogenic lipid pattern card or other visible outputs?
- Can provenance be recovered?
- Should it be treated as medical research improvement required?
```

### 5. CRP / inflammation packages

Questions:

```text
- Confirm distinction between signal_crp_high and signal_systemic_inflammation.
- Confirm which packages define each.
- Confirm which are Pass_3-derived, s24-derived, or study-derived.
- Confirm what remains deferred after CRP-PASS3-MIGRATION.
```

## Classification model

Use these maturity classifications:

```text
pass3_mature
non_pass3_runtime_revalidation_required
study_derived_revalidation_required
batch_json_lineage_review_required
architecture_anchor_review_required
provenance_gap
retire_candidate
accepted_with_rationale
deferred_non_launch_blocker
launch_relevant_review_required
```

No package in the 55-row cohort may remain unclassified.

## Recommended action model

For each package, assign one recommended action:

```text
accept_as_currently_valid_with_rationale
re_run_through_pass3
map_to_existing_pass3_frame
author_new_pass3_frame
recover_provenance
retire_package
defer_with_reason
escalate_for_medical_review
```

## Launch relevance assessment

For each package, classify launch relevance:

```text
launch_visible
runtime_active_not_visible
internal_only
unknown_requires_trace
not_runtime_loaded
```

If a non-Pass_3 package is launch-visible, highlight it clearly.

## Output artefacts

Create:

```text
docs/audit-papers/MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation_audit.md
```

Also create or update a machine-readable classification file:

```text
knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml
```

This governance file should include the 55 non-Pass_3 / unclear-provenance packages and their classification.

It must not be consumed by runtime in this sprint.

## Required report content

The audit report must include:

```text
- executive verdict
- package cohort summary
- full 55-package classification table
- runtime-loaded package count
- launch-visible package count
- packages needing Pass_3 re-run
- packages needing new Pass_3 frames
- packages needing provenance recovery
- packages safe to defer
- packages that may be retired
- package-level recommended actions
- carry-forward register updates
- recommended next sprint
```

## Required governance register fields

For each package in `non_pass3_package_revalidation_register_v1.yaml`, include:

```yaml
package_id:
signal_ids:
source_type:
source_document:
pass3_sourced:
has_signal_library:
runtime_loaded:
launch_relevance:
maturity_classification:
medical_research_revalidation_required:
recommended_action:
recommended_future_sprint:
carry_forward_id:
notes:
```

Optional fields may be added if useful, but do not overcomplicate.

## Out of scope

Do not:

```text
- rewrite packages
- migrate packages
- delete packages
- change runtime package loading
- change SignalEvaluator or SignalRegistry
- change activation thresholds
- change scoring rails
- change biomarker SSOT
- change unit conversion
- change frontend
- add user-facing warnings
- implement medical research lifecycle process
- implement full Pass_3 estate compiler
- expose new hypothesis/contradiction/confirmatory-test content
```

## Required checks

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If they fail, STOP and report.

## STOP conditions

STOP and report if:

```text
1. CRP-PASS3 provenance artefacts are missing.
2. The 55-package cohort cannot be reconstructed.
3. Runtime-loaded status cannot be determined.
4. Launch relevance cannot be determined for a package that appears user-facing.
5. The audit discovers a likely launch blocker.
6. The audit would require package/runtime changes to complete.
7. ARCH-RT-6 validator fails.
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. carry-forward register read/update evidence
3. files inspected
4. package cohort counts
5. 55-package classification table
6. launch-relevant package findings
7. recommended future sprint(s)
8. tests/validators run
9. test results
10. confirmation no production code was changed
```

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

```text
- current branch matches work/MED-RESEARCH-REVIEW-1-non-pass3-package-revalidation
- only audit documentation, governance classification, and carry-forward register files are changed
- no runtime package behaviour is changed
- no production code is changed
- no helper scripts are committed
- no ambiguous stash exists
- latest commit contains only in-scope audit/classification work
```

## Success criteria

This sprint is complete only if:

```text
1. all 55 non-Pass_3 / unclear-provenance packages are classified
2. runtime-loaded status is recorded
3. launch relevance is assessed
4. packages needing Knowledge Bus re-review are clearly identified
5. user-facing disclosure is not introduced
6. future sprint recommendations are clear
7. carry-forward register is updated
8. ARCH-RT-6 validator passes
9. no production code is changed
10. Automation Bus gate passes
```

```
```
