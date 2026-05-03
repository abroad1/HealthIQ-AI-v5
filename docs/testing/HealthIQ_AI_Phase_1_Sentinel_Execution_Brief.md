# HealthIQ AI — Phase 1 Sentinel Execution Brief

**Role:** Head of Testing Strategy  
**Purpose:** Define the first practical implementation slice for HealthIQ AI’s background testing Sentinel.  
**Status:** Draft for team review and critique  
**Scope:** Phase 1 only — no broad autonomous Sentinel, no auto-remediation, no sprint prompt, no code design.

---

## 1. Executive summary

Phase 1 Sentinel should be deliberately narrow.

The goal is not to build the full background testing system. The goal is to prove that a small, governed, report-only testing layer can catch real escaped defect classes earlier than manual UAT.

The first useful slice should cover:

1. alias and canonical biomarker mapping
2. known escaped-defect regression coverage
3. frontend slug/internal-label leakage
4. basic changed-file risk classification
5. report-only issue surfacing

Phase 1 must not attempt auto-remediation.

It should read the codebase, select appropriate deterministic tests, run or recommend the narrow regression packs, and produce a structured issue report. It should not modify product code, SSOT files, Automation Bus artefacts, gate evidence, or governed intelligence assets.

This is the smallest slice that directly targets recent failures: GGT alias miss, bilirubin canonical mismatch, internal labels leaking into UI, and the absence of a coherent escaped-defect regression pack.

---

## 2. Why this slice comes first

The repo audits show HealthIQ AI already has a substantial deterministic test estate. One audit reports a large backend test estate with unit, integration, enforcement, fixture, replay, and golden-panel machinery already present, but notes that CI currently runs only a narrow subset and that Playwright/browser coverage is not clearly blocking in sampled workflows. The same audit identifies the strongest Phase 1 opportunity as backend/golden/enforcement/alias-oriented Sentinel slices rather than a full autonomous system.  

A second audit similarly found the repo materially more test-ready than a typical early-stage product, with 197 backend Python test files, 50 frontend test files, a rich fixture estate, and multiple validator/control-plane scripts. It also found that the repo is not yet ready for a full autonomous Sentinel because escaped-defect packs, slug-leakage guards, and real persisted-result replay are not yet sufficiently formalised.

Therefore Phase 1 should not create a grand testing architecture. It should convert the most recent escaped failure classes into permanent, deterministic, automatically surfaced regression checks.

---

## 3. Phase 1 objective

Phase 1 exists to answer one question:

> Can a small background Sentinel layer catch real HealthIQ escaped-defect classes earlier, without creating governance risk or test noise?

It succeeds if, after 2–3 weeks of use:

- GGT-style alias misses are automatically detected
- bilirubin-style canonical mismatches are automatically detected
- internal slugs or backend identifiers leaking into the UI are automatically detected
- changed-file classification produces useful risk/test recommendations
- Sentinel reports are trusted by the team
- no autonomous code modification is attempted
- the system produces enough evidence to justify or reject Phase 2 expansion

---

## 4. Phase 1 non-goals

Phase 1 must not attempt to:

- build the full autonomous background Sentinel
- generate or apply code fixes
- modify SSOT files
- modify Knowledge Bus packages
- modify Automation Bus artefacts
- modify gate evidence
- rewrite scoring, signal, confidence, consequence, or narrative logic
- solve persisted-result replay fully
- make Playwright the primary release gate before test currency is verified
- clean up the entire test estate before delivering value

This is not a test-cleanup sprint disguised as Sentinel. It is a narrow proof-of-value slice.

---

## 5. Exact first slice

### 5.1 Alias/canonical sweep

Phase 1 should introduce or activate a repeatable check that confirms biomarker aliases resolve to the expected canonical biomarker IDs.

It should focus first on:

- full sweep of the authoritative biomarker alias registry where practical
- exact known failure variants for GGT
- exact known failure variants for bilirubin
- venous/canonical key variants
- “present in payload but shown as missing” cases

The audit evidence shows the repo already contains alias registry services, alias normalisation tests, venous alias integration tests, unit alias tests, and SSOT alias/range validation tooling. This means Phase 1 is mainly about packaging the checks as a reliable regression surface, not inventing new infrastructure.

Expected outputs:

- pass/fail result
- aliases tested
- canonical IDs expected
- canonical IDs returned
- unmapped aliases
- aliases resolving to the wrong biomarker
- indication of whether the failure is a registry issue, parser issue, or runtime canonicalisation issue

---

### 5.2 Escaped-defect regression pack

Phase 1 should create a named escaped-defect regression pack.

This is important because the audits found that the known escaped defects are either partially covered in normal tests or not named as a coherent regression pack. That makes it harder to know whether recent UAT failures are permanently guarded.

Initial pack should include one named check per known escaped defect class:

1. GGT alias miss
2. bilirubin canonical mismatch
3. internal slug/raw identifier leakage
4. Wave 1 domain-card contradiction class
5. stale persisted-result visibility or compatibility placeholder

The first three should be active Phase 1 checks.

The fourth should be included as a narrow report/check where current deterministic assertions exist, but full narrative coherence should remain a Phase 2 target.

The fifth should be documented as a placeholder or limited compatibility check only, because the audits indicate persisted replay is feasible but not yet mature enough to treat as solved.

Expected outputs:

- escaped defect ID
- original failure class
- current reproduction fixture/input
- current expected behaviour
- test status
- linked test asset
- whether the issue is now fully guarded, partially guarded, or not yet guarded

---

### 5.3 Frontend slug/internal-label leakage guard

Phase 1 should add or run a frontend trust-surface check that prevents raw internal identifiers from appearing in customer-facing output.

The audits identify this as a clear current gap. They also note that OPS-S1A/OPS-S1B are good precedents for lightweight trust-surface checks, but that there is no comprehensive runtime/component-level guard against internal IDs or slugs leaking into visible UI.

Phase 1 should focus on:

- Wave 1 domain cards
- results page/customer-facing components
- known internal biomarker slugs such as `total_bilirubin`, `bilirubin_total`, `ggt`, and similar canonical/backend IDs
- internal phenotype IDs such as `ph_*_v*`
- obvious backend/system terms that should never be visible to a customer

Expected outputs:

- component/page checked
- fixture/mock used
- forbidden identifier patterns scanned
- visible text result
- pass/fail
- raw leaked token if found

---

### 5.4 Changed-file risk classifier

Phase 1 Sentinel should classify changed files into broad testing surfaces.

This should be simple and path-based at first. It does not need advanced dependency analysis.

Initial risk surfaces:

| Surface | Example paths | Phase 1 action |
|---|---|---|
| Parser / alias / canonical | `backend/core/canonical/`, parser services, alias registry, upload/reference mapping | Run alias/canonical sweep and escaped-defect mapping checks |
| SSOT / canonical authority | `backend/ssot/` | Report HIGH governance relevance; run validators/regression checks; no auto-fix |
| Analytics / scoring / signal | `backend/core/analytics/`, `backend/core/scoring/`, pipeline paths | Report HIGH risk; recommend deterministic core/enforcement/golden tests |
| Frontend results/trust surface | `frontend/app/components/results/`, relevant frontend lib shaping files | Run slug/internal-label leakage checks and targeted Jest tests |
| Persistence/result snapshot | result models, persistence services, replay/golden result paths | Report persistence relevance; run available persistence tests; flag replay maturity gap |
| Control-plane/governance | `automation_bus/`, gate/kernel scripts, validators | Report governance risk; no Sentinel mutation |
| Knowledge Bus/intelligence content | `knowledge_bus/`, signal libraries, intelligence loaders | Report governed content/intelligence impact; require manual governance |

The output should be a risk classification report, not an approval.

---

## 6. Existing tests to reuse

Phase 1 should reuse the existing estate rather than duplicate it.

From the audits, the strongest reusable assets are:

### Backend

- alias registry service tests
- biomarker alias resolution tests
- alias normalisation tests
- venous alias orchestrator integration tests
- unmapped quarantine tests
- unit normalisation tests
- Wave 1 liver mapping tests
- domain score assembler tests
- domain narrative Wave 1 tests
- enforcement tests
- golden panel runner / replay manifest where relevant

### Frontend

- Wave1DomainCards tests
- uploadReferenceRange tests
- resultsHeroAlignment tests
- primaryFindingShaping tests
- bodyOverviewPrimarySentence tests
- OPS-S1A/OPS-S1B trust baseline pattern
- relevant results component tests

### Fixtures and artefacts

- AB/VR panel fixtures
- golden_panel_160 fixtures
- phenotype fixtures
- golden run artefacts
- frontend analysis-result mocks
- arbitration/collision fixtures where relevant

Phase 1 should not run everything. It should run the smallest targeted set that maps to the changed file surface.

---

## 7. Tests to ignore, repair, or defer

### 7.1 Authoritative tests to keep

These should be treated as trusted assets unless proven otherwise:

- deterministic backend unit tests for analytics/scoring/signal logic
- enforcement tests
- validator tests
- golden/fixture tests
- recent escaped-defect tests
- actively maintained frontend results/component tests

### 7.2 Suspect tests to repair later

These should not block Phase 1, but should be logged as testing-debt candidates:

- stale Playwright tests tied to old UI strings
- tests that pass but only exercise mocked persistence paths
- tests that assert implementation trivia rather than product behaviour
- frontend mocks that may not be schema-synchronised with backend DTOs
- browser tests whose CI status is unclear

### 7.3 Tests to inventory for possible removal

These should not be deleted during Phase 1, but should be flagged:

- duplicate frontend test trees, especially `tests_new/` if confirmed stale
- archived tests that look live
- old sprint-specific tests that no longer represent active product truth
- superficial smoke tests that create false confidence

The Phase 1 stance is: do not purge first; identify and quarantine later.

---

## 8. Report-only operating behaviour

Phase 1 Sentinel should operate in report-only mode.

For each trigger, it should produce:

1. trigger reason
2. changed files or watched surface
3. risk classification
4. tests selected
5. tests run or recommended
6. pass/fail summary
7. escaped-defect coverage status
8. coverage gaps detected
9. escalation recommendation
10. no-fix confirmation

The report should explicitly distinguish:

- defect found
- regression gap found
- stale/noisy test found
- insufficient coverage
- governance escalation required

A failed test is not the only useful output. A finding that “this change touches a surface with no adequate regression coverage” is also a valid Sentinel issue.

---

## 9. Trigger model for Phase 1

Phase 1 should support four trigger types.

### 9.1 Manual operator trigger

Used first.

A developer, Claude, Cursor, GPT, or human reviewer can request a Sentinel run against:

- current branch
- a file list
- a PR diff
- a known escaped-defect class
- a specific path surface

This is the safest starting mode.

### 9.2 Changed-file trigger

When files change under known paths, Sentinel classifies the surface and selects a narrow test pack.

Examples:

- alias registry changed → alias/canonical sweep
- frontend results component changed → slug leakage guard
- domain score assembler changed → escaped-defect pack + relevant backend tests
- persistence model changed → persistence tests + replay gap report

### 9.3 Scheduled sweep

Initially weekly or nightly, but only for lightweight checks:

- alias/canonical sweep
- slug/internal-label scan
- escaped-defect pack
- static trust-surface checks

Do not start with full-suite scheduled runs until signal/noise is understood.

### 9.4 Escaped-defect trigger

Whenever UAT finds a new defect, Sentinel should require an escaped-defect record:

- defect class
- input/fixture
- expected behaviour
- current guard status
- whether a regression test exists

This should gradually build the regression pack.

---

## 10. Phase 1 issue taxonomy

Sentinel Phase 1 should classify issues as follows:

| Issue class | Meaning | Phase 1 action |
|---|---|---|
| ALIAS_MAPPING_DEFECT | Alias fails to resolve to expected canonical ID | Report defect; escalate for governed fix |
| CANONICAL_ID_MISMATCH | Present marker treated as missing or wrong canonical key used | Report defect; escalate |
| UI_INTERNAL_LABEL_LEAK | Raw slug/internal/backend label visible to customer | Report defect; may later become narrow auto-fix candidate, but not Phase 1 |
| ESCAPED_DEFECT_UNGUARDED | Known failure class lacks permanent regression test | Report test gap |
| REGRESSION_FAILURE | Existing regression now fails | Report defect; block release recommendation |
| TEST_GAP_ONLY | No defect proven, but inadequate coverage for touched surface | Report coverage gap |
| STALE_TEST_RISK | Test appears stale, duplicated, or no longer representative | Report testing debt |
| PERSISTED_REPLAY_GAP | Snapshot/persistence risk touched but no adequate replay proof exists | Report escalation/gap |
| GOVERNANCE_SURFACE_TOUCHED | SSOT, Knowledge Bus, Automation Bus, gate/kernel or Intelligence Core touched | Escalate; no Sentinel action beyond report |
| FRONTEND_TRUST_RISK | Customer-facing result surface changed | Run/check trust-surface tests and report |

---

## 11. Deterministic proof required

Every Sentinel issue must include deterministic evidence.

Minimum evidence:

- file/path or fixture involved
- test command or check name
- input used
- expected result
- actual result
- pass/fail status
- whether the issue is reproducible
- whether the failure affects customer-facing output
- whether governance escalation is required

For alias/canonical defects:

- alias input
- expected canonical ID
- actual canonical ID
- registry source
- normaliser/parser path tested

For slug leakage:

- component/page tested
- fixture/mock result used
- rendered visible text scanned
- leaked token/pattern found

For escaped-defect gaps:

- escaped defect class
- current test coverage status
- missing fixture/test asset
- recommended test pack location

For persistence/snapshot gaps:

- stored/golden result used, if any
- current schema/DTO expectation
- compatibility result
- whether old result can be safely displayed

Phase 1 should not rely on LLM judgement as proof. LLMs may summarise, classify, and recommend. Deterministic tests and file evidence must decide pass/fail.

---

## 12. Escalation thresholds

Sentinel must escalate rather than act when:

- scoring logic is affected
- confidence logic is affected
- signal firing is affected
- consequence logic is affected
- medical meaning may change
- SSOT files are touched
- Knowledge Bus signal libraries are touched
- Automation Bus or gate/kernel files are touched
- persistence/backfill behaviour is involved
- multiple authorities disagree
- root cause is unclear
- a fix cannot be proven deterministically
- customer-facing medical interpretation could change
- any HIGH-risk SOP surface is involved

In Phase 1, all fixes escalate. Sentinel reports only.

---

## 13. Evidence and audit output

Phase 1 Sentinel should produce a compact report per run.

Suggested report fields:

```yaml
sentinel_report_version: "0.1"
run_id:
run_type: manual | changed_files | scheduled | escaped_defect
timestamp_utc:
branch:
changed_files:
classified_surfaces:
risk_summary:
tests_selected:
tests_run:
results:
issues:
coverage_gaps:
escaped_defect_pack_status:
governance_escalation_required:
recommended_next_action:
auto_remediation_attempted: false
```

Reports should live outside Automation Bus state.

Recommended location:

```text
sentinel/reports/
sentinel/state/
sentinel/packs/
```

This avoids corrupting or confusing existing Automation Bus artefacts.

Sentinel must read but not write:

- `automation_bus/state/work_package_active.json`
- `automation_bus/latest_gate_evidence.json`
- `automation_bus/latest_gate_output.txt`
- `automation_bus/latest_audit_summary.md`
- SSOT files
- Knowledge Bus packages
- gate/kernel scripts

---

## 14. Success criteria after 2–3 weeks

Phase 1 should be judged by practical value, not architectural elegance.

Success criteria:

1. GGT-style alias failures are automatically caught.
2. Bilirubin-style canonical mismatches are automatically caught.
3. Internal slug/internal-label leaks are automatically caught or reported.
4. Known escaped defects have named regression coverage or documented coverage gaps.
5. Sentinel can classify changed files into sensible risk surfaces.
6. Sentinel can recommend the correct narrow test pack for common changes.
7. Reports are readable enough for GPT/Claude/Cursor/humans to act on.
8. No code or governed asset is modified by Sentinel.
9. The team sees fewer surprises in UAT.
10. The team can decide Phase 2 based on evidence, not theory.

Failure criteria:

- Sentinel produces noisy reports nobody trusts
- it runs too many irrelevant tests
- it misses the recent escaped-defect classes
- it attempts to modify governed files
- it blurs the boundary between testing intelligence and implementation authority
- it adds process without reducing defect escape risk

---

## 15. Phase 2 candidates, not Phase 1

If Phase 1 proves useful, Phase 2 can consider:

- persisted-result compatibility harness
- old golden-run replay against current DTO schema
- Playwright results-page trust scan
- narrative coherence checks across collapsed and expanded sections
- automated PR comments with selected test recommendations
- stricter CI integration
- stale/duplicate test quarantine
- structured escaped-defect ledger
- limited proposal-only fix generation

Auto-remediation should remain out of scope until Phase 2 or Phase 3, and even then only for narrow non-medical changes such as:

- adding a safe display label
- adding a missing alias where deterministic proof is overwhelming
- generating a regression test fixture
- adding a forbidden-token UI test

Even these should start as proposed fixes, not automatically applied fixes.

---

## 16. Open decisions for leadership

Before implementation, leadership should decide:

1. Should Phase 1 Sentinel run manually first, or should it be wired immediately into PR/branch workflows?
2. What is the canonical home for Sentinel reports: `sentinel/`, `docs/testing/sentinel/`, or another location?
3. Should escaped-defect packs live under `backend/tests/regression/` and `frontend/tests/regression/`?
4. Should Phase 1 block merges, or only advise?
5. Who owns accepting a new escaped defect into the regression pack?
6. Should Playwright be repaired before Phase 2, or deferred until after alias/canonical and slug checks prove value?
7. Should stale/duplicate test-tree cleanup be a separate testing-debt sprint?
8. Should Sentinel eventually integrate with Automation Bus, or remain a parallel reporting layer?

Recommended answers for Phase 1:

- manual first
- report-only
- no merge blocking initially
- escaped-defect packs under explicit regression folders
- Sentinel reports outside Automation Bus
- Playwright repair deferred until after Phase 1 value is proven
- no auto-remediation

---

## 17. Final recommendation

Proceed with a narrow Phase 1 Sentinel slice.

Build only enough to prove value:

1. changed-file classification
2. alias/canonical sweep
3. escaped-defect regression pack
4. frontend slug/internal-label leakage guard
5. report-only evidence output

Do not start with the full Sentinel architecture.

The product already has enough deterministic testing assets to support this first slice. The immediate gap is not test volume. The immediate gap is focused orchestration around known escaped defect classes and customer-trust surfaces.

Phase 1 should be treated as a product-quality experiment with a strict outcome:

> After 2–3 weeks, either Sentinel is catching real issues earlier and earning trust, or it is not.

That evidence should determine the next investment.
