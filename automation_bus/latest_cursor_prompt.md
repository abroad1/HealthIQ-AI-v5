---
work_id: P1-21
branch: sprint/P1-21-ferritin-high-authority-reconciliation
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-21 — Ferritin-High Signal Authority Reconciliation and PSI Promotion

You are Cursor, acting as the Knowledge Bus / Medical Intelligence implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is a Knowledge Bus authority-reconciliation and production PSI promotion sprint.

It is not a runtime sprint, not a frontend sprint, not a Core Engine sprint, and not a Medical Review sprint.

## Purpose

Resolve the ferritin-high signal authority collision blocking promotion of the Pass 3 ferritin-high PSI cohort.

The authorised architectural direction is Option A from Stage B advisory:

Retire legacy `pkg_s24_ferritin_high_overload` from active signal authority and migrate ferritin-high authority into modern `pkg_kb*` production packages using the governed Pass 3 ferritin-high PSI artefacts.

This sprint must record the authority decision, prove retirement safety, create the modern production package hosts, install the two validated Pass 3 PSIs, and validate the resulting Knowledge Bus package estate.

## Authority decision to record before implementation

Before modifying package files, create a concise ADR / decision note recording:

`ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1`

Location:

* use the repository’s existing ADR / architecture decision location if present;
* otherwise create under `docs/architecture/`.

The ADR must record:

1. `pkg_s24_ferritin_high_overload` is legacy authority.
2. `pkg_s24` owns `signal_ferritin_high` only through a legacy `signal_library.yaml`.
3. `pkg_s24` has no `promoted_signal_intelligence.yaml`.
4. `pkg_s24` uses a validator-compatibility placeholder threshold and is not the governed Pass 3 intelligence authority.
5. The two Pass 3 ferritin-high candidates are distinct clinical interpretive frames:

   * inflammatory hyperferritinemia;
   * iron-overload context.
6. The repository already supports multiple modern packages sharing one `signal_id` where they represent distinct PSI contexts.
7. Option A is selected:

   * retire `pkg_s24_ferritin_high_overload` from active authority;
   * promote the two Pass 3 ferritin-high contexts into modern `pkg_kb*` production packages;
   * keep `signal_ferritin_high` as the signal ID;
   * do not create new signal IDs;
   * do not change runtime evaluator behaviour.
8. Options B and C are rejected:

   * Option B creates unnecessary signal-evaluator surface risk;
   * Option C creates an incoherent mixed legacy/modern package host.
9. No medical content is invented or changed.

Keep the ADR concise. Do not write a long narrative paper.

## Baseline evidence

Stage B advisory found:

* `knowledge_bus/packages/pkg_s24_ferritin_high_overload/signal_library.yaml` defines `signal_id: signal_ferritin_high`;
* `pkg_s24` has no `promoted_signal_intelligence.yaml`;
* `pkg_s24` uses legacy `library.package_id: KBP-2404`;
* `pkg_s24` uses a placeholder threshold of `9999.0`;
* the two staged Pass 3 PSIs are validated and distinct;
* existing production precedent supports multiple packages sharing the same signal ID where each package has distinct PSI context.

Use Stage B advisory as inherited structural evidence only where still current. Re-verify all fresh claims required by hardening.

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-19_production_opt_in_manifest.yaml`
* `docs/sprints/beta_readiness/P1-19_blood_iron_oxygen_kb_production_intelligence.md`
* `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
* `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md`
* `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
* `knowledge_bus/schema/package_manifest_schema.yaml`
* `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml`
* `backend/scripts/validate_promoted_signal_intelligence.py`
* `backend/scripts/validate_knowledge_package.py`
* `backend/scripts/validate_staged_psi_activation_readiness.py`
* `backend/tests/regression/test_signal_authority_collision_enforcement.py`
* `knowledge_bus/packages/pkg_s24_ferritin_high_overload/package_manifest.yaml`
* `knowledge_bus/packages/pkg_s24_ferritin_high_overload/research_brief.yaml`
* `knowledge_bus/packages/pkg_s24_ferritin_high_overload/signal_library.yaml`
* staged generated-pilot artefacts and compile manifests for:

  * `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`
  * `pkg_kb52c_ferritin_high_iron_overload_context`

Use targeted search:

* `rg "pkg_s24_ferritin_high_overload|KBP-2404|signal_ferritin_high" .`
* `rg "pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia|pkg_kb52c_ferritin_high_iron_overload_context" knowledge_bus docs`
* `rg "ferritin_high|hyperferritinemia|iron_overload_context" knowledge_bus docs backend`
* `rg "promoted_signal_intelligence" knowledge_bus/packages/pkg_s24_ferritin_high_overload knowledge_bus/generated_pilot`
* `rg "signal_ferritin_high" backend knowledge_bus docs`

Inspect relevant hits before editing.

## Files in scope

Allowed if justified:

* ADR / decision note:

  * `docs/architecture/ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1.md`
  * or equivalent existing ADR location;
* `docs/sprints/beta_readiness/P1-21_ferritin_high_authority_reconciliation.md`
* `docs/sprints/beta_readiness/P1-21_ferritin_high_promotion_manifest.yaml`
* `docs/sprints/beta_readiness/P1-21_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* retirement/archive treatment for:

  * `knowledge_bus/packages/pkg_s24_ferritin_high_overload/`
* new modern production package directories for the two ferritin-high Pass 3 contexts;
* within those new package directories only:

  * `package_manifest.yaml`
  * `research_brief.yaml`
  * `signal_library.yaml`
  * `promoted_signal_intelligence.yaml`
* `backend/tests/regression/test_signal_authority_collision_enforcement.py` only if the existing regression fixture has a hardcoded `pkg_s24` expectation that must be updated after authority migration.

## Files out of scope

Do not modify:

* backend runtime/evaluator code;
* frontend;
* parser files;
* DTO/report/Gemini/scoring files;
* validators;
* non-regression tests;
* raw Pass 3 research content;
* generated-pilot artefacts;
* compile manifests;
* unrelated Knowledge Bus packages;
* ferritin-low packages;
* TSAT / transferrin saturation policy files;
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Critical prohibitions

Do not:

* invent medical content;
* rewrite medical interpretation meaning;
* approximate missing Pass 3 fields;
* change signal evaluator behaviour;
* introduce new signal IDs;
* split `signal_ferritin_high` into separate runtime signals;
* attach multiple PSI files to `pkg_s24`;
* mix legacy `pkg_s24` schema with modern PSI context;
* alter ferritin-low packages;
* alter TSAT calculated-mode policy;
* edit generated-pilot staged PSI;
* edit compile manifests;
* edit raw Pass 3 research;
* use a fallback parser;
* use global/default reference ranges.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-21-ferritin-high-authority-reconciliation`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-21`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Mandatory authority and naming gate

Before package creation or retirement:

### 1A — hardcoded reference check

Search the repo for:

* `pkg_s24_ferritin_high_overload`
* `KBP-2404`
* `signal_ferritin_high`

Specifically inspect:

* backend Python;
* domain assembler config;
* scoring policy;
* signal evaluator paths;
* Knowledge Bus loaders;
* regression tests;
* package manifests.

If any runtime/backend/scoring path hardcodes `pkg_s24_ferritin_high_overload` or `KBP-2404`, STOP unless the fix is a non-behavioural authority reference update within scope.

Do not modify runtime/evaluator code in this sprint.

### 1B — production package ID naming gate

Resolve the exact target production package IDs before creating directories.

Do not use the staged `pkg_kb52c_*` IDs as final production package IDs unless hardening proves that `pkg_kb52c` is the correct production naming family for ferritin-high.

Preferred naming must follow the repository’s current `pkg_kb*` production naming convention and the P1-20 precedent for resolving staging IDs into production hosts.

Candidate production package IDs must be explicitly recorded in:

`docs/sprints/beta_readiness/P1-21_ferritin_high_promotion_manifest.yaml`

For each proposed ID, record:

* staged source package ID;
* proposed production package ID;
* naming rationale;
* nearest production naming precedent;
* collision check result;
* final decision.

If production naming is ambiguous, STOP before creating packages and classify:

`BLOCKED_PRODUCTION_PACKAGE_ID_NAMING_UNRESOLVED`

### 1C — source hash and staged PSI integrity gate

For both staged candidates:

* read compile manifest;
* confirm PSI source hash;
* confirm `promoted_signal_intelligence_validation: PASS`;
* verify staged PSI SHA256 matches compile manifest expected hash;
* confirm staged PSI has not changed since compilation.

If hash verification fails, STOP for that candidate and classify:

`BLOCKED_MANIFEST_OR_HASH`

Do not edit generated-pilot files.

## Phase 2 — Record authority decision

Create the ADR / decision note.

The ADR must be written before authority migration occurs.

Record Option A as authorised and cite repo evidence.

If hardcoded reference checks or naming checks fail, the ADR may instead record a deferral decision and implementation must stop.

## Phase 3 — Retire legacy `pkg_s24` authority

Retire `knowledge_bus/packages/pkg_s24_ferritin_high_overload` from active production authority.

Preferred method:

* use the repository’s established archive/deprecation pattern if one exists;
* otherwise move the package out of active `knowledge_bus/packages/` into a clearly documented archive/deprecated package location if validation and repo conventions allow;
* if moving directories would break tooling or package enumeration, replace active authority by neutralising/removing the collision only through an explicitly documented, validator-clean deprecation mechanism.

Do not delete history silently.

Do not leave `pkg_s24` claiming active `signal_ferritin_high` authority in `knowledge_bus/packages/`.

After retirement, run the signal authority collision regression test.

If the package cannot be retired cleanly without changing runtime code or breaking validation, STOP and classify:

`BLOCKED_LEGACY_AUTHORITY_RETIREMENT_PATH_UNRESOLVED`

## Phase 4 — Create modern ferritin-high production packages

For each candidate passing Phase 1:

* create the resolved modern production package directory;
* create:

  * `package_manifest.yaml`
  * `research_brief.yaml`
  * `signal_library.yaml`
  * `promoted_signal_intelligence.yaml`

`promoted_signal_intelligence.yaml` must be a byte-copy from the staged generated-pilot PSI.

`signal_library.yaml`, `research_brief.yaml`, and `package_manifest.yaml` may be authored only from governed Pass 3 source and/or validated staged compile artefacts.

Every field must trace to source evidence.

Do not create placeholder thresholds.

Do not invent clinical text.

Do not weaken or merge the two distinct clinical contexts.

Both packages should retain:

`signal_id: signal_ferritin_high`

unless hardening proves this is invalid. Do not create new signal IDs.

## Phase 5 — Validation

Run applicable validation:

* direct PSI validation for both new production PSI files;
* `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<new_package>` for both new packages;
* `python backend/scripts/validate_staged_psi_activation_readiness.py`;
* `python -m pytest backend/tests/regression/test_signal_authority_collision_enforcement.py` or repository-equivalent command.

If a standard Knowledge Bus package validation batch exists, run it as well.

Do not edit validators to make validation pass.

If regression test requires fixture update because `pkg_s24` was retired, update only that regression fixture/test expectation and explain why.

## Phase 6 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-21_pass3_carry_forward.yaml`

Include only unresolved items.

For each unresolved item record:

* item ID;
* package/candidate reference;
* reason not implemented;
* blocker class;
* owner agent;
* launch/beta relevance;
* recommended next package.

Do not re-document unrelated P1-20 CBC items.

Do not include ferritin-low or TSAT unless accidentally encountered and explicitly out of scope.

## Phase 7 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-21_ferritin_high_authority_reconciliation.md`

Keep it concise.

Maximum structure:

1. start state;
2. authority decision;
3. legacy package retirement result;
4. production package creation result;
5. validation result;
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

P1-21 passes only if:

1. `pkg_s24_ferritin_high_overload` authority status is explicitly resolved.
2. ADR / decision note records Option A before implementation.
3. Repo is searched for `pkg_s24_ferritin_high_overload`, `KBP-2404`, and `signal_ferritin_high`.
4. No runtime/backend/scoring hardcoded dependency on `pkg_s24` is left unresolved.
5. Target modern production package IDs are explicitly resolved and recorded before creation.
6. Staged PSI hashes are verified against compile manifests before copy.
7. No generated-pilot files are modified.
8. No raw Pass 3 research is modified.
9. No ferritin-low package is modified.
10. No TSAT calculated-mode policy is modified.
11. No new signal IDs are introduced.
12. `signal_ferritin_high` remains the signal ID for both modern Pass 3 ferritin-high packages.
13. Two modern production packages are created only if naming, hash, source and validation gates pass.
14. `promoted_signal_intelligence.yaml` files are byte-copies from staged artefacts.
15. No medical content is invented.
16. No placeholder thresholds are created.
17. Every changed/new PSI validates.
18. Every changed/new package validates.
19. Signal authority collision regression passes.
20. No runtime/frontend/parser/validator/DTO/Gemini/scoring changes occur.
21. Any regression test edit is limited to reflecting `pkg_s24` retirement and must not weaken collision enforcement.
22. Carry-forward manifest captures unresolved items, if any.
23. Build register is updated concisely.
24. Sprint report is concise.
25. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
