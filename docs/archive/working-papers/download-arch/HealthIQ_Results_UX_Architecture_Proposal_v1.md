# HealthIQ AI Results Experience — UX Architecture Proposal v1

## 1. Design principles

The page should feel like:
- a guided biological interpretation
- evidence-backed, not decorative
- layered, not crowded
- calm for retail users
- deep for advanced users without making default mode feel clinical or technical

The governing principles are:

### Narrative first
The user should understand “what this likely means” before they are asked to inspect biomarkers.

### Systems before atoms
Clusters/systems should sit above biomarkers in the reading order because the product advantage is connected interpretation, not isolated numbers.

### Evidence beneath interpretation
Biomarkers are the trust layer. They support the story and let the user inspect the evidence.

### Progressive disclosure, not constant expansion
The main page should show the smallest useful surface by default. Detail should be revealed where it is contextually relevant, not hidden in random tabs.

### Default mode must be non-technical
Retail users should not be asked to interpret engine objects, policy labels, or internal model concepts.

### Advanced mode must be explicit
Technical detail should exist, but in a deliberate layer. “Show technical detail” is the correct concept, but it needs to become a true advanced disclosure model rather than a loose page-wide toggle.

### No placeholder theatre
Anything that is clearly not live, such as symptom relevance, should not consume meaningful visual weight on the main page.

## 2. Proposed page hierarchy

Recommended page order:

A. Results header  
B. Hero interpretation  
C. Confidence and data-quality strip  
D. Systems overview  
E. Biomarker evidence grid  
F. Advanced analysis area

### A. Results header
Purpose: orient the user.

Contents:
- page title
- sample/report date
- biomarker count
- share/export actions in a quieter position

This should be compact. It is not the main event.

### B. Hero interpretation
Purpose: answer “what is the main story?”

Contents:
- primary concern / co-primary concern
- short lead interpretation
- one plain-English confidence statement
- one next-step or “what to look at next” prompt

This remains the first major section.

### C. Confidence and data-quality strip
Purpose: explain how much to trust the current story.

Contents:
- panel completeness
- confidence caveat
- missing-data summary if materially relevant

This should be visually lighter than the hero but always visible near it.

### D. Systems overview
Purpose: show which biological systems are most implicated.

Contents:
- a compact set of system cards
- top systems first
- one-line interpretive description on each
- expand-on-demand for educational/system detail

This is the second major reading layer.

### E. Biomarker evidence grid
Purpose: let the user inspect the evidence under the system story.

Contents:
- biomarker cards
- current value, range, status, short interpretation
- optional trend mini-chart when available
- on-demand educational explainer

This is the most browsable part of the page.

### F. Advanced analysis area
Purpose: contain clinician/deeper/technical detail without polluting the default path.

Contents:
- full clinician report rendering
- all insights
- export/debug-adjacent material if retained

This should sit at the bottom behind an explicit advanced entry point.

## 3. Default mode vs advanced mode

### Recommended approach

#### Default mode
- Hero interpretation
- Confidence/data-quality strip
- Systems overview
- Biomarker evidence grid
- No raw “engine” wording
- No clinician tab visible by default
- No technical metadata card open by default

#### Advanced mode
- Full clinician report
- deeper reasoning/insight panels
- full confirmatory-test lists
- technical metadata
- export JSON
- anything that refers to internal objects or runtime policy

### How it should work
Replace the current loose “Show technical detail” behaviour with a clearer advanced-mode entry:
- default page stays clean
- a single “Advanced analysis” control opens the deeper layer lower on the page
- advanced mode persists for the session once opened

### Rejected alternative
A permanent top-level tab set where retail and clinician content are equal peers.

**Why rejected:** That makes the page feel split-brain and encourages duplication. The default user path should be singular.

### Rejected alternative
A page-wide toggle that changes every card’s density at once.

**Why rejected:** Too coarse. It makes the whole page jitter between states instead of revealing depth where needed.

## 4. Hero interpretation specification

### Recommended contents
- lead heading: “Your main result story”
- primary concern title
- co-primary concern presentation only when ambiguity is real
- 2–4 sentence summary
- confidence sentence
- one next-step link/anchor such as “See affected body systems” or “Review supporting biomarkers”

### Hierarchy
- first line: outcome
- second line: explanation
- third line: confidence qualifier
- optional fourth: next step

### Ambiguity handling
If one concern clearly leads:
- show one primary card

If concerns are materially tied:
- show two co-primary concern chips/cards side by side within the same hero block
- never force a fake single winner

This supports the product principle of honest ambiguity.

### Rejected alternative
A huge dashboard-style hero with scores, bars, risk blocks, and many small stats.

**Why rejected:** It dilutes the main story and turns the hero into a summary board rather than an interpretation surface.

## 5. Confidence / data-quality layer specification

### Recommended approach
Turn the current PipelineStatus section into a compact trust strip directly below the hero.

#### Default visible fields
- completeness: Complete / Mostly complete / Partial
- confidence caveat: one sentence
- missing key markers: only if materially important

#### Optional expansion
- confirmatory tests
- lab-range quality specifics
- detailed pass/fail flags

#### Visual weight
- secondary to hero
- always visible
- one card or horizontal strip, not a large standalone block

#### Tone
- plain language
- not “pipeline status”
- not “engine confidence object”
- not engineering vocabulary

#### Recommended labels
- “How complete this picture is”
- “How confident we are”
- “What may be missing”

### Rejected alternative
Hide confidence inside the hero only.

**Why rejected:** Too important to bury, especially for a product that wants to be trustworthy.

### Rejected alternative
Large technical section with pass/fail diagnostics in default mode.

**Why rejected:** Intimidating and unnecessary for most users.

## 6. System / cluster card specification

### Role of this layer
This is the “connected biology” surface. It should feel different from biomarkers.

### Default card contents
- system name
- severity/status badge
- one-line interpretive summary
- confidence or support indicator
- number of contributing biomarkers
- optional “why this matters” link

### Expanded state
- short educational explainer
- contributing biomarkers as linked pills
- recommendations / next areas to inspect
- category tag if useful

### Interpretive vs educational split
#### Interpretive content
- what appears to be happening in this system for this user

#### Educational content
- what this system does biologically
- why this system matters more generally

This distinction should be visible in the expanded state:
- first: “What your results suggest”
- second: “About this system”

### How it differs from biomarker cards
- more narrative
- less numeric
- broader biological meaning
- fewer cards, more importance

### Recommended interaction
Inline expand/collapse within the card.

**Why:** The user is already in a stacked page. Systems are few enough that inline expansion is manageable.

### Rejected alternative
System cards as separate page navigation.

**Why rejected:** Too heavy for the current product maturity and breaks the single-page interpretive flow.

## 7. Biomarker card specification

### Recommended overall model
Keep cards, not tables.

**Why:** The repo is already committed to a card+dial/grid model, and cards are better for progressive disclosure and mixed content than rows in a generic lab table. The current value/range/status structure can stay, but the card needs a much stronger collapsed and expanded anatomy.

### Collapsed state
Every biomarker card should show:
- biomarker name
- latest value + unit
- lab range
- status: high / low / in range
- one short interpretation sentence
- small dial or marker visual
- optional tiny trend sparkline if history exists
- expand chevron/button

The collapsed state should be genuinely scannable.

### Expanded state
When opened, the card reveals:
- educational explainer text
- contribution context if available
- slightly larger trend mini-chart
- related system tags
- optional recommendation or “why this was flagged”

### Missing explainer handling
If educational explainer is absent:
- do not leave a blank panel
- show no educational section at all
- optionally show a muted label such as “Detailed explainer coming soon” only in advanced mode, not default mode

### Historical graph placement
- collapsed: tiny sparkline on the right or bottom edge, only if history exists
- expanded: larger inline trend module beneath the interpretation and above the educational text

### Grid vs table recommendation
Cards in a grid.

#### Desktop
- 3 columns maximum

#### Tablet
- 2 columns

#### Mobile
- 1 column

This aligns with the existing repo structure and avoids a dense spreadsheet feel.

### Interpretation sentence rule
Keep it short:
- one sentence only in collapsed state
- longer narrative belongs in expanded content

### Rejected alternative
Return to a table/list for all biomarkers.

**Why rejected:** Too generic, worse for mixed numeric + explanatory content, and undermines the product’s interpretive feel.

### Rejected alternative
Show full educational text inline on all cards by default.

**Why rejected:** Creates a wall of content and kills scanability.

## 8. Disclosure and interaction model

### Recommended model

#### Hero
No collapse. It is always visible.

#### Confidence strip
Compact by default, optional “more detail” inline expansion.

#### System cards
Inline accordion-style expansion, one or multiple open allowed.

#### Biomarker cards
Single-card expand/collapse inline.

#### Advanced analysis
Bottom-of-page expandable section or segmented area activated by an explicit “Advanced analysis” control.

### Why this mix works
- Systems are few: inline expansion is acceptable.
- Biomarkers are many: each card can expand independently, but the default must stay compact.
- Advanced material is conceptually different: it should be separated as a mode/layer, not mixed into each retail-facing section.

### Rejected alternative
Use drawers or slide-over panels for biomarker detail.

**Why rejected:** Too disruptive for repeated comparison across many biomarkers.

### Rejected alternative
Use hover tooltips heavily.

**Why rejected:** Poor on touch devices and too weak for substantive educational content.

### Rejected alternative
Put everything in tabs.

**Why rejected:** Tabs hide too much structure and make comparison harder on a deep, explanatory page.

## 9. Responsive behaviour

### Desktop
- Hero full width
- Confidence strip full width below hero
- Systems in 2–3 column compact card layout depending on count
- Biomarkers in 3-column grid
- Advanced analysis as full-width section

### Tablet
- Systems in 2 columns
- Biomarkers in 2 columns
- Keep hero and trust strip stacked

### Mobile
- Single-column stack
- Hero simplified
- System cards and biomarker cards full width
- Expanded content must remain inline, not modal-dependent
- Reduce tab density; avoid multi-column tab bars

### Specific repo-driven recommendation
The current insights tab structure is likely too dense for narrow viewports. That advanced area should be simplified or restructured before it is considered part of the final UX.

## 10. Section-by-section changes from current repo reality

### Results header
Keep, but reduce prominence.

### Hero interpretation
Keep and strengthen as the true opening section.

### PipelineStatus
Keep, but compress into a trust strip and rename conceptually away from technical/pipeline language.

### ClusterSummary
Keep, but split interpretive and educational content more clearly. Add system educational explainer when available. Remove fake trend placeholder unless real.

### BiomarkerDials
Keep the card/grid direction, but upgrade card anatomy substantially:
- add expand/collapse
- add educational explainer support
- add contribution context support
- add trend support when real

### Symptom relevance placeholder
Remove from default experience until it is live.

### Overview tab
Demote into advanced analysis or remove if redundant.

### All insights tab
Retain only if it becomes part of advanced mode and is cleaned up for responsiveness.

### Clinician report tab
Retain, but place inside advanced analysis rather than as a peer to the main user path.

### Show technical detail toggle
Replace with a clearer advanced-mode pattern.

## 11. Design decisions locked

- The results experience remains a single stacked page.
- The page hierarchy is: hero → trust → systems → biomarkers → advanced analysis.
- Systems stay above biomarkers.
- Biomarkers remain card-based, not table-based.
- Biomarker detail is progressively disclosed inside each card.
- System cards use inline expansion.
- Confidence/data quality remains visible near the top, but compressed.
- Clinician and technical content move into an explicit advanced layer.
- Symptom relevance placeholder is removed from the default page until real.
- Missing explainer content is handled gracefully by omission, not by empty shells.

## 12. Rejected alternatives

### Generic lab-table-first design
Rejected because it collapses the product back into a standard report viewer.

### Widget dashboard hero
Rejected because it weakens narrative clarity.

### Everything in tabs
Rejected because it obscures structure and increases hiding/showing overhead.

### Drawer-based biomarker detail
Rejected because repeated exploration becomes clumsy.

### Expose technical detail throughout the default page
Rejected because it harms clarity and trust for retail users.

### Equal-weight clinician and retail surfaces
Rejected because it creates duplication and split attention.

## 13. Requires further product decision

- Whether advanced analysis should be an expandable section, a lower-page segmented area, or a dedicated subview.
- Whether biomarker mini-trends should appear only when there are at least 2–3 real historical points.
- Whether educational explainers should include related-system links inside biomarker expansions.
- Whether contribution context is shown in default expanded view or only in advanced mode.
- Whether export JSON remains user-visible or becomes debug/admin only.
- Whether clinician report stays in the retail product surface at all, or becomes role-gated later.

## 14. Ready for implementation

This is ready to convert into a governed frontend implementation package in phases.

Recommended implementation sequence:
1. restructure page hierarchy and remove duplication
2. convert PipelineStatus into trust strip
3. upgrade system cards to support educational explainer content
4. upgrade biomarker cards with collapsed/expanded anatomy
5. add explainer and contribution-context rendering
6. create advanced analysis section and move clinician/technical content there
7. remove placeholder symptom block
8. add trend visual only when backed by real data
