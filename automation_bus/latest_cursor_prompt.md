---
work_id: P2-4
branch: feature/p2-4-narrativepayload-brief-hardening
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: BEHAVIOUR
---

# P2-4 — NarrativePayload Brief Hardening

You are Cursor, acting as Core Engine implementation agent under Automation Bus SOP v1.3.1.

This is a HIGH-risk BEHAVIOUR sprint.

This sprint audits and hardens `NarrativePayloadV1` v1.1 as the governed B→C brief contract required before future Gemini narrative activation.

Do not run another advisory.

## Sprint purpose

P2-4 must confirm that the NarrativePayload contract is sufficient to govern future constrained Gemini narrative generation.

It must verify and, only where necessary, harden:

1. section intents;
2. slot definitions;
3. anti-hallucination constraints;
4. claim-boundary / evidence-boundary fields;
5. field completeness for the currently active Wave 1 domains;
6. compatibility with the prose substrate delivered in P2-1 and P2-2+P2-3.

This sprint does not activate Gemini.

## Product output

At completion:

* `NarrativePayloadV1` is confirmed or hardened as the safe Layer B→Layer C brief contract.
* The contract can carry sufficient governed structure for future Gemini wording/presentation.
* Tests prove that the contract supports active Wave 1 prose substrate needs.
* Tests prove anti-hallucination / no-invention constraints are present and enforceable at the contract level.
* A sprint report records whether the contract changed or was confirmed sufficient as-is.

## Controlling advisory

Use `automation_bus/latest_pipeline_advisory.md` as sequencing authority.

Key advisory facts:

* P2-2+P2-3 is complete.
* Retail explainer coverage is now 40/~79 biomarkers.
* Pathway entries are now 5.
* Missing-marker entries are bootstrapped.
* Layer B prose substrate is now deep enough for P2-4.
* P2-4 is the next programme unlock.
* P2-4 must complete before P4-1/P4-2 Gemini activation.
* Gemini remains inactive.
* CEO approval is required before Gemini narrative is enabled in production.

## Files in scope

Expected primary file:

* `backend/core/contracts/narrative_payload_v1.py`

Expected tests:

* existing NarrativePayload contract tests, if present;
* new or updated P2-4 tests under the current backend test convention.

Expected documentation / sprint artefacts:

* `docs/sprints/beta_readiness/P2-4_narrativepayload_brief_hardening_manifest.yaml`
* `docs/sprints/beta_readiness/P2-4_narrativepayload_brief_hardening_completion.md`
* `docs/sprints/beta_readiness/P2-4_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Read-only reference files may include:

* `backend/core/contracts/narrative_report_v1.py`
* `backend/core/analytics/narrative_payload_builder_v1.py`
* `backend/core/analytics/narrative_report_compiler_v1.py`
* `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
* `backend/core/analytics/narrative_brief_enforcement_v1.py`
* P2-1 completion artefacts
* P2-2+P2-3 completion artefacts
* ADR_WP2 Layer B / Layer C contract authority

Do not modify read-only reference files unless Stage D hardening returns `REJECT_AND_RETURN` and GPT explicitly expands scope.

## Files out of scope

Do not modify:

* Gemini activation files;
* Gemini prompt templates;
* frontend files;
* report redesign files;
* signal activation files;
* scoring policy files;
* `domain_score_assembler.py`;
* `signal_evaluator.py`;
* parser files;
* questionnaire files;
* retail explainer registry files;
* pathway explainer files;
* missing-marker explainer files;
* production PSI package files;
* compiled card files;
* frame-level routing files;
* P2-FRAME-ROUTING-ARCHITECTURE-1 files;
* WBC / lymphocyte / neutrophil files;
* calculated TSAT files;
* `.codex/`;
* `.cursor/`;
* `.vscode/`;
* `AGENTS.md`.

If any out-of-scope file appears necessary, STOP and return to GPT.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`feature/p2-4-narrativepayload-brief-hardening`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P2-4`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed.
6. Confirm P2-2+P2-3 is merged.
7. Confirm no advisory or fork/background agent is running for this sprint.

STOP if preflight fails.

## Phase 1 — Authority and contract verification

Read the minimum necessary files to verify:

1. current `NarrativePayloadV1` structure;
2. existing section intents;
3. existing slot / field definitions;
4. existing anti-hallucination constraints;
5. evidence / claim boundary fields;
6. how `NarrativePayloadV1` is consumed by current Layer C compiler/report assembly;
7. whether P2-1 and P2-2+P2-3 prose substrate outputs are representable without contract gaps.

Required authority:

* ADR_WP2 Layer B / Layer C contract path;
* latest pipeline advisory;
* P2-1 completion report;
* P2-2+P2-3 completion report.

Do not perform broad repo discovery.

## Phase 2 — Gap assessment

Assess whether `NarrativePayloadV1` already supports:

* retail summary intent;
* lead narrative intent;
* body overview intent;
* next steps narrative intent;
* clinician synthesis intent;
* active Wave 1 domain representation;
* source provenance;
* claim boundaries;
* evidence boundaries;
* prohibited claim patterns;
* LLM translation constraints;
* missing-marker caution context;
* no-diagnosis / no-treatment constraints;
* future Gemini presentation-only use.

If the current contract is sufficient, make no contract change. Strengthen tests and close the sprint as “contract confirmed sufficient”.

If the current contract is insufficient, make the smallest necessary contract hardening change.

STOP if the gap requires:

* Gemini activation;
* frontend change;
* report schema redesign;
* payload builder redesign;
* claim-boundary engine redesign;
* signal activation change;
* scoring change;
* routing architecture change.

## Phase 3 — Contract hardening

If changes are required, modify only:

* `backend/core/contracts/narrative_payload_v1.py`

Allowed changes may include:

* clarifying section intent fields;
* adding or tightening brief-slot definitions;
* strengthening LLM translation constraints;
* strengthening prohibited claim / anti-hallucination boundary fields;
* adding missing provenance or source-boundary fields if required by the existing architecture;
* adding documentation comments / typed model constraints consistent with repo style.

Do not change runtime signal logic.

Do not activate Gemini.

Do not create free-text generation behaviour.

Do not weaken any existing safety boundary.

## Phase 4 — Tests

Create or update tests proving:

* `NarrativePayloadV1` contains all required section intents;
* brief slots are present and deterministic;
* provenance / evidence boundary fields are present;
* anti-hallucination / no-invention constraints are present;
* prohibited claim patterns or equivalent guard fields are present;
* future Gemini use is constrained to wording/presentation and cannot create medical meaning;
* active Wave 1 domains can be represented;
* missing-marker caution context can be represented where applicable;
* existing Layer C compiler/report assembly consumers still accept the contract;
* no Gemini activation path is enabled.

If contract unchanged, tests must prove sufficiency rather than merely asserting no change.

## Phase 5 — Carry-forward management

Create:

`docs/sprints/beta_readiness/P2-4_carry_forward.yaml`

Record:

* whether `NarrativePayloadV1` was changed or confirmed sufficient;
* any deferred Gemini activation requirement;
* CEO approval remains required before Gemini narrative activation;
* P4-1/P4-2 status after P2-4;
* P2-FRAME-ROUTING-ARCHITECTURE-1 remains deferred;
* any contract gaps deferred because they require broader architecture;
* any tests or validators still needed before Gemini.

## Phase 6 — Completion report and build register

Create:

`docs/sprints/beta_readiness/P2-4_narrativepayload_brief_hardening_completion.md`

Keep concise.

Maximum structure:

1. start state;
2. authority reviewed;
3. contract sufficiency assessment;
4. changes made, if any;
5. validation result;
6. Gemini readiness impact;
7. carry-forwards;
8. recommended next sprint.

Create:

`docs/sprints/beta_readiness/P2-4_narrativepayload_brief_hardening_manifest.yaml`

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight.

## Validation

Run all relevant validation.

At minimum:

* NarrativePayload contract tests;
* Layer C report / compiler consumer regression tests, if present;
* claim-boundary / anti-hallucination tests, if present;
* P2-1 and P2-2+P2-3 relevant prose substrate regressions, if affected;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to force a pass.

## Acceptance criteria

P2-4 passes only if:

1. Front matter remains `risk_level: HIGH`, `change_type: BEHAVIOUR`, unless Stage D returns `REJECT_AND_RETURN` with a lower-risk evidence-only closure path.
2. Automation Bus preflight passes.
3. `NarrativePayloadV1` is either hardened or explicitly confirmed sufficient with test evidence.
4. Section intents are present and tested.
5. Brief slots are present and tested.
6. Evidence/provenance boundary fields are present and tested.
7. Anti-hallucination / no-invention constraints are present and tested.
8. Future Gemini use remains constrained to wording/presentation only.
9. No Gemini activation occurs.
10. No frontend files are modified.
11. No signal activation, scoring, domain assembler, signal evaluator, parser, questionnaire, retail explainer, pathway explainer, missing-marker, compiled card or production PSI files are modified.
12. Existing Layer C consumers remain compatible.
13. Active Wave 1 domains can be represented by the contract.
14. Missing-marker caution context can be represented where applicable.
15. Carry-forward records Gemini activation prerequisites and CEO approval requirement.
16. Build register is updated concisely.
17. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
