---
work_id: P1-20
branch: sprint/P1-20-cbc-package-provenance-and-psi-opt-in
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-20 — CBC Package Provenance Resolution and PSI Opt-In

You are Cursor, acting as the Knowledge Bus / Medical Intelligence implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is a Knowledge Bus provenance-resolution and production PSI opt-in sprint.

It is not a runtime sprint, not a frontend sprint, not a Core Engine sprint, and not a medical-review sprint.

## Purpose

Resolve the CBC package-identity mismatch blocking the `pkg_kb52c_*` staged PSI cohort from promotion into the existing `pkg_kb58_*` production packages.

If provenance is proven for each candidate, place the staged PSI into the correct `pkg_kb58_*` production package directory as a byte-copy, then opt it into production in the same sprint.

Do not split successful provenance resolution and PSI opt-in into separate sprints. That would create unnecessary SOP overhead.

## Baseline

Stage 0 Pipeline Advisory initially referenced five CBC candidates, but Stage B Mode 1 corrected this.

The canonical candidate set is four candidates from `docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`, `cf_003` to `cf_006`.

Stage B also confirmed that the four `pkg_kb58_*` production package manifests all cite:

`knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json`

and that the staged PSI source paths match the same source document.

Therefore, if candidate-level provenance proof passes, opt-in should proceed in this sprint.

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-19_production_opt_in_manifest.yaml`
* `docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml`
* `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
* `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md`
* `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
* `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml`
* `knowledge_bus/schema/package_manifest_schema.yaml`
* `backend/scripts/validate_promoted_signal_intelligence.py`
* `backend/scripts/validate_knowledge_package.py`
* `backend/scripts/validate_staged_psi_activation_readiness.py`

Use targeted search:

* `rg "pkg_kb52c_rbc_high_erythrocytosis_pattern|pkg_kb58_rbc_high_erythrocytosis_pattern" knowledge_bus docs`
* `rg "pkg_kb52c_rbc_low_iron_restricted_anemia_pattern|pkg_kb58_rbc_low_iron_restricted_anemia_pattern" knowledge_bus docs`
* `rg "pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis|pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis" knowledge_bus docs`
* `rg "pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern|pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern" knowledge_bus docs`
* `rg "cbc_hematology_pass_3.json" knowledge_bus/generated_pilot knowledge_bus/packages docs`

Inspect relevant hits before editing.

## Canonical candidate mapping

The candidate set is exactly these four mappings unless hardening proves the repository state differs:

1. `pkg_kb52c_rbc_high_erythrocytosis_pattern`
   → `pkg_kb58_rbc_high_erythrocytosis_pattern`

2. `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern`
   → `pkg_kb58_rbc_low_iron_restricted_anemia_pattern`

3. `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis`
   → `pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis`

4. `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern`
   → `pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern`

Do not add a fifth candidate unless direct repository evidence proves a distinct fifth candidate exists in the P1-19 carry-forward manifest.

If the Stage 0 advisory’s duplicated candidate appears again, record it as an advisory duplication, not a fifth implementation candidate.

## Files in scope

Allowed if justified:

* `docs/sprints/beta_readiness/P1-20_cbc_package_provenance_and_psi_opt_in.md`
* `docs/sprints/beta_readiness/P1-20_cbc_provenance_manifest.yaml`
* `docs/sprints/beta_readiness/P1-20_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* the staged PSI YAML file for each of the four mapped `pkg_kb52c_*` candidates under `knowledge_bus/generated_pilot/` — read-only for provenance verification; must not be edited
* `knowledge_bus/packages/pkg_kb58_rbc_high_erythrocytosis_pattern/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb58_rbc_high_erythrocytosis_pattern/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb58_rbc_low_iron_restricted_anemia_pattern/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb58_rbc_low_iron_restricted_anemia_pattern/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern/promoted_signal_intelligence.yaml`

## Files out of scope

Do not modify:

* backend/
* frontend/
* runtime loaders
* parser files
* DTO/report/Gemini/scoring files
* tests
* validators
* raw Pass 3 research content
* generated-pilot files of any kind — all generated-pilot PSI files and compile manifests are read-only in P1-20
* generated-pilot compile manifests
* existing production `signal_library.yaml`
* existing production `research_brief.yaml`
* package manifests outside the four mapped `pkg_kb58_*` production hosts
* production packages outside the four mapped `pkg_kb58_*` hosts
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Critical prohibitions

Do not:

* invent medical content;
* rewrite medical interpretation text;
* alter thresholds, activation rules, evidence strength, supporting markers, contradiction markers, clinical modifiers or meaning;
* edit raw Pass 3 research;
* edit generated-pilot compile manifests;
* edit signal libraries;
* edit research briefs;
* create new signal definitions;
* create new production package hosts;
* place PSI into any production package whose provenance proof has not passed Phase 2;
* opt in any candidate whose provenance proof fails;
* edit backend, frontend, runtime, validator, parser, DTO, Gemini, scoring or test files;
* use a fallback parser;
* use global/default reference ranges.

## Re-homing definition

For this sprint, re-homing means production placement only. Do not edit any generated-pilot file.

1. Copy the staged PSI byte-for-byte from `knowledge_bus/generated_pilot/p1_11_batch_b/<pkg_kb52c_*>/promoted_signal_intelligence.yaml` into the mapped `pkg_kb58_*` production package directory as `promoted_signal_intelligence.yaml`. Do not alter the file in any way.
2. Add `promoted_signal_intelligence: promoted_signal_intelligence.yaml` to the mapped `pkg_kb58_*` production `package_manifest.yaml`. No other fields in the production manifest are changed.
3. Validate the production PSI.
4. Validate the production package.

No other generated-pilot or production package edits are permitted.

## Hash-bound generated-pilot rule

The staged PSI and its compile manifest are hash-bound. The compile manifest records the SHA256 of the staged PSI under `output_hashes_sha256`. Editing the staged PSI would change its SHA256 and cause `validate_staged_psi_activation_readiness.py` to report `BLOCKED_MANIFEST_OR_HASH` for that candidate. Therefore all generated-pilot PSI files and compile manifests are read-only in P1-20. Do not rename generated-pilot directories.

After opt-in, the staged activation-readiness validator will continue to report `production_manifest_opt_in: false` for these four candidates. This is expected behaviour: the validator derives package identity from the staged directory name (`pkg_kb52c_*`) and the production opt-in is registered under `pkg_kb58_*` — the names will never match. The production opt-in is structurally valid regardless. Document this in the sprint report; do not attempt to fix it.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-20-cbc-package-provenance-and-psi-opt-in`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-20`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Confirm canonical candidate set

Read:

* `docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-19_production_opt_in_manifest.yaml`

Confirm the canonical CBC candidate set is four candidates, not five.

Create:

`docs/sprints/beta_readiness/P1-20_cbc_provenance_manifest.yaml`

For each candidate record:

* carry-forward ID;
* staged `pkg_kb52c_*` package ID;
* mapped production `pkg_kb58_*` package ID;
* staged PSI path;
* staged PSI current internal `package_id`;
* staged source path;
* production package manifest path;
* production `source_document`;
* whether production package already has `promoted_signal_intelligence`;
* provenance decision;
* re-homing decision;
* opt-in decision;
* validation result;
* blocker class if not promoted.

Allowed decisions:

* `PROVENANCE_CONFIRMED_REHOME_AND_OPT_IN`
* `ALREADY_OPTED_IN`
* `BLOCKED_SOURCE_DOCUMENT_MISMATCH`
* `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`
* `BLOCKED_PRODUCTION_HOST_MISSING`
* `BLOCKED_PRODUCTION_PSI_ALREADY_PRESENT`
* `BLOCKED_VALIDATION_FAILURE`
* `BLOCKED_REQUIRES_MEDICAL_REVIEW`
* `BLOCKED_REQUIRES_CORE_BACKEND_AGENT`
* `OUT_OF_SCOPE_FOR_P1_20`

## Phase 2 — Candidate-level provenance proof gate

For each of the four candidates, prove provenance before editing.

Provenance is confirmed only if all of the following are true:

1. Staged PSI exists.
2. Staged PSI internal `package_id` currently equals the expected `pkg_kb52c_*` ID.
3. Staged PSI or compile manifest cites source path:
   `knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json`
4. Mapped production `pkg_kb58_*` package manifest exists.
5. Mapped production package manifest `package_id` equals the expected `pkg_kb58_*` ID.
6. Mapped production package manifest `source_document` equals:
   `knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json`
7. Production package has no existing `promoted_signal_intelligence` field.
8. No medical-review or frame-authority blocker exists for the candidate.
9. No signal-library change is required.
10. No medical content change is required.

If any condition fails, STOP for that candidate and classify in the provenance manifest.

Do not opt in failed candidates.

## Phase 3 — Re-home and opt in successful candidates

For each candidate passing Phase 2:

1. Copy the staged PSI byte-for-byte from `knowledge_bus/generated_pilot/p1_11_batch_b/<pkg_kb52c_*>/promoted_signal_intelligence.yaml` into the mapped production package directory as `promoted_signal_intelligence.yaml`. Do not edit the file.
2. Add `promoted_signal_intelligence: promoted_signal_intelligence.yaml` to the mapped production `package_manifest.yaml`. Do not alter any other field in the production manifest.
3. Validate the production PSI.
4. Validate the production package.
5. Record decision: `PROVENANCE_CONFIRMED_REHOME_AND_OPT_IN`.

Do not edit the staged PSI under `knowledge_bus/generated_pilot/`. Do not edit compile manifests.

## Phase 4 — Post-change readiness validation

Run:

* direct PSI validation for every new production PSI;
* `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<pkg_kb58_package>` for each changed production package;
* `python backend/scripts/validate_staged_psi_activation_readiness.py`.

If a standard Knowledge Bus validation batch command exists, run it as well.

Do not edit validators to make validation pass.

The staged activation-readiness validator will continue to show `production_manifest_opt_in: false` for the four re-homed candidates. This is expected — see the Hash-bound generated-pilot rule above. Record the validator output as-is; do not treat this as a failure.

## Phase 5 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-20_pass3_carry_forward.yaml`

Include only material unresolved items.

For each unresolved item record:

* item ID;
* candidate/package reference;
* rich Pass 3 content at risk;
* why not implemented;
* blocker class;
* owner agent:

  * Knowledge Bus
  * Medical Review
  * Core Engine
  * Frontend/Presentation
* launch/beta relevance;
* recommended future package.

If all four CBC candidates are successfully opted in, record that there are no remaining CBC package-provenance carry-forwards from this sprint.

Do not re-document unrelated P1-19 ferritin or TSAT blockers unless they are needed for next-sprint sequencing.

## Phase 6 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-20_cbc_package_provenance_and_psi_opt_in.md`

Keep it concise.

Maximum structure:

1. start state;
2. canonical candidate set;
3. provenance proof results;
4. re-homing and opt-ins completed;
5. validation results;
6. carry-forwards;
7. recommended next sprint.

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight:

* delivered;
* blocked/carry-forward;
* recommended next sprint.

Do not write long narrative documentation.
Do not duplicate audit content.
Do not list every untouched file.

## Acceptance criteria

P1-20 passes only if:

1. The candidate set is confirmed from P1-19 carry-forward as four candidates.
2. The Stage 0 duplicated fifth candidate is not implemented as a separate candidate.
3. Each of the four candidates receives candidate-level provenance adjudication.
4. Every successful candidate proves staged compile manifest `source_path` and production `source_document` both equal `knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json`.
6. Every successful candidate is opted into the mapped `pkg_kb58_*` production package in the same sprint.
7. No candidate is opted in if provenance proof fails.
8. No medical content is invented or changed.
9. No signal_library files are changed.
10. No research_brief files are changed.
11. No raw Pass 3 research files are changed.
12. No generated-pilot files are modified — staged PSI files and compile manifests are read-only.
13. Production PSI files are byte-copies of the staged PSI; no field is altered during copying.
14. Production package manifests are updated only to add `promoted_signal_intelligence: promoted_signal_intelligence.yaml`; no other field is changed.
15. No backend, frontend, runtime, parser, validator, test, DTO, Gemini or scoring files are modified.
16. Every new production PSI validates.
17. Every changed production package validates.
18. Staged activation-readiness validator runs successfully after changes. The validator will continue to show `production_manifest_opt_in: false` for the four re-homed candidates because it matches by staged directory name; this is expected and must be documented in the sprint report, not treated as a failure.
19. Carry-forward manifest captures any unresolved CBC items with owner and blocker class.
20. Build register is updated concisely.
21. Sprint report is concise and documents the staged-validator expected behaviour for re-homed packages.
22. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

## Closure requirements

Before finish, perform the mandatory Post-Implementation Closure Protocol.

Run and report:

* `git branch --show-current`
* `git status --short`
* `git log --oneline -n 5`
* `git diff --name-only`
* `git diff --cached --name-only`
* `git stash list`

Confirm:

* branch matches this sprint branch;
* no unrelated tracked/untracked files;
* no tooling leakage;
* no stash ambiguity;
* no parked files outside the repository;
* latest commit contains only in-scope work.

Then run:

`python backend/scripts/run_work_package.py finish`

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.
