# HealthIQ AI — Results Page UX / Design Package

Version: v1
Scope: Blood-results experience only
Status: Design proposal for governed implementation planning

---

## 1. Purpose

This document defines the proposed UX architecture for the HealthIQ AI results experience.

It is intentionally focused on the interpreted blood-results page only.
It does not redesign the whole platform.
It assumes the surrounding product journey exists, but treats that as an external boundary rather than the main design task.

This package is based on the audited repo reality that the current results surface already contains:

- hero interpretation content
- confidence / data-quality content
- system / cluster content
- biomarker content
- deeper clinician / technical content

The design task is therefore not to invent a brand-new dashboard.
It is to reorganise, clarify, and deepen the existing results experience so that it feels biologically intelligent, trustworthy, and progressively revealing.

---

## 2. Design Principles

### 2.1 Narrative first

The user should understand the main biological story before being asked to inspect the supporting evidence.

### 2.2 Systems before biomarkers

HealthIQ’s advantage is connected interpretation, not isolated test values.
The page should therefore present system-level meaning before biomarker-level detail.

### 2.3 Biomarkers as evidence layer

Biomarkers should support and validate the interpretation.
They are not the hero of the page.

### 2.4 Progressive disclosure

The page should show the smallest useful amount of information by default, then allow users to reveal educational and technical depth on demand.

### 2.5 Retail-first default mode

The default experience must feel clear and calm for a standard retail user.
It must not read like a clinician console or an engineering debug screen.

### 2.6 Explicit advanced depth

Technical, clinician-oriented, or model-adjacent detail should exist in a clearly separated advanced layer.

### 2.7 Honest ambiguity

If two concerns are genuinely tied, the product must be allowed to show both.
It must not manufacture false certainty.

### 2.8 No placeholder theatre

Placeholder functionality should not occupy meaningful space in the live results page.
If something is not active, it should be removed from the default experience.

---

## 3. Proposed Page Hierarchy

The results page should remain a single stacked page.

Recommended order:

1. Results header
2. Hero interpretation
3. Confidence / data-quality strip
4. Systems overview
5. Biomarker evidence grid
6. Advanced analysis area

### 3.1 Results header

Purpose:
Orient the user.

Contents:
- page title
- date of analysis / report date
- biomarker count
- low-emphasis share / export actions

This section should be compact and functional.
It should not compete with the hero interpretation.

### 3.2 Hero interpretation

Purpose:
Answer the user’s first question: what is the main story here?

Contents:
- primary concern title
- co-primary concern handling when appropriate
- short lead interpretation
- brief confidence qualifier
- one prompt guiding the user to the next section

### 3.3 Confidence / data-quality strip

Purpose:
Explain how complete and trustworthy the current picture is.

Contents:
- completeness state
- confidence caveat
- missing-data note when materially important

This should sit directly below the hero.

### 3.4 Systems overview

Purpose:
Translate the interpretation into connected biology.

Contents:
- compact system cards
- system status / severity
- one-line interpretive summary
- expandable educational depth

### 3.5 Biomarker evidence grid

Purpose:
Let the user inspect the evidence beneath the system story.

Contents:
- biomarker cards
- current result
- range and direction
- short interpretation
- optional trend indicator
- expandable educational content

### 3.6 Advanced analysis area

Purpose:
Contain deeper clinician / technical content without polluting the main user flow.

Contents:
- clinician report
- full insights surfaces
- technical metadata
- export / debug-adjacent material if retained

---

## 4. Default Mode vs Advanced Mode

### 4.1 Recommended approach

#### Default mode

Visible by default:
- results header
- hero interpretation
- confidence / data-quality strip
- systems overview
- biomarker evidence grid

Not visible by default:
- clinician report as a peer tab
- raw technical metadata
- debug-like wording
- internal object references

#### Advanced mode

Accessible through a clear entry point such as:
- Advanced analysis
- View detailed report

Advanced mode may contain:
- full clinician report renderer
- deeper confirmatory content
- full insights surface
- technical metadata
- export JSON

### 4.2 Why this approach is recommended

The current page already contains the right broad content layers, but they are too equal in weight.
The default experience should feel like one coherent narrative path.
Advanced content should remain available, but explicitly separated.

### 4.3 Rejected alternatives

#### Rejected: equal-weight tabs for retail and clinician users
Why rejected:
Creates duplication and split attention.

#### Rejected: one coarse page-wide technical toggle controlling all density
Why rejected:
Too blunt and structurally messy.

---

## 5. Hero Interpretation Specification

### 5.1 Purpose

The hero is the interpretive opening of the page.
It should feel like the product’s strongest moment.

### 5.2 Required content

- heading: main result story
- primary concern title
- co-primary concern support when ambiguity is real
- 2–4 sentence narrative summary
- short confidence sentence
- one next-step pointer

### 5.3 Reading hierarchy

Order:
1. What appears to matter most
2. Why that matters biologically
3. How confident the product is
4. Where the user should go next

### 5.4 Ambiguity handling

If one concern leads clearly:
- show a single primary concern surface

If two concerns are materially tied:
- show two co-primary concerns in one hero block
- do not force one to dominate artificially

### 5.5 Rejected alternatives

#### Rejected: stat-heavy dashboard hero
Why rejected:
Turns the hero into a score panel rather than an interpretation surface.

---

## 6. Confidence / Data-Quality Layer Specification

### 6.1 Role

This layer should communicate trust without intimidation.

### 6.2 Recommended format

A compact trust strip directly below the hero.

### 6.3 Default visible content

- completeness summary
- confidence caveat
- missing-marker summary only when material

### 6.4 Optional expanded content

- confirmatory test suggestions
- lab-range quality specifics
- pass/fail detail if still useful

### 6.5 Content tone

Use plain language such as:
- How complete this picture is
- How confident we are
- What may be missing

Avoid:
- pipeline jargon
- engine-object terminology
- internal reasoning labels

### 6.6 Rejected alternatives

#### Rejected: hide confidence entirely inside hero copy
Why rejected:
Too important to bury.

#### Rejected: large technical diagnostic block in default mode
Why rejected:
Too heavy for the retail path.

---

## 7. System / Cluster Card Design Specification

### 7.1 Role of system cards

System cards are the connected-biology layer.
They should help the user understand which areas of the body or biological model appear most involved.

### 7.2 Default visible content

Each system card should show:
- system name
- severity / status badge
- one-line interpretive summary
- support indicator or confidence level
- number of contributing biomarkers

### 7.3 Expanded content

When expanded, the card should reveal:
- short educational explainer
- contributing biomarkers as linked pills/tags
- recommendation or next inspection cue
- category label only if useful

### 7.4 Interpretive vs educational split

Expanded system cards should clearly separate:

What your results suggest:
- interpretive summary for this user

About this system:
- short educational explainer about the biological system itself

### 7.5 Interaction model

Use inline expand/collapse inside the card.

Why:
- system cards are relatively few
- inline expansion preserves context
- the user can read systems in sequence without leaving the page

### 7.6 Differences from biomarker cards

System cards should be:
- broader
- more narrative
- less number-led
- more interpretive

### 7.7 Rejected alternatives

#### Rejected: separate system detail pages
Why rejected:
Too heavy for current product maturity and breaks the stacked interpretive flow.

---

## 8. Biomarker Card Design Specification

### 8.1 Recommended model

Keep card-based presentation, not table-based presentation.

Why:
- current frontend is already structurally aligned to cards and dials
- cards support progressive disclosure better than generic tables
- tables would make the product feel more like a conventional lab viewer

### 8.2 Collapsed state

Each biomarker card should display:
- biomarker name
- latest value and unit
- lab range
- direction / status: high, low, in range
- one short interpretation sentence
- compact visual indicator (dial / marker)
- optional tiny trend sparkline if history exists
- expand control

### 8.3 Expanded state

Expanded biomarker card should reveal:
- educational explainer text
- contribution context when available
- larger trend mini-chart when history exists
- related systems or context tags
- optional “why this matters” line

### 8.4 Trend handling

Collapsed state:
- tiny sparkline only when meaningful history exists

Expanded state:
- larger mini-chart inline inside the card

### 8.5 Missing explainer handling

If no educational explainer exists:
- do not render an empty explainer area
- do not create visual dead space
- optionally show muted “Detailed explainer coming soon” only in advanced mode if required

### 8.6 Interpretation sentence rule

Collapsed state:
- one sentence only

Expanded state:
- supporting educational depth may be longer

### 8.7 Grid behaviour

Desktop:
- maximum 3 columns

Tablet:
- 2 columns

Mobile:
- 1 column

### 8.8 Rejected alternatives

#### Rejected: table-first biomarker presentation
Why rejected:
Too generic and poor for mixed explanatory content.

#### Rejected: all educational text visible by default
Why rejected:
Creates a wall of content and destroys scanability.

---

## 9. Disclosure / Interaction Pattern Recommendation

### 9.1 Recommended pattern by section

#### Hero
Always visible. No collapse.

#### Confidence strip
Compact by default, optional inline “more detail”.

#### System cards
Inline expand/collapse.

#### Biomarker cards
Inline per-card expand/collapse.

#### Advanced analysis
Explicit bottom-of-page advanced section.

### 9.2 Why this mix is recommended

- systems are few enough for inline expansion to remain manageable
- biomarkers are many, so expansion must remain local to each card
- advanced material is conceptually different from the retail path and should sit in its own layer

### 9.3 Rejected alternatives

#### Rejected: drawer / slide-over for biomarker detail
Why rejected:
Disruptive for repeated browsing and comparison.

#### Rejected: heavy tooltip usage
Why rejected:
Weak on touch devices and too shallow for meaningful educational content.

#### Rejected: tabs as the primary structure for the full page
Why rejected:
Tabs hide too much of the page hierarchy and increase mode-switching.

---

## 10. Responsive / Layout Guidance

### 10.1 Desktop

- full-width hero
- trust strip directly below hero
- systems in 2–3 column compact arrangement depending on count
- biomarkers in 3-column grid
- advanced area full width at bottom

### 10.2 Tablet

- systems in 2 columns
- biomarkers in 2 columns
- hero and trust strip remain stacked

### 10.3 Mobile

- single-column stack
- hero simplified but still narrative-first
- system cards full width
- biomarker cards full width
- expanded content stays inline
- avoid tab-heavy dense controls

### 10.4 Specific repo-aware note

The current insights surface appears too interaction-dense for narrower screens.
It should be treated as advanced/deeper material rather than as core page navigation.

---

## 11. Section-by-Section Changes from Current Repo Reality

### 11.1 Results header
Keep, but reduce visual dominance.

### 11.2 Hero interpretation
Keep and strengthen as the true opening section.

### 11.3 Pipeline status area
Keep the underlying information, but recast it as a compact trust strip with plain-language framing.

### 11.4 Cluster summary
Keep the section, but:
- separate interpretive and educational content more clearly
- add system educational explainer rendering when available
- remove fake trend placeholders until real data exists

### 11.5 Biomarker dials
Keep the grid/card direction, but upgrade the card anatomy by adding:
- expand/collapse
- explainer rendering
- contribution-context rendering
- real trend placement when available

### 11.6 Symptom relevance placeholder
Remove from the default page until live functionality exists.

### 11.7 Overview / All insights / Clinician report tabs
Demote these into the advanced analysis layer rather than treating them as peer navigation for the default user path.

### 11.8 Technical detail toggle
Replace the coarse page-wide technical detail approach with a clearer advanced-layer model.

---

## 12. Design Decisions Locked

The following decisions are recommended as locked for implementation planning:

- the results experience remains a single stacked page
- systems remain above biomarkers
- biomarkers remain card-based, not table-based
- biomarker detail is progressively disclosed within each card
- system cards use inline expansion
- confidence/data-quality remains visible near the top in compressed form
- clinician / technical material moves into an explicit advanced layer
- placeholder symptom space is removed from the default path until real
- missing explainer content is handled by omission, not empty shells

---

## 13. Rejected Alternatives

### 13.1 Generic lab dashboard / table-first design
Rejected because it collapses the product back into a standard result viewer.

### 13.2 Widget-heavy summary board hero
Rejected because it weakens the interpretive opening.

### 13.3 Full-page tabbed architecture
Rejected because it hides hierarchy and encourages duplication.

### 13.4 Drawer-based biomarker exploration
Rejected because repeated evidence browsing becomes clumsy.

### 13.5 Exposing technical detail throughout default mode
Rejected because it undermines clarity for retail users.

### 13.6 Equal-weight clinician and retail surfaces
Rejected because it produces split attention and structural repetition.

---

## 14. Requires Further Product Decision

The following points remain product decisions rather than locked UX decisions:

- whether advanced analysis is a lower-page expandable section or a dedicated subview
- whether biomarker mini-trends should appear only when there are at least 2–3 real historical points
- whether contribution context belongs in normal expanded view or advanced mode only
- whether export JSON remains user-visible or becomes debug/admin only
- whether clinician report remains visible in the retail product surface long-term or becomes role-gated later

---

## 15. Ready for Implementation

This design package is ready to be translated into a governed frontend implementation plan.

Recommended implementation sequence:

1. restructure page hierarchy and reduce duplication
2. compress trust/data-quality into a trust strip
3. add system educational explainer rendering to system cards
4. upgrade biomarker cards to collapsed + expanded anatomy
5. add biomarker educational explainer and contribution-context rendering
6. create explicit advanced analysis layer
7. remove symptom placeholder from default results page
8. add trend visuals only when backed by real data

---

## 16. Summary

This proposal keeps the current deliverable tightly focused on the results experience.
It assumes the wider platform journey exists, but treats that as a boundary rather than a second full design project.

The core UX objective is not to make the page more decorative.
It is to make the deterministic biological interpretation more legible, more trustworthy, and more obviously superior to a conventional lab report.
