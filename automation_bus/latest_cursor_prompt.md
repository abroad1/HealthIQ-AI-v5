---
work_id: LC-S5-LAUNCH-CORE-PROVING-AND-HUMAN-VALIDATION
branch: sprint5/launch-core-proving-and-human-validation
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S5 — Launch-Core Proving and Human Validation

## Objective

Implement Sprint 5: prove that the launch-core product now works coherently across automated proving and human validation.

Sprint 5 must confirm that the governed analytical pipeline, questionnaire context, narrative payload, report carriage, statin context, and consumer-facing surfaces behave consistently after LC-S1 through LC-S4, WP2, WP3, and LC-OBS2.

This is a proving and validation sprint.

Do not change analytical logic.  
Do not change questionnaire logic.  
Do not change Knowledge Bus assets.  
Do not change SSOT files.  
Do not change frontend report carriage unless a STOP condition is reached and explicitly approved.

## Authority and evidence

Primary implementation authority:

- This LC-S5 SOP prompt

Primary evidence source:

- `docs/audit-papers/lc_s5_proving_readiness_preflight_audit.md`

Claude has already completed the LC-S5 readiness preflight. Cursor should use that audit as the factual source for current proving state, known stale artefacts, remaining CHECKs, recommended implementation scope, and human validation checklist.

Historical authority, for conflict resolution only:

- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`

Do not reread the full historical planning pack unless the LC-S5 audit and this prompt conflict or are unclear.

## Current state

The following are complete and merged:

- LC-S1 analytical hardening
- LC-S2 statin/context integration
- WP2 Layer B → Layer C contract closure
- LC-S3 narrative payload implementation
- WP3 questionnaire rationalisation
- LC-S4 report carriage
- LC-S4 Sentinel promotion for `statin_signal_isolation`

The LC-S5 preflight found that Sprint 5 is ready to author, with one mandatory pre-action:

The proving artefacts are stale and must be regenerated against current `main` before binary assertions are finalised.

## Scope

Sprint 5 should include:

1. Fresh proving harness run.
2. Updated proving artefacts.
3. Binary automated checks for remaining CHECKs 2, 5, and 6.
4. Sentinel graduation for `wave1_contradiction` if CHECK 5 becomes a real guard.
5. Human validation checklist execution and documentation.
6. Sprint 5 completion note.

## Mandatory Stage 1 — Fresh proving harness run

Before writing new binary assertions, run the proving harness fresh from repo root:

```bash
python backend/tools/launch_core_proving_harness.py
````

Required outputs:

* `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`
* `docs/audit-papers/launch-core-proving/latest_fingerprints.json`

Required checks after run:

* confirm artefacts are stamped with current branch/HEAD
* confirm AB and VR runs are present
* confirm baseline, lifestyle/context, statin-off, and statin-on scenarios are present
* inspect `lead_narrative_head` for alcohol/lifestyle bridge wording
* inspect `consumer_band_labels` / domain card consequence sentence heads for contradiction risk
* inspect `clinician_page1.primary_concern_head` and `narrative.retail_summary_head` for lead coherence

If the harness fails to run, STOP and report.

If the fresh fingerprints differ materially from expected launch-core behaviour, STOP and report before writing assertions.

## Task 1 — Add CHECK 2 binary assertion

CHECK 2:

Alcohol bridge appears in human language in `lead_narrative`.

Expected file:

* new test file, preferably `backend/tests/unit/test_lc_s5_proving_checks.py`
* or a dedicated regression file if Sentinel promotion is chosen immediately

Required:

* use the fresh proving artefact or run the proving harness in-test if current project pattern supports it
* inspect `AB__lifestyle_context`
* assert that `narrative.lead_narrative_head` includes recognisable alcohol / methylation / macrocytosis context language
* choose the substring based on the fresh harness output
* do not hardcode a phrase before the harness has been run and inspected

Do not change the narrative compiler.

## Task 2 — Add CHECK 5 binary assertion

CHECK 5:

No band/headline contradiction.

Required:

* verify consumer domain card band labels and associated consequence/headline text do not contradict
* at minimum, assert that stable/strong bands do not carry danger/emergency wording and that concern/elevated bands do not carry falsely reassuring wording
* use current fresh AB and VR fingerprints or fixture output
* keep the check conservative and transparent

If contradiction rules cannot be safely inferred from current output, STOP and report the exact ambiguity.

Do not change domain score assembly logic.

## Task 3 — Add CHECK 6 binary assertion

CHECK 6:

Clinician `primary_concern` and `retail_summary` reference the same lead pattern.

Required:

* use fresh AB and VR baseline fingerprints
* compare `clinician_page1.primary_concern_head` with `narrative.retail_summary_head`
* assert that both reference the same lead pattern or lead biomarker family
* encode this transparently, using known fresh output terms
* avoid brittle over-specific wording if a stable signal ID or deterministic lead label is available

Do not change clinician report compiler or narrative compiler.

## Task 4 — Sentinel graduation for `wave1_contradiction`

Current status:

* `wave1_contradiction` is a placeholder/status-reporting Sentinel class.

If Task 2 creates a real deterministic CHECK 5 guard, update:

* `sentinel/packs/escaped_defects_v1.json`
* `sentinel/sentinel_runner.py`

Required:

* promote `wave1_contradiction` from placeholder/status-reporting to guarded/active deterministic only if the new test genuinely asserts no contradiction
* wire the new test path into the runner
* run Sentinel for `wave1_contradiction`
* report 0 issues / 0 gaps

If the CHECK 5 test cannot be made robust in this sprint, leave `wave1_contradiction` as PLACEHOLDER and document why.

## Task 5 — Human validation walkthrough

Execute or prepare the human validation walkthrough using the checklist from:

`docs/audit-papers/lc_s5_proving_readiness_preflight_audit.md`

At minimum, document validation for:

### Upload/questionnaire

* 9 mandatory questionnaire fields can be completed
* statin-on path can be triggered using `Statins (cholesterol medication)`
* alcohol/context path can be triggered with non-zero alcohol input

### Results page

* mock-mode honesty banner visible
* hero label is user-facing, not a backend slug
* retail summary visible
* “What this means” open by default
* body overview visible
* lead narrative visible
* next steps visible
* alcohol/lifestyle bridge visible where expected
* statin context visible where expected
* no legacy insights visible on consumer paths

### Actions page

* no generic legacy action cards from `legacy_v1`
* action cards do not show internal identifiers

### Advanced/clinician section

* clinician synthesis visible only in advanced/clinician section
* no raw markdown tokens visible
* clinician primary concern agrees with retail summary lead pattern

Document whether this walkthrough was:

* executed fully in browser
* partially executed
* prepared as a checklist only

If a browser/manual run is not performed in this sprint, record that clearly as a limitation and carry it forward.

## Task 6 — Update proving artefacts

Commit regenerated proving artefacts if this is the established project pattern:

* `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`
* `docs/audit-papers/launch-core-proving/latest_fingerprints.json`

If the harness generates additional timestamped artefacts, include only those normally committed by prior proving runs.

Do not commit transient local files.

## Task 7 — Completion note

Create:

`docs/sprints/LC-S5_proving_and_human_validation_completion_2026-05.md`

It must record:

* fresh proving harness run command and result
* current HEAD used for fingerprints
* AB/VR scenario matrix covered
* CHECK 2 result
* CHECK 4 status
* CHECK 5 result
* CHECK 6 result
* Sentinel changes, if any
* human validation walkthrough status
* remaining manual validation gaps
* frontend Sentinel infrastructure gaps carried forward
* confirmation no analytical engine, SSOT, Knowledge Bus, questionnaire, narrative compiler, or report carriage code changed unless explicitly approved

## Expected files touched

Expected:

* `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`
* `docs/audit-papers/launch-core-proving/latest_fingerprints.json`
* `backend/tests/unit/test_lc_s5_proving_checks.py`
* or `backend/tests/regression/test_lc_s5_proving_checks.py`
* `docs/sprints/LC-S5_proving_and_human_validation_completion_2026-05.md`

Possibly expected:

* `sentinel/packs/escaped_defects_v1.json`
* `sentinel/sentinel_runner.py`

Only if `wave1_contradiction` is promoted to a real guarded defect class.

Not expected:

* `backend/ssot/`
* `knowledge_bus/`
* `backend/core/pipeline/`
* `backend/core/analytics/`
* `backend/core/contracts/`
* `frontend/app/(app)/results/page.tsx`
* `frontend/app/(app)/actions/page.tsx`
* questionnaire files
* narrative compiler files
* biomarker interpretation logic
* Automation Bus control-plane scripts

## Tests and validation

Required:

1. Run the proving harness fresh:

```bash
python backend/tools/launch_core_proving_harness.py
```

2. Run new LC-S5 proving tests.

3. Run relevant existing regression tests:

```bash
python -m pytest backend/tests/regression -m regression --tb=short -q
```

4. If `wave1_contradiction` is promoted, run:

```bash
python sentinel/sentinel_runner.py --defect-class wave1_contradiction
```

5. Run `statin_signal_isolation` Sentinel again to confirm no regression:

```bash
python sentinel/sentinel_runner.py --defect-class statin_signal_isolation
```

Report all commands and results.

## Stop conditions

STOP and report before implementation if:

* proving harness does not run
* fresh fingerprints are not generated
* AB/VR scenarios are missing
* lifestyle/context scenario no longer produces a usable lead narrative
* statin-on/off scenario no longer preserves analytical invariants
* CHECK 2 wording cannot be identified safely from fresh output
* CHECK 5 contradiction criteria cannot be made robust
* CHECK 6 cannot compare lead pattern coherently from current fingerprints
* adding checks requires modifying analytical engine code
* any change appears to require SSOT, Knowledge Bus, questionnaire, narrative compiler, or report carriage code
* Sentinel promotion requires control-plane script changes

## Explicit non-goals

Do not:

* modify analytical engine logic
* modify narrative compiler logic
* modify questionnaire logic
* modify report carriage UI
* modify Knowledge Bus assets
* modify SSOT files
* activate Gemini
* build frontend Sentinel/Jest runner support
* implement PDF export testing
* implement paywall/pricing testing
* implement longitudinal narrative
* restructure `AnalysisDTO`
* author Sprint 6

## Risk classification

Risk level: STANDARD.

Rationale:

Sprint 5 is expected to touch tests, proving artefacts, Sprint documentation, and possibly Sentinel pack/runner entries. It must not touch Intelligence Core, SSOT, Knowledge Bus, backend pipeline logic, frontend report UI, or Automation Bus control-plane scripts.

If any HIGH-risk path becomes necessary, STOP and escalate to GPT before proceeding.

## Closure evidence required

Before finish, report:

* branch
* work_id
* files changed
* proving harness command/result
* current HEAD in fingerprints
* CHECK 2 pass/fail
* CHECK 4 status
* CHECK 5 pass/fail
* CHECK 6 pass/fail
* Sentinel commands/results
* whether `wave1_contradiction` was promoted
* human validation walkthrough status
* known limitations
* confirmation no analytical engine files changed
* confirmation no SSOT files changed
* confirmation no Knowledge Bus files changed
* confirmation no questionnaire files changed
* confirmation no frontend report files changed
* confirmation no Automation Bus control-plane scripts changed

## Final expected outcome

After LC-S5, HealthIQ AI should have current launch-core proving artefacts, binary checks for the remaining key proving obligations, and a documented human validation outcome/checklist.

The product should be ready for the next planning decision based on evidence rather than assumption.
