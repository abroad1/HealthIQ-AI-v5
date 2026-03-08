# ADR-003 — Knowledge Bus Evidence Architecture

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-08 |
| **Authority** | Knowledge Bus SOP v1.2; Claude Translation Specification v1 |
| **Supersedes** | — |
| **Superseded by** | — |

---

## Context

Clinical thresholds and signal definitions must be anchored to published research
evidence. Without a formal mechanism to translate research into platform logic, two
failure modes occur:

1. **Threshold drift** — thresholds are set by convention, assumption, or convenience
   rather than evidence, and the evidence basis is lost over time
2. **Implementation divergence** — research findings are correctly understood but
   incorrectly implemented because there is no structured translation layer

The Knowledge Bus solves this by creating a formal, validated, version-controlled
bridge between published research and executable platform logic. Every signal threshold
in the platform must trace back to a specific study, a specific population, and a
specific evidence class.

---

## Decision

All disease-specific signal definitions and thresholds must be introduced through the
Knowledge Bus pipeline. No signal threshold may be added to the platform by any other
route.

---

## The Knowledge Bus Pipeline

```
Research Report (.md)
        ↓
Claude Translation Engine
(Research-to-Knowledge Translation Specification v1)
        ↓
Knowledge Bus Package (KB Package)
  ├── package_manifest.yaml    — package identity and metadata
  ├── research_brief.yaml      — evidence sources and biomarker list
  ├── signal_library.yaml      — signal definitions and thresholds
  └── clinical_signoff.md      — pending decisions and reviewer sign-off
        ↓
KB Validator (validate_knowledge_package.py)
        ↓
Clinical Sign-Off (human reviewer)
        ↓
Layer B Implementation (KB-S9, KB-S10)
```

---

## Package Structure Invariants

### package_manifest.yaml
- `package_id` format: `pkg_[a-z0-9_]+`
- `translation_mode`: either `confirmation` (existing signal validated) or
  `creation` (new signal or materially different thresholds)

### research_brief.yaml
- All `derived_metrics` entries use plain names without prefix (`tyg_index`, not
  `derived.tyg_index`) — pattern `^[a-z0-9_]+$`
- All cited sources must include journal, year, and key finding
- `evidence_strength` must be stated: `strong` / `moderate` / `weak`

### signal_library.yaml
- `library.package_id` format: `KBP-\d{4}`
- All `derived_metrics` in dependencies use `derived.` prefix (`derived.tyg_index`)
- Thresholds must state the evidence source in their description
- Override rules must be escalation-only (see ADR-004)

### clinical_signoff.md
- Status must be `PENDING REVIEW` until a named clinical reviewer completes sign-off
- All unresolved design decisions must be listed explicitly as numbered decisions
- No package may be promoted to Layer B implementation without a completed sign-off

---

## Translation Rules (Standing — confirmed 2026-03-08)

These rules apply to every KB package translation, without exception:

1. **Follow research conclusions to the letter.** Use the threshold the paper states
   for the disease being studied. Do not substitute a threshold from a different
   condition, a different guideline's general classification, or an architectural
   preference.

2. **The threshold belongs to the signal, not the biomarker.** The same biomarker
   may carry different thresholds in different signals because each signal targets a
   specific disease type. A threshold appropriate for one signal may be incorrect for
   another — both can be simultaneously correct.

3. **Do not extrapolate across populations.** If a threshold was derived in a specific
   population (e.g., statin-treated patients, East Asian cohorts), state that limitation
   explicitly. Do not apply the threshold universally unless the research does so.

4. **Do not invent thresholds.** If the literature does not support a specific cut-off,
   state "threshold evidence inconclusive — additional validation required."

5. **When ambiguous, raise a Decision in `clinical_signoff.md`.** Do not resolve
   clinical ambiguity silently with a judgment call.

---

## Architectural Invariants

1. **Knowledge Bus is the only route for signal thresholds.** No threshold value may
   be added to `ratio_registry.py`, `insight_graph_builder.py`, or any other platform
   file without first being defined in a validated and signed-off KB package.

2. **Validator must pass before implementation.** `validate_knowledge_package.py` must
   return `ready_for_implementation: True` before any KB-derived logic is written to
   `backend/core/`.

3. **Clinical sign-off is mandatory before Layer B.** A KB package with
   `PENDING REVIEW` status in `clinical_signoff.md` must not be promoted to Layer B
   implementation. All numbered decisions must be resolved.

4. **Package IDs are permanent and sequential.** `KBP-0001`, `KBP-0002`, etc. are
   assigned in order and never reused. A deprecated package retains its ID and is
   marked deprecated in its manifest.

5. **Translation mode must be declared.** Every package must declare whether it is
   `confirmation` (validating an existing signal) or `creation` (introducing a new
   design). Creation mode packages require explicit sign-off on the threshold delta
   against any existing signal with the same `signal_id`.

---

## Consequences

- All future signal work begins with a research report reviewed against the translation
  rules above
- The validator must be run on every package before commit
- KB-S9 implements derived metrics identified by KB packages; KB-S10 wires the
  Signal Evaluation Engine to consume them
- `KBP-0001` through `KBP-0005` are the initial validated packages; studies 5–10
  from `study_topics_metabolic_core.md` will yield further packages

---

## Current Package Registry

| Package | Signal | Mode | Status |
|---------|--------|------|--------|
| KBP-0001 | Multiple signals (legacy) | — | Superseded by KBP-0002 through KBP-0005 where conflicts exist |
| KBP-0002 | `signal_insulin_resistance` | Confirmation | Awaiting clinical sign-off |
| KBP-0003 | `signal_lipid_transport_dysfunction` | Creation | Awaiting clinical sign-off |
| KBP-0004 | `signal_hepatic_metabolic_stress` | Creation | Awaiting clinical sign-off |
| KBP-0005 | `signal_systemic_inflammation` | Creation | Awaiting clinical sign-off |

---

## Source Documents

- `docs/KNOWLEDGE_BUS_SOP_v1.2.md` — Knowledge Bus governance
- `docs/CLAUDE_TRANSLATION_SPEC_v1.md` — translation specification
- `docs/RESEARCH_KNOWLEDGE_PIPELINE_v1.md` — pipeline overview
- `knowledge_bus/research/RESEARCH_PROMPT_TEMPLATE.md` — research LLM prompt template
