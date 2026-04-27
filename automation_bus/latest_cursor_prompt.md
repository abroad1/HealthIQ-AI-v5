---
work_id: D-6
branch: feature/wave1-architecture-remediation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# D-6 — Wave 1 architecture remediation + backfill

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.

---

## Objective

Implement the coordinated remediation package for the Wave 1 consumer-layer defect cluster.

This sprint must fix the structural problem where multiple independent authorities can tell different stories across:

- Wave 1 headline
- Wave 1 contributor
- Wave 1 consequence
- Wave 1 next step
- “What’s driving this”

It must also ensure that:
- new analyses use corrected Wave 1 behaviour
- existing analyses can be repaired via governed backfill
- corrected vs legacy card outputs are explicitly versioned

This sprint must fix both:
1. the underlying multi-authority architecture problem
2. the primary observed UAT symptom, where a card can say “looks strong” while the same card’s consequence text signals risk/review

This is the bounded remediation for the Wave 1 consumer layer.
It is not a Phase 2 sprint.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/wave1-architecture-remediation`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Precondition

Prior investigations have already established:

- Wave 1 consumer-layer architecture is structurally flawed because multiple independent authorities can produce contradictory narratives
- existing analyses are served from frozen stored snapshots
- lightweight recompute is not feasible
- programmatic rerun from stored raw inputs is feasible with a small adapter/shim
- versioned backfill is required

Before implementation, restate briefly:

- the structural defect being fixed
- why a single primary-pattern selector is required
- why backfill is required for existing analyses
- why this sprint must fix the real UAT symptom, not just internal architecture

If prior findings appear inconsistent with repo reality, STOP and report.

---

## In scope

### Wave 1 domains only
- Cardiovascular health
- Blood sugar control
- Liver health

### This sprint must include all of the following:

#### A. Model/versioning
1. Add explicit version state to Wave 1 card objects:
   - `card_schema_version`
2. This field **must** be declared with a safe default:
   - `Field(default="1.0")`
3. Ensure old records deserialize safely with default `"1.0"`
4. New corrected records must emit `"1.1"`
5. Preserve legacy card output during backfill validation via temporary legacy storage

#### B. Unified primary-pattern selector
1. Introduce one authoritative primary-pattern resolution step per Wave 1 domain
2. Use the **existing** resolver in:
   - `backend/core/analytics/domain_score_assembler.py`
   - `_select_primary_idl()`
3. Do **not** introduce a second parallel resolver
4. Wire the resolved output from `_select_primary_idl()` through to:
   - headline
   - contributor
   - consequence
   - next step
   - evidence anchor
5. Remove independent greedy re-selection across those fields

#### C. Headline coherence fix
1. The headline logic must no longer say:
   - “looks strong”
   - or any similarly reassuring equivalent
   when the resolved primary pattern is risk-led / strain-led / review-led
2. This must apply to all relevant bands, not just `stable`
3. Specifically:
   - `headline_cv_coherent()` must guard **strong as well as stable**
   - `headline_met_coherent()` must guard **strong as well as stable**
4. The resolved primary pattern must control whether the headline is reassuring or cautionary
5. Do not leave headline logic band-only when the primary pattern clearly indicates risk/review
6. For the `strong + active risk-pattern` case, use a context-aware alternative headline instead of “looks strong”

#### D. Liver confidence tier fix
1. Include the liver confidence architecture fix in this sprint
2. Do not allow the structurally weak hepatic cluster rail confidence to suppress the correct domain-level hepatic confidence result
3. The user-facing liver confidence tier must reflect the proper domain-level hepatic marker-depth logic already identified in investigation
4. If this requires replacing the merge behaviour in `liv_block()`, do so explicitly and report it

#### E. Lipid-dominant cardiovascular consequence gap
This issue is **deferred** from D-6.

1. Do not expand this sprint into a KB content sprint for the lipid-dominant CV `why_it_matters` gap
2. Explicitly preserve/report this as a known deferred item for a later KB/content sprint
3. Do not silently lose or ignore the issue in reporting

#### F. “What’s driving this” authority alignment
This sprint must structurally align “What’s driving this” with the same resolved Wave 1 authority.

Chosen implementation direction:
- **backend-led authority alignment**

Required approach:
1. The backend must emit the resolved Wave 1 authority needed for aligned driving-signal rendering
2. The frontend must consume that aligned Wave 1 authority rather than continuing to rely on the independent arbitration-cluster path for the Wave 1 story
3. Do not implement a superficial frontend-only patch that leaves the independent authority intact underneath
4. Be explicit about the chosen mechanism. For this sprint:
   - backend emits Wave 1-aligned driving signal basis
   - frontend renders from that emitted aligned basis for Wave 1
5. Do not leave mechanism choice open

#### G. Backfill runner
1. Create a dedicated backfill runner that:
   - reads stored `raw_biomarkers`
   - reads stored `questionnaire_data`
   - reconstructs the minimum input needed
   - reruns the corrected pipeline programmatically
   - writes corrected `consumer_domain_scores`
   - tags corrected records with `card_schema_version: "1.1"`
   - preserves original card payload during validation window as legacy data
2. This must not require user resubmission

#### H. Backfill prerequisites explicitly required
The backfill runner must handle both of these known requirements:

1. **analysis_id override**
   - the orchestrator currently generates a fresh `analysis_id`
   - backfill must preserve the stored original analysis id when repairing an existing record
   - implement the minimum safe override/adaptation required

2. **unit-normalisation metadata recreation**
   - stored raw biomarkers do not carry persisted `__unit_normalisation_meta__`
   - the backfill runner must re-apply unit normalisation before invoking the pipeline so the orchestrator validation passes

#### I. Validation path
1. Add the minimum validation/audit output needed so the backfill run is deterministic and reviewable
2. At minimum log:
   - analysis id
   - old card version
   - new card version
   - old/new card hash or equivalent
   - whether legacy copy was preserved

---

## Out of scope

- hemoglobin/unit bug unless it turns out to be a tiny, clearly isolated, and safe fix discovered during implementation
- broader results-page redesign
- Phase 2 domains
- clinician PDF redesign
- pricing/billing/trends/actions/upload work
- broad pipeline refactor unrelated to Wave 1 remediation
- KB/content fix for lipid-dominant cardiovascular `why_it_matters`

Do not widen scope.

---

## Architectural constraints

### 1. Fix authority, not just copy
Do not patch sentence templates while leaving independent selection authorities in place.

### 2. Fix the real UAT symptom
A successful sprint must eliminate the observed “looks strong” + “risk/review” contradiction, not just tidy internal architecture.

### 3. Keep the core engine intact
This sprint fixes the consumer translation layer and its authority wiring.
Do not redesign the deeper analytical engine unless absolutely required.

### 4. Backfill is mandatory
A code-only fix is not acceptable because existing analyses are frozen snapshots.

### 5. Preserve auditability
Do not destructively overwrite old card outputs without preserving a legacy comparison path during validation.

### 6. Determinism
Backfill reruns must remain deterministic and auditable.

### 7. No mixed-truth rollout
Do not leave the system in a state where:
- new analyses are corrected
- old analyses remain silently broken
without an explicit governed backfill path

---

## Required implementation details

## A. ConsumerDomainScoreV1 schema

Add:
- `card_schema_version: str = Field(default="1.0")`

New corrected analyses must emit:
- `"1.1"`

Old records must continue to deserialize safely.

---

## B. Primary-pattern selector

Use the existing `_select_primary_idl()` as the single Wave 1 domain-resolution anchor.

This selector must resolve the domain’s authoritative pattern once.

At minimum it must determine:
- primary pattern id / record
- primary contributor basis
- primary consequence basis
- aligned evidence anchor basis
- aligned next-step basis
- aligned driver-biomarker basis for Wave 1 rendering

Downstream functions must consume this resolved object instead of independently re-resolving from separate authorities.

Do not create a second resolver.

---

## C. Headline logic requirements

For cardiovascular and blood sugar:

1. If the resolved primary pattern is risk-led / strain-led / review-led, the collapsed headline must not use “looks strong” language.
2. This applies regardless of whether the numeric band is `strong` or `stable`.
3. The headline must be coherently downstream of the resolved primary pattern, not only of the band label.
4. Report the exact new conditional logic used.

---

## D. Driving-strip alignment requirements

Chosen approach:
- backend emits Wave 1-aligned driving basis
- frontend uses that emitted aligned authority for Wave 1 rendering

Do not leave:
- Wave 1 card on one authority
- driving strip on another

If some non-Wave-1 parts of the page still use arbitration-derived driver logic, keep that distinction bounded and report it clearly.

---

## E. Backfill runner design

Create a dedicated backfill runner, not a broad pipeline rewrite.

Expected shape:
1. query existing analyses/results needing Wave 1 correction
2. load:
   - `analysis_id`
   - `raw_biomarkers`
   - `questionnaire_data`
   - `user_id`
3. re-apply unit normalisation
4. reconstruct minimal rerun inputs
5. preserve original analysis id during rerun
6. rerun corrected pipeline programmatically
7. extract corrected `consumer_domain_scores`
8. write corrected cards back into stored result blob
9. preserve original cards under temporary legacy key for validation window
10. log deterministic migration evidence

If a small orchestrator adapter/shim is needed, implement the minimum safe version.

---

## F. Legacy preservation / version policy

Use:
- explicit `card_schema_version`
- temporary legacy storage during validation window

Do not choose destructive overwrite-only behaviour.

If you need a naming decision for the temporary legacy key, make a clean minimal choice and report it.

---

## Files likely in scope

These are likely, not mandatory:

### Backend / analytics
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`
- any new helper module for authority alignment if needed

### Models / DTO
- `backend/core/models/results.py`
- any directly relevant DTO builder or serialization path

### Results read/write path
- `backend/app/routes/analysis.py`
- `backend/core/dto/builders.py`
- any directly relevant persistence serialization path

### Backfill / tooling
- new dedicated backfill runner under an appropriate governed scripts path
- any minimal helper needed to rerun analyses from stored inputs

### Frontend
- only what is needed to consume aligned Wave 1 authority safely
- keep frontend changes minimal and Wave 1-only

### Tests
- targeted backend tests
- targeted backfill tests
- targeted frontend tests only if rendering changes are necessary

---

## Files likely out of scope

Do not touch unless absolutely required and justified:

- unrelated Phase 2 domain logic
- pricing/billing
- upload flow redesign
- clinician PDF/export surfaces
- unrelated control-plane scripts
- broad SSOT content files beyond minimum justified changes

---

## Testing discipline

Do not run the full repository test suite.

Run only:

### Backend
1. targeted tests for primary-pattern resolution and narrative alignment
2. targeted tests proving no contributor/consequence mismatch remains within Wave 1 cards
3. targeted tests proving “strong” headline is blocked when the resolved primary pattern is risk-led
4. targeted tests for corrected liver confidence tier behaviour
5. targeted tests for driving-strip alignment
6. targeted tests for safe deserialization of old records with missing `card_schema_version`

### Backfill
7. targeted tests for the backfill runner using stored-analysis-like fixtures
8. targeted tests proving:
   - old cards preserved
   - new cards versioned `"1.1"`
   - corrected cards written deterministically
   - original analysis id preserved
   - unit-normalisation pre-step applied

### Frontend
9. only directly relevant tests if UI rendering changes are required
10. type-check for touched surfaces

Before running tests, state:
- what you will run
- why it is relevant
- what broader suites you are deliberately excluding

---

## Acceptance criteria

This sprint is successful only if:

1. Wave 1 cards no longer rely on multiple independent narrative selection authorities.
2. A single resolved primary pattern per domain is used for:
   - headline
   - contributor
   - consequence
   - next step
   - evidence anchor
3. “What’s driving this” is no longer an uncoordinated conflicting authority for Wave 1.
4. Cardiovascular and blood sugar cards can no longer say “looks strong” when the resolved primary pattern indicates risk/review.
5. Liver user-facing confidence tier reflects the correct domain-level hepatic logic.
6. `ConsumerDomainScoreV1` includes safe explicit versioning.
7. New corrected analyses emit `card_schema_version: "1.1"`.
8. Existing records can be backfilled from stored raw inputs without user resubmission.
9. Legacy card data is preserved during the validation window.
10. Targeted tests pass.
11. No Phase 2 scope creep is introduced.
12. The deferred lipid-dominant cardiovascular content gap is explicitly reported as deferred, not silently ignored.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- structural defect being fixed
- concrete UAT symptom being fixed

### 3. Requested changes made
- exact files changed
- where the primary-pattern selector now lives
- how headline/contributor/consequence/next-step now share authority
- how “What’s driving this” was aligned
- how versioning was added
- how the strong-band headline contradiction was eliminated
- how liver confidence was corrected
- confirm the lipid-dominant consequence gap remains explicitly deferred

### 4. Backfill runner
- exact files added/changed
- how stored analyses are rerun
- how original analysis id is preserved
- how unit-normalisation metadata is recreated
- what legacy preservation key/path is used
- what evidence/logging is produced

### 5. Tests run
- exact tests
- results

### 6. Operational rollout note
- what needs to happen in order:
  - deploy
  - backfill
  - validation
  - cleanup of legacy key, if planned

### 7. Known limits intentionally deferred
- anything intentionally left for later
- especially any hemoglobin/unit issue kept out of scope
- lipid-dominant cardiovascular content gap

### 8. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report if any of the following occurs:

1. A unified primary-pattern selector cannot be introduced without broad engine refactor.
2. Driving-strip alignment turns out to require a much larger product redesign than this sprint can safely hold.
3. Stored raw inputs are insufficient in practice for deterministic rerun.
4. Legacy preservation cannot be implemented cleanly.
5. A separate hemoglobin/unit bug begins to dominate scope.
6. Phase 2 work starts to creep in.

If blocked, report:
- exact blocker
- affected files/surfaces
- smallest safe remediation path