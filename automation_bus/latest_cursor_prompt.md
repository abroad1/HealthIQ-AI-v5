---
work_id: P1-18
branch: sprint/P1-18-blood-iron-oxygen-pass3-system-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-18 — Blood/Iron/Oxygen Pass 3 System Activation Pack

You are Cursor, acting as the Core Engine implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is a product-forward build sprint, not a clean-up/adjudication sprint.

## Agent assignment

Primary agent: Core Engine agent.

Reason:

* this sprint targets backend system/subsystem firing;
* it may touch runtime/domain/subsystem/activation/test logic;
* it must not be assigned to the Medical Intelligence / Knowledge Bus agent.

Knowledge Bus artefacts are source inputs and validation references. Do not rewrite medical intelligence content unless explicitly allowed by a STOP gate. If missing medical artefacts are discovered, classify and carry forward rather than inventing content.

## Purpose

Move HealthIQ AI from governed Pass 3-derived artefacts toward working runtime capability by making the blood/iron/oxygen system/subsystems fire correctly from existing governed intelligence.

This sprint must:

1. inspect the existing `wave1_blood_iron_oxygen` implementation;
2. identify how current domain/subsystem firing uses, or fails to use, governed signal packages;
3. wire or correct runtime activation where existing governed signal_library/package assets are already sufficient;
4. resolve the core-engine side of the `transferrin_saturation` blocker if it is a backend/validator/runtime-policy issue;
5. add representative backend tests proving medically credible firing behaviour;
6. update the build register and carry forward any unresolved Knowledge Bus or medical-review work.

Do not water down Pass 3 research because implementation is difficult. If a rich Pass 3-derived signal, edge case, lifestyle modifier, drug-category modifier, contradiction, or supporting-marker relationship cannot yet be implemented safely, document it as a carry-forward with owner and blocker reason.

## Strategic constraints

HealthIQ AI’s differentiator is deterministic, medically rich blood-panel analysis.

Do not reduce this to generic high/low marker commentary.

The accepted architecture is:

`investigation_spec / Pass 3 research -> governed compile -> package triple + optional PSI + hypothesis artefact + card evidence artefact -> thin runtime loaders -> DTOs -> frontend render-only`

In this sprint:

* `signal_library.yaml` is the deterministic firing mechanism.
* package manifests and research briefs provide package governance/traceability.
* PSI provides optional signal-layer semantics.
* compiled hypotheses / root-cause and card evidence provide richer WHY/subsystem explanation where available.
* frontend remains out of scope.

## Current baseline

From the build register:

* P1-3 implemented `wave1_blood_iron_oxygen` with compiled oxygen-carrying subsystem evidence, routing, narrative copy, replay contract and targeted tests.
* P1-3 carried forward launch-visible CBC / iron signal wiring pending frame adjudication.
* P1-9 confirmed a large unpromoted tail between Pass 3 research and runtime-visible surfaces.
* P1-10 to P1-12 staged Pass 3-derived PSI batches.
* P1-14 locked the staged PSI cohort: 22 activation-ready and 19 blocked.
* P1-15 and P1-16 moved 22 staged PSI artefacts into production package opt-in.
* P1-17 confirmed 7 transferrin-saturation / iron-panel candidates require Core Engine ownership before Knowledge Bus opt-in can safely proceed.

P1-18 must now build capability, not merely classify blockers.

## Mandatory files to read before editing

Read:

* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
* docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
* docs/sprints/beta_readiness/P1-17_core_backend_handoff_manifest.yaml
* docs/sprints/beta_readiness/P1-17_remaining_psi_blocker_resolution.md
* docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml
* docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
* docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
* docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md

Then discover actual runtime files with targeted search. Do not assume paths.

Use:

* `rg "wave1_blood_iron_oxygen|blood_iron_oxygen|oxygen" backend docs knowledge_bus`
* `rg "transferrin_saturation" backend knowledge_bus docs`
* `rg "DERIVED_MARKER_IDS" backend docs`
* `rg "signal_library" backend/core backend/scripts backend/tests`
* `rg "SignalRegistry|SignalEvaluator|activation_key|source_spec_id" backend`
* `rg "domain assembler|domain_score|subsystem" backend/core backend/tests`

Read the relevant implementation files before editing.

## Files in scope

Allowed if required and justified:

* backend/core/**/*
* backend/tests/**/*
* backend/scripts/validate_staged_psi_activation_readiness.py
* docs/sprints/beta_readiness/P1-18_blood_iron_oxygen_pass3_system_activation.md
* docs/sprints/beta_readiness/P1-18_pass3_system_activation_carry_forward.yaml
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

Read-only unless STOP gate permits otherwise:

* knowledge_bus/packages/**/*
* knowledge_bus/schema/**/*
* backend/ssot/biomarkers.yaml

Do not edit Knowledge Bus medical content in this sprint unless the change is strictly non-medical metadata needed for runtime integration and is explicitly justified. Prefer handoff/carry-forward for Knowledge Bus content changes.

## Files out of scope

Do not modify:

* frontend/**/*
* Gemini files
* user-facing prose templates
* raw Pass 3 / investigation research files under `knowledge_bus/research/`
* generated pilot PSI under `knowledge_bus/generated_pilot/`
* scoring policy unless the discovered runtime path proves it is directly required for blood/iron/oxygen firing and the change is not medical-content improvisation
* package medical content, thresholds, activation logic, interpretation text or evidence strength
* automation_bus/latest_gate_evidence.json
* automation_bus/latest_gate_output.txt

Do not allow tooling files into the sprint branch:

* .codex/
* .cursor/
* .vscode/
* AGENTS.md

## Critical prohibitions

Do not:

* water down Pass 3 research;
* replace rich Pass 3-derived logic with generic high/low commentary;
* invent medical content;
* create fallback or dummy parsers;
* use global/default reference ranges where lab ranges are required;
* change lab-range interpretation policy;
* compute derived markers unless a governed policy exists or is safely implemented in this sprint with tests;
* make frontend infer medical meaning;
* read raw Pass 3 research at runtime;
* silently ignore edge cases because implementation is hard;
* alter medical thresholds, evidence strength, contradiction logic, override logic or interpretation text without medical authority;
* edit Knowledge Bus generated-pilot artefacts;
* cross-place PSI into mismatched package IDs.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-18-blood-iron-oxygen-pass3-system-activation`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm token has `work_id: P1-18`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Runtime reality map

Create a concise runtime map in:

* docs/sprints/beta_readiness/P1-18_blood_iron_oxygen_pass3_system_activation.md

Document:

* current `wave1_blood_iron_oxygen` domain/subsystem entry points;
* current tests/replay coverage;
* current signal package / signal_library consumption path;
* whether existing package signals are actually evaluated for this system;
* whether PSI is runtime-dead or validation-only in this path;
* where transferrin_saturation is blocked;
* what existing package/PSI/card evidence assets are available;
* what is missing.

This section must be evidence-backed from actual files.

## Phase 2 — Select build target inside blood/iron/oxygen

Select the highest-value safe build target from current repo evidence.

Preferred target order:

1. transferrin / iron transport subsystem firing, if core-engine blocker is resolvable;
2. CBC oxygen-carrying / anaemia-related subsystem firing, if package identity blockers do not prevent safe runtime use;
3. existing implemented `wave1_blood_iron_oxygen` subsystem enrichment using already-valid package signals;
4. replay/test harness proving existing system firing against representative panels, if runtime wiring already exists but is under-tested.

Do not select a target that requires medical-review-blocked content.

### STOP gate 1 — Build target safety

STOP or narrow scope if the chosen target requires:

* new medical authority;
* Knowledge Bus package creation;
* hand-authored medical content;
* frontend changes;
* raw Pass 3 runtime reads;
* global/default reference ranges;
* unresolved package identity decisions;
* medical-review-blocked signals.

If STOP fires for one target, try the next safe target. Do not collapse the sprint into a report-only output unless all safe targets fail.

## Phase 3 — Core-engine derived-marker policy for transferrin_saturation

Inspect the actual backend handling of `transferrin_saturation`.

Decide whether the issue is:

A. `transferrin_saturation` is lab-provided and SSOT-canonical, but incorrectly hard-blocked by validation policy;
B. `transferrin_saturation` must be calculated from other markers before runtime use;
C. both lab-provided and calculated modes exist and need separate handling;
D. the correct policy cannot be safely resolved in this sprint.

Allowed implementation:

* If `transferrin_saturation` is SSOT-canonical and lab-provided values are already accepted by the runtime input model, update only the backend validator/runtime policy needed to stop incorrectly blocking lab-provided `transferrin_saturation`.
* Add tests proving lab-provided `transferrin_saturation` is accepted only when present as a real input marker.
* If calculation is required when absent, implement only if a governed existing formula/policy is already present and safe; otherwise classify as carry-forward.

### STOP gate 2 — Derived-marker safety

STOP before implementation if resolution requires:

* inventing a formula;
* calculating without a governed policy;
* using global/default reference ranges;
* changing medical interpretation;
* changing lab-range policy;
* changing Knowledge Bus medical content;
* creating or modifying Pass 3 research;
* frontend/DTO/Gemini changes.

If calculation mode is unsafe, still implement lab-provided mode if safe and useful.

## Phase 4 — Runtime activation / subsystem firing implementation

Implement the selected safe build target.

Expected implementation may include:

* correcting backend system/subsystem wiring so existing governed signal_library/package signals are evaluated;
* ensuring activation_key/source_spec_id/package_id provenance is preserved where the runtime already supports it;
* ensuring blood/iron/oxygen domain/subsystem output reflects actual fired signals rather than static card presence;
* adding backend tests for representative blood panels.

Tests must include at least:

1. normal/control panel where the subsystem does not falsely fire;
2. a panel that should trigger the selected blood/iron/oxygen signal/subsystem;
3. a missing-marker or partial-panel case that fails safely;
4. if transferrin_saturation is implemented, a lab-provided transferrin_saturation case.

Do not change user-facing frontend behaviour.

### STOP gate 3 — Runtime safety

STOP or narrow implementation if:

* signal firing requires unresolved Knowledge Bus content;
* multiple plausible frames exist and runtime cannot distinguish them safely;
* package identity is ambiguous;
* medical-review-blocked content would be needed;
* tests cannot prove safe behaviour;
* implementation would silently alter unrelated domains.

## Phase 5 — Carry-forward manifest

Create:

* docs/sprints/beta_readiness/P1-18_pass3_system_activation_carry_forward.yaml

Record every relevant Pass 3-derived item discovered but not implemented.

For each item record:

* item ID;
* source / package / PSI reference;
* what rich medical information is at risk of being lost;
* why it was not implemented;
* owner agent:

  * Core Engine
  * Knowledge Bus
  * Medical Review
  * Frontend/Presentation
* blocker class;
* launch/beta relevance:

  * launch-critical
  * beta-critical
  * deferred
* recommended future package.

This manifest is mandatory. It prevents rich Pass 3 content being dropped because it is difficult.

## Phase 6 — Validation

Run relevant tests and validators discovered from the repo.

Minimum required:

* targeted backend tests for modified runtime/system/subsystem files;
* any existing tests covering `wave1_blood_iron_oxygen`;
* any existing tests covering SignalRegistry/SignalEvaluator behaviour if touched;
* staged PSI activation-readiness validator if derived-marker policy was changed;
* package/Knowledge Bus validators only if Knowledge Bus package files were changed.

Do not edit tests merely to make weak behaviour pass.

## Phase 7 — Sprint report and build register

Complete:

* docs/sprints/beta_readiness/P1-18_blood_iron_oxygen_pass3_system_activation.md

The report must include:

1. runtime reality map;
2. selected build target and why;
3. what was implemented;
4. what Pass 3-derived intelligence now fires or is better represented;
5. transferrin_saturation policy decision if addressed;
6. tests and validation results;
7. explicit statement that Pass 3 richness was not watered down;
8. carry-forwards and agent ownership;
9. recommended next outcome-based build package.

Update:

* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

Keep the register entry lightweight.

## Acceptance criteria

P1-18 passes only if:

1. It delivers actual backend/runtime/system/subsystem capability, unless every candidate target hits a documented STOP gate.
2. Current blood/iron/oxygen runtime firing path is mapped from actual repo evidence.
3. At least one safe system/subsystem firing improvement or test-backed runtime correction is implemented.
4. Representative backend tests are added or updated.
5. No Pass 3-derived richness is silently discarded.
6. Carry-forward manifest exists and classifies unimplemented rich medical content.
7. No raw Pass 3 research is read at runtime.
8. No frontend medical inference is introduced.
9. No Knowledge Bus medical content is invented or watered down.
10. No global/default reference ranges are introduced.
11. No medical-review-blocked content is activated.
12. Any transferrin_saturation change is limited to safe core-engine policy/runtime handling and is test-backed.
13. All modified runtime tests pass.
14. Build register is updated.
15. Final report recommends the next outcome-based build package.

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

* `python backend/scripts/run_work_package.py finish`

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.

