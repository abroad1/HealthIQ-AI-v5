---
work_id: F-1
branch: feature/f-1-frontend-reentry-narrative-surfacing
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# F-1 — Frontend re-entry: deterministic narrative surfacing

## Objective

Re-enter the frontend in a bounded, controlled way by surfacing the new deterministic `narrative_report_v1` output in the results journey.

This is a frontend integration sprint.
It is not a backend architecture sprint.
It is not a new narrative-asset sprint.
Do not invent narrative logic in the frontend.
Do not introduce Gemini or any other LLM dependency.
Do not widen into a broad redesign of the whole application.

The purpose of F-1 is to replace weak or placeholder narrative areas in the results journey with the deterministic narrative outputs that now exist in the backend.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The deterministic narrative support stack has now been built through N-3 to N-9B.
- The backend runtime is now considered strong enough for controlled frontend re-entry.
- The frontend must consume deterministic compiled outputs, not recreate narrative logic locally.
- F-1 is a bounded surfacing sprint, not a new product strategy sprint.

Your job is to integrate the deterministic narrative output into the frontend results journey in a clean, user-readable, architecturally disciplined way.

---

## Required inputs

Treat the following as required inputs:

1. Backend runtime output path and contracts
- `backend/core/contracts/narrative_report_v1.py`
- `backend/core/models/results.py`
- any API/DTO path exposing `narrative_report_v1`

2. Current results frontend implementation
- results page components and their data path from the API
- any current sections using older placeholder or weaker narrative content

3. Validation authority
- `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`

4. Current sprint-note and architecture authority where useful
- `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

---

## Core problem this sprint must solve

The backend now produces a deterministic narrative layer, but the frontend results journey was built before that layer existed and still contains weaker, thinner, or placeholder narrative surfaces.

This sprint must surface the deterministic narrative output cleanly so the user journey starts to feel like one coherent investigation rather than a stitched stack of older sections.

---

## Required outcome

Deliver a bounded frontend integration that:

1. reads and uses `narrative_report_v1`
2. surfaces the benchmark-priority compiled narrative sections in the results journey
3. removes or de-emphasises weaker placeholder narrative where the deterministic replacement now exists
4. preserves authority separation by keeping narrative generation in the backend
5. leaves the frontend in a strong state for focused UAT

---

## Required frontend scope

At minimum, integrate and surface these compiled sections where appropriate:

### 1. Retail summary
Use the compiled `retail_summary` as the primary patient-facing summary layer near the top of the results experience.

### 2. Body overview
Use the compiled `body_overview` instead of weak placeholder or generic framing where appropriate.

### 3. Lead narrative
Surface the compiled `lead_narrative` as the main deep explanation of the primary issue.

### 4. Secondary narrative
Surface the compiled `secondary_narratives` in a bounded secondary position, clearly subordinate to the lead.

### 5. Longitudinal narrative
Surface the compiled `longitudinal_narrative` where trend and prior/current comparison belong.

### 6. Next steps
Surface the compiled `next_steps_narrative` as the action-oriented follow-up block.

### 7. Clinician synthesis
Make the compiled `clinician_synthesis` available in the appropriate advanced / clinician-facing area.

---

## In scope

### 1. Frontend data integration
Verify that the frontend receives `narrative_report_v1` cleanly from the existing backend/API result path.

If small frontend-side typing or DTO updates are required to consume the field safely, make them in a bounded way.

### 2. Results-page narrative replacement / surfacing
Replace or de-emphasise older weaker narrative areas where the deterministic narrative output now provides a better source.

Be disciplined:
- frontend should display
- backend should interpret

### 3. Section ordering and hierarchy
Use the deterministic sections to create a cleaner story order on the page.

At minimum, ensure the user can experience:
- top-level summary
- broad body overview
- lead issue
- secondary issue
- trend / direction of travel
- next steps

without having to piece the story together from unrelated blocks.

### 4. Progressive disclosure
Keep more technical or dense layers appropriately placed.
The frontend should not overwhelm the user with everything at once.

### 5. Styling and presentation cleanup
Light presentation improvements are allowed where necessary to make the new narrative readable and coherent.

Do not widen into a full visual redesign.

### 6. UAT-readiness
Leave the page in a state that can be tested meaningfully against the narrative ambition.

---

## Out of scope

The following are explicitly out of scope:

- new backend narrative generation logic
- new governed content assets
- broad new frontend redesign unrelated to narrative surfacing
- changing benchmark narrative authority
- Gemini / LLM work
- broad product copy rewrite outside the compiled sections

---

## Design rules

### Rule 1 — no frontend-authored narrative logic
Do not recreate or paraphrase backend narrative logic in the frontend unless there is a tiny display-only necessity.

### Rule 2 — backend remains the authority
`narrative_report_v1` is the source of truth for these new sections.

### Rule 3 — bounded replacement, not total redesign
Improve the journey where the deterministic output now exists.
Do not widen into unrelated layout redesign.

### Rule 4 — hierarchy matters
The user should encounter a coherent story, not a long undifferentiated stack.

### Rule 5 — preserve advanced access
Clinician-style and more technical content should remain accessible without cluttering the top-level patient journey.

### Rule 6 — HIGH-risk discipline
If any backend-touching integration issue arises, keep it minimal and justified.

---

## Expected implementation shape

The expected shape is:

1. inspect how `narrative_report_v1` currently reaches or does not reach the frontend
2. update frontend typing/data flow if needed
3. surface the compiled sections in the results journey
4. remove or de-emphasise weaker overlapping narrative blocks
5. leave the page ready for UAT

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. `narrative_report_v1` is not actually available on the frontend result path
2. frontend consumption would require a much wider backend DTO/API change than expected
3. the current results page architecture makes bounded narrative surfacing impossible without a broader redesign
4. substantial missing backend output is discovered during integration
5. touched-file scope expands materially beyond bounded frontend integration

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. the frontend now consumes `narrative_report_v1`
2. the main deterministic narrative sections are surfaced in the results journey
3. weaker placeholder narrative is reduced or replaced where appropriate
4. the page tells a clearer, more coherent story
5. the sprint remains bounded and does not become a broad redesign
6. the results page is ready for focused UAT

---

## Deliverables

At finish, the sprint should leave behind:

- bounded frontend integration changes
- any required type/data-flow updates
- a short sprint note explaining:
  - what sections are now surfaced
  - what old sections were reduced/replaced
  - what UAT should focus on next

Report back with:
- files touched
- how `narrative_report_v1` is now surfaced
- what still remains weak in the journey
- whether the page is ready for UAT

---

## Evidence requirements

You must show, with exact file paths and grounded runtime evidence:

- where `narrative_report_v1` is consumed
- what frontend sections now use it
- what weaker narrative surfaces were replaced or reduced
- how the page hierarchy improved

Do not claim success merely because the field is displayed somewhere.
Show that the results journey now makes meaningful use of the deterministic narrative output.