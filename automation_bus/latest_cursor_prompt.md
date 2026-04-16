---
work_id: BE-IDL-1
branch: feature/be-idl-1-interpretation-display-layer
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-IDL-1 — Interpretation Display Layer v1

## Objective

Create the governed Interpretation Display Layer (IDL) as the sole authority between Layer B interpretation entities and the future Section 5 frontend pattern cards.

This sprint is a backend/content governance sprint.

It exists to solve a classification, naming, and surfacing-contract gap.

It does not redesign the underlying medical reasoning model.
It does not introduce new interpretation entities.
It does not implement Section 5 frontend rendering.

---

## Strategic decision already made

The following is already decided and is not open for reinterpretation in this sprint:

- HealthIQ retains **phenotype** as a strategic, GTM, and B2B methodology term.
- The current retail interpretation layer will use the medically stricter mixed classification model.
- The current interpretation set is a governed mixed set, not a blanket “all phenotype” set.
- Naming must remain revisable later through the governed IDL without rebuilding Layer B.
- Frontend Section 5 remains blocked until the IDL exists.

Your job is to implement that decision cleanly and deterministically.

---

## Required outcome

Deliver a versioned Interpretation Display Layer that:

1. classifies the current interpretation entities using the approved mixed model
2. provides approved clinician and retail labels
3. provides subtitle and why-it-matters copy
4. controls whether restricted terminology is permitted on the retail surface
5. publishes a typed IDL bundle on the analysis result payload
6. is sufficiently governed that a later FE sprint can render Section 5 without inventing taxonomy

---

## Classification model to support

The IDL must support these exact classes:

- `phenotype`
- `risk_construct`
- `organ_pattern`
- `syndrome_state`

No additional classes may be introduced in this sprint.

The implementation must preserve the ability to rename or reclassify later through the governed IDL layer without rebuilding the underlying Layer B interpretation system.

---

## Sprint scope

### In scope

#### 1. Define the IDL contract
Create a versioned typed backend contract for the Interpretation Display Layer.

At minimum, support fields for:

- `internal_id`
- `scientific_class`
- `clinical_display_label`
- `retail_display_label`
- `subtitle`
- `why_it_matters`
- `severity_state`
- `supporting_biomarkers_summary`
- `frontend_allowed_term`
- `display_order_priority`
- `enabled_for_frontend`

Support optional fields for:

- `supporting_systems_summary`
- `user_safe_description`
- `future_commercial_domain`
- `display_caveat`

Do not widen the contract casually beyond what is needed for governed Section 5 rendering.

#### 2. Create the governed records for the current interpretation set
Author the initial IDL records for the current 9 existing interpretation entities using the agreed mixed classification model.

The records must live in a governed backend/content authority layer, not in frontend code.

#### 3. Publish the IDL deterministically
Add the deterministic publisher / compiler / mapper step required to expose the IDL bundle on the analysis result payload.

The frontend must later be able to consume this bundle directly.

#### 4. Extend DTO / API output
Expose the IDL bundle in the typed analysis result path.

#### 5. Add governance validation
Add tests / validations covering at minimum:

- required field completeness
- valid `scientific_class`
- valid `frontend_allowed_term`
- unique `display_order_priority`
- banned generic retail labels
- enforcement of restricted-term rules at retail label level

#### 6. Preserve reversibility
Ensure naming and classification remain externalised and revisable later through the IDL authority, rather than hardcoded into core reasoning logic or frontend presentation logic.

---

## Out of scope

The following are explicitly out of scope:

- Section 5 frontend implementation
- any Gemini / LLM-generated Section 5 copy
- new interpretation entities
- changes to biomarker-level UX
- broader GTM copywriting
- redesign of clinician summary architecture unless minimally required to consume typed IDL output
- analytical or behavioural changes to Layer B reasoning unless strictly required for bounded deterministic publication of already-existing entities

---

## Architectural rules

### Rule 1 — IDL is the sole Section 5 authority
Section 5 must not read directly from raw clusters, raw system outputs, or ad hoc frontend mappings once the IDL exists.

### Rule 2 — backend/content authority only
Naming, classification, subtitles, and why-it-matters copy must live in a governed backend/content authority source.

Frontend code must not:
- classify entities
- invent labels
- infer whether something is a phenotype
- substitute generic buckets as product card labels

### Rule 3 — no duplicate authority
Do not create multiple competing authority sources for classification or naming.

### Rule 4 — preserve Layer B / Layer C separation
This sprint creates the contract between Layer B and Layer C.
It must not collapse presentation naming into raw reasoning logic, and it must not move taxonomy decisions into the frontend.

### Rule 5 — naming must remain revisable
The implementation must support future naming revision by editing the governed IDL authority, not by rebuilding the interpretation engine.

---

## Required preflight investigation

Before implementing, verify and cite:

1. the current authoritative source for the existing interpretation entities
2. the current runtime loader / publisher path that emits the analysis result
3. the typed DTO / contract file that must be extended
4. whether any duplicate or parallel naming authority already exists
5. the current source of cluster / system / interpretation naming used by the results surface
6. the exact current path that FE would otherwise use for Section 5-adjacent data

If authority is ambiguous, stop and report before modifying files.

---

## Required implementation approach

Use the smallest clean architecture that produces a governed IDL.

Expected shape:

1. versioned typed IDL model
2. governed source of IDL records for the current interpretation set
3. deterministic mapping / publication step from internal interpretation entities to IDL records
4. DTO / API exposure of the IDL bundle
5. tests and validation for governance rules

Do not use frontend fallbacks as a substitute for missing backend governance.

---

## Initial content / governance posture

Implement the IDL in line with the already-approved product direction:

- phenotype remains a strategic company/methodology term
- the retail naming layer is medically stricter
- the current interpretation set is mixed
- naming remains revisable later through the IDL

Do not reinterpret this sprint as permission to reopen the phenotype strategy debate.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. there is no single authoritative source for the existing interpretation entities
2. implementing the IDL would require broad uncontrolled changes across intelligence-core reasoning rather than a bounded publication-layer addition
3. the proposed implementation would create duplicate naming/classification authorities
4. classification or naming would end up embedded in frontend code
5. completing the sprint would require inventing new interpretation entities
6. touched-file scope expands into broader behavioural logic unrelated to deterministic IDL publication
7. the only feasible approach appears to hardcode labels directly into DTO assembly without a governed source layer
8. the repo reality contradicts the assumption that the current 9 interpretation entities already exist in a stable enough form to map

If blocked, produce the exact blocker, affected files, and the smallest safe remediation path.

---

## Success criteria

This sprint is successful only if:

1. a typed versioned IDL contract exists
2. the current 9 interpretation records exist in governed form
3. the analysis result exposes the IDL bundle
4. the bundle is sufficient for a later FE Section 5 renderer to consume without inventing taxonomy
5. naming and classification are externalised and changeable later
6. governance tests pass
7. no Section 5 frontend implementation is attempted in this sprint

---

## Deliverables

At finish, the sprint should leave behind:

- versioned IDL model(s)
- governed record authority for the current 9 entities
- deterministic publisher / mapper path
- DTO / API exposure
- tests / validations
- brief implementation notes in the audit summary explaining where the authority now lives

---

## Evidence requirements

You must show, with file citations and repo evidence:

- where the interpretation entities live today
- where the new IDL authority lives after implementation
- where the analysis result is extended
- where the deterministic publication step occurs
- where validation tests enforce the rules

Do not claim the architecture is governed unless the authority paths are explicit and singular.

---

## After this sprint

If BE-IDL-1 passes, the next sprint becomes a thin frontend surfacing sprint:

**FE-R8 — Section 5 rendering against the approved IDL**

That later sprint should render the approved IDL only.
It must not reopen classification, taxonomy, or naming strategy.

---
