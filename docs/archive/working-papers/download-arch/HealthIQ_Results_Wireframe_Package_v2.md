# HealthIQ AI — Results Wireframe Package

**Version:** v2  
**Date:** April 2026  
**Status:** Low-fidelity wireframe package for implementation planning  
**Scope:** Results experience only

---

## 1. Purpose

This document provides low-fidelity wireframes and structural guidance for the HealthIQ AI results experience.

It is derived from the locked results-page UX package and is intended to bridge UX architecture into implementation planning.

This version incorporates three key refinements:
- Hero-to-primary-System visual threading
- stable biomarker expansion behaviour
- missing-chapter treatment for materially absent markers

---

## 2. Page-Level Wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ RESULTS HEADER                                                              │
│ Report date • Biomarker count                            Share • Export      │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ HERO INTERPRETATION                                                         │
│ Main result story                                                           │
│                                                                              │
│ [Primary concern]   or   [Co-primary concern A] [Co-primary concern B]      │
│                                                                              │
│ 2–4 sentence lead interpretation                                            │
│ Confidence qualifier                                                        │
│ See the main System Groups involved ↓                                       │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ TRUST STRIP                                                                 │
│ Completeness: Mostly complete                                               │
│ Confidence: Good, but limited by missing folate                             │
│ Missing chapter: Folate helps complete this vascular/methylation story      │
│ [More detail]                                                               │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ SYSTEM GROUPS                                                               │
│                                                                              │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐   │
│ │ PRIMARY DRIVER       │ │ SYSTEM GROUP         │ │ SYSTEM GROUP         │   │
│ │ Metabolic Group      │ │ Vascular Group       │ │ Thyroid Group        │   │
│ │ Short interpretation │ │ Short interpretation │ │ Short interpretation │   │
│ │ Support/confidence   │ │ Support/confidence   │ │ Support/confidence   │   │
│ │ Biomarkers: 4        │ │ Biomarkers: 3        │ │ Biomarkers: 2        │   │
│ │ [Expand]             │ │ [Expand]             │ │ [Expand]             │   │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ BIOMARKER EVIDENCE                                                          │
│                                                                              │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐   │
│ │ Homocysteine         │ │ B12                  │ │ Folate               │   │
│ │ 16.23 µmol/L         │ │ 245 pmol/L           │ │ Not tested           │   │
│ │ Range 3.7–13.9       │ │ Range ...            │ │ Missing chapter      │   │
│ │ High                 │ │ Low-normal           │ │ Why it matters ↓     │   │
│ │ Short interpretation │ │ Short interpretation │ │                      │   │
│ │ [Expand]             │ │ [Expand]             │ │ [Expand]             │   │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘   │
│                                                                              │
│ [Selected biomarker expands into controlled full-width detail row below]    │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS                                                           │
│ [Open advanced analysis]                                                    │
│  - Clinician report                                                         │
│  - Detailed insights                                                        │
│  - Confirmatory detail                                                      │
│  - Technical metadata                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Hero Wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ MAIN RESULT STORY                                                           │
│                                                                              │
│ [Primary concern badge]                                                     │
│ or                                                                           │
│ [Co-primary concern A] [Co-primary concern B]                               │
│                                                                              │
│ Your results most strongly suggest a vascular / methylation stress pattern  │
│ driven by elevated homocysteine with incomplete supporting context.         │
│                                                                              │
│ We are reasonably confident in this pattern, but folate was not tested,     │
│ which limits how complete this story is.                                    │
│                                                                              │
│ → See the Primary Driver in System Groups                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Notes
- no dashboard clutter in the Hero
- confidence remains visible but subordinate to the interpretation
- Hero should visually connect to the matching System Group card below

---

## 4. Trust Strip Wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ HOW COMPLETE THIS PICTURE IS                                                │
│                                                                              │
│ Completeness      Mostly complete                                           │
│ Confidence        Good, with one important gap                              │
│ Missing chapter   Folate was not tested and helps explain this pattern      │
│                                                                              │
│ [More detail]                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Notes
- compact and always visible
- missing-data line should only appear when it materially affects the story
- this section must not read like a technical QA panel

---

## 5. System Group Card Wireframe

### 5.1 Collapsed

```text
┌──────────────────────────────┐
│ PRIMARY DRIVER               │
│ Vascular / Methylation Group │
│                              │
│ Elevated waste-handling      │
│ pressure with incomplete     │
│ methylation support context  │
│                              │
│ Support: High                │
│ Biomarkers: 4                │
│ [Expand]                     │
└──────────────────────────────┘
```

### 5.2 Expanded

```text
┌────────────────────────────────────────────────────────────────────┐
│ PRIMARY DRIVER — Vascular / Methylation Group                     │
│                                                                    │
│ What your results suggest                                          │
│ Elevated homocysteine suggests increased vascular stress and an    │
│ incomplete methylation clearance picture.                          │
│                                                                    │
│ About this system                                                  │
│ This group relates to how the body recycles and clears compounds   │
│ that can affect vascular integrity and inflammatory burden.        │
│                                                                    │
│ Supporting biomarkers                                              │
│ [Homocysteine] [B12] [Folate missing] [MCV not tested]            │
│                                                                    │
│ [Collapse]                                                         │
└────────────────────────────────────────────────────────────────────┘
```

### Notes
- interpretive and educational content must be visibly separated
- the Primary Driver card must be visually anchored to the Hero

---

## 6. Biomarker Card Wireframe

### 6.1 Collapsed

```text
┌──────────────────────────────┐
│ Homocysteine                 │
│ 16.23 µmol/L                 │
│ Range 3.7–13.9               │
│ High                         │
│                              │
│ Elevated above lab range and │
│ supportive of the lead story │
│                              │
│ (dial visual)   (trend cue)  │
│ [Expand]                     │
└──────────────────────────────┘
```

### 6.2 Expanded — controlled breakout row

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ HOMOCYSTEINE                                                                │
│ 16.23 µmol/L • High • Range 3.7–13.9                                        │
│                                                                              │
│ Short interpretation                                                         │
│ Elevated above lab range and supportive of the lead vascular/methylation     │
│ pattern.                                                                     │
│                                                                              │
│ Trend                                                                        │
│ [larger inline sparkline / micro-chart if real history exists]               │
│                                                                              │
│ Educational explainer                                                        │
│ Homocysteine is a metabolic waste product that is usually recycled through   │
│ vitamin-dependent pathways. When this picture is incomplete or stressed,     │
│ levels may rise.                                                             │
│                                                                              │
│ Contribution context                                                         │
│ This marker contributes directly to the current primary system-group story.   │
│                                                                              │
│ Related System Groups                                                        │
│ [Vascular / Methylation Group]                                               │
│                                                                              │
│ [Collapse]                                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Notes
- expansion should not stretch one cell inside a 3-column grid awkwardly
- selected card detail should appear as a stable controlled row
- no empty educational panel when explainer content is absent

---

## 7. Missing Chapter Card / Cue Wireframe

This is the recommended treatment when a missing marker materially affects the story.

```text
┌──────────────────────────────┐
│ Folate                       │
│ Not tested                   │
│ Missing chapter              │
│                              │
│ This marker helps complete   │
│ the methylation side of this │
│ vascular story               │
│                              │
│ [Why it matters]             │
└──────────────────────────────┘
```

Expanded:

```text
┌────────────────────────────────────────────────────────────────────┐
│ FOLATE — MISSING CHAPTER                                          │
│                                                                    │
│ Folate was not included in this panel.                             │
│                                                                    │
│ Why it matters                                                     │
│ Folate helps interpret whether elevated homocysteine reflects an   │
│ incomplete methylation support picture rather than a more isolated │
│ signal.                                                            │
│                                                                    │
│ This does not invalidate the current story, but it makes it less   │
│ complete.                                                          │
│                                                                    │
│ [Collapse]                                                         │
└────────────────────────────────────────────────────────────────────┘
```

### Notes
- this should feel clinically meaningful, not commercial
- later product versions may choose to connect this to retesting flows

---

## 8. Advanced Analysis Wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ADVANCED ANALYSIS                                                           │
│ For deeper clinical and technical detail                                    │
│                                                                              │
│ [Clinician report] [Detailed insights] [Confirmatory detail] [Technical]    │
│                                                                              │
│ Content shown only after explicit open                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Notes
- this is not part of the default retail reading flow
- no need to surface it as equal-weight top-level navigation

---

## 9. Responsive Guidance

### Desktop
- Hero full width
- Trust Strip full width
- System Groups up to 3 across
- biomarker cards up to 3 across
- breakout detail row spans full content width

### Tablet
- System Groups 2 across
- biomarker cards 2 across
- breakout detail remains full section width

### Mobile
- single column
- expanded biomarker detail appears inline beneath the selected card
- avoid dense tab treatment in advanced layer

---

## 10. Wireframe Decisions Locked

1. Hero must connect visually to the matching primary System Group.  
2. System Groups are the middle layer between Hero and biomarkers.  
3. Biomarker cards remain grid-based in collapsed view.  
4. Expanded biomarker detail must use a stable pattern, not naïve cell growth.  
5. Missing-data can appear as a Missing Chapter cue where biologically relevant.  
6. Advanced analysis is explicitly separated from the default journey.

---

## 11. Open Implementation Choices

These are still valid implementation choices within the locked wireframe direction:

1. breakout biomarker detail row vs single shared detail panel  
2. exact visual treatment of the Primary Driver badge/state  
3. exact copy style for Missing Chapter cues  
4. whether Advanced Analysis is accordion-like or segmented lower-page navigation

---

## 12. Summary

The wireframe direction is now:
- interpret first
- connect that interpretation to System Groups
- support it with biomarker evidence
- reveal deeper information on demand

The three most important v2 refinements are:
- visible Hero-to-System continuity
- biomarker expansion without layout jank
- missing-data presented as meaningful incompleteness where relevant

