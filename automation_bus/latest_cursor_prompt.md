---
work_id: CLIN-PRIORITY-CORE-1
branch: feature/clin-priority-core-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CLIN-PRIORITY-CORE-1
## Cross-Domain Clinical Findings and Prioritisation — START Phase

## 1. Authority and execution boundary

This is the Automation Bus START prompt for `CLIN-PRIORITY-CORE-1`.

It authorises Cursor implementation only after:

1. Claude Code has hardened this exact work package using:

   `harden work_id: CLIN-PRIORITY-CORE-1 — verify source content and produce evidence checklist`

2. `automation_bus/latest_prompt_hardening.json` records:

   `"status": "HARDENED"`

3. The kernel has successfully run:

   `python backend/scripts/run_work_package.py start`

4. `automation_bus/state/work_package_active.json` exists and matches:

   - `work_id: CLIN-PRIORITY-CORE-1`
   - `branch: feature/clin-priority-core-1`
   - the current repository HEAD

Cursor must not implement before kernel-issued execution authority exists.

This START phase authorises work through:

- Phase 0 verification;
- hepatic pilot;
- remaining five-domain rollout;
- `APPROVED_SCENARIO_ESTATE_COVERAGE: 109/109`.

After those outcomes are complete, Cursor must STOP for independent review.

This START phase does **not** authorise:

- longitudinal Checkpoint 4 implementation beyond any minimum scaffolding strictly necessary for the START architecture;
- frontend Checkpoint 5 completion beyond additive DTO compatibility or minimal non-behavioural scaffolding strictly required to keep existing builds green;
- Automation Bus `finish`;
- merge;
- release;
- any new clinical, product, regulatory or legal decision.

## 2. Product outcome

Construct the governed runtime layer that converts current blood-test signals into consolidated clinical findings and surfaces those findings in the already-approved clinical priority order.

HealthIQ is a secondary, consumer-facing blood-test interpretation application. Users upload blood-test results produced elsewhere. HealthIQ interprets, consolidates, prioritises and explains those results to support informed discussion with a healthcare professional.

HealthIQ does not:

- provide blood testing;
- replace the originating laboratory or clinician;
- diagnose autonomously;
- prescribe or manage treatment;
- operate an emergency escalation service;
- route users to emergency or clinical services;
- monitor whether users act on advice.

Do not introduce behaviour that conflicts with this product boundary.

## 3. Governing authority

Read in full before implementation and apply in this precedence order:

1. `docs/discussion documents/HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md`
2. `docs/discussion documents/HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md`
3. `docs/discussion documents/HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md`
4. `docs/discussion documents/HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md`
5. `docs/discussion documents/HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md`
6. `docs/discussion documents/HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_2.md`
7. `docs/discussion documents/HEALTHIQ_CROSS_DOMAIN_PRODUCT_RATIFICATION_CLINICIAN_FIRST_v1_0.md`
8. `docs/architecture/CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md`
9. `docs/architecture/CLIN-PRIORITY-IMPLEMENTATION-RESET-1_repository_inspection.md`
10. `docs/sprints/CLIN-PRIORITY-CORE-1_cross_domain_clinical_findings_and_prioritisation_v1_1.md`
11. `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_vNEXT_1.md`
12. `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
13. `docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md`
14. `docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md`
15. `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md`

Also read the six domain prioritisation rulesets referenced by the closure report.

Use actual repository paths where names differ. Do not create duplicate authority files to match the paths above.

The six domain rulesets are subordinate evidence. Their content may be compiled only where incorporated, preserved, adjudicated or left unchanged by the higher-order ratified package.

Do not reopen or reinterpret any approved clinical or product decision.

## 3A. Signal preservation and non-subordination

### 3A.1 Purpose

The Cross-Domain Clinical Findings and Prioritisation layer sits **above** the existing signal estate. Its job is to organise, consolidate and prioritise signals that already fire, so the user knows what to focus on. It is **not** a second activation authority.

This package must not switch off, suppress, retire, subordinate or rewrite existing runtime signals or supporting signals.

### 3A.2 Required invariants

- All currently wired, promoted, runtime-eligible signals and supporting signals must continue to fire under the same conditions as before this package.
- Existing activation thresholds, biomarker requirements, activation keys, package lineage and runtime eligibility must remain unchanged.
- Prioritisation tier, finding role and consolidation must not act as activation gates. A finding's tier, role, or consolidation state may change how it is *presented*; it must never determine whether the underlying signal *fires*.
- An independent signal must not become supporting-only unless an explicit approved relationship rule (a named combination/consolidation rule in the ratified authority, e.g. `HAEM-OV-*`, `RE-OV-*`, `IRIN-OV-*`, `XD-C*`) requires that treatment for the current result set. Absent such a rule, an independently-firing signal remains an independent finding.
- Constituent signals must remain identifiable and provenance-complete after consolidation — consolidating frames into one finding must never destroy the ability to recover which signals/activation-keys contributed to it.
- No Knowledge Bus promotion status may change as a result of this package. This package is a runtime consumer of the existing promoted estate, not a promotion authority.
- The 109 approved scenarios validate concern-construction and prioritisation *behaviour*. They do not authorise signal suppression, retirement, or threshold changes — a scenario passing must never be achieved by altering what an existing signal does.
- `SIGNALS_INTENTIONALLY_RETIRED` must be `0` for this package, unless a pre-existing explicit retirement authority (a named, dated decision in a ratified document, distinct from this package) is cited as the basis.

### 3A.3 Revised authority hierarchy

Distinguish these five layers; do not let one silently override another:

1. **The existing authorised signal activation and promotion estate defines what fires.** `SignalRegistry`, activation keys, package promotion status, and runtime eligibility as they exist today are the ground truth for signal activation and are not reopened by this package.
2. **Domain clinical authority defines what active signals mean.** The six domain rulesets, subordinate to the ratified cross-domain package, supply clinical meaning for a signal once it has fired.
3. **Cross-domain authority defines how findings are consolidated and prioritised.** Contract v0.6.3, ruleset v0.5, adjudication register v0.4, closure report v0.4 govern consolidation, tiering, urgency, severity, and lead selection — all operating on findings built from signals that already fired under layer 1.
4. **Product authority defines presentation.** Clinician-first v1.0 governs prominence, ordering display, and lead/co-lead/no-forced-lead presentation — never activation.
5. **Acceptance scenarios validate the implementation.** The 109-scenario estate proves concern-construction and prioritisation behave correctly; it does not independently authorise signal retirement, threshold change, or promotion-status change at any layer above.

## 4. Stage 1A authority preflight

Before changing code, Cursor must verify and record in the implementation evidence:

### 4.1 Authoritative clinical source

Confirm the exact repository paths and version/status metadata for:

- the clinical prioritisation contract;
- cross-domain ruleset;
- HMR adjudication register;
- closure report;
- approval pack v1.2;
- clinician-first product ratification;
- all six domain rulesets.

Confirm no later competing or duplicate authority source governs the same clinical-finding and prioritisation behaviour.

### 4.2 Runtime authority path

Confirm:

- `backend/core/analytics/signal_evaluator.py` supplies the activation-key-keyed upstream signal registry;
- `backend/core/analytics/insight_graph_builder.py` is the sole current `InsightGraphV1` assembly path;
- `backend/core/contracts/insight_graph_v1.py` is the canonical InsightGraph contract;
- `backend/core/models/results.py` is the relevant response DTO path;
- no parallel clinical-finding constructor already exists.

If a parallel finding authority, loader or constructor exists, STOP before implementation and report it.

### 4.3 Compiled prioritisation authority

Determine the canonical location, schema, compiler and loader for the new compiled prioritisation artefact.

The implementation must produce one authoritative compiled prioritisation source consumed by one runtime loader.

Do not:

- hard-code the 109 scenarios into runtime logic;
- create one authority file per test;
- make domain rulesets runtime-authoritative independently;
- create a second clinical-prioritisation loader;
- allow tests and runtime to load different authority sources.

If the repository does not contain enough architecture to establish one canonical compiled artefact path without guessing, STOP.

### 4.4 Signal activation baseline

Before Cursor changes any concern-construction behaviour, it must create a repository-derived baseline inventory of every currently active and promoted signal and supporting signal.

For each record, capture:

- signal ID;
- activation key;
- package/source;
- promotion and runtime status;
- primary biomarker;
- supporting biomarkers/signals;
- derived-marker dependencies;
- existing DTO or frontend exposure;
- regression fixture or test evidence showing current activation.

This inventory is mandatory implementation evidence. It must be used as the non-regression baseline for the closure metrics in §13/§15 — every signal and supporting signal in the baseline must still be shown firing, under the same conditions, at Checkpoint 3 closure. Build this inventory during Checkpoint 0 (§9), before any concern-construction code changes.

## 5. Stage 1B baseline reality check

Confirm on the current branch that the problem still exists:

- no canonical `ClinicalFinding` model implements the approved contract;
- no `ConsolidatedConcernSet` exists;
- no runtime layer separates urgency, severity and tier;
- no finding-level same-domain and cross-domain consolidation exists;
- current lead selection still includes or depends on technical tiebreak behaviour;
- no finding-level insufficient-data versus indeterminate-severity state machine exists;
- no approved 109-scenario clinical-concern runner exists.

If these capabilities already exist and satisfy the approved specification, STOP and report the no-op or rescope condition.

## 6. Intelligence Core surface

This package changes Intelligence Core behaviour.

Affected surfaces include:

- signal-to-finding construction;
- governed-content compilation and loading;
- same-domain and cross-domain consolidation;
- urgency, severity and tier assignment;
- finding roles and relationships;
- serious-result classification;
- lead, co-lead and no-forced-lead selection;
- InsightGraph and AnalysisDTO output assembly;
- acceptance and regression harnesses.

Expected output changes:

- a new additive `clinical_concern_set`;
- deterministic clinical findings with full provenance;
- governed ordering and role assignment;
- no forced lead where no governed clinical distinguisher exists;
- preserved serious findings without downgrade or suppression;
- explicit missing-data and indeterminate states;
- quarantine-consistent constrained outputs.

## 7. In-scope START implementation

### 7.1 Canonical models

Create additive, version-stamped models for at least:

- `ClinicalFinding`;
- `ConsolidatedConcernSet`;
- finding provenance;
- finding role;
- urgency;
- severity or severity treatment;
- tier;
- missing-data or indeterminate state;
- serious-result state;
- consolidation and supporting/contextual relationships;
- dependency or quarantine state;
- lead/co-lead/no-forced-lead presentation state.

Preferred location:

- `backend/core/models/clinical_finding.py`

Use repository conventions and exact final paths determined during preflight.

Do not rename, remove or restructure existing `Insight`, `InsightGraphV1`, `AnalysisDTO`, report or clinician-report fields in START.

### 7.2 Compiled prioritisation artefact

Create the canonical governed prioritisation artefact schema, compiler and loader needed to transform the approved authority into deterministic runtime rules.

Requirements:

- stable rule and source identifiers;
- source document/version provenance;
- activation-key lineage where applicable;
- domain and cross-domain consolidation mappings;
- urgency and severity rules;
- tier algebra;
- role and lead-selection constraints;
- missing-data and indeterminate-state rules;
- overrides and prohibited behaviours;
- serious-result classification;
- quarantine/dependency states;
- compile-manifest and package provenance consistent with ADR-RT-004;
- deterministic ordering;
- fail-closed rejection of malformed, ambiguous or unsupported content.

Use the hepatic domain as the first real compiled vertical slice, then extend the same architecture to the remaining five domains.

Do not invent a new clinical rule to make compilation easier.

**Compilation scope boundary.** Compile only the rules necessary to reproduce the 109 approved scenarios (`HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_2.md`) and their governing structural context. Do not attempt to compile a domain's full band/threshold table merely because the domain ruleset presents it as a table. Any domain-ruleset band or threshold recorded as unset or unresolved (for example a value marked `[U]`) must be excluded from compilation and recorded as a follow-on item — never estimated, approximated, or inferred from an adjacent band.

### 7.3 Concern-construction service

Create one canonical concern-construction service between upstream signal evaluation and InsightGraph assembly.

Preferred location:

- `backend/core/analytics/concern_constructor.py`

The service must:

1. consume governed current-result inputs and activation-key provenance;
2. construct clinical findings;
3. apply same-domain consolidation;
4. apply cross-domain combination and duplicate rules;
5. separate urgency from severity;
6. assign the governed tier;
7. create supporting, contextual and independent-secondary relationships;
8. represent insufficient data and indeterminate severity distinctly;
9. preserve serious findings and attach bounded serious-result state;
10. select lead/co-lead/no-forced-lead according to approved authority;
11. produce a deterministic ordered visible concern set;
12. preserve complete rule and source provenance.

It must not reuse cluster-level arbitration scoring as clinical finding prioritisation.

It must not act as a second activation authority: it consumes signals that have already fired under the existing `SignalRegistry`/promotion estate (§3A.3 layer 1) and organises them; it must never decide whether a signal fires in the first place, and tier/role/consolidation assignment must never feed back into upstream activation.

### 7.4 InsightGraph and DTO integration

Extend additively:

- `backend/core/contracts/insight_graph_v1.py`
- `backend/core/analytics/insight_graph_builder.py`
- `backend/core/models/results.py`

Add:

`clinical_concern_set: Optional[ConsolidatedConcernSet]`

or the repository-conventional equivalent confirmed during implementation.

Requirements:

- one server-side construction call;
- no duplicate construction in report or frontend paths;
- deterministic serialisation;
- backward compatibility for existing consumers;
- explicit contract version stamp;
- provenance retained through DTO assembly.

### 7.5 Lead behaviour

Implement the approved product model:

- one lead where governed clinical authority identifies one;
- co-leads only where governed clinical rules permit;
- same-day co-equal groups preserved without arbitrary ranking;
- below the same-day band, the ordinary two-co-lead rule is a maximum, not a requirement;
- where three or more equally ranked non-same-day findings have no governed clinical distinguisher, do not force a lead and do not manufacture two co-leads;
- keep all clinically distinct findings visible in their governed tier.

Do not adapt or reuse `technical_tiebreak_lead` as the finding-level algorithm.

START may add backend compatibility mapping if required to prevent existing frontend breakage, but must not complete the frontend behaviour redesign. The frontend redesign belongs to FINISH.

### 7.6 Serious-result state

Implement a bounded data classification, not an escalation workflow.

Requirements:

- preserve governed severity, urgency and priority;
- never silently downgrade, suppress or convert a serious finding to no-concern;
- expose a deterministic serious-result state;
- support later consumer-safe presentation wording;
- preserve auditability and provenance;
- do not route users;
- do not choose services;
- do not manage escalation;
- do not monitor response;
- do not create territory-specific emergency logic.

Internal Tier 0 terminology may remain where the ratified clinical contract uses it.

Do not describe this implementation as preparation for a future HealthIQ-operated escalation service.

### 7.7 Quarantines

Preserve and prove existing quarantine behaviour for:

- cardiovascular-risk calculation;
- FIB-4 calculation;
- consumer-facing disease diagnosis;
- specialist pregnancy interpretation;
- any other R1-R6 constrained capability identified by the governing documents.

If a live consumer-facing FIB-4 or cardiovascular-risk calculation exists, apply the STOP condition in §12 before hepatic implementation.

Do not activate quarantined capabilities.

### 7.8 Acceptance harness

Create one clinical-prioritisation scenario harness modelled on:

- `backend/tools/run_arbitration_scenarios.py`
- `backend/tests/unit/test_arbitration_scenario_runner.py`
- `backend/tests/fixtures/arbitration_scenarios_v2.json`

The new harness must:

- load one canonical scenario fixture estate;
- enumerate every approved active scenario ID;
- run the real compiled prioritisation loader and concern-construction service;
- assert the complete expected field set;
- assert prohibited behaviours negatively;
- emit a deterministic manifest and per-scenario evidence;
- report pass/fail without skips;
- prove `APPROVED_SCENARIO_ESTATE_COVERAGE`.

Do not build 109 bespoke runtime code paths.

## 8. Approved scenario estate

The governing acceptance specification is:

`HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_2.md`

Required START exit:

`APPROVED_SCENARIO_ESTATE_COVERAGE: 109/109`

The harness must cover:

- 39 cross-domain scenarios;
- 6 formal haematology scenarios;
- 14 hepatic scenarios;
- 14 renal/electrolyte scenarios;
- 12 iron/inflammatory scenarios;
- 12 thyroid/endocrine scenarios;
- 12 active cardiometabolic/nutritional scenarios;
- the contract hepatic fixture and its documented duplicate relationship to `HEP-AS-1`.

Reconcile literal rows versus unique active scenarios exactly as the approved pack does.

No scenario may be silently skipped because a capability is quarantined. Quarantined scenarios must assert the approved constrained state.

## 9. Internal START checkpoints

### Checkpoint 0 — Phase 0 verification

Before new behavioural code:

- verify branch and clean-tree state;
- verify `SignalRegistry` activation-key behaviour;
- verify canonical authority paths and loaders;
- verify no parallel finding constructor exists;
- inspect all live FIB-4 and cardiovascular-risk code paths;
- verify forbidden-path boundaries;
- identify canonical existing regression commands;
- record baseline tests;
- **build the signal activation baseline inventory required by §4.4, before any concern-construction behaviour is changed.**

If Phase 0 passes, proceed.

### Checkpoint 1 — Hepatic pilot

Implement:

- canonical models;
- compiled artefact schema/compiler/loader;
- concern-construction service;
- serious-result state;
- additive InsightGraph/DTO integration;
- hepatic compiled rules;
- hepatic scenario fixtures and tests;
- contract hepatic regression fixture;
- deterministic evidence.

Required outcome:

- every active hepatic scenario passes;
- `CONTRACT-FIX-1` and `HEP-AS-1` retain their documented duplicate relationship;
- no existing cluster arbitration or WHY behaviour is repurposed;
- no quarantine is activated.

Commit Checkpoint 1 separately.

### Checkpoint 2 — Six-domain estate rollout

Extend the same architecture to:

- haematology;
- renal/electrolyte;
- iron/inflammatory;
- thyroid/endocrine;
- cardiometabolic/nutritional;
- cross-domain rules.

Required outcome:

- one canonical compiled prioritisation package;
- one canonical loader;
- one concern-construction service;
- all 109 approved active scenarios pass;
- zero skips;
- zero unresolved expectation differences;
- zero invented clinical or product rules;
- no-forced-lead behaviour matches `XD-AS-32`;
- serious findings are preserved and never downgraded;
- quarantined capabilities remain constrained.

Commit Checkpoint 2 separately.

### Checkpoint 3 — START evidence and STOP preparation

Produce evidence for independent review:

- branch and HEAD;
- changed-file inventory;
- compile-manifest and package provenance;
- exact test commands;
- test totals;
- scenario manifest showing 109/109;
- hepatic-pilot evidence;
- cross-domain ordering and consolidation evidence;
- no-forced-lead evidence;
- serious-result-state evidence;
- missing-data versus indeterminate evidence;
- quarantine negative assertions;
- regression summary;
- known carry-forwards;
- confirmation that longitudinal Checkpoint 4 and frontend Checkpoint 5 are not complete.

Do not run Automation Bus `finish`.

STOP after presenting the evidence.

## 10. Longitudinal boundary during START

The FINISH phase will implement the six explicitly governed longitudinal rules and report:

`GOVERNED_LONGITUDINAL_RULE_COVERAGE: 6/6`

START must not claim that result.

During START, only implement longitudinal code that is strictly necessary for:

- `RE-AS-3`;
- `RE-AS-5`;
- preserving existing prior-result data contracts;
- keeping the new finding architecture compatible with later FINISH integration.

Do not implement:

- new trend thresholds;
- generic score-band movement as a clinical finding;
- comprehensive trend interpretation;
- trend-triggered tier promotion;
- the four additional longitudinal fixtures reserved for FINISH.

If concern construction cannot support `RE-AS-3` or `RE-AS-5` without broader longitudinal implementation, implement only the minimum governed logic required for those two approved scenarios and document the boundary.

## 11. Explicit exclusions

Do not implement or modify:

- comprehensive Tier 0 escalation pathways;
- emergency-service routing;
- user-response monitoring;
- autonomous disease diagnosis;
- specialist pregnancy interpretation;
- broad questionnaire redesign;
- laboratory-provider integrations;
- FIB-4 activation;
- cardiovascular-risk activation;
- trend-triggered tier promotion;
- comprehensive trend interpretation;
- treatment or prescribing logic;
- final regulatory-release documentation;
- merge or release automation.

Do not modify unless a STOP condition is met and explicit approval is obtained:

- `backend/core/analytics/precedence_engine.py`
- `backend/core/analytics/arbitration_engine.py`
- `backend/core/analytics/state_engine.py`
- questionnaire schema or broad questionnaire flow
- existing WHY/root-cause compiler or presentation authority

## 12. Mandatory STOP conditions

STOP immediately and report exact evidence if:

1. Any of the 109 scenarios cannot be implemented without inventing a threshold, tier, urgency band, severity rule, override, action class, product rule or wording policy.
2. Authority files conflict in a way that the ratified source-precedence hierarchy cannot resolve.
3. A duplicate or parallel clinical-finding authority, loader or constructor is found.
4. Tests and runtime would need to consume different prioritisation authority sources.
5. Phase 0 finds a live consumer-facing FIB-4 or cardiovascular-risk calculation path. Do not proceed to hepatic implementation until explicit quarantine-implementation scope is approved.
6. The package would require changing cluster-level `precedence_engine.py`, `arbitration_engine.py` or `state_engine.py`.
7. The package would require broad questionnaire-schema redesign or specialist pregnancy rules.
8. Serious-result representation cannot be implemented without implying a HealthIQ-operated escalation workflow.
9. No-forced-lead behaviour cannot coexist with existing DTO/report compatibility without a product-policy change.
10. A six-domain rule cannot be compiled without silently treating a draft domain ruleset as independent runtime authority.
11. A baseline regression failure is introduced and cannot be attributed to an approved expected-output change.
12. The working tree contains unrelated, tooling or out-of-scope changes.
13. The kernel-issued work-package token is missing, mismatched or invalid.
14. Any Automation Bus state would need manual editing.
15. START would need to implement longitudinal Checkpoint 4 or frontend Checkpoint 5 to claim 109/109 coverage beyond the narrow compatibility boundary in §§7.5 and 10.
16. A scenario can pass only by disabling, hiding, or altering an existing active signal or supporting signal.
17. Consolidation loses activation-key or signal provenance — the constituent signal identities behind a consolidated finding cannot be fully recovered.
18. Prioritisation logic (tier, role, consolidation) changes upstream signal activation behaviour, rather than only how an already-fired finding is presented.
19. Implementation requires changing Knowledge Bus promotion status or runtime eligibility for any existing signal.
20. A newer document appears to retire an established signal without a clear, cited, pre-existing superseding decision.
21. Existing signal behaviour conflicts with the prioritisation contract in a way that cannot be resolved by presentation/consolidation alone.

For STOP conditions 16-21, report the conflict as a **provenance conflict** and escalate it — do not silently resolve it in favour of the newest document. The existing authorised signal activation and promotion estate (§3A.3, layer 1) is not overridden merely because a later document exists; a genuine conflict between the signal estate and the prioritisation contract requires explicit human/GPT adjudication, not an implementation-time judgement call.

Do not weaken a STOP condition to complete the sprint.

## 13. Required tests and evidence

Determine exact repository commands during Phase 0 and record them before implementation.

At minimum, evidence must include:

- focused model/schema tests;
- compiler and loader tests;
- concern-construction unit tests;
- hepatic pilot scenario tests;
- full clinical-prioritisation scenario harness;
- `APPROVED_SCENARIO_ESTATE_COVERAGE: 109/109`;
- `SIGNAL_ACTIVATION_BASELINE_TOTAL`, `SIGNAL_ACTIVATION_PRESERVED_TOTAL`, `SUPPORTING_SIGNAL_BASELINE_TOTAL`, `SUPPORTING_SIGNAL_PRESERVED_TOTAL`, `SIGNALS_INTENTIONALLY_RETIRED` — required result: activation preserved for every baseline signal and supporting signal (preserved totals equal baseline totals), no disappearance caused by consolidation or ordering, all constituent identities retained in finding provenance, `SIGNALS_INTENTIONALLY_RETIRED: 0` unless explicit prior authority is cited;
- no-forced-lead test;
- same-day co-equal-group tests;
- more-serious-tier-wins test;
- consolidation and duplicate tests;
- supporting/contextual nesting tests;
- insufficient-data tests;
- indeterminate-severity tests;
- serious-result non-downgrade tests;
- quarantine negative tests;
- DTO serialisation and backwards-compatibility tests;
- existing relevant backend regression suites;
- static/type checks required by the repository;
- frontend build/type compatibility only to the extent needed to prove additive DTO changes do not break the current baseline.

Do not claim a pass without command output.

## 14. Commit discipline

Use bounded commits aligned to checkpoints.

Suggested commit sequence:

1. `feat(clin-priority): add canonical finding models and hepatic compiler`
2. `feat(clin-priority): implement hepatic concern construction`
3. `test(clin-priority): prove hepatic acceptance scenarios`
4. `feat(clin-priority): compile six-domain prioritisation estate`
5. `feat(clin-priority): implement cross-domain concern prioritisation`
6. `test(clin-priority): prove 109-scenario acceptance estate`
7. `docs(clin-priority): record START evidence and carry-forwards`

Adjust descriptions to actual changes, but preserve checkpoint separation and avoid unrelated files.

Do not merge.

## 15. START completion response

At STOP, return:

- current branch;
- HEAD SHA;
- commits created;
- files changed;
- canonical authority paths;
- compiled artefact path;
- compiler path;
- loader path;
- concern-construction path;
- DTO paths;
- exact test commands and outcomes;
- hepatic scenario result;
- `APPROVED_SCENARIO_ESTATE_COVERAGE`;
- number of skipped scenarios;
- unresolved scenario differences;
- `SIGNAL_ACTIVATION_BASELINE_TOTAL`;
- `SIGNAL_ACTIVATION_PRESERVED_TOTAL`;
- `SUPPORTING_SIGNAL_BASELINE_TOTAL`;
- `SUPPORTING_SIGNAL_PRESERVED_TOTAL`;
- `SIGNALS_INTENTIONALLY_RETIRED` (and citation to prior authority if non-zero);
- no-forced-lead result;
- serious-result-state result;
- quarantine verification;
- regression result;
- deviations from this prompt;
- blockers;
- carry-forwards for FINISH;
- confirmation that Checkpoint 4 longitudinal integration is incomplete;
- confirmation that Checkpoint 5 frontend completion is incomplete;
- confirmation that `run_work_package.py finish` was not run;
- confirmation that no merge occurred.

End with exactly one START verdict:

- `START_READY_FOR_INDEPENDENT_STOP_REVIEW`
- `START_BLOCKED`
- `START_FAILED`

Do not self-authorise FINISH.
