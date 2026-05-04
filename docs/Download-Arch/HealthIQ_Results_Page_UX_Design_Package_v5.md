# HealthIQ Results Page UX / Design Package v3

## Status
Locked for implementation prompting, subject to final product sign-off.

## Scope
This document covers the blood-results experience only.
It does not redesign the public site, auth, upload, or account/history areas.

---

## 1. Design principles

The results experience must feel:
- biologically intelligent
- trustworthy
- layered
- premium rather than cluttered
- deep on demand, not dense by default

Core product hierarchy:
1. Hero interpretation
2. Trust Strip
3. System Groups
4. Biomarkers
5. Advanced Analysis

Core design rules:
- Narrative first
- Systems before biomarkers
- Evidence beneath interpretation
- Progressive disclosure over visual overload
- Honest ambiguity over false certainty
- Default mode must remain retail-friendly
- Advanced analysis must remain separated from the retail flow
- No placeholder UI in the default experience

---

## 2. User-facing terminology lock

Retail-facing term:
- **System Groups**

Do not use on the default retail surface:
- phenotype groups
- phenotype clusters
- phenotype map terminology

Internal/technical terms may still exist in code and payloads, but the user-facing label is locked to **System Groups**.

---

## 3. Proposed page hierarchy

### A. Results header
Compact context only:
- page title
- report/test date
- biomarker count
- share/export actions in a quieter position

### B. Hero interpretation
Purpose:
- answer the user’s first question: what is the main story?

### C. Trust Strip
Purpose:
- explain how complete and how trustworthy the current picture is

### D. System Groups
Purpose:
- show the main biological systems/patterns implicated by the results

### E. Biomarker evidence layer
Purpose:
- let users inspect the evidence beneath the system-level story

### F. Advanced Analysis
Purpose:
- contain clinician/deeper/technical material outside the main retail flow

---

## 4. Default mode vs advanced mode

### Default mode
Visible in the main reading flow:
- Hero interpretation
- Trust Strip
- System Groups
- Biomarker evidence layer

Not visible by default:
- full clinician report
- technical metadata
- export/debug-adjacent detail
- long confirmatory detail
- internal/runtime language

### Advanced Analysis
Advanced Analysis is locked to:
- **a lower-page expandable section on the same stacked page**

It is not:
- a dedicated subview
- a separate page
- a top-level peer tab to the main retail flow

Advanced Analysis may contain:
- clinician report rendering
- all-insights view
- deeper confirmatory detail
- technical metadata
- export JSON if retained

---

## 5. Hero interpretation specification

### Role
The Hero is the opening biological narrative.
It should immediately explain the user’s main result story before any numeric inspection.

### Copy structure lock
The Hero is capped to:
1. **1 headline line**
2. **1 interpretation paragraph**
3. **1 confidence qualifier line**
4. **1 next-step cue maximum**

This replaces looser “2–4 sentence” phrasing.

### Content
- primary concern title
- co-primary concern handling when ambiguity is real
- short interpretation paragraph
- confidence qualifier
- one next-step cue, e.g. “See affected System Groups” or “Review supporting biomarkers”

### Honest ambiguity rule
If one concern clearly leads:
- show one primary concern layout

If two concerns are materially tied:
- show co-primary concern treatment in the Hero
- do not force a false single winner

### Primary Driver visual thread
The System Group corresponding to the Hero’s lead concern must carry a distinct visual anchor, for example:
- subtle border emphasis
- active-state treatment
- “Primary Driver” badge

This creates a visible narrative link from Hero to System Groups.

---

## 6. Trust Strip specification

### Role
The Trust Strip explains confidence and completeness without becoming advisory-heavy.

### Default content cap
Default Trust Strip content is locked to:
- **maximum 2 visible lines by default**

Recommended default structure:
- line 1: completeness / confidence summary
- line 2: one caveat or one missing-data cue only when materially relevant

Everything else goes behind reveal.

### Default-visible content priority
Priority order:
1. completeness/confidence summary
2. confidence caveat, if important
3. missing chapter cue, if triggered by threshold rule

### Hidden behind reveal
- detailed confirmatory notes
- lab-range quality specifics
- secondary caveats
- additional missing-data commentary

### Tone rule
Do not use:
- pipeline language
- engine-object language
- technical runtime phrasing

Use plain-language trust framing only.

---

## 7. Formal content-layer separation rule

The results page must preserve the distinction between three different content classes.
They must not be merged into one generic text blob.

### A. Short interpretation
Purpose:
- explain what this result suggests for this user

Characteristics:
- short
- interpretive
- tied to the current result
- visible in collapsed/default card state where appropriate

### B. Educational explainer
Purpose:
- explain what the biomarker or system is and why it matters biologically

Characteristics:
- educational
- broader and more durable
- not specific to this exact user state alone
- revealed on demand

### C. Contribution context
Purpose:
- explain how the biomarker contributes to the current System Group or lead story

Characteristics:
- relational
- links atom-level evidence to system-level meaning
- neither generic education nor generic interpretation
- revealed only in expanded detail

### Implementation rule
Interpretation, educational explainer, and contribution context must remain separate UI fields and separate rendering zones.
They must not be concatenated into one paragraph during implementation.

---

## 8. System Group card specification

### Role
System Groups are the secondary biological surface.
They sit above biomarkers and carry the connected-body meaning of the results.

### Default-visible card content
- System Group name
- severity/status badge
- one-line interpretive summary
- confidence/support indicator
- number of contributing biomarkers
- Primary Driver indicator when applicable

### Expanded content
- short educational explainer when available
- contributing biomarkers as linked pills/tags
- recommendations or next inspection prompts

### Fallback rule
If system educational explainer is absent:
- keep the System Group card interpretive only
- do not create an empty education area

### Interaction pattern
System Group cards use:
- inline expand/collapse

---

## 9. Biomarker card specification

### Role
Biomarkers are the evidence layer.
They support the system-level story rather than acting as the page’s primary narrative.

### Layout model
Biomarkers remain:
- card-based
- grid-based

Desktop:
- up to 3 columns

Tablet:
- 2 columns

Mobile:
- 1 column

### Collapsed/default state
Each biomarker card shows:
- biomarker name
- latest result + unit
- lab range
- direction/status
- one short interpretation sentence
- small visual gauge/marker
- expand control
- tiny trend cue only when real history exists
- no stub trend icon, empty chart frame, or visual promise of history when the contract is absent

### Expanded/detail state
Expanded detail shows, in order:
1. educational explainer
2. contribution context
3. trend module when history exists
4. related System Group tags where useful

### Biomarker detail interaction lock
The biomarker detail pattern is locked to:
- **single shared detail panel below the grid on desktop/tablet**
- **inline beneath the selected card on mobile**

This replaces the earlier open choice between breakout-row and shared-panel patterns.

### Why this pattern is chosen
- more stable than per-card grid expansion
- avoids layout jank
- simpler to maintain
- preserves premium grid behaviour

### Fallback rules
If biomarker educational explainer is absent:
- omit cleanly

If contribution context is absent:
- omit cleanly

If no history exists:
- no trend module

---

## 10. Missing Chapter pattern

### Role
Missing-data treatment should be clinically meaningful, not sales-like.

### Trigger threshold lock
A Missing Chapter cue appears only when the missing marker affects at least one of the following:
1. the Hero concern
2. the Primary Driver System Group
3. a confidence downgrade already present in the Trust Strip

If none of those are true:
- do not surface Missing Chapter in the default experience

### Placement
Preferred placement:
- Trust Strip reveal content
- or a muted contextual cue attached to the relevant System Group / biomarker detail area

Do not scatter Missing Chapter cards throughout the page.

---

## 11. Advanced Analysis specification

Advanced Analysis is locked to:
- a lower-page expandable section within the same stacked results page

It may contain:
- clinician report
- all insights
- expanded confirmatory material
- technical metadata
- export/debug-adjacent information if retained

It must not interrupt the default retail reading flow.

---

## 12. Partial content coverage and graceful fallback rules

Because content coverage is currently partial/pilot, the UI must degrade cleanly.

Formal fallback rules:
- if biomarker explainer absent: omit cleanly
- if contribution context absent: omit cleanly
- if system explainer absent: keep System Group card interpretive only
- if no history exists: omit trend module
- if no co-primary concern exists: use single-lead Hero layout only
- if no Missing Chapter trigger threshold is met: omit Missing Chapter treatment entirely

No empty shells.
No “coming soon” noise in the default retail flow.

---

## 13. Section-by-section change from current repo reality

### Keep
- single stacked page model
- Hero section
- trust/data-quality concept
- System Group layer
- biomarker layer
- advanced/deeper material on same page

### Change
- standardise retail term to System Groups
- compress Trust Strip
- tighten Hero copy structure
- add Primary Driver visual thread
- render system educational explainer when available
- render biomarker education and contribution context as separate layers
- lock shared biomarker detail panel pattern
- lock Advanced Analysis to lower-page expandable section
- remove placeholder symptom section from default experience until live

---

## 14. Design decisions locked

- User-facing term is **System Groups**
- Results experience remains a single stacked page
- Page hierarchy is Hero → Trust Strip → System Groups → Biomarkers → Advanced Analysis
- Systems stay above biomarkers
- Hero copy is capped to headline + paragraph + confidence line + one next-step cue
- Trust Strip default content is capped to 2 visible lines
- Interpretation / educational explainer / contribution context remain formally separate content classes
- Biomarkers stay grid/card-based
- Biomarker detail uses a single shared detail panel below the grid on desktop/tablet and inline beneath the selected card on mobile
- Missing Chapter appears only under the defined threshold rule
- Advanced Analysis is a lower-page expandable section, not a dedicated subview
- Partial content coverage must degrade cleanly with omission rather than placeholders

---

## 15. Ready for implementation

### Implementable now in FE-B2
- Hero
- Trust Strip
- System Groups
- biomarker cards
- educational explainers
- contribution context
- advanced analysis

### Deferred dependency (not part of FE-B2 build scope)
- live trend/history rendering

Trend/history layout is in scope architecturally, but live rendering is excluded from the first implementation sprint until the backend history contract is available.


This document is ready to drive implementation prompting.

Recommended implementation sequence:
1. restructure page hierarchy and remove duplication
2. implement tightened Hero structure and Primary Driver visual thread
3. compress Trust Strip to default 2-line model with reveal
4. upgrade System Group cards with educational explainer support and fallback behaviour
5. upgrade biomarker cards with explicit interpretation / educational / contribution-context separation
6. implement shared biomarker detail panel pattern
7. implement Missing Chapter trigger logic and placement rules
8. implement Advanced Analysis as lower-page expandable section
9. remove placeholders from the default retail flow


---

## Controlled amendment — trend/history dependency note

This document remains the governing UX/design package for the results experience.

### Trend/history status clarification

Trend/history remains part of the intended biomarker expanded experience and has **not** been removed from the frontend architecture.

However, implementation of live trend rendering is dependent on backend/platform delivery of a reliable history contract.

### Required backend/platform dependency

For the trend module to be activated in the frontend, the platform must provide a trustworthy per-user, per-biomarker history payload including, at minimum:

- prior biomarker values
- associated dates
- stable biomarker identity matching across analyses/tests

Preferred additional support:

- prior lab/reference range context where available
- unit continuity or explicit unit context where relevant

### Frontend implementation rule

The frontend should:

- preserve a trend/history slot in the biomarker expanded state
- scaffold the component boundary and layout position in implementation
- activate live trend rendering only when the backend history contract is delivered and verified

### Phase-1 interpretation

For phase 1, the absence of currently implementation-ready backend history support does **not** change the intended UX architecture.

It means only that trend/history is a **declared backend dependency** for delivery, not a feature to be silently removed from the frontend design.

### Build-team handoff note

Any implementation prompt derived from this document must explicitly flag biomarker trend/history as:

- retained in UX scope
- blocked by backend/platform dependency
- requiring contract delivery before production activation


### Implementation boundary clarification
The backend history dependency is a separate platform/data contract track and is not part of this frontend implementation package.
