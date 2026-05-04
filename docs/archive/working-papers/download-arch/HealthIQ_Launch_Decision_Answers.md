# HealthIQ — Launch Decision Answers Paper

## Purpose

This paper answers the launch-decision questions required to unblock operational planning for HealthIQ.

It is designed to be short, decisive, and operationally useful.

The aim is not to describe every possible future.
The aim is to define the most coherent **Phase 1 launch posture** so that OPS-S1 can be scoped deliberately rather than guessed.

This response is based on the background paper and on the current product/GTM context already established for HealthIQ, including the distinction between:

- the **best long-term enterprise revenue markets**, and
- the **best first launch posture** for the product that has actually been built so far. fileciteturn21file0

---

## Executive decision

### Recommended Phase 1 launch posture

- **First launch market:** United Kingdom
- **Launch scope:** one market only at first
- **First true launch customer:** individual self-directed retail user with an already-tested blood panel
- **First true economic buyer:** that same retail user
- **Primary operating model at launch:** B2C
- **Secondary motion running in parallel:** B2B business development only, not B2B product launch
- **Minimum compliance posture:** UK consumer health-data compliance baseline with strict non-diagnostic positioning
- **Data residency decision:** UK-hosted by default for Phase 1

This is the cleanest, fastest, and least internally contradictory launch posture.

---

## Why this is the right answer

## 1. The first launch posture should match the product that is already built

The current product state described in the background paper is much closer to a coherent self-serve retail launch product than to a true enterprise deployment product.

What is already materially in place:

- authenticated shell
- upload flow
- results journey
- reports/history
- profile/settings
- narrative presentation
- context-aware interpretation
- medication caveat pathways
- coherent frontend experience. fileciteturn21file0

That is a strong fit for:

- a retail upload user
- who already has a tested panel
- and wants post-test interpretation

It is **not yet obviously a first-launch B2B platform** for:

- enterprise tenancy
- buyer/admin controls
- cohort management
- batch upload operations
- account hierarchy
- procurement and security reviews
- customer success workflows
- enterprise reporting
- partner billing logic

So the first principle is simple:

**launch first where product reality and operating reality already align.**

---

## 2. This does not contradict the larger B2B strategy

There is an important distinction between:

- **the first launch market**, and
- **the best medium-term scaling markets**

Those are not the same decision.

My view remains:

- the best near-term **commercial wedge** is still labs / blood panel companies
- the best medium-term **economic buyer** is still insurers
- the largest potential **contract markets** may still be workforce / public-sector screening

But that does **not** mean the first real-world launch should be B2B.

Why not:

- B2B needs more operational machinery
- B2B has longer sales cycles
- B2B adds data / contract / support complexity immediately
- B2B would force product and ops work that is not clearly the shortest path to first live usage

So the correct sequencing is:

### Phase 1 launch posture
UK retail B2C launch

### Phase 1.5 commercial expansion
B2B business development and pilot pursuit in parallel

### Phase 2 scaling posture
labs / insurers / workforce screening once proof, ops readiness, and enterprise packaging exist

That is coherent.

---

## 3. Why the UK should be the first launch market

## Recommended answer
**UK only at first.**

## Why

### 3.1 Operational simplicity
A one-market launch keeps:

- data posture simpler
- trust/compliance language simpler
- support simpler
- pricing simpler
- UX wording simpler
- claims review simpler

### 3.2 Product-language fit
The HealthIQ product is being positioned as a post-test metabolic interpretation layer, not as a lab or diagnostic provider. A UK-first launch makes it easier to keep that positioning tight without trying to harmonise US and UK language, expectations, and compliance assumptions at the same time.

### 3.3 Lower organisational drag
A US launch from day one would force immediate answers on:

- HIPAA posture
- US state privacy questions
- broader vendor and contracting expectations
- more aggressive litigation / claims sensitivity

That is not the cleanest first move for Phase 1.

### 3.4 Trust coherence
For a health-data product, launch trust matters. A UK-first posture with UK data residency and clearly bounded claims is easier to communicate and defend than a multi-market launch with patchwork rules.

---

## 4. Recommended first launch customer and buyer

## First launch customer
**Retail end user with an already-tested blood panel**

## First economic buyer
**That same retail end user**

## Why

This is the cleanest pair because:

- the user already exists
- the upload flow already exists
- the value proposition is direct
- no enterprise sales dependency is required for first usage
- no partner integration is required to prove utility
- the buyer/user are the same person, which removes launch complexity

Most importantly, this lets HealthIQ prove the core proposition:

**can we take an already-tested panel and make the customer meaningfully better off afterwards?**

That is the right first proof.

---

## 5. Recommended primary operating model

## Decision
**B2C-primary at launch**

## With this explicit nuance
B2B is **not rejected**.
It is simply **not the primary launch operating model**.

## Why B2C-primary is the right Phase 1 answer

### 5.1 Fastest route to real usage
You can launch without waiting for:

- procurement
- enterprise contracting
- white-label packaging
- admin hierarchy work
- partner implementation cycles

### 5.2 Cleanest learning loop
A B2C launch gives the fastest signal on:

- onboarding friction
- upload success
- comprehension
- trust
- narrative usefulness
- repeat usage intent
- willingness to pay

### 5.3 Better product truth before enterprise packaging
Enterprise buyers do not want a theory. They want evidence.
A live B2C launch is the fastest way to generate:

- user behaviour evidence
- message clarity evidence
- product-surface evidence
- repeat-panel behaviour evidence
- proof that users find the output valuable

### 5.4 Lowest launch contradiction
The background paper makes clear that OPS-S1 is blocked by launch-definition inputs, not by lack of more product build. fileciteturn21file0
That strongly suggests the right answer is the **least contradictory launch posture**.

That is B2C-primary.

---

## 6. Recommended minimum compliance / trust posture

## Decision
For Phase 1, HealthIQ should adopt a **UK consumer health-data compliance floor**, not an enterprise-maximal posture.

## Minimum credible posture

### 6.1 Legal / privacy baseline
- UK GDPR special-category health data handling
- Data Protection Act 2018 compliance
- clear privacy notice
- lawful basis and explicit user-facing transparency
- processor agreements with all relevant vendors
- clear retention and deletion rules

### 6.2 Security / operational baseline
- encryption in transit and at rest
- role-based access control
- audit logging for access to health data
- incident response process
- secure authentication practices
- defined backup / recovery posture
- vulnerability management and routine security review

### 6.3 Product / claims baseline
- explicit non-diagnostic positioning
- no claims implying formal diagnosis or treatment recommendation
- careful wording around interpretation, likelihood, uncertainty, and next-step discussion
- internal review discipline on user-facing medical copy

### 6.4 Governance baseline
- data flow documentation
- vendor/subprocessor inventory
- DPIA or equivalent structured privacy-risk review before launch
- named internal accountability for privacy/security decisions

## What this deliberately does **not** require for Phase 1
- HIPAA-ready US launch posture
- enterprise-grade buyer questionnaires as the launch floor
- ISO 27001 certification as a hard launch dependency
- SOC 2 as a hard launch dependency
- medical device positioning
- clinic workflow insertion

Those may become commercially useful later. They should not be allowed to slow the first launch if the first launch is UK B2C.

---

## 7. Data residency decision

## Decision
**UK-hosted by default for Phase 1**

## Why

If the first launch market is the UK and the first launch model is UK retail B2C handling health data, then the cleanest trust position is:

- UK market
- UK users
- UK data residency

This is not because no other model could work.
It is because this is the least ambiguous and easiest to defend in early market-facing trust language.

## Practical effect
This should be treated as:

- UK-hosted primary application/data posture
- no unnecessary cross-border sprawl in Phase 1
- no multi-region complexity unless forced by a specific operational need

---

## 8. What is explicitly out of scope for Phase 1

To keep launch coherent, the following should be explicitly deferred:

### Markets
- US launch
- multi-market launch
- employer/public-sector programme launch
- insurer-first launch
- clinic-first launch

### Operating model
- B2B-primary launch
- hybrid-everything-from-day-one launch
- white-label launch as the main product posture

### Compliance
- HIPAA-led launch posture
- enterprise procurement-grade compliance buildout as launch floor
- regulated medical device posture

### Product / ops capabilities
- enterprise tenancy
- cohort admin tools
- buyer dashboards
- bulk customer management
- partner batch processing as launch-critical feature
- custom residency requirements by client
- complex enterprise onboarding / customer success motions

This is important because without an explicit out-of-scope list, the company will blur back into a pseudo-hybrid launch and lose focus.

---

## 9. Why not choose B2B first even though B2B is the bigger prize?

Because the question is not:

**where is the biggest eventual contract value?**

The question is:

**what is the first launch posture that most cleanly converts the built product into live usage, proof, and learnings?**

Those are different questions.

My judgement is:

- B2B is still the bigger company-building direction
- B2C is the better first launch posture

That is not a retreat from the B2B thesis.
It is the cleanest route into it.

---

## 10. Resulting launch decision statement

### Recommended launch decision statement

HealthIQ should launch first as a **UK-only, retail B2C, post-test metabolic interpretation product** for individuals who already have tested blood panels.

The first true launch customer and economic buyer should be the self-directed retail user.

The minimum Phase 1 trust/compliance posture should be a UK consumer health-data baseline with strict non-diagnostic positioning, clear privacy/security controls, and UK data residency by default.

B2B business development should continue in parallel, but B2B should not be treated as the primary launch operating model until enterprise proof, enterprise packaging, and the required operational machinery are in place.

---

## 11. Operational consequence

If this decision is accepted, OPS-S1 can now be scoped around a coherent Phase 1 posture:

- UK launch only
- B2C-primary
- UK data residency
- consumer health-data compliance floor
- explicit out-of-scope list for US / enterprise / hybrid sprawl

That is enough to move from abstract launch debate into concrete operational planning.

---

## Final recommendation

Do **not** launch into multiple markets.
Do **not** launch as hybrid by default.
Do **not** let the bigger eventual B2B opportunity distort the first real launch posture.

The correct first move is:

**UK, one market, B2C-primary, self-upload customer, UK data residency, consumer health-data trust floor, B2B expansion in parallel rather than at launch.**
