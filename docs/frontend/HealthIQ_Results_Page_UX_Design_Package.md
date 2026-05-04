# HealthIQ Results Wireframe Package

## Status
Aligned to UX / Design Package.
Locked for implementation prompting, subject to final product sign-off.

## Scope
Low-fidelity structural wireframes for the results experience only.
Not polished visual design.

---

## 1. Page-level wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Results Header                                                      │
│ Test date • biomarker count                              Share Export│
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ HERO INTERPRETATION                                                 │
│ [Primary Concern] or [Co-Primary Concerns]                          │
│ Headline line                                                       │
│ Interpretation paragraph                                            │
│ Confidence qualifier line                                           │
│ Next-step cue                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ TRUST STRIP                                                         │
│ Line 1: completeness / confidence summary                           │
│ Line 2: caveat OR missing chapter cue (only when threshold met)     │
│ [More detail]                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ SYSTEM GROUPS                                                       │
│ [Primary Driver group] [System Group] [System Group]                │
│ [System Group]        [System Group] [System Group]                 │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ BIOMARKER EVIDENCE                                                  │
│ [Card] [Card] [Card]                                                │
│ [Card] [Card] [Card]                                                │
│ [Card] [Card] [Card]                                                │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ SHARED BIOMARKER DETAIL PANEL (desktop/tablet when a card selected) │
│ Biomarker title                                                     │
│ Educational explainer                                               │
│ Contribution context                                                │
│ Trend module (only if real history exists; otherwise omitted)       │
│ Related System Groups                                               │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS [expand]                                          │
│ Clinician report / insights / confirmatory detail / technical meta  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Hero wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ HERO                                                                │
│ [Primary Concern Badge]                                              │
│ or                                                                   │
│ [Co-Primary Concern A] [Co-Primary Concern B]                        │
│                                                                      │
│ Headline line                                                        │
│ Interpretation paragraph (single short paragraph only)               │
│ Confidence qualifier line                                            │
│ Next-step cue                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

### Hero copy discipline
Locked structure:
- 1 headline line
- 1 interpretation paragraph
- 1 confidence qualifier line
- 1 next-step cue max

---

## 3. Trust Strip wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ TRUST STRIP                                                         │
│ Complete enough for a strong first view                             │
│ Folate missing may limit confidence in the lead story               │
│                                                     [More detail]    │
└──────────────────────────────────────────────────────────────────────┘
```

### Default rule
Maximum 2 visible lines by default.
Everything else goes behind reveal.

### Reveal content may include
- expanded confidence explanation
- confirmatory note
- missing chapter explanation

---

## 4. System Groups wireframe

```text
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ SYSTEM GROUP                 │  │ SYSTEM GROUP                 │
│ Metabolic Group              │  │ Vascular Group               │
│ [Primary Driver] [High]      │  │ [Moderate]                   │
│ Short interpretive summary   │  │ Short interpretive summary   │
│ 4 biomarkers contributing    │  │ 3 biomarkers contributing    │
│ [Expand]                     │  │ [Expand]                     │
└──────────────────────────────┘  └──────────────────────────────┘
```

### Expanded state
```text
┌──────────────────────────────────────────────────────────────────────┐
│ SYSTEM GROUP EXPANDED                                               │
│ What your results suggest                                           │
│ Short educational explainer (only if present)                       │
│ Contributing biomarkers: [HbA1c] [Triglycerides] [HDL]              │
│ Recommendations / next inspection prompt                            │
└──────────────────────────────────────────────────────────────────────┘
```

### Fallback rule
If educational explainer absent:
- expanded state remains interpretive only
- no empty educational shell

---

## 5. Biomarker grid wireframe

```text
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ HOMOCYSTEINE         │ │ B12                  │ │ FOLATE               │
│ 16.2 µmol/L          │ │ 280 pmol/L           │ │ Not tested           │
│ Range 3.7–13.9       │ │ Range ...            │ │                      │
│ High                 │ │ In range             │ │ Missing chapter cue? │
│ Short interpretation │ │ Short interpretation │ │ if threshold met      │
│ [mini gauge] [open]  │ │ [mini gauge] [open]  │ │ [muted state] [open] │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

### Default card anatomy
- biomarker name
- latest result + unit
- lab range
- direction/status
- short interpretation
- mini gauge/marker
- expand control
- tiny trend cue only if real history exists
- no stub trend icon, empty chart frame, or visual promise of history when the contract is absent

---

## 6. Shared biomarker detail panel wireframe

### Desktop / tablet

```text
┌──────────────────────────────────────────────────────────────────────┐
│ BIOMARKER DETAIL PANEL                                              │
│ Homocysteine                                                        │
│                                                                      │
│ Educational explainer                                               │
│ What this biomarker is and why it matters biologically              │
│                                                                      │
│ Contribution context                                                │
│ How this biomarker contributes to the current System Group / Hero   │
│                                                                      │
│ Trend module (only if real history exists; otherwise omitted)       │
│ [sparkline / compact chart]                                         │
│                                                                      │
│ Related System Groups                                               │
│ [Vascular Group] [Methylation Group]                                │
└──────────────────────────────────────────────────────────────────────┘
```

### Mobile
Selected card opens detail inline beneath itself rather than into a shared lower panel.

### Content-layer order lock
Expanded biomarker detail must preserve separate rendering zones for:
1. educational explainer
2. contribution context
3. trend module

Do not merge these into one text block.

---

## 7. Missing Chapter wireframe

### Trigger rule
A Missing Chapter cue appears only if the missing marker affects:
- the Hero concern
- the Primary Driver System Group
- or a confidence downgrade already present in the Trust Strip

### Example treatment
```text
┌──────────────────────────────────────────────────────────────────────┐
│ TRUST STRIP REVEAL / CONTEXTUAL CUE                                 │
│ Missing chapter: Folate was not tested.                             │
│ This matters because it limits confidence in the lead vascular      │
│ methylation story.                                                  │
└──────────────────────────────────────────────────────────────────────┘
```

This is not a general sales card.
It is a contextual completeness cue.

---

## 8. Advanced Analysis wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS                                      [Expand]      │
└──────────────────────────────────────────────────────────────────────┘

When expanded:

┌──────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS                                                   │
│ [Clinician Report] [All Insights] [Technical Detail]                │
│                                                                      │
│ Selected advanced panel content                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### Interaction lock
Advanced Analysis is:
- a lower-page expandable section
- inside the same stacked page

It is not:
- a separate page
- a dedicated subview

---

## 9. Responsive behaviour wireframe notes

### Desktop
- Hero full width
- Trust Strip full width
- System Groups in 2–3 column layout
- Biomarker cards in 3-column grid
- Shared biomarker detail panel below grid

### Tablet
- System Groups in 2 columns
- Biomarkers in 2 columns
- Shared biomarker detail panel below grid

### Mobile
- single-column stack
- System Groups full width
- Biomarkers full width
- biomarker detail opens inline beneath selected card
- no reliance on hover

---

## 10. Graceful fallback rules

Formal implementation fallback rules:
- if biomarker explainer absent: omit cleanly
- if contribution context absent: omit cleanly
- if system explainer absent: keep System Group card interpretive only
- if no history exists: omit trend module
- if no co-primary concern exists: use single-lead Hero layout only
- if Missing Chapter threshold not met: omit Missing Chapter entirely

No empty shells.
No placeholder content in the default retail flow.

---

## 11. Locked decisions carried into implementation

- User-facing term is **System Groups**
- Hero copy structure is locked
- Trust Strip is capped to 2 visible lines by default
- Primary Driver visual thread is required
- Biomarker detail uses shared panel on desktop/tablet and inline on mobile
- Advanced Analysis is lower-page expandable section
- Interpretation / education / contribution-context remain separate rendered layers
- Missing Chapter uses threshold-based triggering only
- Partial content coverage must degrade cleanly


---

## Controlled amendment — trend/history dependency note

These wireframes remain valid.

### Trend module clarification

Where the wireframes show a biomarker trend/history area in the expanded biomarker experience, that area remains part of the intended frontend design.

It should be interpreted as a **reserved component slot** pending backend/platform support for reliable biomarker history retrieval.

### Implementation note

The frontend build may:

- scaffold the trend container and spacing
- keep the expanded biomarker layout ready for trend content
- defer live chart rendering until the history contract is available

### Dependency statement

Production activation of the trend/history module requires backend/platform support for:

- prior values for the same biomarker for the same user
- associated dates
- stable matching across analyses/tests
- preferably prior range/lab context where available

This is a dependency flag, not a change in design direction.


Trend/history layout is in scope architecturally, but live rendering is excluded from the first implementation sprint until the backend history contract is available.
