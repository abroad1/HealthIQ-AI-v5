# HealthIQ AI — Results Experience Wireframe Package v1

## Purpose

This document translates the locked results UX architecture into low-fidelity wireframe guidance.

This is not polished visual design.
It is structural.

---

## Page-level wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Results header                                                      │
│ Date / panel summary / quiet actions                                │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ HERO INTERPRETATION                                                 │
│ Main result story                                                   │
│ Primary concern / co-primary concerns if tied                       │
│ 2–4 sentence summary                                                │
│ Confidence sentence                                                 │
│ “See affected systems” anchor                                       │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ TRUST / CONFIDENCE STRIP                                            │
│ Completeness | Confidence | Missing key data                        │
│ [optional more detail]                                              │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ BODY SYSTEMS OVERVIEW                                               │
│ [System card] [System card] [System card]                           │
│ [System card] [System card] [System card]                           │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ BIOMARKER EVIDENCE                                                  │
│ [Biomarker card] [Biomarker card] [Biomarker card]                  │
│ [Biomarker card] [Biomarker card] [Biomarker card]                  │
│ ...                                                                 │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS                                                   │
│ [clinician detail / all insights / technical metadata]              │
│ collapsed by default                                                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 1 — Results header

### Wireframe

```text
┌───────────────────────────────────────────────────────────────┐
│ Your results                                                  │
│ Processed: [date]  |  [x] biomarkers analysed                │
│                                               [Share] [Export]│
└───────────────────────────────────────────────────────────────┘
```

### Notes
- keep compact
- actions are secondary
- no large technical metadata block in default view

---

## Section 2 — Hero interpretation

### Wireframe: single primary concern

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Your main result story                                              │
│                                                                      │
│ Primary concern: [Insulin resistance pattern]                        │
│                                                                      │
│ Your results most strongly suggest a pattern consistent with ...     │
│ This is supported by ...                                             │
│                                                                      │
│ Confidence: This interpretation is reasonably well supported,        │
│ although several helpful markers were not available.                 │
│                                                                      │
│ [See affected body systems ↓]                                        │
└──────────────────────────────────────────────────────────────────────┘
```

### Wireframe: tied co-primary concerns

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Your main result story                                              │
│                                                                      │
│ Two patterns are currently tied for lead relevance:                  │
│ [Concern A]    [Concern B]                                           │
│                                                                      │
│ Your results support both patterns, and the current data does not    │
│ cleanly separate one from the other.                                 │
│                                                                      │
│ Confidence: This is a genuine ambiguity, not an error.               │
│                                                                      │
│ [See affected body systems ↓]                                        │
└──────────────────────────────────────────────────────────────────────┘
```

### Notes
- no score clutter here
- no widget dashboard treatment
- this section should read like the opening paragraph of the whole page

---

## Section 3 — Trust / confidence strip

### Wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ How complete this picture is  |  How confident we are  |  Missing data│
│ Mostly complete               |  Moderate confidence    |  Folate absent│
│                                                      [More detail]    │
└──────────────────────────────────────────────────────────────────────┘
```

### Expanded detail state

```text
┌──────────────────────────────────────────────────────────────────────┐
│ How complete this picture is  |  How confident we are  |  Missing data│
│ Mostly complete               |  Moderate confidence    |  Folate absent│
│                                                                      │
│ Additional detail:                                                    │
│ - Panel completeness explanation                                      │
│ - Confirmatory tests / useful next tests                              │
│ - Lab range caveat where relevant                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### Notes
- stays near the top
- compact by default
- plain language only

---

## Section 4 — Body systems overview

### Collapsed system card wireframe

```text
┌──────────────────────────────┐
│ Vascular / inflammation      │
│ [Elevated]                   │
│                              │
│ Signals suggest pressure on  │
│ vascular health pathways.    │
│                              │
│ Support: 4 biomarkers        │
│ [Expand ▾]                   │
└──────────────────────────────┘
```

### Expanded system card wireframe

```text
┌──────────────────────────────┐
│ Vascular / inflammation      │
│ [Elevated]                   │
│                              │
│ What your results suggest    │
│ Signals suggest pressure on  │
│ vascular health pathways.    │
│                              │
│ About this system            │
│ This system influences ...   │
│                              │
│ Supporting biomarkers        │
│ [Homocysteine] [CRP] [B12]   │
│                              │
│ [Collapse ▴]                 │
└──────────────────────────────┘
```

### Notes
- interpretive content first
- educational content second
- supporting biomarkers visible only when expanded
- remove fake trend unless real

---

## Section 5 — Biomarker evidence grid

### Collapsed biomarker card wireframe

```text
┌──────────────────────────────┐
│ Homocysteine                 │
│ 16.23 µmol/L   [High]        │
│ Range: 3.7–13.9              │
│                              │
│ Short interpretation:        │
│ Higher than expected for     │
│ this lab range.              │
│                              │
│ [small dial / marker visual] │
│ [mini trend if available]    │
│ [Expand ▾]                   │
└──────────────────────────────┘
```

### Expanded biomarker card wireframe

```text
┌──────────────────────────────┐
│ Homocysteine                 │
│ 16.23 µmol/L   [High]        │
│ Range: 3.7–13.9              │
│                              │
│ Short interpretation:        │
│ Higher than expected for     │
│ this lab range.              │
│                              │
│ [small dial / marker visual] │
│ [larger trend module]        │
│                              │
│ What this marker means       │
│ Homocysteine is associated   │
│ with ...                     │
│                              │
│ Why it matters here          │
│ This marker contributes to   │
│ the vascular pattern because │
│ ...                          │
│                              │
│ Related systems              │
│ [Vascular] [Methylation]     │
│                              │
│ [Collapse ▴]                 │
└──────────────────────────────┘
```

### Missing explainer state

```text
┌──────────────────────────────┐
│ Ferritin                     │
│ 88 ng/mL   [In range]        │
│ Range: xx–yy                 │
│                              │
│ Short interpretation:        │
│ Within the reported range.   │
│                              │
│ [small dial / marker visual] │
│ [Expand ▾]                   │
└──────────────────────────────┘
```

Expanded state simply omits the educational block if no explainer is present.

### Notes
- cards remain scannable when collapsed
- interpretation remains one short sentence in collapsed state
- educational depth belongs only in expanded state

---

## Section 6 — Advanced analysis

### Wireframe

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Advanced analysis                                                    │
│ For deeper interpretation, clinician-style detail, and technical     │
│ review.                                                              │
│                                                      [Open ▾]        │
└──────────────────────────────────────────────────────────────────────┘
```

### Open state

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Advanced analysis                                                    │
│                                                                      │
│ [Overview] [All insights] [Clinician detail]                         │
│                                                                      │
│ Detailed content here                                                │
└──────────────────────────────────────────────────────────────────────┘
```

### Notes
- advanced layer exists, but is visually and conceptually separate
- current tabs migrate here rather than competing with the main retail journey

---

## Desktop / tablet / mobile guidance

### Desktop
- systems: 2–3 columns
- biomarkers: 3 columns max
- advanced area full width

### Tablet
- systems: 2 columns
- biomarkers: 2 columns

### Mobile
- single column throughout
- no hover dependencies
- expansions remain inline
- avoid dense tab bars

---

## Locked structural decisions

- single stacked page remains the governing model
- hero opens the narrative
- trust strip sits immediately after hero
- systems come before biomarkers
- biomarker cards remain card-based, not table-based
- system cards and biomarker cards both use inline expansion
- advanced analysis is a separate lower-page layer
- placeholder symptom area is removed from default UX

---

## What this wireframe package is for

This is the bridge between:
- UX architecture
- governed frontend implementation planning

It is now ready to be converted into implementation slices.
