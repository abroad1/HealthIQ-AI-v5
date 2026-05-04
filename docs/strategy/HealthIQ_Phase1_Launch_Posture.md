# HealthIQ — Phase 1 Launch Posture

## Purpose

This document records the agreed Phase 1 launch posture for HealthIQ so that product, GTM, and operations planning can proceed from a single stable source of truth.

It exists to prevent drift between:
- product strategy
- GTM assumptions
- operational scoping
- future sprint authoring

It should be treated as the governing launch-position input for OPS-S1 scoping and any adjacent launch-readiness planning.

---

## Executive decision

### Agreed Phase 1 launch posture

HealthIQ will launch first as a:

- **UK-first** product
- **single-market** launch
- **B2C-primary** launch model
- for people who **already have blood test results** and want better interpretation
- with **UK data residency by default**
- under a **UK consumer health-data compliance baseline**
- with **strict non-diagnostic positioning**

This is a deliberate choice.
It is not a fallback position and it is not a temporary holding pattern while waiting for B2B.

---

## Strategic framing

## B2C-first is a deliberate wedge, not the final destination

The company’s long-term economic centre of gravity is still expected to sit more naturally in:

- **B2B**
- **B2B2C**
- and infrastructure / platform-style health interpretation opportunities

However, the cleanest and fastest first launch posture is **B2C-first**.

This is because the current product is already much closer to a coherent self-serve post-test interpretation experience than to a true enterprise deployment model.

So the strategic model is:

- **launch = B2C**
- **company destination = B2B / B2B2C infrastructure**

That is the intended sequencing.

---

## Why B2C-first has been chosen

B2C-first is valid only if it is treated as a wedge with a clear job to do.

For HealthIQ, that job is to:

- prove that users value post-test interpretation enough to pay for it
- refine outputs quickly using real user behaviour
- generate repeat upload / repeat panel behaviour
- create longitudinal data assets over time
- stress-test the clarity and depth of outputs across user types
- generate user-carried clinician exposure through the downloadable clinician report
- build proof points that can later support B2B sales, partnerships, and enterprise packaging

So B2C is not being used here as “something to do until a better model appears.”
It is being used as a **data, proof, product-learning, and messaging engine**.

---

## Phase 1 launch customer and buyer

### First launch customer

The first launch customer is:

**the self-directed retail user who already has a tested blood panel and wants a much better interpretation layer afterwards**

### First economic buyer

The first economic buyer is:

**that same retail user**

### Why this pairing is right for Phase 1

This is the cleanest first launch pair because:

- the user already exists
- the upload flow already exists
- the value proposition is direct
- no procurement cycle is needed
- no partner integration is needed to prove utility
- the product can create immediate value from existing lab output
- the buyer and user are the same person, which simplifies launch dynamics

The core Phase 1 proof question is:

**Can HealthIQ take an already-tested panel and make the user meaningfully better off afterwards through interpretation, clarity, depth, and clinician-ready output?**

---

## B2C launch subsegments

Although the launch model is B2C-first, the Phase 1 B2C audience is not one homogeneous user group.

HealthIQ should treat Phase 1 B2C as having **two explicit subsegments**.

### 1. Standard retail user

This user primarily wants:

- clarity
- reassurance
- readable interpretation
- simple prioritisation of what matters
- practical understanding of what to discuss next
- something credible they can take to a clinician

The product job for this user is:

- make the blood panel understandable
- make the result feel useful and grounded
- reduce confusion without pretending to diagnose

### 2. Technical / biohacker user

This user primarily wants:

- more depth
- more systems logic
- more biomarker granularity
- more nuance and interpretive detail
- more ability to inspect and interrogate the output

The product job for this user is:

- prove that the engine is genuinely intelligent
- show deeper system-level interpretation
- make the product feel superior to standard lab commentary and simplistic wellness summaries

### Why both matter

These two segments make the B2C wedge stronger, not weaker.

- the **standard retail user** tests broad-market clarity, trust, usefulness, and willingness to pay
- the **technical user** stress-tests depth, quality, and perceived intelligence of the system

Both segments can also contribute to clinician exposure through the downloadable clinician report.

---

## Clinician report as a distribution mechanism

One of the most important outputs in the Phase 1 wedge is the **downloadable clinician report**.

This is not just a product feature.
It is also a **distribution mechanism**.

The logic is:

- the user uploads an existing blood panel
- HealthIQ produces a high-quality interpretation experience
- the user can download a clinician-oriented report
- the user brings that report into a real clinical conversation
- clinicians are exposed to HealthIQ output without the company needing direct clinician acquisition at launch

This matters because it allows HealthIQ to:

- generate real-world clinician exposure indirectly
- test whether the clinician-facing output earns trust when carried in by patients
- learn how the report performs in real conversations
- build evidence for future practitioner, lab, and insurer conversations

So the clinician report should be viewed as both:

- a user-value feature
- and a strategic bridge into later B2B trust and distribution

---

## Launch market decision

### Decision

**United Kingdom only at first**

### Why

A UK-first launch keeps Phase 1 simpler across:

- hosting and data posture
- legal and privacy expectations
- support model
- product language
- trust positioning
- compliance framing

It also reduces the risk of trying to harmonise UK and US expectations at the same time before the company has evidence from live usage.

The goal of Phase 1 is not to prove that HealthIQ can theoretically operate everywhere.
It is to prove that it can launch coherently and successfully somewhere.

For Phase 1, that somewhere is the UK.

---

## Operating model decision

### Decision

**B2C-primary at launch**

### Clarification

This does **not** mean B2B is rejected.
It means B2B is **not** the primary launch operating model.

### Parallel motion

HealthIQ should continue **B2B business development in parallel**, but not treat B2B as the launch model.

That means:

- keep exploring labs, clinics, insurers, workforce, and public-sector pathways
- gather evidence that supports those later motions
- do not force Phase 1 product and ops complexity to look like enterprise launch machinery before the product has earned it

---

## Data residency decision

### Decision

**UK-hosted by default for Phase 1**

### Why

Given that the chosen launch posture is:

- UK users
- UK-first launch
- B2C-primary
- health-data handling

The cleanest and least ambiguous trust position is:

- UK market
- UK users
- UK data residency

This is not because no other option could ever work.
It is because this is the simplest and most defensible early trust posture.

---

## Minimum compliance / trust posture

### Decision

HealthIQ should adopt a **UK consumer health-data compliance baseline** for Phase 1, not an enterprise-maximal or US-first posture.

### Minimum credible Phase 1 posture

#### Privacy / legal baseline

- UK GDPR special-category health data handling
- Data Protection Act 2018 compliance
- clear privacy notice and user transparency
- lawful basis and explicit clarity around data use
- processor agreements with relevant vendors
- clear retention and deletion posture

#### Security / operational baseline

- encryption in transit and at rest
- role-based access control
- audit logging for health-data access
- secure authentication practices
- defined backup and recovery posture
- incident response capability
- vulnerability management and routine security review

#### Product / claims baseline

- strict non-diagnostic positioning
- no claims implying diagnosis or treatment recommendation
- careful wording around interpretation, uncertainty, and next-step discussion
- disciplined review of user-facing medical copy

#### Governance baseline

- data-flow documentation
- vendor / subprocessor inventory
- DPIA or equivalent privacy risk review before launch
- named internal accountability for privacy/security decisions

### What is **not** required as a Phase 1 floor

The following may become useful later, but should not be allowed to delay a coherent UK B2C launch if they are not yet required:

- HIPAA-led launch posture
- enterprise questionnaire response packs as launch minimum
- ISO 27001 certification as a hard launch dependency
- SOC 2 as a hard launch dependency
- medical device positioning
- clinic workflow insertion as the primary launch model

---

## What the B2C wedge must prove

To stop B2C-first becoming a waiting room, Phase 1 must be evaluated as a **bridge strategy**.

That means its success must be judged not only by consumer usage, but by whether it creates assets and proof that support later B2B expansion.

The launch has to prove that HealthIQ can generate:

- real user demand
- real willingness to pay
- repeat usage behaviour
- trust in the outputs
- clinician exposure through report carry-through
- evidence that enterprise buyers will later find credible

---

## Bridge metrics

The following metrics should be defined and tracked early, because they determine whether the B2C wedge is doing its intended job.

### Commercial and behavioural metrics

- paid conversion rate
- repeat upload / repeat panel rate
- retention over a defined period
- clinician report download rate
- clinician report carry-through rate
- percentage of users who say they discussed the report with a clinician
- percentage of users who say the report improved that conversation
- user-rated usefulness / trust

### Product proof metrics

- narrative summary engagement
- clinician report usage by segment
- longitudinal usage over time
- signal density across panels
- segment-level differences between standard and technical users

### Segment-specific metrics

Track separately where possible for:

- **standard retail users**
- **technical / biohacker users**

At minimum compare:

- paid conversion by segment
- repeat upload rate by segment
- retention by segment
- clinician report usage by segment
- trust/usefulness by segment

This is important because these two B2C subsegments may create different forms of evidence and may reveal different strengths or weaknesses in the product.

---

## What is explicitly out of scope for Phase 1

To preserve focus, the following should be treated as explicitly out of scope for the first launch posture.

### Markets out of scope

- US-first launch
- multi-market launch
- employer/public-sector programme launch
- insurer-first launch
- clinic-first launch

### Operating-model scope exclusions

- B2B-primary launch
- hybrid-everything-from-day-one launch
- white-label launch as the primary product posture

### Compliance scope exclusions

- HIPAA-led launch posture as the baseline
- enterprise-maximal compliance buildout as the launch floor
- regulated medical device posture for Phase 1

### Product / operating capability exclusions

- enterprise tenancy
- cohort admin tools
- buyer dashboards
- bulk customer management
- partner batch processing as a launch-critical requirement
- complex enterprise onboarding and customer-success machinery
- client-specific custom data residency options

---

## Resulting launch decision statement

### Final Phase 1 launch decision

HealthIQ should launch first as a **UK-only, B2C-primary, post-test metabolic interpretation product** for individuals who already have tested blood panels.

The B2C launch should explicitly serve two retail subsegments:

- the **standard retail user** seeking clarity, reassurance, and a credible interpretation layer
- the **technical / biohacker user** seeking deeper logic, granularity, and systems-level insight

The launch should be treated as a **deliberate wedge strategy** whose purpose is to:

- prove demand
- improve outputs quickly
- generate repeat-panel behaviour
- create longitudinal data
- validate willingness to pay
- produce clinician exposure through downloadable clinician reports
- build proof for later B2B and B2B2C expansion

The minimum Phase 1 trust/compliance posture should be a **UK consumer health-data baseline** with strict non-diagnostic positioning and **UK data residency by default**.

B2B business development should continue in parallel, but B2B should **not** be treated as the primary launch operating model until the product, evidence, and operating machinery are ready.

---

## Implication for OPS-S1

If this launch posture is accepted, OPS-S1 can now be scoped on a concrete basis rather than assumption.

The governing inputs are now:

- **launch market:** UK only
- **primary operating model:** B2C-first
- **strategic destination:** B2B / B2B2C later
- **data residency:** UK by default
- **compliance floor:** UK consumer health-data baseline
- **product role:** post-test interpretation, not diagnostic service
- **out-of-scope list:** explicitly defined

That should now be sufficient to begin OPS-S1 preflight work.
