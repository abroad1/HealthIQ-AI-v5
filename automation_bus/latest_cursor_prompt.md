---
work_id: D-1
branch: feature/domain-score-assembler-wave1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# D-1 — Wave 1 domain score + confidence contract and assembler

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.
Do not use `healthiq-frontend-shell`, `healthiq-qa-uat`, or `healthiq-docs-hygiene` for this sprint.

---

## Objective

Implement the first deterministic customer-domain translation layer for the three Wave 1 domains:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

This sprint must create the backend/domain contract and deterministic assembler that outputs:

- domain score
- band label
- confidence tier
- raw evidence references needed for later narrative assembly

This sprint must **not** expose these domains to the frontend yet.

Score and confidence must ship together in the backend contract.
Do not create an intermediate state where domain scores exist without confidence.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/domain-score-assembler-wave1`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Required background inputs

Read these before implementation:

1. `docs/HealthIQ_phased_customer_domain_score_sprint_plan_FINAL.md`
2. `docs/Strategy_A_Launch_Domains_Implementation_Blueprint.md`
3. `docs/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md`
4. `docs/Strategy_A_Domain_Narrative_Contract_v1.md`
5. `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`
6. `AGENTS.md`
7. `.cursor/rules/healthiq-core-engine.mdc`
8. `docs/AUTOMATION_BUS_SOP_v1.3.1.md`

Treat those as the governing context for this sprint.

---

## In scope

### Domain coverage
Wave 1 only:

- Cardiovascular health
- Blood sugar control
- Liver health

### Backend work
1. Create a new deterministic domain score assembler layer above the current engine outputs.
2. Extend the analysis result contract with a new domain score structure.
3. Implement score + confidence together for the three in-scope domains.
4. Emit raw evidence references needed for Sprint D-2 narrative assembly.
5. Document any explicit calibration or mapping rules required to avoid mixing incompatible tracks.

---

## Out of scope

- frontend rendering
- domain narrative sentence assembly
- clinician PDF changes
- thyroid scoring
- kidney eGFR redesign
- blood/iron/oxygen aggregation
- second-wave domains
- LLM narrative generation
- broad refactors outside the minimal touched surfaces

Do not widen scope.

---

## Architectural constraints

### 1. Translation layer only
This sprint creates a new deterministic translation layer above:
- scoring results
- burden/capacity outputs
- active signals
- IDL references

It must not alter the underlying scoring engine, burden engine, or phenotype engine except where strictly required for contract-safe read access.

### 2. Score and confidence ship together
No domain score object may be produced without confidence.

### 3. Do not mix scoring tracks casually
You must explicitly distinguish between:
- scoring-policy range-position rails
- burden/capacity rails

They use different calibrations.
They cannot be blended unless the domain-specific rule is explicit and documented in code/comments/tests.

### 4. Consumer/clinical naming separation
The new contract may carry both consumer and clinical labels, but consumer labels must remain a dashboard-layer construct and must not replace clinician-facing labels elsewhere.

### 5. No frontend exposure
The new contract is backend-only in this sprint.
Do not wire it into results pages yet.

---

## Required domain rules

## Domain 1 — Cardiovascular health

### Base score source
Use the existing `cardiovascular` scoring rail as the base score source.

### Confidence
Build confidence from current repo-grounded evidence such as:
- core lipid marker coverage
- ratio availability where applicable
- signal coherence
- any approved extended-marker support as confidence enhancement, not silent score blending

### Constraint
Do not silently fold CRP, homocysteine, ApoB, ApoA1, or other non-rail markers into the numeric score unless you define and document an explicit domain rule and it remains within the approved repo-grounded Strategy A plan.

### Raw evidence references to emit
At minimum enough to support later narrative assembly:
- contributing system key(s)
- active signal ids
- primary IDL record id if any
- missing markers / confidence-improvers
- any explicit caveat flags

---

## Domain 2 — Blood sugar control

### Base score source
Use the existing `metabolic` scoring rail as the base score source.

### Confidence
Build confidence from:
- glucose/HbA1c base coverage
- insulin/triglyceride/TyG-supporting availability where applicable
- signal coherence

### Constraint
Keep this domain explicitly separated from the broader metabolic burden track.
Do not let electrolyte-heavy capacity/burden logic distort the consumer blood sugar domain score.

### Important note
Do not claim a governed “prediabetes override” unless you are directly using an existing approved implementation path already present in the repo and can cite it in your report.

### Raw evidence references to emit
Same minimum structure as above.

---

## Domain 3 — Liver health

### Base score source
Use the existing `liver` scoring rail as the base score source.

### Important mapping rule
Scoring uses `liver`.
Burden/capacity uses `hepatic`.

This must be handled explicitly and correctly.
Do not accidentally look up `system_capacity_scores["liver"]` if the actual key is `hepatic`.

### Confidence
You must not rely only on existing hepatic cluster confidence if it is too narrow.
Implement the explicit Wave 1 liver confidence logic required by the narrative research and plan.

### Constraint
If you use hepatic burden/capacity context, the blend or caveat rule must be explicit and documented.
Do not imply a comprehensive liver assessment if the score is still largely enzyme-driven.

### Raw evidence references to emit
Same minimum structure as above, plus any liver/hepatic mapping or caveat flags needed later.

---

## Required contract shape

Add a new backend/domain contract surface, for example `consumer_domain_scores` or equivalent, containing per-domain objects.

Each per-domain object must contain at minimum:

- `domain_id`
- `consumer_label`
- `clinical_label`
- `score`
- `band_label`
- `confidence_tier`
- `active_signal_ids`
- `primary_idl_record_id` (nullable)
- `missing_marker_ids` or equivalent
- `source_track` or equivalent, if needed to make calibration provenance explicit
- `caveat_flags` or equivalent, if needed to support truthful frontend behaviour later

Do not populate final user-facing prose sentences yet unless a field is unavoidable for backward-compatible reasons.
Sprint D-2 owns sentence assembly.

If placeholder/null sentence fields are introduced now for contract stability, state that explicitly and keep them unpopulated.

---

## Files likely in scope

These are likely, not mandatory:

- `backend/core/analytics/` (new assembler module likely lives here)
- `backend/core/models/results.py`
- `backend/core/dto/builders.py`
- `backend/core/pipeline/orchestrator.py`
- any closely related contract/model files required to carry the new domain structure
- targeted backend tests
- minimal supporting docs/comments where essential

### Likely new file
- `backend/core/analytics/domain_score_assembler.py` or equivalent

---

## Files likely out of scope

Do not touch unless absolutely required and justified in your report:

- `frontend/**`
- `knowledge_bus/**`
- clinician PDF/export surfaces
- unrelated analytics modules
- broad SSOT changes
- broad cluster/scoring redesign

---

## Implementation boundary between D-1 and D-2

This sprint must leave behind:

### D-1 owns
- domain score object shape
- numeric score
- confidence tier
- raw evidence references
- mapping/caveat fields
- deterministic backend assembly

### D-2 will own
- contributor sentence assembly
- confidence sentence assembly
- consequence sentence assembly
- next-step sentence assembly
- any small governed content fix needed for the cardiovascular lipid-dominant consequence path

Do not absorb D-2 work into D-1.

---

## Testing discipline

Do not run the full repository test suite.

Run only:

1. new or updated targeted backend tests for the domain assembler and DTO contract
2. directly relevant existing tests for touched result/DTO/orchestrator paths
3. any minimal validation needed to prove:
   - the three domains are emitted
   - score and confidence are emitted together
   - liver/hepatic mapping is correct
   - no accidental frontend dependency was introduced

Before running tests, state:
- what you will run
- why it is relevant
- what you are deliberately not running

---

## Acceptance criteria

This sprint is successful only if:

1. Wave 1 domain objects exist for:
   - cardiovascular health
   - blood sugar control
   - liver health

2. Each domain object emits:
   - score
   - band label
   - confidence tier
   - raw evidence references for later narrative assembly

3. Score and confidence are emitted together.

4. No frontend exposure is introduced.

5. Liver/hepatic key handling is explicit and correct.

6. Any use of burden/capacity context is explicit and calibration-safe.

7. The contract is additive and backward-compatible.

8. Tests pass for the targeted touched surfaces.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- explicit score source per domain
- explicit confidence source per domain

### 3. Requested changes made
- exact files changed
- what new contract/model was created
- where assembler logic lives
- how each of the three domains is built

### 4. Calibration handling
- how scoring rails vs burden/capacity rails were handled
- especially for liver/hepatic

### 5. Tests run
- exact tests
- results

### 6. Known limits intentionally deferred to D-2
- sentence assembly
- cardiovascular lipid-dominant consequence content gap
- anything else deferred on purpose

### 7. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report instead of widening scope if any of the following occurs:

1. A domain cannot be built without a broader SSOT redesign.
2. You need to alter frontend code to validate the backend contract.
3. Confidence cannot be emitted without inventing unsupported logic.
4. The liver/hepatic mapping cannot be resolved cleanly.
5. The work begins to require narrative sentence generation rather than raw contract assembly.
6. A second-wave domain starts to creep into the implementation.

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path