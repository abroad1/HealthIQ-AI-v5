# HealthIQ AI — IDL Naming Decision Note

**Status:** Approved  
**Date:** 2026-04-16  
**Owner:** CEO / Product Strategy Authority

## Purpose

This note records the approved naming and governance decision for the Interpretation Display Layer (IDL), so that implementation can proceed without further ambiguity.

## Decision

HealthIQ approves the current conservative retail naming posture for the Interpretation Display Layer.

This means:

- the IDL architecture is approved
- the current retail interpretation layer will use the medically stricter mixed classification model
- phenotype remains a strategic, GTM, and B2B methodology term
- the current retail surface will not force broad phenotype language across all interpretation cards
- the current naming posture is approved for now, but remains revisable later through the governed IDL

## Architectural position

HealthIQ has not built the wrong Layer B system.

The underlying architecture remains valid:

- Layer A = canonicalisation / SSOT
- Layer B = governed medical interpretation and reasoning
- Layer C = presentation / translation

The issue addressed by BE-IDL-1 was not a failure of the medical reasoning architecture.
It was a governance gap between Layer B and Layer C.

The IDL now exists to govern how interpretation entities are classified, named, and surfaced.

## Naming and classification rule

The current interpretation set is treated as a governed mixed set, not as a blanket “all phenotype” set.

The approved classification model remains:

- phenotype
- risk_construct
- organ_pattern
- syndrome_state

This model is now the authority for retail interpretation surfacing.

## Reversibility rule

This decision is intentionally reversible at the naming layer.

HealthIQ may later:

- rename existing entities
- reclassify existing entities
- allow broader phenotype usage on the retail surface
- add new interpretation entities

These changes must be made through the governed IDL authority layer.

They must not require a rebuild of the underlying Layer B reasoning architecture.

## Implementation consequence

BE-IDL-1 is approved as complete and ready for merge/push.

The next sprint may proceed as:

**FE-R8 — Section 5 rendering against the approved IDL**

## Document authority consequence

The Interpretation Display Layer Design Lock should now be updated from:

**Proposed**

to:

**Approved**

so that there is no ambiguity for future implementation.

## Final statement

HealthIQ is approving the current IDL naming posture as the correct implementation position for now, while explicitly preserving the ability to evolve naming and classification later in response to medical, product, or market needs.