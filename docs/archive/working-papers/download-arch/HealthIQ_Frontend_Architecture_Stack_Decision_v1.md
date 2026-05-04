# HealthIQ AI — Frontend Architecture & Stack Decision v1

## Purpose

This note sets the frontend architectural direction **before** detailed wireframing and implementation slicing.

It is intentionally short and decision-led.

---

## Executive decision

**HealthIQ should retain and modernise its current React + Next.js + TypeScript frontend foundation, not replatform at this stage.**

The current repo audit shows the live frontend already runs on a Next.js App Router structure with a working results flow, shared component model, typed analysis contracts, and an existing route hierarchy. Replatforming now would introduce large delivery cost, reset implementation momentum, and delay the real product work: refining the results experience and secure user journey.

This is not a defence of the current frontend as “finished.”
It is a decision that the existing foundation is still strategically viable and modern enough to build the next phase on, provided it is tightened architecturally.

---

## Why this decision is correct

### 1. The current stack family is still modern

React’s current guidance is to build new React apps with a framework rather than from raw setup, and Next.js remains a current production framework with active guidance for App Router, security, deployment, and production readiness. citeturn530183search0turn530183search1turn530183search5turn530183search11

### 2. Replatforming would solve the wrong problem

The current bottleneck is not “wrong framework.”
The current bottleneck is:
- immature page architecture
- weak disclosure model
- duplicated content layers
- incomplete rendering of explainer content
- some contract/store drift

Those are architecture and UX execution issues, not proof that the framework is obsolete.

### 3. The repo already has working product surfaces

The audit confirms there is already:
- a working results route
- a data-fetch path
- results components
- a typed frontend contract
- upload-to-results flow

That means the correct architectural move is **controlled evolution**, not stack restart.

### 4. Future-fit does not mean shiny-for-its-own-sake

A future-fit frontend stack is one that:
- supports secure authenticated product growth
- supports component reuse
- supports responsive layouts
- supports charting/motion where genuinely useful
- supports maintainable typed contracts
- can host both public and secure-area flows cleanly

The current stack can do that.

---

## Strategic stack position

### Retain
- **Framework:** Next.js
- **UI runtime:** React
- **Language:** TypeScript
- **Styling direction:** utility-first/component-token approach if already present in the codebase

### Modernise / tighten
- route/layout architecture
- shared component boundaries
- results-page composition
- contract typing consistency
- auth/account-area shell planning
- charting approach for trends
- advanced-mode / disclosure architecture

### Do not do now
- full frontend rewrite
- framework migration for aesthetic reasons
- Vite-style replatform simply because it sounds newer
- 3D/novel UX experiments as core product architecture

---

## Architectural implications for HealthIQ

### 1. We should treat Next.js as the application shell

HealthIQ has both:
- public pages
- secure authenticated product pages

That suits a framework-led application shell.

The architecture should ultimately separate:
- public marketing surface
- authenticated app shell
- upload flow
- results flow
- account/history flow

### 2. We need cleaner route and layout ownership

The repo audit already suggests results currently sit outside the `(app)` shell.
That does not force an immediate rewrite, but it does mean the frontend architecture should decide deliberately:
- which pages live in public shell
- which pages live in secure app shell
- how shared navigation/header logic is handled

### 3. Type discipline matters more than framework novelty

The audit found contract/store drift.
That is a more important architectural issue than adopting a shinier bundler.
HealthIQ is a governed product with complex payloads; typed contract integrity is core.

### 4. Security posture must be included in architecture, not added later

Current guidance on auth, file upload, and production hardening should be treated as design-time concerns, not bolt-ons. Next.js also has active production and security guidance, and React disclosed a critical RSC vulnerability in late 2025, which reinforces the need for version/security review rather than casual dependency drift. citeturn530183search5turn530183search10turn530183search17

---

## Stack decision for adjacent tooling

### Charts / trends
No replatform is needed.
Choose a lightweight trend visual approach compatible with the current React/Next stack.
This is a component decision, not a framework decision.

### Motion
Only add a motion library if it materially improves progressive disclosure and perceived polish.
Do not turn motion into a core dependency before wireframes and interaction patterns are locked.

### UI component primitives
Use a controlled component system approach.
Do not let one-off page components proliferate without shared anatomy.

---

## Explicit recommendation

**Decision:** Stay on the current Next.js/React/TypeScript foundation.

**Immediate architecture priority:**
1. lock results UX wireframes
2. define public vs authenticated shell boundaries
3. reconcile frontend data contracts/types
4. plan secure-area route/layout structure
5. then implement the results experience on that foundation

---

## Rejected alternatives

### Rebuild now on a new stack
Rejected because there is no evidence yet that the existing stack blocks the product.

### Freeze stack discussion entirely
Rejected because the stack does need an explicit strategic decision now.

### Adopt Gemini’s suggested stack wholesale
Rejected because it is not the governing repo reality and has not been justified by an actual blocker analysis.

---

## Design consequence

Because the foundation is retained, the next correct artefact is:

**the wireframe package for the results experience**

not a frontend rewrite plan.

---

## Status

**Locked recommendation for current phase:** retain and modernise the existing frontend foundation; do not replatform.
