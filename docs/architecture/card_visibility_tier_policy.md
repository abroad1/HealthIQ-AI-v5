# Card Visibility Tier Policy

**Status:** DRAFT (ARCH-RT-3 pilot)  
**Authority:** ADR-RT-001, ARCH-RT-3

## Purpose

Control which subsystem evidence blocks appear on Wave 1 Health Systems Cards and how thin evidence is presented during estate rollout.

## Tiers

| Tier | Consumer behaviour |
|------|-------------------|
| `scored_subsystem` | Subsystem block is eligible for main card evidence section when backend emits `subsystems` rows. Primary pilot tier. |
| `contextual_evidence` | Subsystem may render as secondary/context-only block; score chip de-emphasised or omitted per frontend contract. |
| `hidden_v1` | Subsystem compiled for provenance but **not shown** in Wave 1 UI; backend may omit from DTO or frontend suppresses by tier. |

## Medical review control

- Visibility tier is set at **compile time** in the card evidence artefact.  
- Medical review gates promotion from `hidden_v1` → `contextual_evidence` → `scored_subsystem`.  
- Runtime must not upgrade tier without a new compiled artefact.

## Thin evidence handling

- When `included_marker_ids` is empty and tier is `scored_subsystem`, existing Wave 1 zero/partial evidence UX applies (no new inference).  
- When tier is `contextual_evidence`, prefer showing mechanism/context lines only if backend emitted `mechanism_line` / marker rows.  
- When tier is `hidden_v1`, frontend must not render the subsystem block.

## Full estate regeneration (future)

- Each subsystem receives a compiled artefact with an explicit tier.  
- Batch compile must not default all subsystems to `scored_subsystem`.  
- Estate index should list tier + artefact path for audit.

## ARCH-RT-3 pilot

- Pilot subsystem `wave1_met_glycaemic_control` uses `scored_subsystem`.  
- Non-pilot subsystems remain on legacy hard-coded path until individually compiled.
