---
work_id: KB-HBA1C-GOV1
branch: feature/hba1c-dual-id-governance
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-HBA1C-GOV1 — HbA1c Dual-ID Governance and Unit Reconciliation

## Objective

Fix the critical UAT blocker where HbA1c in `mmol/mol` fails analysis start, and enforce deterministic single-path Layer B analytical handling for HbA1c when commercial blood panels contain both:

- `HbA1c (Venous)` / IFCC-style reporting
- `HbA1c % (Venous)` / NGSP-style reporting

This is not a UI sprint.
This is not a broad unit-system redesign.
This is a governed ingestion-and-analysis input correction.

The required product outcome is:

- both HbA1c report-line representations may remain available to user-visible biomarker/results surfaces
- only one canonical HbA1c representation may feed Layer B analysis
- Layer B canonical HbA1c identity remains:
  - biomarker id: `hba1c`
  - canonical analytical unit: `%`

---

## Stage 1A — Authority Preflight (MANDATORY)

### Canonical Layer B HbA1c Analytical Truth

The authoritative Layer B HbA1c analytical identity for this sprint is fixed as:

- biomarker id: `hba1c`
- canonical unit: `%`

This is based on existing repo reality across:

- `backend/ssot/biomarkers.yaml`
- `backend/ssot/clusters.yaml`
- `backend/ssot/criticality.yaml`
- `backend/ssot/ranges.yaml`
- `backend/core/analytics/insight_graph_builder.py`

Cursor must treat this as already decided architecture, not an open choice.

### Parallel HbA1c Identifier

A second SSOT biomarker id exists:

- `hba1c_pct`

This remains a valid parsed/display identifier in current repo reality, but it must not remain an independently contributing Layer B analytical path after this sprint.

### Unit Conversion Authority

Authoritative unit metadata and runtime handling are in:

- `backend/ssot/units.yaml`
- `backend/core/units/registry.py`

### Parsing / Canonicalisation / Analysis Path

Relevant runtime seam files include at minimum:

- `backend/app/routes/upload.py`
- `backend/app/routes/analysis.py`
- `backend/core/canonical/normalize.py`
- `backend/core/units/registry.py`
- `backend/core/pipeline/orchestrator.py`

---

## Stage 1B — Reality Check

Repo reality already established:

- `hba1c` and `hba1c_pct` are separate SSOT ids
- both can survive canonicalisation into runtime biomarker maps
- `hba1c` is the dominant Layer B analytical identity for core engine subsystems
- some KB signals still reference `hba1c_pct`
- `system_burden_registry.yaml` contains both ids
- runtime currently lacks `mmol/mol -> %` conversion for `hba1c`
- duplicate analytical contribution risk is real if both ids remain live

This sprint is not a no-op.

---

## Stage 1C — Intelligence Preflight

This sprint modifies governed runtime behaviour in the ingestion / normalisation / Layer B input path.

It affects:

- which HbA1c input reaches Layer B
- unit reconciliation before analysis
- whether duplicate HbA1c analytical contribution is possible
- which downstream signals and burden paths remain live

Therefore:

- `risk_level: HIGH`
- `change_type: MIXED`

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Canonical analytical HbA1c path

Only `hba1c` may feed Layer B analysis after arbitration.

### 2. Canonical analytical unit

Layer B analytical HbA1c must remain `%`.

Do not change canonical HbA1c base unit in SSOT.

### 3. Arbitration gate location

The arbitration gate must be inserted:

- after canonicalisation
- before `apply_unit_normalisation`

Cursor must not choose a different seam.

This is the required architectural insertion point.

### 4. Product handling rule

If both `hba1c` and `hba1c_pct` are present in one runtime biomarker set:

- both may remain available to user-visible/raw/result-facing layers if current response shaping supports that
- only `hba1c` may proceed into Layer B analytical input

### 5. Fate of `hba1c_pct` in Layer B

For this sprint:

- `hba1c_pct` must be suppressed from Layer B analytical input after arbitration
- `hba1c_pct`-based signals therefore become dormant in practice for this path
- `hba1c_pct` burden contribution therefore becomes dormant in practice for this path

Do not invent a second suppression mechanism elsewhere.
Do not leave `hba1c_pct` analytically live.

### 6. Conversion requirement

`hba1c` must support `mmol/mol -> %` so UK-style uploads can normalise successfully into the canonical Layer B HbA1c input.

---

## Scope

## Required Changes

### A. Add missing HbA1c reverse conversion support

Update the governed unit-conversion path so `hba1c` can normalise from:

- `mmol/mol` -> `%`

Preferred authoritative implementation:
- explicit SSOT conversion definition in `backend/ssot/units.yaml`
- corresponding runtime support in `backend/core/units/registry.py`

If runtime already loads SSOT conversion factors generically, use that path.
Do not hardcode a shadow authority elsewhere.

### B. Add deterministic HbA1c arbitration gate

At the exact architectural seam:

- after canonicalisation
- before `apply_unit_normalisation`

implement deterministic arbitration such that:

- `hba1c` remains the sole Layer B analytical HbA1c input
- `hba1c_pct` is removed from the Layer B-bound biomarker set
- this occurs before unit normalisation and before orchestrator input assembly

### C. Preserve downstream analysis contract

Do not redesign Layer B consumers.
Do not patch orchestrator, signal evaluator, or insight graph to compensate for duplicate HbA1c ids if the arbitration gate can prevent that upstream.

### D. Tests

Add the narrowest relevant test coverage proving:

1. `hba1c` accepts `mmol/mol` and normalises to `%`
2. when both `hba1c` and `hba1c_pct` are present, only `hba1c` reaches the Layer B-bound path
3. duplicate analytical contribution does not occur for the governed HbA1c path
4. current user-visible/raw retention is not broken unintentionally by the arbitration step, to the extent covered by existing response/normalisation tests

---

## Explicit Non-Goals

- no UI workaround
- no manual upload-data rewrite
- no change to canonical Layer B HbA1c id away from `hba1c`
- no change to canonical analytical unit away from `%`
- no broad redesign of the unit system
- no broad redesign of parsed biomarker display surfaces
- no refactor of all duplicate-clinical-analyte handling in the platform
- no Knowledge Bus content rewrite beyond what is strictly required by this governed runtime correction
- do not redesign `hba1c_pct` package strategy globally outside this sprint

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. The arbitration gate cannot be implemented at the declared seam without contradicting current runtime architecture
2. Implementing the gate would require changing the canonical Layer B HbA1c id away from `hba1c`
3. Both user-visible preservation and single analytical contribution cannot coexist without a broader response-model redesign
4. `hba1c_pct` suppression from Layer B would break a contract that cannot be safely adjusted within this sprint
5. A second authority source for HbA1c units or canonicality would be introduced
6. The fix would require opportunistic redesign of orchestrator, signal evaluator, or insight graph beyond bounded upstream arbitration
7. Clinical conversion precision cannot be implemented deterministically from governed SSOT/runtime authority

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Governed Fix

Implement:

- `mmol/mol -> %` support for `hba1c`
- HbA1c arbitration gate at the declared seam
- suppression of `hba1c_pct` from Layer B-bound analytical input

### Phase 2 — Validation

Verify:

- UAT blocker is removed
- Layer B sees only canonical `hba1c`
- `hba1c_pct` no longer contributes analytically
- determinism preserved
- no unintended breakage in upload -> analysis start path

---

## Regression Targets

Must verify all of the following.

### Unit Normalisation

- `hba1c` in `%` still behaves correctly
- `hba1c` in `mmol/mol` now normalises successfully to `%`
- no regression to existing glucose/lipid unit conversions

### Arbitration

- when only `hba1c` exists, behaviour is unchanged
- when only `hba1c_pct` exists, deterministic handling is explicit and tested according to the implemented gate logic
- when both exist, only `hba1c` reaches Layer B analytical input

### Layer B

- no duplicate HbA1c signal contribution
- no duplicate HbA1c burden contribution through the Layer B-bound input set
- core Layer B consumers (`clusters`, `criticality`, `insight graph`) continue to operate on canonical `hba1c`

### UAT blocker path

- analysis start no longer fails on UK-style HbA1c `mmol/mol` input

### Determinism

- same dual-input set always produces the same arbitrated Layer B-bound HbA1c outcome
- no randomness
- no silent fallback
- no implicit ordering dependence

---

## Test Requirements

Minimum required tests must cover:

1. `hba1c mmol/mol -> %` conversion
2. arbitration when both `hba1c` and `hba1c_pct` are present
3. proof that the Layer B-bound biomarker set excludes `hba1c_pct` after arbitration
4. proof that no duplicate analytical contribution path remains in the tested flow
5. preservation of expected behaviour for existing single-id HbA1c inputs

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- do not choose a different arbitration seam
- do not invent a different canonical HbA1c analytical id
- do not leave `hba1c_pct` analytically live and “hope” downstream consumers ignore it
- do not widen scope beyond this governed correction
- do not modify unrelated files

---

## Deliverables

Cursor must return:

1. files changed
2. exact arbitration seam used, with file path and function
3. implementation summary
4. tests run and results
5. evidence that `hba1c mmol/mol` now passes normalisation
6. evidence that only canonical `hba1c` reaches Layer B analytical input when both ids are present
7. confirmation of the practical fate of:
   - `hba1c_pct` signals
   - `hba1c_pct` burden contribution
8. any blockers encountered

---

## Governance

This is HIGH-risk governed behaviour work.

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