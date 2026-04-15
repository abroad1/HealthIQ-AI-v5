# HealthIQ AI — Strategy Stack and Document Authority Map

## Purpose

This note defines how HealthIQ’s main strategic papers should relate to each other.

The goal is to keep each document separate and useful, while preventing contradiction, duplication, and drift.

This is not a new strategy paper.
It is a short governance note that explains:

- which document is authoritative for which topic
- how the documents relate
- which document wins if there is a conflict
- which major decisions should be tracked across the whole strategy stack

---

## 1. Recommended approach

HealthIQ should **keep the strategic papers separate**, but manage them as a **single strategy stack**.

Do **not** merge them into one large master document.

Why:

- each paper solves a different problem
- each paper will evolve at a different speed
- merging them would make the system harder to maintain
- but leaving them unconnected would create contradictions

So the right model is:

**separate authority documents, linked by a clear hierarchy and decision framework**

---

## 2. Current strategy stack

### Document A — 12-Month Strategic Plan
**Role:** Master strategic direction document

**Authoritative for:**
- overall company/product direction
- phase structure
- platform sequencing
- Phase 1 / Phase 2 / Phase 3 intent
- major strategic bets
- high-level roadmap priorities
- dependency ordering between workstreams

**Should not own in detail:**
- exact results-page architecture
- detailed asset-to-UX surfacing rules
- detailed phenotype taxonomy/naming model
- section-level frontend content design

---

### Document B — Final Results Journey Recommendation Paper
**Role:** Results experience and frontend interpretation authority

**Authoritative for:**
- target results-page journey
- section ordering
- what the user should see and when
- asset-to-UX surfacing logic
- deterministic narrative spine for the frontend
- section-level fallback principles
- how biomarkers, reassurance, uncertainty, and clinician handoff should be positioned

**Should not own in detail:**
- company-wide phase sequencing
- full commercial screening expansion strategy
- enterprise go-to-market prioritisation
- broad phenotype market positioning

---

### Document C — Phenotype / Commercial Expansion Research
**Role:** Future interpretation expansion and commercial prioritisation authority

**Authoritative for:**
- which future interpretation domains are commercially valuable
- which classes are best framed as phenotype / risk construct / syndrome-state / organ-pattern
- Phase 2 / Phase 3 expansion priorities for interpretation coverage
- alignment with preventive health / population screening / insurer / employer opportunities
- interpretation taxonomy direction

**Should not own in detail:**
- current results-page UX architecture
- section-by-section frontend design
- full company roadmap structure
- immediate UI implementation choices

---

## 3. How the documents relate

The documents should be read in this order:

### 1. Strategic Plan
Answers:
- where the company is going
- what phases matter
- what the major platform priorities are

### 2. Results Journey Paper
Answers:
- how the user should experience HealthIQ’s intelligence
- how governed assets should be surfaced in the product

### 3. Phenotype / Commercial Expansion Research
Answers:
- which future interpretation classes are worth building next
- how future expansion aligns to real commercial opportunity

In simple terms:

- the **Strategic Plan** sets the destination
- the **Results Journey Paper** defines the user experience architecture
- the **Phenotype / Commercial Paper** defines future interpretation expansion priorities

---

## 4. Precedence rules

If two documents appear to conflict, use these precedence rules.

### A. Company/platform sequencing conflicts
**Winner:** 12-Month Strategic Plan

Examples:
- what belongs in Phase 1 vs Phase 2
- whether a workstream is core or secondary
- strategic ordering of platform investments

---

### B. Results experience / frontend interpretation conflicts
**Winner:** Final Results Journey Recommendation Paper

Examples:
- section order
- what appears before biomarkers
- how reassurance is positioned
- where uncertainty belongs
- whether biomarkers are primary or secondary in the journey

---

### C. Future interpretation expansion / taxonomy / commercial prioritisation conflicts
**Winner:** Phenotype / Commercial Expansion Research

Examples:
- which future domains are commercially important
- whether something is best framed as phenotype, risk, state, or organ-pattern
- which future interpretation groups deserve Phase 2 / Phase 3 investment

---

## 5. Operating rule for overlap

If a document needs to mention a topic owned by another document:

- include only the short summary needed for context
- do not restate the full logic
- point back to the authority document

Example:
- the Strategic Plan may mention that the results experience will follow the recommended reasoning journey
- but it should not duplicate the full section-by-section UX architecture from the Results Journey Paper

This keeps the stack aligned without duplication.

---

## 6. Proposed cross-stack decision register

HealthIQ should maintain a short decision register containing the most important cross-document decisions.

These are decisions that affect multiple papers and therefore must remain consistent everywhere.

### Recommended initial decision register

1. **HealthIQ is a guided reasoning journey, not a better lab report**
2. **Deterministic assets are the narrative spine**
3. **Biomarkers do not lead the experience, but remain a premium evidence layer**
4. **Balanced / reassuring interpretation is first-class**
5. **The lead finding must be explained, not merely stated**
6. **Uncertainty and why-the-lead-won must be visible and user-readable**
7. **Signal-library explanation assets should be compiler-mediated, not surfaced raw**
8. **Gemini is optional polish, not the core reasoning authority**
9. **Phenotype is a strategic umbrella term, but not every governed interpretation entity should be called a phenotype**
10. **Future interpretation expansion should prioritise cardiometabolic prevention and population-screening value**
11. **Section 5 / pattern-layer implementation is gated behind an existence check**
12. **Clinician handoff remains distinct from the retail journey**

This register should be short and stable.

---

## 7. Suggested maintenance model

### The Strategic Plan should be updated when:
- company direction changes
- phase sequencing changes
- platform priorities change
- major new workstreams are added or removed

### The Results Journey Paper should be updated when:
- the target results-page architecture changes
- section sequencing changes
- new governed assets become available for surfacing
- UX authority decisions change

### The Phenotype / Commercial Paper should be updated when:
- new interpretation domains are researched
- commercial priorities change
- population-screening strategy sharpens
- taxonomy decisions evolve

### The Strategy Stack note should be updated when:
- a new authority paper is added
- precedence rules change
- the decision register materially changes

---

## 8. Recommended practical next step

Save this note alongside the other strategic papers and treat it as the index/governance layer for the strategy stack.

Then ensure each existing paper contains a short header note stating its authority scope.

Suggested header example:

**Authority scope:**  
This document is authoritative for [X].  
If this document conflicts with [Y] on [topic], [Y] takes precedence.

That small change will make the whole strategy stack much easier to govern.

---

## 9. Final recommendation

HealthIQ should not run its strategy through one giant document.

It should run its strategy through:

- a master strategic plan
- a results experience authority paper
- a phenotype / commercial expansion authority paper
- and this short strategy-stack governance note

That will give the company:

- clarity
- maintainability
- less duplication
- less contradiction
- stronger decision discipline
- easier future updates

**Recommended principle: separate papers, one coherent strategy system.**
