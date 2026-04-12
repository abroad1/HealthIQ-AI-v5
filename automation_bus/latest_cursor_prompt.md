---
work_id: BE-W1-PR1
branch: feature/parse-range-edit-and-missing-range-ux
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W1-PR1 — Parse fidelity, manual range correction, and missing-range UX

## Objective

Deliver a single governable Wave 1 remediation pass for the upload → parse → review → analysis-input journey.

This sprint must improve parsing fidelity where the lab provides richer range/context detail, allow users to add or edit reference range data manually in marker review, and clearly flag biomarkers whose range data is missing or insufficient so the user knows intervention is needed before trusting the result.

This sprint is explicitly **not** a broad fallback-range sprint.
Do not introduce broad hard-coded fallback ranges for ordinary biomarkers.
Do not change analytical scoring policy for ordinary biomarkers.

The required outcome is:

- parsed biomarkers preserve more usable lab range/context detail where already present
- marker review allows manual correction/addition of range data
- missing or insufficient range data is clearly surfaced in UX
- corrected range data flows through to analysis start
- the user is visibly informed when parsing requires intervention

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime investigations have established that:

- parser output can carry:
  - raw `reference`
  - `ref_low`
  - `ref_high`
- frontend upload mapping currently builds `referenceRange` only when both bounds exist in certain paths
- marker review/edit currently preserves `referenceRange` if present but does not let the user add or change it
- backend analysis payload already accepts `reference_range`
- scoring/display for ordinary biomarkers is currently lab-range sovereign
- broad governed fallback for ordinary biomarkers is not part of current runtime policy

This sprint must not guess a different policy truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- parser models / parser output definitions used in upload parse
- `backend/app/routes/upload.py`
- `backend/app/routes/analysis.py`
- normalization / biomarker metadata flow files actually used in the upload-to-analysis path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/upload/page.tsx`
- marker review components
- parsed biomarker edit dialog/component
- any parsed biomarker types/interfaces used between parse and analysis start

If hardening finds the active component paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real UAT and investigation findings and is not a no-op.

Confirmed current issues include:

- rich lab reference detail can be flattened or lost in parse/review
- some biomarkers reach results as “Not scored - no reference range available”
- the edit flow does not allow users to add or amend range data
- users currently have no credible correction path when parsing misses range information
- partial/one-sided bounds may be dropped before analysis even though downstream contracts can carry richer range metadata

---

## Stage 1C — Intelligence Preflight

This sprint changes user-editable data entering analysis and changes how missing/insufficient range data is surfaced before submission.

It therefore affects:

- upload review contract
- user-corrected biomarker payloads
- analysis input quality
- pre-analysis UX and gating

This is HIGH risk because it changes governed user-supplied input entering analysis, even though it must not change the scoring policy for ordinary biomarkers.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. No broad fallback-range expansion

Do not introduce broad hard-coded fallback ranges for ordinary biomarkers.

This sprint is not the place to change lab-range sovereignty for standard measured analytes.

### 2. Manual correction is the approved recovery path

When parsing misses or incompletely captures lab range data, the approved product response is:

- visibly flag the biomarker in the review UX
- allow the user to add or edit range data manually
- pass corrected range data into analysis

Do not replace this with hidden fallback behaviour.

### 3. Preserve richer lab detail where already available

If the parser already captures richer reference information, the frontend/review path must preserve as much usable range/context detail as the current contracts safely support.

Do not unnecessarily drop partial or structured information before analysis.

### 4. Missing/insufficient range data must be visible in UX

Users must be clearly shown which biomarkers need attention before analysis can be trusted.

This may be warning-state UX, row-level flags, or equivalent bounded cues — but it must be explicit.

### 5. Range editing must include the actual analytical fields

The user must be able to add/edit, at minimum where the contract supports it:

- minimum bound
- maximum bound
- unit

If raw reference text can be preserved safely in the parsed review model, that may also be retained, but the core requirement is analytical min/max/unit correction.

### 6. Keep the change within the upload-review seam

This sprint must stay in the seam:

- parse output
- upload review/edit state
- analysis-start payload preparation

Do not turn this into a broader scoring-policy or results-page sprint.

### 7. Apo ratio contract issue may be fixed only if it is in this same seam

If the `apolipoprotein_ratio_(venous)` unit/canonicalisation issue is confirmed to arise within the same upload-review contract seam, it may be fixed in this sprint.

Do not widen beyond that seam.

---

## Scope

## Required Changes

### A. Parse/review fidelity improvement

Improve the upload-review path so richer lab-provided range/context data is preserved where already available from the parser.

This includes eliminating avoidable frontend dropping of usable range information.

### B. Manual range editing in marker review

Update marker review/edit functionality so users can add/edit:

- min
- max
- unit

for parsed biomarkers before analysis start.

### C. Missing-range attention UX

Add clear review-stage indication for biomarkers whose range data is missing or insufficient for trusted downstream interpretation.

This must help users understand that they need to intervene.

### D. Analysis payload propagation

Ensure manually corrected range data is sent through the existing `reference_range` contract to analysis start.

### E. Contract-alignment fixes within the same seam

If the apo ratio unit/key issue is confirmed to live in this upload-review contract seam, fix it here in the narrowest safe way.

---

## Explicit Non-Goals

- no broad fallback-range implementation for ordinary biomarkers
- no scoring-policy change for ordinary biomarkers
- no Gemini/narrative/results-page work
- no questionnaire redesign
- no broad parser rewrite
- no full multi-profile sex/pregnancy-specific fallback-range system
- no second authority source for ranges
- no changes to downstream analytical logic except to consume corrected input already supported by contract

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Fixing the issue would require changing ordinary-biomarker scoring policy rather than the upload-review contract
2. Manual range correction cannot be propagated without changing core analytical boundaries beyond the existing `reference_range` contract
3. Preserving richer lab detail would require a broad parser rewrite rather than a bounded seam fix
4. A second range authority source would be introduced
5. The UX cannot clearly indicate missing/insufficient range state without broad redesign of the upload flow
6. Apo ratio remediation would require widening beyond the upload-review seam
7. The sprint would require introducing broad fallback behaviour contrary to the locked policy for this wave

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Upload-review contract improvement

Implement the bounded backend/frontend changes required so that:

- richer parsed range detail is preserved where possible
- users can manually add/edit range data in marker review
- missing/insufficient range data is clearly flagged
- corrected range data flows into analysis start

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- parsed biomarkers with missing range data are visibly flagged
- edited range data persists into analysis submission
- existing valid parse/review flow still works
- no scoring-policy changes were introduced

---

## Regression Targets

Must verify all of the following.

### Upload parse / review

- parsed biomarkers still load correctly into review
- valid existing range data is preserved
- richer parser-provided range detail is not unnecessarily dropped
- biomarkers with missing or insufficient range data are visibly flagged

### Edit flow

- users can add/edit min, max, and unit
- edited values survive save/reopen within the review flow
- range correction is included in analysis-start payload

### Analysis handoff

- existing `reference_range` contract is used
- corrected ranges reach backend analysis input
- no regressions to normal successful analysis submission

### Apo ratio (if included)

- if fixed in this sprint, unit/canonicalisation behaviour is correct within the upload-review seam
- no new validation blocker occurs for the ratio marker in the tested path

### Determinism and safety

- no hidden fallback ranges introduced for ordinary biomarkers
- no second range authority source introduced
- same edited input produces the same payload
- no randomness or implicit hidden repair logic

---

## Test Requirements

Minimum required tests must cover:

1. marker review edit/add of range min/max/unit
2. analysis payload includes corrected `reference_range`
3. missing-range attention state in the review layer
4. preservation of existing valid range data through review
5. any narrow apo ratio contract fix included in scope

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- do not turn this into a fallback-range sprint
- do not change ordinary-biomarker scoring policy
- do not invent a second range authority
- do not widen into results/questionnaire/narrative work
- do not perform broad parser redesign beyond the bounded seam improvement
- do not modify unrelated files

---

## Deliverables

Cursor must return:

1. files changed
2. exact backend files touched
3. exact frontend files touched
4. implementation summary
5. tests run and results
6. before/after evidence that:
   - missing-range biomarkers are now visibly flagged
   - users can add/edit min/max/unit
   - corrected ranges reach analysis start
7. whether apo ratio was included and, if so, exactly how it was fixed within seam
8. any blockers encountered

---

## Governance

This is HIGH-risk governed input-contract work.

Requires:

- Claude hardening
- kernel start
- controlled execution
- kernel finish
- gate evidence
- Claude audit summary
- GPT architectural review
- dual approval before merge

No shortcuts permitted.