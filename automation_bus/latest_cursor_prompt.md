---
work_id: P1-24
branch: sprint/P1-24-bio-oxygen-subsystem-signal-depth
risk_level: STANDARD
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# P1-24 — Bio-oxygen Subsystem Signal Depth

You are Cursor, acting as the Core Engine implementation agent with Knowledge Bus read-only evidence access.

Implement this work package under Automation Bus SOP v1.3.1.

This is a STANDARD-risk CONTENT sprint.

It is not a runtime signal sprint.
It is not a scoring sprint.
It is not a domain allowlist sprint.
It is not a frontend sprint.
It is not a Gemini/report-prose sprint.
It is not a Knowledge Bus package-promotion sprint.

## Purpose

Update the existing compiled bio-oxygen subsystem card so `wave1_blood_iron_oxygen` reflects the current production PSI estate after the recent ferritin/transferrin promotions.

The target product outcome is:

1. `wave1_bio_oxygen_carrying_capacity` reflects ferritin-high signal depth:

   * inflammatory hyperferritinemia context;
   * iron overload context.
2. `wave1_bio_oxygen_carrying_capacity` reflects transferrin-high signal intelligence.
3. The compiled card remains traceable to governed source specs.
4. No new PSI opt-ins are performed.
5. No scoring behaviour changes.
6. No domain allowlist changes.
7. No signal evaluator changes.
8. No frontend/Gemini/report prose work.
9. No medical content is invented.

## Stage B baseline

Stage B Throughput Check confirmed:

* sprint shape is correct as one package;
* no split is required;
* `risk_level: STANDARD`;
* `change_type: CONTENT`;
* all writes should remain within `knowledge_bus/compiled/` plus tests and sprint artefacts;
* the P1-3 manifest must not be mutated;
* a new P1-24 compile manifest must be created;
* `knowledge_bus/compiled/estate_index_v1.yaml` must be explicitly in scope;
* the three new investigation spec IDs must be named directly;
* transferrin must be explicitly authorised as a governed marker entry.

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_5.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* latest P1-23 sprint artefacts, if present
* `knowledge_bus/compiled/health_system_cards/wave1_bio_oxygen_carrying_capacity.yaml`
* `knowledge_bus/compiled/manifests/p1_3_blood_iron_oxygen_card_evidence.yaml`
* `knowledge_bus/compiled/estate_index_v1.yaml`
* compiled health-system card schema / validator files
* compiled health-system card examples
* `knowledge_bus/packages/pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb52c_ferritin_high_iron_overload_context/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb52c_ferritin_high_iron_overload_context/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation/package_manifest.yaml`
* `knowledge_bus/packages/pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation/promoted_signal_intelligence.yaml`
* existing tests for compiled subsystem evidence, especially:

  * `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
  * `backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py`
  * any existing compiled-card evidence tests found by search.

Use targeted search:

* `rg "wave1_bio_oxygen_carrying_capacity|bio_oxygen_carrying_capacity|blood_iron_oxygen" knowledge_bus backend docs`
* `rg "health_system_card_evidence|compiled_subsystem|assemble_subsystem_from_compiled_card_evidence" backend knowledge_bus`
* `rg "p1_3_blood_iron_oxygen_card_evidence|estate_index_v1" knowledge_bus`
* `rg "inv_ferritin_high_inflammatory_hyperferritinemia|inv_ferritin_high_iron_overload_context|inv_transferrin_high_iron_deficiency_transport_upregulation" knowledge_bus`
* `rg "ferritin_high|transferrin_high|signal_ferritin_high|signal_transferrin_high" knowledge_bus backend docs`
* `rg "domain_ux1c_governed_subsystem_evidence|subsystem evidence row|compiled card" backend/tests`

Inspect relevant hits before editing.

## Files in scope

Allowed if justified:

### Compiled card estate

* `knowledge_bus/compiled/health_system_cards/wave1_bio_oxygen_carrying_capacity.yaml`
* `knowledge_bus/compiled/manifests/p1_24_blood_iron_oxygen_card_evidence.yaml`
* `knowledge_bus/compiled/estate_index_v1.yaml`

### Tests

* `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
* `backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py`
* a new P1-24-specific test file if needed:

  * `backend/tests/unit/test_p1_24_bio_oxygen_subsystem_signal_depth.py`

### Sprint artefacts

* `docs/sprints/beta_readiness/P1-24_bio_oxygen_subsystem_signal_depth.md`
* `docs/sprints/beta_readiness/P1-24_bio_oxygen_card_manifest.yaml`
* `docs/sprints/beta_readiness/P1-24_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `knowledge_bus/compiled/manifests/p1_3_blood_iron_oxygen_card_evidence.yaml`
* Knowledge Bus package files under `knowledge_bus/packages/`
* `promoted_signal_intelligence.yaml` files
* `signal_library.yaml` files
* `research_brief.yaml` files
* `package_manifest.yaml` files
* raw Pass 3 research
* generated-pilot files
* backend signal evaluator
* backend scoring policy
* domain allowlist files
* frontend files
* Gemini files
* report prose / Layer C files
* parser files
* TSAT / transferrin saturation policy
* thyroid files
* iron-low packages
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Explicit source spec IDs to add

Add exactly these three new source spec IDs to `wave1_bio_oxygen_carrying_capacity.yaml`:

* `inv_ferritin_high_inflammatory_hyperferritinemia`
* `inv_ferritin_high_iron_overload_context`
* `inv_transferrin_high_iron_deficiency_transport_upregulation`

Existing source spec IDs must remain unless validation proves they are invalid.

Do not invent source spec IDs.

Do not derive source spec IDs from package names without verifying them in package/PSI evidence.

## Explicit marker-signal additions

The existing card must be enriched using governed evidence from production PSI packages.

### Ferritin-high

Use the existing ferritin marker structure if present.

Add ferritin-high context depth for:

* inflammatory hyperferritinemia;
* iron overload context.

Evidence source:

* `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia/promoted_signal_intelligence.yaml`
* `pkg_kb52c_ferritin_high_iron_overload_context/promoted_signal_intelligence.yaml`

### Transferrin-high

Add a new governed marker entry for transferrin if it is not already present.

Evidence source:

* `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation/promoted_signal_intelligence.yaml`

The transferrin marker entry is explicitly authorised in this sprint.

Suggested governed role, if supported by PSI evidence:

* `marker_role: contextual_marker`
* `relationship_kind: contextual_support`
* `presence_policy: optional_on_panel`

Do not use this suggested role unless the PSI evidence supports it.

STOP if marker role, relationship kind, rationale, or presence policy cannot be derived from governed PSI/package evidence without inventing content.

## Manifest strategy

Do not mutate:

`knowledge_bus/compiled/manifests/p1_3_blood_iron_oxygen_card_evidence.yaml`

Create a new manifest:

`knowledge_bus/compiled/manifests/p1_24_blood_iron_oxygen_card_evidence.yaml`

The new manifest must:

* use a fresh P1-24 compile run ID;
* list all source specs used by the updated card, including existing and new specs;
* record that it supersedes the P1-3 manifest for the current compiled card version;
* preserve P1-3 provenance by leaving the P1-3 manifest unchanged;
* include output hash fields in the repository’s established pattern.

Update:

`knowledge_bus/compiled/estate_index_v1.yaml`

so the `wave1_bio_oxygen_carrying_capacity` entry points to the new P1-24 manifest path.

## Canonical test module

Use this as the canonical test target for governed subsystem evidence emission:

`backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`

Also update:

`backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py`

if it contains assertions that must reflect the enriched bio-oxygen card.

If the canonical regression test cannot express the enriched-card assertion cleanly, create:

`backend/tests/unit/test_p1_24_bio_oxygen_subsystem_signal_depth.py`

The new test file, if created, must be limited to P1-24 card-depth assertions.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-24-bio-oxygen-subsystem-signal-depth`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-24`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Evidence and schema gate

### 1A — Package evidence verification

Verify the following production PSI packages exist and contain `promoted_signal_intelligence.yaml`:

* `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`
* `pkg_kb52c_ferritin_high_iron_overload_context`
* `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation`

For each, verify:

* investigation spec ID;
* signal ID;
* package manifest status;
* `behavioural_impact: NONE`;
* PSI validation status where recorded.

Record findings in:

`docs/sprints/beta_readiness/P1-24_bio_oxygen_card_manifest.yaml`

STOP if any package is missing, not production-opted-in, or cannot supply governed evidence.

### 1B — Compiled card schema verification

Inspect the compiled health-system card schema and existing compiled card examples.

Confirm:

* how `source_spec_ids` are represented;
* how marker entries are represented;
* allowed `marker_role` values;
* allowed `relationship_kind` values;
* allowed `presence_policy` values;
* manifest reference pattern;
* estate index pattern.

Record schema decisions in the P1-24 manifest.

STOP if schema requirements are unclear.

### 1C — Source spec traceability gate

For each new source spec ID:

* `inv_ferritin_high_inflammatory_hyperferritinemia`
* `inv_ferritin_high_iron_overload_context`
* `inv_transferrin_high_iron_deficiency_transport_upregulation`

verify traceability through production package/PSI evidence.

STOP if any source spec ID cannot be traced.

### 1D — Transferrin governed role gate

Before adding a transferrin marker entry, derive its marker role, relationship kind, rationale and presence policy from:

`pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation/promoted_signal_intelligence.yaml`

STOP if this requires invented medical content.

### 1E — Test target confirmation

Confirm whether:

`backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`

is the correct canonical test module for enriched subsystem evidence emission.

If yes, update it.

If not, record why in the P1-24 manifest and create:

`backend/tests/unit/test_p1_24_bio_oxygen_subsystem_signal_depth.py`

Do not proceed without a named test target.

## Phase 2 — Compiled card update

Update:

`knowledge_bus/compiled/health_system_cards/wave1_bio_oxygen_carrying_capacity.yaml`

Required updates:

1. Add the three new source spec IDs.
2. Add ferritin-high context depth from the two ferritin-high PSI packages.
3. Add transferrin-high marker intelligence from the transferrin-high PSI package.
4. Update `compile_manifest_ref` from `knowledge_bus/compiled/manifests/p1_3_blood_iron_oxygen_card_evidence.yaml` to `knowledge_bus/compiled/manifests/p1_24_blood_iron_oxygen_card_evidence.yaml`.
5. Preserve existing valid content.
6. Do not invent medical wording.
7. Do not introduce scoring, allowlist, or signal evaluator implications.

## Phase 3 — New compile manifest and estate index

Create:

`knowledge_bus/compiled/manifests/p1_24_blood_iron_oxygen_card_evidence.yaml`

Do not modify:

`knowledge_bus/compiled/manifests/p1_3_blood_iron_oxygen_card_evidence.yaml`

Update:

`knowledge_bus/compiled/estate_index_v1.yaml`

so `wave1_bio_oxygen_carrying_capacity` points to the new P1-24 manifest.

## Phase 4 — Validation and tests

Run applicable validation:

* compiled health-system card schema validation;
* compiled estate index validation, if available;
* P1-24 test target;
* existing bio-oxygen domain/card tests;
* governed subsystem evidence regression tests;
* architecture/governance tests required by Automation Bus finish.

Required proof:

* enriched subsystem evidence is emitted;
* existing `wave1_blood_iron_oxygen` behaviour is not regressed;
* existing card evidence remains valid;
* no signal evaluator change occurred;
* no scoring change occurred;
* no domain allowlist change occurred;
* no new PSI opt-ins occurred;
* P1-3 manifest remains unchanged.

## Phase 5 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-24_pass3_carry_forward.yaml`

Expected outcome: no P1-24 carry-forward if all gates pass.

If any item cannot be completed, record:

* item ID;
* reference;
* reason not implemented;
* blocker class;
* owner agent:

  * Core Engine
  * Knowledge Bus
  * Medical Review
  * Frontend/Presentation
* launch/beta relevance;
* recommended future package.

Do not re-document unrelated thyroid, FT3-low, iron-low, TSAT, or antibody carry-forwards unless P1-24 directly changes their status.

## Phase 6 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-24_bio_oxygen_subsystem_signal_depth.md`

Keep it concise.

Maximum structure:

1. start state;
2. package evidence verified;
3. compiled card changes;
4. manifest/index changes;
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

P1-24 passes only if:

1. `risk_level: STANDARD` and `change_type: CONTENT` remain valid.
2. All writes remain within compiled card estate, tests, sprint artefacts and Automation Bus artefacts.
3. No backend runtime, scoring, signal evaluator, domain allowlist or frontend file is modified.
4. The three target production PSI packages are verified.
5. The three new source spec IDs are added exactly as named.
6. Source spec traceability is recorded.
7. Transferrin marker addition is explicitly governed by production PSI evidence.
8. Ferritin-high context depth is added from the two governed ferritin-high PSI packages.
9. No medical content is invented.
10. No new PSI opt-ins occur.
11. No scoring changes occur.
12. No domain allowlist changes occur.
13. No signal evaluator changes occur.
14. `p1_3_blood_iron_oxygen_card_evidence.yaml` is not modified.
15. `p1_24_blood_iron_oxygen_card_evidence.yaml` is created.
16. `estate_index_v1.yaml` points `wave1_bio_oxygen_carrying_capacity` to the P1-24 manifest.
17. Compiled card schema validation passes.
18. Estate index validation passes, if available.
19. Tests prove enriched subsystem evidence is emitted.
20. Tests prove existing bio-oxygen behaviour is not regressed.
21. Canonical test target is recorded.
22. Carry-forward manifest is created.
23. Build register is updated concisely.
24. Sprint report is concise.
25. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

## Validation commands

Run all relevant existing validation commands.

At minimum:

* compiled health-system card schema validation;
* compiled estate index validation, if available;
* governed subsystem evidence regression test;
* bio-oxygen domain/card tests;
* any new P1-24 test file if created;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to make validation pass.

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
