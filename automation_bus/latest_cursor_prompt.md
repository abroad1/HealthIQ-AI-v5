---
work_id: FE-R8A
branch: feature/fe-r8a-results-dto-repair
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R8A — Results DTO mapping repair and Section 5/Stable-layer recovery

## Objective

Repair the frontend analysis-result mapping so the live results page consumes the full backend analysis payload already emitted by the server, then verify whether the missing governed interpretation layer and stable-system layer now appear correctly in the journey.

This is a bounded frontend/data-consumption sprint.

It exists to fix a surfacing gap between the backend DTO and the frontend store/render path.

It is not a redesign sprint.
It is not a new narrative sprint.
It must not reopen naming, taxonomy, or Gemini strategy.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- BE-IDL-1 is complete and approved.
- FE-R8 is complete and approved as the thin Section 5 rendering sprint.
- The current live journey feels dull and underpowered in part because richer backend assets are not being surfaced fully in the frontend.
- The strongest immediate hypothesis is that the frontend mapping layer is dropping fields the backend already returns, especially:
  - `balanced_systems_v1`
  - `interpretation_display_layer_v1`
  - `risk_assessment`
- The immediate goal is to restore the intended DTO-to-UI flow before making broader product judgments about narrative quality or Gemini.

Your job is to confirm that repo reality, repair it cleanly, and prove whether the missing layers now appear.

---

## Required outcome

Deliver a bounded fix that:

1. repairs the frontend result-mapping layer so it consumes the backend analysis payload fields already emitted by the API
2. ensures the frontend store and typed result shape preserve those fields end to end
3. restores missing governed sections where the backend has already supplied valid data
4. proves, with browser/repo evidence, whether:
   - `balanced_systems_v1` now populates “What’s working well”
   - `interpretation_display_layer_v1` now renders Section 5
   - `risk_assessment` is now available to the existing frontend surfaces that expect it
5. leaves the wider results journey structurally unchanged unless a minimal wiring correction is strictly required

---

## Primary hypothesis to test

The backend DTO already contains richer payload fields, but the frontend analysis service is constructing a narrowed object and omitting fields that already exist in the backend response contract.

The sprint must verify this hypothesis from source and fix it if true.

---

## Authority and preflight checks

Before modifying files, verify and cite:

1. the backend DTO builder that emits the analysis result payload
2. the frontend analysis service path that fetches and maps the result
3. the frontend type definitions for `AnalysisResult`
4. the frontend store shape receiving the mapped result
5. the component(s) consuming:
   - `balanced_systems_v1`
   - `interpretation_display_layer_v1`
   - `risk_assessment` or equivalent advanced/overview fields
6. whether the current bug is caused by:
   - dropped mapping fields
   - inconsistent typing
   - store omission
   - conditional rendering logic
   - or a combination

If the backend is not actually emitting the expected fields for this analysis result, stop and report that explicitly before widening scope.

---

## In scope

### 1. Repair frontend result mapping
Fix the frontend path so that backend-emitted fields are preserved instead of silently dropped.

At minimum, investigate and repair handling for:

- `balanced_systems_v1`
- `interpretation_display_layer_v1`
- `risk_assessment`

Also preserve any other already-emitted fields that are required by the current results journey and are being lost by the narrowed mapping shape.

### 2. Align types and store shape
Ensure `frontend/app/types/analysis.ts`, any analysis service mapping layer, and store/state shape remain consistent with the consumed backend payload.

### 3. Verify governed sections now populate
Once mapping is repaired, verify whether existing components now render richer content without further redesign.

Specifically:
- “What’s working well”
- Section 5 / Interpretation Patterns
- any existing advanced/overview surface expecting `risk_assessment`

### 4. Add bounded tests
Add tests covering the repaired mapping path.

At minimum, include fixture-backed proof that:
- IDL survives the API mapping into the store/result object
- balanced systems survive the API mapping into the store/result object
- omitted/narrowed mapping regression is prevented

### 5. Browser verification
After implementation, verify the live page for the provided analysis result and confirm whether the missing layers now appear.

---

## Out of scope

The following are explicitly out of scope:

- changing BE-IDL-1 content or registry values
- changing naming/classification
- redesigning the results journey
- rewriting hero/body-overview copy
- Gemini integration
- backend analytical logic changes
- new interpretation entities
- broad Advanced analysis redesign
- speculative “wow” enhancements not required to confirm the repaired data flow

---

## Implementation rules

### Rule 1 — consume existing authority, do not invent new data
This sprint must consume the backend DTO more faithfully.
It must not fabricate replacement frontend content.

### Rule 2 — smallest clean fix
Use the smallest clean architecture that preserves the backend payload shape safely in the frontend.

If spreading the backend result is safer and cleaner than hand-picking fields, prefer the cleaner durable option, provided typing remains explicit and safe.

### Rule 3 — no duplicate mapping authority
Do not leave one narrowed mapping path in place while adding a second richer path elsewhere.

### Rule 4 — preserve reversibility and clarity
The repaired mapping should make future result fields easier to preserve, not harder.

### Rule 5 — do not widen into a composition sprint
If the repaired fields surface correctly and the page still feels flat, report that separately.
Do not silently convert this sprint into a copy/design overhaul.

---

## Expected implementation shape

The expected shape is:

1. inspect backend result payload contract
2. inspect frontend mapping narrowing point
3. repair the narrowing/omission bug
4. align types/store
5. add regression tests
6. validate in browser against the live page

This should remain a bounded frontend/data-flow repair sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the backend does not actually emit the expected fields for the tested analysis result
2. the missing sections are caused primarily by backend null data rather than frontend omission
3. fixing the issue would require backend contract redesign rather than frontend mapping repair
4. the existing frontend state architecture makes a bounded repair impossible without a much wider refactor
5. the issue is not a mapping omission but a deeper rendering/logic bug requiring a separate sprint
6. repo reality contradicts the hypothesis that FE-R8A is primarily a DTO-consumption repair sprint

If blocked, report the exact blocker, affected files, and the smallest safe remediation path.

---

## Success criteria

This sprint is successful only if:

1. the frontend preserves the required backend payload fields instead of dropping them
2. `balanced_systems_v1` reaches the component(s) that need it
3. `interpretation_display_layer_v1` reaches the component(s) that need it
4. `risk_assessment` reaches any existing consumer surface that expects it
5. regression tests prove the repaired mapping path
6. browser verification confirms whether the missing layers now appear on the live page
7. the sprint stays bounded to data-consumption repair, not broad redesign

---

## Deliverables

At finish, the sprint should leave behind:

- repaired frontend mapping/service path
- aligned type/store handling
- regression tests for preserved payload fields
- browser-verified confirmation of what now appears on the page
- audit-ready notes stating whether the wow-gap is still primarily a composition/copy problem after mapping repair

---

## Evidence requirements

You must show, with file citations and repo/browser evidence:

- where the backend emits the relevant fields
- where the frontend was dropping them
- where the mapping was repaired
- where tests lock the fix
- what changed in the live page after the fix

Do not claim the issue is solved unless the browser confirms the missing layers now appear when backed by real data.

---

## After this sprint

After FE-R8A, report one of these outcomes clearly:

1. **Mapping repair solved the missing-layer problem**  
   The journey can now be reassessed for experiential quality with the intended assets actually present.

2. **Mapping repair was necessary but not sufficient**  
   The missing layers now appear, but the page still lacks wow due to composition/copy/experience quality.  
   In that case, the next sprint should be a bounded journey-refinement sprint, not Gemini by default.

3. **Backend data was absent/null for this run**  
   The problem was misdiagnosed as frontend omission and needs a different corrective sprint.