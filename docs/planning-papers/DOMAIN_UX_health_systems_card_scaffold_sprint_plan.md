# HealthIQ AI — Health Systems Card Scaffold Sprint Plan

**Document purpose:** Architecture proposal for team review  
**Status:** Proposed sprint plan  
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

## 6. Proposed sprint sequence

---

# Sprint 1 — DOMAIN-UX1A  
## Health Systems Card contract scaffold and Wave 1 DTO hardening

### Intended outcome

Create the backend/frontend contract foundation for the Health Systems Card.

This sprint should make the Health Systems Card a real product contract, not just a hidden existing component.

### Scope

- Extend the Wave 1 domain DTO with evidence completeness numerator and denominator.
- Add or confirm plain-English descriptor for each Wave 1 domain.
- Confirm score, band, reliability, short read, consequence and next-step fields.
- Ensure frontend TypeScript types match backend output.
- Define a forward-compatible placeholder structure for future subsystem evidence without pretending it is populated.
- Add regression tests proving the frontend does not calculate score, reliability, evidence completeness or missing markers.

### In scope domains

- Cardiovascular health
- Blood sugar control
- Liver health

### Explicitly out of scope

- subsystem chips
- per-subsystem biomarker grouping
- greyed-out biomarker cards
- score dial/gauge
- Wave 2 domains
- frontend-invented marker groupings

### Risk classification

**STANDARD / MIXED**

Reason: light backend DTO assembly plus frontend contract/type alignment. No new scoring logic should be introduced.

### Success criteria

- Backend emits evidence completeness numerator and denominator.
- Frontend can read the new fields.
- Wave 1 card contract is stable and test-covered.
- No consumer/clinical naming layer contamination.
- No frontend calculation of governed evidence logic.

---

# Sprint 2 — DOMAIN-UX1B  
## Wave 1 Health Systems Card frontend scaffold

### Intended outcome

Build the reusable frontend card shell using the agreed design-control direction.

This sprint should create the first visible implementation of the Health Systems Card scaffold for the three Wave 1 domains.

### Scope

- Render the three Wave 1 Health Systems Cards in the main results journey.
- Use the DTO fields from DOMAIN-UX1A.
- Show score, band, score reliability and evidence completeness.
- Keep prose light.
- Display missing markers as a simple evidence-completeness state.
- Use consumer-safe labels only.
- Avoid subsystem chips unless backend-governed subsystem data exists.

### Explicitly out of scope

- per-subsystem sections
- compact biomarker evidence cards
- greyed-out missing-marker cards
- frontend-invented subsystem labels
- Wave 2 domains

### Risk classification

**LOW to STANDARD**

Reason: primarily frontend rendering, assuming Sprint 1 has supplied the required DTO fields.

### Success criteria

- Three Wave 1 domain cards are visible without user needing to open a hidden disclosure.
- The card feels like a first-pass Health Systems Card, not a generic report block.
- Evidence completeness and reliability are visible and understandable.
- The frontend remains renderer-only.
- Clinical labels are not shown in consumer cards.

---

# Sprint 3 — DOMAIN-UX1C  
## Biomarker evidence visual model and missing-marker state

### Intended outcome

Create the reusable biomarker evidence display needed inside future Health Systems Cards.

This sprint should reduce reliance on prose by creating a visual evidence language.

### Scope

- Create compact canonical biomarker card variant.
- Support uploaded/scored marker state.
- Support greyed-out “Not uploaded” marker state.
- Preserve value, unit, range and status visual logic.
- Ensure the same biomarker visual language is used across the product.
- Add missing-marker explanation copy.
- Do not group markers into subsystems unless DTO supplies that structure.

### Explicitly out of scope

- subsystem grouping
- subsystem scores/statuses
- backend marker-to-subsystem logic
- Wave 2 domain assembly

### Risk classification

**LOW / frontend**

Reason: presentation component work only, no analytical logic.

### Success criteria

- A compact biomarker evidence component exists.
- Uploaded/scored markers can be shown visually.
- Missing markers can be shown in a clear greyed-out state.
- Existing biomarker visual semantics are preserved.
- The component is reusable inside future domain/system cards.

---

# Sprint 4 — DOMAIN-UX1D  
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
- frontend-hardcoded subsystem groupings
- unsupported biological labels
- Wave 2 domains

### Risk classification

**HIGH**

Reason: this creates new governed backend interpretation structure and could affect emitted reasoning. It must not create fake scoring or unsupported subsystem claims.

### Success criteria

- Subsystems are backend-governed.
- Marker-to-subsystem groupings are backend-supplied.
- Missing markers can be shown per subsystem.
- Frontend does not decide biological grouping.
- Output is deterministic and test-covered.

---

# Sprint 5 — DOMAIN-UX1E  
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

Reason: frontend plus governed DTO consumption. Risk depends on Sprint 4 output.

### Success criteria

- Full Health Systems Card design works for Wave 1.
- User can see the system score and evidence chain.
- Subsystems and biomarker evidence are visually understandable.
- Missing markers are visible and trust-building.
- The card feels premium, calm and evidence-transparent.
- Fresh UAT confirms a material improvement in user comprehension and perceived product quality.

---

# Sprint 6 — DOMAIN-UX2A  
## Wave 2 domain backend readiness: Blood, iron & oxygen

### Intended outcome

Begin extending the Health Systems Card model beyond Wave 1.

This sprint prepares the first Wave 2 domain for the same card architecture.

### Scope

- Define backend assembly for Blood, iron & oxygen.
- Resolve CBC / iron / B12 / folate marker grouping.
- Define confidence and evidence completeness logic.
- Connect existing governed IDL/Knowledge Bus assets where available.
- Emit domain card DTO only when sufficiently supported.
- Avoid absorbing unrelated one-carbon/methylation constructs wholesale.

### Risk classification

**HIGH**

Reason: new domain assembly and likely cross-system logic.

### Success criteria

- Blood, iron & oxygen can emit a governed domain card DTO.
- Confidence and evidence completeness are explicit.
- Missing-marker logic is deterministic.
- The domain does not overstate unsupported claims.
- Frontend can render the domain using the existing Health Systems Card scaffold.

---

# Sprint 7 — DOMAIN-UX2B  
## Wave 2 domain backend readiness: Thyroid and Kidney

### Intended outcome

Prepare the remaining launch-core domains.

### Scope

- Assess and implement thyroid domain support where deterministic scoring is sufficient.
- Assess and implement kidney domain support with careful eGFR handling.
- Define confidence logic.
- Prevent overstatement on mild abnormalities.
- Emit only if deterministic support is sufficient.
- Ensure missing-marker logic is clear.

### Risk classification

**HIGH**

Reason: likely SSOT/scoring-policy involvement and potential clinical sensitivity around renal/thyroid interpretation.

### Success criteria

- Thyroid & energy regulation and Kidney function are either safely emitted or explicitly gated.
- No fake score is shown where evidence is insufficient.
- Mild abnormality handling is calm and non-alarmist.
- The six launch-core domains have a realistic path to full support.

---

## 7. Recommended immediate next step

The next sprint should be:

> DOMAIN-UX1A — Health Systems Card contract scaffold and Wave 1 DTO hardening

This sprint should not be framed as a quick frontend exposure exercise.

It should be framed as the first step in building the full Health Systems Card architecture.

The immediate goal is to harden the contract for the first three supported domains and make sure the frontend has the correct governed fields before any richer card presentation is built.

---

## 8. Team message

The recommended message to the team is:

> We are not trying to quickly expose a partial card. We are building the Health Systems Card scaffold properly.
>
> The first phase should harden the DTO and frontend contract for the three domains already supported by the repo. The second phase should add the visual biomarker evidence model. The third phase should add governed subsystem evidence, because subsystem labels and marker groupings must come from backend output, not frontend invention.
>
> Once the full card works for Cardiovascular health, Blood sugar control and Liver health, we can extend the same architecture to Blood, iron & oxygen, Thyroid & energy regulation and Kidney function.

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

The right next step is to build the scaffold deliberately, beginning with the contract and DTO hardening for the three Wave 1 domains already supported by the current repo.
