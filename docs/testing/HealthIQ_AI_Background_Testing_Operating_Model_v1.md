# HealthIQ AI — Background Testing and Issue-Surfacing Operating Model

**Author role:** Head of Testing Strategy  
**Document type:** Operating brief beneath the agentic testing strategy paper  
**Status:** Draft for team feedback and critique  
**Scope:** Continuous/background test intelligence, issue surfacing, and narrowly governed auto-remediation  
**Implementation status:** No code or sprint prompts included

---

## 1. Executive summary

HealthIQ AI now needs a background testing and issue-surfacing system that continuously watches for product-quality risks across parsing, canonical mapping, deterministic analytics, persistence, and customer-facing rendering.

The system should not be an autonomous engineering agent. It should be a governed quality layer that:

1. observes code, fixture, schema, and output-surface changes;
2. classifies the affected risk surface;
3. selects the appropriate deterministic regression pack;
4. runs or requests targeted tests;
5. produces structured evidence;
6. proposes narrowly bounded fixes only where pre-approved;
7. escalates all meaning-bearing, medical, behavioural, or persistence-affecting issues to human/governed review.

The correct operating model is:

> background test intelligence + deterministic proof + governed remediation boundary

LLMs may assist with risk analysis, test selection, missing-coverage detection, and issue summarisation. They must not approve their own findings, decide medical correctness, or modify meaning-bearing logic without the existing Automation Bus lifecycle.

This paper proposes a phased system that starts lightweight: file-path triggers, fixture replay, alias/canonical checks, frontend trust-surface checks, persisted-result replay, and structured issue reporting. Only later should the system mature into narrow auto-remediation for safe content-only defects such as alias-registry additions, user-facing label-map additions, and regression-test generation.

---

## 2. Why the previous strategy paper is not enough on its own

The previous strategy paper established the need for a multi-agent testing model and a broader regression architecture. That is necessary, but it does not define how the system behaves day to day.

The missing layer is operational:

- what causes the testing system to run;
- what repository surfaces it watches;
- how it chooses tests;
- how it classifies defects;
- when it may propose a fix;
- when it must refuse to act;
- how evidence is captured;
- how findings enter the existing HealthIQ governance model.

Without this operating layer, HealthIQ risks creating either:

1. another end-of-sprint testing checklist that finds issues too late; or
2. an over-powerful autonomous agent that bypasses the governance discipline already built into the Automation Bus and Knowledge Bus.

Neither is acceptable for a deterministic health-analysis platform.

The operating model must therefore sit between normal CI and formal sprint governance. It should be always-on enough to catch issues early, but constrained enough that it cannot silently change analytical behaviour.

---

## 3. Background operating model

### 3.1 System name

Working name:

**HealthIQ Background Testing Sentinel**

The name is deliberately operational rather than agentic. The system watches, tests, classifies, reports, and in narrow cases proposes or applies pre-approved non-behavioural fixes.

### 3.2 Core principle

The Sentinel must never become an alternative authority source.

It must operate beneath the existing governance model:

- Knowledge Bus governs clinical/signal knowledge.
- Automation Bus governs work-package execution.
- Validators and gates decide pass/fail.
- Humans retain merge and release authority.
- LLMs may reason, inspect, propose, and challenge, but not self-certify.

### 3.3 Operating modes

The Sentinel should have five operating modes.

#### Mode 1 — Observe

Detect repository, fixture, schema, and output-contract changes.

Example: a change touches `backend/ssot/`, `frontend/app/results/`, or `backend/core/pipeline/`.

#### Mode 2 — Classify

Map the change to one or more risk surfaces.

Example: a change to biomarker aliases triggers parser/canonical coverage checks; a change to results rendering triggers UI trust-surface checks.

#### Mode 3 — Test

Run the minimum required deterministic test pack for the risk surface.

Example: alias registry tests, AB/VR fixture replay, persisted-snapshot replay, Playwright rendering checks.

#### Mode 4 — Report

Produce a structured issue report with evidence, affected files, test output, risk classification, and recommended next action.

#### Mode 5 — Governed narrow remediation

Only for pre-approved issue classes, the system may either:

- generate a proposed patch for review; or
- eventually apply the patch on a dedicated branch if deterministic proof passes and the issue is explicitly within the safe auto-fix envelope.

This mode must be unavailable for all analytical, medical, scoring, confidence, consequence, persistence, and signal-firing changes.

---

## 4. Trigger model

The Sentinel should run on multiple triggers rather than only at sprint closure.

### 4.1 Code-change trigger

Runs when files change in mapped risk surfaces.

Examples:

| Changed surface | Triggered checks |
|---|---|
| Parser or upload parsing path | parser fixture replay, alias coverage, unit conversion checks |
| Canonical/SSOT files | canonical-ID integrity, duplicate authority checks, marker presence/missing checks |
| Signal or analytics path | deterministic engine regression, fixture panels, output drift checks |
| Persistence/result DTO path | persisted-result replay, result-version compatibility, stale snapshot checks |
| Results frontend | rendering checks, internal-label leak checks, card coherence checks |
| Narrative/domain-card layer | coherence checks, consequence/headline alignment, forbidden phrase/internal slug checks |

### 4.2 File-path based trigger

A practical first version can use a file-path classifier.

Initial path families:

- `backend/ssot/`
- `backend/core/canonical/`
- `backend/core/analytics/`
- `backend/core/pipeline/`
- `backend/core/validation/`
- `backend/scripts/`
- `knowledge_bus/`
- `automation_bus/`
- `frontend/app/results/`
- `frontend/app/types/`
- `frontend/app/services/`
- `tests/`
- `frontend/tests/` or equivalent E2E folders

The exact live paths must be verified against the current repo before implementation.

### 4.3 Pull request / branch trigger

On a PR or sprint branch, the Sentinel should:

1. identify changed files;
2. classify risk surfaces;
3. run targeted tests;
4. compare with required gates;
5. generate a branch-level test intelligence report.

This does not replace `run_work_package.py finish`. It gives earlier feedback before formal closure.

### 4.4 Fixture-change trigger

Any change to fixture panels, synthetic panels, or expected outputs should trigger:

- fixture schema validation;
- replay of affected panels;
- expected-output diff review;
- regression-pack classification.

A fixture change should not be allowed to silently weaken expectations.

### 4.5 Schema-change trigger

Any schema or contract change should trigger:

- producer/consumer compatibility checks;
- backend/frontend type parity checks;
- persisted-result compatibility checks;
- fixture replay against the new contract.

Schema changes are high-risk if they affect emitted analysis or customer-facing output.

### 4.6 Manual operator trigger

Operators should be able to run:

- full background sweep;
- alias/canonical sweep;
- persisted-result sweep;
- UI trust-surface sweep;
- escaped-defect replay;
- release-confidence sweep.

This gives leadership a way to ask, “What could currently embarrass us in UAT?” without waiting for a sprint boundary.

### 4.7 Scheduled background sweep

A scheduled sweep should run even without active code changes.

Suggested cadence:

- daily lightweight scan: alias/canonical integrity, internal-label leak checks, fixture metadata checks;
- twice-weekly medium scan: AB/VR fixture replay, persisted-result replay, UI smoke checks;
- pre-release full scan: all critical regression packs, E2E flows, snapshot compatibility, known escaped defects.

### 4.8 Escaped UAT defect trigger

Every escaped UAT defect should become a structured regression asset unless explicitly rejected.

The trigger should create an issue record containing:

- defect class;
- example payload or screenshot;
- expected behaviour;
- actual behaviour;
- affected surface;
- proposed regression test location;
- whether auto-remediation is ineligible, proposed-only, or eligible.

---

## 5. Watch / monitor model

The Sentinel should watch five architectural surfaces.

### 5.1 Input truth surface

Covers upload, parsing, alias normalisation, canonical biomarker resolution, units, and ranges.

Failure examples:

- GGT alias not mapping;
- bilirubin present but treated as missing;
- a unit displayed or converted incorrectly;
- a derived marker missing because its prerequisites were not recognised.

Required monitoring:

- alias registry integrity;
- duplicate canonical IDs;
- orphan aliases;
- unsupported live marker names;
- present-but-missing contradictions;
- unit compatibility and display sanity.

### 5.2 Analytical truth surface

Covers deterministic scoring, signal firing, confidence, missing-marker logic, primary-pattern selection, consequence selection, and domain-card assembly.

Failure examples:

- card headline says reassuring while consequences imply strain;
- confidence improver lists markers already present;
- multiple authorities select different stories;
- consequence logic escalates without supporting signal state.

Required monitoring:

- single-authority anchoring;
- primary-pattern consistency;
- signal-to-card traceability;
- missing-marker truth;
- contradiction checks;
- fixture output drift.

### 5.3 Persistence and snapshot surface

Covers stored analysis results, result versions, frozen snapshots, regeneration paths, and API result contracts.

Failure examples:

- backend fix does not surface because old result snapshot remains frozen;
- frontend displays old broken domain-card text;
- result contract changes but old persisted outputs are still treated as current.

Required monitoring:

- result version presence;
- persisted fixture replay;
- stale snapshot detection;
- old/new analysis comparison;
- fallback behaviour review;
- DB-backed vs in-memory output parity where relevant.

### 5.4 Customer trust surface

Covers frontend domain cards, labels, units, values, empty states, mobile/desktop rendering, and narrative coherence.

Failure examples:

- `total_bilirubin` or other slugs visible to users;
- impossible-looking values shown without explanation;
- missing values rendered as confusing blanks;
- page summary and card detail disagree.

Required monitoring:

- internal identifier leak detection;
- label map completeness;
- unit/value display sanity;
- card coherence;
- no unsupported clinician-review language;
- visual smoke checks on representative panels.

### 5.5 Governance surface

Covers Automation Bus, Knowledge Bus, validators, gates, work-package state, and evidence files.

Failure examples:

- duplicated SSOT authority;
- no-op remediation sprint;
- missing hardening evidence;
- gate output not produced;
- knowledge package treated as active without validator proof.

Required monitoring:

- control-plane file changes;
- evidence presence;
- branch/sprint state consistency;
- Knowledge Bus status validity;
- no duplicate authority paths;
- no forbidden fallback parser introduction.

---

## 6. Test-selection model

The Sentinel should not run every test on every change. It should select tests by risk surface and blast radius.

### 6.1 Selection inputs

Test selection should consider:

- changed files;
- changed schema fields;
- changed fixtures;
- changed frontend components;
- changed output contracts;
- affected known defects;
- whether the change touches Intelligence Core;
- whether the change affects persisted outputs;
- whether the change changes customer-visible text.

### 6.2 Minimum test packs

#### Parser / alias pack

Triggered by parser, alias, canonical, SSOT, upload, unit, or fixture input changes.

Should include:

- canonical resolution tests;
- alias variants;
- live payload replay;
- unit normalisation checks;
- present-but-missing checks;
- unsupported marker reporting.

#### Deterministic engine pack

Triggered by signal, scoring, confidence, consequence, domain-card, analytics, or pipeline changes.

Should include:

- synthetic single-signal panels;
- AB/VR fixture replay;
- known domain-card defect replay;
- confidence/missing-marker assertions;
- output drift comparison.

#### Persistence / snapshot pack

Triggered by result DTO, persistence, API result, frontend type, DB, or snapshot-version changes.

Should include:

- old persisted result replay;
- new analysis replay;
- result-version compatibility;
- stale-output detection;
- API/frontend contract parity checks.

#### UI trust-surface pack

Triggered by results page, domain-card, label, formatter, type, or frontend service changes.

Should include:

- no internal labels/slugs;
- value display sanity;
- unit display checks;
- card coherence assertions;
- empty/partial states;
- mobile/desktop smoke paths.

#### Full E2E / UAT pack

Triggered by release candidate, broad output contract change, major domain-card change, or repeated escape defects.

Should include:

- upload-to-results journey;
- representative realistic panels;
- persisted-result reload;
- browser-visible domain-card assertions;
- user-trust checklist.

### 6.3 Escalation of test selection

The Sentinel should escalate from targeted to broader testing when:

- multiple risk surfaces are touched;
- output contracts change;
- Intelligence Core is touched;
- persistence and frontend are both touched;
- a previous escaped defect class is implicated;
- the test selector cannot confidently classify the change.

Uncertainty must increase testing breadth, not reduce it.

---

## 7. Issue taxonomy

The Sentinel should classify issues into stable categories.

### 7.1 Proposed issue categories

| Code | Category | Description | Default action |
|---|---|---|---|
| MAP-ALIAS | Alias mapping defect | Marker present under a real-world alias but not resolved | Proposed-only or narrow auto-fix if safe |
| MAP-CANON | Canonical-ID mismatch | Marker resolves to wrong or inconsistent canonical ID | Escalate |
| MAP-UNIT | Unit/display defect | Unit conversion or display inconsistency | Escalate unless display-only |
| PRES-MISS | Present-but-missing defect | Marker exists in panel but appears in missing/improver list | Escalate |
| CARD-COHERE | Narrative/card coherence defect | Headline, consequence, summary, or details contradict | Escalate |
| CARD-AUTH | Multi-authority output defect | Different page/card sections draw from different story authorities | Escalate |
| UI-LABEL | Internal label leak | Slug/internal identifier visible to user | Narrow auto-fix possible if label-map only |
| UI-VALUE | Trust-damaging value display | Impossible-looking or unformatted values visible | Escalate unless formatter-only |
| SNAP-STALE | Stale snapshot defect | Old persisted result presents outdated/broken logic as current | Escalate |
| CONTRACT | Producer/consumer contract defect | Backend/frontend/result schema mismatch | Escalate |
| GOV-BUS | Governance/control-plane defect | Automation/Knowledge Bus state or evidence inconsistency | Escalate |
| TEST-GAP | Missing regression coverage | Defect found but no permanent regression asset exists | Auto-generate test proposal allowed |
| FIXTURE-GAP | Fixture realism gap | Current fixtures do not represent live payload risk | Proposed fixture addition allowed |
| PERF-REL | Performance/reliability defect | Test execution, API, or page load risk | Report/propose |
| SEC-DATA | Security/data-safety defect | PII, access, RLS, or exposure concern | Immediate escalation |

### 7.2 Severity levels

| Severity | Meaning |
|---|---|
| S0 | Could produce clinically misleading, unsafe, or materially wrong output |
| S1 | Customer-facing trust failure or governed output inconsistency |
| S2 | Functional regression with contained blast radius |
| S3 | Test-gap, fixture-gap, or non-customer-visible hygiene issue |

S0 and S1 issues must block release until resolved or explicitly risk-accepted by leadership.

---

## 8. Auto-remediation eligibility rules

Auto-remediation must be treated as exceptional, narrow, and pre-approved.

### 8.1 Eligible for eventual narrow auto-fix

These are the only categories that should ever become eligible for direct auto-remediation, and only after the system matures.

#### A. Alias-registry additions

Eligible only when all conditions are met:

- the source marker is present in a real or fixture payload;
- the proposed alias maps to an existing canonical biomarker;
- no new canonical biomarker is created;
- no thresholds, scoring, or signal logic change;
- no ambiguity exists with another biomarker;
- deterministic alias tests prove before/after resolution;
- affected fixture replay passes.

Example: adding a safe spelling/casing/lab-name alias for GGT if canonical GGT already exists and the mapping is unambiguous.

#### B. User-facing label-map additions

Eligible only when:

- an internal slug is visible in UI;
- the slug maps to an existing canonical biomarker or domain;
- the proposed label is display-only;
- no analytical logic changes;
- no medical interpretation text changes;
- frontend trust tests prove the slug no longer leaks.

Example: mapping `total_bilirubin` to `Total bilirubin` if the canonical label authority confirms that wording.

#### C. Rendering-safe fallback labels

Eligible only when:

- the fallback is purely presentational;
- it uses a safe title-casing or existing canonical display name;
- it does not invent clinical meaning;
- it is covered by UI snapshot tests;
- it does not hide a missing canonical mapping defect.

This must be used carefully. A fallback label must not mask a real canonical-ID failure.

#### D. Regression-test generation

Eligible when:

- an escaped defect is documented;
- the expected behaviour is already agreed;
- the test encodes existing intended behaviour;
- it does not redefine product logic.

This is the safest early auto-remediation class: the system can generate a proposed regression test for review.

#### E. Fixture addition for observed live payload variants

Eligible as proposed-only initially, and later narrow auto-fix if:

- the fixture is anonymised;
- no clinical expectations are changed;
- it is used only to replay parser/rendering behaviour;
- expected outputs are reviewed separately if meaning-bearing.

### 8.2 Proposed-only, never direct auto-apply initially

These classes may have automated proposed fixes, but must not be directly applied without human/governed approval:

- canonical display-name corrections;
- unit display formatter changes;
- stale snapshot warning text;
- non-meaning-bearing UI empty-state wording;
- test harness wiring;
- fixture expected-output updates;
- schema compatibility warnings;
- result-version metadata additions.

### 8.3 Must always escalate

The Sentinel must never auto-fix:

- scoring logic;
- confidence logic;
- signal firing;
- thresholds;
- consequence selection;
- primary-pattern selection;
- missing-marker clinical logic;
- root-cause or WHY logic;
- narrative meaning;
- clinician-review recommendations;
- medication/intervention interpretation;
- persistence/backfill logic;
- result migration logic;
- Knowledge Bus package promotion;
- Automation Bus lifecycle or gate scripts;
- any duplicate SSOT authority issue;
- any issue with unclear root cause.

These changes are meaning-bearing or governance-bearing and must remain under formal sprint control.

---

## 9. Deterministic proof model

No surfaced issue or auto-fix proposal should be accepted without deterministic proof.

### 9.1 Required proof for surfaced issues

Every issue report must include:

- trigger reason;
- changed or affected files;
- issue taxonomy code;
- severity;
- reproducible input;
- actual output;
- expected output or expected invariant;
- tests run;
- pass/fail result;
- confidence level;
- recommended next action;
- escalation status.

### 9.2 Required proof for auto-fix proposals

Every proposed fix must include:

- exact files proposed to change;
- why the issue is eligible;
- before/after evidence;
- deterministic tests proving the defect;
- deterministic tests proving the fix;
- blast-radius classification;
- statement that no analytical behaviour changed;
- statement that no duplicate authority source was created;
- statement that no fallback parser was introduced.

### 9.3 Pass/fail standard

A fix can only pass if:

- the original defect reproduces before the fix;
- the defect no longer reproduces after the fix;
- all targeted tests pass;
- relevant fixture replay passes;
- no wider output drift occurs unless explicitly expected;
- no HIGH-risk files are touched;
- no meaning-bearing logic changes;
- no governance rules are bypassed.

### 9.4 Automatic application blockers

Automatic application must be blocked if:

- the file path is HIGH-risk;
- the defect changes analytical meaning;
- the issue touches persistence/backfill;
- the issue touches control-plane scripts;
- the proposed fix changes schema or runtime contract;
- the proposed fix changes outputs beyond display-only surfaces;
- the root cause is uncertain;
- tests are missing or inconclusive;
- multiple possible canonical mappings exist;
- the fix would create or rely on a fallback parser;
- an LLM is the only source of proof.

---

## 10. Human escalation thresholds

The Sentinel must escalate rather than act when any of the following apply.

### 10.1 Medical meaning affected

Any change that could affect interpretation, risk, recommendations, clinician-review language, or domain-card meaning must escalate.

### 10.2 Governed outputs affected

Any change that affects analytical output construction, filtering, ranking, emission, or structured report content must escalate.

### 10.3 Intelligence Core touched

Any touched path in analytical pipeline, signal evaluation, root-cause compilation, InsightGraph construction, or governed-content loading must escalate.

### 10.4 Persistence or backfill touched

Any issue involving stored results, migrations, regeneration, old snapshots, or backfill must escalate.

### 10.5 Multiple authorities disagree

If parser, backend, persisted result, and frontend disagree about the state of a marker or card, the system must report and escalate. It must not choose an authority itself.

### 10.6 Root cause unclear

If the system can prove a symptom but not the root cause, it may create an issue report and regression proposal, but it must not fix.

### 10.7 Large blast radius

If a fix could affect multiple domains, many biomarkers, all result pages, or shared contracts, it must escalate.

### 10.8 Deterministic proof absent

If the issue or fix cannot be reproduced deterministically, it must escalate.

---

## 11. Evidence and audit model

### 11.1 Proposed evidence location

The Sentinel should write findings under a dedicated non-authoritative evidence area, for example:

```text
testing_sentinel/
  reports/
    YYYY-MM-DD/
      <run_id>_summary.md
      <run_id>_issues.json
      <run_id>_test_output.txt
      <run_id>_diff_summary.txt
  registry/
    escaped_defects.yaml
    issue_taxonomy.yaml
    surface_map.yaml
    auto_fix_policy.yaml
```

This location is intentionally separate from Automation Bus evidence. Sentinel evidence supports decision-making; it does not replace formal gate evidence.

The exact directory should be agreed before implementation.

### 11.2 Issue report structure

Each issue should record:

```yaml
issue_id:
detected_utc:
trigger_type:
branch:
head_sha:
changed_files:
affected_surfaces:
issue_category:
severity:
reproduction_input:
actual_output:
expected_invariant:
tests_run:
test_results:
auto_remediation_status: ineligible | proposed_only | eligible | blocked
proposed_files_to_change:
escalation_required:
recommended_owner:
status: open | accepted | rejected | fixed | regression_added
```

### 11.3 Auto-fix audit trail

For any proposed or applied fix:

- record before/after outputs;
- record changed files;
- record eligibility rule used;
- record tests run;
- record reviewer decision;
- record whether it entered Automation Bus or remained outside due to safe content-only policy;
- record final merge decision.

### 11.4 Relationship with Automation Bus evidence

If a finding leads to a governed sprint, the Sentinel report becomes supporting evidence only.

Automation Bus remains authoritative for:

- work-package execution;
- branch isolation;
- hardening;
- gate evidence;
- audit summary;
- HIGH-risk review;
- merge readiness.

### 11.5 Relationship with Knowledge Bus evidence

If a finding affects signal definitions, biomarker relationships, derived metrics, or physiological system modelling, it must move through Knowledge Bus validation and promotion rules.

The Sentinel may detect the issue. It cannot promote clinical knowledge.

---

## 12. Repo-grounded feasibility notes

This section is grounded in the available HealthIQ shared-folder materials. A live repo checkout should be used to confirm exact current paths before implementation.

### 12.1 Existing governance foundations that can support the Sentinel

The Automation Bus already defines the control-plane model required for governed execution:

- role separation;
- deterministic gates;
- hardening evidence;
- branch isolation;
- immutable gate evidence;
- HIGH-risk escalation;
- no-op protection;
- no fallback parser rule;
- no duplicate SSOT authority rule.

This means the Sentinel does not need to invent governance. It should plug into the existing philosophy.

Practical implication: the Sentinel should be an early-warning and evidence-generation layer, not a second execution bus.

### 12.2 Existing deterministic gate concepts

Available materials identify these relevant control-plane artefacts and scripts:

- `automation_bus/latest_cursor_prompt.md`
- `automation_bus/latest_prompt_hardening.json`
- `automation_bus/latest_cursor_status.json`
- `automation_bus/latest_gate_evidence.json`
- `automation_bus/latest_gate_output.txt`
- `automation_bus/latest_audit_summary.md`
- `automation_bus/state/work_package_active.json`
- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/scripts/update_cursor_status.py`

These are suitable anchors for formal sprint gating, but the Sentinel should not mutate them.

### 12.3 Existing Knowledge Bus validator foundations

The Knowledge Bus already establishes a canonical validator:

- `backend/scripts/validate_knowledge_package.py`

It also records that the current lifecycle controller has a `KBP-*` versus `pkg_*` mismatch and is not currently authoritative for `pkg_*` package promotion.

Practical implication: the Sentinel can check knowledge status and package validation evidence, but must not rely on the Knowledge Bus lifecycle script as authoritative until reconciled.

### 12.4 Existing testing and fixture references

The shared materials reference:

- AB/VR as minimum commercial test harnesses;
- fixture expansion as a formal roadmap need;
- persistence testing;
- backend unit/integration tests;
- frontend component and E2E testing with Playwright;
- security and performance checks;
- result DTO/frontend TypeScript parity;
- `result_version` as a compatibility concept.

This supports a background testing layer that can start with existing test categories rather than inventing a new test universe.

### 12.5 Practical file-surface classification

File-path classification is feasible because the architecture already has clear surface boundaries:

- `backend/ssot/` for biomarker/questionnaire/lifestyle authority;
- `knowledge_bus/` for governed clinical/signal packages;
- `backend/core/analytics/` and `backend/core/pipeline/` for Intelligence Core;
- `backend/scripts/` for control-plane scripts;
- `frontend/app/results/` for customer-visible results;
- `frontend/app/types/analysis.ts` for frontend result contracts;
- `backend/ssot/questionnaire.json` and `backend/ssot/lifestyle_registry.yaml` for context-input foundations.

Exact current path names should be confirmed in a live repo audit before implementation.

### 12.6 Persisted-result checks need special handling

Snapshot persistence cannot be tested only through fresh pipeline runs.

The Sentinel needs explicit persisted-result fixtures:

- old result snapshot produced under previous logic;
- new result generated under current logic;
- frontend reload of stored result;
- comparison of result version and visible output;
- stale-result warning or regeneration behaviour, once product policy is agreed.

This is a special test class because code correctness and customer-visible correctness can diverge when old analysis results are frozen.

### 12.7 Frontend trust-surface checks need special handling

The frontend is officially renderer-only, but renderer-only does not mean risk-free.

Trust failures can arise even when the backend is technically correct:

- raw slugs displayed;
- label maps incomplete;
- values rendered in confusing ways;
- card hierarchy contradicts itself visually;
- missing markers shown as available or vice versa.

The Sentinel should therefore treat frontend rendering as a customer-trust risk surface even when it is not an analytical authority.

---

## 13. Phased rollout proposal

### Phase 0 — Policy and taxonomy only

Goal: agree the operating model before implementation.

Deliverables:

- issue taxonomy;
- risk-surface map;
- auto-remediation policy;
- evidence schema;
- escalation rules;
- list of existing test commands and fixture locations from live repo audit.

No automation yet.

### Phase 1 — Reporting-only Sentinel

Goal: background issue surfacing with no code modification.

Capabilities:

- detect changed files;
- classify risk surface;
- recommend test packs;
- run safe existing tests where available;
- produce issue reports;
- flag missing regression coverage;
- maintain escaped-defect registry.

No auto-remediation.

### Phase 2 — Deterministic replay packs

Goal: make the system useful for current UAT pain.

Capabilities:

- alias/canonical sweep;
- AB/VR fixture replay;
- known escaped-defect replay;
- persisted-result replay;
- UI internal-label leak scan;
- card coherence assertions for fixture outputs.

Still no auto-remediation.

### Phase 3 — Proposed-only remediation

Goal: allow agents to propose safe patches without applying them.

Eligible proposal classes:

- alias additions;
- label-map additions;
- regression-test additions;
- fixture additions;
- display-only formatter suggestions.

All proposals require human or formal sprint acceptance.

### Phase 4 — Narrow governed auto-fix pilot

Goal: test safe auto-remediation on a very small class of issues.

Eligible pilot class:

- display-only user-facing label-map additions, or
- unambiguous alias additions.

Constraints:

- dedicated branch;
- deterministic before/after proof;
- no HIGH-risk paths;
- no analytical output change;
- no schema change;
- no persistence change;
- automatic issue report;
- human merge approval.

This is still not autonomous production modification. It is automated patch preparation under deterministic proof.

### Phase 5 — Release-confidence dashboard

Goal: provide leadership with a concise release-readiness view.

Metrics:

- open S0/S1 issues;
- fixture replay pass rate;
- alias/canonical coverage pass rate;
- known escaped-defect regression status;
- persisted-result compatibility status;
- UI trust-surface status;
- control-plane/gate status;
- unresolved test gaps;
- last full sweep date.

A customer-facing release should not proceed with unresolved S0/S1 Sentinel issues unless explicitly risk-accepted.

---

## 14. Open decisions still needing leadership input

### 14.1 Auto-remediation appetite

Leadership needs to decide whether Phase 4 should ever be enabled, or whether the system should remain permanently proposed-only.

Recommendation: begin proposed-only and do not enable auto-apply until the team has reviewed at least 20–30 Sentinel issue reports and confirmed taxonomy reliability.

### 14.2 Evidence location

The team should decide whether Sentinel reports live under:

- `testing_sentinel/`
- `qa_sentinel/`
- `automation_bus/sentinel/`
- `docs/testing/`

Recommendation: use a separate top-level non-authoritative folder such as `testing_sentinel/` to avoid confusing Sentinel evidence with Automation Bus gate evidence.

### 14.3 Release blocking authority

Leadership must decide whether Sentinel S0/S1 issues are hard blockers or advisory blockers.

Recommendation: S0 should be a hard blocker. S1 should block customer-facing release unless explicitly risk-accepted.

### 14.4 Persisted-result policy

The team must decide what the product should do when old persisted results were generated under outdated logic.

Options:

1. show as-is with result version;
2. show stale-result warning;
3. offer regeneration;
4. force regeneration for known defective versions;
5. maintain migration/backfill process.

Recommendation: do not allow silent stale-result presentation once the system can detect known defective output versions.

### 14.5 Fixture ownership

The team needs a clear owner for approving expected outputs in fixture panels.

Recommendation: LLMs may generate fixture proposals, but expected clinical/customer-facing output fixtures require human/GPT architectural approval where meaning-bearing.

### 14.6 UAT-to-regression workflow

Leadership should agree that every escaped UAT defect must be triaged into:

- permanent regression;
- fixture addition;
- known limitation;
- rejected as non-defect.

Recommendation: default to permanent regression unless explicitly rejected.

### 14.7 Live-repo audit requirement before implementation

Before any sprint prompt is written, a live repo audit should confirm:

- current test commands;
- current fixture locations;
- current parser/alias authority files;
- current frontend results components;
- current persisted-result schema and version behaviour;
- current CI/gate integration points;
- whether existing tests already cover any proposed Sentinel checks.

---

## Final operating position

The background testing system should become HealthIQ AI’s continuous quality intelligence layer.

It should not replace the Automation Bus, Knowledge Bus, deterministic validators, or human authority.

Its purpose is to detect risk earlier, classify defects consistently, preserve escaped defects as regression assets, and give leadership release-confidence evidence before UAT exposes avoidable trust failures.

The safest initial version is reporting-only.

The mature version may support narrowly governed auto-remediation, but only for display-only or mapping-only defects where deterministic proof is complete and no medical meaning can change.

The governing rule is simple:

> The Sentinel may accelerate detection and evidence. It must not become an ungoverned source of product truth.

