---
work_id: P2-1
branch: feature/prose-substrate-wave1-wired
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: MIXED
---

# P2-1 — Prose Substrate Wave 1 Wired

You are Cursor, acting as a combined Core Engine + Knowledge Bus implementation agent under Automation Bus SOP v1.3.1.

This is a HIGH-risk MIXED sprint.

This sprint delivers the first runtime-reachable governed prose substrate for newly activated Wave 1 signals by wiring bounded Layer C pathway selection for iron and thyroid signals and authoring the associated Knowledge Bus pathway / functional interpretation YAML content.

## Controlling scoping decisions

Use the completed P2-1 scope advisory and STOP-1 verification as current scoping authority.

Material findings:

* Layer C infrastructure already exists.
* `NarrativePayloadV1`, `NarrativeReportV1`, `compile_narrative_report_v1()`, `narrative_compiler_lc_s3_assembly_v1.py`, `narrative_payload_builder_v1.py`, and claim-boundary enforcement already exist.
* P2-1 is not a greenfield Layer C infrastructure build.
* The compiler currently uses a two-slot model:

  * one lead pathway block;
  * one secondary pathway block.
* Runtime inclusion is controlled by `_LEAD_SIGNAL_HINTS` and `_SECONDARY_SIGNAL_HINTS`.
* These signal-hint sets are duplicated in:

  * `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
  * `backend/core/analytics/narrative_report_compiler_v1.py`
* The current lead hint set covers homocysteine / MCV.
* The current secondary hint set covers lipid signals.
* Iron and thyroid signals are not currently wired into the lead hint set.
* The payload path does not provide richer routing than the legacy path; it uses the same signal-hint mechanism.
* Therefore, runtime-reachable P2-1 prose requires bounded Python behaviour changes.

## Sprint purpose

Deliver a bounded, runtime-reachable prose substrate by:

1. Extending existing lead signal hint sets to include newly activated iron and thyroid signals.
2. Adding Knowledge Bus interpretation entity entries for iron and thyroid.
3. Adding pathway explainer YAML content for iron and thyroid.
4. Adding functional interpretation YAML content for iron and thyroid.
5. Preserving existing homocysteine lead routing.
6. Preserving existing lipid secondary routing.
7. Testing that iron and thyroid signals now trigger lead pathway prose.
8. Explicitly deferring frame-level routing and full multi-domain simultaneous prose.

## Product output

After P2-1:

* `signal_iron_low` can trigger a governed lead prose block.
* `signal_iron_high` can trigger a governed lead prose block.
* `signal_free_t3_low` can trigger a governed lead prose block.
* `signal_tpo_ab_high` can trigger a governed lead prose block.
* Existing homocysteine lead prose behaviour still works.
* Existing lipid secondary prose behaviour still works.
* The compiler returns valid `NarrativeReportV1` output with governed pathway / functional prose for the newly wired signal families when they are selected as the lead finding.
* No frontend work is required.
* No Gemini work is required.
* No new medical meaning is invented outside governed PSI / package / card evidence.

## Important limitation

P2-1 does not solve frame-level prose routing.

Explicitly out of scope:

* distinguishing `signal_iron_low` absolute deficiency frame from functional inflammatory restriction frame at compiler-routing level;
* distinguishing `signal_homocysteine_high` B-vitamin frame from renal-clearance frame at compiler-routing level;
* simultaneous prose blocks for all 6 domains;
* more than one lead block;
* routing redesign;
* changing entity-loop semantics;
* adding per-frame signal identity;
* changing ranking/scoring or top-finding selection.

If frame-level routing is required, record a future carry-forward:

`P2-FRAME-ROUTING-ARCHITECTURE-1`

## Files in scope

### Behaviour — Core Engine / Layer C assembly

Only these Python files may be modified:

* `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
* `backend/core/analytics/narrative_report_compiler_v1.py`

Allowed changes only:

* extend `_LEAD_SIGNAL_HINTS` with:

  * `signal_iron_low`
  * `signal_iron_high`
  * `signal_free_t3_low`
  * `signal_tpo_ab_high`

The two files must contain matching lead signal hint sets after the change.

Do not modify:

* routing logic;
* entity loop;
* compiler structure;
* payload structure;
* `infer_yaml_flags_from_payload()` logic, except if formatting or comment update is unavoidable and no logic changes occur;
* `_SECONDARY_SIGNAL_HINTS`, unless a hardening check proves an existing test requires formatting-only alignment;
* any scoring, ranking, signal activation, or domain assembler logic.

### Content — Knowledge Bus prose substrate YAML

Update:

* `knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml`
* `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
* `knowledge_bus/functional_interpretation_v1/functional_interpretation_v1.yaml`

Required content additions:

1. Iron / blood-iron-oxygen lead entity:

   * connects the lead compiler role to the iron pathway explainer ID;
   * connects to iron functional interpretation domain ID;
   * uses governed source material from P1-26 iron PSI and compiled card evidence.

2. Thyroid lead entity:

   * connects the lead compiler role to the thyroid pathway explainer ID;
   * connects to thyroid functional interpretation domain ID;
   * uses governed source material from P1-25 thyroid PSI and compiled card evidence.

3. Iron pathway explainer:

   * neutral, non-diagnostic prose;
   * covers iron-low and iron-high as a domain-level pattern only;
   * does not distinguish absolute vs functional iron-low at routing level;
   * does not diagnose iron deficiency, anaemia of inflammation, haemochromatosis, inflammation, liver disease, haemolysis, or treatment need.

4. Thyroid pathway explainer:

   * neutral, non-diagnostic prose;
   * covers FT3-low and TPOAb-high as thyroid-domain context only;
   * does not diagnose hypothyroidism, Hashimoto’s disease, autoimmune thyroid disease, thyroid failure, or immune attack.

5. Iron functional interpretation:

   * explains what the blood/iron/oxygen axis reflects at a high level;
   * must be derived from governed PSI/card evidence;
   * no treatment advice.

6. Thyroid functional interpretation:

   * explains what thyroid hormone/antibody context reflects at a high level;
   * must be derived from governed PSI/card evidence;
   * no diagnosis or treatment advice.

Existing homocysteine and lipid content must be preserved unless a schema-level addition requires non-destructive formatting.

### Tests

Create or update tests in the appropriate test location.

Expected new test file:

* `backend/tests/unit/test_p2_1_prose_substrate_wave1_wired.py`

If repo convention requires another name/location, use that convention.

### Sprint artefacts

Create:

* `docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_manifest.yaml`
* `docs/sprints/beta_readiness/P2-1_prose_substrate_carry_forward.yaml`
* `docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_completion.md`

Update:

* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `backend/core/analytics/domain_score_assembler.py`
* `backend/core/analytics/signal_evaluator.py`
* `backend/core/analytics/narrative_payload_builder_v1.py`
* `backend/core/analytics/narrative_brief_enforcement_v1.py`
* `backend/core/contracts/narrative_payload_v1.py`
* `backend/core/contracts/narrative_report_v1.py`
* `backend/core/pipeline/orchestrator.py`
* `backend/core/models/results.py`
* scoring files
* signal activation files
* parser files
* questionnaire files
* frontend files
* Gemini files
* report redesign files
* PSI package files unless read-only source reference is needed
* compiled card files unless read-only source reference is needed
* WBC / lymphocyte / neutrophil files
* TSAT calculated-mode files
* TgAb / TPOAb euthyroid files
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`feature/prose-substrate-wave1-wired`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P2-1`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed.
6. Confirm P1-25 and P1-26 are merged.
7. Confirm no advisory or fork/background agent is running for P2-1.

STOP if preflight fails.

## Phase 1 — Source verification

Perform targeted verification only.

Read:

* current `_LEAD_SIGNAL_HINTS` and `_SECONDARY_SIGNAL_HINTS` in `narrative_compiler_lc_s3_assembly_v1.py`;
* current matching hint sets in `narrative_report_compiler_v1.py`;
* existing interpretation entity YAML shape;
* existing pathway explainer YAML shape;
* existing functional interpretation YAML shape;
* P1-25 thyroid completion report / package artefacts as source authority;
* P1-26 iron/homocysteine completion report / package artefacts as source authority.

Do not broaden into a repo audit.

Confirm:

* the two lead hint sets currently match;
* the expected existing homocysteine hints are present;
* the expected existing lipid secondary hints are present;
* YAML schema/shape is understood.

STOP if the two Python files use incompatible hint mechanisms.

## Phase 2 — Behaviour wiring

Update both Python files:

* `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
* `backend/core/analytics/narrative_report_compiler_v1.py`

Add to `_LEAD_SIGNAL_HINTS`:

* `signal_iron_low`
* `signal_iron_high`
* `signal_free_t3_low`
* `signal_tpo_ab_high`

Requirements:

* both files must have identical lead hint additions;
* preserve existing homocysteine / MCV lead hints;
* preserve existing lipid secondary hints;
* no routing logic changes;
* no entity-loop changes;
* no compiler structural changes.

STOP if adding hints alone is insufficient to make lead YAML inclusion true for the target signals. Do not redesign routing inside P2-1.

## Phase 3 — Knowledge Bus content authoring

### 3A — Interpretation entities

Update:

`knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml`

Add non-conflicting entity entries for:

* iron / blood-iron-oxygen lead context;
* thyroid lead context.

Each entity must include required schema fields, including:

* `interpretation_entity_id`
* `compiler_role`
* `phenotype_id`
* `idl_internal_id`
* `pathway_explainer_id`
* `functional_interpretation_domain_id`

Use existing naming conventions.

Because the compiler has one lead slot, entity ordering / collision behaviour must be handled carefully:

* Do not create an ordering that silently causes all new lead entities to collapse to the wrong block.
* If entity-loop last-match behaviour makes multiple lead entities unsafe, STOP and record routing redesign carry-forward.
* Do not redesign the entity loop in this sprint.

### 3B — Pathway explainers

Update:

`knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`

Add pathway explainer entries for:

* iron / blood-iron-oxygen;
* thyroid hormone/antibody context.

Use governed source material only from:

* P1-25 thyroid PSI / sprint report / compiled card evidence;
* P1-26 iron PSI / sprint report / compiled card evidence;
* existing production PSI fields;
* existing compiled card evidence.

Do not invent medical content.

Prohibited wording for iron:

* “iron deficiency diagnosis”
* “you have iron deficiency”
* “anaemia of inflammation”
* “haemochromatosis”
* “iron overload disorder”
* “you need iron”
* treatment advice.

Prohibited wording for thyroid:

* “hypothyroidism diagnosis”
* “you have hypothyroidism”
* “Hashimoto’s disease”
* “autoimmune thyroid disease” as a diagnosis;
* “your immune system is attacking your thyroid”
* “your thyroid will fail”
* treatment advice.

### 3C — Functional interpretation

Update:

`knowledge_bus/functional_interpretation_v1/functional_interpretation_v1.yaml`

Add functional interpretation entries for:

* blood/iron/oxygen pathway context;
* thyroid pathway context.

Keep content domain-level.

Do not attempt frame-level interpretation.

## Phase 4 — Tests

Create or update tests proving:

### Behaviour wiring

* `test_iron_low_signal_triggers_lead_pathway_block`
* `test_iron_high_signal_triggers_lead_pathway_block`
* `test_thyroid_ft3_low_triggers_lead_pathway_block`
* `test_thyroid_tpoab_triggers_lead_pathway_block`
* `test_homocysteine_lead_block_unchanged`
* `test_lipid_secondary_block_unchanged`
* test both Python hint sets remain aligned.

### Narrative output

* representative payload with `signal_iron_low` as top finding produces a non-placeholder lead narrative;
* representative payload with `signal_iron_high` as top finding produces a non-placeholder lead narrative;
* representative payload with `signal_free_t3_low` as top finding produces a non-placeholder lead narrative;
* representative payload with `signal_tpo_ab_high` as top finding produces a non-placeholder lead narrative;
* compiler returns valid `NarrativeReportV1`;
* no crash if a pathway block is missing;
* missing block fallback remains graceful.

### Claim boundaries

Assert generated prose / YAML content does not contain prohibited diagnostic or treatment wording.

### Regression

* existing homocysteine lead pathway behaviour still works;
* existing lipid secondary pathway behaviour still works.

## Phase 5 — Carry-forward management

Create:

`docs/sprints/beta_readiness/P2-1_prose_substrate_carry_forward.yaml`

Must record:

* frame-level routing deferred:

  * `signal_iron_low` absolute vs functional distinction;
  * `signal_homocysteine_high` B-vitamin vs renal distinction;
* full six-domain simultaneous prose coverage deferred due to one-lead / one-secondary compiler model;
* routing redesign deferred:

  * `P2-FRAME-ROUTING-ARCHITECTURE-1`;
* any entity-loop collision or ordering limitation discovered;
* any stopped content block with exact reason.

Do not re-document unrelated WBC / TSAT / TgAb carry-forwards unless directly relevant to prose substrate.

## Phase 6 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_completion.md`

Keep concise.

Maximum structure:

1. start state;
2. confirmed compiler limitation;
3. behaviour wiring result;
4. YAML content result;
5. tests / validation result;
6. known limitations;
7. carry-forwards;
8. recommended next sprint.

Create:

`docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_manifest.yaml`

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight.

## Validation

Run all relevant validation.

At minimum:

* tests for the two modified Python hint sets;
* P2-1 prose substrate tests;
* existing narrative compiler tests;
* relevant claim-boundary tests;
* YAML/schema validation for:

  * interpretation entities;
  * pathway explainers;
  * functional interpretation;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to force a pass.

## Acceptance criteria

P2-1 passes only if:

1. Front matter remains `risk_level: HIGH`, `change_type: MIXED`.
2. Automation Bus preflight passes.
3. Only the two declared Python files are modified for behaviour wiring.
4. Python changes are limited to `_LEAD_SIGNAL_HINTS` additions.
5. `_SECONDARY_SIGNAL_HINTS` behaviour remains unchanged.
6. Existing homocysteine lead routing remains unchanged.
7. Existing lipid secondary routing remains unchanged.
8. `signal_iron_low` triggers lead YAML inclusion.
9. `signal_iron_high` triggers lead YAML inclusion.
10. `signal_free_t3_low` triggers lead YAML inclusion.
11. `signal_tpo_ab_high` triggers lead YAML inclusion.
12. Iron pathway YAML is authored from governed P1-26 PSI/card evidence.
13. Thyroid pathway YAML is authored from governed P1-25 PSI/card evidence.
14. Iron functional interpretation YAML is present.
15. Thyroid functional interpretation YAML is present.
16. Generated narrative output is non-placeholder for the four newly wired signal IDs when each is top finding.
17. No prohibited diagnostic or treatment wording is introduced.
18. Compiler returns valid `NarrativeReportV1`.
19. Missing-pathway fallback remains graceful.
20. No signal activation, scoring, domain allowlist, signal evaluator, parser, questionnaire, frontend, Gemini, payload schema, report schema, payload builder or claim-boundary files are modified.
21. Frame-level routing limitation is recorded as carry-forward.
22. Full six-domain simultaneous prose limitation is recorded as carry-forward.
23. Build register is updated concisely.
24. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
