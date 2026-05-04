# HealthIQ Intelligence Model Design Workshop

## Purpose

This exercise is designed to answer one strategic question:

**What questions do we want the platform to be able to answer downstream, and what upstream knowledge must exist to answer them intelligently?**

We are not designing YAML fields yet.  
We are not designing package schemas yet.  
We are defining the intelligence target the platform must support.

If we get this right, the future schema can be built from first principles rather than from whatever happens to be in current source files.

---

## Core framing

The platform will only ever be as intelligent as the knowledge it captures upstream.

So before we ask:
- what fields should the schema contain?

we must ask:
- what questions will users, clinicians, and future internal reasoning systems want to ask the platform?
- what kind of answers would make those questions feel genuinely intelligent, useful, and defensible?
- what information must exist upstream for those answers to be possible?

---

## Workshop output

By the end of this exercise we want:

1. a list of the most important downstream questions the platform should be able to answer
2. a clear view of which user types will ask those questions
3. a definition of what a strong answer looks like
4. a list of the upstream knowledge required to support those answers
5. an early view of which knowledge must be structured vs which can remain narrative
6. a basis for designing the target biomarker intelligence schema

---

## Rules for the session

### Do
- think strategically
- think about future platform use, not just current MVP use
- focus on what intelligence the platform should eventually provide
- be specific about the kinds of questions and answers that matter

### Do not
- jump straight into YAML/schema design
- get lost in implementation details
- over-focus on current package limitations
- assume current source files already contain everything we need

---

## Part 1 — Future user types

List the types of users or system components that will interrogate the platform in future.

Examples:
- consumer user
- advanced user / biohacker
- clinician
- internal analytics / intelligence engine
- future phenotype / pathway layer
- future clinical review / audit layer

### Working table

| User / system type | What are they trying to achieve? | Why do they need the platform? |
|---|---|---|
| | | |
| | | |
| | | |

---

## Part 2 — Downstream questions

For each user type, list the important questions they will want to ask the system.

Think in plain language first.

Examples:
- Why is this biomarker abnormal?
- What is the most likely explanation?
- What evidence supports that?
- What else should I look at?
- What alternative explanations remain plausible?
- How serious is this?
- What system or pathway is implicated?
- What should a clinician test next?
- What would make this interpretation stronger or weaker?
- What do these biomarkers mean together?

### Working table

| User / system type | Downstream question | Why this question matters |
|---|---|---|
| | | |
| | | |
| | | |

---

## Part 3 — What a strong answer looks like

For each downstream question, define what would make the answer feel:
- intelligent
- useful
- defensible
- materially better than a shallow “traffic light” interpretation

Examples of weak answers:
- “This is high.”
- “This may indicate inflammation.”
- “You may want to speak to your doctor.”

Examples of strong answers:
- identifies likely explanations
- distinguishes between competing causes
- explains what evidence supports the interpretation
- highlights uncertainty and contradiction
- points to confirmatory markers or tests
- shows mechanism, severity, and differential meaning separately

### Working table

| Downstream question | What would a weak answer look like? | What would a strong answer look like? |
|---|---|---|
| | | |
| | | |
| | | |

---

## Part 4 — Upstream knowledge required

For each downstream question, ask:

**What information must exist upstream for the system to answer this well?**

This is the most important part of the whole exercise.

Examples of upstream knowledge types:
- primary biomarker
- trigger direction
- supporting biomarkers
- supporting biomarker directionality
- supporting biomarker role
- differential markers
- corroborating markers
- severity markers
- contradiction markers
- pathway / system relationships
- confirmatory tests
- rule-level evidence source links
- evidence strength
- physiological claim
- threshold notes
- caveats / confounders
- medication effects
- demographic modifiers
- pre-analytic influences
- phenotype relationships
- interactions with other biomarkers
- confidence / uncertainty factors

### Working table

| Downstream question | Upstream knowledge needed to answer it properly |
|---|---|
| | |
| | |
| | |

---

## Part 5 — Structured vs narrative

Now ask:

Which of the upstream knowledge items must be:
- structured
- narrative
- hybrid

Use this rule of thumb:

If the information affects:
- reasoning
- ranking
- auditability
- cross-biomarker linkage
- future automation
- consistency of interpretation

then it probably needs to be structured.

### Working table

| Knowledge item | Structured / narrative / hybrid | Why |
|---|---|---|
| | | |
| | | |
| | | |

---

## Part 6 — Core now vs later

Not everything has to land in version 1 of the target schema.

Separate:
- core intelligence requirements now
- future enrichment later

### Working table

| Knowledge item | Core now / later | Why |
|---|---|---|
| | | |
| | | |
| | | |

---

## Part 7 — Open design questions

Capture anything that still feels unresolved.

Examples:
- Do we need explicit contradiction markers?
- Do we need confidence weighting for supporting markers?
- Do we need structured rule-level provenance everywhere?
- Do we need explicit phenotype links now or later?
- Do we need explicit confounder classes?
- How far do we go in modelling severity vs differential vs corroboration?

### Working table

| Open question | Why it matters | Needed before target schema? |
|---|---|---|
| | | |
| | | |
| | | |

---

## Suggested kickoff prompt

Use this to open the workshop:

**“In 3 years, what questions do we want people — and the system itself — to be able to ask HealthIQ, and what would make the answers feel truly intelligent rather than generic?”**

---

## Suggested sequence for the first session

1. Agree the user groups
2. Brainstorm downstream questions
3. Define what strong answers would look like
4. Identify upstream knowledge needed
5. Only then discuss structure and schema implications

---

## Minimum success criteria for session 1

By the end of the first session we should have:
- 3–5 user types
- 15–25 important downstream questions
- a first pass at strong vs weak answers
- a first pass at the upstream knowledge needed
- a shortlist of likely structured knowledge requirements

That will be enough to begin designing the target intelligence schema from first principles.

---

## Final reminder

The goal is not to ask:

**“What fields do we have now?”**

The goal is to ask:

**“What intelligence do we want later, and what knowledge must exist upstream to make that possible?”**