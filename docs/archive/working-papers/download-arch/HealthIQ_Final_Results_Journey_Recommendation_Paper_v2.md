
# HealthIQ AI — Final Recommendation Paper v2
## Recommended world-class results journey and asset-to-UX mapping

**Status:** Final recommendation for delivery-team review  
**Purpose:** To define the recommended user journey for the HealthIQ AI results experience, grounded in the governed assets already present in the codebase, refined for delivery realism, and explicit about where content or contract dependencies still exist.

---

## 1. Executive summary

HealthIQ AI should not behave like a better lab report.

Most users will already have seen a conventional blood report, often with at least a reasonable marker-by-marker explanation. That means the product must achieve two things at once:

1. **Point of parity**  
   It must still let users inspect individual biomarkers, understand what each marker means, and feel that the system respects the familiar “show me my actual results” expectation.

2. **Point of differentiation**  
   It must go far beyond that by showing the body as an interconnected system, surfacing the lead pattern, making the reasoning visible, balancing strain with reassurance, and teaching the user something deeper about how their biology works.

That means the results experience must be organised as a **guided reasoning journey** rather than a report surface.

The strongest direction is not to add novelty for novelty’s sake. It is to use the exceptional deterministic assets already present in the system and present them in a clearer, tighter, more emotionally intelligent sequence.

The recommended final journey is:

1. Your body overview  
2. What’s working well  
3. Primary finding and why  
4. Why this lead won / uncertainty  
5. Patterns across your body  
6. Marker-level evidence  
7. Key body-level insights  
8. What to do next  
9. Clinician summary  

This sequence is recommended because it:
- shows the user their story quickly
- reassures before alarming
- explains before drowning them in evidence
- preserves biomarkers as a credible evidence layer
- keeps the “wow” factor grounded in governed truth, not visual gimmicks
- separates retail understanding from clinician handoff cleanly

The key recommendation is:

**Use deterministic assets as the narrative spine, preserve biomarkers as a high-quality evidence layer, and use richer explanation only where it genuinely improves understanding.**

However, two delivery realities must be stated clearly:

- the proposed **pattern layer** is partly grounded in the current cluster/system implementation, but a fully governed phenotype-display layer with strong retail naming may still require an explicit contract check before being treated as implementation-ready
- rich **mechanism/pathway explanation text** exists only where authored knowledge-bus packages currently provide it; it is not universally available across all biomarkers

Those constraints do **not** invalidate the journey. They simply mean some parts of it are buildable immediately, while others require content/contract verification or staged fallback behaviour.

---

## 2. Why this recommendation is the right one

The current strategic challenge is not whether HealthIQ can analyse a panel. It clearly can.

The real question is:

**How should a world-class metabolic reasoning engine reveal its intelligence to the user?**

In arriving at this recommendation, the governing principles were:

### 2.1 Users need orientation before detail
Users are not opening the page to browse cards. They are trying to understand what their body is telling them overall. That means the page should start with orientation, not evidence.

### 2.2 Reassurance must come early
A product that only reports concerns feels alarming and narrow. A system that can say what appears stable, resilient, or well-regulated feels more trustworthy and more intelligent.

### 2.3 The lead finding must be explained, not merely stated
The main value of HealthIQ is not that it can identify a concern, but that it can explain:
- why that concern matters
- why it won over other possibilities
- how the markers connect
- what would change the conclusion

### 2.4 Biomarkers still matter commercially and experientially
Many users will expect to see individual biomarker results because that is what traditional blood reports provide. That is the point of parity.

So biomarker evidence should not be marginalised or weakened. It should be presented later in the journey, but when the user gets there, it should still feel premium and unusually rich.

That means:
- clear values and ranges
- contribution context
- strong educational expansion
- explicit relevance to the wider patterns

### 2.5 “Wow” must be earned
The strongest “wow” moment is not an abstract futuristic visual. It is the moment a user feels:
- “this system sees my body as a whole”
- “it can explain what is strong as well as weak”
- “it can justify why it chose this lead”
- “it can teach me how my biomarkers connect to meaningful patterns”

That is why this recommendation prioritises explanation hierarchy over decorative novelty.

---

## 3. The most important strategic design choice

The single most important design choice is this:

**The product should not begin with biomarker data, but it must eventually deliver a biomarker experience that is richer than conventional blood-report UX.**

That means biomarkers are:
- **not the opening layer**
- **not the main narrative engine**
- **but absolutely still a high-value experience layer**

This is critical because it reconciles:
- the product’s systems-level differentiation
- with the user’s existing expectation of marker-by-marker inspection

The result is a journey where:
- the body story comes first
- the evidence comes later
- and the biomarker expansion experience itself becomes a second-tier “wow” layer through explanation depth

---

## 4. Recommended final results journey

---

### Section 1 — Your body overview

**Purpose:**  
Immediate whole-body orientation.

**What this section must answer:**  
- what the main area of strain is
- what appears stable
- whether the lead concern was clear or closely contested
- how HealthIQ is reading the body overall

**Why this comes first:**  
Users need a body-level frame before they can interpret any detailed content.

**Recommended UX character:**  
Calm, concise, orienting, confidence-building.

**Primary assets:**  
- `arbitration_result`
- `system_capacity_scores`
- primary concern fields from `clinician_report_v1.sections.page1`
- selected top-level report metadata

**What belongs here:**  
- a short body-level summary
- lead concern
- one-sentence framing that HealthIQ reads the body as interacting systems, not isolated markers
- light overview visual if it clarifies the system picture

**What does not belong here:**  
- biomarker grids
- long evidence blocks
- deep uncertainty copy
- clinician-style prose

---

### Section 2 — What’s working well

**Purpose:**  
Anchor the user in strengths and resilience before discussing what needs attention.

**What this section must answer:**  
- which systems appear stable or resilient
- what evidence supports that
- why this matters

**Why this comes second:**  
This is one of the strongest trust-building layers in the entire product. It proves the engine is not merely scanning for problems.

**Recommended UX character:**  
Grounded, reassuring, evidence-based, not sentimental.

**Primary assets:**  
- `balanced_systems_v1`
- selected burden/capacity evidence
- low-strain deterministic system facts
- optional system explainers where useful

**What belongs here:**  
- named stable systems
- brief evidence lines
- short capacity notes
- plain-language reassurance

**What does not belong here:**  
- false reassurance
- generic “all good” language
- anything unsupported by deterministic evidence

---

### Section 3 — Primary finding and why

**Purpose:**  
Deliver the lead interpretation with real explanatory depth.

**What this section must answer:**  
- what the lead pattern is
- what it means
- why it matters
- what supports it
- what complicates it

**Why this comes here:**  
Once the user is oriented and reassured where possible, the experience should move directly into the core reasoning moment.

**Recommended UX character:**  
Serious, educational, reasoned, non-alarmist.

**Primary assets:**  
- `clinician_report_v1.sections.page1.primary_concern`
- `top_hypothesis_line`
- `chains[]`
- `root_cause_v1`
- evidence-for / evidence-against / missing-data / confirmatory-tests
- selected compiler-mediated signal explanation snippets where available

**What belongs here:**  
- lead pattern statement
- top hypothesis line
- 1–2 chain narratives
- strongest evidence for
- strongest evidence against or complicating factor
- concise “why this matters” framing

**What does not belong here:**  
- full biomarker vault
- all findings at once
- raw explainability traces
- generic lifestyle content

**Important delivery qualification:**  
This section is highly buildable where root-cause and hypothesis coverage exists. Where the primary finding falls outside current root-cause coverage, the UX must gracefully fall back to:
- primary concern
- top findings
- chain narrative if available
- confidence/missing-data explanation
without pretending a full hypothesis layer exists.

---

### Section 4 — Why this lead won / uncertainty

**Purpose:**  
Build trust through transparency immediately after the lead finding.

**What this section must answer:**  
- what nearly became the lead
- why it did not
- how certain the engine is
- what data is missing
- what would change the conclusion

**Why this comes fourth rather than later:**  
Once the user sees the lead finding, their next natural question is: “How sure are you?”  
This is the right moment to answer it.

**Recommended UX character:**  
Intellectually honest, precise, calm, non-defensive.

**Primary assets:**  
- `runner_up_topic_line`
- `runner_up_why_not_lead_line`
- `confidence_and_missing_data`
- `data_quality.confidence_caveat`
- selected explainability/arbitration outputs, compiler-shaped for users
- missing-data logic from root cause / report structures

**What belongs here:**  
- confidence statement
- runner-up explanation
- missing-data note
- rationale for why the lead won

**What does not belong here:**  
- raw engine trace
- debug language
- scoring internals
- opaque technical wording

---

### Section 5 — Patterns across your body

**Purpose:**  
Show the structured interpretation layer that sits beneath the lead finding and above the biomarker evidence.

**What this section must answer:**  
- what the main patterns across the body are
- how they are named
- what each means in plain language
- what evidence family supports each

**Why this is the middle layer:**  
This is the bridge between body-level reasoning and marker-level truth.

**Recommended UX character:**  
Structured, medically meaningful, readable, high-value.

**Primary assets:**  
- current cluster/system outputs
- system explainers
- supporting biomarker summaries
- any governed phenotype-display layer where it exists

**Important delivery qualification:**  
This section is **partly grounded** in current repo reality and **partly aspirational**.

What appears real now:
- cluster/system layer
- system summaries
- supporting marker groupings
- system educational explainers where wired

What is not yet proven as a fully implementation-ready current asset:
- a mature, governed phenotype-display layer with consistent:
  - clinical display name
  - plain-English subtitle
  - why-it-matters line

So this section should be treated as:

**Phase-1 buildable using current system/cluster layer, with stronger naming and structure where possible**

and

**subject to an explicit existence check before a fuller phenotype-display contract is assumed**

**Required naming model where supported:**  
Each pattern should ideally use:
1. Clinical display name  
2. Plain-English subtitle  
3. Why-it-matters explainer  

**What belongs here:**  
- strong pattern names where available
- brief plain-English description
- why-it-matters line where contract support exists
- severity/status
- top supporting markers or signals
- optional system education on demand

**What does not belong here:**  
- generic health buckets
- weak labels like “Organ Health”
- raw internal ids
- undifferentiated cards with no explanation

---

### Section 6 — Marker-level evidence

**Purpose:**  
Deliver the familiar blood-report layer, but make it significantly richer than a conventional report.

**What this section must answer:**  
- what the biomarker is
- how the result sits relative to the range
- how it contributes to the wider pattern
- how the user can learn more
- why this biomarker matters in the context of the body story

**Why this comes after the reasoning journey:**  
The evidence is more meaningful once the user already understands the body frame and the main patterns.

**Recommended UX character:**  
Clear, premium, evidence-focused, educational on demand.

**Primary assets:**  
- `biomarkers[]`
- `contribution_context`
- `biomarker_educational_explainer`
- reference range data
- scores / interpretations

**Important strategic note:**  
This section is the point of parity with conventional blood-report experiences, but it should still become a point of differentiation through:
- better contribution-context surfacing
- stronger educational expansion
- clearer relationship to the identified pattern(s)

**Biomarker expansion should wow the user too.**  
A user who opens a biomarker should feel:
- this system knows what the marker is
- it can explain what the marker does
- it can explain why it matters for this user
- it can connect that marker to the wider pattern, not just define it generically

**What belongs here:**  
- current result
- reference range
- status
- short interpretation
- contribution context
- strong educational explainer expansion
- pattern relevance

**What does not belong here:**  
- biomarker grid as the main emotional centre of the page
- educational content without relevance framing
- generic explanation without linkage to the wider body story

---

### Section 7 — Key body-level insights

**Purpose:**  
Deliver the selective higher-order “wow” layer once the core story is already understood.

**What this section must answer:**  
- what broader derived insights the engine has found
- what those mean in a body-level sense
- why they are noteworthy

**Why this comes late rather than early:**  
These insights should feel earned and credible, not flashy or over-promoted.

**Recommended UX character:**  
High-value, surprising where warranted, tightly controlled.

**Primary assets:**  
- `layer_c_features`
- selected deterministic higher-order feature summaries
- only those robust enough for user-facing display

**Important runtime qualification:**  
This section is **not** dependent on Gemini if it is built from deterministic Layer C features.

However, if the delivery team expects richer **insight-card interpretation prose**, they must assume one of two tracks:
- enable and govern Gemini
- or improve the deterministic synthesiser

This paper recommends the section itself, but does **not** assume production Gemini is active.

**What belongs here:**  
- only robust, explainable features
- concise explanation
- clear relevance to the wider journey

**What does not belong here:**  
- gimmicky visuals
- unsupported composite scores
- too many feature cards
- “future-feeling” ideas that are not actually defendable

---

### Section 8 — What to do next

**Purpose:**  
Move the user from understanding to action.

**What this section must answer:**  
- what confirmatory tests could help
- what should be discussed with a clinician
- what monitoring or follow-up matters
- what the priority order is

**Recommended UX character:**  
Practical, prioritised, specific, non-generic.

**Primary assets:**  
- `confirmatory_tests[]`
- `actions`
- `next_steps[]`
- selected intervention or follow-up fields from report structures

**What belongs here:**  
- prioritised roadmap
- confirmatory test rationale
- follow-up logic
- clinician discussion cues

**What does not belong here:**  
- vague lifestyle advice
- generic wellness filler
- unprioritised lists

---

### Section 9 — Clinician summary

**Purpose:**  
Provide a professional handoff without contaminating the retail journey.

**Why this remains separate:**  
The retail user journey and the clinician handoff solve different problems. They should remain related, but distinct.

**Primary assets:**  
- full `ClinicianReportV1`

**Recommended UX character:**  
Structured, professional, exportable, separate from the core retail flow.

**What belongs here:**  
- full clinician summary
- clean lower-page or exportable section
- professional handoff logic

**What does not belong here:**  
- live mode-switch transformation of the whole page
- clinician detail injected throughout the retail flow

---

## 5. Recommended asset-to-UX mapping

| UX section | Main purpose | Primary text assets | Supporting assets | Delivery note |
|---|---|---|---|---|
| Your body overview | orientation | `primary_concern`, selected page1 summary fields | `arbitration_result`, `system_capacity_scores` | buildable now |
| What’s working well | reassurance | `balanced_systems_v1` | low-burden evidence, capacity notes | buildable now |
| Primary finding and why | explain the lead | `top_hypothesis_line`, `chains[]`, `root_cause_v1` | selected signal explanation snippets, confirmatory-test rationale | buildable with fallback where hypothesis coverage absent |
| Why this lead won / uncertainty | trust | `runner_up_topic_line`, `runner_up_why_not_lead_line`, `confidence_and_missing_data` | explainability/arbitration outputs, missing-data logic | buildable now if compiler surfaces fields |
| Patterns across your body | structured interpretation | current system/cluster naming; phenotype display layer where available | system explainers, supporting marker summaries | requires phenotype existence check before stronger contract assumed |
| Marker-level evidence | evidence depth + parity | `biomarkers[]`, contribution context, short interpretations | `biomarker_educational_explainer`, reference ranges, pattern relevance | buildable now |
| Key body-level insights | selective wow | deterministic `layer_c_features` summaries | selected derived metrics | buildable only where feature computation is robust; does not require Gemini by default |
| What to do next | action | confirmatory-test rationale, actions, `next_steps[]` | follow-up logic | buildable now |
| Clinician summary | handoff | full `ClinicianReportV1` | optional export metadata | buildable now |

---

## 6. How biomarkers should deliver both parity and differentiation

This deserves explicit treatment.

### 6.1 Point of parity
Users expect:
- to find their marker
- to see the value
- to understand range position
- to understand whether it looks normal, low, or high

HealthIQ must meet that expectation cleanly.

### 6.2 Point of differentiation
HealthIQ should then go further by using the assets already available to say:
- what that biomarker actually does biologically
- how it contributes to the user’s identified pattern
- why it matters in this wider body context
- how it connects to related markers or systems

### 6.3 Biomarker expansion rule
Every biomarker expansion should be structured as:

1. **What this result means now**  
   Short interpretation tied to this user’s actual result

2. **Why this marker matters**  
   Educational explainer content

3. **How it connects to your wider pattern**  
   Contribution context and pattern relevance

This is where the biomarker layer becomes a second-order wow experience rather than just a technical appendix.

### 6.4 Fallback rule
If richer educational or pattern-linking content is absent:
- still show value, range, status, and short interpretation
- omit missing deeper layers cleanly
- do not fabricate a richer explanation than the data supports

---

## 7. How signal-library explanation assets should be used

The signal packages in:
- `knowledge_bus/packages/**/signal_library.yaml`

contain some of the richest explanation-bearing assets in the system, including where authored:
- `explanation.mechanism`
- `explanation.biological_pathway`
- `explanation.interpretation`
- `explanation.implications`
- structured supporting metric roles / rationales

### Critical qualification
These fields are **not universally available across all biomarkers or all systems**.

They exist only where richer **knowledge-bus packages** have been authored. They do **not** exist generally in the core `biomarkers.yaml` SSOT.

So the correct delivery assumption is:

- use them where governed package coverage exists
- never assume universal availability
- always support a fallback compiler path when package-level explanation fields are absent

These should **not** be surfaced raw.

They should instead be used as governed source material for **compiler-mediated copy** that can support:
- pattern-level “why this matters” statements
- lead-finding significance framing
- system-group explanation snippets
- richer evidence summaries
- biomarker relevance framing

This approach protects:
- tone consistency
- length discipline
- version control
- user comprehension

---

## 8. Deterministic vs Gemini recommendation

The recommendation remains clear:

### Deterministic assets should form the narrative spine
The primary journey should be powered by:
- `clinician_report_v1`
- `root_cause_v1`
- `balanced_systems_v1`
- current system/cluster outputs
- explainability-derived rationales
- deterministic educational explainers
- compiler-mediated signal explanation excerpts where available

### Gemini should remain supplementary
Gemini can later help with:
- smoothing section summaries
- improving connective tissue
- optional polished summary layers

But Gemini should not be the authority for:
- clinical reasoning
- lead interpretation
- confidence
- prioritisation
- confirmatory tests
- core body story

### Current production reality
The delivery team should assume:
- production Gemini is not currently the default narrative spine
- sections depending on deterministic assets remain buildable
- richer prose in optional insight cards may remain thin unless Gemini is enabled or deterministic synthesis is improved

The wow factor should come from governed truth, not prose styling.

---

## 9. Design rules that should now be treated as locked

1. The page is a guided reasoning journey, not a report surface.  
2. Biomarkers do not lead the experience.  
3. Balanced systems are first-class, not supplementary.  
4. The lead finding must be explained, not merely stated.  
5. Uncertainty must be visible and user-readable.  
6. Pattern naming must be strong and three-layered where supported:
   - clinical display name
   - plain-English subtitle
   - why-it-matters line
7. Biomarker expansion should be rich enough to wow the user too.  
8. Signal-library explanation assets should be compiler-mediated, not pasted raw.  
9. Rich KB explanation fields must be treated as selective, not universal.  
10. Gemini is optional polish, not the product spine.  
11. Clinician handoff remains separate from the retail journey.

---

## 10. Content coverage and fallback rules

This section is included specifically to keep delivery honest.

### 10.1 If root-cause coverage is absent
Use:
- primary concern
- top findings
- chain narratives where available
- confidence/missing-data explanation

Do not pretend a full hypothesis layer exists.

### 10.2 If system explainer is absent
Keep the system/pattern card interpretive only.
Do not insert generic education filler.

### 10.3 If richer KB explanation text is absent
Use compiler-safe summary text only.
Do not imply that mechanism/pathway detail exists when it does not.

### 10.4 If Gemini remains off
The core journey remains valid.
Do not block delivery of the main sections.
Only optional polished narrative layers become thinner.

### 10.5 If Layer C feature support is uneven
Show only robust, explainable features.
Omit the rest cleanly.

---

## 11. Delivery dependencies and minimum viable scope

### Buildable now from current deterministic assets
- Your body overview
- What’s working well
- Primary finding and why (with fallback)
- Why this lead won / uncertainty
- Marker-level evidence
- What to do next
- Clinician summary

### Requires explicit existence/content check before stronger implementation assumptions
- full phenotype-display pattern layer
- universal three-layer pattern naming
- richer mechanism/pathway text at scale
- any section assuming broad KB explanation coverage

### Independent of Gemini being on
- overview
- reassurance
- primary finding
- uncertainty
- biomarkers
- next steps
- clinician summary
- deterministic Layer C features where truly available

### Becomes richer if Gemini is later enabled or improved
- connective prose
- optional insight-card interpretation language
- smoother summary transitions

---

## 12. Immediate practical recommendation to the delivery team

The next step is **not** more abstract ideation.

The next step is to turn this recommendation into a concrete section-by-section specification covering:

### A. Results page section specification
For each section:
- purpose
- key user question
- intro message
- show layer
- summary layer
- exact data assets
- expanded / hidden content
- fallback condition if richer content absent

### B. Pattern existence and naming check
Before fully speccing Section 5, verify:
- what current system/cluster layer already exists
- whether a governed phenotype-display layer exists
- what naming fields are already available versus needing new contract work

### C. Deterministic narrative spine specification
Define exactly which existing assets drive:
- body overview
- reassurance layer
- lead interpretation
- why / uncertainty
- pattern layer
- biomarker evidence
- action layer

### D. Biomarker expansion specification
Define exactly how each biomarker card uses:
- short interpretation
- educational explainer
- contribution context
- pattern relevance
- fallback if deeper layers absent

That is now the most practical way to move from discussion into delivery.

---

## 13. Final recommendation

HealthIQ should now move decisively from “results interface” thinking to **guided reasoning journey** thinking.

The strongest version of the product is one that:
- teaches the user how to understand their body without feeling tutorial-heavy
- reassures before alarming
- explains before overloading with evidence
- preserves biomarkers as a premium evidence layer
- uses deterministic assets more boldly
- links marker-level truth back to system-level understanding
- reserves clinician content for a distinct lower section
- treats the best existing assets as a disciplined narrative system rather than as scattered text

If this is executed well, the user should leave the results page feeling:

- I understand my body at a whole-system level  
- I know what appears strong and what needs attention  
- I understand why the engine concluded this  
- I can inspect my biomarker evidence without losing the bigger picture  
- I learned something genuinely new about how my biology works  

That is the standard the front end should now be built to meet.
