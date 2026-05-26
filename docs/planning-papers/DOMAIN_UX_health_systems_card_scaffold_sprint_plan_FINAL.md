# HealthIQ AI — Health Systems Card Scaffold Sprint Plan

**Document purpose:** Architecture proposal for team review  
**Status:** Revised proposed sprint plan after CC and frontend specialist feedback  
**Prepared by:** GPT Head of Architecture  
**Recommended repo path:** `docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan.md`

---

## 1. Executive summary

HealthIQ AI should not treat the Health Systems Card as a quick frontend exposure of existing hidden content.

The strategic aim is to build the architectural scaffold for a reusable customer-facing health-system presentation layer. This layer should translate the deterministic engine into a clear, visual, evidence-transparent experience that users can understand and trust.

The Health Systems Card should show that HealthIQ scores are:

- evidence-built, not opinion-generated
- based on multiple biomarkers and system-level patterns
- constrained by what the user actually uploaded
- transparent about missing markers
- visually understandable without relying on long prose

The first implementation should focus on the three repo-ready Wave 1 domains:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

The remaining launch-core domains should be added only after backend/governed support is ready:

4. Blood, iron & oxygen
5. Thyroid & energy regulation
6. Kidney function

---

## 2. Strategic principle

We are not racing to put a partial card in front of live users.

There are no live users yet. The current priority is to build the correct architectural scaffold.

A partial implementation is valuable only if it forms part of the intended final Health Systems Card model. It should not create a stopgap UI that later has to be unwound.

The guiding principle is:

> Build the full Health Systems Card scaffold properly, then populate it progressively with the domains and evidence structures the backend can safely support.

---

## 3. Evidence base

This sprint plan is based on:

- `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md`
- `docs/architecture/User Health to Systems Map_FINAL.md`
- `docs/audit-papers/DOMAIN-R1_launch_core_health_domain_readiness_audit.md`
- `docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md`
- recent post-MAP-R1A UAT findings showing that the current report is clinically coherent but not yet a world-class user experience

Claude’s DOMAIN-UX1 audit found that:

- Wave 1 domain outputs already exist for Cardiovascular health, Blood sugar control and Liver health
- existing domain cards are hidden too low in the page
- evidence completeness numerator/denominator are not currently emitted
- supporting subsystem structures are not currently available as governed DTO output
- subsystem labels and marker groupings must not be invented in the frontend
- the richer expanded reveal requires backend-governed subsystem evidence before it can be implemented safely

---

## 4. Target end-state

The intended Health Systems Card should eventually support:

### Collapsed state

- health-system name
- plain-English descriptor
- score visual
- score band
- score reliability
- evidence completeness
- short health-system read
- supporting biological system preview
- expand action

### Expanded state

- what this score means
- why the score looks this way
- supporting biological systems / subsystems
- uploaded and scored biomarkers
- missing relevant biomarkers
- biomarker values, units, ranges and status
- reliability explanation
- what this may mean over time
- what to do next

### Evidence-transparency rule

The user should be able to see:

- what HealthIQ used
- what HealthIQ could not use
- which markers shaped the score
- which missing markers would improve completeness

This is central to trust.

---

## 5. Design and governance constraints

The frontend may:

- render governed backend output
- arrange fields visually
- apply layout and progressive disclosure
- reuse compact biomarker card components
- display missing-marker states if supplied by backend

The frontend must not calculate:

- domain score
- score band
- score reliability
- evidence completeness
- expected marker sets
- missing relevant markers
- subsystem interpretation
- consequence wording
- marker-to-subsystem groupings

Consumer labels must remain separate from clinician-facing labels.

No consumer-facing Health Systems Card implementation should leak internal phenotype, signal, cluster or clinical-handout labels into the retail UI.

---

## 6. Revised sprint sequence

The initial plan separated contract hardening and frontend surfacing into two sprints. After review, that separation is unnecessary because the existing `Wave1DomainCards` component is already connected to backend output and hidden mainly by page placement/disclosure state.

The revised sequence combines the initial surfacing and contract-hardening work into `DOMAIN-UX1A`.

---

# Sprint 1 — DOMAIN-UX1A  
## Wave 1 Health Systems Card scaffold + contract hardening

### Intended outcome

Create the first visible Wave 1 Health Systems Card scaffold while hardening the backend/frontend contract needed to support the agreed design.

This sprint should not be treated as a quick exposure of a hidden component. It should establish the first working slice of the intended Health Systems Card architecture.

### Scope

- Surface the existing Wave 1 domain cards in the main results journey.
- Reposition them so they are no longer buried behind a closed disclosure section.
- Add or confirm plain-English descriptor for each Wave 1 domain.
- Extend the Wave 1 domain DTO with evidence completeness numerator and denominator.
- Confirm score, band, reliability, short read, consequence and next-step fields.
- Remap confidence wording into score reliability vocabulary.
- Align band wording with the agreed UX language.
- Add a prose quality gate for `headline_sentence`, `contributor_sentence` and other newly prominent card text.
- Ensure frontend TypeScript types match backend output.
- Clarify that any forward-compatible subsystem placeholder means nullable/non-rendered DTO structure only, not a visible “coming soon” or placeholder UI section.
- Add regression tests proving backend-emitted fields round-trip correctly and frontend renders supplied values without deriving governed logic.

### In scope domains

- Cardiovascular health
- Blood sugar control
- Liver health

### Explicitly out of scope

- visible subsystem chips unless backend-governed subsystem data already exists
- per-subsystem biomarker grouping
- greyed-out biomarker cards
- domain score dial/gauge
- Wave 2 domains
- frontend-invented marker groupings
- visible placeholder subsystem UI

### Risk classification

**STANDARD / MIXED**, provided the sprint only adds DTO fields derived from existing deterministic domain rail state and does not alter scoring or emitted reasoning.

### Risk escalation caveat

Escalate to **HIGH** if the sprint changes:

- expected marker sets
- missing-marker logic
- score logic
- reliability/confidence rules
- domain scoring behaviour
- any Intelligence Core output construction beyond adding explicit DTO fields for existing values

### Success criteria

- Wave 1 Health Systems Cards are visible in the main results journey.
- Backend emits evidence completeness numerator and denominator.
- Frontend renders evidence completeness using backend-supplied values.
- Frontend does not calculate score, reliability, evidence completeness or missing markers.
- Plain-English descriptors appear for the three Wave 1 domains.
- `clinical_label` is not displayed in the consumer-facing card.
- Newly prominent card copy passes a prose quality check and does not introduce mechanical “on this panel” style repetition into the first-screen experience.
- No visible subsystem placeholder UI is rendered.

---

# Sprint 2 — DOMAIN-UX1B  
## Premium score visual, refined card layout and biomarker evidence visual model

### Intended outcome

Move the first visible card implementation closer to the agreed visual design by adding the premium score visual and reusable biomarker evidence language.

This sprint should make the Health Systems Card feel less like a text block and more like a premium, visual, evidence-built system read.

### Scope

- Add a premium domain score visual: dial, gauge, radial score or equivalent score device.
- Refine collapsed-card layout for desktop and mobile.
- Create compact canonical biomarker card variant.
- Support uploaded/scored marker state.
- Support greyed-out “Not uploaded” marker state.
- Preserve value, unit, range and status visual logic.
- Ensure the same biomarker visual language is used across the product.
- Add missing-marker explanation copy.
- Keep the card prose-light.

### Explicitly out of scope

- subsystem grouping unless backend supplies the structure
- subsystem scores/statuses
- backend marker-to-subsystem logic
- Wave 2 domain assembly
- frontend-invented biological groupings

### Risk classification

**LOW to STANDARD**

Reason: primarily frontend component and layout work, with no analytical logic. Escalate only if DTO or backend contract changes become necessary.

### Success criteria

- Domain card has a premium score visual, not just a large text number.
- A compact biomarker evidence component exists.
- Uploaded/scored markers can be shown visually.
- Missing markers can be shown in a clear greyed-out state.
- Existing biomarker visual semantics are preserved.
- The component is reusable inside future health-system/domain cards.
- The card visually previews the final intended scaffold without rendering unsupported subsystem claims.

---

# Sprint 3 — DOMAIN-UX1C  
## Governed subsystem evidence model

### Intended outcome

Build the backend-governed structure required for the full expanded Health Systems Card reveal.

This is the sprint that enables the card to show what makes up the headline health-system score.

### Scope

- Define subsystem model for Wave 1 domains.
- Add subsystem ID and label.
- Add included marker IDs.
- Add missing marker IDs.
- Add subsystem status only if safely supported.
- Emit subsystem evidence in DTO.
- Add tests preventing frontend-invented subsystem labels or marker groupings.

### Example target structure

Cardiovascular health may eventually include:

- Lipid transport
- Vascular strain
- Homocysteine pathway

Blood sugar control may eventually include:

- Glycaemic regulation
- Insulin/metabolic context
- Lipid-metabolic coupling, if supported

Liver health may eventually include:

- Hepatic strain
- Liver processing/load context
- Metabolic-liver context, if supported

### Explicitly out of scope

- fake subsystem scores
- decorative subsystem labels unsupported by backend logic
- frontend-hardcoded subsystem groupings
- unsupported biological labels
- Wave 2 domains

### Risk classification

**HIGH**

Reason: this creates new governed backend interpretation structure and could affect emitted reasoning. It must not create fake scoring or unsupported subsystem claims.

### Non-negotiable rule

No subsystem status, subsystem score or marker-to-subsystem grouping may be emitted unless it is backend-governed and test-covered.

### Success criteria

- Subsystems are backend-governed.
- Marker-to-subsystem groupings are backend-supplied.
- Missing markers can be shown per subsystem.
- Frontend does not decide biological grouping.
- Output is deterministic and test-covered.
- Consumer labels, clinical labels and internal engine labels remain separate.

---

# Sprint 4 — DOMAIN-UX1D  
## Full Wave 1 expanded Health Systems Card

### Intended outcome

Complete the intended Wave 1 Health Systems Card experience.

This sprint should bring together the contract, frontend scaffold, biomarker evidence visual model and governed subsystem structure into the full expanded card experience.

### Scope

- Render subsystem sections.
- Show uploaded/scored biomarker mini-cards under each subsystem.
- Show missing markers under each subsystem.
- Show score reliability explanation.
- Show evidence completeness explanation.
- Show concise “what this may mean” and “what to do next”.
- Validate against fresh UAT.

### Explicitly out of scope

- Wave 2 domains
- new medical content authoring
- new scoring rails unless separately authorised
- clinician report redesign

### Risk classification

**STANDARD / MIXED**

Reason: frontend plus governed DTO consumption. Risk depends on Sprint 3 output.

### Success criteria

- Full Health Systems Card design works for Wave 1.
- User can see the system score and evidence chain.
- Subsystems and biomarker evidence are visually understandable.
- Missing markers are visible and trust-building.
- The card feels premium, calm and evidence-transparent.
- Fresh UAT confirms a material improvement in user comprehension and perceived product quality.

---

# Sprint 5 — DOMAIN-UX2A  
## Wave 2 readiness and design audit: Blood, iron & oxygen

### Intended outcome

Assess and design the safest route for extending the Health Systems Card scaffold to Blood, iron & oxygen.

This should be a readiness/design sprint before implementation unless backend evidence is already strong enough to justify direct assembly.

### Scope

- Assess current support for Blood, iron & oxygen.
- Resolve whether CBC, iron, B12, folate and related markers can be safely combined.
- Define likely confidence and evidence completeness logic.
- Identify existing governed IDL/Knowledge Bus assets.
- Identify required backend assembly.
- Determine whether implementation is ready or whether further governed content/scoring work is needed.
- Prevent the domain from becoming an unsupported catch-all.

### Risk classification

**STANDARD for audit/design only**  
**HIGH if implementation changes backend scoring, SSOT, Knowledge Bus, IDL or emitted reasoning**

### Success criteria

- Clear readiness verdict.
- Proposed DTO/domain assembly route if safe.
- STOP conditions for implementation.
- No premature domain score emitted.

---

# Sprint 6 — DOMAIN-UX2B  
## Wave 2 readiness and design audit: Thyroid and Kidney

### Intended outcome

Assess and design the safest route for extending the Health Systems Card scaffold to Thyroid & energy regulation and Kidney function.

This should be a readiness/design sprint first, not a direct implementation sprint, unless prior evidence proves the backend is ready.

### Scope

- Assess current thyroid domain support.
- Assess current kidney domain support.
- Identify scoring-policy or SSOT dependencies.
- Define likely confidence and evidence completeness logic.
- Identify mild-abnormality handling requirements.
- Identify whether eGFR, age/sex context or other governed inputs are required.
- Determine whether implementation is ready or further governed backend work is needed.

### Risk classification

**STANDARD for audit/design only**  
**HIGH if implementation changes backend scoring, SSOT, Knowledge Bus, IDL or emitted reasoning**

### Success criteria

- Thyroid and Kidney readiness verdicts.
- Clear implementation prerequisites.
- No fake score is proposed where evidence is insufficient.
- Mild abnormality handling is treated as a clinical safety concern.
- The route to six launch-core domains is clarified.

---

## 7. Recommended immediate next step

The next sprint should be:

> DOMAIN-UX1A — Wave 1 Health Systems Card scaffold + contract hardening

This sprint should not be framed as a quick frontend exposure exercise.

It should be framed as the first step in building the full Health Systems Card architecture.

The immediate goal is to surface the first supported Wave 1 slice while hardening the contract for evidence completeness and ensuring the frontend has the correct governed fields before richer card presentation is built.

---

## 8. Team message

The recommended message to the team is:

> We are not trying to quickly expose a partial card. We are building the Health Systems Card scaffold properly.
>
> The first phase should surface the three domains already supported by the repo while hardening the DTO and frontend contract. The second phase should add the premium score visual and biomarker evidence visual model. The third phase should add governed subsystem evidence, because subsystem labels and marker groupings must come from backend output, not frontend invention.
>
> Once the full card works for Cardiovascular health, Blood sugar control and Liver health, we can use readiness/design sprints to define how Blood, iron & oxygen, Thyroid & energy regulation and Kidney function should be safely added.

---

## 9. Key risks to manage

### Risk 1 — Stopgap UI

Do not expose a partial card in a way that becomes permanent technical debt.

### Risk 2 — Frontend invention

Do not allow frontend to calculate or infer evidence completeness, subsystem labels, missing markers or biological grouping.

### Risk 3 — Fake precision

Do not show subsystem scores or confidence levels unless backend-governed logic supports them.

### Risk 4 — Naming layer contamination

Consumer labels must not leak into clinician outputs. Clinical labels must not dominate the retail UI.

### Risk 5 — Over-broad Wave 2 domains

Blood/iron, thyroid and kidney support must be built carefully and not rushed into the card before deterministic support exists.

### Risk 6 — Underwhelming first implementation

The first visible card must not feel like just another score plus sentence. It should visually preview the intended scaffold, even if the full subsystem evidence model is not yet populated.

### Risk 7 — Prose quality regression

Surfacing the cards makes their prose more prominent. Mechanical or repetitive text should not be promoted into a first-screen position without review.

---

## 10. Working conclusion

The Health Systems Card remains one of the strongest routes to expressing HealthIQ’s USP.

It can show that the product is not a biomarker table, not a generic AI summary, and not a traffic-light report.

It can show a user:

- where their body looks strong
- where it may be under strain
- what evidence was used
- what evidence was missing
- why the score is reliable or limited
- how multiple biomarkers combine into a system-level read

The right next step is not more abstract design work.

The right next step is to build the scaffold deliberately, beginning with `DOMAIN-UX1A`: a combined Wave 1 surface and contract-hardening sprint.
