# HealthIQ — Phase 1 Launch Sprint Plan

## Purpose

This document captures the agreed Phase 1 launch plan for HealthIQ so that sprint sequencing, operational scoping, and GTM execution remain aligned.

It is intended to stop planning drift and provide a durable source of truth for the final launch work required after the major product-building lineages have been completed.

This plan is based on:
- the agreed Phase 1 launch posture
- the completed frontend and backend product lineages
- the FE-LAUNCH-INTEGRATION preflight and follow-on implementation
- the OPS-S1 preflight
- the agreed GTM clarification that B2C is a deliberate wedge, not the long-term end state

---

## 1. Phase 1 launch posture

### Agreed launch posture

HealthIQ Phase 1 should launch as a:

- **UK-only**
- **B2C-primary**
- **post-test blood interpretation product**
- for users who already have a tested blood panel

### B2C user groups at launch

Phase 1 B2C has **two meaningful user groups**:

1. **Standard retail user**
   - wants clarity
   - wants understandable interpretation
   - wants help knowing what matters
   - may want something credible to take to a clinician

2. **Technical / biohacker user**
   - wants more depth
   - wants more systems-level interpretation
   - wants more biomarker granularity and logic
   - stress-tests the intelligence and sophistication of the product

### Economic model

- **Primary launch buyer:** the retail user
- **Primary launch operating model:** B2C
- **Long-term economic centre of gravity:** B2B / B2B2C
- **Role of B2C:** deliberate wedge / proof engine, not the final business model

### Secondary distribution channel

A key strategic part of the B2C wedge is the **downloadable clinician report**.

This means the launch model is not just:
- consumer interpretation

It is also:
- **clinician exposure without direct clinician acquisition**

Users can carry a clinician-grade report into real-world clinical conversations, allowing HealthIQ to:
- test whether the output earns trust
- create indirect clinician exposure
- gather evidence useful for later practitioner, lab, insurer, or B2B conversations

---

## 2. Planning assumptions

This sprint plan assumes:

- the current product shell, results experience, account surfaces, narrative presentation, and launch integration work are materially complete
- the deterministic analytical core remains the product truth layer
- narrative remains a companion translation layer, not a reasoning layer
- Phase 1 does **not** require:
  - US-first launch
  - multi-market launch
  - HIPAA-led posture as the default launch baseline
  - SOC 2 or ISO 27001 as a hard launch dependency
  - enterprise tenancy / admin hierarchy / cohort management
  - B2B-first product packaging
- OPS-S1 is now unblocked because the launch posture has been explicitly decided

---

## 3. Completed work to date

The major product-facing build lineages are now materially in place:

- FE-PAGES
- FE-ACCOUNT
- FE-S2A / FE-S2B
- FE-LAUNCH-INTEGRATION-A / FE-LAUNCH-INTEGRATION-B
- backend narrative enablement
- context hardening
- medication caveat foundation and output

This means the product is no longer waiting on core build shape.
What remains is the final **launch-readiness and operational trust layer**.

---

## 4. Remaining sprint sequence

## Sprint 1 — OPS-S1A
### Trust and UK baseline

**Purpose**

Create the minimum credible trust/compliance/user-facing baseline for a UK B2C launch.

**Primary scope**

- review and correct UK launch-facing claims
- remove or qualify unsupported or jurisdictionally wrong trust claims
- add or wire real:
  - Privacy
  - Terms
  - Contact
  surfaces
- align launch-facing copy with:
  - UK-first posture
  - non-diagnostic positioning
  - consumer health-data trust baseline

**Why this sprint is critical**

This is the sprint that closes the biggest remaining launch contradiction:
- product and strategy say one thing
- current trust/legal surfaces do not yet fully support it

**Launch criticality**
- **Required before launch**

---

## Sprint 2 — OPS-S1B
### Operational evidence and controls

**Purpose**

Create the minimum operational and governance evidence needed to support a credible UK B2C launch.

**Primary scope**

- UK hosting / residency evidence
- subprocessor / vendor inventory
- data-flow documentation
- DPIA or equivalent structured privacy-risk review
- operational controls / runbook baseline
- incident / backup / recovery / secrets / checklist documentation as needed for Phase 1

**Why this sprint is critical**

This is the sprint that turns the launch posture from a declared intention into something operationally defensible.

**Launch criticality**
- **Required before launch**

---

## Sprint 3 — Wedge metrics / launch instrumentation
### Proof-engine measurement layer

**Purpose**

Ensure the B2C launch can be measured as a deliberate wedge rather than treated as an unmeasured consumer experiment.

**Primary scope**

Define and, where appropriate, implement the minimum instrumentation required to evaluate whether the B2C wedge is working.

Likely metric areas:
- paid conversion
- repeat upload / repeat panel rate
- retention
- clinician report download / carry-through
- user trust / usefulness
- segment split:
  - standard retail
  - technical/biohacker
- enterprise-relevant proof signals

**Why this sprint matters**

Without these measures, B2C risks becoming a waiting room rather than a bridge into the larger B2B/B2B2C strategy.

**Launch criticality**
- **Highly recommended**
- may be partly launch-critical depending on leadership appetite for launching without formal wedge measurement

---

## 5. Launch-critical vs follow-on classification

### Launch-critical
- **OPS-S1A — Trust and UK baseline**
- **OPS-S1B — Operational evidence and controls**

### Strongly recommended / strategic follow-on
- **Wedge metrics / launch instrumentation**

### Possible later work after initial launch
- B2B packaging
- enterprise readiness
- insurer/lab/workforce expansion support
- broader analytics and cohort measurement
- multi-market readiness
- US posture
- stronger certification programmes if commercially needed later

---

## 6. Dependency order

The correct sequence is:

1. **OPS-S1A**
2. **OPS-S1B**
3. **Wedge metrics / launch instrumentation**

### Dependency logic

- OPS-S1A comes first because launch-facing trust, claims, and legal surfaces are the most visible contradiction today
- OPS-S1B follows because operational evidence must support the declared launch posture
- wedge metrics can follow once launch trust/control foundations are clear, though some metric design work may begin in parallel

---

## 7. Success measures for the B2C wedge

The B2C-first model is valid only if it behaves as a deliberate wedge.

The programme should therefore track, at minimum, whether Phase 1 launch is producing evidence in the following areas:

- paid conversion
- repeat upload / repeat testing behaviour
- retention / return usage
- clinician report download or carry-through
- user-reported usefulness / trust
- segment behaviour differences between:
  - standard retail users
  - technical/biohacker users
- signals that can later support B2B conversations

These do not all need to be fully productionised in one sprint, but the plan must not lose sight of them.

---

## 8. Explicitly out of scope for Phase 1

To preserve launch focus, the following are explicitly out of scope for this sprint plan unless separately re-authorised:

- US-first launch
- multi-market launch
- B2B-primary launch
- hybrid-everything-from-day-one launch
- enterprise tenancy / admin hierarchy / cohort tools
- HIPAA-led launch posture as the default
- SOC 2 or ISO 27001 as hard launch blockers
- medical-device positioning
- broad marketing-site redesign
- backend reasoning changes
- clinician workspace redesign
- enterprise/commercial workflow redesign

---

## 9. Immediate next move

The next actionable sprint to author is:

- **OPS-S1A — Trust and UK baseline**

That sprint is the first operational sprint genuinely unblocked by the launch-posture decisions.

---

## 10. Planning summary

### Recommended remaining Phase 1 sprint count

- **2 sprints minimum** to reach a credible first-market launch product:
  - OPS-S1A
  - OPS-S1B

- **3 sprints recommended** if HealthIQ wants the B2C wedge to be measured deliberately:
  - OPS-S1A
  - OPS-S1B
  - Wedge metrics / launch instrumentation

### Final planning position

HealthIQ is now in the final launch-preparation phase for its first market.

The remaining work is not about inventing the product.
It is about:
- making the launch posture credible
- making the operating baseline defensible
- and ensuring the B2C wedge is capable of generating real proof for the longer-term B2B destination
