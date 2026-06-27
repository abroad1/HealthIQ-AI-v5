---
work_id: P2-2+P2-3
branch: feature/p2-2-p2-3-retail-pathway-explainer-expansion
risk_level: STANDARD
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# P2-2+P2-3 — Retail Explainer and Pathway Explainer Expansion

You are Cursor, acting as Knowledge Bus CONTENT implementation agent under Automation Bus SOP v1.3.1.

This is a STANDARD-risk CONTENT sprint.

This sprint combines:

* P2-2 — Retail Explainer Expansion, Wave 1.
* P2-3 — Pathway and Missing-Marker Explainer Pack.

Do not split these into separate sprints unless a hard STOP gate fires.

Do not run another advisory.

## Sprint purpose

Expand the governed prose substrate for Wave 1 by:

1. Increasing retail biomarker explainer coverage from the current sparse baseline to at least 40 key panel markers.
2. Adding pathway / missing-marker explainer entries for the newly active domains and signal families.
3. Improving user-facing prose breadth for active Wave 1 domains without touching Intelligence Core, scoring, signal activation, compiler routing, Gemini, or frontend files.

## Controlling advisory

Use `automation_bus/latest_pipeline_advisory.md` as the sequencing authority.

Key advisory facts:

* P2-1 is complete.
* Signal-scoped lead entity routing is live for iron, thyroid and homocysteine.
* Retail explainer registry coverage is sparse, around 17/79 biomarkers.
* P2-2 and P2-3 are both STANDARD / CONTENT.
* Both target the same Knowledge Bus prose surface.
* They should be combined into one outcome-based sprint.
* P2-FRAME-ROUTING-ARCHITECTURE-1, P2-4, Gemini activation, calculated TSAT, WBC / lymphocyte / neutrophil and medical-review PSI work are not next.

## Product output

At completion:

* Retail biomarker explainer coverage is expanded to at least 40 key panel markers.
* New or updated pathway / missing-marker explainers exist for:

  * blood / iron / oxygen;
  * thyroid;
  * kidney;
  * homocysteine / cardiovascular context;
  * any other active Wave 1 domain where the existing registry gap is obvious and safely covered by governed sources.
* All authored content is governed, neutral, educational and non-diagnostic.
* Missing-marker explainers caution appropriately where context is absent without inventing medical meaning.
* No runtime behaviour changes are introduced.

## Files in scope

Use current repo paths. Expected Knowledge Bus files may include:

* retail biomarker explainer registry files;
* pathway explainer registry files;
* missing-marker explainer registry files;
* relevant Knowledge Bus validation manifests;
* relevant tests for retail explainers, pathway explainers and missing-marker content;
* sprint artefacts under `docs/sprints/beta_readiness/`;
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`.

Before editing, identify the exact current registry paths from existing Knowledge Bus structure and tests.

This identification belongs to Stage D / implementation verification, not a new advisory.

## Sprint artefacts

Create:

* `docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_manifest.yaml`
* `docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_completion.md`
* `docs/sprints/beta_readiness/P2-2_P2-3_carry_forward.yaml`

Update:

* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `backend/core/analytics/narrative_report_compiler_v1.py`
* `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
* `backend/core/analytics/narrative_payload_builder_v1.py`
* `backend/core/analytics/narrative_brief_enforcement_v1.py`
* `backend/core/contracts/narrative_payload_v1.py`
* `backend/core/contracts/narrative_report_v1.py`
* `backend/core/analytics/domain_score_assembler.py`
* `backend/core/analytics/signal_evaluator.py`
* scoring policy files
* signal activation files
* parser files
* questionnaire files
* frontend files
* Gemini files
* payload/report schema files
* compiled card routing files unless read-only source reference is needed
* production PSI package files unless read-only source reference is needed
* calculated TSAT files
* WBC / lymphocyte / neutrophil files
* TPOAb euthyroid or TgAb deferred files
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

If any Intelligence Core or runtime behaviour file appears necessary, STOP and return to GPT. Do not convert this into a MIXED sprint inside Cursor.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`feature/p2-2-p2-3-retail-pathway-explainer-expansion`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P2-2+P2-3`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed.
6. Confirm P2-1 is merged.
7. Confirm no advisory or fork/background agent is running for this sprint.

STOP if preflight fails.

## Phase 1 — Registry and source verification

Perform targeted verification only.

Identify:

* current retail biomarker explainer registry path;
* current pathway explainer registry path;
* current missing-marker explainer registry path;
* existing test patterns for these registry files;
* current coverage count or equivalent registry count mechanism;
* governed source artefacts that may be used for content authoring.

Allowed source authorities:

* existing production PSI;
* Pass 3 promoted / investigation-spec content where already governed;
* compiled health-system cards;
* P1-25 thyroid completion artefacts;
* P1-26 iron/homocysteine completion artefacts;
* P2-1 prose substrate completion artefacts;
* existing retail explainer content-boundary rules.

Do not use memory as source authority.

Do not perform medical review.

Do not invent new clinical interpretations.

## Phase 2 — Retail explainer expansion

Expand retail biomarker explainer coverage to at least 40 key panel markers.

Prioritise active Wave 1 and common panel markers, including where present and governed:

* iron;
* ferritin;
* transferrin;
* transferrin saturation;
* CRP;
* haemoglobin;
* MCV;
* vitamin B12;
* active B12;
* folate;
* homocysteine;
* creatinine;
* eGFR;
* ALT;
* AST;
* bilirubin;
* TSH;
* free T3;
* free T4;
* TPOAb;
* key lipid markers already active;
* key metabolic markers already active;
* kidney markers already active;
* liver markers already active.

Use existing registry naming, schema, tone and validation rules.

Retail explainer entries must:

* be educational and user-facing;
* avoid diagnosis;
* avoid treatment advice;
* avoid embedding fixed reference ranges;
* avoid overriding lab-derived ranges;
* avoid creating medical meaning beyond governed Layer B artefacts;
* explain what the marker broadly relates to;
* state that interpretation depends on wider pattern and lab range where appropriate.

STOP if the content boundary rules cannot support a proposed marker safely.

## Phase 3 — Pathway and missing-marker explainers

Add or update pathway / missing-marker explainers for active Wave 1 areas where registry support is sparse.

Prioritise:

* blood / iron / oxygen;
* thyroid;
* kidney;
* homocysteine / one-carbon / cardiovascular context;
* relevant liver, lipid, metabolic and inflammation contexts if existing registry gaps are clear.

Missing-marker explainers must:

* explain why an absent supporting marker can limit interpretation;
* avoid implying that the missing marker is required for diagnosis;
* avoid telling the user to order tests;
* avoid treatment advice;
* use cautious wording such as “can make interpretation less specific” or repo-consistent equivalent;
* align with existing content-boundary rules.

Pathway explainers must:

* cite governed PSI, Pass 3, compiled card or existing package authority;
* avoid unsupported causal claims;
* avoid diagnosis;
* avoid risk prediction unless already governed;
* avoid new medical interpretations.

## Phase 4 — P1-26 mechanical defect absorption

If and only if the sprint touches the relevant iron explainer/source area and doing so does not broaden scope, correct the P1-26 M1 mechanical defect:

* update obsolete `KBP-473x` naming in the three iron `signal_library.yaml` headers to the correct `pkg_kb52c_*` package IDs.

This is allowed only as a mechanical hygiene correction.

Do not modify iron gate logic, PSI meaning, package manifests, runtime behaviour, or signal activation.

If this correction would require broader package edits, defer it again.

## Phase 5 — Tests and validation

Add or update tests proving:

* retail explainer coverage is at least 40 markers;
* all new retail explainer entries validate against schema;
* all new pathway / missing-marker entries validate against schema;
* no new entry contains prohibited diagnostic or treatment wording;
* no fixed reference ranges are embedded where prohibited;
* all new content has governed provenance/source references where the schema supports it;
* missing-marker entries use cautionary, non-directive language;
* existing P2-1 prose substrate tests continue to pass;
* no Intelligence Core files changed.

Expected tests may include:

* retail explainer registry coverage count;
* content-boundary phrase checks;
* pathway explainer schema validation;
* missing-marker explainer schema validation;
* provenance/source-reference checks.

Use existing test conventions.

Do not weaken tests to make the sprint pass.

## Phase 6 — Carry-forward management

Create:

`docs/sprints/beta_readiness/P2-2_P2-3_carry_forward.yaml`

Record:

* markers not covered and why;
* pathway/missing-marker entries deferred and why;
* any marker lacking sufficient governed source authority;
* P1-26 M1 status:

  * closed if corrected;
  * still deferred if untouched;
* P2-FRAME-ROUTING-ARCHITECTURE-1 remains deferred;
* P2-4 NarrativePayload hardening remains deferred;
* Gemini activation remains deferred;
* WBC / lymphocyte / neutrophil remains blocked;
* calculated TSAT remains blocked.

Do not re-open P2-1 architectural issues unless this sprint directly affects them.

## Phase 7 — Completion report and build register

Create:

`docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_completion.md`

Keep concise.

Maximum structure:

1. start state;
2. registry paths confirmed;
3. retail explainer expansion result;
4. pathway / missing-marker result;
5. validation result;
6. carry-forwards;
7. recommended next sprint.

Create:

`docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_manifest.yaml`

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight.

## Validation

Run all relevant validation.

At minimum:

* retail explainer registry tests;
* pathway explainer tests;
* missing-marker explainer tests;
* content-boundary/prohibited wording tests;
* provenance/source-reference tests where supported;
* existing P2-1 prose substrate regression tests if affected;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to force a pass.

## Acceptance criteria

P2-2+P2-3 passes only if:

1. Front matter remains `risk_level: STANDARD`, `change_type: CONTENT`.
2. Automation Bus preflight passes.
3. No Intelligence Core or runtime behaviour files are modified.
4. No scoring, signal activation, signal evaluator, domain assembler, parser, questionnaire, frontend, Gemini, payload schema, report schema, compiler routing or compiled card routing files are modified.
5. Retail biomarker explainer coverage reaches at least 40 key panel markers, or the sprint STOPs and records exact blockers.
6. New retail explainer entries validate.
7. New pathway explainer entries validate.
8. New missing-marker entries validate.
9. New content has governed source authority.
10. No fixed reference ranges are embedded where prohibited.
11. No diagnostic wording is introduced.
12. No treatment advice is introduced.
13. Missing-marker entries are cautionary, not directive.
14. Existing retail/pathway explainer content is preserved unless intentionally updated.
15. Existing P2-1 prose substrate behaviour is not regressed.
16. P1-26 M1 is either closed as mechanical hygiene or explicitly carried forward.
17. Carry-forward file records all deferred markers/pathways and blocked high-risk items.
18. Build register is updated concisely.
19. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
