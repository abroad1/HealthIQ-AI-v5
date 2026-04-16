---
work_id: FE-R8
branch: feature/fe-r8-section-5-idl-render
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R8 — Section 5 rendering against approved IDL

## Objective

Implement Section 5, “Patterns across your body”, as a thin frontend surfacing sprint that renders the approved Interpretation Display Layer (IDL) from the analysis result payload.

This sprint is not a design sprint.
This sprint is not a taxonomy sprint.
This sprint must not reopen naming, classification, or phenotype strategy.

The IDL now exists and is the sole authority for this section.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The Interpretation Display Layer (IDL) is the sole authority for Section 5.
- The current retail naming posture is approved.
- The current interpretation layer uses the medically stricter mixed classification model.
- Naming and classification remain governed through the IDL, not through frontend logic.
- FE-R8 is a thin rendering sprint only.

Your job is to render the approved IDL cleanly, accurately, and without inventing product logic in the UI.

---

## Required outcome

Deliver a frontend Section 5 implementation that:

1. reads the typed `interpretation_display_layer_v1` payload from the analysis result
2. renders approved pattern cards using only IDL-approved fields
3. respects all IDL rendering and omission rules
4. omits the section cleanly when no frontend-enabled records exist
5. does not invent labels, classification, or explanatory text in frontend code
6. fits correctly into the approved results journey structure

---

## Authority and preflight checks

Before implementing, verify and cite:

1. the current frontend results-page entry point and Section 5 insertion point
2. the typed frontend path consuming the analysis result DTO
3. the exact payload shape now exposing `interpretation_display_layer_v1`
4. any existing component currently acting as the Section 5 placeholder / bridge
5. whether any duplicate or conflicting Section 5 logic already exists in frontend code
6. whether any existing frontend naming fallback would conflict with the new IDL authority

If there is ambiguity around where Section 5 should be inserted, resolve it by following the approved results journey authority and current repo reality before modifying components.

---

## In scope

### 1. Render Section 5 from IDL only
Implement Section 5 so that it renders from `interpretation_display_layer_v1` and not from raw clusters, raw system outputs, or any ad hoc frontend mapping.

### 2. Card rendering
Each pattern card must render only approved IDL fields.

At minimum, render:

- `retail_display_label`
- `subtitle`
- `severity_state`
- `supporting_biomarkers_summary`
- `why_it_matters`

Optionally render, only when present:

- `supporting_systems_summary`
- `user_safe_description`
- `display_caveat`

### 3. Section render gate
Render Section 5 only if at least one IDL record is both present and enabled for frontend display.

If no such records exist, omit the section cleanly with no broken layout and no empty placeholder.

### 4. Card ordering
Use the ordering provided by the approved payload / IDL fields.
Do not invent frontend ranking logic.

If the payload contains more than the approved default visible count, follow the governing display order and implement the approved truncation / expansion behaviour only if repo reality and existing design structure support it cleanly.
If not, preserve deterministic ordered rendering and report any gap.

### 5. Integrate into the results journey
Insert Section 5 into the correct position in the results journey, between the already-approved surrounding sections, without destabilising the rest of the page.

### 6. Frontend tests / validation
Add bounded frontend coverage for:
- section presence when IDL exists
- section omission when IDL absent or empty
- correct rendering of required fields
- absence of forbidden/internal fields
- stable ordered rendering from payload data

---

## Out of scope

The following are explicitly out of scope:

- changing IDL content
- changing IDL classification
- changing retail labels
- changing `frontend_allowed_term`
- changing backend DTO/API structure
- changing Layer B reasoning
- creating new interpretation entities
- deriving new explanatory text in frontend code
- introducing Gemini or LLM behaviour
- redesigning the wider results journey beyond the bounded insertion needed for Section 5

---

## Rendering rules

### Rule 1 — frontend is renderer only
Frontend must render approved IDL content.
It must not infer taxonomy.

### Rule 2 — no label invention
Frontend must not:
- generate alternative names
- substitute generic buckets such as “Metabolic Health”
- infer that something is a phenotype
- rewrite retail labels

### Rule 3 — no internal or forbidden fields
Frontend must not show:
- `internal_id`
- raw `scientific_class`
- raw engine confidence numbers
- raw biomarker values/ranges inside Section 5 cards
- diagnostic claims
- lifestyle prescriptions

### Rule 4 — no phenotype inference
Frontend may only show the word “phenotype” where it already appears in the approved IDL retail label.
No additional frontend logic may introduce that term.

### Rule 5 — no duplicate authority
If an older placeholder component or naming fallback exists, remove or bypass it rather than allowing parallel Section 5 authority paths.

---

## Expected implementation shape

Use the thinnest clean frontend implementation that:

1. consumes the typed IDL bundle
2. maps records directly to a Section 5 component
3. renders a pattern-card component from approved fields
4. omits the section cleanly when no records qualify
5. leaves naming/classification authority entirely in backend/content

The UI should feel production-quality, but this sprint must stay a rendering sprint, not become a new interpretation-design sprint.

---

## UX expectations

The section should feel:

- structured
- readable
- medically credible
- calm
- clearly part of the guided reasoning journey

It should not feel:

- like a generic dashboard bucket layer
- like a debug surface
- like a biomarker table in disguise
- like a new design experiment disconnected from the rest of the page

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the frontend cannot access a stable `interpretation_display_layer_v1` payload path
2. implementing Section 5 would require frontend code to invent names, classifications, or text
3. there is an existing parallel Section 5 authority path that cannot be cleanly removed or bypassed
4. the repo reality contradicts the assumption that FE-R8 is a thin rendering sprint
5. the implementation would require backend contract changes rather than frontend rendering work
6. the surrounding results-page structure is materially different from the assumed insertion model and would require a wider redesign sprint
7. frontend typing for the analysis result is missing or inconsistent enough that safe rendering cannot proceed without widening scope

If blocked, report the exact blocker, affected files, and the smallest safe remediation path.

---

## Success criteria

This sprint is successful only if:

1. Section 5 renders from `interpretation_display_layer_v1`
2. the section uses only approved IDL display fields
3. no naming or classification logic is invented in frontend code
4. the section omits cleanly when no frontend-enabled records are present
5. forbidden/internal fields are not shown
6. rendering order is deterministic and payload-driven
7. the implementation fits the approved results journey without destabilising other sections

---

## Deliverables

At finish, the sprint should leave behind:

- Section 5 frontend component(s)
- payload-to-component wiring from the typed analysis result
- bounded tests or UI validation coverage
- removal or bypass of any conflicting placeholder/fallback authority
- audit-ready clarity on where Section 5 now renders from

---

## Evidence requirements

You must show, with file citations and repo evidence:

- where `interpretation_display_layer_v1` enters the frontend
- where Section 5 is inserted in the results page
- where the card component renders approved IDL fields
- where omission logic is handled
- where tests/validation prove the section behaves correctly

Do not claim Section 5 is governed unless the frontend is demonstrably reading only from the IDL.

---

## After this sprint

After FE-R8, Section 5 should be live as a governed frontend surface.

Any future change to naming, classification, or phenotype usage must be handled through the IDL authority layer, not by reopening frontend logic.