---
work_id: P1-26
branch: feature/p1-26-mr-v2-iron-homocysteine-signal-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-26 — MR-v2 Cleared Signal Activation Cohort: Iron + Homocysteine

You are Cursor, acting as a combined Knowledge Bus + Core Engine implementation agent under Automation Bus SOP v1.3.1.

This is a HIGH-risk MIXED sprint.

This sprint implements the MR-v2-cleared iron and homocysteine activation cohort as one outcome-based package.

Candidate set:

1. Iron low / absolute iron deficiency context.
2. Iron low / functional inflammatory restriction context.
3. Iron high / iron overload context.
4. Homocysteine high / B-vitamin processing context.
5. Homocysteine high / renal clearance context.

Do not split this into separate iron-only, homocysteine-only, PSI-only, allowlist-only, package-only, card-only or test-only sprints unless a hard STOP gate fires.

Do not run another advisory.

## Controlling scoping facts

Use the completed P1-26 scope advisory as current scoping authority.

Key facts:

* P1-26 remains one sprint.
* No whole-sprint blocker exists.
* All five candidate package paths are present.
* All five candidates have staged PSI available.
* Three iron candidates require new production package folders.
* Two homocysteine production packages already exist but lack `promoted_signal_intelligence.yaml`.
* Iron requires `domain_score_assembler.py` change: add `signal_iron_low` and `signal_iron_high` to `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS`.
* Homocysteine requires no `domain_score_assembler.py` change because `_is_wave1_cardiovascular` already routes `signal_homocysteine_high` by predicate.
* Directly reported `transferrin_saturation` is SSOT-canonical.
* No calculated TSAT mode is required or allowed.
* No obvious prohibited user-facing wording blocker was found.
* Compiled card enrichment is safe for:

  * `wave1_bio_oxygen_carrying_capacity`
  * `wave1_cv_homocysteine_pathway`

## Authority inputs

Read before editing:

* `automation_bus/latest_audit_summary.md`
* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_pipeline_advisory_throughput_challenge.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/Medical Research Documents/Medical_Research_Activation_Review_Deferred_Wave_1_Items_v2.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `docs/sprints/beta_readiness/P1-25_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-25_thyroid_mr_v2_activation_completion.md`

Use production package examples only if needed for schema pattern confirmation:

* P1-21 ferritin-high package pattern
* P1-23 TSH package pattern
* P1-25 TPOAb package pattern

Do not broaden into advisory work.

## Sprint purpose

Deliver one governed activation cohort that:

* creates production packages for three iron candidates;
* promotes staged PSI for three iron candidates;
* completes production PSI for two homocysteine candidates;
* updates iron runtime allowlist in `domain_score_assembler.py`;
* leaves homocysteine assembler routing unchanged;
* enforces MR-v2 gates using directly reported TSAT only;
* avoids unsafe diagnostic wording;
* updates compiled card evidence for iron and homocysteine;
* updates tests and sprint artefacts;
* records candidate-level outcomes and carry-forwards.

## Files in scope

### HIGH-risk behaviour / Intelligence Core

* `backend/core/analytics/domain_score_assembler.py`

Allowed changes only:

* add `signal_iron_low` to `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS`;
* add `signal_iron_high` to `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS`;
* update the iron comment to record that MR-v2 dated 2026-06-23 is the frame adjudication resolving the prior P1-3/P1-18 iron carry-forward;
* do not alter homocysteine routing;
* do not alter scoring logic, ranking logic, assembler structure, signal evaluator logic, or other domain constants.

### Iron production packages to create

Create full production package folders:

* `knowledge_bus/packages/pkg_kb52c_iron_low_absolute_iron_deficiency/`
* `knowledge_bus/packages/pkg_kb52c_iron_low_functional_iron_restriction_inflammation/`
* `knowledge_bus/packages/pkg_kb52c_iron_high_iron_overload_context/`

Each production package must include the required current package structure, expected to include:

* `research_brief.yaml`
* `signal_library.yaml`
* `package_manifest.yaml`
* `promoted_signal_intelligence.yaml`

Use the staged PSI from:

* `knowledge_bus/generated_pilot/p1_12_batch_c/pkg_kb52c_iron_low_absolute_iron_deficiency/`
* `knowledge_bus/generated_pilot/p1_12_batch_c/pkg_kb52c_iron_low_functional_iron_restriction_inflammation/`
* `knowledge_bus/generated_pilot/p1_12_batch_c/pkg_kb52c_iron_high_iron_overload_context/`

Follow the P1-21 ferritin-high production package pattern.

Do not byte-copy blindly if current production package schema requires additional fields.

### Homocysteine production packages to complete

Update existing production package folders:

* `knowledge_bus/packages/pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment/`
* `knowledge_bus/packages/pkg_kb52c_homocysteine_high_renal_clearance_reduction/`

Create:

* `promoted_signal_intelligence.yaml` in each package.

Use staged PSI from:

* `knowledge_bus/generated_pilot/p1_10_batch_a/pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment/`
* `knowledge_bus/generated_pilot/p1_10_batch_a/pkg_kb52c_homocysteine_high_renal_clearance_reduction/`

Update each homocysteine `package_manifest.yaml` to reflect production PSI availability and runtime surfacing accurately.

Manifest amendment rule:

* Do not imply a new homocysteine assembler allowlist activation.
* Predicate routing is already live.
* If active package pattern supports `SIGNAL_RUNTIME_ACTIVATION`, use it only if it means production PSI/runtime surfacing.
* If that value specifically implies a newly added allowlist switch, choose the closest accurate package status used by existing active predicate-routed packages.
* Record the decision in the sprint report.

### Compiled card estate

Update:

* `knowledge_bus/compiled/health_system_cards/wave1_bio_oxygen_carrying_capacity.yaml`
* `knowledge_bus/compiled/health_system_cards/wave1_cv_homocysteine_pathway.yaml`
* `knowledge_bus/compiled/estate_index_v1.yaml`

Create:

* `knowledge_bus/compiled/manifests/p1_26_iron_homocysteine_card_evidence.yaml`

Expected card changes:

* add passing iron source specs and package refs to `wave1_bio_oxygen_carrying_capacity`;
* preserve P1-24 transferrin-high enrichment;
* update `wave1_cv_homocysteine_pathway` from legacy `pkg_s24` / legacy source-spec references to the new KB-S52C homocysteine package refs and source-spec IDs;
* update relevant `compile_manifest_ref`;
* update estate index paths for changed cards only;
* do not add stopped candidates as active card depth.

### Tests

Create:

* `backend/tests/unit/test_p1_26_iron_homocysteine_activation.py`

Use existing test files only if current repo pattern requires a different placement.

### Sprint artefacts

Create:

* `docs/sprints/beta_readiness/P1-26_iron_homocysteine_manifest.yaml`
* `docs/sprints/beta_readiness/P1-26_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-26_iron_homocysteine_mr_v2_activation.md`

Update:

* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `backend/core/analytics/signal_evaluator.py`
* `backend/ssot/biomarkers.yaml`
* `backend/ssot/questionnaire.json`
* `backend/ssot/scoring_policy.yaml`
* calculated TSAT logic
* parser files
* frontend files
* Gemini files
* report prose / Layer C prose substrate
* thyroid files
* WBC packages
* lymphocyte packages
* neutrophil packages
* TgAb / TPOAb files
* `pkg_kb52c_iron_high_hepatocellular_or_hemolytic_release`
* unrelated Knowledge Bus packages
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`feature/p1-26-mr-v2-iron-homocysteine-signal-activation`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-26`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.
6. Confirm P1-25 is closed and merged before beginning.
7. Confirm no advisory or fork/background agent is running for P1-26.

STOP if preflight fails.

## Phase 1 — Authority and B1 verification

### 1A — MR-v2 authority verification

Read MR-v2 sections covering:

* iron low / absolute iron deficiency;
* iron low / functional inflammatory restriction;
* iron high / overload context;
* homocysteine high / B-vitamin processing context;
* homocysteine high / renal-clearance context.

Confirm:

* all five candidates are medically cleared with strict gates;
* calculated TSAT remains blocked;
* directly reported TSAT may be used;
* hepatocellular / haemolytic release is not a standalone iron-high activation;
* WBC / lymphocyte / neutrophil work remains out of scope.

STOP affected candidate if MR-v2 does not support activation.

### 1B — B1 fact verification

Verify only the minimum blocker facts before editing:

1. all five candidate package paths exist;
2. staged PSI exists for all five candidates;
3. `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS` is the correct iron allowlist constant;
4. homocysteine is already routed to cardiovascular by predicate and requires no assembler change;
5. no candidate depends on calculated TSAT;
6. no obvious prohibited wording exists in user-facing PSI fields.

If any B1 fact is stale, apply candidate-level STOP gates rather than expanding scope.

## Phase 2 — Iron implementation

### 2A — Create iron production packages

For each passing iron candidate, create a production package folder under `knowledge_bus/packages/` with current production structure.

Candidates:

1. `pkg_kb52c_iron_low_absolute_iron_deficiency`
2. `pkg_kb52c_iron_low_functional_iron_restriction_inflammation`
3. `pkg_kb52c_iron_high_iron_overload_context`

Each package must include:

* `research_brief.yaml`
* `signal_library.yaml`
* `package_manifest.yaml`
* `promoted_signal_intelligence.yaml`

Use staged PSI as the content source. Follow current active package patterns. Do not invent unsupported medical content.

### 2B — Iron low / absolute iron deficiency context

Candidate must require:

* serum iron below lab-provided range;
* ferritin below lab-provided range;
* directly reported `transferrin_saturation` low;
* CRP/inflammation contradiction handling where available;
* supplement / recent iron infusion context where available;
* no “iron deficiency diagnosis” wording;
* no treatment advice.

Candidate STOP:

* if directly reported TSAT is not required in the candidate gate;
* if staged PSI assumes calculated TSAT;
* if ferritin-low is not required;
* if unsafe diagnosis wording cannot be corrected.

### 2C — Iron low / functional inflammatory restriction context

Candidate must require:

* serum iron below lab-provided range;
* directly reported `transferrin_saturation` low;
* ferritin normal/high or explicitly non-low;
* CRP high or declared inflammation/infection context where available;
* contradiction if ferritin is low;
* no “anaemia of inflammation” diagnosis wording;
* no treatment advice.

Candidate STOP:

* if directly reported TSAT is not required;
* if ferritin state does not distinguish functional restriction from absolute deficiency;
* if inflammation/CRP context cannot be represented;
* if unsafe diagnosis wording cannot be corrected.

### 2D — Iron high / overload context

Candidate must require:

* serum iron above lab-provided range;
* directly reported `transferrin_saturation` high;
* ferritin above lab-provided range;
* liver markers checked where available;
* recent iron ingestion / infusion caveat where available;
* hepatocellular / haemolytic release handled only as caveat or suppressor, not standalone signal;
* no haemochromatosis diagnosis wording;
* no treatment advice.

Candidate STOP:

* if directly reported TSAT is not required;
* if ferritin-high is not required;
* if staged PSI frames haemochromatosis diagnostically;
* if hepatocellular/haemolytic material becomes standalone signal content.

## Phase 3 — Homocysteine implementation

### 3A — Homocysteine high / B-vitamin processing context

Candidate must require:

* homocysteine above lab-provided range;
* active B12 and/or vitamin B12 context;
* folate present;
* MCV retained as useful context where available;
* renal contradiction handled through the separate renal-clearance frame where applicable;
* no consumer-facing “methylation impairment” wording;
* no primary cardiovascular-risk claim;
* no diagnosis or treatment advice.

Internal package identity may contain `methylation_impairment` if user-facing PSI fields do not.

Candidate STOP:

* if active B12 / vitamin B12 and folate cannot be required or represented;
* if user-facing “methylation impairment” wording cannot be corrected;
* if the frame becomes a primary cardiovascular-risk claim.

### 3B — Homocysteine high / renal-clearance context

Candidate must require:

* homocysteine above lab-provided range;
* creatinine and/or eGFR supportive context;
* B12 / folate contradiction handling;
* no kidney disease diagnosis wording;
* no treatment advice.

Candidate STOP:

* if creatinine/eGFR cannot be required or represented;
* if wording implies kidney disease diagnosis;
* if B-vitamin contradiction handling cannot be represented.

### 3C — Homocysteine routing

Do not modify `domain_score_assembler.py` for homocysteine if the current predicate already routes `signal_homocysteine_high` to cardiovascular.

If the predicate is absent or materially different from the advisory finding:

* stop homocysteine candidates;
* do not create a new assembler route without explicit human approval;
* proceed with iron candidates if valid.

## Phase 4 — Iron allowlist update

Update:

`backend/core/analytics/domain_score_assembler.py`

Only if at least one relevant iron candidate passes.

Expected target:

* `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS` includes:

  * existing active signals, including `signal_transferrin_high`;
  * `signal_iron_low` if at least one iron-low candidate passes;
  * `signal_iron_high` if iron-high overload candidate passes.

If both iron-low candidates STOP:

* do not add `signal_iron_low`.

If iron-high overload STOPs:

* do not add `signal_iron_high`.

Update comment at the iron allowlist section to record:

* P1-3/P1-18 iron frame carry-forward resolved by MR-v2 dated 2026-06-23;
* P1-26 activated governed iron-low and iron-high contexts.

Do not change scoring/ranking logic.

Do not modify homocysteine routing.

## Phase 5 — Compiled card enrichment

### 5A — Blood / iron / oxygen card

Update:

`knowledge_bus/compiled/health_system_cards/wave1_bio_oxygen_carrying_capacity.yaml`

Include passing iron candidates only.

Expected enrichment:

* add `inv_iron_low_absolute_iron_deficiency` if absolute iron-low passes;
* add `inv_iron_low_functional_iron_restriction_inflammation` if functional iron-low passes;
* add `inv_iron_high_iron_overload_context` if iron-high overload passes;
* add corresponding package refs;
* update mechanism/subsystem summary only to reflect activated governed context;
* preserve P1-24 transferrin-high enrichment;
* do not add unactivated candidates.

### 5B — Homocysteine card

Update:

`knowledge_bus/compiled/health_system_cards/wave1_cv_homocysteine_pathway.yaml`

If both homocysteine candidates pass:

* replace or supersede legacy `pkg_s24` / legacy source-spec references with KB-S52C source specs and package refs;
* add:

  * `inv_homocysteine_high_b_vitamin_related_methylation_impairment`
  * `inv_homocysteine_high_renal_clearance_reduction`
* update package refs to:

  * `pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment`
  * `pkg_kb52c_homocysteine_high_renal_clearance_reduction`
* update compile manifest reference.

If one homocysteine candidate stops:

* include only the passing candidate;
* do not remove legacy context unless the new card remains coherent.

If ownership or schema is unexpectedly unclear:

* do not create a new card;
* record carry-forward for homocysteine compiled-card ownership;
* keep production PSI activation if otherwise valid.

### 5C — Compile manifest and estate index

Create:

`knowledge_bus/compiled/manifests/p1_26_iron_homocysteine_card_evidence.yaml`

Update:

`knowledge_bus/compiled/estate_index_v1.yaml`

Update estate index paths only for cards actually changed.

## Phase 6 — Tests

Create:

`backend/tests/unit/test_p1_26_iron_homocysteine_activation.py`

Required tests:

### Domain allowlist

* `test_iron_low_signal_in_blood_iron_oxygen_allowlist_after_p1_26`
* `test_iron_high_signal_in_blood_iron_oxygen_allowlist_after_p1_26`
* assert `signal_transferrin_high` remains active
* assert homocysteine assembler routing remains unchanged

### Iron gates

* `test_iron_low_absolute_fires_with_ferritin_low_and_tsat_low`
* `test_iron_low_absolute_suppresses_without_tsat`
* `test_iron_low_functional_fires_with_crp_high_and_ferritin_normal`
* `test_iron_low_functional_suppresses_when_ferritin_low`
* `test_iron_high_overload_fires_with_tsat_high_and_ferritin_above_range`
* `test_iron_high_overload_suppresses_without_tsat`
* `test_iron_high_overload_ctr_alt_high_weakens_overload_interpretation`

### Homocysteine gates

* `test_homocysteine_b_vitamin_fires_with_active_b12_and_folate_present`
* `test_homocysteine_renal_fires_with_creatinine_high`
* `test_homocysteine_no_methylation_impairment_wording_in_consumer_fields`
* test no primary cardiovascular-risk framing
* test no kidney disease diagnosis wording

### Compiled card tests

* `test_wave1_bio_oxygen_card_includes_iron_source_specs`
* `test_wave1_cv_homocysteine_card_updated_to_kb52c_packages`

### Wording tests

Assert user-facing PSI fields do not contain prohibited phrases:

* “iron deficiency diagnosis”
* “anaemia of inflammation”
* “haemochromatosis”
* “methylation impairment”
* “kidney disease”
* primary cardiovascular-risk framing
* treatment advice

Use exact phrase checks plus targeted safe-frame checks where current test pattern supports it.

## Phase 7 — Carry-forward management

Create:

`docs/sprints/beta_readiness/P1-26_pass3_carry_forward.yaml`

Record each candidate as:

* `closed` if activated;
* `stopped` if candidate STOP fired;
* `deferred` if blocked by scope/identity/schema.

Must include if relevant:

* calculated TSAT remains deferred / blocked;
* WBC / lymphocyte / neutrophil remain out of scope;
* hepatocellular/haemolytic iron-high release remains non-standalone;
* homocysteine compiled-card ownership if unexpectedly unclear;
* any stopped candidate with exact reason.

Expected carry-forward closures if all candidates pass:

* P1-3 / iron signal wiring deferred pending frame adjudication: closed for `signal_iron_low` and `signal_iron_high`;
* P1-18 additional CBC/iron launch signals pending frame adjudication: closed for iron-low and iron-high;
* Homocysteine medical-review blocker from P1-10/P1-14: closed for both homocysteine frames.

Do not re-document unrelated thyroid carry-forwards except as already closed by P1-25.

## Phase 8 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-26_iron_homocysteine_mr_v2_activation.md`

Keep concise.

Maximum structure:

1. start state;
2. MR-v2 authority used;
3. iron implementation result;
4. homocysteine implementation result;
5. allowlist / routing result;
6. compiled card updates;
7. validation results;
8. carry-forwards;
9. recommended next sprint.

Create:

`docs/sprints/beta_readiness/P1-26_iron_homocysteine_manifest.yaml`

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight.

## Validation

Run all relevant validation.

At minimum:

* package validation for new/modified Knowledge Bus packages;
* PSI validation for new/modified PSI;
* signal library validation;
* package manifest validation;
* compiled card validation;
* estate index validation;
* domain score assembler / allowlist tests;
* P1-26 activation tests;
* relevant blood/iron/oxygen regression tests;
* relevant cardiovascular/homocysteine tests if present;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to force a pass.

## Acceptance criteria

P1-26 passes only if:

1. Front matter remains `risk_level: HIGH`, `change_type: MIXED`.
2. Automation Bus preflight passes.
3. MR-v2 authority is cited and used.
4. All five candidates are attempted unless a candidate STOP fires.
5. Candidate-level STOP gates are applied independently.
6. No calculated TSAT mode is introduced.
7. Iron candidates use directly reported `transferrin_saturation` only.
8. `signal_iron_low` is allowlisted only if at least one iron-low candidate passes.
9. `signal_iron_high` is allowlisted only if iron-high overload candidate passes.
10. `signal_transferrin_high` remains active.
11. Homocysteine assembler routing is not modified.
12. Homocysteine production PSI is completed for passing candidates.
13. Homocysteine package manifests accurately reflect production PSI/runtime surfacing without falsely implying a new assembler allowlist change.
14. No prohibited diagnostic wording remains in user-facing PSI fields.
15. No treatment advice is introduced.
16. No WBC, lymphocyte, neutrophil, thyroid, frontend, Gemini, prose, questionnaire, parser, scoring-policy or signal-evaluator files are modified.
17. `wave1_bio_oxygen_carrying_capacity` is enriched only for passing iron candidates.
18. `wave1_cv_homocysteine_pathway` is updated only for passing homocysteine candidates.
19. Estate index is updated only for changed compiled cards.
20. Tests prove iron allowlist behaviour.
21. Tests prove iron MR-v2 gates.
22. Tests prove homocysteine MR-v2 gates.
23. Tests prove prohibited wording is absent.
24. P1-26 carry-forward file records candidate outcomes and remaining blockers.
25. Build register is updated concisely.
26. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
