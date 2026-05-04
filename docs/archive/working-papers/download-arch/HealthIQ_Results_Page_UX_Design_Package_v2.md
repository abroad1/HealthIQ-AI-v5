# HealthIQ AI — Results Page UX / Design Package

**Version:** v3  
**Date:** April 2026  
**Status:** Design direction locked for implementation planning  
**Scope:** Results experience only

---

## 1. Purpose

This document defines the target UX architecture for the HealthIQ AI results experience.

It is not a full-platform redesign and it is not a sprint prompt.
It exists to lock the structure, hierarchy, disclosure model, and component behaviour for the results page so the design can be converted into governed frontend implementation work.

This version incorporates strategic review feedback and adds three important refinements:

1. a **primary-driver visual thread** linking the Hero interpretation to the relevant System Group  
2. a **stable biomarker expansion rule** that avoids grid jank  
3. a **missing-data / missing-chapter pattern** that turns absent markers into clinically meaningful incompleteness rather than a dead warning

---

## 2. Governing Design Principles

### 2.1 Narrative before numbers
The first thing the user should understand is the biological story, not the biomarker spreadsheet.

### 2.2 Systems before biomarkers
The results experience should move in this order:

**Hero Interpretation → System Groups → Biomarkers**

### 2.3 Biomarkers are the evidence layer
Biomarker cards exist to support, inspect, and deepen the story rather than replace it.

### 2.4 Progressive disclosure is mandatory
Depth must be revealed deliberately. The default page must feel clear and premium, not dense.

### 2.5 Trust requires honest ambiguity
If two lead concerns are materially tied, both may be shown. The interface must not force false certainty.

### 2.6 Technical detail must not contaminate the retail surface
Technical, clinician, or debug-heavy content belongs in an explicit advanced layer.

### 2.7 No placeholder clutter
Non-live concepts must not consume meaningful visual weight in the default experience.

### 2.8 Missing data should feel meaningful, not administrative
Where a missing marker weakens the current biological story, the UI should explain why that missing marker matters.

---

## 3. Proposed Page Hierarchy

The results page remains a single stacked page.

### Section order

1. Results header  
2. Hero interpretation  
3. Trust strip  
4. System Groups overview  
5. Biomarker evidence layer  
6. Advanced analysis area

### 3.1 Results header
Purpose:
- orient the user
- confirm which result set they are viewing
- provide share/export actions without competing with the Hero

Contents:
- page title
- sample/report date
- biomarker count
- share action
- export action if retained

This should remain compact.

### 3.2 Hero interpretation
Purpose:
- answer “what is the main result story?” immediately

Contents:
- primary concern or co-primary concerns
- 2–4 sentence lead interpretation
- confidence qualifier
- next-step cue

### 3.3 Trust strip
Purpose:
- explain how complete and reliable the current picture is

Contents:
- completeness state
- confidence caveat
- missing-data summary if materially relevant

### 3.4 System Groups overview
Purpose:
- show which body systems or phenotype groups are driving the interpretation

Contents:
- grouped cards
- one-line interpretive summary per card
- support level / confidence
- linked biomarkers
- optional educational expansion

### 3.5 Biomarker evidence layer
Purpose:
- allow users to inspect the evidence under the system story

Contents:
- biomarker card grid
- status, range, value, short interpretation
- optional trend
- optional educational expansion

### 3.6 Advanced analysis area
Purpose:
- contain clinician, technical, and deep-detail material without disrupting the default retail reading path

Contents:
- clinician report
- all insights view if retained
- technical metadata
- confirmatory-test detail
- JSON export if retained

---

## 4. Default Mode vs Advanced Mode

### 4.1 Default mode
Default mode should include:
- Hero interpretation
- Trust strip
- System Groups overview
- Biomarker evidence layer

Default mode should exclude:
- raw engine wording
- technical metadata cards
- clinician-first language
- debug-style data presentation

### 4.2 Advanced mode
Advanced mode should contain:
- full clinician report
- deeper insight views
- extended confirmatory detail
- technical metadata
- export/debug-adjacent content

### 4.3 Interaction model
The current loose “Show technical detail” concept should be replaced by a more deliberate advanced-analysis layer.

Recommended pattern:
- default page remains calm and readable
- user explicitly opens advanced analysis
- advanced content is visually separated from the main narrative path

---

## 5. Hero Interpretation Specification

### 5.1 Required structure
The Hero should contain:
- a lead heading
- primary concern or co-primary concern treatment
- 2–4 sentence explanation
- confidence statement
- next-step pointer

### 5.2 Ambiguity behaviour
If one concern clearly leads:
- show one primary concern treatment

If two concerns are materially tied:
- show both as co-primary within the same Hero block
- do not force a false winner

### 5.3 Next-step cue
The Hero should include a clear continuation cue such as:
- “See the main System Groups involved”
- “Review the biomarkers supporting this pattern”

### 5.4 Primary-driver visual thread
This is now a locked requirement.

Whichever System Group corresponds to the Hero’s primary concern must carry a distinct visual link back to the Hero.

Recommended treatment:
- subtle badge or label such as **Primary Driver**
- stronger border/emphasis state than peer cards
- optional anchor/jump behaviour from Hero into that specific System Group card

Purpose:
- preserve narrative continuity when the user scrolls
- make the story-to-evidence relationship visually obvious

Rejected alternative:
- leaving the Hero disconnected from the system layer and expecting the user to infer the link manually

---

## 6. Trust Strip Specification

### 6.1 Role
This section explains how complete and dependable the current picture is.

### 6.2 Default visible content
- completeness state
- one confidence/caveat sentence
- important missing-data note if applicable

### 6.3 Expanded content
Optional expansion may reveal:
- confirmatory tests
- additional quality flags
- deeper completeness detail

### 6.4 Tone
This strip must not read like engineering plumbing.

Preferred framing:
- how complete this picture is
- how confident we are
- what may still be missing

### 6.5 Missing-data / missing-chapter pattern
This is now a locked requirement.

If a missing marker materially affects the leading biological story, the UI should not only say that it is absent.
It should briefly explain why it matters.

Recommended behaviour:
- show a muted **Missing Chapter** cue inside the Trust Strip or relevant downstream section
- example framing: “Folate was not tested, which limits how complete this vascular/methylation story is.”

This is not a sales widget.
It is a clinical completeness explanation that can later support retention or retesting logic.

Rejected alternative:
- generic “data missing” warning with no biological meaning

---

## 7. System Group Card Specification

### 7.1 Role
System Group cards are the main connected-biology layer.
They sit between the Hero and biomarkers.

### 7.2 Default card content
Each card should show:
- system/group name
- status or severity badge
- one-line interpretive summary
- support/confidence indicator
- number of supporting biomarkers
- optional Primary Driver treatment if relevant

### 7.3 Expanded state
Expanded content should show:
- short educational explainer
- linked biomarker chips
- next relevant areas or recommendations
- category/context tag where useful

### 7.4 Content split
Interpretive content answers:
- what this user’s results suggest about this system

Educational content answers:
- what this system does
- why it matters biologically

### 7.5 Interaction pattern
System Group cards should use inline expansion.
This is appropriate because:
- system groups are relatively few
- users are likely to inspect only a small number in one session
- inline expansion keeps the reading flow intact

---

## 8. Biomarker Card Specification

### 8.1 Strategic role
Biomarkers are the evidence layer.
They should feel precise and trustworthy, but not dominate the page.

### 8.2 Grid model
Biomarkers remain card-based, not table-based.

Target layout:
- desktop: up to 3 columns
- tablet: 2 columns
- mobile: 1 column

### 8.3 Collapsed state
Every collapsed biomarker card should show:
- biomarker name
- latest value and unit
- lab range
- direction/status
- short interpretation sentence
- dial/marker visual
- tiny trend cue only if real history exists
- expand affordance

### 8.4 Expanded state
Expanded biomarker card should show:
- educational explainer text
- contribution context where available
- larger trend view when history exists
- related system tags
- optional “why flagged” note

### 8.5 Missing explainer handling
If educational explainer content is absent:
- do not render an empty explainer shell
- omit the section cleanly
- do not clutter the default interface with placeholder text

### 8.6 Stable expansion rule
This is now a locked requirement.

Inline expansion must **not** produce broken or uneven grid behaviour.

The architectural requirement is:
- expansion must remain visually stable and premium
- no awkward column drops or jagged CSS-grid collapse effects

Recommended implementation behaviour:
- when expanded, the selected biomarker card should break into a controlled full-width detail row within the biomarker section
- the collapsed grid remains stable above/below it

This is preferred over naïve same-cell height expansion.

Alternative that may still be acceptable if chosen deliberately:
- single active detail panel below the grid, populated by the selected biomarker card

Rejected by default:
- naïve per-card expansion inside a standard 3-column grid causing layout jank
- casual masonry adoption without a deliberate architectural decision

### 8.7 Trend placement
Collapsed state:
- only a tiny cue if real history exists

Expanded state:
- larger inline trend module

No fake trend placeholders should be shown.

---

## 9. Disclosure and Interaction Model

### 9.1 Hero
Always visible, never collapsible.

### 9.2 Trust strip
Compact by default with optional “more detail” reveal.

### 9.3 System Group cards
Inline expansion.

### 9.4 Biomarkers
Collapsed scan surface + controlled stable detail reveal.

### 9.5 Advanced analysis
Explicit advanced layer at the bottom of the page or equivalent clearly separated area.

### 9.6 Why this mix is correct
- Hero must anchor the experience
- System Groups are few enough for inline reveal
- Biomarkers are numerous and need scanability first
- advanced content is conceptually different and should not be mixed into the retail journey

---

## 10. Responsive Behaviour

### 10.1 Desktop
- Hero full width
- Trust strip full width
- System Groups in compact multi-column layout
- Biomarkers in up to 3 columns
- advanced analysis full width

### 10.2 Tablet
- System Groups in 2 columns
- Biomarkers in 2 columns
- keep stacked reading order

### 10.3 Mobile
- single-column stack
- compact Hero
- full-width system cards
- full-width biomarker cards
- inline detail retained
- no dependence on hover
- no overcrowded multi-column advanced tabs

---

## 11. Section-by-Section Change from Current Repo Reality

### Keep
- single-page results architecture
- Hero interpretation layer
- Trust/data-quality concept
- System Group layer
- biomarker grid direction
- advanced/clinician material as a lower-priority layer

### Change
- compress and reframe PipelineStatus into a Trust Strip
- visibly connect Hero to the relevant primary System Group
- add system educational explainer rendering
- add biomarker educational explainer rendering
- add contribution context rendering where appropriate
- replace unstable inline biomarker expansion with a controlled stable expansion pattern
- convert missing-data warnings into a missing-chapter pattern when clinically relevant
- reduce duplication across Hero / Overview / Clinician surfaces

### Remove or hide
- symptom-relevance placeholder from the default page
- fake trend placeholder behaviour
- technical language leaking into default retail-facing areas

---

## 12. Design Decisions Locked

The following decisions are now considered locked unless a strong architectural objection emerges:

1. The results experience remains a single stacked page.  
2. The page hierarchy is Hero → Trust Strip → System Groups → Biomarkers → Advanced Analysis.  
3. System Groups remain above biomarkers.  
4. Biomarkers remain card-based rather than table-based.  
5. Biomarker detail uses a controlled stable expansion pattern rather than naïve inline grid growth.  
6. Hero-to-primary-System visual linkage is required.  
7. Missing-data should become a biologically meaningful missing-chapter pattern where relevant.  
8. Technical/clinician/deep-detail content moves into an explicit advanced layer.  
9. Missing explainer content is handled by clean omission, not empty shells.  
10. Symptom relevance remains out of the default retail experience until live.

---

## 13. Rejected Alternatives

### 13.1 Generic biomarker table as the main results surface
Rejected because it collapses the product back into a standard lab dashboard.

### 13.2 Widget-heavy dashboard hero
Rejected because it weakens narrative clarity.

### 13.3 Equal-weight clinician and retail layers
Rejected because it produces duplication and split attention.

### 13.4 Naïve inline biomarker expansion in a fixed 3-column grid
Rejected because it risks layout jank and a low-quality interaction feel.

### 13.5 Generic missing-data warning with no biological explanation
Rejected because it wastes one of the product’s clearest trust and retention opportunities.

### 13.6 3D or gimmick-led redesign as the route to “wow”
Rejected because HealthIQ’s advantage should come from interpretation clarity and deterministic depth, not novelty effects.

---

## 14. Requires Further Product Decision

These are not blockers to direction, but still need product decisions before final implementation scoping:

1. whether advanced analysis is a lower expandable section, segmented sub-area, or dedicated subview  
2. whether contribution context appears in default expanded biomarker view or advanced only  
3. whether export JSON remains user-visible  
4. whether clinician report remains visible to all users in the same surface long term  
5. whether missing-chapter cues stay informational only or later become linked retest prompts  
6. whether the stable biomarker detail pattern is implemented as full-width breakout rows or a single shared detail panel

---

## 15. Ready for Implementation

This package is now ready to be translated into governed frontend implementation planning.

Recommended implementation order:

1. restructure the page hierarchy and remove duplication  
2. convert PipelineStatus into the Trust Strip  
3. implement Hero-to-primary-System visual threading  
4. upgrade System Group cards with educational explainer rendering  
5. upgrade biomarker cards with stable expansion behaviour  
6. add biomarker explainer and contribution-context rendering  
7. add missing-chapter behaviour where clinically relevant  
8. isolate advanced analysis properly  
9. remove placeholder symptom block and any fake trend behaviour

---

## 16. Summary

The results page should now be understood as a guided biological interpretation surface.

Its structure is:
- lead with the story
- connect that story to body-system groups
- let users inspect the biomarker evidence
- reveal deeper material on demand

The most important refinements added in v2 are:
- the Hero must visibly connect to the primary System Group
- biomarker expansion must remain stable and premium
- missing data must be explained as biological incompleteness where relevant

