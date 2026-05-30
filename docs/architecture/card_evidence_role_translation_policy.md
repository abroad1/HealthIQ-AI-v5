# Card Evidence Role Translation Policy

**Status:** DRAFT (ARCH-RT-3 pilot)  
**Authority:** ADR-RT-001, ARCH-RT-3

## Purpose

Define how research, package, and PSI role concepts translate into governed **card marker roles** for Health Systems Card subsystem evidence. Card roles describe presentation and evidence participation on the card; they are not scoring-rail instructions.

## Role vocabulary (card surface)

| Card role | Meaning on the card |
|-----------|---------------------|
| `score_contributor` | Marker expected to influence the scored subsystem when present on the panel. |
| `confidence_contributor` | Marker that affects confidence or completeness signalling without being a primary score driver. |
| `contextual_marker` | Supporting context; shown when present but not scored as a primary driver. |
| `mechanism_marker` | Mechanistic context line support (paired with `mechanism_line` when emitted). |
| `differential_marker` | Differential/context branch marker for consumer-safe grouping only. |
| `exclusion_marker` | Marker whose absence or presence gates exclusion messaging (rare on Wave 1 pilot). |
| `missing_for_confidence` | Expected marker whose absence reduces confidence copy, not “not uploaded” clinical absence. |
| `optional_deeper_marker` | Optional depth marker suppressed or deferred per visibility tier. |

## Translation from research / package / PSI

| Upstream concept | Card role mapping rule |
|------------------|------------------------|
| Package `supporting_metrics.role` (e.g. mechanism_marker, contextual_marker) | Map 1:1 where enum exists in card vocabulary; otherwise map to `contextual_marker` and document in compile manifest. |
| PSI promoted roles | **Not used at runtime in ARCH-RT-3.** Translation is compile-time only when PSI-backed compiles are approved later. |
| Scoring rail participation | **Does not auto-set card role.** Rail presence is determined at assembly from panel + rail scores; card role comes from compiled artefact. |
| Investigation spec hypothesis roles | **Out of scope for card evidence pilot.** Root-cause hypothesis roles must not be inferred at card runtime. |

## Scoring rail vs card role

- **Scoring rail:** which biomarkers received values and contribute to domain score rails.  
- **Card role:** how the subsystem card explains each marker’s evidential job.  
- A marker may be on the rail (`included_marker_ids`) while its card role is `contextual_marker`.  
- Frontend and backend must not derive card role from rail membership.

## Contextual vs score contributor

- `score_contributor`: listed as primary evidence for a scored subsystem (`visibility_tier: scored_subsystem`).  
- `contextual_marker`: may appear in included lists but must not be labelled as primary drivers unless backend sets `status_label` from governed fields (pilot: leave `status_label` null).

## Missing-for-confidence vs not uploaded

- **`missing_for_confidence`:** marker expected for subsystem confidence; assembly may list in `missing_marker_ids` with governed labels.  
- **Not uploaded:** presentation label for markers in `missing_marker_ids` when role is not `missing_for_confidence`; Wave 1 UI uses “Not uploaded” only as display text, not clinical inference.  
- **`total_bilirubin` must not appear** as an expected marker when `bilirubin` is canonical (WAVE1-EQUIV1 carry-forward).

## Frontend rules

- Render `marker_role`, `relationship_kind`, `rationale_short`, and `presence_policy` only when provided on DTO marker rows.  
- **Do not infer** clinical role, severity, or diagnosis from `marker_id` or `display_label`.  
- **Do not map** marker name substrings to roles in the UI layer.  
- Optional fields absent → omit role chips; do not substitute defaults.

## Backend rules

- Card roles come only from compiled artefacts via the loader.  
- Assembly partitions included/missing from panel + rail evidence; roles come from artefact markers.  
- Fail closed when artefact validation fails.
