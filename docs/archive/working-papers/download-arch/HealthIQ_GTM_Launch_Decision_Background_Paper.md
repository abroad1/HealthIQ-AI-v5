# Background paper: launch decision inputs required to unblock operational planning for HealthIQ

## Purpose

We have now completed the main product-building and integration lineages needed for a coherent Phase 1 user experience. The frontend shell, results journey, account surfaces, narrative presentation, context hardening, and medication caveat pathways are now materially in place. What remains blocked is not another product sprint, but the operational scoping needed to decide how HealthIQ should actually launch. The roadmap explicitly states that OPS-S1 must not be authored until four external decisions are made: intended launch market or markets, data residency requirements, the operating model, and the minimum compliance framework applicable to health data in those markets.

This paper sets out the decisions now required, why they matter, and the consequences of leaving them unresolved.

## Why these decisions are needed now

Up to this point, the programme has been able to progress by strengthening product truth, frontend coherence, and the translation layer without committing to a final market or operating model. That flexibility has now run its course.

We are at the point where operational, legal, and launch-readiness choices begin to shape architecture, hosting, onboarding, messaging, data handling, and what claims the product can safely make. The roadmap treats this as a deliberate handoff: product construction first, launch-operating definition second. It also explicitly separates FE-LAUNCH-INTEGRATION from OPS-S1, and states that OPS-S1 is blocked until the relevant business inputs are confirmed.

In practical terms, we now need to decide not just what HealthIQ is, but who it is launching for, where it will launch, how it will operate commercially, and what trust/compliance standard is the minimum acceptable for that launch.

## The four decisions to be made

### 1. Intended launch market or markets

We need to decide the first geography in which HealthIQ will actually launch.

This is not simply a marketing choice. It affects data handling, legal language, user expectations, healthcare framing, and commercial viability. A UK-first launch creates one set of assumptions. A US-first launch creates another. A multi-market launch immediately increases complexity across compliance, hosting, support, pricing, and product language.

The key decision here is whether we are launching in:
- one initial market only, or
- multiple markets from day one

The most important question is not “where could we eventually operate?” but “where will we actually launch first?”

### 2. Data residency requirements

We need to decide where user data must live for the chosen launch model.

This decision cannot sensibly be made in isolation from launch geography and operating model. Data residency requirements will differ depending on whether we are serving UK retail users, clinics, employers, or a broader international base. It also affects vendor choices, hosting setup, contractual posture, and how confidently we can speak about privacy and trust.

The key question is whether our Phase 1 product needs:
- a specific country-residency requirement,
- a broader region-based residency requirement,
- or a simpler initial model that is still acceptable for the first launch audience

### 3. Operating model

We need to decide whether Phase 1 is launching as:
- B2C,
- B2B,
- or hybrid

This is a foundational decision because it changes almost everything around the product:
- onboarding journey
- account model
- trust expectations
- reporting needs
- customer success model
- sales cycle
- who actually pays
- who is the primary user versus the primary buyer

A hybrid model may eventually be right, but it is usually not a helpful first-launch answer unless we can state clearly which side is primary at launch.

The GTM team should therefore answer not only “which model do we want eventually?” but “which model is primary for Phase 1?”

### 4. Minimum compliance framework

We need to decide the minimum compliance posture required for the chosen launch combination.

This is not the same as asking what the maximum eventual compliance ambition should be. The useful question is: what is the minimum credible and defensible trust/compliance position for the first launch market and operating model?

This choice will affect:
- what claims we can make publicly
- how we position the product
- internal controls and documentation
- launch timeline and cost
- operational burden

It should be framed as a Phase 1 floor, not an all-future ceiling.

## Why these decisions should be made together

Although the roadmap lists four separate inputs, they are really one connected launch decision stack.

For example, it is difficult to decide data residency before knowing the launch market. It is difficult to decide compliance posture before knowing whether the first model is B2C or B2B. It is difficult to decide operating model properly without knowing who the first launch customer is meant to be.

If these choices are taken independently, we risk creating a launch model that is internally inconsistent. For example, we might choose a retail-facing product experience while assuming a B2B trust/compliance stance, or commit to a data posture that is too heavy for the first commercial model, or adopt wording that does not match the actual legal and operational setup.

The GTM team should therefore treat these as linked decisions that need to resolve into one coherent Phase 1 launch posture.

## What has already been built, and why that matters

This is not a blank-sheet launch conversation. The current product direction already implies certain constraints and opportunities.

The product now has:
- a coherent authenticated shell and navigation model
- upload, results, reports/history, profile, and settings surfaces
- structured deterministic interpretation
- narrative summaries as a companion translation layer
- context-aware interpretation pathways
- deterministic medication/supplement caveat output
- a launch-integrated frontend experience that now feels like one product rather than disconnected modules

That means the GTM decision is not about inventing a totally different product. It is about deciding how this product should be brought to market first, under what conditions, and with what degree of trust and operational readiness.

## Risks of not deciding now

If these four inputs remain unresolved, several things stay blocked or uncertain.

First, OPS-S1 remains blocked by design. That means we cannot sensibly author the operational readiness workpackage without risking guesswork.

Second, product claims and launch messaging remain unstable. That creates a risk that landing-page or GTM language drifts ahead of the actual compliance and operating posture.

Third, infrastructure and hosting decisions may be made indirectly rather than intentionally.

Fourth, commercial focus may blur. A product can technically support multiple futures while still failing to launch well because it is not clear who the first customer really is.

## Recommended decision framing for the GTM team

The most useful way for the GTM team to approach this is to decide the following in sequence:

First, define the first launch customer and buyer combination. For example, are we launching primarily for individual consumers, clinics, employers, or another clearly defined user-buyer pair?

Second, choose the first actual launch market for that model.

Third, choose the operating model that best matches that customer and market combination.

Fourth, define the minimum acceptable compliance/trust posture for that exact combination.

Fifth, confirm the resulting data residency requirement.

That sequence tends to produce a more coherent answer than debating all four dimensions independently.

## Questions for the GTM team to answer

The discussion should produce explicit answers to the following:

What is the first market we are actually launching in?

Are we launching in one market only at first, or more than one?

Who is the first true launch customer?

Who is the first true economic buyer?

Is the Phase 1 operating model B2C, B2B, or hybrid, and which of those is primary at launch?

What is the minimum compliance/trust posture required to support that launch honestly and credibly?

Where must customer data reside for that model and market?

What is explicitly out of scope for Phase 1, even if it may be relevant later?

## Decision output required

The output from the GTM discussion does not need to be a long strategy document. It needs to be a clear launch decision statement that covers:

- first launch market
- first launch customer and buyer
- primary operating model
- minimum compliance posture
- data residency decision
- what is explicitly deferred until later

Once that is agreed, OPS-S1 can be scoped properly rather than guessed.

## Closing position

The product programme has reached the point where additional operational planning without these decisions would be speculative. The roadmap anticipated this and explicitly required dedicated scoping before OPS-S1 prompt authoring. The immediate need is therefore not another product build decision, but a launch-definition decision.

The GTM team is being asked to define the first real-world launch posture for HealthIQ so that operational planning, trust/compliance work, and final market-facing integration can proceed on a deliberate basis rather than assumption.
