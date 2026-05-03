Use this as the implementation brief.

````md id="61842"
You are preparing the implementation brief for **HealthIQ AI Phase 1 Sentinel**.

This is a build brief for the first practical Sentinel slice.
Do not broaden scope.
Do not redesign the full future Sentinel.
Do not add auto-remediation.
Do not convert this into a giant testing platform sprint.

## Objective

Implement the smallest useful **report-only** Sentinel slice that can catch recent escaped defect classes earlier than manual UAT.

Phase 1 Sentinel must cover only:

1. changed-file risk classification
2. alias/canonical sweep
3. escaped-defect regression pack
4. frontend slug/internal-label leakage guard
5. structured report output

This is a proof-of-value slice, not the final system.

---

## What Phase 1 Sentinel is

A small background/manual-run quality layer that:

- inspects changed files or a requested surface
- classifies the risk surface
- selects the narrow relevant deterministic checks
- runs those checks
- reports defects, regression failures, and coverage gaps
- never modifies product code
- never modifies governed assets
- never approves its own findings

It is **report-only**.

---

## What Phase 1 Sentinel is not

Do not build:

- a full autonomous Sentinel
- auto-fix or auto-remediation
- branch creation
- PR comment bots
- merge blocking
- full persisted-result replay infrastructure
- broad Playwright orchestration
- test-estate cleanup
- whole-repo smart dependency analysis

Stay narrow.

---

## In scope

### A. Changed-file classifier
A simple path-based classifier that maps an input file list into broad risk surfaces.

Minimum surfaces:

- parser / alias / canonical
- SSOT / canonical authority
- analytics / scoring / signal
- frontend trust surface
- persistence / snapshot surface
- governance / control-plane
- Knowledge Bus / intelligence content

It is acceptable for the classifier to be conservative.
If uncertain, it should widen the recommendation, not narrow it.

### B. Alias / canonical sweep
Add or wire a deterministic sweep that can:
- validate known alias → canonical mappings
- surface unmapped aliases
- surface wrong-canonical resolutions
- specifically include the recent GGT and bilirubin escaped-defect cases

This should reuse existing alias/normalisation infrastructure wherever possible.

### C. Escaped-defect regression pack
Create a named escaped-defect regression pack for the known defect classes.

At minimum, include checks for:
1. GGT alias miss
2. bilirubin canonical mismatch
3. internal slug/internal-label leakage
4. Wave 1 contradiction class status
5. persisted-result replay gap status placeholder

The first three should be active deterministic checks.
The last two may initially be status/reporting items if full deterministic coverage is not yet ready.

### D. Frontend slug/internal-label leakage guard
Add or wire a deterministic frontend trust-surface check that can detect:
- raw biomarker slugs
- snake_case labels
- `ph_*_v*` style internal ids
- obvious backend/internal identifiers
appearing in customer-facing results surfaces

Keep this narrowly focused on customer-visible result surfaces first.

### E. Structured report output
Each Sentinel run must produce a compact structured report containing:

- run id
- trigger type
- branch
- changed files
- classified surfaces
- tests selected
- tests run
- results
- issues found
- coverage gaps found
- escaped-defect pack status
- governance escalation required
- confirmation that no auto-remediation was attempted

Reports must live outside Automation Bus artefacts.

---

## Out of scope

- any code modification to product logic
- SSOT changes
- Knowledge Bus package changes
- Automation Bus artefact mutation
- gate/kernel script mutation
- scoring/signal/confidence/consequence changes
- persistence/backfill implementation
- broad UI redesign
- full Playwright restore programme
- stale test cleanup sprint

Do not widen scope.

---

## Reuse first

Phase 1 must reuse existing assets wherever possible.

Expected reuse areas include:
- alias registry service / alias resolution tests
- normalisation tests
- venous alias integration tests
- Wave 1 liver/marker mapping tests
- relevant frontend results/component tests
- OPS-style trust checks
- existing fixtures: AB/VR, golden panels, phenotype fixtures, frontend result mocks

Do not duplicate existing valuable tests unless there is a clear reason.

---

## Existing tests: handling policy

### Keep and reuse
Treat these as authoritative unless clearly broken:
- deterministic backend unit tests
- enforcement tests
- validator tests
- golden/fixture tests
- recent escaped-defect tests
- active frontend results/component tests

### Flag but do not clean up yet
Only report these as debt candidates:
- stale browser tests
- duplicate test trees
- over-mocked persistence tests
- archived or sprint-specific tests that may be misleading
- frontend mocks that may be out of sync

Phase 1 is not a cleanup sprint.

---

## Trigger model for Phase 1

Phase 1 should support:

### 1. Manual run
Primary starting mode.
Allow Sentinel to be run against:
- current branch
- a file list
- a known defect class
- a specific surface

### 2. Changed-file run
Given a changed-file list, classify surfaces and run the narrow relevant checks.

### 3. Scheduled lightweight sweep
Only if simple to support without scope creep.
Keep it narrow:
- alias/canonical sweep
- slug/internal-label guard
- escaped-defect pack

### 4. Escaped-defect intake
Support a simple way to record that a newly escaped defect should be added to the regression pack.

---

## Deterministic proof requirements

Every surfaced issue must include deterministic evidence.

Minimum evidence:
- what triggered the run
- what files/surface were involved
- what check/test was selected
- what input/fixture was used
- expected result/invariant
- actual result
- pass/fail
- whether customer-facing output is affected
- whether governance escalation is required

Phase 1 must not rely on LLM judgement as proof.

---

## Governance rules

Phase 1 Sentinel must:

- read but not write Automation Bus artefacts
- read but not write SSOT
- read but not write Knowledge Bus packages
- never modify product code
- never mutate gate evidence
- never self-certify a fix
- escalate when HIGH-risk or meaning-bearing surfaces are implicated

If a touched path falls into governed medical/analytical/control-plane territory, Sentinel may report, but not act.

---

## Recommended file/output location

Use a separate Sentinel namespace, for example:

```text
sentinel/
  reports/
  state/
  packs/
````

Do not place Sentinel run output inside `automation_bus/`.

---

## Acceptance criteria

Phase 1 is successful only if:

1. It can classify changed files into sensible broad risk surfaces.
2. It can run or select a narrow alias/canonical sweep.
3. It can run or report the escaped-defect regression pack.
4. It can detect/report frontend slug/internal-label leakage on scoped result surfaces.
5. It produces a structured report for each run.
6. It does not modify product code or governed assets.
7. It clearly reports coverage gaps where proof is inadequate.
8. It remains narrow and report-only.

---

## Reporting requirements

When the implementation is complete, report back in these sections:

### 1. Scope delivered

* what was built
* what was intentionally not built

### 2. Files added/changed

* exact locations
* why each was needed

### 3. Changed-file classifier

* what surfaces it recognises
* how conservative it is

### 4. Alias/canonical sweep

* what exact checks now run
* whether GGT and bilirubin cases are explicitly covered

### 5. Escaped-defect pack

* what defect classes are now actively guarded
* what remains placeholder/report-only

### 6. Frontend slug/internal-label guard

* what surfaces it checks
* what forbidden patterns it looks for

### 7. Report output

* report schema
* output location
* example of what a run produces

### 8. Deterministic proof

* what evidence is attached to failures
* how coverage gaps are surfaced

### 9. Governance boundaries preserved

* what Sentinel does not mutate
* what still escalates

### 10. Tests run

* exact tests/checks
* results

### 11. Known limits intentionally deferred

* anything left for later Phase 2+

### 12. Uncommitted / not merged

* confirm work is not merged to `main`

---

## STOP conditions

STOP and report if:

1. the implementation starts drifting into auto-remediation
2. the implementation requires mutation of Automation Bus or gate artefacts
3. the implementation requires SSOT or Knowledge Bus modification
4. the first slice grows beyond alias/canonical + escaped-defect + slug guard + reporting
5. the changed-file classifier cannot be implemented without much broader repo intelligence work
6. the deterministic proof model cannot be satisfied for the included checks

If blocked, report:

* exact blocker
* affected files/surfaces
* smallest safe fallback

```