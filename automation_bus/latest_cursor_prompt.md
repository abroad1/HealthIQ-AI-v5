---
work_id: ARCH-RT-5D_package_provenance_backfill
branch: work/ARCH-RT-5D-package-provenance-backfill
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-5D — Package Provenance Backfill

## Purpose

Resolve or explicitly classify the remaining package/source provenance gaps that prevent the HealthIQ day-one architecture from being fully provenance-complete.

This sprint must address the unresolved provenance estate identified across ARCH-RT-0 through ARCH-RT-5C:

```text
package inventory
→ source_document/source_spec_id classification
→ explicit vs inferred provenance distinction
→ kb52c / batch JSON resolution or classification
→ activation_key/source_spec_id provenance quality
→ compile manifest hash refresh
→ estate index / authority manifest refresh
````

This sprint must not change clinical runtime behaviour.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
ARCH-RT-2_identity_runtime_pilot — merged
ARCH-RT-3_card_evidence_vertical_slice — merged
ARCH-RT-4_compiled_hypothesis_root_cause_slice — merged
ARCH-RT-5_full_regeneration_and_launch_gate — merged
ARCH-RT-5B_card_evidence_estate_and_required_provenance — merged
ARCH-RT-5C_hypothesis_runtime_promotion — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 14
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-5C is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch Knowledge Bus package manifests, compiled estate index/provenance artefacts, compile manifests, provenance validators, audit papers and package governance policy. Package/provenance authority is foundational to runtime safety, even if runtime behaviour must not change.

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Authoritative inputs

Read these files before making changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/compile_manifest_contract.md
docs/architecture/activation_compile_gap_report.md
docs/architecture/package_generation_inventory.md
docs/architecture/legacy_package_retirement_candidates.md
docs/architecture/signal_id_collision_inventory.md
docs/audit-papers/ARCH-RT-5_M1_package_provenance_and_collision_audit.md
docs/audit-papers/ARCH-RT-5B_card_evidence_provenance_audit.md
docs/audit-papers/ARCH-RT-5C_hypothesis_runtime_promotion_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
knowledge_bus/compiled/estate_index_v1.yaml
knowledge_bus/schema/compile_manifest_schema_v1.yaml
backend/scripts/validate_compile_manifest.py
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required authority file is missing.

If the updated sprint plan has a different path, locate it and report the path before proceeding.

## Mandatory inherited decisions and carry-forwards

The following are binding:

```text
compile_id is canonical.
compile_run_id is transitional only.
If both compile_id and compile_run_id are present, they must be equal.
activation_key is required for runtime activation identity.
signal_id remains signal-family identity.
source_spec_id must distinguish explicit provenance from inferred provenance.
Directory-derived source_spec_id is not canonical research provenance.
Inferred provenance may not be silently upgraded to explicit provenance.
PSI remains signal-layer semantics only.
Hypothesis graphs must not be placed into PSI.
Frontend must not infer clinical meaning.
```

Carry-forward from ARCH-RT-1:

```text
compile_manifest_schema_v1 was initially DRAFT.
activation_keys_emitted, collisions_detected and policy_version were optional only while DRAFT.
Before production compiler use, schema lock, or launch-critical compile manifest use, ADR-required manifest fields must become required or explicitly classified.
```

Carry-forward from ARCH-RT-2:

```text
source_spec_id inferred from package_id is interim identity fallback only.
Future provenance work must distinguish explicit source_spec_id from inferred source_spec_id.
```

Carry-forward from ARCH-RT-3 / ARCH-RT-5B:

```text
Compiled card artefacts may contain inferred source_spec_ids only if explicitly declared.
Five card markers remained inferred provenance after ARCH-RT-5B:
- total_cholesterol
- tc_hdl_ratio
- insulin
- ast
- bilirubin
```

Carry-forward from ARCH-RT-5 / ARCH-RT-5C:

```text
Some compile manifest hashes were pending_inventory_refresh.
kb52c / batch JSON packages remained blocked_pending_spec_extraction.
Full 186-package provenance backfill remained unresolved.
```

Do not reopen these decisions.

If repository evidence contradicts any inherited decision, STOP and report.

## Main objective

This sprint must produce a complete, repo-grounded provenance classification for all active package manifests and launch-relevant compiled artefacts.

For each package / artefact, classify provenance as one of:

```text
explicit_source_spec_id
source_document_derived
package_manifest_inferred
package_id_inferred
batch_json_blocked_pending_spec_extraction
architecture_doc_source_blocked
legacy_retained_with_justification
deferred_for_regeneration
retire_candidate
provenance_gap
unknown_requires_review
```

No active package may remain unclassified.

## Scope

Allowed scope:

1. Scan all package manifests.
2. Classify each package by provenance status.
3. Resolve simple `source_document` → explicit/spec-derived provenance where the source file exists and is unambiguous.
4. Add or update provenance metadata in package manifests only where safe, explicit and mechanically verifiable.
5. Do not fabricate source_spec_id.
6. Do not turn inferred IDs into explicit IDs.
7. Refresh compile manifest hashes for launch-relevant compiled artefacts where source/output files are stable.
8. Tighten compile manifest validator to enforce `compile_run_id == compile_id` when both are present.
9. Decide whether manifest fields currently optional remain DRAFT-only or should become required for launch-relevant manifests.
10. Refresh `estate_index_v1.yaml` provenance status where needed.
11. Update active authority manifest and traceability audit.
12. Produce package provenance backfill audit.
13. Produce unresolved provenance register for remaining blocked/deferred items.

## Required deliverables

Create or update:

```text
docs/audit-papers/ARCH-RT-5D_package_provenance_backfill_audit.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
docs/audit-papers/ARCH-RT-5D_compile_manifest_refresh_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/research_to_runtime_traceability_audit.md
knowledge_bus/compiled/estate_index_v1.yaml
```

May update only if justified by scope:

```text
knowledge_bus/packages/**/package_manifest.yaml
knowledge_bus/compiled/manifests/*.yaml
knowledge_bus/schema/compile_manifest_schema_v1.yaml
backend/scripts/validate_compile_manifest.py
backend/tests/**/*compile_manifest*provenance*.py
```

Do not create broad helper scripts unless they are permanent governed validators and explicitly justified.

## Package manifest rules

Allowed package manifest changes:

* add `source_spec_id` only where directly verified from an actual investigation spec field or inv YAML source path
* add `source_spec_id_source` or equivalent field to distinguish:

  * explicit
  * source_document_derived
  * package_id_inferred
  * batch_json_unresolved
* add `activation_key` only if it follows ADR-RT-002 and can be generated deterministically from verified frame identity
* add `provenance_classification`
* add `compile_manifest_ref` only if a real manifest exists and resolves

Forbidden package manifest changes:

* do not add explicit `source_spec_id` based only on package directory name
* do not add explicit `source_spec_id` for batch JSON packages unless the exact spec record is extracted or verified
* do not modify signal thresholds
* do not modify clinical criteria
* do not modify signal_id to avoid collision
* do not modify package evidence content
* do not regenerate packages
* do not change PSI opt-in unless directly justified and validated

## kb52c / batch JSON rule

For kb52c / batch JSON packages:

* attempt to determine whether the exact source spec record can be identified from batch JSON content
* if exact extraction is not safe or not in scope, classify as:

```text
batch_json_blocked_pending_spec_extraction
```

* do not infer explicit source_spec_id from package directory
* do not fabricate canonical provenance
* produce a list of all affected packages

If extraction would require a broad batch parser/compiler, STOP and classify rather than implementing that compiler in this sprint.

## Five inferred card marker rule

For the five known inferred card markers:

```text
total_cholesterol
tc_hdl_ratio
insulin
ast
bilirubin
```

This sprint must either:

* find explicit provenance, or
* confirm the current inferred classification, or
* mark blocked_pending_spec_extraction / blocked_pending_medical_review

Do not silently treat them as fully resolved.

## Compile manifest rules

For launch-relevant compile manifests:

* `compile_id` is canonical
* if `compile_run_id` exists, validator must enforce equality with `compile_id`
* refresh hashes if previous value was `pending_inventory_refresh`
* do not leave manifest hash fields stale if the referenced artefact is launch-relevant
* if hash cannot be refreshed, classify why
* manifest refs in compiled artefacts must resolve to real manifest files or estate index entries

If changing schema strictness:

* do not break existing non-launch draft manifests without classification
* document whether schema remains DRAFT or is partially launch-locked
* add tests for validator behaviour

## Out of scope

Do not:

* change runtime behaviour
* modify SignalRegistry
* modify SignalEvaluator
* modify root-cause compiler runtime logic
* modify card evidence loader runtime logic
* modify frontend
* implement PSI runtime wiring
* implement activation compiler
* regenerate packages
* extract all batch JSON specs unless hardening confirms safe bounded scope
* modify clinical thresholds
* modify scoring rails
* modify biomarker SSOT
* modify investigation specs
* modify PSI artefacts
* modify root-cause YAML
* modify card evidence clinical content
* introduce fallback parsers

## Authority preflight

Before implementation, verify and report:

1. total package manifest count
2. package generation counts
3. current package fields available for provenance
4. count of packages with source_spec_id
5. count of packages with activation_key
6. count of batch JSON source packages
7. count of architecture-doc-sourced packages
8. count of package_id-inferred provenance candidates
9. current compile manifest files and validation status
10. current pending_inventory_refresh occurrences
11. current estate index entries
12. current five inferred card marker provenance status
13. current unresolved provenance classifications from ARCH-RT-5 audits

If the scope is too broad to resolve safely, STOP and propose a split.

## Required tests

At minimum, add or update tests covering:

1. compile manifest validator enforces `compile_run_id == compile_id` when both exist
2. launch-relevant compile manifests validate
3. manifest refs resolve from compiled artefacts
4. estate index resolves launch-relevant artefacts
5. package provenance classification output includes all package manifests
6. no package remains unclassified in the audit output
7. inferred provenance is not treated as explicit
8. kb52c / batch JSON packages are classified correctly
9. five inferred card markers are classified

If tests are implemented as script-level audit tests, they must be permanent and justified.

## STOP conditions

STOP and report if:

1. required authority files are missing
2. package manifest scan cannot be performed
3. any package cannot be classified
4. explicit source_spec_id cannot be distinguished from inferred
5. kb52c extraction would require broad compiler work
6. compile manifest hashes cannot be refreshed or classified
7. manifest validator changes would break existing launch-relevant manifests
8. package changes would alter runtime signal behaviour
9. work requires modifying package clinical content
10. scope expands into PSI wiring, card runtime, root-cause runtime, frontend or activation compiler
11. tests cannot prove provenance classification completeness

## Required reports

Create:

```text
docs/audit-papers/ARCH-RT-5D_package_provenance_backfill_audit.md
```

Must include:

* total package count
* classification counts
* table or grouped listing by classification
* packages updated
* packages not updated and why
* batch JSON/kb52c status
* architecture-doc-sourced package status
* explicit vs inferred source_spec_id status
* activation_key status
* remaining launch blockers, if any

Create:

```text
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
```

Must include every unresolved/deferred provenance item, with:

* item id
* package/artefact/marker
* classification
* reason
* required future action
* launch blocker status

Create:

```text
docs/audit-papers/ARCH-RT-5D_compile_manifest_refresh_audit.md
```

Must include:

* manifests checked
* hashes refreshed
* hashes still pending
* validator changes
* schema strictness decision
* manifest refs resolved
* unresolved manifest issues

## Evidence required from Cursor

Cursor must report:

1. baseline branch/status/HEAD evidence
2. authority preflight findings
3. package classification counts
4. exact package manifests modified, if any
5. exact compile manifests modified, if any
6. validator/schema changes, if any
7. estate index changes
8. tests added/updated
9. test commands run
10. test results
11. unresolved provenance register summary
12. confirmation no runtime behaviour changed
13. confirmation no clinical package content changed
14. confirmation no PSI/card/root-cause/frontend work included

## Closure requirements

Before `run_work_package.py finish`, complete the Automation Bus post-implementation closure protocol.

Run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify:

* tracked modified files
* staged files
* untracked files
* tooling files
* out-of-scope files
* stash entries

Do not run finish unless:

* current branch matches `work/ARCH-RT-5D-package-provenance-backfill`
* all changed files are tied to provenance scope
* no runtime/code clinical behaviour files are modified unless explicitly approved by hardening
* no helper scripts are included unless permanent and justified
* no ambiguous stash exists
* all packages are classified
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. all active packages are classified by provenance status
2. explicit vs inferred source_spec_id is distinguished
3. kb52c / batch JSON packages are resolved or classified
4. five inferred card markers are resolved or classified
5. compile manifest refs resolve or are classified
6. pending_inventory_refresh hashes are refreshed or classified
7. validator enforces compile_run_id == compile_id when both exist
8. estate index and authority manifest are refreshed
9. no runtime behaviour changes occur
10. no package clinical content changes occur
11. unresolved provenance register exists
12. tests prove provenance classification and manifest validation
13. Automation Bus gate passes

```
```
