---
work_id: ARCH-RT-IDENTITY-PROV-1
branch: feature/arch-rt-identity-prov-1-runtime-identity-provenance-integrity
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
stage_b_mode: MODE_2
knowledge_bus_impact: YES
medical_review_gate: CONDITIONAL
---

# ARCH-RT-IDENTITY-PROV-1 — Runtime Identity and Provenance Integrity

## 1. Product outcome

Deliver one coherent runtime integrity outcome:

> Every active signal result must retain its activation-frame identity through downstream reasoning, clinician reporting, API contracts and frontend consumption, while carrying an honest, traceable provenance status that distinguishes explicit research authority from inferred, legacy, unresolved or blocked lineage.

This work package combines two dependent workstreams:

### Workstream A — Activation-frame preservation

Preserve `activation_key` and its source-spec frame through:

- signal interaction construction;
- root-cause compilation;
- report compilation;
- output-authority provenance construction;
- clinician-report contracts;
- API/DTO assembly;
- persistence and replay paths where present;
- frontend type contracts and render-only consumers;
- deterministic tests and golden evidence.

### Workstream B — Explicit provenance closure

Establish and enforce an honest provenance contract for the active launch-critical signal estate:

- explicit `source_spec_id` where deterministically evidenced;
- explicit classification of inferred, unresolved, legacy, or blocked lineage;
- no silent conversion of inferred lineage into explicit authority;
- compile-manifest reference consistency;
- beta-critical gate coverage;
- traceability from source authority to package, activation frame, runtime result, clinician report and output provenance.

This is a single outcome-based package, not two micro-sprints.

---

## 2. Why this package is required

The independently verified executable audits and subsequent prompt hardening established that:

1. `SignalRegistry` correctly stores signals by `activation_key`.
2. Duplicate activation keys fail closed.
3. Multiple frames can coexist at registry/evaluator level.
4. At least five downstream production surfaces lose or collapse frame-specific identity:
   - `backend/core/analytics/signal_interaction_builder.py`;
   - `backend/core/analytics/root_cause_compiler_v1.py`;
   - `backend/core/analytics/report_compiler_v1.py`;
   - `backend/core/analytics/output_authority_provenance_builder_v1.py`;
   - `backend/core/contracts/clinician_report_v1.py`, mirrored by `frontend/app/types/analysis.ts`, where a list of root-cause findings is reduced to a single optional finding.
5. The five known surfaces are not assumed exhaustive; a full consumer search is required.
6. The audited package estate contained 191 provenance rows and zero explicit `source_spec_id`.
7. Two provenance scanners exist and differ in classification taxonomy over the same estate.
8. `knowledge_bus/schema/package_manifest_schema.yaml` does not currently expose the `source_spec_id` field already required by accepted architecture policy.
9. `compile_manifest_ref` and `compile_manifest_path` naming are both present and require authority reconciliation.
10. Controlled beta cannot safely claim frame-correct reasoning or explicit provenance until these gaps are resolved.

The current authoritative programme baseline is:

```text
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
```

This work package must begin from that baseline.

---

## 3. Mandatory governance model

This package requires full Automation Bus governance and Knowledge Bus validation.

Required sequence:

1. Confirm branch, HEAD and clean repository state.
2. Complete Stage 1A authority preflight.
3. Complete Stage 1B repository reality check.
4. Complete **Stage B Mode 2 architecture hardening** before implementation.
5. Claude Code must harden this revised prompt and produce the evidence checklist.
6. Run Automation Bus kernel start only after hardening returns no blocking correction.
7. Execute Phase 1 discovery and produce the mandatory architecture-extension ADR.
8. Honour Internal STOP Gate 1 before behaviour changes.
9. Implement only the approved design.
10. Run Knowledge Bus validators for every modified package or governed knowledge artefact.
11. Honour Internal STOP Gate 2 before any medical-authority or frame-binding promotion.
12. Complete post-implementation closure protocol.
13. Run kernel finish and deterministic gates.
14. Obtain independent Claude audit.
15. Do not merge without explicit human authority.

Required hardening invocation:

> **harden work_id: ARCH-RT-IDENTITY-PROV-1 — Stage B Mode 2; verify subordinate ADR authority, runtime identity, clinician-report cardinality, provenance schema migration, compile-manifest naming, fail-closed behaviour, and evidence checklist**

---

## 4. Governing authority and required reading

Read every applicable file in full before implementation.

### Current programme baseline and audits

```text
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md
docs/audit-papers/CLAUDE_CODE_independent_executable_architecture_assurance_audit.md
docs/audit-papers/ARCH-GOV-BASELINE-1_implementation_and_verification_report.md
docs/audit-papers/ARCH-GOV-BASELINE-1_historical_governance_exception_record.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

### Governing architecture and knowledge contracts

Locate and read the current repository versions of:

```text
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md

docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_identity_and_registry_architecture.md
docs/architecture/ADR-RT-003_hypothesis_and_root_cause_transition_architecture.md
docs/architecture/ADR-RT-004_compile_manifest_and_provenance_policy.md

knowledge_bus/compiled/estate_index_v1.yaml
knowledge_bus/schema/package_manifest_schema.yaml
knowledge_bus/research/investigation_specs/investigation_spec_schema_v3.0.0.yaml

backend/core/knowledge/signal_activation_identity_v1.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/signal_interaction_builder.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/contracts/clinician_report_v1.py
backend/core/knowledge/launch_estate_v1.py
backend/core/knowledge/package_provenance_scan_v1.py
backend/core/knowledge/compiled_hypothesis.py
backend/core/knowledge/root_cause_registry_v1.py
frontend/app/types/analysis.ts
```

If an ADR filename differs slightly from the names above, resolve the actual accepted file path and record the correction before proceeding.

### DTO, persistence, replay and frontend consumers

Locate and read all production consumers of:

```text
activation_key
signal_id
source_spec_id
compile_manifest_ref
compile_manifest_path
provenance
root_cause
root_causes
signal_interactions
signal_results
clinician_report
```

This must include:

- backend DTO models and serializers;
- clinician-report contracts;
- API response builders;
- persistence or replay contracts;
- report DTOs;
- frontend result consumers;
- any audit/evidence payloads.

### Pass 3 protocol status

`KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` remains DRAFT.

It may be consulted as supporting design input but must not be treated as approved promotion authority.

No PSI activation or Pass 3 promotion is authorised by this package.

---

## 5. Architectural subordination rule

The new ADR required by this package is an **implementation-extension ADR** subordinate to accepted ADR-RT-001 through ADR-RT-004.

It must not reopen settled decisions on:

- research-to-runtime authority;
- activation identity;
- registry keying;
- rejection of one-frame-per-direction simplification;
- compiled versus legacy hypothesis transition;
- compile-manifest authority;
- explicit provenance policy.

If current code makes an accepted ADR impossible to implement as written, STOP and escalate for human architecture adjudication.

The package may extend accepted policy into downstream contracts, schema migration and runtime enforcement. It may not replace accepted policy by convenience.

---

## 6. Stage 1A — Authority preflight

Before changing code, report:

1. The current authoritative source of activation identity.
2. The exact accepted decisions in ADR-RT-002 that this package must operationalise.
3. The exact accepted decisions in ADR-RT-003 that constrain root-cause migration and frame binding.
4. The exact accepted decisions in ADR-RT-004 that constrain `source_spec_id`, compile manifests and provenance.
5. The current authoritative package provenance scanners.
6. The difference between:
   - `launch_estate_v1.scan_package_provenance`;
   - `package_provenance_scan_v1.scan_all_package_provenance`.
7. The authoritative schema fields currently available for:
   - package source authority;
   - investigation-spec identity;
   - compile-manifest identity;
   - runtime activation identity;
   - output provenance.
8. Whether package manifests currently permit explicit `source_spec_id`.
9. Why the manifest schema extension required by ADR-RT-004 is absent despite prior ARCH-RT work.
10. Whether signal-library entries or compiled artefacts already carry source-spec identity.
11. Whether runtime activation-key construction currently infers identity when explicit provenance is absent.
12. Whether `knowledge_bus/current/latest_knowledge_status.json` exists and is authoritative on the current branch.
13. Which launch-critical package or signal set is actually consumed by production runtime.
14. Which documents or code comments still describe compiled vitamin-D WHY as shadow-only despite active runtime promotion.
15. Where `compile_manifest_ref` is used.
16. Where `compile_manifest_path` is used.
17. Whether those fields are:
    - aliases;
    - internal path versus stable logical reference;
    - genuinely conflicting contract names.
18. Whether BUILD_DELIVERABLE_REGISTER lacks historical continuity entries for ARCH-RT-1, ARCH-RT-2 and ARCH-RT-3.
19. Whether any authority conflict requires human adjudication before implementation.

If the package manifest schema cannot represent the accepted explicit provenance contract, this package owns a safe versioned or backward-compatible schema correction.

---

## 7. Stage 1B — Repository reality check

Reproduce the current defects before modifying anything.

At minimum prove:

### Multi-frame behaviour

- distinct frames sharing one `signal_id` can coexist in `SignalRegistry`;
- duplicate `activation_key` collisions fail closed;
- evaluator output preserves `activation_key`;
- each known collapse surface still loses frame identity:
  - interaction builder;
  - root-cause compiler;
  - report compiler;
  - output-authority provenance builder;
  - clinician-report contract and frontend mirror;
- the clinician-report path reduces an upstream list of root-cause findings to a single optional value;
- no later consumer reconstructs the lost frame safely;
- current tests prove registry coexistence but do not prove end-to-end frame preservation;
- a repository-wide search identifies any additional collapse surface not listed above.

### Provenance

- current package/provenance row count;
- current explicit `source_spec_id` count;
- classification counts from both scanners;
- active launch-critical packages/signals;
- which active paths have compile-manifest-backed provenance;
- which active paths use inferred, unparsed, unresolved or legacy provenance;
- whether runtime or DTO output can distinguish explicit from inferred provenance;
- whether any package marked blocked or unresolved is still consumed by production runtime;
- the current manifest schema gap;
- the current `compile_manifest_ref` / `compile_manifest_path` drift.

### Adjacent controls

- PSI remains absent from production imports;
- MR-BATCH-001B remains test-only;
- narrative Gemini remains default-off and non-authoritative;
- architecture gate passes before changes;
- current stale PSI activation-readiness test status is recorded but not automatically pulled into scope;
- missing ARCH-RT-1/2/3 continuity entries are historical documentation gaps, not evidence that the underlying code is absent.

If the audit findings no longer reproduce, STOP and escalate with evidence.

---

## 8. Mandatory Stage B Mode 2 architecture-extension ADR

Before implementation, create:

```text
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
```

The ADR must be drafted during Phase 1 and reviewed through prompt hardening before behaviour changes.

The ADR must explicitly state that it is subordinate to ADR-RT-001 through ADR-RT-004.

It must decide and document:

### A. Canonical runtime identity

The canonical unit of active signal identity must remain:

```text
activation_key = signal_id::source_spec_id
```

or the exact equivalent already fixed by ADR-RT-002.

The ADR must define:

- `signal_id` as signal-family identity;
- `source_spec_id` as activation-frame/research-source identity;
- `activation_key` as runtime frame identity;
- legacy behaviour when explicit `source_spec_id` is absent;
- compatibility and migration rules;
- collision behaviour;
- ordering guarantees;
- replay guarantees.

### B. Downstream preservation rule

Every downstream structure that can contain more than one frame for the same `signal_id` must:

- preserve `activation_key`;
- avoid unqualified dictionaries keyed solely by `signal_id`;
- avoid first-match selection by `signal_id`;
- avoid cardinality reduction from list to single item unless explicitly governed;
- expose family-level aggregation only where intentionally designed;
- make any family-level collapse deterministic, named, tested and non-lossy.

### C. Clinician-report cardinality rule

The ADR must define how clinician reports represent multiple authorised root-cause findings.

It must address:

- backend `ClinicianSectionsV1.root_cause`;
- upstream `List[RootCauseFindingV1]`;
- frontend `analysis.ts` mirror;
- backward compatibility for existing single-root-cause consumers;
- additive contract migration where possible;
- rendering behaviour when multiple frames or root causes coexist;
- prohibition on silent selection of a single “first” finding.

### D. Root-cause authority rule

The ADR must define how root-cause compilation selects the correct frame.

It must not:

- silently use the first result matching `signal_id`;
- attach one frame’s WHY to another frame;
- convert family-level legacy hypotheses into frame-specific authority without evidence.

Where a legacy root-cause asset is family-level only, the output must identify that status honestly.

### E. Provenance status model

Define a closed, deterministic provenance classification such as:

```text
EXPLICIT_SPEC
COMPILED_MANIFEST
SOURCE_DOCUMENT_DERIVED
LEGACY_INFERRED
UNRESOLVED
BLOCKED
```

Exact enum names may differ if repository conventions require it.

The model must distinguish:

- explicit authority;
- deterministic derivation;
- inference;
- missing/unresolved authority;
- promotion-blocked state.

### F. Manifest schema migration

Define the safe correction for the missing `source_spec_id` manifest field.

The ADR must specify:

- whether the existing manifest schema is extended additively;
- whether a versioned schema revision is required;
- how historical promoted packages remain valid;
- how the bounded launch-critical cohort migrates;
- how legacy packages are represented without falsely claiming explicit provenance;
- how Knowledge Bus validation distinguishes old and new schema states.

### G. Compile-manifest naming authority

Define the canonical role of:

```text
compile_manifest_ref
compile_manifest_path
```

The ADR must state whether:

- one is the stable logical reference and one an internal path;
- one is deprecated;
- aliases are temporarily accepted;
- migration must be additive;
- consumer-facing DTOs must exclude filesystem paths.

Do not perform a blind global rename.

### H. Launch-critical enforcement policy

Define the minimum provenance requirement for:

- runtime execution;
- internal development;
- controlled beta;
- medical-content promotion.

Do not automatically make all 191 packages runtime-fatal.

The design must:

- remain backward-compatible for non-beta legacy packages unless explicitly approved otherwise;
- fail closed for identity collisions;
- fail honestly for beta-readiness claims;
- prevent inferred lineage from being represented as explicit lineage.

### I. Migration boundary

The ADR must define:

- which active launch-critical packages/signals are in this sprint’s migration cohort;
- which packages remain legacy or unresolved;
- how unresolved items are recorded;
- whether any active item must be blocked from controlled beta;
- how later packages inherit the explicit provenance requirement.

---

## 9. Internal STOP Gate 1 — Architecture approval

After the ADR and migration inventory are drafted, STOP before production changes if any of the following applies:

1. The canonical identity contract conflicts with ADR-RT-002.
2. The proposed WHY handling conflicts with ADR-RT-003.
3. The proposed provenance contract conflicts with ADR-RT-004.
4. The canonical identity contract requires changing medical signal meaning.
5. Two active frames cannot be distinguished from existing source evidence.
6. Root-cause frame selection requires new medical interpretation.
7. Explicit provenance cannot be established without guessing or unsupported authority.
8. Package schema changes would invalidate promoted immutable packages without a migration mechanism.
9. Runtime fail-closed enforcement would disable a material part of the application.
10. DTO or clinician-report changes would be breaking without a compatibility plan.
11. Replay compatibility cannot be preserved.
12. The migration cohort cannot be bounded safely.
13. Human approval is required for displaying simultaneous frames or multiple root causes.
14. `compile_manifest_ref` / `compile_manifest_path` semantics cannot be reconciled safely.
15. The new ADR would re-decide accepted policy rather than extend it.

If none apply, record `STOP_GATE_1: PASS` in the implementation report and continue.

---

## 10. Workstream A — Activation-frame preservation

### Deliverable A1 — Canonical signal-result indexing

Replace downstream lossy indexing with an explicit structure that supports:

- lookup by `activation_key`;
- grouping by `signal_id`;
- deterministic ordering;
- legacy single-frame compatibility;
- explicit detection of duplicate or malformed activation identity.

Do not scatter bespoke fixes across individual files.

Prefer one shared, tested helper or domain object used by all affected consumers.

### Deliverable A2 — Signal interaction preservation

Update signal-interaction construction so simultaneous frames are not overwritten.

The interaction output must:

- retain participating `activation_key`s;
- preserve signal-family identity;
- distinguish frame-level interaction from family-level interaction;
- remain deterministic;
- avoid changing medical interaction rules unless explicitly required and approved.

### Deliverable A3 — Root-cause frame selection

Update root-cause compilation so:

- compiled frame-specific hypotheses match by `activation_key` or explicit frame identity;
- legacy family-level hypotheses are labelled as family-level;
- no first-match-by-`signal_id` behaviour remains where multiple frames exist;
- ambiguous multi-frame WHY fails safely or returns an explicit unresolved/family-level status;
- no new medical WHY content is created.

### Deliverable A4 — Report compilation

Update report compilation so:

- internal maps do not overwrite same-family frames;
- report sections retain frame identity;
- family-level presentation is explicitly aggregated rather than accidental;
- existing single-frame outputs remain stable where clinically and contractually appropriate.

### Deliverable A5 — Output authority and provenance builder

Update output-authority indexing so:

- evidence rows are keyed by `activation_key`;
- provenance can be traced per frame;
- same-family frames do not overwrite each other;
- family-level summaries are explicit derived views.

### Deliverable A6 — Clinician-report contract migration

Update clinician-report contracts so:

- multiple authorised root-cause findings can be represented without loss;
- the backend no longer collapses an upstream list into one optional value;
- frontend types mirror the additive backend contract;
- legacy single-root-cause clients remain supported where practical;
- no arbitrary first-item selection is introduced;
- frontend remains render-only.

### Deliverable A7 — DTO, persistence and replay compatibility

Update applicable contracts to preserve activation identity.

Requirements:

- additive schema changes are preferred;
- legacy fields may remain temporarily for compatibility;
- no client should infer activation identity from free text;
- replay of old single-frame records must remain deterministic;
- new multi-frame records must round-trip without loss;
- frontend must not calculate clinical meaning.

---

## 11. Workstream B — Explicit provenance closure

### Deliverable B1 — Canonical provenance contract

Implement the ADR provenance classification in the appropriate schema/model layer.

Each active signal result or output-authority record must be able to state:

- provenance status;
- `source_spec_id` when explicit;
- source document or package reference where applicable;
- canonical compile-manifest reference where applicable;
- package identifier;
- whether lineage is explicit, derived, inferred, unresolved or blocked.

Do not expose internal filesystem paths to consumer-facing UI.

### Deliverable B2 — Package manifest schema correction

Correct the absent `source_spec_id` manifest field through a safe, governed migration.

Requirements:

- preserve validity of historical packages where required;
- prefer additive or versioned schema evolution;
- validate the bounded launch-critical cohort;
- do not rewrite promoted package history silently;
- document why prior ARCH-RT continuity claimed the extension while the live schema lacked it;
- add tests preventing regression of the required field/contract.

### Deliverable B3 — Scanner reconciliation

Reconcile the two provenance scanners so:

- their purposes are explicit;
- overlapping facts use consistent terminology;
- materially conflicting classification of the same package is eliminated or deliberately explained;
- one authoritative beta-readiness view is defined;
- tests identify accidental taxonomy drift.

Do not delete useful scanner functionality merely to produce matching counts.

### Deliverable B4 — Compile-manifest contract normalisation

Reconcile `compile_manifest_ref` and `compile_manifest_path`.

Requirements:

- identify the canonical stable logical reference;
- retain internal paths only where technically necessary;
- prevent filesystem paths leaking into consumer DTOs;
- support temporary aliases if backward compatibility requires them;
- add deterministic validation and migration tests;
- avoid blind global renaming.

### Deliverable B5 — Active launch-cohort inventory

Produce:

```text
docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md
```

For each active launch-critical package/signal include:

- package ID;
- signal ID;
- source-spec ID;
- activation key;
- provenance status;
- source authority reference;
- compile-manifest reference where present;
- runtime consumer;
- beta eligibility;
- unresolved action.

This inventory must be generated or verified deterministically from repository evidence.

### Deliverable B6 — Explicit provenance migration

For the bounded launch-critical cohort:

- populate explicit `source_spec_id` only where repository evidence proves the mapping;
- update package/schema fields through Knowledge Bus governance;
- preserve immutable-history principles;
- create versioned migration or replacement artefacts where required;
- validate every modified package.

Do not invent source-spec IDs.

Where explicit mapping cannot be proven:

- classify the item `UNRESOLVED` or `BLOCKED`;
- keep runtime behaviour backward-compatible unless the ADR says otherwise;
- mark it ineligible for controlled beta if required.

### Deliverable B7 — Runtime provenance propagation

Propagate honest provenance through:

```text
package/source authority
→ activation identity
→ signal result
→ interaction/root-cause/report
→ clinician report
→ output-authority provenance
→ DTO/replay evidence
```

Do not make the frontend calculate or repair provenance.

### Deliverable B8 — Beta-readiness gate

Add a deterministic gate that evaluates the launch-critical cohort against the ADR provenance policy.

The gate must:

- fail if explicit lineage is falsely claimed;
- fail if activation keys collide;
- fail if a launch-critical multi-frame result is collapsed;
- fail if clinician-report cardinality discards authorised findings;
- report unresolved/blocked items precisely;
- distinguish runtime compatibility from controlled-beta eligibility;
- avoid blocking unrelated legacy packages merely because they are outside the launch cohort.

Integrate the gate into the existing architecture validation flow without creating a duplicate governance system.

---

## 12. Historical continuity reconciliation

The BUILD register contains no historical entries for ARCH-RT-1, ARCH-RT-2 and ARCH-RT-3 despite those accepted architecture outcomes being merged.

Do not fabricate retrospective contemporaneous entries.

Create one concise reconciliation note within the Package 2 BUILD-register entry or a directly linked continuity note that:

- identifies the accepted ADR/work-package outcomes;
- cites repository commit or document evidence;
- states that the entries were historically absent;
- does not claim that original closure evidence existed when it did not;
- does not alter the authority of ADR-RT-001 through ADR-RT-004.

This is a continuity repair subordinate to Package 2, not a separate sprint.

---

## 13. Internal STOP Gate 2 — Medical and authority review

Before promoting any explicit source mapping or changing root-cause frame binding, STOP if:

- source evidence supports more than one plausible `source_spec_id`;
- a legacy family-level hypothesis would be assigned to a specific frame;
- multi-frame interaction semantics would change;
- clinician-report aggregation would change clinical emphasis;
- a package would move from blocked/unresolved to beta-eligible without clear research authority;
- any new medical statement or interpretation is required.

For mechanical identity/cardinality preservation with no medical meaning change, medical review is not required.

For ambiguous frame binding or authority promotion, obtain targeted medical review before continuing.

Record each reviewed item and decision.

---

## 14. Test requirements

Create or update tests proving the production path, not only isolated helpers.

### Required multi-frame tests

At minimum cover:

1. Two distinct activation frames sharing one `signal_id` load simultaneously.
2. Both can fire independently.
3. Interaction building preserves both.
4. Root-cause compilation does not attach the wrong frame.
5. Report compilation preserves both or performs an explicit named aggregation.
6. Output-authority provenance retains both.
7. Clinician-report contracts retain all authorised root-cause findings.
8. Frontend type contracts accept and preserve the additive multi-finding shape.
9. DTO serialization retains both frames.
10. Persistence/replay round-trip retains both.
11. Duplicate activation keys fail closed.
12. Legacy single-frame output remains compatible.
13. Unresolved frame-specific WHY is represented honestly.
14. Ordering is deterministic across repeated runs.
15. Any additional collapse surface found in Stage 1B is covered.

### Required provenance tests

At minimum cover:

1. Explicit provenance is reported as explicit.
2. Derived provenance is not reported as explicit.
3. Inferred provenance is labelled inferred.
4. Unresolved provenance is not silently promoted.
5. Canonical compile-manifest references resolve.
6. Internal compile-manifest paths do not leak into consumer DTOs.
7. Source-spec IDs resolve to authoritative investigation specs.
8. Package-manifest schema accepts the new governed contract.
9. Historical package compatibility is preserved.
10. Scanner outputs agree on shared facts.
11. Launch-critical gate fails on false explicit claims.
12. Launch-critical gate reports blocked items without blocking unrelated legacy packages.
13. Runtime result → DTO → clinician report → replay provenance round-trip is lossless.
14. Schema and naming drift regression tests prevent recurrence.

### Regression requirements

Run and preserve:

- architecture validation gate;
- launch-estate gate;
- signal evaluator and activation identity suites;
- interaction-map tests;
- root-cause compiler tests;
- report compiler tests;
- clinician-report contract tests;
- output-authority provenance tests;
- compiled hypothesis tests;
- card-evidence tests;
- replay/auditability tests;
- golden-panel tests;
- PSI isolation tests;
- MR-BATCH isolation tests;
- narrative NO-LLM tests;
- relevant frontend type/render tests.

The pre-existing stale `test_validate_staged_psi_activation_readiness.py` failures may be refreshed only if the changed provenance inventory directly alters the same authoritative counts. Otherwise leave them as a disclosed carry-forward.

Do not weaken assertions to obtain green tests.

---

## 15. Knowledge Bus requirements

For each modified package or governed knowledge artefact:

1. Run the canonical package validator directly.
2. Record exact command and PASS/FAIL output.
3. Do not use the unreliable lifecycle controller as promotion authority for `pkg_*`.
4. Do not promote without validator PASS.
5. Do not update `latest_knowledge_status.json` unless an actual package promotion occurs.
6. Do not treat `backend/artifacts/knowledge_status.json` as a substitute for the authoritative current status file.
7. Preserve package immutability:
   - prefer versioned replacement/migration artefacts;
   - never silently rewrite historical meaning.
8. Do not activate PSI.
9. Do not promote MR-BATCH-001B.
10. Do not use the DRAFT Pass 3 protocol as sole promotion authority.

---

## 16. Expected implementation scope

Likely production files include, subject to repository reality:

```text
backend/core/knowledge/signal_activation_identity_v1.py
backend/core/analytics/signal_interaction_builder.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/contracts/clinician_report_v1.py
backend/core/knowledge/launch_estate_v1.py
backend/core/knowledge/package_provenance_scan_v1.py
backend/core/pipeline/
backend/core/models/
backend/app/models/
backend/app/routes/
backend/scripts/run_architecture_validation_gate.py
backend/scripts/validate_day_one_architecture.py
knowledge_bus/schema/package_manifest_schema.yaml
knowledge_bus/packages/<bounded launch-critical cohort only>
frontend/app/types/analysis.ts
frontend/app/<direct render-only consumers only>
docs/architecture/
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
backend/tests/
frontend tests
```

This list is indicative, not permission for broad edits.

Every touched file must be directly necessary to the stated outcome.

---

## 17. Forbidden scope

Do not:

- activate or wire PSI;
- promote Pass 3 intelligence;
- promote MR-BATCH-001B;
- create new medical prose;
- change medical thresholds;
- change signal activation criteria;
- expand clinical hypotheses;
- migrate the remaining legacy WHY estate beyond what is required for correct frame identity;
- redesign the results page;
- enable Gemini;
- change narrative LLM authority;
- perform broad package cleanup unrelated to the launch-critical cohort;
- fix the dangling v0_4 reference inside the LOCKED Automation Bus SOP;
- select or author Package 3;
- claim controlled-beta readiness.

Do not use this package to solve Layer B prose routing or modifier binding. Those belong to Package 3 after identity and provenance are settled.

---

## 18. Acceptance criteria

The package is complete only when all applicable criteria pass.

### Architecture decision

- [ ] ADR exists and is explicitly subordinate to ADR-RT-001 through ADR-RT-004.
- [ ] No accepted architecture policy was reopened without STOP escalation.
- [ ] Migration cohort is explicitly bounded.
- [ ] STOP Gate 1 is recorded.
- [ ] Any required medical/authority decisions are recorded through STOP Gate 2.

### Multi-frame preservation

- [ ] No affected downstream production consumer accidentally collapses distinct activation frames by bare `signal_id`.
- [ ] No clinician-report contract silently reduces multiple authorised root-cause findings to one.
- [ ] Family-level aggregation is explicit, named and tested.
- [ ] Root-cause frame binding cannot attach the wrong frame.
- [ ] Output-authority provenance is frame-specific.
- [ ] DTO, clinician-report and replay paths preserve activation identity.
- [ ] Frontend types mirror the additive backend contract and remain render-only.
- [ ] Legacy single-frame behaviour remains compatible.
- [ ] Duplicate activation keys still fail closed.
- [ ] Repository-wide search confirms no unaddressed collapse surface remains in the launch path.

### Provenance

- [ ] Package-manifest schema can represent the accepted explicit provenance contract.
- [ ] Historical package compatibility is preserved.
- [ ] Provenance status distinguishes explicit, derived, inferred, unresolved and blocked lineage.
- [ ] No inferred provenance is presented as explicit.
- [ ] Both scanners have reconciled shared facts and documented distinct purposes.
- [ ] `compile_manifest_ref` and `compile_manifest_path` have a governed canonical relationship.
- [ ] Consumer DTOs do not leak internal filesystem paths.
- [ ] Launch-critical inventory exists and is reproducible.
- [ ] Every launch-critical item has an explicit status.
- [ ] Every resolvable launch-critical item has evidence-backed `source_spec_id`.
- [ ] Unresolvable items are not guessed and are marked beta-ineligible where required.
- [ ] Compile-manifest and source-spec references resolve.
- [ ] Runtime, clinician-report and DTO outputs propagate provenance honestly.

### Continuity

- [ ] Missing ARCH-RT-1/2/3 BUILD continuity is reconciled without fabricated retrospective closure claims.

### Gates and regression

- [ ] New launch-critical identity/provenance gate passes.
- [ ] Architecture validation gate passes.
- [ ] Launch-estate gate passes.
- [ ] Required multi-frame end-to-end tests pass.
- [ ] Required provenance tests pass.
- [ ] Clinician-report contract tests pass.
- [ ] Root-cause, report, card, replay and golden regressions pass.
- [ ] PSI remains unwired.
- [ ] MR-BATCH-001B remains test-only.
- [ ] Gemini remains non-authoritative.

### Scope integrity

- [ ] No new medical content was authored.
- [ ] No signal threshold or firing rule changed.
- [ ] No broad legacy WHY migration occurred.
- [ ] No PSI activation occurred.
- [ ] No Package 3 implementation was started.
- [ ] Controlled beta was not declared.

---

## 19. STOP conditions

STOP immediately and report evidence if:

1. Stage 1A authority cannot identify trustworthy source-spec authority.
2. The current branch does not contain the merged Package 1 baseline.
3. ADR-RT-002, ADR-RT-003 or ADR-RT-004 conflicts with the proposed design.
4. Multi-frame collapse cannot be fixed additively without changing medical meaning.
5. Root-cause frame selection is clinically ambiguous.
6. Clinician-report multi-finding support requires product-policy selection without approval.
7. Explicit `source_spec_id` mappings would need to be invented.
8. Package immutability cannot be preserved.
9. A schema migration would invalidate active packages without a safe versioned path.
10. Runtime compatibility would require silently discarding a frame.
11. Replay compatibility cannot be maintained.
12. A launch-critical package has no defensible authority but is required for continued runtime operation.
13. `compile_manifest_ref` / `compile_manifest_path` cannot be reconciled without a breaking change.
14. Knowledge Bus validation fails for a modified package.
15. Architecture or launch-estate gates fail for an unexplained reason.
16. PSI, MR-BATCH-001B or Gemini would need to be activated.
17. The work expands into prose routing, modifiers or broad WHY content migration.
18. Unrelated working-tree changes or tooling leakage are present.
19. Human product or medical policy approval is required and has not been obtained.
20. The package would re-decide accepted ADR policy instead of extending it.

---

## 20. Required implementation report

Create:

```text
docs/audit-papers/ARCH-RT-IDENTITY-PROV-1_implementation_and_verification_report.md
```

Include:

1. Executive outcome.
2. Baseline branch and SHA.
3. Authority preflight.
4. Accepted ADR decisions inherited.
5. Reality-check evidence.
6. Stage B Mode 2 architecture-extension decision summary.
7. STOP Gate 1 disposition.
8. Migration cohort.
9. Files changed.
10. Workstream A implementation.
11. Clinician-report contract migration.
12. Workstream B implementation.
13. Manifest-schema migration.
14. Compile-manifest naming reconciliation.
15. Knowledge Bus validation evidence.
16. Medical/authority review decisions.
17. Before/after multi-frame evidence.
18. Before/after clinician-report cardinality evidence.
19. Before/after provenance evidence.
20. Commands and exit codes.
21. Acceptance-criteria table.
22. STOP-condition assessment.
23. Remaining unresolved or beta-ineligible items.
24. Historical BUILD continuity reconciliation.
25. Confirmation that PSI, MR-BATCH and Gemini authority remain unchanged.
26. Carry-forwards for Package 3.

---

## 21. Build-register continuity

Append one concise entry to:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Record:

- outcome delivered;
- inherited ADR authority;
- activation-frame preservation status;
- clinician-report cardinality status;
- provenance cohort and unresolved count;
- manifest-schema migration status;
- compile-manifest naming decision;
- gates/tests run;
- medical review decisions;
- historical ARCH-RT-1/2/3 continuity reconciliation;
- remaining Package 3 dependencies;
- no beta authorisation;
- no PSI or MR-BATCH promotion.

The BUILD register remains continuity only, not architecture authority.

---

## 22. Closure requirements

Before `finish`, complete the mandatory Post-Implementation Closure Protocol.

At minimum report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify all modified, staged, untracked, tooling and out-of-scope files.

Do not use stash as routine closure convenience.

Do not run `finish` until:

- branch matches this prompt;
- Stage B Mode 2 and STOP gates are recorded;
- all modified packages have validator evidence;
- all required gates and tests pass;
- no unrelated files are present;
- implementation report and BUILD register entry are complete;
- working tree is closure-ready.

After successful `finish`, handle the kernel-generated COMPLETE status exactly as required by the Automation Bus SOP and confirm the branch is clean.

Do not merge without explicit human authority.
