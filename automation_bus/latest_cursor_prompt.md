---
work_id: P1-19
branch: sprint/P1-19-blood-iron-oxygen-kb-production-intelligence
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-19 — Blood/Iron/Oxygen Knowledge Bus Production Intelligence Expansion

You are Cursor, acting as the Knowledge Bus / Medical Intelligence implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is a Knowledge Bus production-intelligence sprint. It is not a runtime sprint, not a frontend sprint, and not a Core Engine sprint.

## Purpose

Promote the newly unblocked blood/iron/oxygen Pass 3-derived PSI cohort into governed production Knowledge Bus artefacts where safe.

This sprint must avoid a single-file opt-in micro-sprint. The work must check the full current `ACTIVATION_READY` cohort and include every safe candidate that can be promoted without crossing STOP gates.

The intended product movement is:

* production PSI opt-in for clean activation-ready packages;
* creation of missing ferritin-high production package hosts where evidence-backed;
* blocker classification for unsafe candidates;
* concise carry-forward of unresolved rich Pass 3 intelligence.

## Baseline

CTRL-01 has adopted the Pre-SOP Prompt Scoping Workflow v0.4.

Stage 0 pipeline advisory identified Sprint 1 as:

`KB61 PSI opt-in + ferritin-high host package`

The advisory also stated that Sprint 1 should check whether any other staged PSI from the former derived-marker cohort is now activation-ready and eligible for the same opt-in pass. If yes, they must be bundled rather than split into micro-sprints.

Stage B Mode 1 advisory returned `AMEND`, not `SPLIT`. The sprint is throughput-justified if it includes:

1. KB61 PSI opt-in;
2. ferritin-high host package creation where safe;
3. all other currently activation-ready staged PSI that can be safely production-opted-in;
4. candidate-level STOP gates for unsafe candidates.

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md` if present
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `docs/sprints/beta_readiness/P1-18_blood_iron_oxygen_pass3_system_activation.md`
* `docs/sprints/beta_readiness/P1-18_pass3_system_activation_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-17_core_backend_handoff_manifest.yaml`
* `docs/sprints/beta_readiness/P1-17_blocker_resolution_manifest.yaml`
* `docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml`
* `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
* `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md`
* `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
* `knowledge_bus/schema/package_manifest_schema.yaml`
* `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml`
* `backend/scripts/validate_knowledge_package.py`
* `backend/scripts/validate_promoted_signal_intelligence.py`
* `backend/scripts/validate_staged_psi_activation_readiness.py`

Use targeted search:

* `rg "transferrin_high|ferritin_high|iron_overload|inflammatory_hyperferritinemia|iron_deficiency_transport" knowledge_bus docs backend`
* `rg "pkg_kb61|pkg_kb52c_ferritin_high|pkg_s24_ferritin_high_overload" knowledge_bus docs`
* `rg "ACTIVATION_READY|activation_ready_count|BLOCKED_MEDICAL_REVIEW_REQUIRED|FRAME_AUTHORITY|BLOCKED_PACKAGE_IDENTITY" docs/sprints/beta_readiness`
* `rg "promoted_signal_intelligence" knowledge_bus/packages docs/sprints/beta_readiness`
* `rg "white_blood_cells|crp|ferritin|transferrin_saturation|transferrin|iron" backend/ssot knowledge_bus docs`

Inspect relevant hits before editing.

## Files in scope

Allowed if justified:

* `docs/sprints/beta_readiness/P1-19_blood_iron_oxygen_kb_production_intelligence.md`
* `docs/sprints/beta_readiness/P1-19_production_opt_in_manifest.yaml`
* `docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `knowledge_bus/packages/<safe_candidate>/package_manifest.yaml`
* `knowledge_bus/packages/<safe_candidate>/research_brief.yaml`
* `knowledge_bus/packages/<safe_candidate>/signal_library.yaml`
* `knowledge_bus/packages/<safe_candidate>/promoted_signal_intelligence.yaml`

## Files out of scope

Do not modify:

* `backend/`
* `frontend/`
* runtime loaders
* parser files
* DTO/report/Gemini/scoring files
* tests
* validators
* raw Pass 3 research content except read-only evidence inspection
* generated pilot PSI except read-only evidence inspection
* existing production package `signal_library.yaml` files
* existing production package `research_brief.yaml` files
* existing production medical content
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Critical prohibitions

Do not:

* invent medical content;
* infer missing medical logic from general clinical knowledge;
* water down Pass 3 research;
* simplify signal conditions to make package creation easier;
* change thresholds, activation logic, modifiers, contradiction logic, evidence strength, supporting-marker relationships or interpretation meaning unless those values are directly traced to governed Pass 3 source;
* edit raw Pass 3 research;
* edit generated-pilot staged PSI content;
* cross-place PSI into a package with a different `package_id`;
* opt in medical-review-blocked candidates;
* opt in frame-authority-blocked candidates;
* create duplicate active medical authority;
* create thin placeholder packages;
* alter runtime behaviour;
* alter frontend presentation;
* alter validators or tests.

## Signal-library rule

Existing production packages:

* Do not edit `signal_library.yaml` in any existing production package.
* Do not edit `research_brief.yaml` in any existing production package.
* Do not alter existing signal logic.

New production package creation:

* Permitted only for candidates explicitly cleared by STOP gates.
* For newly created production packages, `signal_library.yaml`, `research_brief.yaml`, and `package_manifest.yaml` may be authored only from governed Pass 3 source and/or validated staged compile artefacts.
* Every signal condition, threshold, supporting marker, contradiction marker, modifier and context rule must trace to a cited field in the source Pass 3 investigation spec or validated compiled artefact.
* If any required field is missing, thin, ambiguous or non-deterministic, STOP for that candidate.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-19-blood-iron-oxygen-kb-production-intelligence`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-19`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Establish current activation-ready cohort

Run:

`python backend/scripts/validate_staged_psi_activation_readiness.py`

Capture the full list of `ACTIVATION_READY` package IDs.

Do not rely only on previous sprint reports.

Create:

`docs/sprints/beta_readiness/P1-19_production_opt_in_manifest.yaml`

For each `ACTIVATION_READY` candidate record:

* candidate package ID;
* staged PSI path;
* staged compile manifest path;
* source spec ID;
* source path;
* signal ID;
* primary biomarker;
* production package host status;
* production package path if present;
* production package ID;
* PSI internal package ID;
* current blocker class if any;
* opt-in decision;
* validation result;
* carry-forward owner if not promoted.

Allowed decisions:

* `OPT_IN_EXISTING_HOST`
* `CREATE_HOST_AND_OPT_IN`
* `ALREADY_OPTED_IN`
* `BLOCKED_MISSING_PRODUCTION_HOST`
* `BLOCKED_DUPLICATE_AUTHORITY_RISK`
* `BLOCKED_INSUFFICIENT_PASS3_SOURCE`
* `BLOCKED_BIOMARKER_IDENTITY_UNRESOLVED`
* `BLOCKED_MEDICAL_REVIEW_REQUIRED`
* `BLOCKED_FRAME_AUTHORITY_UNRESOLVED`
* `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`
* `BLOCKED_REQUIRES_CORE_BACKEND_AGENT`
* `BLOCKED_VALIDATION_FAILURE`
* `OUT_OF_SCOPE_FOR_P1_19`

## Phase 2 — Existing-host opt-in pass

For each `ACTIVATION_READY` candidate:

1. Check whether an ID-matched production host exists under `knowledge_bus/packages/`.
2. Confirm production package manifest `package_id` matches PSI internal `package_id`.
3. Confirm no medical-review blocker applies.
4. Confirm no frame-authority blocker applies.
5. Confirm no package-identity blocker applies.
6. Confirm PSI validates.
7. Confirm package validates.

If all pass:

* copy or install production `promoted_signal_intelligence.yaml` from staged PSI;
* update `package_manifest.yaml` to opt in:
  `promoted_signal_intelligence: promoted_signal_intelligence.yaml`;
* preserve `behavioural_impact` and existing manifest semantics;
* classify as `OPT_IN_EXISTING_HOST`.

If any condition fails, STOP for that candidate and classify.

Expected named candidate:

* `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation`

Do not stop after KB61. Continue through the full activation-ready cohort.

## Phase 3 — Ferritin-high production host package gate

This phase applies only to:

* `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`
* `pkg_kb52c_ferritin_high_iron_overload_context`

These candidates may proceed only if all gates below pass.

### Gate 3A — Production-host absence

Confirm no ID-matched production package host already exists for each candidate.

If an ID-matched production host exists, use the existing-host opt-in path instead.

### Gate 3B — Duplicate-authority check

Before creating either package, inspect:

`knowledge_bus/packages/pkg_s24_ferritin_high_overload/`

**Step 1 — signal_id collision check:**

Read `pkg_s24_ferritin_high_overload/signal_library.yaml` and identify every `signal_id` defined there.

For each proposed ferritin-high candidate, confirm that its `signal_id` (from the staged PSI) does not already exist in any production `signal_library.yaml` under `knowledge_bus/packages/`.

If a collision exists:

* STOP for that candidate;
* do not create the package;
* classify as `BLOCKED_DUPLICATE_AUTHORITY_RISK`;
* record the colliding package and signal_id.

Do not proceed to Gate 3D if a signal_id collision is found, regardless of clinical scope distinction.

**Step 2 — clinical and authority scope check:**

Compare the proposed ferritin-high candidate scope against `pkg_s24_ferritin_high_overload`.

If there is overlap, duplicate medical authority, conflicting signal logic, or unclear authority boundary:

* STOP for that candidate;
* do not create the package;
* classify as `BLOCKED_DUPLICATE_AUTHORITY_RISK`;
* record the specific overlap risk.

If scopes are clinically and architecturally distinct, proceed.

Do not make unsupported clinical assertions to justify distinction.

### Gate 3C — Pass 3 source sufficiency

For each ferritin-high candidate, inspect the source Pass 3 / investigation spec evidence cited by the staged compile manifest.

Known expected source IDs:

* `inv_ferritin_high_inflammatory_hyperferritinemia`
* `inv_ferritin_high_iron_overload_context`

Confirm the source provides sufficient governed evidence for:

* package identity;
* signal ID;
* primary biomarker;
* trigger direction;
* signal conditions;
* thresholds or lab-range logic;
* supporting markers;
* contradiction markers;
* context modifiers;
* evidence/rationale required by `research_brief.yaml`;
* package manifest fields;
* any biomarker IDs used, including `white_blood_cells` and `crp` where applicable.

Also confirm all biomarker IDs are SSOT-canonical.

If source is thin, ambiguous, missing required fields, or requires approximation:

* STOP for that candidate;
* classify as `BLOCKED_INSUFFICIENT_PASS3_SOURCE`;
* do not create the production package;
* do not fill gaps.

### Gate 3D — Deterministic package creation

If Gates 3A–3C pass, create production package host:

* `knowledge_bus/packages/pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia/`
* `knowledge_bus/packages/pkg_kb52c_ferritin_high_iron_overload_context/`

Create only:

* `package_manifest.yaml`
* `research_brief.yaml`
* `signal_library.yaml`
* `promoted_signal_intelligence.yaml`

Every field must trace to governed source or validated staged artefacts.

Do not create placeholder text.

Do not create broad generic ferritin-high interpretation.

Do not alter `pkg_s24_ferritin_high_overload`.

Validate each new package and PSI.

If validation fails and the fix would require medical content invention, revert/exclude that candidate and classify as `BLOCKED_VALIDATION_FAILURE`.

## Phase 4 — Blocked candidates

The following must remain blocked unless repository evidence proves a same-ID, non-medical, validation-clean path:

CBC KB-S52c versus KB-S58 package-identity candidates:

* `pkg_kb52c_rbc_high_erythrocytosis_pattern`
* `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern`
* `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis`
* `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern`

Do not cross-place PSI into `pkg_kb58_*`.

If same-ID provenance is not resolved, classify as:

`BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`

Iron Batch C medical-review/frame-authority candidates must remain blocked unless already formally cleared by repo evidence before this sprint:

* `BLOCKED_MEDICAL_REVIEW_REQUIRED`
* `BLOCKED_FRAME_AUTHORITY_UNRESOLVED`

Do not clear medical-review or frame-authority blockers inside this Knowledge Bus sprint.

## Phase 5 — Validation

Run applicable validation for every changed package and PSI.

Required:

* direct PSI validation for every newly installed production PSI;
* `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<package>` for every changed or newly created package;
* `python backend/scripts/validate_staged_psi_activation_readiness.py`
* `pytest backend/tests/regression/test_signal_authority_collision_enforcement.py` — mandatory regression target if any new production `signal_library.yaml` was created.

If the repository has a standard package-validation batch command, use it as well.

Do not edit validators to make validation pass.

## Phase 6 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-19_pass3_carry_forward.yaml`

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

At minimum, carry forward:

* duplicate-authority blocked ferritin-high candidates, if any;
* insufficient-source ferritin-high candidates, if any;
* missing-production-host activation-ready candidates, if any;
* CBC KB-S52c versus KB-S58 unresolved identity candidates;
* iron Batch C medical-review/frame-authority candidates;
* TSAT calculated mode if encountered, but do not expand its scope.

## Phase 7 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-19_blood_iron_oxygen_kb_production_intelligence.md`

Keep it concise.

Maximum structure:

1. start state;
2. activation-ready cohort;
3. production opt-ins completed;
4. production packages created;
5. candidates blocked and why;
6. validation results;
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

P1-19 passes only if:

1. Current activation-ready cohort is regenerated at sprint start.
2. Every activation-ready candidate is adjudicated.
3. Every safe existing-host candidate is opted in.
4. KB61 is opted in if still activation-ready and ID-clean.
5. Ferritin-high production host creation is attempted only through the STOP gates.
6. No ferritin-high package is created if `pkg_s24_ferritin_high_overload` creates duplicate-authority risk.
7. No ferritin-high package is created from thin or ambiguous Pass 3 source.
8. No medical content is invented.
9. No cross-ID PSI placement occurs.
10. No generated-pilot content is edited.
11. No raw Pass 3 research content is edited.
12. No existing production `signal_library.yaml` files are edited.
13. No backend, frontend, validator, test, runtime, parser, DTO, Gemini or scoring files are modified.
14. No medical-review or frame-authority blocked candidate is opted in.
15. Every changed/new PSI validates.
16. Every changed/new package validates.
17. Staged activation-readiness validator runs successfully after changes.
18. Carry-forward manifest captures unresolved rich Pass 3 content with owner and blocker class.
19. Build register is updated concisely.
20. Sprint report is concise.
21. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason` per CTRL-01 adoption.

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
